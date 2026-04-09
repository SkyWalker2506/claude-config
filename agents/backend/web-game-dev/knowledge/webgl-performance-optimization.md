---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# WebGL Performance Optimization

## Quick Reference

| Technique | Benefit |
|-----------|---------|
| **Instancing** | Many same mesh |
| **Texture atlases** | Fewer binds |
| **Frustum culling** | Skip off-screen |
| **LOD** | Cheaper distant meshes |

**Draw calls:** Minimize state changes; batch geometry.

## Anti-Patterns

| Bad | Why |
|-----|-----|
| New texture every frame | GPU stall |

## Code Examples

```typescript
const mesh = new THREE.InstancedMesh(geometry, material, count);
```

## Deep Dive Sources

- [WebGPU — MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) — next-gen (when available)
