---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# WebSocket Architecture Patterns

## Quick Reference

| Concern | Pattern |
|---------|---------|
| **Sticky sessions** | Same instance for socket (LB IP hash) |
| **Heartbeat** | Ping/pong to detect dead peers |
| **Backpressure** | Slow consumer handling |

**2025–2026:** Prefer managed gateways (API GW WebSocket) or dedicated WS service behind LB.

## Patterns & Decision Matrix

| Mimari | Seçim |
|--------|--------|
| İnce gateway | Sadece WS terminate |
| BFF | Auth + rate limit edge |

## Code Examples

```javascript
const ws = new WebSocket('wss://api.example.com/stream');
ws.onmessage = (ev) => handle(JSON.parse(ev.data));
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| WSS’siz prod | MITM |
| Heartbeat yok | Ölü bağlantı birikimi |

## Deep Dive Sources

- [RFC 6455 — WebSocket](https://www.rfc-editor.org/rfc/rfc6455.html)
