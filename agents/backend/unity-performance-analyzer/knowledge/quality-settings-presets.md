---
last_updated: 2026-04-18
confidence: high
sources: 3
---

# Quality Settings Presets

## Quick Reference

| Preset | Target | FPS | Memory | GPU | Use Case |
|--------|--------|-----|--------|-----|----------|
| Mobile-Low | Entry-level Android/iOS | 30 | 512MB | Mali/Adreno | Budget phones, Asia |
| Mobile-High | High-end mobile | 60 | 2GB | A15+/Snapdragon 8x | Flagship phones |
| Desktop | PC/Mac | 60+ | 4GB+ | GTX1080+/RTX | Gaming PCs |
| Console | PS5/Xbox SX | 60 | 10GB+ | Custom | Console games |

## Mobile-Low Preset

### Hiyerarşi
```
Quality Setting: Mobile-Low
├─ Textures
│  └─ Default Texture Quality: 1/2 (0.5)
├─ Rendering
│  ├─ Anti-Aliasing: Disabled
│  ├─ Anisotropic Filtering: Disabled
│  ├─ Shadows: Disabled
│  └─ LOD Bias: 2.0 (aggressive)
├─ Physics
│  ├─ Rigidbody Simulation: Yes
│  └─ Collider Detail: Simple
└─ UI
   └─ Canvas Scalability: High
```

### Script
```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class MobileLowPreset : MonoBehaviour
{
    void ApplyPreset()
    {
        // Set quality level
        QualitySettings.SetQualityLevel(0, true); // Mobile-Low
        
        // Texture quality
        QualitySettings.masterTextureLimit = 1; // 50% resolution
        
        // Rendering
        QualitySettings.antiAliasing = 0; // No MSAA
        QualitySettings.anisotropicFiltering = AnisotropicFiltering.Disable;
        QualitySettings.shadowDistance = 0; // No shadows
        QualitySettings.lodBias = 2.0f; // Aggressive LOD
        
        // Physics
        Physics.defaultSolverIterations = 2;
        Physics.defaultSolverVelocityIterations = 1;
        Time.fixedDeltaTime = 0.033f; // 30 FPS physics
        
        // URP-specific
        var pipelineAsset = GraphicsSettings.defaultRenderingPipeline as UniversalRenderPipelineAsset;
        if (pipelineAsset != null)
        {
            pipelineAsset.renderScale = 0.75f; // 75% render resolution
            pipelineAsset.shadowDistance = 0f;
            pipelineAsset.supportsDynamicResolution = true;
        }
        
        Debug.Log("Mobile-Low preset applied");
    }
}
```

## Mobile-High Preset

```csharp
public class MobileHighPreset : MonoBehaviour
{
    void ApplyPreset()
    {
        QualitySettings.SetQualityLevel(2, true); // Mobile-High
        
        // Texture quality
        QualitySettings.masterTextureLimit = 0; // Full resolution
        
        // Rendering
        QualitySettings.antiAliasing = 2; // MSAA 2x
        QualitySettings.anisotropicFiltering = AnisotropicFiltering.Enable;
        QualitySettings.shadowDistance = 50f;
        QualitySettings.lodBias = 1.0f;
        
        // Physics
        Physics.defaultSolverIterations = 6;
        Physics.defaultSolverVelocityIterations = 2;
        Time.fixedDeltaTime = 0.0167f; // 60 FPS physics
        
        // URP
        var pipelineAsset = GraphicsSettings.defaultRenderingPipeline as UniversalRenderPipelineAsset;
        if (pipelineAsset != null)
        {
            pipelineAsset.renderScale = 1.0f;
            pipelineAsset.shadowDistance = 50f;
            pipelineAsset.supportsDynamicResolution = true;
        }
        
        Debug.Log("Mobile-High preset applied");
    }
}
```

## Desktop Preset

```csharp
public class DesktopPreset : MonoBehaviour
{
    void ApplyPreset()
    {
        QualitySettings.SetQualityLevel(4, true); // Desktop/Ultra
        
        // Texture quality
        QualitySettings.masterTextureLimit = 0;
        
        // Rendering
        QualitySettings.antiAliasing = 4; // MSAA 4x
        QualitySettings.anisotropicFiltering = AnisotropicFiltering.ForceEnable;
        QualitySettings.shadowDistance = 150f;
        QualitySettings.lodBias = 0.7f; // Finer LOD transitions
        
        // Physics
        Physics.defaultSolverIterations = 10;
        Physics.defaultSolverVelocityIterations = 2;
        Time.fixedDeltaTime = 0.0167f; // 60 FPS
        
        // URP/HDRP
        var pipelineAsset = GraphicsSettings.defaultRenderingPipeline as UniversalRenderPipelineAsset;
        if (pipelineAsset != null)
        {
            pipelineAsset.renderScale = 1.0f;
            pipelineAsset.shadowDistance = 150f;
            pipelineAsset.additionalLightsRenderingMode = LightRenderingMode.Forward;
            pipelineAsset.mainLightRenderingMode = LightRenderingMode.Forward;
        }
    }
}
```

## URP/HDRP Asset Tuning

### URP Asset Settings
```
Universal Render Pipeline Asset:
├─ Rendering
│  ├─ Render Scale: 0.75-1.0 (mobile: 0.75, desktop: 1.0)
│  ├─ Shadow Distance: 10-150 (mobile: 10, desktop: 100+)
│  ├─ Shadow Resolution: 512-2048
│  └─ Cascade Count: 1-4
├─ Quality
│  ├─ MSAA: 1-4x
│  ├─ Decal Tech: Screen Space / Clustered
│  └─ Post-Processing: Enabled/Disabled
└─ Lighting
   ├─ Max Visible Lights: 4-32
   └─ Per-Object Limit: 4-16
```

### HDRP Asset Settings (Desktop)
```
HDRP Asset:
├─ Rendering
│  ├─ Color Buffer: HDR 10bit
│  ├─ Depth Buffer: D32
│  └─ Upsampling Filter: Catmull-Rom
├─ Pathtracer: Enabled (optional)
└─ RayTracing: Enabled (optional)
```

## Runtime Device Detection

```csharp
public class AdaptiveQuality : MonoBehaviour
{
    void Start()
    {
        // Get device specs
        int totalMemory = SystemInfo.systemMemorySize;
        string deviceModel = SystemInfo.deviceModel;
        
        if (totalMemory < 1024) // < 1GB
        {
            ApplyMobileLow();
        }
        else if (totalMemory < 3072) // < 3GB
        {
            ApplyMobileHigh();
        }
        else
        {
            ApplyDesktop();
        }
        
        Debug.Log($"Device: {deviceModel}, RAM: {totalMemory}MB");
    }
    
    private void ApplyMobileLow() { /* ... */ }
    private void ApplyMobileHigh() { /* ... */ }
    private void ApplyDesktop() { /* ... */ }
}
```

## Anti-Patterns
- Hardcoded quality settings, device detection yok
- Desktop preset'i mobile'a apply etmek (memory waste, crash)
- Shadows'u 0 set etmek ama shadowy look'u istekten shader'da yapmaya calisma
- URP asset'i tunemeden only Quality Settings'i change etmek

## Decision Matrix

| Senaryo | Preset | Render Scale | LOD Bias | Shadows |
|---------|--------|--------------|----------|---------|
| Budget Android 2023 | Mobile-Low | 0.5 | 2.0 | No |
| Flagship iOS/Android | Mobile-High | 0.9 | 1.0 | Baked/Light |
| Gaming PC | Desktop | 1.0 | 0.7 | Realtime |
| Console (PS5/XSX) | Console-Ultra | 1.0 | 0.7 | Hybrid RT/Baked |

## Verification Checklist
- [ ] Her preset'in baseline FPS'i test edildi (30fps mobile-low, 60fps+desktop)
- [ ] Memory budget'ta stay (512MB mobile-low, 2GB mobile-high, 4GB+ desktop)
- [ ] Texture resolution mobile vs desktop'ta visibly different degil (PSNR > 30dB)
- [ ] Preset switch'leri runtime'da smooth (no stutter, no asset reload)
- [ ] URP/HDRP asset settings preset'e uyumlu

## Deep Dive Sources
- [QualitySettings API](https://docs.unity3d.com/ScriptReference/QualitySettings.html)
- [URP Asset Configuration](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal/manual/universalrp-asset.html)
- [HDRP Asset Setup](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition/manual/index.html)
- [Android Performance Guide](https://developer.android.com/games/optimize)
