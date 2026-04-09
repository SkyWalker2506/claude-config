---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Zero-Downtime Migrations

## Quick Reference

| Phase | Action |
|-------|--------|
| 1 | Add new column nullable / new table (backward compatible) |
| 2 | Dual-write or backfill in batches |
| 3 | Switch reads |
| 4 | Remove old column (after deploy window) |

**Expand/contract:** Schema **expands** in release N; **contracts** in N+k.

**Locks:** `ALTER TABLE ... ADD COLUMN` cheap in PG 11+ (nullable default). Avoid rewriting table in peak — use `CONCURRENTLY` for indexes.

**2025–2026:** Tools: `gh-ost`, `pt-online-schema-change` (MySQL); PG favors native + concurrent index.

## Patterns & Decision Matrix

| Change | Safe order |
|--------|------------|
| Rename column | Add new → copy → switch app → drop old |
| NOT NULL | Add nullable → backfill → set NOT NULL with check |
| Type change | New column + migrate |

## Code Examples

```sql
-- Phase 1: add column
ALTER TABLE users ADD COLUMN display_name text;

-- Phase 2: backfill batch
UPDATE users SET display_name = name WHERE id BETWEEN $1 AND $2;

-- Phase 3: enforce (after full backfill)
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
```

## Anti-Patterns

| Bad | Risk |
|-----|------|
| Blocking `ALTER` on huge table | Long locks |
| Deploy + schema incompatible | Downtime / errors |

## Deep Dive Sources

- [PostgreSQL — ALTER TABLE notes](https://www.postgresql.org/docs/current/sql-altertable.html)
- [Braintree — Safe Production SQL](https://www.braintreepayments.com/blog/safe-sql/)
- [Strong Migrations (thoughtbot)](https://github.com/ankane/strong_migrations) — Rails but principles universal
