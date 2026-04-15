---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/noise.html
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeTexNoise.html
  - https://docs.blender.org/manual/en/latest/compositing/types/texture/voronoi.html
  - https://101.school/courses/procedural-materials-in-blender/modules/4-advanced-procedural-texturing
  - https://devtalk.blender.org/t/merging-the-musgrave-texture-and-noise-texture-nodes/30646
---

# Procedural Textures — Material & Lighting Artist Knowledge

## 1. Noise Texture

### Node Type: `ShaderNodeTexNoise`

The workhorse of procedural materials. Generates Perlin-based noise patterns.

### Parameters

| Parameter | Input Name | Range | Default | Description |
|-----------|------------|-------|---------|-------------|
| Scale | `Scale` | 0-∞ | 5.0 | Overall size of noise pattern. Higher = smaller features |
| Detail | `Detail` | 0-15 | 2.0 | Number of noise octaves. Higher = more fine detail |
| Roughness | `Roughness` | 0-1 | 0.5 | How much each octave contributes. Higher = more variation |
| Distortion | `Distortion` | 0-∞ | 0.0 | Warps the noise pattern. Creates organic, swirly effects |
| Lacunarity | `Lacunarity` | 0-∞ | 2.0 | Frequency multiplier between octaves [4.1+] |
| Normalize | — (property) | bool | True | Normalizes output to 0-1 range [4.1+] |

### Noise Type Property (Blender 4.1+ — merged Musgrave)

```python
noise_node = nodes.new('ShaderNodeTexNoise')
noise_node.noise_type = 'FBM'  # default — standard Perlin noise
```

| noise_type | Value | Description | Use Case |
|------------|-------|-------------|----------|
| `FBM` | `'FBM'` | Fractal Brownian Motion — smooth, homogeneous | General purpose, clouds, soft surfaces |
| `MULTIFRACTAL` | `'MULTIFRACTAL'` | Multiplicative cascade — more varied | Terrain, natural variation |
| `HYBRID_MULTIFRACTAL` | `'HYBRID_MULTIFRACTAL'` | Peaks and valleys with variable roughness | Mountain terrain, dramatic surfaces |
| `RIDGED_MULTIFRACTAL` | `'RIDGED_MULTIFRACTAL'` | Sharp ridges and creases | Veins, cracks, mountain ridges |
| `HETERO_TERRAIN` | `'HETERO_TERRAIN'` | Heterogeneous terrain with river-like channels | Eroded landscapes, organic flow |

### Outputs

| Output | Name | Description |
|--------|------|-------------|
| Factor | `Fac` | Grayscale noise value (0-1) |
| Color | `Color` | RGB noise (3 independent channels) |

### Use Cases & Scale Guidelines

| Use Case | Scale | Detail | Notes |
|----------|-------|--------|-------|
| Skin pores | 80-200 | 4-6 | Very fine detail |
| Skin blotchiness | 3-8 | 2-4 | Broad color variation |
| Wrinkles | 10-30 | 6-10 | Medium detail |
| Muscle definition | 2-8 | 2-4 | Broad bumps |
| Rock surface | 5-15 | 8-12 | High detail for grit |
| Wood grain | 3-8 | 4-6 | With distortion |
| Cloud/fog | 1-4 | 3-5 | Large-scale soft |
| Metal scratches | 20-50 | 2-3 | Fine linear marks |
| Fabric weave | 40-100 | 1-2 | Regular pattern base |
| Dirt/grime | 2-6 | 4-8 | Irregular patches |

### IMPORTANT: Musgrave Merger (Blender 4.1+)

In Blender 4.1, `ShaderNodeTexMusgrave` was merged INTO `ShaderNodeTexNoise`.
- The `noise_type` property on Noise Texture now includes all former Musgrave types
- `ShaderNodeTexMusgrave` still exists for backward compatibility but is deprecated
- New files should ALWAYS use `ShaderNodeTexNoise` with the appropriate `noise_type`
- The `Dimension` parameter was replaced by `Roughness` where `Roughness = Lacunarity^(-Dimension)`

## 2. Voronoi Texture

### Node Type: `ShaderNodeTexVoronoi`

Generates cell patterns based on Worley noise. Perfect for organic cellular structures.

### Properties

```python
voronoi = nodes.new('ShaderNodeTexVoronoi')
voronoi.distance = 'EUCLIDEAN'      # Distance metric
voronoi.feature = 'F1'             # Feature output type
voronoi.voronoi_dimensions = '3D'  # Dimensions
```

### Distance Metric (`distance` property)

| Value | Description | Use Case |
|-------|-------------|----------|
| `EUCLIDEAN` | Standard straight-line distance | Natural cells, pores |
| `MANHATTAN` | Grid-aligned distance | Architectural, crystal |
| `CHEBYCHEV` | Maximum axis distance | Blocky patterns |
| `MINKOWSKI` | Adjustable (uses Exponent param) | Custom hybrid shapes |

### Feature Output (`feature` property)

| Value | Description | Use Case |
|-------|-------------|----------|
| `F1` | Distance to nearest cell point | Rounded cells, bubbles, pores |
| `F2` | Distance to 2nd nearest point | Larger cells with boundaries |
| `SMOOTH_F1` | Smoothed F1 | Softer cells, organic shapes |
| `DISTANCE_TO_EDGE` | Distance to cell boundary | Cell outlines, cracks |
| `N_SPHERE_RADIUS` | Radius of inscribed sphere | Dot patterns |

### Parameters

| Parameter | Input Name | Default | Description |
|-----------|------------|---------|-------------|
| Scale | `Scale` | 5.0 | Number of cells — higher = more, smaller cells |
| Smoothness | `Smoothness` | 1.0 | Blend between cells [SMOOTH_F1 only] |
| Randomness | `Randomness` | 1.0 | 0=grid, 1=random cell placement |
| Exponent | `Exponent` | 0.5 | [MINKOWSKI distance only] |

### Outputs

| Output | Name | Description |
|--------|------|-------------|
| Distance | `Distance` | Distance value (grayscale) |
| Color | `Color` | Random color per cell |
| Position | `Position` | Cell center position |

### Scale Ranges for Common Uses

| Use Case | Scale | Feature | Notes |
|----------|-------|---------|-------|
| Skin pores | 100-200 | F1 | Fine cellular detail |
| Scales (reptile) | 15-40 | DISTANCE_TO_EDGE | Clear cell boundaries |
| Cobblestone | 5-12 | F1 | Rounded stones |
| Cracked earth | 3-8 | DISTANCE_TO_EDGE | Edge lines as cracks |
| Cell pattern | 5-15 | SMOOTH_F1 | Soft organic cells |
| Bubble foam | 8-20 | F1 | Round, varied sizes |

## 3. Musgrave Texture (LEGACY — Use Noise Texture Instead)

### Blender 4.1+: Use ShaderNodeTexNoise with noise_type

The old `ShaderNodeTexMusgrave` is DEPRECATED. Its functionality is now in the Noise
Texture node via the `noise_type` property.

### Migration Map

| Old Musgrave Type | New Noise noise_type | Notes |
|-------------------|---------------------|-------|
| fBM | `'FBM'` | Direct equivalent |
| Multifractal | `'MULTIFRACTAL'` | Direct equivalent |
| Hybrid Multifractal | `'HYBRID_MULTIFRACTAL'` | Direct equivalent |
| Ridged Multifractal | `'RIDGED_MULTIFRACTAL'` | Direct equivalent |
| Hetero Terrain | `'HETERO_TERRAIN'` | Direct equivalent |

### When to Use Each Type

- **FBM**: General purpose noise, clouds, soft organic surfaces (DEFAULT)
- **MULTIFRACTAL**: Terrain with natural variation, non-uniform surfaces
- **HYBRID_MULTIFRACTAL**: Mountains, dramatic terrain with peaks and valleys
- **RIDGED_MULTIFRACTAL**: Sharp features — veins, cracks, ridgelines, rivers
- **HETERO_TERRAIN**: Eroded landscapes, channel-like features

## 4. Wave Texture

### Node Type: `ShaderNodeTexWave`

Generates regular banded patterns. Ideal for structured materials.

### Properties

```python
wave = nodes.new('ShaderNodeTexWave')
wave.wave_type = 'BANDS'        # 'BANDS' or 'RINGS'
wave.bands_direction = 'X'      # 'X', 'Y', 'Z', 'DIAGONAL'
wave.wave_profile = 'SIN'       # 'SIN', 'SAW', 'TRI'
```

### Parameters

| Parameter | Input Name | Default | Description |
|-----------|------------|---------|-------------|
| Scale | `Scale` | 5.0 | Frequency of bands/rings |
| Distortion | `Distortion` | 0.0 | Organic warping |
| Detail | `Detail` | 2.0 | Noise octaves on the wave |
| Detail Scale | `Detail Scale` | 1.0 | Scale of detail noise |
| Detail Roughness | `Detail Roughness` | 0.5 | Roughness of detail |
| Phase Offset | `Phase Offset` | 0.0 | Shifts wave pattern |

### Use Cases

| Use Case | wave_type | bands_direction | Scale | Distortion |
|----------|-----------|----------------|-------|-----------|
| Wood grain | BANDS | X or Z | 3-8 | 2-5 |
| Fabric weave | BANDS | X then overlay Y | 30-60 | 0-1 |
| Water ripples | RINGS | — | 5-15 | 0.5-2 |
| Concentric rings | RINGS | — | 3-10 | 0 |
| Marble veins | BANDS | DIAGONAL | 2-5 | 5-10 |

## 5. Color Ramp (ValToRGB)

### Node Type: `ShaderNodeValToRGB`

Converts grayscale input to color or remaps value ranges. Essential for controlling
the output of any procedural texture.

### Common Uses

1. **Grayscale to color**: Map noise to a color palette
2. **Contrast control**: Sharpen or soften transitions
3. **Threshold/mask**: Create sharp cutoffs for mixing materials
4. **Value remapping**: Convert 0-1 range to useful material values

### bpy Setup

```python
ramp = nodes.new('ShaderNodeValToRGB')

# Access color stops
ramp.color_ramp.elements[0].position = 0.3
ramp.color_ramp.elements[0].color = (0.2, 0.15, 0.1, 1.0)  # Dark
ramp.color_ramp.elements[1].position = 0.7
ramp.color_ramp.elements[1].color = (0.6, 0.4, 0.3, 1.0)   # Light

# Add extra stops
elem = ramp.color_ramp.elements.new(0.5)
elem.color = (0.4, 0.25, 0.18, 1.0)  # Mid

# Interpolation
ramp.color_ramp.interpolation = 'LINEAR'  # 'EASE', 'CARDINAL', 'B_SPLINE', 'CONSTANT'
```

### Outputs

| Output | Name |
|--------|------|
| Color | `Color` |
| Alpha | `Alpha` |

## 6. Texture Coordinate Node

### Node Type: `ShaderNodeTexCoord`

Provides coordinate systems for texture mapping.

### Outputs and When to Use Each

| Output | Name | When to Use |
|--------|------|-------------|
| Generated | `Generated` | Default for procedural textures. Object bounding box 0-1. Consistent but stretches with non-uniform scale |
| Object | `Object` | Best for procedural on characters. Uses object local space. Scale-independent — texture stays consistent regardless of mesh deformation |
| UV | `UV` | When UV maps exist. Required for image textures. May have seams |
| Normal | `Normal` | For environment-dependent effects. World-space direction |
| Camera | `Camera` | Screen-space effects (rain on window) |
| Window | `Window` | UI/viewport-relative mapping |
| Reflection | `Reflection` | Environment map effects |

### Recommendation for Procedural Character Materials

**Always use `Object` coordinates** for procedural character textures:
- Consistent across mesh topology changes
- No UV dependency
- No stretching from scaling
- Works with any mesh resolution

```python
tex_coord = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeMapping')
links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
# Then connect mapping output to all texture node Vector inputs
```

## 7. Layering: Combining Multiple Textures

### Strategy: Frequency Layering

Build complex surfaces by combining textures at different frequencies:

```
Large-scale variation (scale 1-5)    →  Base color/roughness shifts
Medium detail (scale 5-30)            →  Surface features, bumps
Fine detail (scale 30-200)            →  Micro-surface (pores, grain)
```

### Mixing Techniques

#### Color Mixing
```python
# Node: ShaderNodeMix (replaces MixRGB in 4.0+)
mix = nodes.new('ShaderNodeMix')
mix.data_type = 'RGBA'
mix.blend_type = 'MIX'        # 'MIX', 'MULTIPLY', 'ADD', 'OVERLAY', etc.
mix.inputs[0].default_value = 0.5  # Factor (Fac)
# Input A (index 6 for RGBA) = first color
# Input B (index 7 for RGBA) = second color
```

#### Bump Chaining
Chain multiple bump nodes for layered surface detail:
```python
# Coarse bump → fine bump → BSDF Normal
bump_coarse = nodes.new('ShaderNodeBump')
bump_fine = nodes.new('ShaderNodeBump')

links.new(noise_coarse.outputs['Fac'], bump_coarse.inputs['Height'])
links.new(bump_coarse.outputs['Normal'], bump_fine.inputs['Normal'])  # Chain!
links.new(voronoi_fine.outputs['Distance'], bump_fine.inputs['Height'])
links.new(bump_fine.outputs['Normal'], bsdf.inputs['Normal'])
```

#### Math Operations for Blending
```python
math_node = nodes.new('ShaderNodeMath')
math_node.operation = 'MULTIPLY'  # 'ADD', 'SUBTRACT', 'MULTIPLY', 'MAXIMUM', etc.
```

## 8. Scale Guidelines Reference Table

### Quick Reference: Texture Scale by Purpose

| Purpose | Recommended Scale | Texture Type | Notes |
|---------|------------------|--------------|-------|
| **Micro-Surface** | | | |
| Skin pores | 80-200 | Voronoi F1 | Very fine cellular |
| Metal grain | 100-300 | Noise (FBM) | Barely visible roughness |
| Fabric fiber | 150-400 | Noise + Wave | Directional fine detail |
| **Surface Detail** | | | |
| Wrinkles | 10-30 | Noise (FBM) | Medium frequency |
| Scratches | 20-50 | Noise (RIDGED) | Linear features |
| Pebble texture | 15-40 | Voronoi SMOOTH_F1 | Rounded bumps |
| Scales (reptile) | 15-40 | Voronoi EDGE | Clear cell edges |
| Bark texture | 5-15 | Noise (HYBRID) | Layered detail |
| **Form/Shape** | | | |
| Muscle definition | 2-8 | Noise (FBM) | Broad, gentle bumps |
| Color patches | 2-6 | Noise (FBM) | Broad variation |
| Terrain features | 1-5 | Noise (HETERO) | Large-scale relief |
| Wood grain | 3-8 | Wave + Noise | Banded with distortion |

### Scale Interaction Note

Scale values assume Object coordinate space at roughly 1 Blender unit = 1 meter
(standard human character ~1.8 units tall). If your character is at different scale,
adjust proportionally:
- Character at 0.1 scale → multiply all texture scales by 10
- Character at 10 scale → divide all texture scales by 10
