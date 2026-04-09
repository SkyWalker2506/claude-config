---
last_updated: 2026-04-09
refined_by: cursor
confidence: medium
---

# Report Generator Anti-Patterns

## Best practices
- Prefer small, composable steps for Report Generator.
- Make failure modes explicit.
- Write down assumptions and verification upfront.

## Patterns

| Situation | Recommended pattern | Why |
|----------|----------------------|-----|
| Unknown scope | Start with inventory + minimal repro | Avoid premature optimization |
| Risky change | Feature-flag / rollback plan | Reduce blast radius |
| Repeated tasks | Script the workflow | Consistency and speed |

### Example snippet

```bash
# Capture context quickly
git status
git diff
```

## Anti-patterns
- Changing multiple concerns in one step.
- Skipping verification because it "looks right".
- Writing docs that drift from reality.

## Decision checklist
- [ ] Do we have clear acceptance criteria?
- [ ] What can break and how do we roll back?
- [ ] What is the minimal safe change?
- [ ] How will we verify success?
