---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# SDK Wrapper Design

## Quick Reference

| Layer | Responsibility |
|-------|----------------|
| **Thin client** | HTTP/gRPC calls, auth header injection |
| **Wrapper** | Domain-friendly methods, error mapping, retries |
| **Facade** | Combine multiple calls for one use case |

**Naming:** `PaymentsClient.createIntent()` not `POST /v1/intents`.

**2025–2026:** OpenAPI generator for TS/Java/Kotlin; hand-wrap for ergonomics and retries.

## Patterns & Decision Matrix

| Need | Design |
|------|--------|
| Testability | Interface + fake implementation |
| Multi-region | Base URL from config |
| Observability | Wrap fetch with tracing span per call |

## Code Examples

```typescript
export class StripePayments {
  constructor(private http: HttpClient, private cfg: { apiKey: string }) {}

  async createCharge(params: CreateChargeParams): Promise<Charge> {
    const res = await this.http.post('/v1/charges', params, {
      headers: { Authorization: `Bearer ${this.cfg.apiKey}` },
    });
    if (!res.ok) throw mapStripeError(res);
    return res.json();
  }
}
```

## Anti-Patterns

| Smell | Fix |
|-------|-----|
| Leaking vendor JSON types everywhere | Map to internal DTO |
| One mega class 100 methods | Split by subdomain |
| No timeout | Default timeout per call |

## Deep Dive Sources

- [OpenAPI Generator](https://openapi-generator.tech/)
- [Stripe API — Idempotent requests](https://stripe.com/docs/api/idempotent_requests)
- [Microsoft — REST client guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md)
