---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Merge vs Rebase Decision

## Quick Reference

| Op | Result |
|----|--------|
| **merge** | Preserves history; merge commit |
| **rebase** | Linear history; rewrites commits |
| **squash merge** | One commit on main (GitHub PR) |

**Rule:** Never rebase commits already pushed that others built on — use `git pull --rebase` only on **your** branch tip.

**2025–2026:** Default squash merge on GitHub for cleaner main.

## Patterns & Decision Matrix

| Situation | Prefer |
|-----------|--------|
| Shared branch | Merge |
| Private feature branch before PR | Rebase onto main |

## Code Examples

```bash
git fetch origin && git rebase origin/main
# if conflict: fix files → git add → git rebase --continue
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Force push to shared main | Destroys collaboration |

## Deep Dive Sources

- [Git Book — Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [GitHub — About merge methods](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges)
