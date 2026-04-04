# Multi-Agent OS v6 — Agent Definitions

## Overview
110 agents across 13 categories. v0.2 has 30 active agents with .md definitions; remaining 80 are in pool (activate on demand).

## Categories
| Prefix | Category | Active (.md) | Pool |
|--------|----------|--------------|------|
| A | Orchestrator & Sistem | 5 | 3 |
| B | Kod / Backend | 7 | 8 |
| C | Code Review | 3 | 3 |
| D | Dizayn / 2D | 0 | 8 |
| E | 3D / CAD | 0 | 5 |
| F | Veri & Analiz | 0 | 10 |
| G | AI Ops / Workflow | 3 (G1, G3, G7) | 7 |
| H | Pazar Arastirmasi | 3 (H1, H5, H6) | 9 |
| I | Jira & Proje Yonetimi | 3 (I1, I2, I4) | 7 |
| J | DevOps & Altyapi | 2 (J2, J7) | 6 |
| K | Arastirma & Ogrenme | 3 (K1, K3, K4) | 5 |
| L | Kisisel Verimlilik | 1 (L1) | 5 |
| M | Pazarlama Motoru | 0 | 4 |

## Model Distribution
- **Free/Local:** ~65% (scripts, Ollama, OpenRouter free)
- **Haiku:** ~18%
- **Sonnet:** ~13%
- **Opus:** ~4% (only B1 Backend Architect, B13 Security Auditor)

## Agent .md Format
Each agent has frontmatter (id, model, capabilities) + 3 sections (Amac, Kapsam, Escalation). ~20 lines each.

## Routing
Task Router (A2, Sonnet) uses capability tags for matching. See `config/agent-registry.json` for full mapping.

## Activating Pool Agents
In `config/agent-registry.json`, change `"status": "pool"` to `"status": "active"` and add the ID to `active_agents` array.
