---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/index.html
  - https://docs.blender.org/api/current/bpy.types.SceneEEVEE.html
  - https://superrendersfarm.com/article/blender-render-settings-optimization-guide
  - https://code.blender.org/2024/07/eevee-next-generation-in-blender-4-2-lts/
  - https://renderguide.com/blender-eevee-vs-cycles-tutorial/
---

# Render Settings — Material & Lighting Artist Knowledge

## 1. EEVEE vs Cycles: Trade-offs

### EEVEE (Real-time Rasterizer)
- **Speed:** 10-100x faster than Cycles
- **Method:** Screen-space techniques, shadow maps, probe-based lighting
- **Strengths:** Fast iteration, good for previews, interactive viewport
- **Weaknesses:** Limited global illumination, screen-space artifacts, no true caustics
- **Best for:** Quick previews, UI thumbnails, animation pre-viz, game-like rendering

### Cycles (Path Tracer)
- **Speed:** Slow, physically accurate
- **Method:** Ray tracing, Monte Carlo sampling
- **Strengths:** Full GI, accurate caustics, volumetrics, SSS accuracy
- **Weaknesses:** Slow, needs denoising, noise at low samples
- **Best for:** Final renders, portfolio pieces, physically accurate materials

### Decision Matrix

| Need | Use EEVEE | Use Cycles |
|------|-----------|------------|
| Quick preview | YES | — |
| Animation render | YES (fast) | Only if quality critical |
| SSS accuracy | — | YES |
| Caustics | — | YES |
| Glass/transparency | Limited | YES |
| Game asset preview | YES | — |
| Portfolio/hero shot | — | YES |
| Batch processing | YES | — |

## 2. Render Engine API Names

### CRITICAL: Engine name changed across Blender versions

```python
import bpy

# Blender 4.0 - 4.1 (old EEVEE)
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Blender 4.2 - 4.x (EEVEE Next)
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Blender 5.x (EEVEE Next renamed back to EEVEE)
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Cycles (all versions)
bpy.context.scene.render.engine = 'CYCLES'

# Workbench (all versions)
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
```

### Version-Safe Engine Setting

```python
import bpy

def set_render_engine(engine='eevee'):
    """Set render engine with version-safe fallback.
    
    Engine names by version:
      - 4.0-4.1:  BLENDER_EEVEE (old EEVEE)
      - 4.2-4.x:  BLENDER_EEVEE_NEXT (EEVEE Next)
      - 5.x:      BLENDER_EEVEE (EEVEE Next renamed back)
    """
    scene = bpy.context.scene

    if engine.lower() == 'cycles':
        scene.render.engine = 'CYCLES'
        return True

    if engine.lower() in ('eevee', 'eevee_next'):
        # 5.x uses BLENDER_EEVEE, 4.2-4.x uses BLENDER_EEVEE_NEXT
        for name in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
            try:
                scene.render.engine = name
                return True
            except TypeError:
                continue
    return False
```

## 3. EEVEE Settings for Quality

### EEVEE (4.0-4.1 Legacy)

```python
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
eevee = scene.eevee

# Sampling
eevee.taa_render_samples = 64    # Anti-aliasing samples (render)
eevee.taa_samples = 16           # Viewport samples

# Ambient Occlusion
eevee.use_gtao = True            # Screen-space AO
eevee.gtao_distance = 0.2        # AO radius
eevee.gtao_factor = 1.0          # AO strength
eevee.gtao_quality = 0.25        # AO quality

# Screen Space Reflections
eevee.use_ssr = True
eevee.use_ssr_refraction = True
eevee.ssr_quality = 0.25
eevee.ssr_max_roughness = 0.5
eevee.ssr_thickness = 0.2

# Shadows
eevee.shadow_cube_size = '1024'   # Point/Spot shadow resolution
eevee.shadow_cascade_size = '2048' # Sun shadow resolution
eevee.use_shadow_high_bitdepth = True
eevee.use_soft_shadows = True

# Bloom
eevee.use_bloom = True
eevee.bloom_threshold = 0.8
eevee.bloom_radius = 6.5
eevee.bloom_intensity = 0.05
```

### EEVEE Next (4.2+ / 5.x)

```python
scene = bpy.context.scene
# 4.2-4.x: BLENDER_EEVEE_NEXT, 5.x: BLENDER_EEVEE
set_render_engine('eevee')  # Use version-safe helper above
eevee = scene.eevee

# Sampling — EEVEE Next uses different sampling
eevee.taa_render_samples = 64     # Render samples
eevee.taa_samples = 16            # Viewport samples

# Ray Tracing (NEW in EEVEE Next)
eevee.use_raytracing = True        # Enable ray-traced effects
eevee.ray_tracing_method = 'SCREEN'  # 'SCREEN' or 'FULL' (if available)

# Shadow — EEVEE Next has improved shadow system
# Shadow settings are per-light in EEVEE Next

# Ambient Occlusion — EEVEE Next handles AO differently
# Ray-traced AO when raytracing enabled, otherwise screen-space
```

### EEVEE Quality Presets

| Setting | Preview | Quality | Maximum |
|---------|---------|---------|---------|
| taa_render_samples | 32 | 64 | 128 |
| taa_samples (viewport) | 8 | 16 | 32 |
| use_gtao | True | True | True |
| use_ssr | False | True | True |
| shadow_cube_size | '512' | '1024' | '2048' |
| shadow_cascade_size | '1024' | '2048' | '4096' |
| use_soft_shadows | False | True | True |

## 4. Cycles Settings

### Sample Configuration

```python
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
cycles = scene.cycles

# Sampling
cycles.samples = 256              # Render samples (128-512 typical)
cycles.preview_samples = 32       # Viewport samples
cycles.use_adaptive_sampling = True
cycles.adaptive_threshold = 0.01  # Noise threshold (lower = cleaner)
cycles.adaptive_min_samples = 32  # Minimum before adaptive kicks in

# Denoising
cycles.use_denoising = True
cycles.denoiser = 'OPENIMAGEDENOISE'  # 'OPENIMAGEDENOISE' or 'OPTIX'
cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'

# Light Paths
cycles.max_bounces = 12           # Total max bounces
cycles.diffuse_bounces = 4        # Diffuse bounce limit
cycles.glossy_bounces = 4         # Specular bounce limit
cycles.transmission_bounces = 8   # Glass/transmission bounce limit
cycles.volume_bounces = 0         # Volume scatter bounces
cycles.transparent_max_bounces = 8

# Performance
cycles.device = 'GPU'             # 'CPU' or 'GPU'
cycles.use_fast_gi = True         # Fast GI approximation
cycles.ao_bounces_render = 3      # AO approximation bounces
```

### Cycles Quality Presets

| Setting | Draft | Production | Hero |
|---------|-------|------------|------|
| samples | 64 | 256 | 512 |
| adaptive_threshold | 0.05 | 0.01 | 0.005 |
| max_bounces | 8 | 12 | 16 |
| diffuse_bounces | 2 | 4 | 6 |
| glossy_bounces | 2 | 4 | 8 |
| use_denoising | True | True | True |
| denoiser | OPENIMAGEDENOISE | OPENIMAGEDENOISE | OPENIMAGEDENOISE |

## 5. Color Management

### Filmic vs Standard

```python
scene = bpy.context.scene

# Filmic (RECOMMENDED for most renders)
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'None'  # Or 'Medium Contrast', 'High Contrast'
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0

# AgX (Blender 4.0+ alternative — improved over Filmic)
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'None'  # Or 'AgX - Punchy'

# Standard (raw, no tone mapping)
scene.view_settings.view_transform = 'Standard'
```

### When to Use Each

| Transform | When | Why |
|-----------|------|-----|
| Filmic | Default for most renders | Best highlight recovery, wide dynamic range |
| AgX | Modern replacement for Filmic (4.0+) | Better color preservation in highlights |
| Standard | UI icons, texture baking | No color transformation, exact values |
| Raw | Technical/data renders | No exposure or gamma, pure linear data |

### Color Space

```python
# Scene color space
scene.display_settings.display_device = 'sRGB'  # Monitor standard

# For HDR output
scene.view_settings.view_transform = 'Filmic'
scene.render.image_settings.file_format = 'OPEN_EXR'
scene.render.image_settings.color_depth = '32'
```

## 6. Resolution Settings

### Common Resolution Presets

```python
scene = bpy.context.scene

# Portrait (character showcase)
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

# Landscape (scene/environment)
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Square (social media / icon)
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024

# 4K (hero render)
scene.render.resolution_x = 3840
scene.render.resolution_y = 2160

# Thumbnail (quick preview)
scene.render.resolution_x = 512
scene.render.resolution_y = 512
```

### Resolution by Purpose

| Purpose | Resolution | Aspect | Format |
|---------|-----------|--------|--------|
| Character portrait | 1080x1920 | 9:16 | PNG |
| Character turnaround | 1920x1080 | 16:9 | PNG |
| Thumbnail | 512x512 | 1:1 | JPEG |
| Social media | 1080x1080 | 1:1 | PNG |
| Hero render | 3840x2160 | 16:9 | PNG/EXR |
| Animation frame | 1920x1080 | 16:9 | PNG |
| Game asset preview | 1024x1024 | 1:1 | PNG |

## 7. Output Format Settings

### PNG (Quality — lossless)

```python
scene = bpy.context.scene
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'    # Include alpha
scene.render.image_settings.color_depth = '16'     # 8 or 16 bit
scene.render.image_settings.compression = 15       # 0-100 (lossless, just size)
```

### JPEG (Speed — lossy)

```python
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.color_mode = 'RGB'     # No alpha in JPEG
scene.render.image_settings.quality = 90            # 0-100 (90+ for quality)
```

### OpenEXR (HDR — production)

```python
scene.render.image_settings.file_format = 'OPEN_EXR'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '32'     # Full float
scene.render.image_settings.exr_codec = 'DWAA'     # Good compression
```

### Format Decision Guide

| Need | Format | Why |
|------|--------|-----|
| Final render with transparency | PNG RGBA 16-bit | Lossless, alpha channel |
| Quick preview | JPEG 85-90% | Small file, fast |
| Post-processing pipeline | OpenEXR 32-bit | Full dynamic range |
| Animation frames | PNG 8-bit | Good balance |
| Web/social sharing | JPEG 90% or PNG 8-bit | Universal compatibility |
| Texture baking | PNG 8-bit RGB | Standard texture format |

## 8. Complete Render Setup — bpy Code Template

```python
import bpy

def setup_render(engine='eevee', quality='production', resolution='portrait'):
    """Configure render settings for character rendering.

    Args:
        engine: 'eevee' or 'cycles'
        quality: 'draft', 'production', 'hero'
        resolution: 'portrait', 'landscape', 'square', '4k', 'thumbnail'
    """
    scene = bpy.context.scene

    # --- Engine ---
    if engine == 'cycles':
        scene.render.engine = 'CYCLES'
        cycles = scene.cycles

        samples = {'draft': 64, 'production': 256, 'hero': 512}
        cycles.samples = samples.get(quality, 256)
        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.01 if quality != 'draft' else 0.05
        cycles.use_denoising = True
        cycles.denoiser = 'OPENIMAGEDENOISE'
        cycles.device = 'GPU'
        cycles.max_bounces = 12
        cycles.diffuse_bounces = 4
        cycles.glossy_bounces = 4
        cycles.transmission_bounces = 8

    else:  # eevee
        # Version-safe: 5.x=BLENDER_EEVEE, 4.2-4.x=BLENDER_EEVEE_NEXT
        for name in ('BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT'):
            try:
                scene.render.engine = name
                break
            except TypeError:
                continue

        eevee = scene.eevee
        samples = {'draft': 32, 'production': 64, 'hero': 128}
        eevee.taa_render_samples = samples.get(quality, 64)
        eevee.taa_samples = 16

        # Enable quality features (version-safe)
        try:
            eevee.use_gtao = True
            eevee.gtao_distance = 0.2
        except AttributeError:
            pass  # EEVEE Next handles AO differently

        try:
            eevee.use_ssr = True
            eevee.use_ssr_refraction = True
        except AttributeError:
            pass

        try:
            eevee.use_soft_shadows = True
        except AttributeError:
            pass

    # --- Resolution ---
    res_map = {
        'portrait':  (1080, 1920),
        'landscape': (1920, 1080),
        'square':    (1024, 1024),
        '4k':        (3840, 2160),
        'thumbnail': (512, 512),
    }
    rx, ry = res_map.get(resolution, (1080, 1920))
    scene.render.resolution_x = rx
    scene.render.resolution_y = ry
    scene.render.resolution_percentage = 100

    # --- Color Management ---
    # Use AgX if available (4.0+), else Filmic
    try:
        scene.view_settings.view_transform = 'AgX'
    except TypeError:
        scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0

    # --- Output ---
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '16'
    scene.render.image_settings.compression = 15

    # --- Film ---
    scene.render.film_transparent = True  # Transparent background

    return scene
```

## 9. Performance Tips

### EEVEE Performance

1. **Reduce shadow resolution** for preview: `shadow_cube_size = '512'`
2. **Disable SSR** when not needed: `use_ssr = False`
3. **Lower TAA samples** for viewport: `taa_samples = 8`
4. **Use EEVEE for iteration**, switch to Cycles for final only

### Cycles Performance

1. **Always use GPU** if available: `cycles.device = 'GPU'`
2. **Enable adaptive sampling**: fewer samples where image is clean
3. **Use denoising**: allows fewer samples with clean output
4. **Limit bounces** for draft: `max_bounces = 6`
5. **Use fast GI**: `cycles.use_fast_gi = True` approximates indirect light
6. **Reduce light paths** for SSS-heavy scenes: lower diffuse_bounces
7. **Tile size**: Let Blender auto-detect (default is optimal for modern GPUs)
