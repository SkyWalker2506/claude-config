---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Safe Refactoring Workflow

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Ensure tests pass baseline |
| 2 | One mechanical change (rename, extract) |
| 3 | Run tests |
| 4 | Commit (small) |
| 5 | Repeat |

**Branch:** `refactor/` or short-lived; avoid mixing with features.

**2025–2026:** Type system catches renames; use compiler for safety.

## Patterns & Decision Matrix

| Risk | Mitigation |
|------|------------|
| Untested legacy | Characterization tests (B6) |
| Public API | Deprecation cycle |

## Code Examples

```bash
git checkout -b refactor/extract-pricing
# extract + test
git commit -m "refactor: extract pricing module"
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| 50 files one commit | Incremental PRs |

## Deep Dive Sources

- [Working Effectively with Legacy Code — Feathers](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)
