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

## Patterns & Decision Matrix

| Durum | Şema kararı |
|-------|-------------|
| Çok-tenant | `tenantId` + composite unique |
| Soft delete | `deletedAt` + filtreli unique index |
| Büyük metin | Ayrı tablo veya depolama pointer |

## Code Examples

```prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  posts Post[]
}
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| İlişkisiz cascade | Veri kaybı |
| Index’siz sık filtre | Full scan |

## Deep Dive Sources

- [Prisma — Schema reference](https://www.prisma.io/docs/orm/reference/prisma-schema-reference)
