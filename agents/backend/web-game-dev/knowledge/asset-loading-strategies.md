---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Asset Loading Strategies

## Quick Reference

| Strategy | Use |
|----------|-----|
| **Preload scene** | Critical path |
| **Lazy load** | Large optional packs |
| **Progress events** | UX bar |
| **Compression** | BasisU textures, Ogg/Opus audio |

**2025–2026:** HTTP/2 multiplexing; service worker cache for PWA games.

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Block main thread decode | Use workers where possible |

## Code Examples

```typescript
this.load.atlas('sprites', 'assets/atlases/sprites.png', 'assets/atlases/sprites.json');
```

## Deep Dive Sources

- [Phaser — Loader](https://docs.phaser.io/api-documentation/class/loader-loaderplugin)
