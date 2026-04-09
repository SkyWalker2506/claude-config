---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Prisma Schema Patterns

## Quick Reference

| Directive | Use |
|-----------|-----|
| `@id`, `@default(uuid())` | Keys |
| `@relation` | FK + referential actions |
| `@@index` | Query paths |

**Migrations:** `prisma migrate dev` — never edit applied SQL by hand in team settings.

## Code Examples

```prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  posts Post[]
}
```

## Deep Dive Sources

- [Prisma — Schema reference](https://www.prisma.io/docs/orm/reference/prisma-schema-reference)
