# API Documentation Standards (OpenAPI)

## OpenAPI Schema Conversion Workflow

When converting an API (from CURL or description) to OpenAPI format:

1. **Analyze the API details**:
   - Endpoint path and method (GET, POST, PUT, DELETE, PATCH)
   - Request body structure and field types
   - Query parameters and path parameters
   - Response structure and status codes
   - Authentication method

2. **Map to OpenAPI structure**:
   - `paths` → endpoint definitions
   - `components/schemas` → reusable data models
   - `components/securitySchemes` → auth definitions
   - `servers` → always include base URL

3. **Always include server block**:
```yaml
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
```

## OpenAPI Best Practices

### Schema Design
- Use `$ref` to reference reusable components — never repeat schemas inline
- Define all response schemas explicitly (200, 400, 401, 404, 500)
- Use `required` arrays to indicate mandatory fields
- Always specify `type` for all properties

### Naming Conventions
- Paths: lowercase, hyphenated (`/user-profiles`, not `/userProfiles`)
- Operation IDs: camelCase, descriptive (`getUserProfile`, not `get`)
- Schema names: PascalCase (`UserProfile`, `ErrorResponse`)

### Common Error Response Schema
```yaml
ErrorResponse:
  type: object
  required: [code, message]
  properties:
    code:
      type: string
    message:
      type: string
    details:
      type: array
      items:
        type: string
```

### Security Schemes
```yaml
securitySchemes:
  BearerAuth:
    type: http
    scheme: bearer
    bearerFormat: JWT
  ApiKeyAuth:
    type: apiKey
    in: header
    name: X-API-Key
```

## API Design Pitfalls to Avoid

| Anti-pattern | Better Approach |
|-------------|----------------|
| `/getUsers` | `GET /users` |
| Returning 200 for errors | Correct HTTP status codes |
| No pagination | Add `limit`/`offset` or cursor params |
| Inconsistent date formats | Always ISO 8601: `2024-01-15T10:30:00Z` |
| Exposing internal IDs | Use UUIDs or slugs |
| No versioning | `/v1/`, `/v2/` prefix or header-based |

## Validation Checklist

Before finalizing an API schema:
- [ ] All endpoints have operationId
- [ ] All response codes documented (at minimum 200, 400, 401, 500)
- [ ] Server block included
- [ ] Authentication scheme defined and applied
- [ ] Reusable components extracted with `$ref`
- [ ] Required fields marked
- [ ] Example values provided for key fields
