---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Reference Implementations

## 1. agent-skills (github.com/anthropics/agent-skills)

A collection of production-grade engineering skills for AI coding agents.

### Architecture
```
skills/           → Core skills (SKILL.md per directory)
agents/           → Reusable agent personas
hooks/            → Session lifecycle hooks
.claude/commands/ → Slash commands (/spec, /plan, /build, etc.)
references/       → Supplementary checklists
```

### Skills by Phase
| Phase | Skills |
|-------|--------|
| Define | spec-driven-development |
| Plan | planning-and-task-breakdown |
| Build | incremental-implementation, TDD, context-engineering, frontend-ui, api-design |
| Verify | browser-testing, debugging-and-error-recovery |
| Review | code-review, code-simplification, security, performance |
| Ship | git-workflow, ci-cd, deprecation, documentation, shipping |

### Key Patterns
- **SKILL.md format**: YAML frontmatter (name, description) + structured sections (Overview, When to Use, Process, Red Flags, Verification)
- **Agent personas**: Role-specific system prompts (code-reviewer, security-auditor, test-engineer)
- **Context hierarchy**: 5-level loading from rules files to conversation history
- **No duplication**: Skills reference each other, never copy content

## 2. spec-kit (Specification-Driven Development)

Implements SDD — specifications drive code, not the other way around.

### Core Workflow
```
/speckit.specify → Feature spec with auto-numbering, branch creation
/speckit.plan    → Implementation plan from spec
/speckit.tasks   → Executable task list from plan
```

### Template System
- `spec-template.md` — Feature specification (WHAT, not HOW)
- `plan-template.md` — Implementation plan with phase gates
- `tasks-template.md` — Task breakdown with `[P]` parallel markers
- `constitution-template.md` — Immutable architectural principles

### Key Innovations
- **Forced uncertainty markers**: `[NEEDS CLARIFICATION]` prevents LLM guessing
- **Constitutional gates**: Pre-implementation checks enforce simplicity/anti-abstraction
- **Template-as-prompt**: Templates constrain LLM output toward quality
- **Bidirectional feedback**: Production metrics update specifications

## 3. claude-config (Internal)

Centralized Claude Code configuration management.

### Architecture
- `agents/` — Agent definitions with AGENT.md + knowledge/ + memory/
- `global/skills/` — Shared skills across all projects
- `install.sh` — Bootstraps entire ecosystem
- Redirector pattern: project CLAUDE.md → config CLAUDE.md

### Patterns Worth Noting
- **Knowledge-First agents**: Agent reads knowledge index before acting
- **Layered install**: Stacks (general, flutter, unity) compose features
- **Ecosystem sync**: Changes cascade to all downstream READMEs

## 4. Open Source Landscape

| Project | Pattern | Notable Feature |
|---------|---------|----------------|
| OpenAI Agents SDK | Handoff functions | Production Swarm successor |
| LangGraph | State machine graphs | Checkpointing, streaming |
| CrewAI | Role-based crews | Fastest prototyping |
| AutoGen/AG2 | Conversational agents | Multi-party debate |
| Mastra | TypeScript agent framework | Tool-use focused |
| Semantic Kernel | .NET/Python orchestration | Enterprise integration |

## Patterns Across All Implementations

1. **Agents need identity**: Role, goal, constraints — not just "be helpful"
2. **Skills are reusable**: Separate skill definitions from agent definitions
3. **Context is layered**: Global → project → task → iteration
4. **Files as communication**: Filesystem is the universal message bus
5. **Templates constrain quality**: Structure prevents LLM drift
