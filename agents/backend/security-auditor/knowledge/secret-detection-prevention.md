---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Secret Detection and Prevention

## Quick Reference

| Tool class | Examples |
|------------|----------|
| **Pre-commit** | gitleaks, trufflehog, git-secrets |
| **CI** | Same + GitHub push protection |
| **Runtime** | Vault, cloud secret manager |

**Response:** Rotate key if leaked; history purge does not remove GitHub forks cache — **rotate always**.

**2025–2026:** GitHub secret scanning + push protection for orgs.

## Patterns & Decision Matrix

| Secret | Storage |
|--------|---------|
| API key | Secret manager, injected env |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| `.env` committed | Forever in git history risk |

## Code Examples

```bash
gitleaks detect --source . --verbose
```

## Deep Dive Sources

- [GitHub — Secret scanning](https://docs.github.com/en/code-security/secret-scanning)
- [gitleaks](https://github.com/gitleaks/gitleaks)
