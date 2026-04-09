---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Webhook Design Patterns

## Quick Reference

| Concern | Pattern |
|---------|---------|
| **Authenticity** | HMAC-SHA256 over raw body + shared secret; or mTLS |
| **Idempotency** | Event id + dedupe store (TTL ≥ replay window) |
| **Ordering** | Sequence numbers if provider offers; else at-least-once + idempotent handler |
| **Retries** | Provider retries with backoff; respond 2xx only after durable enqueue |
| **Verification** | Stripe-style signature header; GitHub `X-Hub-Signature-256` |

**2025–2026:** Prefer **signed payloads**; verify timestamp skew (e.g. ±5 min) against replay.

## Patterns & Decision Matrix

| Volume | Approach |
|--------|----------|
| Low | Sync process in request (fast return if queue available) |
| High | Ack fast → queue (SQS, Kafka) → worker |

## Code Examples

**HMAC verification (pseudo):**

```typescript
const sig = req.headers['x-signature'];
const expected = crypto.createHmac('sha256', secret).update(rawBody).digest('hex');
if (!timingSafeEqual(sig, expected)) return 401;
```

**Handler idempotency:**

```sql
INSERT INTO webhook_events (id, payload_hash, processed_at)
VALUES ($1, $2, now())
ON CONFLICT (id) DO NOTHING;
-- if rowcount 0 → duplicate, return 200
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| JSON parse before verify | Verify on raw bytes |
| 500 on duplicate | 200 after dedupe |
| No dead-letter for poison | DLQ + alert |

## Deep Dive Sources

- [Stripe — Webhooks: best practices](https://stripe.com/docs/webhooks/best-practices)
- [GitHub — Webhooks — Securing](https://docs.github.com/en/webhooks/using-webhooks/validating-delivery-deliveries)
- [OWASP — Webhook security](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html)
