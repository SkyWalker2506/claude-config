#!/usr/bin/env python3
"""
PreToolUse hook: intercept `git commit` and `git push` Bash commands,
run configured gates, and optionally block the command.

Behavior:
  - Reads hook input from stdin (Claude Code PreToolUse protocol)
  - Matches tool_name == "Bash" with a command containing git commit/push
  - Loads config/gates/pre-{commit,push}.json
  - For each gate: runs command, compares against expect_empty/exit code
  - If a blocking gate fails -> exit 2 with stderr message (blocks tool)
  - Non-blocking gate failures print warnings to stderr but allow
  - Mode "warn" (default) downgrades all blocking gates to warnings

Never fails on infra errors — swallows and allows.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def find_base() -> Path:
    env_base = os.environ.get("CLAUDE_CONFIG_ROOT")
    if env_base and Path(env_base).exists():
        return Path(env_base)
    here = Path(__file__).resolve().parent.parent
    if (here / "config" / "agent-registry.json").exists():
        return here
    return Path.home() / "Projects" / "claude-config"


def allow() -> None:
    sys.exit(0)


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def run_gate(gate: dict) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            gate["command"], shell=True,
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return False, "timeout after 120s"
    except Exception as exc:
        return False, f"gate runner error: {exc}"

    expect_empty = gate.get("expect_empty", False)
    if expect_empty:
        if result.stdout.strip():
            return False, result.stdout.strip()[:400]
        return True, ""
    if result.returncode != 0:
        return False, (result.stderr.strip() or result.stdout.strip())[:400]
    return True, ""


def main() -> None:
    try:
        raw = sys.stdin.read()
        hook_input = json.loads(raw) if raw.strip() else {}
    except Exception:
        allow()

    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Bash":
        allow()

    tool_input = hook_input.get("tool_input") or {}
    command = tool_input.get("command", "") or ""

    is_commit = "git commit" in command
    is_push = "git push" in command
    if not (is_commit or is_push):
        allow()

    base = find_base()
    gate_file = "pre-push.json" if is_push else "pre-commit.json"
    gate_path = base / "config" / "gates" / gate_file

    if not gate_path.exists():
        allow()

    try:
        cfg = json.loads(gate_path.read_text())
    except Exception:
        allow()

    mode = cfg.get("mode", "warn")
    gates = cfg.get("gates", [])
    warnings: list[str] = []
    failures: list[str] = []

    for gate in gates:
        name = gate.get("name", "unnamed")
        ok, detail = run_gate(gate)
        if ok:
            continue
        msg = f"[{name}] {gate.get('description', '')}\n{detail}"
        if gate.get("blocking") and mode == "enforce":
            failures.append(msg)
        else:
            warnings.append(msg)

    if warnings:
        sys.stderr.write("\n[gate warnings]\n" + "\n".join(warnings) + "\n")

    if failures:
        block(
            "VERIFICATION GATES FAILED (enforce mode):\n"
            + "\n".join(failures)
            + "\n\nTo disable: set 'mode': 'warn' in config/gates/pre-*.json"
        )

    allow()


if __name__ == "__main__":
    main()
