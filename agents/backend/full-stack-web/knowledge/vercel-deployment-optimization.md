---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Vercel Deployment Optimization

## Quick Reference

| Topic | Tip |
|-------|-----|
| **Regions** | Run functions near DB |
| **Edge** | Middleware/edge config for auth redirect |
| **ISR** | `revalidate` in fetch/route segment |
| **Env** | Project settings — no secrets in repo |

**2025–2026:** Fluid compute / concurrency settings per plan — check dashboard.

## Code Examples

```tsx
export const revalidate = 3600; // ISR seconds — segment config
```

## Deep Dive Sources

- [Vercel — Docs](https://vercel.com/docs)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
