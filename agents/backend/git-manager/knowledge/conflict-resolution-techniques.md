---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Conflict Resolution Techniques

## Quick Reference

| Step | Action |
|------|--------|
| 1 | `git status` — which files |
| 2 | Open markers `<<<<<<<` `=======` `>>>>>>>` |
| 3 | Choose or combine; remove markers |
| 4 | Test; `git add` |

**Tools:** `git mergetool`, VS Code merge editor, `git diff --cc`.

**2025–2026:** Lockfile conflicts — often regenerate (`npm install`) vs manual merge.

## Patterns & Decision Matrix

| File | Strategy |
|------|----------|
| Generated lock | Regenerate |
| Source | Understand both sides |

## Code Examples

```bash
git checkout --ours package-lock.json   # or regenerate: rm -rf node_modules && npm install
git add package-lock.json
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Accept both blindly | Duplicate logic |

## Deep Dive Sources

- [Git — Basic merge conflicts](https://git-scm.com/docs/git-merge#_how_conflicts_are_presented)
