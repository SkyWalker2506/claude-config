---
last_updated: 2026-04-16
refined_by: gpt-5.4
confidence: high
---

# Harness Engineering — claude-config Specifics

## Current Architecture
- Jarvis (A0): orchestrator, never implements, dispatches to 196 agents (15 categories)
- CLAUDE.md: 715-line monolithic rules file loaded every session as system prompt
- Dispatch flow: /dispatch skill → agent-router.sh → Agent tool with header
- Dispatch header fields: AGENT, MODEL, EFFORT, TASK, CALLER, WATCHDOG
- Agent registry: config/agent-registry.json (model, fallbacks, capabilities per agent)
- Agent definitions: agents/{category}/{slug}/AGENT.md + knowledge/ + memory/

## Critical Problems Identified
1. CLAUDE.md "dispatch-first" rule at line 680 of 715 — LLM ignores it
2. Sub-agents get NO knowledge — dispatch injects only a header, not AGENT.md or knowledge files
3. Telemetry broken — log_dispatch.py writes "unknown" for every event
4. No execution contracts — tasks dispatched with prose, no completion gates
5. No file-backed state — long tasks lose state on compaction

## Fix Targets
1. CLAUDE.md line 1-5: dispatch-first rule must be first thing model reads
2. Two-Tier Knowledge Loading:
   - Tier 1 (dispatch-time): Read AGENT.md + knowledge/_index.md, inject into prompt
   - Tier 2 (on-demand): Agent reads specific knowledge/*.md based on task
3. Sidecar telemetry: write dispatch metadata to /tmp/watchdog/current_dispatch.json before Agent tool
4. Three-layer split: CLAUDE.md → charter.md (behavior) + harness.md (control) + deterministic (config)
5. Execution contracts: structured header with required_outputs, completion_gate, max_tool_calls

## Key File Paths
- global/CLAUDE.md — master rules (target: restructure)
- global/skills/dispatch/SKILL.md — dispatch protocol (target: add knowledge injection)
- config/agent-dispatch.md — dispatch header template (target: add KNOWLEDGE + CONTRACT blocks)
- config/agent-registry.json — 196 agents, 41 active
- scripts/log_dispatch.py — telemetry logger (target: sidecar fallback)
- config/fallback-chains.json — model fallback per task type
- config/layer-contracts.json — Ultra Plan Mode structured output

## Codex CLI Operational Limits

When dispatching tasks to GPT 5.4 via `codex exec --full-auto`:

### Can Do
- Read/write files in working directory
- Run shell commands (sandboxed)
- Create new files, modify existing ones

### Cannot Do
- Git commit/push (sandbox blocks it) — Jarvis must commit separately
- Network/internet access — no web fetch, API calls, or package install
- Access files outside working directory sandbox
- Handle files over ~500 lines in a single refactor task

### Best Practices
- Never include "Commit: ..." in codex prompts — wastes tokens, can't execute
- Break large file operations into chunks (max ~300 lines per task)
- Run file creation and file modification as separate tasks
- Verify output exists after each task (codex exit 0 doesn't mean files changed)
- Kill zombie processes: codex can hang on large tasks without producing output

### Task Sizing Guide
| Task Size | Max Lines | Expected Duration |
|-----------|-----------|-------------------|
| Small (append, create) | <100 lines | 1-3 min |
| Medium (modify, extract) | 100-300 lines | 3-8 min |
| Large (refactor, split) | 300-500 lines | 8-15 min |
| Too Large (>500 lines) | SPLIT IT | Will timeout/fail |
