---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Environment and Secrets Management

## Quick Reference

| Layer | Mechanism |
|-------|-----------|
| **CI secrets** | GitHub Encrypted secrets, OIDC to cloud |
| **Runtime** | Vault, AWS Secrets Manager, GCP Secret Manager |
| **Config** | Non-secret in env or config service |
| **Rotation** | Short TTL, automated rotation APIs |

**Never:** Commit `.env` with secrets; use `.env.example` without values.

**2025–2026:** OIDC `aud` + `sub` binding for GitHub→cloud role assumption.

## Patterns & Decision Matrix

| Secret | Storage |
|--------|---------|
| DB password | Managed secret + inject at deploy |
| API key (third party) | Same; rotate on people change |

## Code Examples

```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Anti-Patterns

| Bad | Risk |
|-----|------|
| Secret in workflow echo | Log leak |
| Shared prod key in dev | Blast radius |

## Deep Dive Sources

- [GitHub — Encrypted secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [OWASP — Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
