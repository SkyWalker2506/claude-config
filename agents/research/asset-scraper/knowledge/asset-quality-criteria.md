---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Asset Quality Criteria

## Quick Reference

| Kontrol | Araç / yöntem |
|---------|---------------|
| Topology | quad/tri oranı, n-gon |
| UV | overlap, texel yoğunluğu |
| Scale | Birim ve root transform |
| Materials | PBR slot eksiksiz mi |

## Patterns & Decision Matrix

| Platform | Ek |
|------------|-----|
| Mobil | Poly + texture boyutu |
| PC | LOD gereksinimi |

## Code Examples

```text
[QA] tris=12000 | materials=1 | textures=2K | issues=[none|UV_seam]
```

## Anti-Patterns

- Z-fighting ve scale 100x hatalı import.

## Deep Dive Sources

- [Unity Mesh import](https://docs.unity3d.com/Manual/class-Mesh.html)
