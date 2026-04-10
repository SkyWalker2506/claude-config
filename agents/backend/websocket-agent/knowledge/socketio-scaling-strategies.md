---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Socket.IO Scaling Strategies

## Quick Reference

| Need | Mechanism |
|------|-----------|
| Multi-node | **Redis adapter** for pub/sub rooms |
| Sticky | Required for fallback long-polling upgrade path |

**2025–2026:** `socket.io` v4+; match client/server major versions.

## Patterns & Decision Matrix

| Ölçek | Mekanizma |
|-------|-----------|
| Tek node | Memory adapter |
| Çok node | Redis adapter + sticky veya mesaj odası |

## Code Examples

```javascript
const io = require('socket.io')(server);
const { createAdapter } = require('@socket.io/redis-adapter');
io.adapter(createAdapter(pubClient, subClient));
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Redis yokken çok node | Oda tutarsızlığı |
| Sticky olmadan yanlış yönlendirme | Bağlantı kopması |

## Deep Dive Sources

- [Socket.IO — Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/)
