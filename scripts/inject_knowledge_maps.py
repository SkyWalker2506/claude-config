#!/usr/bin/env python3
"""Insert ## Knowledge map tables into AGENT.md for agents that pass coverage but lack the section.

Reads topic titles from the first Markdown H1 in each knowledge/*.md file (excluding _index.md),
falls back to a humanized filename. Inserts the block immediately before ## Knowledge Index.

Usage:
  python3 scripts/inject_knowledge_maps.py           # apply
  python3 scripts/inject_knowledge_maps.py --dry-run # print counts only
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
ANCHOR = "## Knowledge Index"
MAP_HEADER = "## Knowledge map"


def first_h1_title(md_path: Path) -> str | None:
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines()[:40]:
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m:
            return m.group(1).strip()
    return None


def humanize_stem(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ").strip().title()


def build_map_block(knowledge_dir: Path) -> str | None:
    files = sorted(
        p for p in knowledge_dir.glob("*.md") if p.name != "_index.md"
    )
    if not files:
        return None
    rows: list[str] = [
        MAP_HEADER,
        "",
        "| # | Topic | File |",
        "|---|-------|------|",
    ]
    for i, p in enumerate(files, start=1):
        title = first_h1_title(p) or humanize_stem(p.stem)
        rel = f"knowledge/{p.name}"
        rows.append(f"| {i} | {title} | `{rel}` |")
    rows.append("")
    return "\n".join(rows)


def inject_one(agent_md: Path, dry_run: bool) -> bool:
    folder = agent_md.parent
    kid = folder / "knowledge"
    if not kid.is_dir():
        return False
    body = agent_md.read_text(encoding="utf-8", errors="replace")
    if MAP_HEADER in body:
        return False
    if ANCHOR not in body:
        print(f"skip (no anchor): {agent_md.relative_to(ROOT)}", file=sys.stderr)
        return False
    block = build_map_block(kid)
    if not block:
        return False
    # Blank line before ## Knowledge Index (Markdown spacing)
    new_body = body.replace(ANCHOR, block.rstrip() + "\n\n" + ANCHOR, 1)
    if new_body == body:
        return False
    if not dry_run:
        agent_md.write_text(new_body, encoding="utf-8")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    updated = 0
    skipped_has_map = 0
    for agent_md in sorted(AGENTS.rglob("AGENT.md")):
        if "_template" in str(agent_md):
            continue
        body = agent_md.read_text(encoding="utf-8", errors="replace")
        if MAP_HEADER in body:
            skipped_has_map += 1
            continue
        if inject_one(agent_md, args.dry_run):
            updated += 1

    mode = "dry-run" if args.dry_run else "wrote"
    print(f"{mode}: {updated} AGENT.md file(s) updated, {skipped_has_map} already had Knowledge map")


if __name__ == "__main__":
    main()
