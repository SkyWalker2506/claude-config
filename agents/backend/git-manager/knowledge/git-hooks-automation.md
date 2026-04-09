---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Git Hooks Automation

## Quick Reference

| Hook | Typical use |
|------|-------------|
| **pre-commit** | lint-staged, format |
| **commit-msg** | Conventional commits |
| **pre-push** | tests (optional — can be slow) |

**husky (Node):** `.husky/pre-commit`. **core.hooksPath** for custom dir.

**2025–2026:** Run fast checks locally; heavy CI in GitHub Actions.

## Patterns & Decision Matrix

| Check | Where |
|-------|-------|
| Format | pre-commit |
| Full test | CI |

## Code Examples

```bash
# .husky/pre-commit
pnpm exec lint-staged
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| 10 min pre-commit | Developers skip hooks |

## Deep Dive Sources

- [Git — Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Husky](https://typicode.github.io/husky/)
