---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Agent Design Patterns

## Quick Reference

| Concern | Pattern | When |
|--------|---------|------|
| Scope | Single-responsibility agent | One capability cluster per `AGENT.md` |
| Context | Lazy-load knowledge | Read `knowledge/_index.md` first, then topic files |
| Safety | Boundaries: Always / Never / Bridge | Prevents scope creep and duplicate ownership |
| Ops | Escalation table | Every “not my job” path names a target agent ID |
| Registry | `id`, `capabilities`, `related`, `mcps` | Keeps routing and MCP wiring explicit |

**Frontmatter contract (do not invent new keys without registry change):** `id`, `name`, `category`, `tier`, `models`, `refine_model`, `mcps`, `capabilities`, `max_tool_calls`, `related`, `status`.

**Body contract:** Identity → Boundaries (Always / Never / Bridge) → Process → Output Format → When to Use / NOT → Red Flags → Verification → Error Handling → Escalation → Knowledge Index.

## Patterns & Decision Matrix

| Pattern | Use when | Trade-off |
|---------|----------|-----------|
| **Thin orchestrator** | User-facing coordinator that dispatches only | Less duplication; needs strong downstream agents |
| **Fat specialist** | Rare domain, heavy knowledge base | Larger `knowledge/`; harder to maintain |
| **Hooked agent** | Same steps every run (lint, deploy check) | Predictable; risk of rigid process text |
| **Bridge-first** | Org has many overlapping roles | More text; avoids “who owns this?” gaps |

**Capability naming:** use verb-noun or domain shards: `agent-design`, `mcp-integration`, `skill-creation`, `workflow-design` — avoid vague tags like `general` or `misc`.

**`related` field:** list agents that frequently hand off *to* or *from* this agent; Bridge section must mirror with two-way sentences.

## Code Examples

**Minimal `AGENT.md` skeleton (body only; frontmatter stays canonical in repo):**

```markdown
## Identity
Builds and maintains agent definitions: AGENT.md, registry rows, and knowledge maps for routing.

## Boundaries
### Always
- Read `knowledge/_index.md` before loading topic files.
### Never
- Change another agent's knowledge without coordination.
### Bridge
- N1 Prompt Engineer: refines natural-language system prompts after structure is frozen.
```

**`config/agent-registry.json` style row (illustrative — match real schema in repo):**

```json
{
  "id": "N2",
  "name": "Agent Builder",
  "primary_model": "opus",
  "capabilities": ["agent-design", "mcp-integration", "skill-creation", "workflow-design"],
  "status": "pool",
  "related": ["N1", "A1", "G1"]
}
```

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| Copy-paste Identity from another agent | Routing collisions, wrong escalation | Rewrite Identity from this agent’s real job |
| “God agent” with 20+ capabilities | No clear dispatch; token waste | Split agents; narrow `capabilities` |
| Bridge only outbound | Mega-prompt requires A↔B | Add reverse line on peer agent or document handoff |
| Process = generic “1. Understand 2. Do 3. Verify” | Not operational | Use domain phases (design, integrate, verify) |
| Omitting Verification checklist | Drifts to subjective “done” | 4+ concrete checkboxes |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [AWS — Agents for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html) — action groups, knowledge, deployment considerations
- [Model Context Protocol — specification](https://modelcontextprotocol.io/specification/latest) — how tools/resources map to agent capabilities
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — workflow vs autonomous loops, when to split agents
- [Google Cloud — Agent patterns](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — orchestrator, planner, tool-user taxonomy
