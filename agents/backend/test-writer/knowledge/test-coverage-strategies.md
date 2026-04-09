---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Test Coverage Strategies

## Quick Reference

| Metric | Tool examples | Interpretation |
|--------|---------------|----------------|
| **Line coverage** | Istanbul (nyc), JaCoCo, coverage.py | Lines executed |
| **Branch coverage** | Same | if/else both sides |
| **Mutation testing** | Stryker, PIT | Tests actually assert behavior |

**Targets:** 80% line org-wide is common — but **critical paths** matter more than global %.

**2025–2026:** Exclude generated files in `coverage.yml`; upload to Codecov/Coveralls in CI.

## Patterns & Decision Matrix

| Situation | Action |
|-----------|--------|
| New feature | Cover happy + main error paths |
| Legacy untested module | Characterization tests before refactor |
| Low % but high risk | Add tests where incidents occurred |

## Code Examples

```json
// package.json nyc
{ "nyc": { "exclude": ["**/*.d.ts", "dist/**"] } }
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Testing only for coverage % | Meaningless asserts |
| Ignoring flaky tests | Green builds lie |

## Deep Dive Sources

- [Istanbul — nyc](https://github.com/istanbuljs/nyc)
- [Stryker Mutator](https://stryker-mutator.io/)
- [Google — Test sizes](https://testing.googleblog.com/2010/12/test-sizes.html)
