# Maintenance scripts

## Agent coverage

| Script | Purpose |
|--------|---------|
| `agent_coverage_audit.py` | Scans `agents/**/AGENT.md` + `knowledge/` + `memory/`. Writes `agents/AGENT_COVERAGE_AUDIT.md` with tiers **P0 / P1 / P2 / OK**. |

```bash
python3 scripts/agent_coverage_audit.py
```

**Tier rules (short):** P0 = missing index or zero topic files; P1 = thin topics or memory; P2 = missing `## Knowledge map` in `AGENT.md`; OK = all checks pass.

## Knowledge map injection

| Script | Purpose |
|--------|---------|
| `inject_knowledge_maps.py` | Inserts `## Knowledge map` (table of `knowledge/*.md` topics, H1 or humanized filename) immediately before `## Knowledge Index` when the section is missing. |

```bash
python3 scripts/inject_knowledge_maps.py --dry-run   # count only
python3 scripts/inject_knowledge_maps.py             # apply
```

Re-run the audit after injection to confirm **P2 = 0**.

## Knowledge section coverage (mega-prompt)

| Script | Purpose |
|--------|---------|
| `knowledge_quality_audit.py` | Counts topic files missing `Quick Reference`, `Patterns & Decision Matrix`, `Code Examples`, `Anti-Patterns`, or `Deep Dive Sources`. Writes `agents/KNOWLEDGE_QUALITY_AUDIT.md`. |

```bash
python3 scripts/knowledge_quality_audit.py
```
