---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# GitHub Actions Best Practices

## Quick Reference

| Practice | Why |
|----------|-----|
| **Pin actions** | `@v4` → full SHA for supply chain |
| **Least privilege** | `permissions:` minimal |
| **Reusable workflows** | DRY across repos |
| **Concurrency** | `cancel-in-progress` for same branch |
| **Matrix** | Cross-version testing |

**Secrets:** `GITHUB_TOKEN` scoped; org secrets for cross-repo.

**2025–2026:** OIDC to cloud (AWS, GCP) instead of long-lived keys.

## Patterns & Decision Matrix

| Need | Pattern |
|------|---------|
| Monorepo filters | `paths:` filter on workflow |
| Long jobs | Split; cache dependencies |

## Code Examples

```yaml
permissions:
  contents: read
  pull-requests: write
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| Secrets in logs | Mask; use env |
| `pull_request_target` unsafe patterns | Review GitHub security advisories |

## Deep Dive Sources

- [GitHub — Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub — Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
