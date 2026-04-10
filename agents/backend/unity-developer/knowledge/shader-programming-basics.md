---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Shader Programming Basics

## Quick Reference

| Pipeline | Notes |
|----------|-------|
| **URP/HDRP** | Shader Graph first; HLSL for custom |
| **Properties** | Exposed to materials |
| **SRP Batcher** | Compatible shaders batch better |

**2025–2026:** URP default for new projects; always test on target GPU tier.

## Patterns & Decision Matrix

| Hedef | Seçim |
|-------|--------|
| Mobil | URP + basit lit |
| PC konsol | HDRP / URP özellik seti |

## Code Examples

```hlsl
void surf (Input IN, inout SurfaceOutputStandard o) {
  o.Albedo = tex2D(_MainTex, IN.uv_MainTex).rgb;
}
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Her frame branch yoğun | GPU dalgalanması |
| Precision gereksiz yüksek | Mobil yavaş |

## Deep Dive Sources

- [Unity — Shader Graph](https://docs.unity3d.com/Packages/com.unity.shadergraph@latest)
