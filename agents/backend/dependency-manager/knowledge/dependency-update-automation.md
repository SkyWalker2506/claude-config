---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Dependency Update Automation

## Quick Reference

| Tool | Behavior |
|------|----------|
| **Dependabot** | PRs per ecosystem, schedule |
| **Renovate** | Rich rules, grouping |
| **Changesets** | Version bump + changelog for monorepos |

**Batching:** Group patch updates; major separate PR with migration notes.

**2025–2026:** Auto-merge for dev-deps only with required CI green.

## Patterns & Decision Matrix

| Update | Process |
|--------|---------|
| Security patch | Fast-track PR |
| Major framework | Dedicated branch + QA |

## Anti-Patterns

| Bad | Why |
|-----|-----|
| 50 major bumps one PR | Unreviewable |

## Code Examples

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule: { interval: weekly }
```

## Deep Dive Sources

- [Renovate — Docs](https://docs.renovatebot.com/)
- [GitHub — Dependabot options](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
