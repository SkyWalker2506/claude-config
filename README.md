<div align="center">

# claude-config

### **Multi-Agent OS** for [**Claude Code**](https://claude.ai/claude-code)

[![Agents](https://img.shields.io/badge/agents-196_registry-6366f1)](./config/agent-registry.json)
[![Plugins](https://img.shields.io/badge/plugins-21_marketplace-f97316)](https://github.com/SkyWalker2506/claude-marketplace)
[![MCP](https://img.shields.io/badge/MCP-8_integrated-0ea5e9)](./global/settings.json.template)
[![License](https://img.shields.io/badge/license-MIT-22c55e)](./LICENSE)
[![Author](https://img.shields.io/badge/Musab_Kara-GitHub-181717?logo=github)](https://github.com/SkyWalker2506)

**Install once · Skills + hooks + MCP · Agent registry · Session sync to `~/.claude/`**

[Install](#quick-start) · [Architecture](#architecture) · [Ecosystem](#ecosystem-on-github-read-order)

</div>

---

## Ecosystem on GitHub (read order)

1. **[claude-agent-catalog](https://github.com/SkyWalker2506/claude-agent-catalog)** — agent inventory (start the story on GitHub)
2. **[claude-marketplace](https://github.com/SkyWalker2506/claude-marketplace)** — plugins — `ccplugin-*`
3. **claude-config (this repo)** — full OS: `./install.sh`, skills, MCP, hooks, [`agent-registry.json`](./config/agent-registry.json)
4. **[ClaudeHQ](https://github.com/SkyWalker2506/ClaudeHQ)** — multi-project workspace hub

Optional: [sdk-market](https://github.com/SkyWalker2506/sdk-market). Counts follow **`main`** here and the linked repos.

```mermaid
flowchart LR
  A[1 Catalog] --> B[2 Marketplace]
  B --> C[3 claude-config]
  C --> D[4 ClaudeHQ]
```

---

## What is this?

A portable, self-installing configuration system that turns Claude Code into a multi-agent operating system. Clone → `./install.sh` → done.

- **196 registered agents** in [`agent-registry.json`](./config/agent-registry.json) · 15 categories (activate on demand)
- **21 plugins** on our [marketplace](https://github.com/SkyWalker2506/claude-marketplace)
- **8 MCP servers** integrated (GitHub, Atlassian/Jira, Firebase, Flutter, jCodeMunch, Git, Fetch, Context7)
- **34 slash commands** (/yolo, /team-build, /jira-run, /audit, /web-research, /sprint-plan, and more)
- **Telegram bot** with persistent Haiku agent — control Claude from your phone
- **Local-first model routing** — Ollama → Claude → OpenRouter free (saves tokens)
- **Cost control** — automatic model tier switching based on quota remaining

## Quick Start

```bash
git clone https://github.com/SkyWalker2506/claude-config.git ~/Projects/claude-config
cd ~/Projects/claude-config
./install.sh
```

The installer sets up everything: CLAUDE.md hierarchy, skills, MCP servers, hooks, secrets vault, Telegram integration, and plugin marketplace.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Entry Points                    │
│   Claude Code  ·  Telegram Bot  ·  OpenCode/Zen │
└──────────────────────┬──────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────┐
│              Routing & Budget                    │
│   Task Router → Token Budget → Fallback Manager  │
│           Agent Registry (~196)                  │
└──────────────────────┬──────────────────────────┘
                       ▼
┌───────────┬──────────┬──────────┬───────────────┐
│ Opus (4%) │Sonnet(13%)│Haiku(18%)│ Free/Local(65%)│
└───────────┴──────────┴──────────┴───────────────┘
                       ▲
┌─────────────────────────────────────────────────┐
│              Infrastructure                      │
│  Daily Health Check · Watchdog · Cron Scheduler  │
└─────────────────────────────────────────────────┘
```

## Plugin Marketplace

21 plugins, each in its own repo. Add the marketplace:

```bash
claude plugin marketplace add SkyWalker2506/claude-marketplace
```

Then browse with `/plugin > Discover` or install directly:

| Plugin | What it does |
|--------|-------------|
| [jira-suite](https://github.com/SkyWalker2506/ccplugin-jira-suite) | Jira loops, dashboard, sprint, decisions — Atlassian MCP |
| [code-quality](https://github.com/SkyWalker2506/ccplugin-code-quality) | Code audit, CLAUDE.md refine, jCodeMunch indexing |
| [research-tools](https://github.com/SkyWalker2506/ccplugin-research-tools) | Web research, project analysis, PRD, Ralph |
| [autonomous-ops](https://github.com/SkyWalker2506/ccplugin-autonomous-ops) | /yolo, /team-build, /rbg autonomous modes |
| [telegram-bridge](https://github.com/SkyWalker2506/ccplugin-telegram) | Telegram bot — text, photo, doc, voice (Whisper TR/EN) |
| [git-github](https://github.com/SkyWalker2506/ccplugin-git-github) | Git + GitHub MCP integration |
| [flutter-firebase](https://github.com/SkyWalker2506/ccplugin-flutter-firebase) | Flutter + Firebase MCP |
| [sprint-planner](https://github.com/SkyWalker2506/ccplugin-sprint-planner) | Sprint planning from PRD |
| [devtools-setup](https://github.com/SkyWalker2506/ccplugin-devtools-setup) | Install, migrate, secrets, MCP config |
| [agent-browser](https://github.com/SkyWalker2506/ccplugin-agent-browser) | Headless browser automation |
| [opencode-bridge](https://github.com/SkyWalker2506/ccplugin-opencode-bridge) | OpenCode/Zen + Ollama local models |
| [ai-review](https://github.com/SkyWalker2506/ccplugin-ai-review) | GitHub PR review via OpenRouter ($0) |
| [daily-check](https://github.com/SkyWalker2506/ccplugin-daily-check) | Daily system health check |
| [sync-agents](https://github.com/SkyWalker2506/ccplugin-sync-agents) | Agent registry validator |
| [notifications](https://github.com/SkyWalker2506/ccplugin-notifications) | Multi-channel notifications — Telegram, macOS, sound |
| [improve](https://github.com/SkyWalker2506/ccplugin-improve) | Analyzes content (videos, articles) → extracts claude-config improvements |
| [clipboard](https://github.com/SkyWalker2506/ccplugin-clipboard) | Cross-platform clipboard manager — macOS, Linux, Windows |
| [voice-input](https://github.com/SkyWalker2506/ccplugin-voice-input) | macOS mic + Whisper transcript, Türkçe destekli |

## Agent System

Knowledge-First agents across **15 categories** (registry on `main`). Each agent lives in a folder with:
- `AGENT.md` (identity, boundaries, process)
- `knowledge/` (lazy-loaded domain notes)
- `memory/` (sessions + learnings)

| Category | Agents | Examples |
|----------|--------|---------|
| Orchestrator | A1–A8 | Lead Orchestrator, Task Router, Fallback Manager |
| Backend | B1–B19 | Architect (Opus), Coder (Sonnet), Bug Hunter, Security Auditor (Opus) |
| Code Review | C1–C6 | Lint Hook, Security Scanner, AI Reviewer |
| AI Ops | G1–G10 | Agent Coordinator, MCP Health, Update Checker |
| Jira & PM | I1–I10 | Jira Router, Sprint Planner, Status Reporter |
| Research | K1–K9 | Web Researcher, Doc Fetcher, AI Tool Evaluator |
| Market Research | H1–H12 | Competitor Analyst, SEO, GEO |
| DevOps | J1–J8 | Cloud Deploy, Incident Responder |
| And more... | D, E, F, L, M, N, O | Design, 3D/CAD, Data, Productivity, Marketing, Prompt Eng, Sales |

## Telegram Bot

Control Claude from your phone — persistent Haiku agent session:

```bash
# Start the agent (Haiku, low cost)
python3 config/telegram-agent.py ~/Projects/your-project

# Or classic mode (claude -p --continue per message)
bash config/telegram-poll.sh ~/Projects/your-project
```

Features: text commands, photo analysis, document processing, voice transcription (Whisper TR/EN), inline keyboard.

## How It Works

### 3-Layer CLAUDE.md

```
~/.claude/CLAUDE.md          ← Global (all projects)
~/Projects/CLAUDE.md         ← Shared rules (framework-agnostic)
~/Projects/MyApp/CLAUDE.md   ← Project-specific
```

### Auto Project Setup

Open `claude` in any project directory → migration hook fires → setup wizard creates project config.

### Model Routing

| Quota Remaining | Mode | Rules |
|----------------|------|-------|
| ≥10% | Normal | Opus for architecture, Sonnet for code, Haiku for trivial |
| 5–10% | Saving | Opus critical-only, rest Sonnet |
| <5% | Critical | No Opus, Sonnet + Haiku |
| <1% | Sonnet-only | Haiku exhausted, Sonnet takes over |

Fallback priority: **Local (Ollama) → Claude (paid) → Free (OpenRouter)**

## File Structure

```
claude-config/
├── install.sh              # One-command setup
├── uninstall.sh            # Restore from backup
├── CLAUDE.md               # Repo-level rules
├── global/
│   ├── CLAUDE.md           # → ~/.claude/CLAUDE.md
│   ├── settings.json.template  # MCP servers, hooks, permissions
│   └── skills/             # 52 slash commands
├── agents/                 # Knowledge-First agent trees
│   ├── orchestrator/       # A1–A8
│   ├── backend/            # B1–B19
│   ├── code-review/        # C1–C6
│   └── ...                 # 15 categories
├── config/
│   ├── agent-registry.json # Agent → model mapping
│   ├── fallback-chains.json
│   ├── model-tiers.json
│   ├── telegram-agent.py   # Persistent Telegram bot
│   └── daily-check.sh      # Health check script
├── plugins/                # Plugin source (telegram, ai-review, etc.)
└── templates/              # Project scaffolding
```

## Secrets

API keys live in a private git repo, symlinked to `~/.claude/secrets/`. Never touches public repos.

```bash
# Setup happens during install.sh — your private repo is cloned automatically
# Or manually:
echo 'TELEGRAM_BOT_TOKEN=xxx' >> ~/Projects/claude-config/claude-secrets/secrets.env
```

## Moving to Another Machine

```bash
git clone https://github.com/SkyWalker2506/claude-config.git ~/Projects/claude-config
cd ~/Projects/claude-config
./install.sh
# Secrets pulled automatically if you own the private repo
```

## Related

- [Agent Catalog](https://github.com/SkyWalker2506/claude-agent-catalog) — agent inventory (GitHub entry point #1)
- [Plugin Marketplace](https://github.com/SkyWalker2506/claude-marketplace) — plugins for Claude Code, browse & install
- [ClaudeHQ](https://github.com/SkyWalker2506/ClaudeHQ) — ecosystem HQ, cross-project workspace
- [SDK Market](https://github.com/SkyWalker2506/sdk-market) — production-ready SDKs and kits
- [OpenCode](https://opencode.ai/) — Free/local models via Zen + Ollama

## Author

**Musab Kara** — [LinkedIn](https://linkedin.com/in/musab-kara-85580612a) · [GitHub](https://github.com/SkyWalker2506)

## License

MIT
