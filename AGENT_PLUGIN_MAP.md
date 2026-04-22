# Agent–Plugin Compatibility Map

> Auto-maintained reference. Source: `config/agent-registry.json` + `config/plugin-registry.json`
> Last updated: 2026-04-14

---

## Plugin → Agents

Which agents benefit from each plugin. Install a plugin when you frequently use the listed agents.

| Plugin | Key Agents | Category |
|--------|-----------|----------|
| [ccplugin-backend-forge](https://github.com/SkyWalker2506/ccplugin-backend-forge) | B1 (Backend Architect), B2 (Backend Coder), B5 (Database Agent), J2 (Cloud Deploy), A10 (CodeLead) | Development |
| [ccplugin-frontend-craft](https://github.com/SkyWalker2506/ccplugin-frontend-craft) | B3 (Frontend Coder), B15 (Mobile Dev), B16 (Web Game Dev), B17 (Full Stack Web), D1 (UI/UX Researcher) | Development |
| [ccplugin-flutter-firebase](https://github.com/SkyWalker2506/ccplugin-flutter-firebase) | B15 (Mobile Dev Agent), J6 (Firebase Agent), B3 (Frontend Coder) | Development |
| [ccplugin-git-github](https://github.com/SkyWalker2506/ccplugin-git-github) | B1, B2, B3, B5, B7, B13, C3, J2, J7, J10 | Development |
| [ccplugin-agent-browser](https://github.com/SkyWalker2506/ccplugin-agent-browser) | K1 (Web Researcher), H1 (Market Researcher), H2 (Competitor Analyst), H5 (SEO Agent) | Development |
| [ccplugin-opencode-bridge](https://github.com/SkyWalker2506/ccplugin-opencode-bridge) | A3 (Fallback Manager), A5 (Context Pruner), B2, B3 (free-model fallback path) | Development |
| [ccplugin-jira-suite](https://github.com/SkyWalker2506/ccplugin-jira-suite) | I1 (Jira Router), I2 (Sprint Planner), I4 (Status Reporter), I3–I10 (all Jira PM agents) | Productivity |
| [ccplugin-sprint-planner](https://github.com/SkyWalker2506/ccplugin-sprint-planner) | I2 (Sprint Planner), I3 (Task Decomposer), I6 (Backlog Groomer), A1 (Lead Orchestrator) | Productivity |
| [ccplugin-research-tools](https://github.com/SkyWalker2506/ccplugin-research-tools) | K1 (Web Researcher), K3 (Doc Fetcher), K4 (Trend Analyzer), H1 (Market Researcher) | Productivity |
| [ccplugin-devtools-setup](https://github.com/SkyWalker2506/ccplugin-devtools-setup) | A0 (Jarvis), A1 (Lead Orchestrator), G3 (MCP Health), G7 (Update Checker) | Productivity |
| [ccplugin-code-quality](https://github.com/SkyWalker2506/ccplugin-code-quality) | C1 (Lint Hook), C2 (Security Scanner), C3 (AI Reviewer), B13 (Security Auditor), B7 (Bug Hunter) | Code Review |
| [ccplugin-ai-review](https://github.com/SkyWalker2506/ccplugin-ai-review) | C3 (Local AI Reviewer), C4 (Code Rabbit), C5 (CI Review), B13 (Security Auditor) | Code Review |
| [ccplugin-autonomous-ops](https://github.com/SkyWalker2506/ccplugin-autonomous-ops) | A0 (Jarvis), A1 (Lead Orchestrator), A2 (Task Router), G1 (Agent Coordinator) | AI Ops |
| [ccplugin-daily-check](https://github.com/SkyWalker2506/ccplugin-daily-check) | G3 (MCP Health Agent), G7 (Update Checker), A6 (Daily Health Check — pool) | AI Ops |
| [ccplugin-sync-agents](https://github.com/SkyWalker2506/ccplugin-sync-agents) | G4 (Config Manager), G3 (MCP Health), A0 (Jarvis) | AI Ops |
| [ccplugin-improve](https://github.com/SkyWalker2506/ccplugin-improve) | A0 (Jarvis), A1 (Lead Orchestrator), K1 (Web Researcher) | AI Ops |
| [ccplugin-telegram](https://github.com/SkyWalker2506/ccplugin-telegram) | A0 (Jarvis — primary phone interface), A1, A2 | Communication |
| gpt-import (local) | A0 (Jarvis), K1 (Web Researcher), G4 (Config Manager) | Agent Tooling |
| hq-feature (local) | A0 (Jarvis), A1 (Lead Orchestrator), J10 (GitHub Manager) | Dev Workflow |
| [ccplugin-notifications](https://github.com/SkyWalker2506/ccplugin-notifications) | A0 (Jarvis), G1 (Agent Coordinator), J7 (Incident Responder) | Communication |
| [ccplugin-3d-forge](https://github.com/SkyWalker2506/ccplugin-3d-forge) | E1 (3D Concept Planner), E2 (Blender Script), E4 (Render Pipeline), E5 (3D Asset Optimizer), A9 (ArtLead) | Creative |
| [ccplugin-clipboard](https://github.com/SkyWalker2506/ccplugin-clipboard) | A0 (Jarvis — cross-session data passing), all agents writing output | Tools |
| [ccplugin-voice-input](https://github.com/SkyWalker2506/ccplugin-voice-input) | A0 (Jarvis — primary voice entry point) | Tools |

---

## Agent → Required MCPs

Active agents only (`status: active`). Agents with `mcps: ["*"]` accept all available MCPs.

| Agent | ID | Required MCPs | Notes |
|-------|----|---------------|-------|
| Jarvis | A0 | `*` (all) | Primary orchestrator; uses whatever is available |
| Lead Orchestrator | A1 | `*` (all) | Opus-level; full access |
| Task Router | A2 | `*` (all) | Haiku model; routing + dispatch |
| Fallback Manager | A3 | — | No MCP dependency |
| Token Budget Manager | A4 | — | No MCP dependency |
| Context Pruner | A5 | — | No MCP dependency |
| ArtLead | A9 | — | Dispatches to B3, D1, D2, H8, D8 |
| CodeLead | A10 | — | Dispatches to B1, B8, B12, F2, F4, B10 |
| GrowthLead | A11 | — | Dispatches to H5, H7, H9, M4, F2, M3 |
| BizLead | A12 | — | Dispatches to H1, H2, H3, H4, K1, K4 |
| SecLead | A13 | — | Dispatches to B13, C2 |
| Backend Architect | B1 | `github`, `git`, `jcodemunch`, `context7` | Architecture decisions + ADRs |
| Backend Coder | B2 | `github`, `git`, `jcodemunch`, `context7` | Codex CLI primary |
| Frontend Coder | B3 | `github`, `git`, `context7` | React, Flutter, UI |
| Database Agent | B5 | `github`, `git`, `jcodemunch` | SQL/NoSQL, migrations |
| Bug Hunter | B7 | `github`, `git`, `jcodemunch` | Debugging, root-cause |
| Security Auditor | B13 | `github`, `git`, `jcodemunch` | OWASP, secret scan |
| Mobile Dev Agent | B15 | `github`, `git`, `flutter-dev`, `context7` | Flutter, Dart, Firebase |
| Lint & Format Hook | C1 | — | Pre-commit gate |
| Security Scanner Hook | C2 | — | Pre-commit gate |
| Local AI Reviewer | C3 | `github`, `git` | Free-model PR review |
| Agent Coordinator | G1 | `*` (all) | Multi-agent orchestration |
| MCP Health Agent | G3 | — | Health checks via scripts |
| Update Checker | G7 | `fetch` | Version + changelog parsing |
| Market Researcher | H1 | `fetch`, `context7` | Competitor + trend research |
| SEO Agent | H5 | `fetch` | SEO audit, keyword research |
| GEO Agent | H6 | `fetch`, `context7` | AI-visibility optimization |
| Jira Router | I1 | `atlassian` | Issue triage, routing |
| Sprint Planner | I2 | `atlassian` | Sprint planning, estimation |
| Status Reporter | I4 | `atlassian` | Burndown, dashboard |
| Cloud Deploy Agent | J2 | `github`, `git` | Vercel, Firebase, CI/CD |
| Incident Responder | J7 | `github`, `git`, `fetch` | On-call, post-mortem |
| GitHub Manager | J10 | `github`, `git` | Repo management, GH Actions |
| Web Researcher | K1 | `fetch`, `context7` | Web search, summarization |
| Documentation Fetcher | K3 | `context7`, `fetch` | API docs, library lookup |
| Trend Analyzer | K4 | `fetch` | Technology radar |
| Email Summarizer | L1 | `gmail` | Inbox triage, draft replies |

---

## Quick Reference: MCP → Agents

| MCP | Used By (active agents) |
|-----|------------------------|
| `*` (all) | A0 (Jarvis), A1 (Lead Orchestrator), A2 (Task Router), G1 (Agent Coordinator) |
| `github` | B1, B2, B3, B5, B7, B13, B15, C3, J2, J7, J10, K15 |
| `git` | B1, B2, B3, B5, B7, B13, B15, C3, J2, J7, J10 |
| `jcodemunch` | B1, B2, B5, B7, B13 |
| `context7` | B1, B2, B3, B15, H1, H6, K1, K3 |
| `atlassian` | I1, I2, I4 (all active Jira PM agents) |
| `fetch` | G7, H1, H5, H6, J7, K1, K3, K4 |
| `flutter-dev` | B15 (Mobile Dev Agent) |
| `firebase` | J6 (Firebase Agent — pool) |
| `gmail` | L1 (Email Summarizer) |

---

## Plugin–MCP Dependency Matrix

Some plugins bundle or configure specific MCPs. Use this when planning installs.

| Plugin | Bundled/Required MCP | Notes |
|--------|---------------------|-------|
| ccplugin-jira-suite | `atlassian` | Atlassian MCP included in plugin |
| ccplugin-research-tools | `fetch` | Fetch MCP required |
| ccplugin-flutter-firebase | `flutter-dev`, `firebase` | Both MCPs required |
| ccplugin-git-github | `git`, `github` | Both MCPs required |
| ccplugin-backend-forge | — | Uses Vercel/Supabase CLI directly |
| ccplugin-agent-browser | `playwright` | Playwright MCP (headless browser) |
| ccplugin-devtools-setup | — | Manages MCP config, no runtime dependency |
| ccplugin-code-quality | `jcodemunch` | jCodeMunch indexing integration |
| ccplugin-sprint-planner | `atlassian` | Jira task creation |

---

## Notes

- Agents with `mcps: []` use bash tools, scripts, or Codex CLI — they do not require MCP servers.
- Agents with `mcps: ["*"]` should have all 8 core MCPs active: `github`, `git`, `atlassian`, `firebase`, `flutter-dev`, `jcodemunch`, `fetch`, `context7`.
- Pool agents (status: pool) are not listed above — activate them on demand via `agent-registry.json`.
- Plugin compatibility is inferred from capabilities; a plugin may benefit an agent even if not explicitly wired.
