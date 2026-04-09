---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# npm Publish Guide

## Quick Reference

| Adım | Komut / dosya |
|------|----------------|
| Scope | `@org/pkg` |
| `files` | dist only |
| `prepublishOnly` | test + build |

## Patterns & Decision Matrix

| Görünürlük | `access` |
|------------|----------|
| Public | `public` |
| Özel | npm paid org |

## Code Examples

```bash
npm publish --access public
```

## Anti-Patterns

- `node_modules` veya `.env` paketlemek.

## Deep Dive Sources

- [npm docs publishing](https://docs.npmjs.com/cli/v10/commands/npm-publish)
