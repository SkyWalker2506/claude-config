---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Regression Detection

## Quick Reference

| Layer | Detection |
|-------|-----------|
| **Automated** | CI test suite on every PR |
| **Canary** | Small traffic slice before full roll |
| **Synthetic** | Ping critical path every N minutes |
| **Metrics** | SLO burn rate alerts |

**Definition:** Old bug reappears after fix — blocked by regression test tied to ticket.

**2025–2026:** Feature flags kill-switch; progressive delivery.

## Patterns & Decision Matrix

| Risk | Mitigation |
|------|------------|
| Hotfix without test | Follow-up ticket mandatory |
| Flaky test ignored | Quarantine + fix SLA |

## Code Examples

```typescript
// issue BUG-42 — regression
it('rejects negative quantity (BUG-42)', () => {
  expect(() => addLine({ qty: -1 })).toThrow();
});
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| Same class of bug twice | Category test + lint rule |

## Deep Dive Sources

- [Google — Canary releases](https://cloud.google.com/architecture/canary-deployments-overview)
- [Martin Fowler — Feature Toggles](https://martinfowler.com/articles/feature-toggles.html)
