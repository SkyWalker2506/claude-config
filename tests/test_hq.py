"""
Integration tests for hq tooling.

Each test creates an isolated CLAUDE_CONFIG_ROOT pointing at a tempdir
populated with a synthetic agent-registry.json and event log, then runs
the script under test as a subprocess. Tests do not depend on the real
~/Projects/claude-config layout and can run in CI sandboxes.

Run: python3 -m unittest tests/test_hq.py -v
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


def make_registry(extra: dict | None = None) -> dict:
    base = {
        "version": "1.0",
        "agents": {
            "A1": {"name": "Lead Orchestrator", "category": "orchestrator",
                   "status": "active", "primary_model": "opus"},
            "B2": {"name": "Backend Coder", "category": "backend",
                   "status": "active", "primary_model": "sonnet"},
            "B7": {"name": "Bug Hunter", "category": "backend",
                   "status": "active", "primary_model": "sonnet"},
            "C3": {"name": "Local AI Reviewer", "category": "code-review",
                   "status": "active", "primary_model": "haiku"},
            "Z9": {"name": "Dormant Agent", "category": "research",
                   "status": "pool", "primary_model": "sonnet"},
            "Z10": {"name": "Rising Star", "category": "backend",
                    "status": "pool", "primary_model": "sonnet"},
        },
    }
    if extra:
        base["agents"].update(extra)
    return base


def make_event(
    agent_id: str = "B2",
    agent_name: str = "Backend Coder",
    category: str = "backend",
    model: str = "sonnet",
    outcome: str = "success",
    days_ago: int = 0,
    duration: float = 1.0,
) -> dict:
    ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": ts.isoformat(),
        "agent_id": agent_id,
        "agent_name": agent_name,
        "category": category,
        "model_used": model,
        "model_tier": "standard" if "sonnet" in model else "premium",
        "project": "test-project",
        "task_type": "Task",
        "outcome": outcome,
        "duration_seconds": duration,
        "fallback_used": False,
        "fallback_chain": [],
    }


class HQTestBase(unittest.TestCase):
    """Sets up an isolated CLAUDE_CONFIG_ROOT in a tempdir."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="hq-test-"))
        (self.tmp / "config").mkdir()
        (self.tmp / "config" / "telemetry" / "events").mkdir(parents=True)
        (self.tmp / "config" / "telemetry" / "aggregated").mkdir(parents=True)
        (self.tmp / "Reports").mkdir()
        (self.tmp / "agents").mkdir()
        # Default registry
        self.write_registry(make_registry())

        self.env = os.environ.copy()
        self.env["CLAUDE_CONFIG_ROOT"] = str(self.tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_registry(self, data: dict) -> None:
        (self.tmp / "config" / "agent-registry.json").write_text(json.dumps(data))

    def write_events(self, events: list[dict]) -> None:
        # Group by date
        by_day: dict[str, list[dict]] = {}
        for ev in events:
            day = ev["timestamp"][:10]
            by_day.setdefault(day, []).append(ev)
        for day, evs in by_day.items():
            with (self.tmp / "config" / "telemetry" / "events" / f"{day}.jsonl").open("a") as f:
                for ev in evs:
                    f.write(json.dumps(ev) + "\n")

    def run_script(self, name: str, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args],
            env=self.env,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def run_hq(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(SCRIPTS / "hq"), *args],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=30,
        )


# ---------- log_dispatch.py ----------

class LogDispatchTests(HQTestBase):

    def _read_events(self) -> list[dict]:
        events = []
        for f in (self.tmp / "config" / "telemetry" / "events").glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        return events

    def test_extracts_agent_from_dispatch_header(self) -> None:
        hook_input = {
            "tool_name": "Task",
            "tool_input": {
                "description": "test",
                "prompt": "AGENT: B2 — Backend Coder\nROLE: implement\nTASK: test",
            },
            "tool_response": {"is_error": False},
        }
        result = self.run_script("log_dispatch.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)

        events = self._read_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["agent_id"], "B2")
        self.assertEqual(events[0]["agent_name"], "Backend Coder")
        self.assertEqual(events[0]["category"], "backend")
        self.assertEqual(events[0]["outcome"], "success")

    def test_unknown_agent_when_no_header(self) -> None:
        hook_input = {
            "tool_name": "Bash",
            "tool_input": {"command": "ls"},
            "tool_response": {"is_error": False},
        }
        result = self.run_script("log_dispatch.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)
        events = self._read_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["agent_id"], "unknown")
        self.assertEqual(events[0]["task_type"], "Bash")

    def test_failed_outcome_detection(self) -> None:
        hook_input = {
            "tool_name": "Task",
            "tool_input": {"prompt": "AGENT: B7 — Bug Hunter"},
            "tool_response": {"is_error": True, "error": "boom"},
        }
        self.run_script("log_dispatch.py", stdin=json.dumps(hook_input))
        events = self._read_events()
        self.assertEqual(events[0]["outcome"], "failed")
        self.assertEqual(events[0]["agent_id"], "B7")

    def test_malformed_input_does_not_crash(self) -> None:
        result = self.run_script("log_dispatch.py", stdin="not json at all {{{")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self._read_events(), [])

    def test_empty_stdin_no_op(self) -> None:
        result = self.run_script("log_dispatch.py", stdin="")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self._read_events(), [])


# ---------- hq_dashboard.py ----------

class DashboardTests(HQTestBase):

    def _dashboard_json(self) -> dict:
        return json.loads((self.tmp / "config" / "telemetry" / "aggregated" / "dashboard.json").read_text())

    def test_empty_events_unknown_status(self) -> None:
        result = self.run_script("hq_dashboard.py")
        self.assertEqual(result.returncode, 0)
        d = self._dashboard_json()
        self.assertEqual(d["system_health"]["status"], "unknown")
        self.assertEqual(d["system_health"]["total_dispatches"], 0)
        # Registry: 6 agents, 4 active, 2 pool
        self.assertEqual(d["agents"]["registered"], 6)
        self.assertEqual(d["agents"]["active"], 4)
        self.assertEqual(d["agents"]["pool"], 2)

    def test_healthy_status_with_high_success_rate(self) -> None:
        events = [make_event(outcome="success") for _ in range(8)] + [
            make_event(outcome="failed")
        ]
        self.write_events(events)
        self.run_script("hq_dashboard.py")
        d = self._dashboard_json()
        self.assertEqual(d["system_health"]["status"], "healthy")
        self.assertGreaterEqual(d["system_health"]["success_rate"], 0.8)
        self.assertEqual(d["system_health"]["total_dispatches"], 9)

    def test_critical_status_with_low_success_rate(self) -> None:
        events = [make_event(outcome="success")] + [
            make_event(outcome="failed") for _ in range(9)
        ]
        self.write_events(events)
        self.run_script("hq_dashboard.py")
        d = self._dashboard_json()
        self.assertEqual(d["system_health"]["status"], "critical")

    def test_top_agents_ranking(self) -> None:
        events = (
            [make_event(agent_id="B2") for _ in range(5)]
            + [make_event(agent_id="B7") for _ in range(2)]
            + [make_event(agent_id="C3")]
        )
        self.write_events(events)
        self.run_script("hq_dashboard.py")
        d = self._dashboard_json()
        top = d["agents"]["top_10"]
        self.assertEqual(top[0]["id"], "B2")
        self.assertEqual(top[0]["dispatches"], 5)
        self.assertEqual(top[1]["id"], "B7")

    def test_never_used_active_excludes_used(self) -> None:
        self.write_events([make_event(agent_id="B2") for _ in range(3)])
        self.run_script("hq_dashboard.py")
        d = self._dashboard_json()
        self.assertNotIn("B2", d["agents"]["never_used_active"])
        self.assertIn("B7", d["agents"]["never_used_active"])

    def test_unknown_agent_id_does_not_count_as_dispatch(self) -> None:
        self.write_events([make_event(agent_id="unknown") for _ in range(5)])
        self.run_script("hq_dashboard.py")
        d = self._dashboard_json()
        # total_dispatches counts everything, but used_last_30d filters unknowns
        self.assertEqual(d["agents"]["used_last_30d"], 0)
        self.assertEqual(d["system_health"]["total_dispatches"], 5)

    def test_json_flag_outputs_pure_json(self) -> None:
        self.write_events([make_event()])
        result = self.run_script("hq_dashboard.py", "--json")
        self.assertEqual(result.returncode, 0)
        # First non-empty line of stdout must be valid JSON
        parsed = json.loads(result.stdout)
        self.assertIn("system_health", parsed)

    def test_corrupted_event_line_skipped(self) -> None:
        # Write one good event + one garbage line in same file
        events = [make_event()]
        good = json.dumps(events[0])
        path = self.tmp / "config" / "telemetry" / "events" / "test.jsonl"
        path.write_text(good + "\nthis is not json\n" + good + "\n")
        result = self.run_script("hq_dashboard.py")
        self.assertEqual(result.returncode, 0)
        d = self._dashboard_json()
        self.assertEqual(d["system_health"]["total_dispatches"], 2)


# ---------- agent_lifecycle.py ----------

class LifecycleTests(HQTestBase):

    def _recs(self) -> list[dict]:
        path = self.tmp / "Reports" / "lifecycle_recommendations.json"
        if not path.exists():
            return []
        return json.loads(path.read_text())

    def test_insufficient_samples_no_recommendations(self) -> None:
        self.write_events([make_event() for _ in range(5)])
        result = self.run_script("agent_lifecycle.py")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self._recs(), [])

    def test_force_flag_runs_with_low_data(self) -> None:
        self.write_events([make_event(agent_id="B2") for _ in range(5)])
        result = self.run_script("agent_lifecycle.py", "--force")
        self.assertEqual(result.returncode, 0)
        recs = self._recs()
        # B2 used → not flagged. B7, A1, C3 active+unused → demote
        demote_ids = [r["agent_id"] for r in recs if r["recommended"] == "pool"]
        self.assertIn("B7", demote_ids)
        self.assertIn("A1", demote_ids)
        self.assertNotIn("B2", demote_ids)

    def test_promote_pool_with_5_dispatches_in_30d(self) -> None:
        events = [make_event(agent_id="Z10", category="backend") for _ in range(20)] + [
            make_event(agent_id="Z10", category="backend", days_ago=5) for _ in range(6)
        ]
        self.write_events(events)
        self.run_script("agent_lifecycle.py")
        recs = self._recs()
        promote = [r for r in recs if r["recommended"] == "active"]
        self.assertTrue(any(r["agent_id"] == "Z10" for r in promote))

    def test_retire_candidate_for_unused_pool(self) -> None:
        # 25 dispatches all on B2 → enough to pass MIN_SAMPLE,
        # Z9 (pool) is never touched → retire candidate
        self.write_events([make_event(agent_id="B2") for _ in range(25)])
        self.run_script("agent_lifecycle.py")
        recs = self._recs()
        retire_ids = [r["agent_id"] for r in recs if r["recommended"] == "retire_candidate"]
        self.assertIn("Z9", retire_ids)


# ---------- route_optimizer.py ----------

class RouteOptimizerTests(HQTestBase):

    def _recs(self) -> list[dict]:
        path = self.tmp / "Reports" / "routing_recommendations.json"
        if not path.exists():
            return []
        return json.loads(path.read_text())

    def test_no_data_no_recommendations(self) -> None:
        result = self.run_script("route_optimizer.py")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self._recs(), [])

    def test_recommends_cheaper_when_alt_matches_success_rate(self) -> None:
        # B2's primary_model is sonnet. Build history showing haiku
        # achieves the same success rate at lower cost.
        events = [make_event(agent_id="B2", model="sonnet", outcome="success") for _ in range(10)] + [
            make_event(agent_id="B2", model="haiku", outcome="success") for _ in range(10)
        ]
        self.write_events(events)
        self.run_script("route_optimizer.py")
        recs = self._recs()
        b2_recs = [r for r in recs if r["agent_id"] == "B2"]
        self.assertTrue(b2_recs, "Expected at least one recommendation for B2")
        rec = b2_recs[0]
        self.assertIn("haiku", rec["recommended_model"])
        self.assertGreater(rec["cost_savings_pct"], 0)

    def test_no_recommendation_when_alt_is_worse(self) -> None:
        events = [make_event(agent_id="B2", model="sonnet", outcome="success") for _ in range(10)] + [
            make_event(agent_id="B2", model="haiku", outcome="failed") for _ in range(10)
        ]
        self.write_events(events)
        self.run_script("route_optimizer.py")
        recs = self._recs()
        self.assertEqual([r for r in recs if r["agent_id"] == "B2"], [])

    def test_skips_low_sample_alternatives(self) -> None:
        events = [make_event(agent_id="B2", model="sonnet", outcome="success") for _ in range(10)] + [
            make_event(agent_id="B2", model="haiku", outcome="success") for _ in range(3)  # < 5
        ]
        self.write_events(events)
        self.run_script("route_optimizer.py")
        recs = self._recs()
        self.assertEqual([r for r in recs if r["agent_id"] == "B2"], [])


# ---------- plugin_eval.py ----------

class PluginEvalTests(HQTestBase):

    def _make_plugin(self, name: str, *, with_readme=True, with_skill=True,
                     with_commands=True, with_tests=True, with_hardcoded=False,
                     description="A useful plugin that does many helpful things for users.") -> Path:
        plug_root = self.tmp / "plugins-root"
        plug_root.mkdir(exist_ok=True)
        p = plug_root / name
        p.mkdir()
        if with_readme:
            (p / "README.md").write_text("# Plugin")
        if with_skill:
            (p / "skills").mkdir()
            (p / "skills" / "my-skill").mkdir()
            (p / "skills" / "my-skill" / "SKILL.md").write_text("# Skill")
        if with_commands:
            (p / "commands").mkdir()
            (p / "commands" / "do.md").write_text("# do")
        if with_tests:
            (p / "tests").mkdir()
            (p / "tests" / "test_plugin.py").write_text("def test(): pass")
        (p / ".claude-plugin").mkdir()
        (p / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": name, "description": description})
        )
        if with_hardcoded:
            (p / "install.sh").write_text("#!/bin/bash\ncp foo /Users/musab/x")
        else:
            (p / "install.sh").write_text("#!/bin/bash\necho ok")
        # git init for commit recency check (disable signing/hooks for sandboxes)
        git_env = os.environ.copy()
        git_env["GIT_CONFIG_GLOBAL"] = "/dev/null"
        git_env["GIT_CONFIG_SYSTEM"] = "/dev/null"
        common = ["git", "-c", "user.email=t@t", "-c", "user.name=t",
                  "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]
        subprocess.run(["git", "init", "-q"], cwd=p, env=git_env,
                       check=False, capture_output=True)
        subprocess.run(common + ["add", "."], cwd=p, env=git_env,
                       check=False, capture_output=True)
        subprocess.run(common + ["commit", "-q", "--no-verify", "-m", "init"],
                       cwd=p, env=git_env, check=False, capture_output=True)
        return p

    def test_perfect_plugin_grades_a(self) -> None:
        self._make_plugin("ccplugin-good")
        env = self.env.copy()
        env["CLAUDE_PLUGINS_ROOT"] = str(self.tmp / "plugins-root")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "plugin_eval.py")],
            env=env, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        report = json.loads((self.tmp / "Reports" / "plugin_quality.json").read_text())
        self.assertIn("ccplugin-good", report)
        self.assertEqual(report["ccplugin-good"]["grade"], "A")

    def test_minimal_plugin_grades_low(self) -> None:
        self._make_plugin(
            "ccplugin-bad",
            with_readme=False, with_skill=False, with_commands=False,
            with_tests=False, description="x",
        )
        env = self.env.copy()
        env["CLAUDE_PLUGINS_ROOT"] = str(self.tmp / "plugins-root")
        subprocess.run(
            [sys.executable, str(SCRIPTS / "plugin_eval.py")],
            env=env, capture_output=True, text=True, timeout=30,
        )
        report = json.loads((self.tmp / "Reports" / "plugin_quality.json").read_text())
        # Only commit_recency (1) + no_hardcoded_paths (2) = 3 → D
        self.assertIn(report["ccplugin-bad"]["grade"], ["D", "F"])

    def test_hardcoded_paths_penalized(self) -> None:
        self._make_plugin("ccplugin-hardcoded", with_hardcoded=True)
        env = self.env.copy()
        env["CLAUDE_PLUGINS_ROOT"] = str(self.tmp / "plugins-root")
        subprocess.run(
            [sys.executable, str(SCRIPTS / "plugin_eval.py")],
            env=env, capture_output=True, text=True, timeout=30,
        )
        report = json.loads((self.tmp / "Reports" / "plugin_quality.json").read_text())
        self.assertFalse(report["ccplugin-hardcoded"]["checks"]["no_hardcoded_paths"])


# ---------- gate_check.py ----------

class GateCheckTests(HQTestBase):

    def _gate_dir(self) -> Path:
        d = self.tmp / "config" / "gates"
        d.mkdir(exist_ok=True)
        return d

    def test_non_git_command_passes(self) -> None:
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "ls"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)

    def test_non_bash_tool_passes(self) -> None:
        hook_input = {"tool_name": "Edit", "tool_input": {"file_path": "/tmp/x"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)

    def test_warn_mode_does_not_block(self) -> None:
        cfg = {
            "mode": "warn",
            "gates": [
                {"name": "always_fail", "command": "exit 1", "blocking": True},
            ],
        }
        (self._gate_dir() / "pre-commit.json").write_text(json.dumps(cfg))
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)
        self.assertIn("always_fail", result.stderr)

    def test_enforce_mode_blocks_failing_gate(self) -> None:
        cfg = {
            "mode": "enforce",
            "gates": [
                {"name": "always_fail", "command": "exit 1", "blocking": True},
            ],
        }
        (self._gate_dir() / "pre-commit.json").write_text(json.dumps(cfg))
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 2)
        self.assertIn("always_fail", result.stderr)

    def test_enforce_mode_allows_passing_gate(self) -> None:
        cfg = {
            "mode": "enforce",
            "gates": [
                {"name": "always_pass", "command": "true", "blocking": True},
            ],
        }
        (self._gate_dir() / "pre-commit.json").write_text(json.dumps(cfg))
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)

    def test_expect_empty_blocks_when_output_present(self) -> None:
        cfg = {
            "mode": "enforce",
            "gates": [
                {"name": "leak", "command": "echo SECRET",
                 "expect_empty": True, "blocking": True},
            ],
        }
        (self._gate_dir() / "pre-push.json").write_text(json.dumps(cfg))
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "git push origin"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 2)
        self.assertIn("leak", result.stderr)

    def test_missing_gate_command_skipped_safely(self) -> None:
        cfg = {"mode": "enforce", "gates": [{"name": "broken", "blocking": True}]}
        (self._gate_dir() / "pre-commit.json").write_text(json.dumps(cfg))
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)

    def test_missing_gate_file_passes(self) -> None:
        hook_input = {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}
        result = self.run_script("gate_check.py", stdin=json.dumps(hook_input))
        self.assertEqual(result.returncode, 0)


# ---------- hq CLI ----------

class HQCLITests(HQTestBase):

    def test_help_subcommand(self) -> None:
        result = self.run_hq("help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("dashboard", result.stdout)
        self.assertIn("lifecycle", result.stdout)
        self.assertIn("plugin-eval", result.stdout)

    def test_unknown_command_exits_nonzero(self) -> None:
        result = self.run_hq("nonexistent")
        self.assertNotEqual(result.returncode, 0)

    def test_dashboard_subcommand_runs(self) -> None:
        result = self.run_hq("dashboard")
        self.assertEqual(result.returncode, 0)

    def test_dashboard_json_pipe(self) -> None:
        result = self.run_hq("dashboard", "--json")
        self.assertEqual(result.returncode, 0)
        json.loads(result.stdout)  # must be valid JSON

    def test_lifecycle_subcommand_runs(self) -> None:
        result = self.run_hq("lifecycle")
        self.assertEqual(result.returncode, 0)

    def test_optimize_subcommand_runs(self) -> None:
        result = self.run_hq("optimize")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
