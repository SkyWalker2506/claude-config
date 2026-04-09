---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Refactoring Catalog (Fowler)

## Quick Reference

| Name | Mechanism |
|------|-----------|
| **Extract Method** | Split long method |
| **Move Method** | Belongs elsewhere |
| **Replace Conditional with Polymorphism** | Switch on type |
| **Introduce Parameter Object** | Many params |
| **Preserve Whole Object** | Pass object not fields |

**Workflow:** Small steps, tests green after each (when possible).

**2025–2026:** Automated refactors in IDEs (WebStorm, VS Code) reduce risk.

## Patterns & Decision Matrix

| Smell | First refactor |
|-------|----------------|
| Long method | Extract |
| Feature envy | Move method |
| Duplicated branches | Consolidate + polymorphism |

## Code Examples

```typescript
// Before: long
function checkout(cart: Cart) { /* 80 lines */ }

// After: extract
function validate(cart: Cart) { ... }
function charge(cart: Cart) { ... }
function checkout(cart: Cart) { validate(cart); charge(cart); }
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Big-bang refactor | Hard to review and bisect |

## Deep Dive Sources

- [Refactoring.com Catalog](https://refactoring.com/catalog/)
- [Martin Fowler — Refactoring Book](https://martinfowler.com/books/refactoring.html)
