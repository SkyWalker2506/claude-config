#!/usr/bin/env python3
"""Scan knowledge/*.md (except _index.md) for mega-prompt section headers.

Writes agents/KNOWLEDGE_QUALITY_AUDIT.md with counts and file lists per missing section.
"""
from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
OUT = AGENTS / "KNOWLEDGE_QUALITY_AUDIT.md"

SECTIONS = [
    "Quick Reference",
    "Patterns & Decision Matrix",
    "Code Examples",
    "Anti-Patterns",
    "Deep Dive Sources",
]

# Alternate headings still counted (older or shortened variants)
ALIASES: dict[str, tuple[str, ...]] = {
    "Patterns & Decision Matrix": ("## Patterns & Decision Matrix", "## Patterns"),
    "Code Examples": ("## Code Examples", "## Example"),
}


def file_has_section(body: str, section: str) -> bool:
    if section in ALIASES:
        for line in body.splitlines():
            s = line.strip()
            for alt in ALIASES[section]:
                if s.startswith(alt):
                    return True
    needle = f"## {section}"
    for line in body.splitlines():
        if line.strip().startswith(needle):
            return True
    return False


def main() -> None:
    missing: dict[str, list[str]] = defaultdict(list)
    all_paths: list[Path] = []
    for p in sorted(AGENTS.rglob("knowledge/*.md")):
        if "_template" in str(p):
            continue
        if p.name == "_index.md":
            continue
        all_paths.append(p)
        body = p.read_text(encoding="utf-8", errors="replace")
        rel = str(p.relative_to(AGENTS))
        for sec in SECTIONS:
            if not file_has_section(body, sec):
                missing[sec].append(rel)

    total = len(all_paths)
    lines = [
        "# Knowledge quality audit (mega-prompt sections)",
        "",
        f"- **Generated:** `python3 scripts/knowledge_quality_audit.py`",
        f"- **Scanned:** {total} topic files (`knowledge/*.md`, excluding `_index.md`)",
        "",
        "Expected sections (see `cursor-prompts/mega-prompt.md`):",
        "",
        "| Section | Present | Missing |",
        "|---------|--------:|--------:|",
    ]
    for sec in SECTIONS:
        m = len(missing[sec])
        lines.append(f"| {sec} | {total - m} | {m} |")
    complete = sum(
        1
        for p in all_paths
        if not any(
            str(p.relative_to(AGENTS)) in missing[sec] for sec in SECTIONS
        )
    )
    lines += [
        "",
        f"- **Files with all 5 sections:** {complete} / {total}",
        "",
        "## Missing by section",
        "",
    ]
    for sec in SECTIONS:
        files = sorted(missing[sec])
        lines.append(f"### {sec} ({len(files)})")
        lines.append("")
        for f in files:
            lines.append(f"- `{f}`")
        lines.append("")

    report = "\n".join(lines)
    if not os.environ.get("CLAUDE_VERIFY_AUDIT"):
        OUT.write_text(report, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}  complete={complete}/{total}")


if __name__ == "__main__":
    main()
