---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# PostgreSQL Indexing Guide

## Quick Reference

| Index type | When |
|------------|------|
| **B-tree** (default) | Equality, range, sort |
| **GIN** | `jsonb`, arrays, full-text `tsvector` |
| **GiST** | Geometric, full-text some cases |
| **BRIN** | Very large append-only time series |
| **Partial** | `WHERE deleted_at IS NULL` hot subset |

**Selectivity:** Index columns that shrink search space most (equality before range often).

**Write cost:** Every index = INSERT/UPDATE overhead.

**2025–2026:** `INCLUDE` columns for index-only scans; monitor bloat (`pg_stat_user_tables`, `reindex` strategy).

## Patterns & Decision Matrix

| Query pattern | Index |
|---------------|-------|
| `WHERE tenant_id = ? AND created_at > ?` | Composite `(tenant_id, created_at)` — column order matches filter |
| OR across columns | Often separate indexes + bitmap OR or rewrite |
| `ORDER BY x LIMIT n` with filter | Composite ending in `x` |

## Code Examples

```sql
CREATE INDEX CONCURRENTLY idx_orders_tenant_created
  ON orders (tenant_id, created_at DESC)
  WHERE status = 'open';

CREATE INDEX idx_users_email_lower ON users (lower(email));
```

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE tenant_id = $1;
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Index every column | Measure with EXPLAIN |
| Low-cardinality leading column | Reorder or partial index |
| Missing FK index | Add index on referencing column |

## Deep Dive Sources

- [PostgreSQL — Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Use The Index, Luke!](https://use-the-index-luke.com/) — SQL indexing guide
- [PostgreSQL Wiki — Index Types](https://wiki.postgresql.org/wiki/Index_types)
