---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# DTO Mapping Patterns

## Quick Reference

| Layer | Name | Exposed to wire? |
|-------|------|------------------|
| Entity / domain | Rich model, invariants | No |
| DTO / API model | Serialized JSON | Yes |
| Persistence model | ORM row / document | No |

**Mapping styles:** Manual functions, MapStruct (Java), `automapper` (C#), `pydantic` parse (Python), explicit `toResponse()` in TS.

**2025–2026:** Prefer **explicit mapping** for public APIs — codegen from OpenAPI catches drift.

## Patterns & Decision Matrix

| Situation | Approach |
|-----------|----------|
| Same shape, different names | Thin mapper |
| Nested aggregates | Map aggregate root only; hide internals |
| Lists with PII | Separate `PublicUser` vs `InternalUser` types |
| Version bump | `UserV2Response` parallel to V1 |

## Code Examples

**TypeScript — explicit DTO:**

```typescript
export function toOrderResponse(row: OrderRow): OrderResponse {
  return {
    id: row.id,
    status: row.status,
    totalCents: row.total_cents,
  };
}
```

**Input validation separate from entity:**

```typescript
const CreateOrderSchema = z.object({ customerId: z.string(), lines: z.array(LineSchema) });
```

## Anti-Patterns

| Mistake | Risk |
|---------|------|
| ORM entity returned from controller | Leaky schema, lazy-load leaks |
| One DTO for admin + public | Over-exposure |
| Silent `any` mapping | Breaking API without compile error |

## Deep Dive Sources

- [Eric Evans — DDD reference](https://www.domainlanguage.com/ddd/) — bounded context and models
- [MapStruct — Java bean mapping](https://mapstruct.org/)
- [Zod — TypeScript schema validation](https://zod.dev/)
