---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Next.js App Router Patterns

## Quick Reference

| Piece | Role |
|-------|------|
| `app/` | Routes as folders |
| `layout.tsx` | Shared shell |
| `page.tsx` | Route UI |
| **Server Components** | Default — no `use client` unless needed |
| **fetch cache** | `cache`, `revalidate`, `no-store` |

**2025–2026:** Next 15+; `middleware.ts` for edge auth; partial prerendering where enabled.

## Patterns & Decision Matrix

| Data | Pattern |
|------|---------|
| Static | RSC + generateStaticParams |
| User-specific | `no-store` or short revalidate |

## Code Examples

```tsx
// app/items/page.tsx
export default async function Page() {
  const res = await fetch('https://api/items', { next: { revalidate: 60 } });
  const items = await res.json();
  return <ul>{items.map((i) => <li key={i.id}>{i.name}</li>)}</ul>;
}
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Her şeyi client component | Bundle şişer |
| `fetch` önbelleği varsayılanına körü güven | Stale veri |

## Deep Dive Sources

- [Next.js — App Router](https://nextjs.org/docs/app)
- [Next.js — Data fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
