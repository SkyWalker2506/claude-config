---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Mocking vs Integration Tests

## Quick Reference

| Term | Meaning |
|------|---------|
| **Mock** | Asserts interactions; behavior verification |
| **Stub** | Returns canned data |
| **Fake** | Working lightweight impl (e.g. in-memory DB) |
| **Integration** | Real dependency (Testcontainers DB, WireMock) |

**Rule of thumb:** Mock **out** boundaries you do not own (payment API); integrate **with** DB/schema you ship.

**2025–2026:** Testcontainers popular for JVM/Node/Go; `docker compose` in CI for parity.

## Patterns & Decision Matrix

| Boundary | Test with |
|----------|-----------|
| Pure logic | Unit + mocks not needed |
| Repository | Integration with real DB or Testcontainers |
| External HTTP | Mock server or recorded fixtures |

## Code Examples

```typescript
// Jest mock module
jest.mock('../payments');
import { charge } from '../payments';
test('orders', async () => {
  (charge as jest.Mock).mockResolvedValue({ id: 'ch_1' });
});
```

## Anti-Patterns

| Smell | Fix |
|-------|-----|
| Mocking the system under test | Test real class |
| Integration without cleanup | Truncate tables / transactions per test |

## Deep Dive Sources

- [Martin Fowler — Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Testcontainers](https://testcontainers.com/)
- [Prisma — Testing guide](https://www.prisma.io/docs/guides/testing)
