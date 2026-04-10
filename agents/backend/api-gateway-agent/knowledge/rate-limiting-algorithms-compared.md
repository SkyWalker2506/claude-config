---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Rate Limiting Algorithms Compared

## Quick Reference

| Algorithm | Behavior |
|-----------|------------|
| **Token bucket** | Burst + steady rate |
| **Leaky bucket** | Smooth output |
| **Fixed window** | Simple; boundary burst |
| **Sliding window** | Smoother |

**Storage:** Redis with atomic INCR + TTL.

## Patterns & Decision Matrix

| Algoritma | Ne zaman |
|-----------|----------|
| Token bucket | Burst toleransı gerekirse |
| Sliding window | Adil dakika başına limit |
| Fixed window | Basit sayaç; köşe spike riski |

## Code Examples

```lua
-- Pseudocode: token bucket
if tokens >= 1 then tokens -= 1; allow else deny
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| IP-only limit (CGNAT) | Yanlış kısıtlama |
| Limit yanıtında veri sızıntısı | Enumeration |

## Deep Dive Sources

- [Cloudflare — Rate limiting](https://developers.cloudflare.com/waf/rate-limiting-rules/)
