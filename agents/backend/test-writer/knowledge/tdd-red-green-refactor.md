---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# TDD: Red-Green-Refactor

## Quick Reference

| Phase | Action |
|-------|--------|
| **Red** | Write failing test for desired behavior |
| **Green** | Minimal code to pass |
| **Refactor** | Clean up with tests green |

**Outside-in vs inside-out:** Acceptance test drives features; unit tests for modules.

**2025–2026:** Still valid for libraries and pure logic; for UI spikes, prototype then add tests.

## Patterns & Decision Matrix

| Code type | TDD fit |
|-----------|---------|
| Pure functions, parsers | Excellent |
| Exploratory UI | Test after shape stabilizes |
| Bug fix | Regression test first (always red first) |

## Code Examples

```text
1. test('parses ISO date') → fails
2. implement parseIso → passes
3. rename / extract → still passes
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Writing production before test | Loses red phase value |
| Huge steps | Smaller tests |

## Deep Dive Sources

- [Kent Beck — Test Driven Development](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Martin Fowler — TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
