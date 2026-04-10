---
last_updated: 2026-04-10
refined_by: coverage-bootstrap
confidence: high
sources: 3
---

# GitHub API & gh CLI patterns

## Quick Reference

| Araç | Kullanım |
|------|----------|
| `gh repo view` | Metadata okuma |
| `gh api` | REST/GraphQL düşük seviye |
| GitHub MCP | Claude oturumunda entegre |

## Patterns & Decision Matrix

| İşlem | Tercih |
|-------|--------|
| Tek seferlik | `gh` |
| Otomasyon | API + token scope minimal |

## Code Examples

```bash
gh repo edit SkyWalker2506/claude-config --add-topic claude-code
gh api repos/SkyWalker2506/claude-config --jq .description
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| PAT log’a düşmek | Güvenlik ihlali |

## Deep Dive Sources

- [GitHub CLI manual](https://cli.github.com/manual/)
- [GitHub REST API](https://docs.github.com/en/rest)
