---
last_updated: 2026-04-18
confidence: high
sources: 3
---

# LOD and Culling

## Quick Reference

| Teknik | CPU Overhead | GPU Impact | Mobil | Desktop |
|--------|--------------|-----------|-------|---------|
| LOD Groups | Minimal | Dusuk | Ideal | Ideal |
| Occlusion Culling | Medium | Yuksek | Uygun | Ideal |
| Frustum Culling | Minimal | Yuksek | Ideal | Ideal |
| Dynamic Batching | Medium | Orta | Uygun | Sinirli |
| Billboards | Minimal | Orta | Ideal | OK |

## LODGroup Setup

### Hierarchy
```
Model_LOD0_High (256 verts)
  ├─ Model_LOD1_Medium (128 verts)
  ├─ Model_LOD2_Low (64 verts)
  └─ Model_LOD3_Billboard (4 verts)
```

### Editor Setup
```
1. Select parent GameObject
2. Add Component → LOD Group
3. LOD Levels:
   - LOD 0: 100% → 70% distance (high detail)
   - LOD 1: 70% → 40% distance (medium)
   - LOD 2: 40% → 10% distance (low)
   - LOD 3: 10% → 0% distance (billboard/hidden)
4. Drag cada mesh rendererla LOD'a
```

### Code Config
```csharp
using UnityEngine;

public class LODConfigurator : MonoBehaviour
{
    void Start()
    {
        var lodGroup = GetComponent<LODGroup>();
        var lods = lodGroup.GetLODs();
        
        // Distances mobil için
        float[] distances = { 0.7f, 0.4f, 0.1f };
        
        // Android low-end: aggressive LOD
        #if UNITY_ANDROID
        distances = new float[] { 0.5f, 0.25f, 0.05f };
        #endif
        
        lodGroup.SetLODs(lods);
    }
}
```

### Distance Formula
```
LOD Distance = mesh_screen_height / camera_distance

Mobil rule of thumb:
- LOD 0 → screen height > 5%
- LOD 1 → screen height 2-5%
- LOD 2 → screen height 0.5-2%
- LOD 3 → screen height < 0.5%
```

## Occlusion Culling

### Setup Adimi
```
1. GameObject → Rendering → Occlusion Culling (scenede)
2. Window → Rendering → Occlusion Culling
3. Baked tab'ina gec
4. Statik objeleri mark et: Static checkbox → Occlusion Static
5. Bake button
```

### Build Parameters
```
Occlusion Culling window:
- Cell Size: 0.5 (tight), 1.0 (normal), 2.0 (loose)
- Small Occluder Threshold: 5 (aggressive), 50 (conservative)
- Backface Threshold: 100 (default)
```

### Kod'da Aktivasyon
```csharp
GL.SetRevertOnFrameBufferTexture(true); // OC uyumlu

// Runtime occlusion query
var occluded = !GetComponent<Renderer>().isVisible;
```

**Not:** Occlusion Culling baked geometry icin optimal. Dynamic objelerde frustum culling daha hızlı.

## Frustum Culling (Default)

### Otomatik
- Camera.main.cullingMask (Layers ile kontrol)
- Renderer.isVisible (API)

```csharp
// Manual override icin
public class FrustumCuller : MonoBehaviour
{
    Camera mainCam;
    Renderer rend;
    
    void Start()
    {
        mainCam = Camera.main;
        rend = GetComponent<Renderer>();
    }
    
    void Update()
    {
        var plane = new Plane[6];
        GeometryUtility.CalculateFrustumPlanes(mainCam, plane);
        
        if (GeometryUtility.TestPlanesAABB(plane, rend.bounds))
        {
            rend.enabled = true;
        }
        else
        {
            rend.enabled = false;
        }
    }
}
```

## Billboards (Far Distance)

### Simple Billboard Shader
```hlsl
Shader "Custom/Billboard"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" }
        LOD 100
        
        Pass
        {
            Blend SrcAlpha OneMinusSrcAlpha
            ZWrite Off
            
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            #include "UnityCG.cginc"
            
            struct v2f {
                float4 pos : SV_POSITION;
                float2 uv : TEXCOORD0;
            };
            
            sampler2D _MainTex;
            
            v2f vert(float4 vertex : POSITION, float2 uv : TEXCOORD0)
            {
                v2f o;
                
                // Billboard rotation
                float3 objCam = _WorldSpaceCameraPos - mul(unity_ObjectToWorld, float4(0,0,0,1)).xyz;
                float3 right = float3(1, 0, 0);
                float3 up = float3(0, 1, 0);
                
                float3 newPos = vertex.x * right + vertex.y * up;
                o.pos = mul(UNITY_MATRIX_VP, mul(unity_ObjectToWorld, float4(newPos, 1)));
                o.uv = uv;
                return o;
            }
            
            fixed4 frag(v2f i) : SV_Target
            {
                return tex2D(_MainTex, i.uv);
            }
            ENDCG
        }
    }
}
```

## Anti-Patterns
- LOD'ları olmadan detayli mesh'ler kullanmak
- Occlusion Culling'i static geometry icin bake etmek (dynamic objelerde useless)
- Billboard'u far distance'ta render etmek yerine `rend.enabled = false` ile disable etmek (material switch daha hızlı)
- LOD mesh'leri düş kalite olarak tasarlamak (% deplasmant/vertex drop izlenebilir olmali)

## Decision Matrix

| Senaryo | LOD | Occlusion | Billboard | Frustum |
|---------|-----|-----------|-----------|---------|
| Character (melee range) | 1-2 levels | No | No | Yes |
| Building (far distance) | 3-4 levels | Yes | Yes | Yes |
| Vegetation (grass, tree) | 2-3 levels | Optional | Yes | Yes |
| Prop (indoor) | 2 levels | Yes | No | Yes |
| Terrain detail (rock, stone) | 1-2 levels | Yes | Optional | Yes |

## Verification Checklist
- [ ] LOD seviyeleri polycount'ta %30-50 drop (her level)
- [ ] Occlusion culling bake'i completed, artifacts yok
- [ ] Billboard'lar useless pixel yok (transparent blend mode)
- [ ] Frustum culling enabled ve Profiler'de culled count > 0
- [ ] Distance-based LOD switch smooth ve jumpless (no popping)
- [ ] Mobile low-end aggressive LOD'lar, desktop liberal

## Deep Dive Sources
- [LOD Groups](https://docs.unity3d.com/Manual/class-LODGroup.html)
- [Occlusion Culling](https://docs.unity3d.com/Manual/OcclusionCulling.html)
- [Frustum Culling](https://docs.unity3d.com/Manual/FrustumCulling.html)
- [Performance Best Practices](https://docs.unity3d.com/Manual/BestPracticeGuides.html)
