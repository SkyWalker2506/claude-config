---
last_updated: 2026-04-18
confidence: high
sources: 3
---

# Texture Compression Formats

## Quick Reference

| Format | Platform | Ratio | Quality | Mobil | Desktop |
|--------|----------|-------|---------|-------|---------|
| ASTC 6x6 | Mobile (ARM) | 6:1 | Yuksek | Ideal | ✗ |
| ETC2 | Mobile (Qualcomm, etc) | 6:1 | Orta | OK | ✗ |
| BC7 | Desktop (DX11+) | 8:1 | Yuksek | ✗ | Ideal |
| DXT1/5 | Legacy | 4-6:1 | Dusuk | Eski | Yedek |
| RGBA32 | Uncompressed | 1:1 | Perfect | Onerilmez | Worst |

## ASTC (Adaptive Scalable Texture Compression)

### Mobile Ideal
- iOS 8+ (PowerVR, Apple Silicon)
- Android (Mali, Adreno, Tensor)
- Variable block size: 4x4 (high detail) to 12x12 (smooth)

### Setup
```csharp
// Asset → Texture → Platform → Mobile
// Compression: ASTC
// Format: ASTC 6x6 (default, ~3.5 bits/pixel)

// Kod'da
var tex = Resources.Load<Texture2D>("MyTexture");
Debug.Log($"Format: {tex.format}"); // TextureFormat.ASTC_6x6
```

### Best Practices
- Skybox/backgrounds: ASTC 8x8 (daha az kalite, daha hizli)
- Normal maps: ASTC 6x6 + Linear color space
- Diffuse: ASTC 6x6 standart

## ETC2 (Fallback Android)

### Uyumluluk
- Qualcomm, Samsung, HiSilicon chipsets
- BC1 desktop karsiligi degil — daha kaliteli
- Alpha channel → ETC2 RGBA8

```
Editor → Project Settings → Quality
Resolution and Presentation → supported compression:
  ☑ ETC2
  ☐ ASTC (seçerse ASTC)
```

## BC7 (Desktop)

### DirectX 11+ Recommended
- Nvidia, AMD desktop cards
- Near-lossless quality at 8:1 ratio
- HDR texture support (BC6H)

```csharp
// Asset → Texture → Windows Standalone
// Compression: BC7
// Format: BCn (BC7, BC6H for HDR)
```

## DXT1/DXT5 (Legacy)

### Eski Cihazlar
- DXT1: RGB, opacity (1 bit)
- DXT5: RGB + alpha (8 bit)
- 4:1 compression, düşük kalite

**Modern kurallari:** ASTC/BC7 yerine kullanma.

## Texture Size Presets

| Kalite | Diffuse | Normal | Specular | Note |
|--------|---------|--------|-----------|------|
| Low | 512x512 | 256x256 | 256x256 | Mobile low-end |
| Medium | 1024x1024 | 512x512 | 512x512 | Mobile mid-range |
| High | 2048x2048 | 1024x1024 | 1024x1024 | Mobile high-end, desktop |
| Ultra | 4096x4096 | 2048x2048 | 2048x2048 | Desktop only |

## Mipmap Setup

```csharp
// Asset → Texture → Texture Settings
// ☑ Generate Mip Maps
// Filter Mode: Trilinear
// Aniso Level: 4 (mobile), 8-16 (desktop)
```

### Mipmap Ratio
- Level 0 (Full): 2048×2048
- Level 1: 1024×1024 (25% ekstra memory)
- Level 2: 512×512
- ...
- Memory cost: +33% of base texture

## Crunch Compression (Optional)

```
Asset → Texture → Compression
  ☑ Use Crunch Compression
  Quality: 80-95 (0-100)
```

**Avantaj:** DL size %50 daha kucuk
**Dezavantaj:** GPU memory hala full size, unpack latency

## Anti-Patterns
- RGBA32'yi production'a koymak (6x memory waste)
- Mipmap'siz texture kullanmak (GPU sampling penalty)
- Platform-specific compression'u dinamik switch'lemek (compile complexity)
- Normal map'i sRGB'ye ayarlamak (should be Linear)

## Decision Matrix

| Senaryo | Format | Size | Mipmap | Crunch |
|---------|--------|------|--------|--------|
| Mobile diffuse | ASTC 6x6 | 1024×1024 | Yes | Optional |
| Mobile normal | ASTC 6x6 Linear | 512×512 | Yes | No |
| Desktop diffuse | BC7 | 2048×2048 | Yes | No |
| Skybox | ASTC 8x8 | 2048×2048 | Yes | Yes |
| Real-time light map | ASTC 6x6 | 2048×2048 | Yes | No |

## Verification Checklist
- [ ] Her texture'un platform-appropriate compression'u var
- [ ] Mipmaps enabled (Profiler'de GPU memory Sampled Texture kategorisinde %)
- [ ] RGBA32 texture yok (Profiler → Memory → Texture Category)
- [ ] Crunch compression → download size vs. unpack latency trade-off'i balanced
- [ ] Normal map'lar Linear color space'te

## Deep Dive Sources
- [Texture Compression Formats](https://docs.unity3d.com/Manual/class-TextureImporter.html)
- [ASTC Specs](https://github.com/KhronosGroup/KTX-Software)
- [ETC2 Android](https://developer.android.com/games/optimize/texture-compression)
- [Texture Streaming](https://docs.unity3d.com/Manual/TextureStreaming.html)
