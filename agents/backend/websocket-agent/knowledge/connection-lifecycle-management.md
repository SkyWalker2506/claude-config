---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Connection Lifecycle Management

## Quick Reference

| Phase | Action |
|-------|--------|
| **Connect** | Auth handshake (token in first message or subprotocol) |
| **Idle** | Timeout disconnect |
| **Disconnect** | Cleanup subscriptions, presence |

**2025–2026:** Rate limit connection attempts at edge (anti-DoS).

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Unbounded memory per socket | Per-connection cap |

## Code Examples

```javascript
ws.isAlive = true;
ws.on('pong', () => { ws.isAlive = true; });
setInterval(() => { ... ping if !isAlive → terminate }, 30000);
```

## Deep Dive Sources

- [MDN — WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
