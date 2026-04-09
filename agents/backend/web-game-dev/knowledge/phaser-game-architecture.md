---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Phaser Game Architecture

## Quick Reference

| Concept | Phaser 3 |
|---------|----------|
| **Scene** | Screens/states — `preload`, `create`, `update` |
| **Game loop** | `update(time, delta)` |
| **Assets** | Texture atlas, audio sprites |

**2025–2026:** Phaser 3.90+ ecosystem; TypeScript templates common.

## Patterns & Decision Matrix

| Need | Pattern |
|------|---------|
| UI overlay | Separate Scene with higher depth |
| Data-driven levels | JSON + factory |

## Code Examples

```typescript
class PlayScene extends Phaser.Scene {
  constructor() { super({ key: 'Play' }); }
  create() { this.add.sprite(400, 300, 'player'); }
  update(_t: number, dt: number) { /* move */ }
}
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| God scene | Hard to test |

## Deep Dive Sources

- [Phaser 3 — Documentation](https://docs.phaser.io/)
- [Phaser Examples](https://labs.phaser.io/)
