---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Code Smells Detection

## Quick Reference

| Smell | Indicator |
|-------|-----------|
| **Long method** | >20-30 lines doing many things |
| **Large class** | God object |
| **Feature envy** | Method uses other class data more |
| **Primitive obsession** | String for money, status codes |
| **Shotgun surgery** | One change touches many files |

**Tools:** ESLint complexity, SonarQube, RuboCop, pylint.

**2025–2026:** AI-assisted refactor — still needs tests and review.

## Patterns & Decision Matrix

| Smell | Safe first step |
|-------|-----------------|
| Duplication | Extract function |
| Long parameter list | Parameter object |

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Refactor without tests | Add characterization tests first |

## Code Examples

```typescript
// Before: long method → extract
function total() { return subtotal() + tax(); }
```

## Deep Dive Sources

- [Refactoring Guru — Code smells](https://refactoring.guru/refactoring/smells)
- [SonarQube rules](https://rules.sonarsource.com/)
