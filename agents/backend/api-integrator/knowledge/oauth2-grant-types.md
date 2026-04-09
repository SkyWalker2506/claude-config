---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# OAuth 2.0 Grant Types

## Quick Reference

| Grant | Use case | Tokens |
|-------|----------|--------|
| **Authorization Code + PKCE** | SPAs, mobile, server apps (public clients) | Access + refresh |
| **Authorization Code (confidential)** | Server-side web with client secret | Access + refresh |
| **Client Credentials** | M2M, no user | Access only |
| **Device Code** | Input-constrained devices | Access + refresh |
| **Refresh Token** | Rotate access | New access |

**Deprecated/avoid:** Implicit grant for new apps (use PKCE code flow). Resource Owner Password — legacy only.

**2025–2026:** OAuth 2.1 draft consolidates best practices (PKCE required for public clients). Always check IdP docs (Auth0, Okta, Keycloak, Cognito).

## Patterns & Decision Matrix

| Client type | Flow |
|-------------|------|
| Browser SPA | Auth code + PKCE, no secret in bundle |
| First-party mobile | Auth code + PKCE, universal links redirect |
| Cron / worker | Client credentials |
| Long offline access | Refresh with rotation if IdP supports |

## Code Examples

**PKCE (conceptual):**

```text
code_verifier = random 43-128 chars
code_challenge = BASE64URL(SHA256(code_verifier))
→ authorize?response_type=code&code_challenge=...&code_challenge_method=S256
→ token with code_verifier
```

**Client credentials (HTTP):**

```http
POST /oauth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=...&client_secret=...
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Secret in mobile/SPA | Extractable from binary |
| Long-lived access token only | No revocation path |
| Ignoring state/nonce | CSRF / mix-up attacks |

## Deep Dive Sources

- [OAuth 2.0 Security BCP — RFC 8252, 6819 updates](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [OAuth.net — Authorization Code with PKCE](https://oauth.net/2/pkce/)
- [Auth0 — Which OAuth flow](https://auth0.com/docs/get-started/authentication-and-authorization-flow)
- [Keycloak — Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)
