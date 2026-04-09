---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Pipeline Design

## The Standard Pipeline

```
define → plan → build → verify → review → ship
```

This is the backbone. Variants modify phases but keep the flow.

## Phase Breakdown

### Define (specify)
- Input: natural language description
- Output: spec.md with requirements, user stories, success criteria
- Gate: spec quality checklist passes

### Plan (plan + tasks)
- Input: spec.md
- Output: plan.md (architecture), tasks.md (ordered task list)
- Gate: all tasks have IDs, file paths, dependencies marked

### Build (implement)
- Input: plan.md + tasks.md
- Output: working code, committed incrementally
- Pattern: phase-by-phase, TDD optional, parallel where possible
- Gate: all tasks marked [X]

### Verify (test + debug)
- Input: built code
- Output: passing tests, clean build
- Loop: fail → debug → fix → verify (max 3 iterations)

### Review (review)
- Input: completed changes
- Output: scored review (correctness, readability, architecture, security, performance)
- Gate: no Critical findings, Important findings addressed

### Ship (ship)
- Input: reviewed code
- Output: merged PR, deployed artifact

## Pipeline Variants

### Spec-Heavy (complex features)
```
define → clarify → plan → checklist → tasks → implement → review → ship
```
Extra: clarify resolves ambiguities, checklist validates before build.

### Hotfix (urgent bugs)
```
reproduce → fix → test → review → ship
```
Skip define/plan — scope is already known.

### Refactor
```
audit → plan → implement (with tests) → verify → review
```
Start with code analysis, not feature spec.

### Spike/Research
```
define question → research → prototype → report
```
No ship phase — output is knowledge, not production code.

## Phase Composition Rules

1. **Each phase has clear input/output** — no implicit data passing
2. **Gates between phases** — never auto-advance without validation
3. **Phases are independently restartable** — crash in build shouldn't lose plan
4. **Artifacts are files** — spec.md, plan.md, tasks.md (not in-memory only)
5. **Hooks are optional** — before/after any phase for extensibility

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Monolith pipeline | Everything in one pass | Split into phases with gates |
| Missing gates | Bad input propagates | Add validation between phases |
| No artifacts | Can't restart or review | Write phase outputs to files |
| Rigid pipeline | Can't skip unnecessary phases | Make phases composable |
