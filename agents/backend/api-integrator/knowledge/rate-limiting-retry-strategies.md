---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Rate Limiting and Retry Strategies

## Quick Reference

| Retry policy | Formula | Use |
|--------------|---------|-----|
| **Exponential backoff** | `base * 2^n` + jitter | 429, 503, network blips |
| **Full jitter** | `random(0, cap)` | Thundering herd reduction |
| **Max attempts** | e.g. 5 | Avoid infinite loops |

**Respect:** `Retry-After` header (seconds or HTTP-date). **Idempotency-Key** on mutating retries.

**Client limits:** Track provider quota (headers like `X-RateLimit-Remaining` when present).

**2025–2026:** gRPC retry policies; AWS SDK built-in retries; Polly (.NET), resilience4j (Java).

## Patterns & Decision Matrix

| Response | Action |
|----------|--------|
| 429 | Backoff + respect Retry-After |
| 401 | Refresh token once; do not blind retry |
| 400 | No retry — fix request |
| 5xx | Retry with cap |

## Code Examples

**Exponential backoff with jitter (TypeScript sketch):**

```typescript
async function withRetry<T>(fn: () => Promise<T>, max = 5): Promise<T> {
  for (let n = 0; ; n++) {
    try { return await fn(); } catch (e) {
      if (n >= max || !isRetryable(e)) throw e;
      const ms = Math.min(1000 * 2 ** n + Math.random() * 250, 30_000);
      await sleep(ms);
    }
  }
}
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| Retry POST without idempotency | Idempotency-Key or dedupe |
| Same delay every time | Jitter |
| Ignoring 429 body | Parse Retry-After |

## Deep Dive Sources

- [AWS — Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Google Cloud — Retry strategy](https://cloud.google.com/storage/docs/retry-strategy)
- [RFC 6585 — 429 Too Many Requests](https://www.rfc-editor.org/rfc/rfc6585.html)
