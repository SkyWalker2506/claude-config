---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Tailwind Design System

## Quick Reference

| Concept | Detail |
|---------|--------|
| **Design tokens** | `tailwind.config` theme extend |
| **Components** | `@apply` sparingly; prefer React components |
| **v4** | CSS-first config optional |

**2025–2026:** `clsx` + `tailwind-merge` for conditional classes.

## Patterns & Decision Matrix

| İhtiyaç | Yaklaşım |
|---------|----------|
| Tema | CSS variables + `tailwind.config` extend |
| Bileşen kütüphanesi | Headless + token sınıfları |

## Code Examples

```tsx
<button className={clsx('rounded px-3', isPrimary && 'bg-brand text-white')}>Save</button>
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Copy-paste arbitrary values | Use theme scale |

## Deep Dive Sources

- [Tailwind CSS — Documentation](https://tailwindcss.com/docs)
