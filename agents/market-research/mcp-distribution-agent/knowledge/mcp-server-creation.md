---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# MCP Server Creation

## Quick Reference

| Bileşen | Zorunlu |
|---------|---------|
| `tools` list | JSON schema |
| Transport | stdio / HTTP |
| Auth | token / env |

## Patterns & Decision Matrix

| Dil | SDK |
|-----|-----|
| TS | `@modelcontextprotocol/sdk` |
| Python | `mcp` paketi |

## Code Examples

```json
{ "name": "search", "description": "…", "inputSchema": { "type": "object", "properties": { "q": { "type": "string" } } } }
```

## Anti-Patterns

- Şema olmadan tool yayınlamak.

## Deep Dive Sources

- [MCP specification](https://modelcontextprotocol.io/)
