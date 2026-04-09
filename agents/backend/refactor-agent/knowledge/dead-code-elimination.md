---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Dead Code Elimination

## Quick Reference

| Approach | Tool / idea |
|----------|-------------|
| **Unused exports** | ts-prune, knip, ESLint unused-imports |
| **Unreachable** | Compiler / coverage |
| **Feature flags** | Remove stale branches |
| **Deprecate then delete** | Two-release cycle for public API |

**2025–2026:** `knip` for TS monorepos; verify with CI grep for references.

## Patterns & Decision Matrix

| Code | Action |
|------|--------|
| Clearly unused private | Delete |
| Public export maybe used | Search consumers, semver |

## Anti-Patterns

| Risk | Mitigation |
|------|------------|
| Delete still-used via reflection | Grep + integration tests |

## Code Examples

```bash
npx knip
npx ts-prune
```

## Deep Dive Sources

- [knip](https://knip.dev/)
- [ts-prune](https://github.com/nadeesha/ts-prune)
