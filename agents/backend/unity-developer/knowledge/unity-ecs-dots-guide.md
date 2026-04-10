---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Unity ECS and DOTS Guide

## Quick Reference

| Piece | Role |
|-------|------|
| **Entities** | Lightweight IDs |
| **Components** | Data-only `IComponentData` |
| **Systems** | `ISystem`, `SystemAPI.Query` |

**2025–2026:** DOTS packages evolve — check Unity manual version for your editor.

## Patterns & Decision Matrix

| Use ECS | Stay GameObject |
|---------|-----------------|
| Many similar units | Few unique behaviours |

## Code Examples

```csharp
[BurstCompile]
partial struct MovementSystem : ISystem
{
  public void OnUpdate(ref SystemState state) { /* query + Job */ }
}
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| ECS’de GameObject karışımı | Burst/job engeli |
| Tek dev struct | Cache miss |

## Deep Dive Sources

- [Unity — ECS Documentation](https://docs.unity3d.com/Packages/com.unity.entities@latest)
