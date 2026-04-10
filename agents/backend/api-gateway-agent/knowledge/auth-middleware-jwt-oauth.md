---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Auth Middleware: JWT and OAuth

## Quick Reference

| Layer | Check |
|-------|-------|
| Gateway | Signature, `iss`, `aud`, `exp` |
| Service | Fine-grained authZ |

**Pass claims:** Downstream via headers only if trusted network or re-sign.

## Patterns & Decision Matrix

| Senaryo | Seçim |
|---------|--------|
| Public SPA + API | JWT access short TTL + refresh cookie httpOnly |
| S2S | mTLS veya client credentials + audience claim |
| Mobile | PKCE OAuth; no embedded secrets |

## Code Examples

```nginx
# Kong JWT plugin — claims validated before upstream
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Uzun ömürlü JWT | Çalınırsa geniş pencere |
| Claims’e güvenip authZ atlama | IDOR |

## Deep Dive Sources

- [RFC 8725 — JWT Best Current Practice](https://www.rfc-editor.org/rfc/rfc8725.html)
