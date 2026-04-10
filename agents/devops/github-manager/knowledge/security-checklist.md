---
last_updated: 2026-04-10
refined_by: coverage-bootstrap
confidence: high
sources: 3
---

# Security checklist (public repos)

## Quick Reference

| Kontrol | Araç |
|---------|------|
| Secret | `git log -p`, GitHub secret scanning |
| .env | `.gitignore`, asla commit |
| Dependency | Dependabot, `npm audit` |

## Patterns & Decision Matrix

| Risk | Aksiyon |
|------|---------|
| Leaked token | Rotate + history purge (destek gerekir) |

## Code Examples

```gitignore
.env
*.pem
secrets/
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Örnek `.env` gerçek değer | Kalıcı sızıntı |

## Deep Dive Sources

- [GitHub — Secret scanning](https://docs.github.com/en/code-security/secret-scanning)
- [OWASP — VCS](https://owasp.org/)
