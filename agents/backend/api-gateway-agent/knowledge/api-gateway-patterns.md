---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# API Gateway Patterns

## Quick Reference

| Function | Gateway |
|----------|---------|
| Routing | Path → service |
| AuthN | JWT validation, API keys |
| Rate limit | Per client |
| TLS termination | Edge |

**Products:** Kong, Envoy, AWS API Gateway, NGINX.

**2025–2026:** mTLS internal; JWT at edge with short TTL.

## Patterns & Decision Matrix

| Need | Feature |
|------|---------|
| GraphQL federation | Apollo Router / Mesh at edge |

## Code Examples

```yaml
routes:
  - name: orders
    paths: [ /v1/orders ]
    service: orders-svc
```

## Deep Dive Sources

- [Microservices.io — API Gateway pattern](https://microservices.io/patterns/apigateway.html)
