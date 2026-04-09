---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# GraphQL Schema Design

## Quick Reference

| Concept | Role |
|---------|------|
| **Schema** | Types, queries, mutations, subscriptions |
| **Resolver** | Field → data (watch N+1) |
| **DataLoader** | Batch + cache per request |
| **Pagination** | Relay cursor (`first`/`after`) or offset |

**Nullability:** Non-null (`!`) only when truly always present — fewer client crashes.

**2025–2026:** Federation (Apollo, GraphQL Mesh) for multi-subgraph; complexity/cost limits standard in production.

## Patterns & Decision Matrix

| Need | Pattern |
|------|---------|
| Avoid over-fetching | Client selects fields |
| N+1 on lists | DataLoader batch in resolver |
| Breaking change | `@deprecated` + codegen + sunset date |
| File upload | Often separate REST + URL field in mutation |

## Code Examples

```graphql
type Order {
  id: ID!
  totalCents: Int!
  lines: [OrderLine!]!
}

type Query {
  order(id: ID!): Order
}

type Mutation {
  placeOrder(input: PlaceOrderInput!): PlaceOrderPayload!
}
```

```typescript
// DataLoader sketch
const userLoader = new DataLoader(async (ids: string[]) => db.users.findByIds(ids));
```

## Anti-Patterns

| Pitfall | Fix |
|---------|-----|
| GraphQL exposing raw SQL | Domain types + auth at resolver |
| Unbounded lists | Pagination + max `first` |
| No query depth/cost limit | Query complexity analysis |

## Deep Dive Sources

- [GraphQL — Learn](https://graphql.org/learn/)
- [Apollo — Federation](https://www.apollographql.com/docs/federation/)
- [GraphQL Cursor Connections Specification](https://relay.dev/graphql/connections.htm)
- [Shopify — GraphQL Design Tutorial](https://github.com/Shopify/graphql-design-tutorial) — public design guide
