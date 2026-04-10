---
last_updated: 2026-04-10
refined_by: coverage-bootstrap
confidence: medium
sources: 3
---

# SRP Batcher ve batching

## Quick Reference

| Konu | Not |
|------|-----|
| Unity sürümü | Proje `ProjectSettings` ile hizala |
| Pipeline | URP / HDRP / Built-in |

## Patterns & Decision Matrix

| Durum | Öneri |
|-------|--------|
| Prototip | Minimum özellik, ölçülebilir metrik |
| Üretim | Profiling + platform bütçesi |

## Code Examples

```csharp
// Örnek: bileşen referansını Awake'te cache'le
public class Example : MonoBehaviour {
    Transform _t;
    void Awake() { _t = transform; }
}
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Update'te allocate | GC spike |


## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Unity Manual](https://docs.unity3d.com/Manual/index.html) — resmi dokümantasyon
- [Unity Learn](https://learn.unity.com/) — eğitimler
- [Unity Forum](https://forum.unity.com/) — topluluk
