---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# CORS, CSP, and Security Headers

## Quick Reference

| Header | Role |
|--------|------|
| **CORS** | Browser cross-origin **read** of response — not auth replacement |
| **CSP** | Mitigate XSS — script-src, default-src |
| **HSTS** | Force HTTPS |
| **X-Content-Type-Options** | nosniff |

**CORS:** `Access-Control-Allow-Origin` specific origin, not `*` with credentials.

**2025–2026:** `Content-Security-Policy-Report-Only` first; nonce/hash for scripts.

## Patterns & Decision Matrix

| API | CORS |
|-----|------|
| Public read | Specific origins or controlled `*` without cookies |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| CORS * + `Access-Control-Allow-Credentials: true` | Invalid / dangerous |

## Code Examples

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
```

## Deep Dive Sources

- [MDN — CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP — CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
