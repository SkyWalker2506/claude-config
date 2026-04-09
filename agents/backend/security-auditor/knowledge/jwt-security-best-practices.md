---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# JWT Security Best Practices

## Quick Reference

| Topic | Practice |
|-------|----------|
| **Algorithm** | Use strong alg (RS256/ES256); reject `none` |
| **Validation** | `iss`, `aud`, `exp`, `nbf`; clock skew |
| **Storage (browser)** | Not localStorage for XSS-sensitive — prefer HttpOnly cookie + CSRF strategy |
| **Rotation** | Short-lived access + refresh with rotation/revocation |

**2025–2026:** Prefer **opaque tokens + introspection** for high-security; JWT where federation needs claims.

## Patterns & Decision Matrix

| Client | Pattern |
|--------|---------|
| SPA | BFF + HttpOnly cookie or PKCE + short JWT |
| Mobile | Keychain storage; attestation optional |

## Code Examples

```typescript
const payload = await jwtVerify(token, JWKS, { issuer, audience });
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Long-lived JWT without revoke list | Stolen token window |

## Deep Dive Sources

- [RFC 8725 — JWT BCP](https://www.rfc-editor.org/rfc/rfc8725.html)
- [OWASP — JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
