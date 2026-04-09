---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Pipeline Optimization

## Quick Reference

| Technique | Impact |
|-----------|--------|
| **Dependency cache** | npm/pip/maven restore |
| **Docker layer cache** | BuildKit, `--mount=type=cache` |
| **Parallel jobs** | Split lint/test/build |
| **Shallow clone** | `fetch-depth: 1` |
| **Skip CI** | `[skip ci]` only when policy allows |

**Measure:** Wall time per job; queue time.

**2025–2026:** Larger runners for heavy builds; self-hosted for GPU/custom.

## Patterns & Decision Matrix

| Bottleneck | Fix |
|------------|-----|
| Install every time | Lockfile + cache key |
| E2E slow | Shard matrix |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Cache without key on lockfile | Stale deps |

## Code Examples

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

## Deep Dive Sources

- [GitHub — Caching dependencies](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
