---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Testing Pyramid Strategy

## Quick Reference

| Layer | Count | Speed | Scope |
|-------|-------|-------|-------|
| **Unit** | Many | ms | Single class/function |
| **Integration** | Some | sec | DB, queue, real deps |
| **E2E** | Few | min | Full stack, browser/API |

**Mike Cohn pyramid:** Wide base of unit tests; narrow top of UI E2E.

**2025–2026:** Contract tests (Pact) between services sit beside integration; snapshot tests for UI where stable.

## Patterns & Decision Matrix

| Goal | Emphasis |
|------|----------|
| Fast feedback on refactor | Unit |
| Migration correctness | Integration against real DB |
| User journey | E2E (critical paths only) |

## Code Examples

```typescript
describe('pricing', () => {
  it('applies discount', () => {
    expect(applyDiscount(100, 0.1)).toBe(90);
  });
});
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| E2E for every branch | Slow, flaky |
| No integration — only mocks | Misses SQL/serialization bugs |

## Deep Dive Sources

- [Martin Fowler — TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Google Testing Blog](https://testing.googleblog.com/) — flakiness, hermetic tests
- [Test Automation Pyramid (Selenium)](https://www.selenium.dev/documentation/test_practices/overview/)
