---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# REST API Conventions

## Quick Reference

| HTTP | Safe | Idempotent | Typical use |
|------|------|------------|-------------|
| GET | Yes | Yes | Read resource/collection |
| PUT | No | Yes | Replace resource |
| PATCH | No | No* | Partial update (*if implemented carefully) |
| POST | No | No | Create, actions |
| DELETE | No | Yes | Delete |

**Resources:** Plural nouns `/users`, `/users/{id}/orders`. **Status:** 2xx success, 4xx client, 5xx server. **Errors:** RFC 9457 `application/problem+json`.

**2025–2026:** JSON remains default; `Prefer: return=minimal` patterns in some APIs; OpenAPI 3.1 for codegen.

## Patterns & Decision Matrix

| Choice | Prefer | Avoid |
|--------|--------|-------|
| Pagination | Cursor (stable with writes) or keyset | Offset on huge tables |
| Filtering | Query params `?status=open` | Ad-hoc POST for reads |
| Versioning | `/v1` in path or header | Silent breaking changes |
| Create location | `201` + `Location` header | 200 without URI |

## Code Examples

```http
POST /v1/orders HTTP/1.1
Content-Type: application/json

{"customerId":"cust_123","lines":[{"sku":"X","qty":2}]}
```

```http
HTTP/1.1 201 Created
Location: /v1/orders/ord_789
Content-Type: application/json

{"id":"ord_789","status":"pending"}
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| Verbs in URLs `/createOrder` | Noun + POST |
| 200 with error body | Proper 4xx + problem+json |
| Giant GET with side effects | POST for unsafe ops |

## Deep Dive Sources

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9457 — Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html)
- [OpenAPI Specification 3.1](https://spec.openapis.org/oas/v3.1.0)
- [JSON:API — Recommendations](https://jsonapi.org/recommendations/) — opinionated REST
