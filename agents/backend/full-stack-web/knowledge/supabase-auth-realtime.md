---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Supabase Auth and Realtime

## Quick Reference

| Feature | API |
|---------|-----|
| **Auth** | `@supabase/supabase-js` — session in browser; PKCE for SPA |
| **RLS** | Postgres policies — primary security layer |
| **Realtime** | Channel subscribe to table changes |

**2025–2026:** Never trust client alone — RLS for every table exposed to anon key.

## Patterns & Decision Matrix

| Exposure | Rule |
|----------|------|
| Public read | `select` policy scoped |

## Code Examples

```typescript
const { data } = await supabase.from('posts').select('*').eq('published', true);
```

## Deep Dive Sources

- [Supabase — Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase — Realtime](https://supabase.com/docs/guides/realtime)
