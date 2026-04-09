---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# 3D Asset Sources

## Quick Reference

| Tür | Örnek kaynak türleri |
|-----|----------------------|
| PBR | Texture + mesh paketleri |
| Rigged | Mixamo benzeri animasyon hazır |
| Kitbash | Modular parça |

## Patterns & Decision Matrix

| Motor | Format |
|-------|--------|
| Unity | FBX, glTF |
| Blender | .blend + export pipeline |

## Code Examples

```text
[SOURCE] url=… | license=CC-BY | format=glb | poly_budget=50k
```

## Anti-Patterns

- Ticari projede “editorial only” asset kullanımı.

## Deep Dive Sources

- [Khronos glTF](https://www.khronos.org/gltf/)
- [Unity asset pipeline](https://docs.unity3d.com/Manual/ImportingAssets.html)
