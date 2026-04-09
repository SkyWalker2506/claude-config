---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Three.js Scene Management

## Quick Reference

| Object | Role |
|--------|------|
| **Scene** | Graph root |
| **Camera** | Perspective vs Orthographic |
| **WebGLRenderer** | `setPixelRatio`, `setSize` |
| **Dispose** | `geometry.dispose()`, `material.dispose()` |

**2025–2026:** r170+ module imports; `three/addons/` for controls/loaders.

## Patterns & Decision Matrix

| Issue | Fix |
|-------|-----|
| Memory leak | Dispose unused assets on scene exit |

## Code Examples

```typescript
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(75, w / h, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
```

## Deep Dive Sources

- [Three.js — Manual](https://threejs.org/manual/)
- [three.js docs](https://threejs.org/docs/)
