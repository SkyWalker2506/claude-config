#!/usr/bin/env python3
"""Scan knowledge frontmatter for `sources: N` (mega-prompt depth hint).

Writes agents/KNOWLEDGE_SOURCES_AUDIT.md — informational; does not gate CI by default.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
OUT = AGENTS / "KNOWLEDGE_SOURCES_AUDIT.md"

FM_BOUNDARY = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)
SOURCES_LINE = re.compile(r"^sources:\s*(\d+)\s*$", re.MULTILINE)


def parse_sources(body: str) -> int | None:
    m = FM_BOUNDARY.search(body)
    if not m:
        return None
    fm = m.group(1)
    sm = SOURCES_LINE.search(fm)
    if not sm:
        return None
    return int(sm.group(1))


def main() -> None:
    rows: list[tuple[str, int | None]] = []
    for p in sorted(AGENTS.rglob("knowledge/*.md")):
        if "_template" in str(p) or p.name == "_index.md":
            continue
        body = p.read_text(encoding="utf-8", errors="replace")
        rel = str(p.relative_to(AGENTS))
        rows.append((rel, parse_sources(body)))

    total = len(rows)
    with_val = [r for r in rows if r[1] is not None]
    missing_key = [r for r in rows if r[1] is None]
    ge3 = [r for r in with_val if r[1] is not None and r[1] >= 3]

    lines = [
        "# Knowledge sources audit (frontmatter)",
        "",
        f"- **Generated:** `python3 scripts/knowledge_sources_audit.py`",
        f"- **Scanned:** {total} topic files",
        "",
        "Mega-prompt hedefi: `sources: 3+` (frontmatter). Bu rapor **bilgi amaçlı** — yapısal gate `verify_knowledge_structure.py`.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|------:|",
        f"| Topic files | {total} |",
        f"| `sources:` present | {len(with_val)} |",
        f"| `sources:` missing | {len(missing_key)} |",
        f"| `sources` ≥ 3 | {len(ge3)} |",
        "",
    ]
    if missing_key:
        lines += ["## Missing `sources:` in frontmatter", ""]
        for rel, _ in sorted(missing_key)[:80]:
            lines.append(f"- `{rel}`")
        if len(missing_key) > 80:
            lines.append(f"- _… and {len(missing_key) - 80} more_")
        lines.append("")

    lines += [
        "## Distribution (where `sources:` is set)",
        "",
        "| sources | Files |",
        "|---------|------:|",
    ]
    buckets: dict[int, int] = {}
    for _, n in with_val:
        if n is None:
            continue
        buckets[n] = buckets.get(n, 0) + 1
    for k in sorted(buckets.keys()):
        lines.append(f"| {k} | {buckets[k]} |")
    lines.append("")

    report = "\n".join(lines)
    if not os.environ.get("CLAUDE_VERIFY_AUDIT"):
        OUT.write_text(report, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}  sources≥3={len(ge3)}/{total}  missing_field={len(missing_key)}")


if __name__ == "__main__":
    main()
