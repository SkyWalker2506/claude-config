---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Request Validation Schemas

## Quick Reference

| Stack | Tool |
|-------|------|
| **OpenAPI** | JSON Schema for body/query |
| **Kong** | request-validator plugin |
| **Envoy** | ext_authz + external service |

**2025–2026:** Validate at edge for fast 400; duplicate in service for defense in depth optional.

## Code Examples

```yaml
paths:
  /orders:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CreateOrder' }
```

## Deep Dive Sources

- [OpenAPI — Parameter validation](https://swagger.io/docs/specification/data-models/)
