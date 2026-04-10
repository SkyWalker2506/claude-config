# Agent coverage audit

- **Generated:** `python3 scripts/agent_coverage_audit.py`
- **Scanned:** 196 agents (excludes `agents/_template`)

## Tier definitions

| Tier | Meaning |
|------|---------|
| **P0** | Missing `knowledge/_index.md` OR zero topic files — broken / not bootstrapped |
| **P1** | 1–3 topic files OR missing `memory/` markdown — thin bootstrap |
| **P2** | ≥4 topics + memory OK but no `## Knowledge map` in AGENT.md |
| **OK** | Passes all heuristics below |

## Heuristic rules (automated)

1. `knowledge/_index.md` exists
2. ≥ **4** topic files in `knowledge/` (excluding `_index.md`)
3. `memory/` has ≥1 `.md`
4. `AGENT.md` contains `## Knowledge map`

## Summary

| Tier | Count |
|------|-------:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| OK | 196 |

## P0 — critical (fix first)

| ID | Category | Path | k-files | Notes |
|----|----------|------|---------|-------|

## P1

| ID | Category | Path | k-files | Notes |
|----|----------|------|---------|-------|

## P2 (add Knowledge map + optional polish)

_Count: 0_ — full table omitted; run script and filter `tier=P2` or grep `no_knowledge_map` in git.

## Proposed new agents (backlog)

| ID | Name | Category | Why |
|----|------|----------|-----|
| P-N1 | Docs Pipeline Agent | ai-ops | README/changelog sync across catalog ↔ config ↔ marketplace |
| P-N2 | Registry Drift Guard | ai-ops | CI: `sync_agents.py --check` + registry vs AGENT.md |
| P-N3 | Plugin Release Train | devops | `marketplace.json` + semver for all `ccplugin-*` |
| P-N4 | i18n Copy Agent | productivity | TR/EN parity for skills + CLAUDE fragments |
| P-N5 | Cost Telemetry Analyst | ai-ops | Aggregate hook + `.watchdog` token signals |
| P-N6 | Skill Deprecation Manager | prompt-engineering | Sunset skills, migration notes |
| P-N7 | MCP Smoke Agent | ai-ops | Post-install MCP health matrix |
| P-N8 | Unity Package Auditor | backend | UPM dependency + license scan |

_Add to `config/agent-registry.json` + `tools/sync_agent_registry_from_agents.py` when approved._

## Rollout batches (suggested)

1. **P0** — bootstrap `knowledge/` + `memory/` + `Knowledge map`
2. **P1** — bring topic count to ≥4
3. **P2** — `python3 scripts/inject_knowledge_maps.py` (adds `## Knowledge map` from `knowledge/*.md` H1 titles)
4. **Quality** — deepen knowledge files per `cursor-prompts/mega-prompt.md`
