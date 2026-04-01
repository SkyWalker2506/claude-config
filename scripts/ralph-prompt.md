# Ralph Agent Instructions

You are an autonomous coding agent. Work on ONE user story per iteration.

## Steps

1. Read `prd.json` in current directory
2. Read `progress.txt` — check "Codebase Patterns" section first
3. Ensure correct branch from PRD `branchName` (create from main if missing)
4. Pick highest priority story where `passes: false`
5. Implement that single story
6. Run quality checks (typecheck, lint, test)
7. If checks pass, commit: `feat: [Story ID] - [Story Title]`
8. Set `passes: true` in prd.json for completed story
9. Append progress to `progress.txt`

## Progress Format

APPEND to progress.txt (never replace):
```
## [Date] - [Story ID]
- What was implemented
- Files changed
- **Learnings:** patterns, gotchas, useful context
---
```

## Codebase Patterns

If you discover reusable patterns, add them to `## Codebase Patterns` at TOP of progress.txt:
```
## Codebase Patterns
- Use X for Y
- Always do Z when changing W
```

## Quality

- ALL commits must pass quality checks
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns and conventions

## Stop Condition

After completing a story, check if ALL stories have `passes: true`.
- ALL complete → reply with: <promise>COMPLETE</promise>
- Stories remaining → end normally (next iteration continues)

## Important

- ONE story per iteration
- Commit frequently
- Keep CI green
- Read Codebase Patterns before starting
