---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Context Engineering

## Core Principle

Feed agents the right information at the right time. Too little → hallucination. Too much → lost focus.

## The L0/L1/L2 Layer Strategy

### L0 — Always Present (~100 lines)
Rules files loaded at session start. Highest leverage context.

Contents: tech stack, build commands, code conventions, boundaries, persona.
Example: CLAUDE.md, .cursorrules

### L1 — Task-Scoped (~200 lines)
Loaded when a specific task type begins.

Contents: relevant spec section, skill instructions, related source files.
Trigger: task detection, slash command, dispatch.

### L2 — On-Demand (variable)
Loaded only when a specific detail is needed.

Contents: full source file for editing, API docs, database schema.
Trigger: explicit request or pre-edit file read.

## Context Hierarchy (Persistence Order)

```
1. Rules Files (CLAUDE.md)      — always loaded
2. Spec / Architecture Docs     — per feature/session
3. Relevant Source Files         — per task
4. Error Output / Test Results   — per iteration
5. Conversation History          — accumulates, compacts
```

## Loading Strategies

### Selective Include (Preferred)
```
TASK: Add email validation
RELEVANT: src/routes/auth.ts, src/lib/validation.ts, tests/routes/auth.test.ts
PATTERN: See phone validation in validation.ts:45-60
CONSTRAINT: Use existing ValidationError class
```

### Brain Dump (Session Start)
Provide everything upfront in a structured block. Use for complex tasks.

### Hierarchical Summary (Large Projects)
Maintain a project map. Load only the relevant section per task.

## Lazy-Load Pattern

Don't read files until you need them:
1. Start with L0 rules only
2. Detect task type → load L1 skill + spec section
3. About to edit a file → read it (L2)
4. Test fails → read error output (L2)

## Cache Strategy

- **Rules files**: cache per session (don't re-read)
- **Source files**: cache per task (re-read if task changes)
- **Error output**: don't cache (always fresh)

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Context starvation | Load rules + relevant files before each task |
| Context flooding (>5K lines) | Include only task-relevant, aim <2K |
| Stale context | Fresh session when switching features |
| Missing examples | Include one example of the pattern to follow |
| Implicit knowledge | Write it in rules files — unwritten = nonexistent |

## Confusion Management

When context conflicts:
```
CONFUSION: Spec says REST, codebase uses GraphQL
Options: A) Follow spec  B) Follow codebase  C) Ask
→ Surface to user, don't silently pick
```

When requirements are incomplete:
1. Check existing code for precedent
2. If no precedent → stop and ask
3. Never invent requirements
