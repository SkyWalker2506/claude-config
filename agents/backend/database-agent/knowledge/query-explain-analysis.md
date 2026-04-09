---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Query EXPLAIN Analysis

## Quick Reference

| Node | Meaning |
|------|---------|
| **Seq Scan** | Full table read — OK for tiny tables or wide selects |
| **Index Scan** | Index used to find rows |
| **Index Only Scan** | Index covers query (visibility map permitting) |
| **Nested Loop** | For each outer row, scan inner — OK if inner is index probe |
| **Hash Join** | Build hash of one side — good for equi-joins |
| **Bitmap Heap Scan** | Multiple indexes combined |

**Key metrics:** `actual time`, `rows`, `loops`, `Buffers: shared hit/read`.

**2025–2026:** `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` on staging with production-like stats.

## Patterns & Decision Matrix

| Symptom | Investigate |
|---------|-------------|
| High `rows` estimate vs actual | Statistics — `ANALYZE` |
| Seq Scan on big table | Missing index or selective filter |
| Nested Loop with huge loops | Join order / stats |

## Code Examples

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.*
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE c.region = 'EU' AND o.created_at > now() - interval '7 days';
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Tuning without production volume | Use anonymized prod snapshot or `pg_stat_statements` |
| Only looking at cost not buffers | I/O dominates at scale |

## Deep Dive Sources

- [PostgreSQL — EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [Use The Index, Luke — EXPLAIN](https://use-the-index-luke.com/sql/explain-plan/)
