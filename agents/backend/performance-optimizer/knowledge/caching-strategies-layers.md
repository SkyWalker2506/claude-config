---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Caching Strategies and Layers

## Quick Reference

| Layer | Examples |
|-------|----------|
| **Browser** | HTTP Cache-Control, ETag |
| **CDN** | CloudFront, Fastly |
| **Application** | Redis, in-memory |
| **Database** | Query cache (limited), materialized views |

**Invalidation:** TTL, event-driven purge, versioned keys.

**2025–2026:** Stale-while-revalidate for HTTP; Redis cluster for session/cache.

## Patterns & Decision Matrix

| Data | Cache? |
|------|--------|
| Read-heavy immutable | Strong candidate |
| Per-user sensitive | Short TTL + key scoping |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Cache without eviction policy | Memory leak |

## Code Examples

```http
Cache-Control: public, max-age=60, stale-while-revalidate=300
```

## Deep Dive Sources

- [HTTP Caching — MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Redis — Caching patterns](https://redis.io/docs/manual/patterns/)
