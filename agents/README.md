# Multi-Agent OS v6 — Agent Definitions

## Overview
117 agents across 14 categories. 30 active agents, 87 in pool (activate on demand). All agents have .md definitions.

## Categories
| Prefix | Category | Active | Pool | Total |
|--------|----------|--------|------|-------|
| A | Orchestrator & Sistem | 5 | 3 | 8 |
| B | Kod / Backend | 7 | 12 | 19 |
| C | Code Review | 3 | 3 | 6 |
| D | Dizayn / 2D | 0 | 8 | 8 |
| E | 3D / CAD | 0 | 5 | 5 |
| F | Veri & Analiz | 0 | 10 | 10 |
| G | AI Ops / Workflow | 3 | 7 | 10 |
| H | Pazar Arastirmasi | 3 | 9 | 12 |
| I | Jira & Proje Yonetimi | 3 | 7 | 10 |
| J | DevOps & Altyapi | 2 | 6 | 8 |
| K | Arastirma & Ogrenme | 3 | 6 | 9 |
| L | Kisisel Verimlilik | 1 | 5 | 6 |
| M | Pazarlama Motoru | 0 | 4 | 4 |
| N | Prompt Engineering & Agent Design | 0 | 2 | 2 |

## Model Distribution
- **Free/Local:** ~65% (scripts, Ollama, OpenRouter free)
- **Haiku:** ~18%
- **Sonnet:** ~13%
- **Opus:** ~4% (B1 Backend Architect, B13 Security Auditor, N2 Agent Builder)

## Agent .md Format
Each agent has frontmatter (id, model, capabilities) + 3 sections (Amac, Kapsam, Escalation). ~20 lines each.

## Routing
Task Router (A2, Sonnet) uses capability tags for matching. Auto-dispatch integrated into plan template (CLAUDE.md §9a). See `config/agent-registry.json` for full mapping.

## Activating Pool Agents
In `config/agent-registry.json`, change `"status": "pool"` to `"status": "active"` and add the ID to `active_agents` array.

## New Agents (v0.3)
- B16 Web Game Dev (Phaser, Three.js, Babylon.js, WebGPU)
- B17 Full Stack Web (Next.js, React, Supabase)
- B18 Python Specialist (FastAPI, Django, pandas)
- B19 Unity Developer (ECS, DOTS, shaders, UPM)
- K9 AI Tool Evaluator
- N1 Prompt Engineer
- N2 Agent Builder
