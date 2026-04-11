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
| P1 | 47 |
| P2 | 0 |
| OK | 149 |

## P0 — critical (fix first)

| ID | Category | Path | k-files | Notes |
|----|----------|------|---------|-------|

## P1

| ID | Category | Path | k-files | Notes |
|----|----------|------|---------|-------|
| E8 | 3d-cad | `3d-cad/unity-level-designer` | 4 | no_memory_dir |
| E10 | 3d-cad | `3d-cad/unity-lighting-artist` | 4 | no_memory_dir |
| E12 | 3d-cad | `3d-cad/unity-rigging-skinning` | 4 | no_memory_dir |
| E11 | 3d-cad | `3d-cad/unity-terrain-specialist` | 4 | no_memory_dir |
| E9 | 3d-cad/unity-cinematic-director | `3d-cad/unity-cinematic-director` | 4 | no_memory_dir |
| G11 | ai-ops | `ai-ops/unity-ml-agents` | 4 | no_memory_dir |
| G12 | ai-ops | `ai-ops/unity-sentis` | 4 | no_memory_dir |
| B35 | backend | `backend/unity-2d-specialist` | 4 | no_memory_dir |
| B43 | backend | `backend/unity-accessibility` | 4 | no_memory_dir |
| B24 | backend | `backend/unity-ai-navigation` | 4 | no_memory_dir |
| B25 | backend | `backend/unity-ar-xr` | 4 | no_memory_dir |
| B51 | backend | `backend/unity-asset-workflow` | 4 | no_memory_dir |
| B26 | backend | `backend/unity-audio` | 4 | no_memory_dir |
| B37 | backend | `backend/unity-camera-systems` | 4 | no_memory_dir |
| B40 | backend | `backend/unity-cloud-services` | 4 | no_memory_dir |
| B46 | backend | `backend/unity-combat-system` | 4 | no_memory_dir |
| B50 | backend | `backend/unity-dependency-injection` | 4 | no_memory_dir |
| B44 | backend | `backend/unity-dialogue-system` | 4 | no_memory_dir |
| B34 | backend | `backend/unity-ecs-dots` | 4 | no_memory_dir |
| B48 | backend | `backend/unity-game-economy` | 4 | no_memory_dir |
| B36 | backend | `backend/unity-input-system` | 4 | no_memory_dir |
| B45 | backend | `backend/unity-inventory-crafting` | 4 | no_memory_dir |
| B29 | backend | `backend/unity-localization` | 4 | no_memory_dir |
| B38 | backend | `backend/unity-memory-manager` | 4 | no_memory_dir |
| B41 | backend | `backend/unity-monetization` | 4 | no_memory_dir |
| B27 | backend | `backend/unity-physics` | 4 | no_memory_dir |
| B47 | backend | `backend/unity-quest-mission` | 4 | no_memory_dir |
| B28 | backend | `backend/unity-save-serialization` | 4 | no_memory_dir |
| B42 | backend | `backend/unity-security-anticheat` | 4 | no_memory_dir |
| B49 | backend | `backend/unity-state-machine` | 4 | no_memory_dir |
| B52 | backend | `backend/unity-streaming-open-world` | 4 | no_memory_dir |
| B39 | backend | `backend/unity-testing` | 4 | no_memory_dir |
| B33 | backend/unity-console-platform | `backend/unity-console-platform` | 4 | no_memory_dir |
| B30 | backend/unity-editor-tooling | `backend/unity-editor-tooling` | 4 | no_memory_dir |
| B32 | backend/unity-mobile-optimizer | `backend/unity-mobile-optimizer` | 4 | no_memory_dir |
| B31 | backend/unity-procedural-generation | `backend/unity-procedural-generation` | 4 | no_memory_dir |
| F11 | data-analytics | `data-analytics/unity-analytics` | 4 | no_memory_dir |
| F12 | data-analytics | `data-analytics/unity-performance-profiler` | 4 | no_memory_dir |
| F13 | data-analytics | `data-analytics/unity-playtesting-analyst` | 4 | no_memory_dir |
| D13 | design | `design/unity-hud-minimap` | 4 | no_memory_dir |
| D11 | design | `design/unity-ui-developer` | 4 | no_memory_dir |
| D12 | design | `design/unity-ux-flow` | 4 | no_memory_dir |
| J11 | devops | `devops/unity-devops` | 5 | no_memory_dir |
| J12 | devops | `devops/unity-version-control` | 4 | no_memory_dir |
| H16 | market-research | `market-research/unity-market-analyst` | 5 | no_memory_dir |
| K15 | research | `research/unity-tech-researcher` | 4 | no_memory_dir |
| K14 | research/unity-asset-store-researcher | `research/unity-asset-store-researcher` | 4 | no_memory_dir |

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
