---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Database Query Optimization

## Quick Reference

| Action | Effect |
|--------|--------|
| Add selective index | Reduce seq scan |
| Reduce selected columns | Less I/O |
| Batch inserts | Round-trip cost |
| Connection pool tuning | Wait time |

**Coordination:** B5 owns schema/index migrations; B12 profiles end-to-end.

**2025–2026:** `pg_stat_statements` for top queries; prepared statements for hot paths.

## Patterns & Decision Matrix

| Issue | First step |
|-------|------------|
| Slow query | EXPLAIN ANALYZE (B5 doc) |
| Connection wait | Pool sizing |

## Code Examples

```sql
-- Add covering index for hot query
CREATE INDEX CONCURRENTLY idx_orders_t ON orders (tenant_id, created_at DESC);
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| N+1 sorgu | Gecikme |
| Select * büyük tabloda | I/O şişmesi |

## Deep Dive Sources

- [PostgreSQL — Performance tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
