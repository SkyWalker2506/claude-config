#!/usr/bin/env python3
"""
Plugin quality evaluator.

Scans ~/Projects/ccplugin-* (or $CLAUDE_PLUGINS_ROOT) and grades each on:
  has_readme (1), has_skill_md (2), has_commands (2),
  description_length (1), has_tests (2), commit_recency_days (1),
  no_hardcoded_paths (2)

Max score: 11. Grades: A>=10 B>=8 C>=6 D>=3 F<3.
Writes Reports/plugin_quality.json.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path


def find_base() -> Path:
    env_base = os.environ.get("CLAUDE_CONFIG_ROOT")
    if env_base and Path(env_base).exists():
        return Path(env_base)
    here = Path(__file__).resolve().parent.parent
    if (here / "config" / "agent-registry.json").exists():
        return here
    return Path.home() / "Projects" / "claude-config"


BASE = find_base()


def plugin_roots() -> list[Path]:
    env = os.environ.get("CLAUDE_PLUGINS_ROOT")
    candidates: list[Path] = []
    if env:
        candidates.append(Path(env))
    candidates.append(Path.home() / "Projects")
    # Sibling of claude-config
    candidates.append(BASE.parent)

    seen: set[Path] = set()
    results: list[Path] = []
    for root in candidates:
        if not root.exists():
            continue
        if root in seen:
            continue
        seen.add(root)
        for p in sorted(root.glob("ccplugin-*")):
            if p.is_dir() and p not in results:
                results.append(p)
    return results


def eval_plugin(path: Path) -> dict:
    score = 0
    checks: dict = {}

    has_readme = (path / "README.md").exists()
    checks["has_readme"] = has_readme
    score += 1 if has_readme else 0

    skills = list(path.rglob("SKILL.md"))
    has_skill = len(skills) > 0
    checks["has_skill_md"] = has_skill
    score += 2 if has_skill else 0

    cmd_dir = path / "commands"
    has_commands = cmd_dir.exists() and any(cmd_dir.iterdir())
    checks["has_commands"] = bool(has_commands)
    score += 2 if has_commands else 0

    plugin_json = path / ".claude-plugin" / "plugin.json"
    desc_len = 0
    if plugin_json.exists():
        try:
            pj = json.loads(plugin_json.read_text())
            desc_len = len(pj.get("description", ""))
        except Exception:
            pass
    checks["description_length"] = desc_len
    if 50 <= desc_len <= 250:
        score += 1

    has_tests = any(path.rglob("*test*")) or any(path.rglob("*spec*"))
    checks["has_tests"] = bool(has_tests)
    score += 2 if has_tests else 0

    # commit recency
    days = 999
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            cwd=path, capture_output=True, text=True, timeout=5,
        )
        stamp = result.stdout.strip()
        if stamp:
            days = int((time.time() - int(stamp)) / 86400)
    except Exception:
        pass
    checks["commit_recency_days"] = days
    if days <= 90:
        score += 1

    # hardcoded paths
    has_hardcoded = False
    for f in list(path.rglob("*.sh"))[:50]:
        try:
            content = f.read_text(errors="ignore")
            if "/Users/" in content or "/home/" in content:
                has_hardcoded = True
                break
        except Exception:
            continue
    checks["no_hardcoded_paths"] = not has_hardcoded
    score += 2 if not has_hardcoded else 0

    grade = "F"
    for g, threshold in (("A", 10), ("B", 8), ("C", 6), ("D", 3)):
        if score >= threshold:
            grade = g
            break

    return {"score": score, "max": 11, "grade": grade, "checks": checks}


def main() -> None:
    plugins = plugin_roots()

    if not plugins:
        print("No ccplugin-* directories found.")
        print("Set CLAUDE_PLUGINS_ROOT or ensure ~/Projects/ccplugin-* exists.")
        return

    results: dict[str, dict] = {}
    for p in plugins:
        results[p.name] = eval_plugin(p)

    print()
    print("Plugin Quality Report")
    print("=" * 60)
    print(f"{'Plugin':<38} {'Grade':>6} {'Score':>8}")
    print("-" * 60)
    for name, r in sorted(results.items(), key=lambda x: -x[1]["score"]):
        print(f"  {name:<36} {r['grade']:>6} {r['score']:>3}/{r['max']}")

    out_dir = BASE / "Reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "plugin_quality.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nReport -> Reports/plugin_quality.json")


if __name__ == "__main__":
    main()
