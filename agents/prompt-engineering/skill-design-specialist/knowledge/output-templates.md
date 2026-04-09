---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Output Templates — Structured Output Formats

## Why Output Templates Matter

A skill without a defined output format produces inconsistent results. The agent guesses what to show, leading to verbose or incomplete output. Define the exact shape.

## Common Output Patterns

### 1. Status Table (for scan/list skills)
```
Degisiklik olan repolar (3/12):

  CoinHQ          — 3 modified, 1 untracked
  ArtLift         — 5 modified, 2 deleted
  claude-config   — 1 untracked

Devam? (enter = evet, n = iptal)
```
Use when: listing items with status, showing scan results.

### 2. Phase Progress (for multi-step skills)
```
Phase 1: Analysis ✓
Phase 2: Sprint Plan ✓
Phase 3: Implementation (3/5 tasks done)
Phase 4: Review — waiting
```
Use when: forge-style multi-phase workflows.

### 3. Diff Preview (for refine/edit skills)
```
--- CLAUDE.md (before)
+++ CLAUDE.md (after)
@@ -12,3 +12,2 @@
- Gereksiz satir
  Kalan satir
```
Use when: showing proposed changes before applying.

### 4. Decision Prompt (for interactive skills)
```
3 options found:

  [1] Use existing API — low effort, limited features
  [2] Build custom — high effort, full control
  [3] Hybrid approach — medium effort, good coverage

Select (1-3):
```
Use when: the skill needs user choice.

### 5. JSON Output (for machine-consumed results)
```json
{
  "status": "success",
  "tasks_completed": 5,
  "tasks_failed": 0,
  "details": [...]
}
```
Use when: output feeds another skill or script.

## Template Rules

1. **Specify the exact format in SKILL.md** — don't leave it to interpretation
2. **Use code blocks** for structured output so the agent reproduces it literally
3. **Include a real example** with realistic data, not `[placeholder]`
4. **Define empty states** — what to show when there are zero results
5. **Gate destructive actions** — always show preview + confirmation before writes/commits

## Spec-Kit Influence

The spec-kit templates (spec-template.md, plan-template.md, tasks-template.md) use a fill-in format with `[PLACEHOLDER]` markers and HTML comments for instructions. This works well for document generation skills but is too heavy for operational skills. Match template weight to skill complexity.
