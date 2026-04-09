---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Skill Creation Workflow

## Quick Reference

- **Skill** = packaged instructions (e.g. `SKILL.md`) with triggers + procedure; loaded **on demand**, not at every session start.
- **Trigger discipline:** narrow phrases — “install”, “commit all”, “jira spaces” — avoid broad words that fire constantly.
- **Structure:** Title → When to use → Steps → Scripts/paths → Failure modes → Related agents.
- **Dynamic prompts:** optional `$(shell)` snippets — document security (no secrets in output).
- **Ownership:** N2 designs skill *shape* and cross-links; **N7 Skill Design Specialist** deep-dives taxonomy when the catalog is large (Bridge both ways).
- **Deliverables:** `SKILL.md`, optional `scripts/`, update to marketplace/registry if the repo uses a plugin index.

**2025–2026:** Prefer short trigger lists + one primary workflow per skill to reduce accidental activation.

## Patterns & Decision Matrix

| Need | Choose | Avoid |
|------|--------|-------|
| One-off user command | Single skill with 3–7 steps | New agent |
| Repo-wide convention | Skill + link from `CLAUDE.md` | Duplicating policy in 10 skills |
| Heavy branching | Sub-sections + “If X then Y” | Nested skills that differ by one line |
| Automation + API keys | Skill calls script reading env | Inline secrets in SKILL.md |

**Skill vs agent (handoff)**

| Dimension | Skill | Agent (`AGENT.md`) |
|-----------|-------|---------------------|
| Lifecycle | Triggered | Dispatched by router/orchestrator |
| State | Stateless procedure | May own memory/, knowledge/ |
| Scope | One workflow | Role + boundaries + escalation |

## Code Examples

**`SKILL.md` front matter + trigger block (illustrative):**

```markdown
---
name: example-skill
description: Run install flow for claude-config. Triggers install, kurulum, setup config.
---

# Install Flow

## When this applies
User wants to run `install.sh` or fix symlinks/MCP.

## Steps
1. Read `~/Projects/claude-config/install.sh` flags from user.
2. Run installer non-interactively only if flags are explicit.
3. Report `INSTALL_NEEDED` / `MCP_SETUP_NEEDED` signals if hook prints them.
```

**Guardrail for dynamic sections:**

```markdown
Current branch: $(git branch --show-current)
```

**Rule:** only allow commands that are read-only or explicitly user-approved in the skill text.

## Anti-Patterns

| Anti-pattern | Why | Fix |
|--------------|-----|-----|
| Novel-length SKILL.md | Triggers load too much context | Move depth to `knowledge/` or docs |
| Triggers that match everything | Constant misfires | Add negative examples or narrow phrases |
| Duplicate agent instructions | Drift between skill and AGENT.md | Single source: link from skill to agent |
| Skills that bypass Boundaries | Security holes | Reuse Never rules from domain agents |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Anthropic — Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — skills model and packaging
- [Cursor — Agent Skills documentation](https://cursor.com/docs/context/skills) — SKILL.md placement and behavior
- [Claude Code — Skills best practices](https://code.claude.com/docs/en/skills) — authoring and discovery
- [Martin Fowler — LLM-oriented programming](https://martinfowler.com/articles/2025-llm-oriented-programming.html) — instructions as code, maintainability
