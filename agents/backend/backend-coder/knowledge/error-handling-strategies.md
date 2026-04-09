---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Error Handling Strategies

## Quick Reference

| Category | HTTP | problem+json `type` URI |
|----------|------|-------------------------|
| Validation | 400 | `/errors/validation` (stable per API) |
| Auth | 401 | — |
| Forbidden | 403 | — |
| Not found | 404 | — |
| Conflict | 409 | duplicate, state conflict |
| Rate limit | 429 | + `Retry-After` |

**Body (RFC 9457):**

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation failed",
  "status": 400,
  "detail": "email is invalid",
  "instance": "/requests/req_abc"
}
```

**2025–2026:** RFC 9457 obsoletes RFC 7807; same JSON model.

## Patterns & Decision Matrix

| Concern | Pattern |
|---------|---------|
| Stable client handling | Machine-readable `type` URI per error code |
| i18n | `title` generic; `detail` or extension `locale` |
| Internal vs public | Strip stack traces in prod; log server-side with correlation id |
| Retries | Idempotent ops + 429/503 with backoff |

## Code Examples

**Exception → HTTP mapping (concept):**

```typescript
if (e instanceof ValidationError) return problem(400, 'validation-error', e.message);
if (e instanceof NotFoundError) return problem(404, 'not-found', 'Resource not found');
```

**Correlation:**

```http
X-Request-Id: 550e8400-e29b-41d4-a716-446655440000
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| 500 for “not found” | 404 |
| Different JSON shape per endpoint | Single problem format |
| Leaking SQL in `detail` | Generic message + internal log |

## Deep Dive Sources

- [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)
- [Problem Details — IANA](https://www.iana.org/assignments/http-problem-types/http-problem-types.xhtml)
- [Stripe API errors](https://stripe.com/docs/api/errors) — real-world error model reference
