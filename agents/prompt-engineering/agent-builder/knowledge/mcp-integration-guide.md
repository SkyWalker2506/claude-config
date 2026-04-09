---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# MCP Integration Guide

## Quick Reference

- **MCP** = open protocol (JSON-RPC) for tools, resources, prompts between host and server.
- **Primitives:** Tools (model-invoked), Resources (context), Prompts (templates) — see spec for capability negotiation.
- **Transports:** stdio (local dev), HTTP/SSE (remote) — pick per deployment; stdio for CLI agents, HTTP for shared services.
- **Config surface:** Cursor/Claude Desktop MCP config lists `command` + `args` + `env` OR `url` for remote; never commit secrets — use env vars.
- **Agent mapping:** One MCP server often maps to one capability cluster; list `mcps` in frontmatter and name tools in Process/Verification.
- **Health:** G3 (MCP Health Agent) owns runtime probes; N2 owns *design-time* wiring and documentation in agent knowledge.

**Version note:** Spec uses dated versions (e.g. `2025-11-25`); pin client/server to compatible versions in docs you ship.

## Patterns & Decision Matrix

| Scenario | Pattern | Notes |
|----------|---------|-------|
| Local CLI tool wrapping | stdio server, one repo per server | Fast iteration; bind to workspace root |
| Shared org service | HTTP MCP + auth layer | Needs rate limits, audit logs |
| Read-only context | Prefer **Resources** | Safer than arbitrary tools |
| High-risk side effects | Tool with explicit confirmation step | Document in agent Boundaries |
| Many small calls | Batch in tool implementation | Reduces round-trips and token noise |

**Security baseline**

| Risk | Mitigation |
|------|------------|
| Secret exfiltration | No API keys in MCP JSON; env + secret manager |
| Path traversal | Validate paths against allowed roots |
| SSRF (HTTP MCP) | Allowlist hosts; block internal IPs |

## Code Examples

**Cursor / Claude style MCP snippet (stdio — illustrative):**

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["-y", "@org/mcp-my-tools@1.2.3"],
      "env": {
        "MY_API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

**Tool descriptor discipline (what N2 asks implementers to ship):**

```json
{
  "name": "search_repo",
  "description": "Search code by regex under resolved workspace root. Max 200 matches.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "pattern": { "type": "string" },
      "path": { "type": "string" }
    },
    "required": ["pattern"]
  }
}
```

Document in the agent: *when* to call, *what* to do on empty results, and *escalation* if the tool errors twice.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Mega-tool “do everything” | Model ambiguity, hard to test | Split tools by verb + object |
| Undocumented env vars | Onboarding breaks | Table in knowledge + `.env.example` |
| Silent catch-all errors | Ops blind | Map JSON-RPC errors to user-visible codes |
| MCP listed in agent but unused | Registry lies | Remove or implement |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Model Context Protocol — specification (latest)](https://modelcontextprotocol.io/specification/latest) — transports, lifecycle, primitives
- [MCP — servers concept](https://modelcontextprotocol.io/specification/2025-11-25/server) — tools, resources, prompts
- [Anthropic — Model Context Protocol introduction](https://www.anthropic.com/news/model-context-protocol) — motivation and ecosystem
- [MCP GitHub organization](https://github.com/modelcontextprotocol) — reference servers and SDKs
