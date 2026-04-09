---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Frontend Performance Metrics

## Quick Reference

| Metric | Meaning |
|--------|---------|
| **LCP** | Largest Contentful Paint — loading |
| **INP** | Interaction to Next Paint — responsiveness |
| **CLS** | Cumulative Layout Shift — stability |

**Core Web Vitals** — Google ranking and UX signal.

**2025–2026:** INP replaced FID as responsiveness metric.

## Patterns & Decision Matrix

| Bad LCP | Check |
|---------|-------|
| Large image | Responsive images, priority hints |
| Slow API | Backend latency (B2/B12) |

## Code Examples

```javascript
new PerformanceObserver((list) => {
  for (const e of list.getEntries()) console.log(e.name, e.value);
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

## Deep Dive Sources

- [web.dev — Core Web Vitals](https://web.dev/vitals/)
- [Chrome UX Report](https://developer.chrome.com/docs/crux)
