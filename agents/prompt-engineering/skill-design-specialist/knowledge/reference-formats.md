---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Reference Formats — Cross-System Comparison

## Three Reference Systems

### 1. Google Agent-Skills (agent-skills repo)

**Structure:** `skills/<skill-name>/SKILL.md`
**Frontmatter:** `name`, `description`
**Sections:** Overview → When to Use → Core Content (varies) → Summary
**Style:** Long-form English prose, 100-300 lines, educational tone
**Strength:** Deep frameworks (5-axis review, 4-phase gated workflow), "When NOT to use"
**Weakness:** Verbose, no argument parsing, no explicit output format

Example pattern — the gated workflow:
```
SPECIFY → PLAN → TASKS → IMPLEMENT
   ↓        ↓       ↓        ↓
 Review   Review  Review   Review
```

### 2. Spec-Kit (spec-kit repo)

**Structure:** `templates/<type>-template.md`
**Templates:** spec, plan, tasks, checklist, agent-file, constitution
**Style:** Fill-in documents with `[PLACEHOLDER]` markers and `<!-- HTML comments -->` for instructions
**Strength:** Standardized document generation, prioritized user stories (P1/P2/P3)
**Weakness:** Heavy for operational skills, designed for document output not terminal workflows

Key innovation — independent testability per user story:
```markdown
### User Story 1 (P1)
**Independent Test**: Can be fully tested by [action] and delivers [value]
**Acceptance**: Given [X], When [Y], Then [Z]
```

### 3. Our Skills (claude-config/global/skills/)

**Structure:** `skills/<skill-name>/SKILL.md`
**Frontmatter:** `name`, `description` (with triggers), `argument-hint`
**Sections:** Title → Usage → Argument Parsing → Flow (numbered) → Output → Boundaries
**Style:** Turkish prose, English code, 40-120 lines, operational tone
**Strength:** Dense, argument parsing tables, explicit output format, trigger keywords
**Weakness:** Sometimes missing error paths, boundary sections inconsistent

## What to Adopt from Each

| From | Adopt | How |
|------|-------|-----|
| Agent-Skills | "When NOT to Use" section | Add to every skill |
| Agent-Skills | Assumption surfacing blocks | Phase 0 pre-flight |
| Agent-Skills | Push-back guidance | Include in complex skills |
| Spec-Kit | Prioritized acceptance criteria | For PRD/spec skills |
| Spec-Kit | Independent testability | For feature planning skills |
| Our format | Trigger keywords in description | Keep — enables discovery |
| Our format | Argument parsing tables | Keep — handles complex args |
| Our format | Explicit "Ne yapmaz" section | Strengthen — add to all |
