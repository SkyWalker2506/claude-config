---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Schema Versioning Patterns

## Quick Reference

| Tool stack | Typical approach |
|------------|------------------|
| **Flyway** | Versioned SQL `V1__x.sql`, immutable after apply |
| **Liquibase** | XML/YAML/SQL changesets with checksum |
| **Prisma** | `schema.prisma` + migrations folder |
| **Rails ActiveRecord** | Timestamped migrations |
| **Django** | `migrations/` per app |

**Rules:** Migrations **forward** in CI; rollback strategy explicit (often new migration, not down in prod).

**2025–2026:** Separate **migration** job from app deploy or run as init container with locks.

## Patterns & Decision Matrix

| Team size | Practice |
|-----------|----------|
| Small | Linear versioned SQL |
| Large | Code review on migration + load test on copy of prod |

## Code Examples

**Flyway naming:**

```text
V202604091200__add_orders_status_index.sql
```

**Prisma workflow:**

```bash
npx prisma migrate dev --name add_orders_status
npx prisma migrate deploy   # prod
```

## Anti-Patterns

| Mistake | Risk |
|---------|------|
| Editing applied migration file | Checksum drift, env inconsistency |
| Data migration without batch | Lock contention |

## Deep Dive Sources

- [Flyway — Documentation](https://documentation.red-gate.com/flyway)
- [Prisma — Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [PostgreSQL — Versioning migrations](https://www.postgresql.org/docs/current/ddl.html) — DDL reference
