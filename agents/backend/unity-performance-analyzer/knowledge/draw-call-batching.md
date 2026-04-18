---
last_updated: 2026-04-18
confidence: high
sources: 3
---

# Draw-Call Batching

## Quick Reference
| Batching Tipi | CPU Overhead | GPU Uyum | Mobil | Desktop |
|---------------|--------------|---------|-------|---------|
| Static Batching | ~0 | Yuksek | OK | Ideal |
| Dynamic Batching | Orta | Orta | Uygun | Sinirli |
| SRP Batcher | Dusuk | Yuksek | Ideal | Ideal |
| GPU Instancing | Dusuk | Yuksek | Ideal | Ideal |
| BRG (Entities) | Minimal | Maksimal | Yuksek perf | Yuksek perf |

## Static Batching

### Setup
- Prefab'da "Static" checkbox → Batching Static
- Baked assets (statues, buildings, terrain details)
- **Sinir:** 64KB mesh vertex data per batch (orta cihazlarda)

```csharp
// Editor menüsü
GameObject > Rendering > Bake Lightmaps
// Static checkbox ile mesh combine
```

### Uygunluk Kontrol
```
Profiler → Rendering → Batched (Static)
Hedef: 20-50 batches per frame mobilde
```

## Dynamic Batching

### Koşullar
- Mesh'in <500 vertices (mobil), <30KB
- Same material + no instancing
- Shader'da Position, Normal, TexCoord0 gibi vertex attributes

```csharp
// QualitySettings'te enable et
QualitySettings.names[qualityLevel]; // "Mobile-Low" gibi
// veya Edit → Project Settings → Quality → Dynamic Batching checkbox
```

## SRP Batcher (Tavsiye Edilen)

### Nedir
- Shader'a MaterialPropertyBlock'ları dynamic set etmek yerine shader'in aynı bind grubu kullani
- URP/HDRP ile otomatik compatibility (eğer shader SRP Batcher uyumlu yazilmissa)

### Shader Uyum Checklist
```hlsl
// SRP Batcher uyumlu shader şablonu (URP/HDRP)
#include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

cbuffer UnityPerMaterial
{
    float4 _MainTex_ST;
    float4 _Color;
    float _Smoothness;
    // Material properties buraya
};

v2f vert(appdata v)
{
    // Vertex dönüşümü
    o.positionCS = TransformObjectToHClip(v.positionOS);
    return o;
}

float4 frag(v2f i) : SV_Target
{
    return _Color;
}
```

**Kural:** Material properties `UnityPerMaterial` cbuffer'ında olmalı.

### SRP Batcher Doğrulama
```
Profiler → Rendering → Draw Calls
- "SRP Batcher" satırı varsa ve > 0 ise aktif
- MaterialPropertyBlock yerine SetColor/SetFloat kullan
```

## GPU Instancing

### Setup
```csharp
// Shader'da multi_compile pragma
#pragma multi_compile_instancing

// Per-instance properties
UNITY_INSTANCING_BUFFER_START(Props)
    UNITY_DEFINE_INSTANCED_PROP(float4, _Color)
UNITY_INSTANCING_BUFFER_END(Props)

// Fragment shader'da
float4 albedo = UNITY_ACCESS_INSTANCED_PROP(Props, _Color);
```

### Kullan
```csharp
// Material'dan gpu instancing enable et
material.enableInstancing = true;

// Render loop
Graphics.DrawMeshInstanced(mesh, 0, material, matrices);
```

## BRG (Batch Rendering Group)

### Modern Approach (Unity 2021.2+)
```csharp
using Unity.Rendering;

// Entities + Graphics package
var entity = EntityManager.CreateEntity();
entity.AddComponentData(new Rendering { ... });
entity.AddComponentData(new Transforms { ... });
// BRG otomatik batching ve culling yapar
```

## Anti-Patterns
- Static batching'i dinamik objelere uygulamak
- SRP Batcher'i shader'a uygulamadan GPU instancing kullanmak
- Draw call sayisini kontrol etmeden material sayisini arttirmak
- Batching optimization'da frame time variance'i measure etmemek

## Decision Matrix

| Senaryo | Uygulamak | Neden |
|---------|-----------|-------|
| Statik mesh (statue, building) | Static Batching | CPU overhead 0, GPU optimal |
| Dinamik moving obje (enemy) | GPU Instancing + SRP Batcher | CPU-efficient, batching |
| Particle system | BRG + GPU Instancing | Best scalability |
| UI Canvas | Canvas → Batch'le | Built-in optimization |
| Terrain (herbalar) | Static Batching + LOD | CPU overhead minimal |

## Verification Checklist
- [ ] Batched draw call sayisi < 50 mobilde, < 200 desktop
- [ ] ProfilerRecorder ile draw call count'u baseline'dan < 10% sapma
- [ ] SRP Batcher'i kullaniyorsa Profiler'de "SRP Batcher" aktif gostermesi
- [ ] Static batch memory (Editor → Memory Profiler) acceptable range'de

## Deep Dive Sources
- [SRP Batcher Docs](https://docs.unity3d.com/Manual/SRPBatcher.html)
- [GPU Instancing](https://docs.unity3d.com/Manual/GPUInstancing.html)
- [Static Batching](https://docs.unity3d.com/Manual/StaticBatching.html)
- [Batch Rendering Group](https://docs.unity3d.com/Manual/BRG.html)
