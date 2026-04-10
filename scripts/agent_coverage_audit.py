#!/usr/bin/env python3
"""Scan agents/*/ for knowledge completeness. Writes agents/AGENT_COVERAGE_AUDIT.md"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
OUT = AGENTS / "AGENT_COVERAGE_AUDIT.md"


def parse_frontmatter(body: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---", body, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def main() -> None:
    rows: list[dict] = []
    for agent_md in sorted(AGENTS.rglob("AGENT.md")):
        if "_template" in str(agent_md):
            continue
        folder = agent_md.parent
        kid = folder / "knowledge"
        mem = folder / "memory"
        kmds = list(kid.glob("*.md")) if kid.is_dir() else []
        kfiles = [p for p in kmds if p.name != "_index.md"]
        idx = (kid / "_index.md") if kid.is_dir() else None
        body = agent_md.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(body)
        agent_id = fm.get("id", "")
        cat = fm.get("category", "")
        notes: list[str] = []
        if not idx or not idx.exists():
            notes.append("no_knowledge_index")
        if len(kfiles) < 4:
            notes.append(f"km_{len(kfiles)}")
        if mem.is_dir():
            if not any(mem.glob("*.md")):
                notes.append("empty_memory")
        else:
            notes.append("no_memory_dir")
        if "## Knowledge map" not in body:
            notes.append("no_knowledge_map")

        tier = "P0" if ("no_knowledge_index" in notes or any(n.startswith("km_0") for n in notes)) else (
            "P1" if (any(n.startswith("km_") and n != "km_0" for n in notes) or "no_memory_dir" in notes) else (
            "P2" if "no_knowledge_map" in notes else "OK"
            )
        )
        rows.append({
            "path": str(folder.relative_to(AGENTS)),
            "id": agent_id,
            "cat": cat,
            "k_n": len(kfiles),
            "notes": notes,
            "tier": tier,
        })

    by_tier = Counter(r["tier"] for r in rows)
    lines = [
        "# Agent coverage audit",
        "",
        f"- **Generated:** `python3 scripts/agent_coverage_audit.py`",
        f"- **Scanned:** {len(rows)} agents (excludes `agents/_template`)",
        "",
        "## Tier definitions",
        "",
        "| Tier | Meaning |",
        "|------|---------|",
        "| **P0** | Missing `knowledge/_index.md` OR zero topic files — broken / not bootstrapped |",
        "| **P1** | 1–3 topic files OR missing `memory/` markdown — thin bootstrap |",
        "| **P2** | ≥4 topics + memory OK but no `## Knowledge map` in AGENT.md |",
        "| **OK** | Passes all heuristics below |",
        "",
        "## Heuristic rules (automated)",
        "",
        "1. `knowledge/_index.md` exists",
        "2. ≥ **4** topic files in `knowledge/` (excluding `_index.md`)",
        "3. `memory/` has ≥1 `.md`",
        "4. `AGENT.md` contains `## Knowledge map`",
        "",
        "## Summary",
        "",
        f"| Tier | Count |",
        "|------|-------:|",
    ]
    for t in ("P0", "P1", "P2", "OK"):
        lines.append(f"| {t} | {by_tier.get(t, 0)} |")
    lines += ["", "## P0 — critical (fix first)", "", "| ID | Category | Path | k-files | Notes |", "|----|----------|------|---------|-------|"]
    for r in sorted((x for x in rows if x["tier"] == "P0"), key=lambda x: (x["cat"], x["path"])):
        lines.append(f"| {r['id']} | {r['cat']} | `{r['path']}` | {r['k_n']} | {', '.join(r['notes'])} |")
    lines += ["", "## P1", "", "| ID | Category | Path | k-files | Notes |", "|----|----------|------|---------|-------|"]
    for r in sorted((x for x in rows if x["tier"] == "P1"), key=lambda x: (x["cat"], x["path"])):
        lines.append(f"| {r['id']} | {r['cat']} | `{r['path']}` | {r['k_n']} | {', '.join(r['notes'])} |")
    lines += ["", "## P2 (add Knowledge map + optional polish)", "", f"_Count: {by_tier.get('P2', 0)}_ — full table omitted; run script and filter `tier=P2` or grep `no_knowledge_map` in git.", ""]
    lines += [
        "## Proposed new agents (backlog)",
        "",
        "| ID | Name | Category | Why |",
        "|----|------|----------|-----|",
        "| P-N1 | Docs Pipeline Agent | ai-ops | README/changelog sync across catalog ↔ config ↔ marketplace |",
        "| P-N2 | Registry Drift Guard | ai-ops | CI: `sync_agents.py --check` + registry vs AGENT.md |",
        "| P-N3 | Plugin Release Train | devops | `marketplace.json` + semver for all `ccplugin-*` |",
        "| P-N4 | i18n Copy Agent | productivity | TR/EN parity for skills + CLAUDE fragments |",
        "| P-N5 | Cost Telemetry Analyst | ai-ops | Aggregate hook + `.watchdog` token signals |",
        "| P-N6 | Skill Deprecation Manager | prompt-engineering | Sunset skills, migration notes |",
        "| P-N7 | MCP Smoke Agent | ai-ops | Post-install MCP health matrix |",
        "| P-N8 | Unity Package Auditor | backend | UPM dependency + license scan |",
        "",
        "_Add to `config/agent-registry.json` + `tools/sync_agent_registry_from_agents.py` when approved._",
        "",
        "## Rollout batches (suggested)",
        "",
        "1. **P0** — bootstrap `knowledge/` + `memory/` + `Knowledge map`",
        "2. **P1** — bring topic count to ≥4",
        "3. **P2** — add `## Knowledge map` everywhere (scriptable)",
        "4. **Quality** — deepen knowledge files per `cursor-prompts/mega-prompt.md`",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}  P0={by_tier.get('P0',0)} P1={by_tier.get('P1',0)} P2={by_tier.get('P2',0)} OK={by_tier.get('OK',0)}")


if __name__ == "__main__":
    main()
