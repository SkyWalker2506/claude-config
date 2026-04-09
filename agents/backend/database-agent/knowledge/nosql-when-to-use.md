---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# NoSQL: When to Use

## Quick Reference

| Store | Good fit | Weak fit |
|-------|----------|----------|
| **MongoDB** | Flexible doc, horizontal scale, nested data | Multi-doc ACID across many collections (improving but complex) |
| **Firestore** | Mobile sync, real-time listeners, GCP | Heavy ad-hoc joins, strong cross-collection transactions at scale |
| **DynamoDB** | Known access patterns, single-digit ms | Ad-hoc SQL analytics |
| **Redis** | Cache, rate limit, session | Primary durable source of financial truth |

**Rule:** NoSQL shines when **access patterns are fixed** and denormalization is acceptable.

**2025–2026:** MongoDB Atlas, Firestore, DynamoDB — prefer managed + backup/PITR policies.

## Patterns & Decision Matrix

| Need | Lean |
|------|------|
| Flexible schema per tenant | Document |
| Global low-latency key-value | Dynamo / Cosmos |
| Graph relationships | Graph DB or RDBMS with proper modeling — not “default document” |

## Code Examples

**Firestore composite index (concept):**

```text
Collection: orders
Query: where tenantId == X orderBy createdAt desc
→ requires composite index: tenantId ASC, createdAt DESC
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Mongo as relational with $lookup everywhere | Performance surprise |
| No TTL on cache keys in Redis | Memory blowup |

## Deep Dive Sources

- [MongoDB — Data Modeling Introduction](https://www.mongodb.com/docs/manual/core/data-modeling-introduction/)
- [Firestore — Data model](https://firebase.google.com/docs/firestore/data-model)
- [AWS — DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
