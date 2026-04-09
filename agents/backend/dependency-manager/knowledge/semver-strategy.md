---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Semver Strategy

## Quick Reference

| Bump | Meaning |
|------|---------|
| **MAJOR** | Breaking API |
| **MINOR** | Backward-compatible features |
| **PATCH** | Bug fixes |

**Ranges:** `^1.2.0` allows minor/patch; `~1.2.0` patch only (npm).

**2025–2026:** Lockfile (`package-lock.json`, `poetry.lock`) is source of truth for CI reproducibility.

## Patterns & Decision Matrix

| Library type | Pinning |
|--------------|---------|
| App | Lockfile + semver range in package.json |
| Library you publish | Strict semver; changesets/release-please |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| `*` or `latest` in apps | Nondeterministic builds |

## Code Examples

```json
{ "dependencies": { "lodash": "^4.17.21" } }
```

## Deep Dive Sources

- [semver.org](https://semver.org/)
- [npm — package.json dependencies](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#dependencies)
