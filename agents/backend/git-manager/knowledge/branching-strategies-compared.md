---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Branching Strategies Compared

## Quick Reference

| Strategy | Branch usage |
|----------|----------------|
| **GitHub Flow** | `main` + short-lived `feature/*` |
| **Git Flow** | `develop`, `release/*`, `hotfix/*` |
| **Trunk-based** | Small commits to `main`, feature flags |

**2025–2026:** Trunk-based + feature flags common at scale; long-lived `develop` less favored.

## Patterns & Decision Matrix

| Team | Suggest |
|------|---------|
| Continuous deploy | GitHub Flow / trunk |
| Scheduled releases | Release branches optional |

## Code Examples

```bash
git checkout -b feature/TICKET-short-name
git push -u origin feature/TICKET-short-name
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Long-lived feature branches | Merge pain |

## Deep Dive Sources

- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Trunk Based Development](https://trunkbaseddevelopment.com/)
