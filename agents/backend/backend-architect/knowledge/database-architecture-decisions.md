---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Database Architecture Decisions

## Quick Reference

| Store class | Examples | Sweet spot |
|-------------|----------|------------|
| **Relational (OLTP)** | PostgreSQL, MySQL, SQL Server | ACID transactions, joins, constraints |
| **Document** | MongoDB, Firestore | Flexible schema, nested docs, horizontal scale |
| **Key-value** | Redis, DynamoDB | Sessions, caches, idempotency keys |
| **Column / wide-column** | Cassandra, Bigtable | Time series, massive write spread |
| **Search** | Elasticsearch, OpenSearch | Full-text, facets (not primary OLTP) |
| **Warehouse** | BigQuery, Snowflake, Redshift | Analytics, ETL — not serving path for OLTP |

**2025–2026:** PostgreSQL remains default for new OLTP on most stacks; managed offerings (RDS, AlloyDB, Aurora) dominate ops strategy.

## Patterns & Decision Matrix

| Question | If “yes” tends toward… | If “no” tends toward… |
|----------|------------------------|------------------------|
| Need multi-row ACID transactions? | RDBMS | Reconsider denormalization cost |
| Schema changes weekly with different tenants? | Document or per-tenant schema | Strict migrations on RDBMS |
| Globally low-latency reads, eventual OK? | Regional replicas + cache | Single-region strong consistency |
| Full-text is core product feature? | Dedicated search index + sync | `tsvector` in PG for smaller scale |
| Team knows ops for chosen DB? | That stack | Training budget or managed service |

**Polyglot persistence:** Use **different stores for different bounded contexts** — avoid duplicating the same truth in two OLTP systems without sync strategy.

## Code Examples

**Postgres constraints (integrity at DB layer):**

```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
CREATE UNIQUE INDEX ux_orders_external ON orders (external_id) WHERE deleted_at IS NULL;
```

**Idempotency key pattern (API + KV/DB):**

```text
Header: Idempotency-Key: <uuid>
→ Store (key, request_hash, response) with TTL 24h
→ Replay same response on duplicate
```

## Anti-Patterns

| Anti-pattern | Risk | Mitigation |
|--------------|------|------------|
| Elasticsearch as source of truth for money | Lost updates, no cross-doc TX | RDBMS primary; ES secondary |
| Max connections per app instance to DB | Connection storms | PgBouncer / RDS Proxy, pool sizing |
| BIGINT primary keys everywhere without plan | Migration pain | UUID vs snowflake — decide early |

## Deep Dive Sources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/) — DDL, indexing, replication
- [AWS — Purpose-built databases](https://aws.amazon.com/products/databases/) — when to pick which family
- [Martin Fowler — PolyglotPersistence](https://martinfowler.com/bliki/PolyglotPersistence.html) — trade-offs narrative
- [Google — Spanner — TrueTime and external consistency](https://cloud.google.com/spanner/docs/true-time-external-consistency) — strong global consistency model (reference)
