---
last_updated: 2026-04-18
confidence: high
sources: 3
---

# Render Pipeline Auto-Detect

## Türkçe Özet

Unity projesi URP, HDRP veya Built-in render pipeline kullanabilir. Agent her ortamda doğru API'yi seçebilmek için başlangıçta pipeline'ı tespit etmelidir. GraphicsSettings ve package dependencies üzerinden otomatik detection.

## Pipeline Tespit Yöntemi

```csharp
using UnityEngine.Rendering;

public static RenderPipelineType DetectRenderPipeline()
{
    RenderPipeline currentPipeline = GraphicsSettings.defaultRenderPipeline;
    
    if (currentPipeline == null)
    {
        return RenderPipelineType.BuiltIn;
    }
    
    string pipelineType = currentPipeline.GetType().Name;
    
    if (pipelineType == "UniversalRenderPipelineAsset")
    {
        return RenderPipelineType.URP;
    }
    else if (pipelineType == "HDRenderPipelineAsset")
    {
        return RenderPipelineType.HDRP;
    }
    
    return RenderPipelineType.Unknown;
}

public enum RenderPipelineType
{
    BuiltIn,
    URP,
    HDRP,
    Unknown
}
```

## Volume Component Selection

Tespit sonrası doğru Volume component'i seçme:

| Pipeline | Package | Volume Class | Profile Type | Available Effects |
|----------|---------|--------------|--------------|-------------------|
| Built-in | PostProcess v2 | `PostProcessVolume` | `PostProcessProfile` | Bloom, DoF, MotionBlur, Vignette, ChromaticAberration |
| URP | `com.unity.render-pipelines.universal` | `Volume` | `VolumeProfile` | Bloom, DoF, MotionBlur, Vignette, ChromaticAberration, ColorAdjustments |
| HDRP | `com.unity.render-pipelines.high-definition` | `Volume` | `VolumeProfile` | Bloom, DoF, MotionBlur, FilmGrain, GTAO, ColorGrading, ChromaticAberration |

**Kritik fark:** UnityEngine.Rendering.Volume class'ı aynı ancak VolumeProfile içeriğindeki effect'ler pipeline'a özel.

## PostProcess Stack v2 vs Volume Framework

**Built-in (PostProcess Stack v2):**
- `PostProcessVolume` bileşeni
- Profile asset'i manuel olarak assign edilmesi gerekir
- `PostProcessProfile` içinde effect component'ler

**URP/HDRP (Volume Framework):**
- Unified `Volume` component
- `VolumeProfile` asset'ler
- Runtime'da profile swap edilebilir
- Layer-based masking

## Pipeline-Agnostic Agent Behavior

Doğru davranış sırası:

1. **Başlangıç:** `DetectRenderPipeline()` çağrı, pipeline tipini cache'le
2. **Volume oluştur:** Pipeline'a göre doğru component'i instantiate et
3. **Profile yükle:** VolumeProfile (URP/HDRP) veya PostProcessProfile (Built-in)
4. **Efekt uygula:** Pipeline'a göre available effect component'ler

```csharp
public class PipelineAgnosticEffectManager
{
    private RenderPipelineType detectedPipeline;
    private Volume volumeComponent; // URP/HDRP
    private PostProcessVolume postProcessVolume; // Built-in
    
    public void Initialize()
    {
        detectedPipeline = DetectRenderPipeline();
        
        switch (detectedPipeline)
        {
            case RenderPipelineType.URP:
            case RenderPipelineType.HDRP:
                volumeComponent = gameObject.AddComponent<Volume>();
                volumeComponent.profile = LoadVolumeProfile("Assets/VolumeProfiles/Default");
                break;
                
            case RenderPipelineType.BuiltIn:
                postProcessVolume = gameObject.AddComponent<PostProcessVolume>();
                postProcessVolume.profile = LoadPostProcessProfile("Assets/PostProcessProfiles/Default");
                break;
        }
    }
    
    public void ApplyEffect(string effectName, Dictionary<string, float> parameters)
    {
        if (detectedPipeline == RenderPipelineType.BuiltIn)
        {
            ApplyPostProcessEffect(effectName, parameters);
        }
        else
        {
            ApplyVolumeEffect(effectName, parameters);
        }
    }
}
```

## Detection & Fallback

Eğer pipeline tespit edilemezse:

1. Package manifest'i kontrol et (`Packages/manifest.json`)
2. Paket içinde `render-pipelines.universal` veya `render-pipelines.high-definition` ara
3. Fallback: Built-in assume et, warning log'la

## Anti-Patterns

- **Hardcoded pipeline assumption:** Her ortamda URP olduğunu assume etmeme
- **Detection yapılmadan profile assign:** Pipeline mismatch'te sessiz fail
- **Multiple Volume/PostProcessVolume:** Sahnede çakışan volume'ler çok daha kötü sonuç verir

## Deep Dive Sources

- [GraphicsSettings API](https://docs.unity3d.com/ScriptReference/GraphicsSettings.html) — pipeline detection
- [Render Pipeline Overview](https://docs.unity3d.com/Manual/render-pipelines.html) — mimari
- [Package Dependencies](https://docs.unity3d.com/Manual/upm-dependencies.html) — manifest parsing
