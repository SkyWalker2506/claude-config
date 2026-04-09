---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Lockfile Management

## Quick Reference

| File | Ecosystem |
|------|-----------|
| `package-lock.json` | npm |
| `yarn.lock` | Yarn |
| `pnpm-lock.yaml` | pnpm |
| `poetry.lock` | Poetry |
| `Cargo.lock` | Rust (committed for apps) |

**Rule:** Commit lockfile for applications; libraries may omit depending on policy.

**2025–2026:** `npm ci` in CI (not `npm install`) for strict lock adherence.

## Patterns & Decision Matrix

| Conflict | Resolution |
|----------|------------|
| Merge conflict in lock | Regenerate: delete node_modules + lock + `npm install` |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Hand-edit lock | Corrupt graph |

## Code Examples

```bash
npm ci
# exact install from package-lock.json in CI
```

## Deep Dive Sources

- [npm — package-lock.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json)
