---
last_updated: 2026-04-18
confidence: high
sources: 5
---

# PostFX Volume Presets

## Türkçe Özet

URP ve HDRP'de VolumeProfile asset'ler aracılığıyla post-process efektleri yönetilir. Volume Framework ile runtime'da preset'ler arasında geçiş yapılabilir. Her preset, belirli sinema türüne uygun effect kombinasyonlarını tanımlar.

## URP Volume vs HDRP Volume

| Özellik | URP | HDRP |
|---------|-----|------|
| Component adı | `Volume` | `Volume` |
| Profile türü | `VolumeProfile` | `VolumeProfile` |
| Effect component'ler | `VolumeComponent` türevi | `VolumeComponent` türevi |
| Rendering Pipeline | Universal Render Pipeline | High Definition Render Pipeline |
| Available effects | Bloom, DoF, MotionBlur, Chromatic Aberration, Vignette, ColorAdjustments | GTAO, Bloom, DoF, MotionBlur, ChromaticAberration, Vignette, FilmGrain (HDRP only), ColorGrading |

VolumeProfile asset yapısı her iki pipeline'da benzerdir; fark, hangi effect component'lerin available olmasında yatar.

## 6 Preset Profile

### 1. Cinematic
Sinematik görüntü kalitesi, ince efektler, doğal göz hareketleri simülasyonu.

```json
{
  "Bloom": {
    "active": true,
    "intensity": 0.3,
    "threshold": 1.0
  },
  "DepthOfField": {
    "active": true,
    "focusDistance": 10.0,
    "aperture": 5.6,
    "bladeCount": 8
  },
  "ColorAdjustments": {
    "active": true,
    "saturation": 0.0,
    "contrast": 0.0
  },
  "MotionBlur": {
    "active": true,
    "intensity": 0.5,
    "shutterAngle": 180
  },
  "Vignette": {
    "active": true,
    "intensity": 0.2,
    "smoothness": 0.3
  },
  "ChromaticAberration": {
    "active": true,
    "intensity": 0.1
  }
}
```

### 2. Stylized
Sanatsal görünüm, yüksek saturasyon, çizgi roman tarzı renk derinliği.

```json
{
  "Bloom": {
    "active": true,
    "intensity": 0.8,
    "threshold": 0.8
  },
  "ColorAdjustments": {
    "active": true,
    "saturation": 0.3,
    "contrast": 0.15
  },
  "ColorGrading": {
    "active": true,
    "lut": "stylized-lut",
    "lutContribution": 1.0
  },
  "DepthOfField": {
    "active": false
  },
  "MotionBlur": {
    "active": true,
    "intensity": 0.3
  }
}
```

### 3. Realistic
Gerçekçi görseller, minimal efekt, doğru tone mapping (ACES tonemap).

```json
{
  "Bloom": {
    "active": true,
    "intensity": 0.15,
    "threshold": 1.2
  },
  "DepthOfField": {
    "active": false
  },
  "ColorAdjustments": {
    "active": true,
    "saturation": 0.0,
    "contrast": 0.05
  },
  "Vignette": {
    "active": true,
    "intensity": 0.1,
    "smoothness": 0.5
  },
  "TonemappingMode": "ACES"
}
```

### 4. Anime
Düz renkler, stilize LUT, outline efekti (Sobel), yüksek Bloom.

```json
{
  "Bloom": {
    "active": true,
    "intensity": 0.9,
    "threshold": 0.5
  },
  "ColorGrading": {
    "active": true,
    "lut": "anime-lut",
    "lutContribution": 1.0
  },
  "ColorAdjustments": {
    "active": true,
    "saturation": 0.2,
    "contrast": 0.1
  },
  "Outline": {
    "active": true,
    "method": "Sobel",
    "thickness": 1.0
  },
  "DepthOfField": {
    "active": false
  }
}
```

### 5. Horror
Desatüre, kırmızı tint, ağır vignette, film grain, yüksek chromatic aberration.

```json
{
  "ColorAdjustments": {
    "active": true,
    "saturation": -0.4,
    "colorFilter": {
      "r": 1.0,
      "g": 0.6,
      "b": 0.6
    }
  },
  "Vignette": {
    "active": true,
    "intensity": 0.5,
    "smoothness": 0.4
  },
  "FilmGrain": {
    "active": true,
    "intensity": 0.3,
    "type": "Fine"
  },
  "ChromaticAberration": {
    "active": true,
    "intensity": 0.4
  },
  "Bloom": {
    "active": true,
    "intensity": 0.2
  }
}
```

### 6. Dreamy
Yumuşak odak, gölgelerde kat, pembe/şeftali white balance, ışıltılı Bloom.

```json
{
  "DepthOfField": {
    "active": true,
    "focusDistance": 50.0,
    "aperture": 1.4,
    "focalLength": 85.0
  },
  "ColorAdjustments": {
    "active": true,
    "shadows": 0.2,
    "colorFilter": {
      "r": 1.1,
      "g": 0.95,
      "b": 1.0
    }
  },
  "Bloom": {
    "active": true,
    "intensity": 0.7,
    "threshold": 0.8
  },
  "Vignette": {
    "active": true,
    "intensity": 0.15
  },
  "MotionBlur": {
    "active": true,
    "intensity": 0.2
  }
}
```

## Runtime Preset Swap

Volume profile'ını runtime'da değiştirmek:

```csharp
using UnityEngine.Rendering;

Volume volumeComponent = GetComponent<Volume>();
VolumeProfile newProfile = Resources.Load<VolumeProfile>("Presets/Cinematic");
volumeComponent.profile = newProfile;
```

Fade işlemi için volume weight'i interpolate etme:

```csharp
float startWeight = volumeComponent.weight;
float targetWeight = 1.0f;
float duration = 0.5f;
float elapsed = 0f;

while (elapsed < duration) {
    elapsed += Time.deltaTime;
    float t = elapsed / duration;
    volumeComponent.weight = Mathf.Lerp(startWeight, targetWeight, t);
    yield return null;
}
```

## Volume Blending

**Local Volume (small area):**
- Position'a bound, falloff distance
- Specific alanı etkileyebilmek için

**Global Volume (full frame):**
- Sahnede görünen tüm kamera'yı etkiler
- Priority değer high olunca daha öne alınır

**Weight Interpolation:**
```csharp
volumeComponent.weight = Mathf.Clamp01(volumeComponent.weight);
// 0 = inactive, 1 = fully active
```

Priority + Weight kombinasyonu ile birden fazla volume'ü blend etmek mümkündür.

## Anti-Patterns & Common Pitfalls

- **Effect eklenmiş değilse sessiz başarısızlık:** VolumeProfile asset'e component eklenmezse hiçbir hata görmez ama efekt uygulanmaz. Always verify asset contents.
- **Override flag kapalı:** VolumeComponent'in "override" checkbox'ı kapalıysa değerler uygulanmıyor. Mutlaka açılmalı.
- **Pipeline mismatch:** URP profile'ını HDRP'de veya tersi yüklemeye çalışmak; format uyuşmaz ama compile error vermez, runtime'da sessiz fail.
- **Weight = 0:** Volume aktif değilse (weight=0) efektler uygulanmaz. Runtime swap sırasında bunu kontrol etme.

## Deep Dive Sources

- [URP Volume docs](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal/manual/volumes.html) — sürüme göre güncellenmiş
- [HDRP Volume Framework](https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition/manual/volumes.html) — özellik referansı
- [PostProcess v2 (Built-in)](https://docs.unity3d.com/Packages/com.unity.postprocessing/manual/) — legacy pipeline için
