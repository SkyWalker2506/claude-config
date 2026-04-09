---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# API Design: REST vs GraphQL

## Quick Reference

| Aspect | REST (HTTP + resources) | GraphQL |
|--------|-------------------------|---------|
| Model | Resources, verbs via HTTP methods | Single endpoint, typed schema, client queries fields |
| Versioning | URL (`/v1`), header, or content negotiation | Schema evolution, `@deprecated`, breaking change policy |
| Caching | HTTP cache, CDN-friendly `GET` | Needs normalized cache (Apollo, persisted queries) |
| N+1 risk | Extra round-trips if chatty | Resolver N+1 — use DataLoader / batch loaders |
| Best for | Public APIs, caching, simple clients | Flexible mobile/web clients, aggregated views |
| Standards | OpenAPI 3.x | GraphQL spec + federation (Apollo, GraphQL Mesh) |

**2025–2026:** OpenAPI 3.1 (JSON Schema alignment) widely adopted; GraphQL Federation common in multi-team graphs.

## Patterns & Decision Matrix

| Scenario | Lean REST | Lean GraphQL |
|----------|-----------|--------------|
| B2B partner integration, CDN edge caching | Yes | Rarely |
| Mobile app needs one screen = many resources | Possible with BFF | Strong fit |
| Third-party developers, long-term stability | REST + OpenAPI first | If graph complexity justified |
| Real-time subscriptions | Webhooks / SSE / separate WS | GraphQL subscriptions (with infra cost) |
| File upload | Multipart, presigned URLs | Often separate REST endpoint + URL in mutation |

**Hybrid:** Many teams expose **REST for public/webhooks** and **GraphQL for internal apps** — document boundary in architecture.

## Code Examples

**REST resource + OpenAPI-friendly shape:**

```http
GET /users/42/orders?status=open&limit=20
200 OK
{ "items": [...], "next_cursor": "eyJ..." }
```

**GraphQL query (client chooses fields):**

```graphql
query OrderScreen($id: ID!) {
  order(id: $id) {
    id
    total
    lines { sku quantity }
    customer { name email }
  }
}
```

## Anti-Patterns

| Mistake | Fix |
|---------|-----|
| GraphQL for every CRUD without resolver discipline | Add batching, complexity limits, query cost analysis |
| REST with 50 nested includes in one JSON | Introduce BFF or GraphQL |
| No error model | REST: problem+json (RFC 9457); GraphQL: `errors[]` + extensions |
| Breaking changes without version policy | Deprecation window + semver for REST; `@deprecated` + codegen for GraphQL |

## Deep Dive Sources

- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html) — standard error bodies
- [OpenAPI Initiative](https://www.openapis.org/) — specification and tooling
- [GraphQL — Learn](https://graphql.org/learn/) — official concepts
- [IETF — API Guidelines (Zalando RESTful)](https://opensource.zalando.com/restful-api-guidelines/) — pragmatic REST rules
