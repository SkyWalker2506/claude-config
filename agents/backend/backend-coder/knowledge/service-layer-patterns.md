---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Service Layer Patterns

## Quick Reference

| Style | Description |
|-------|-------------|
| **Transaction script** | One service method = one use case script |
| **Domain service** | Pure domain logic when not fitting one entity |
| **Application service** | Orchestrates domain + infra (repos, messaging) |

**Dependencies:** Service → repository interfaces; avoid service→service chains for same aggregate.

**2025–2026:** Hexagonal / ports-adapters still common; “use case” per class in clean architecture tutorials.

## Patterns & Decision Matrix

| Question | Guidance |
|----------|------------|
| Where goes validation? | Input at boundary; invariants in domain |
| Cross-aggregate operation | Single application service + domain events or saga (B1) |
| Idempotency | At application boundary (key + store) |

## Code Examples

```typescript
// application/PlaceOrder.ts
export async function placeOrder(cmd: PlaceOrderCommand, deps: Deps): Promise<OrderId> {
  return deps.db.transaction(async (tx) => {
    const customer = await deps.customers.get(cmd.customerId, tx);
    const order = Order.create(customer, cmd.lines);
    await deps.orders.save(order, tx);
    await deps.events.publish(order.domainEvents, tx);
    return order.id;
  });
}
```

## Anti-Patterns

| Smell | Fix |
|-------|-----|
| God service 2000 lines | Split by use case / bounded context |
| Service calling ORM everywhere | Repository abstraction |
| Business rules in controller | Move to domain or application |

## Deep Dive Sources

- [Martin Fowler — Service Layer](https://martinfowler.com/eaaCatalog/serviceLayer.html)
- [Microsoft — Application layer patterns](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)
- [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/) — services vs entities
