---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/sss.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
  - https://nabesaka.com/blender-a-look-at-skin-shading/
  - https://gachoki.com/blender-subsurface-scattering/
  - https://physicallybased.info
---

# Skin Shader Techniques — Material & Lighting Artist Knowledge

## 1. Subsurface Scattering (SSS) Fundamentals

### What SSS Does
SSS simulates light penetrating a translucent surface, scattering inside, and exiting
at a different point. This is what makes organic materials (skin, wax, milk, leaves)
look "alive" rather than like painted plastic.

Without SSS: skin looks like colored plastic with hard shadow edges.
With SSS: shadows have soft warm edges, thin areas (ears, fingers) glow when backlit.

### When to Use SSS
- ALL organic skin materials (human, creature, alien)
- Wax, candles, soap
- Milk, juice, translucent liquids
- Leaves, petals, thin organic membranes
- Marble, jade, and other translucent stone

### When NOT to Use SSS
- Metals (fully opaque, SSS=0)
- Hard plastics (opaque, SSS=0)
- Glass (use Transmission Weight instead)
- Rock, concrete (fully opaque)

## 2. SSS Values for Different Skin Types

### Principled BSDF SSS Parameters (Blender 4.0+)

| Parameter | Input Name | Description |
|-----------|------------|-------------|
| SSS Amount | `Subsurface Weight` | How much SSS vs pure diffuse (0-1) |
| SSS Scale | `Subsurface Scale` | Global multiplier for radius (meters) |
| SSS Radius | `Subsurface Radius` | Per-channel scatter distance (R, G, B) |
| SSS IOR | `Subsurface IOR` | Internal refraction index |

### Values by Skin Type

#### Human Skin
```
Subsurface Weight:  0.1 - 0.2  (subtle, not overwhelming)
Subsurface Scale:   0.05 - 0.1 (at real-world scale, meters)
Subsurface Radius:  (1.0, 0.2, 0.1)  — canonical values
Subsurface IOR:     1.4
Base Color:         light: (0.79, 0.57, 0.47)
                    medium: (0.55, 0.35, 0.25)
                    dark: (0.32, 0.18, 0.12)
```

#### Goblin / Orc Skin (Green-tinted)
```
Subsurface Weight:  0.1 - 0.15
Subsurface Scale:   0.03 - 0.06  (thicker, less translucent skin)
Subsurface Radius:  (0.8, 0.3, 0.1)  — slightly more green scatter
Subsurface IOR:     1.4
Base Color:         goblin: (0.25, 0.35, 0.18)
                    orc: (0.30, 0.32, 0.15)
```

#### Undead / Pale Skin
```
Subsurface Weight:  0.05 - 0.1  (less blood = less SSS)
Subsurface Scale:   0.02 - 0.04
Subsurface Radius:  (0.6, 0.3, 0.2)  — less red dominance
Subsurface IOR:     1.4
Base Color:         (0.65, 0.60, 0.58)  — desaturated, slightly blue
```

#### Demon / Red Skin
```
Subsurface Weight:  0.15 - 0.25  (more blood = more SSS)
Subsurface Scale:   0.05 - 0.08
Subsurface Radius:  (1.0, 0.15, 0.08)  — strong red dominance
Subsurface IOR:     1.4
Base Color:         (0.55, 0.12, 0.08)
```

## 3. Why R > G > B in Subsurface Radius

Blood beneath the skin scatters **red light** the furthest. This is physically correct:
- **Red (1.0):** Blood hemoglobin is transparent to red light — it travels furthest
- **Green (0.2):** Partially absorbed by blood, scatters medium distance
- **Blue (0.1):** Strongly absorbed by blood and melanin, scatters least

This is why:
- Backlit ears glow RED (red light passes through)
- Thin skin between fingers shows RED when held to light
- Shadow edges on skin are slightly warm/red, not neutral gray

The default `Subsurface Radius` of `(1.0, 0.2, 0.1)` is physically motivated.

**Adjustments:**
- More blood flow (lips, cheeks): increase R further, e.g., `(1.2, 0.2, 0.1)`
- Less blood (corpse, stone creature): flatten ratios, e.g., `(0.5, 0.3, 0.2)`
- Alien green blood: swap channels, e.g., `(0.2, 1.0, 0.1)`

## 4. Roughness Variation Across Body

Skin is NOT uniformly rough. Oil glands, calluses, and moisture create variation:

| Body Region | Roughness | Reason |
|-------------|-----------|--------|
| Forehead (T-zone) | 0.3-0.4 | Oily, sebaceous glands |
| Nose bridge | 0.25-0.35 | Very oily |
| Cheeks | 0.45-0.55 | Normal moisture |
| Lips | 0.2-0.35 | Wet, glossy surface |
| Chin | 0.4-0.5 | Moderate oil |
| Neck | 0.5-0.6 | Drier than face |
| Arms | 0.5-0.65 | Normal body skin |
| Palms | 0.6-0.75 | Callused, textured |
| Elbows | 0.7-0.85 | Very dry, callused |
| Knees | 0.7-0.85 | Similar to elbows |
| Heels | 0.8-0.9 | Thickest callused skin |

**Implementation:** Use a Noise Texture with Map Range to drive roughness variation
procedurally (see node tree below).

## 5. Color Variation

Realistic skin needs color variation — it is never a single flat color:

### AO-Driven Darkening (Creases/Concavities)
- **Eye sockets:** Darker, slightly purple/blue (thin skin shows veins)
- **Nostrils:** Darker, more red
- **Neck creases:** Darker from ambient occlusion
- **Armpit / elbow crease:** Significantly darker
- **Between fingers:** Darker, warmer

### Lighter on Protrusions
- **Nose tip:** Slightly lighter, more red from blood
- **Cheekbones:** Lighter, can have slight flush
- **Knuckles:** Lighter, stretched skin
- **Forehead ridge:** Slightly lighter
- **Chin:** Lighter prominence

### Implementation Strategy
1. Base Color sets overall skin tone
2. Noise Texture (low frequency, scale 2-5) adds warm/cool variation
3. Noise Texture (medium frequency, scale 8-15) adds subtle blotchiness
4. Pointiness/Curvature data (if available) lightens convex areas
5. AO bake or cavity map darkens concavities

## 6. Complete Blender Node Tree for Realistic Skin

### Node Tree Overview

```
[Texture Coordinate] → [Mapping] → [Noise Tex (color var)] → [ColorRamp] ─┐
                                  → [Noise Tex (rough var)]  → [Map Range] ─┤
                                  → [Voronoi Tex (pores)]    → [Bump]     ─┤
                                  → [Noise Tex (wrinkles)]   → [Bump]     ─┤
                                                                            ↓
                                                              [Principled BSDF] → [Output]
```

### Step-by-Step Node Creation (bpy)

#### A. Principled BSDF — Base Settings

```python
# Node: ShaderNodeBsdfPrincipled
bsdf = nodes.new('ShaderNodeBsdfPrincipled')
bsdf.inputs['Base Color'].default_value = (0.79, 0.57, 0.47, 1.0)  # Light skin
bsdf.inputs['Metallic'].default_value = 0.0        # Skin is NEVER metallic
bsdf.inputs['Roughness'].default_value = 0.5        # Will be driven by texture
bsdf.inputs['IOR'].default_value = 1.4
bsdf.inputs['Subsurface Weight'].default_value = 0.15
bsdf.inputs['Subsurface Scale'].default_value = 0.05
bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
bsdf.inputs['Subsurface IOR'].default_value = 1.4
bsdf.inputs['Specular IOR Level'].default_value = 0.5
bsdf.inputs['Coat Weight'].default_value = 0.0      # No clearcoat on skin
bsdf.inputs['Sheen Weight'].default_value = 0.0     # No sheen on skin
```

#### B. Color Variation — Noise Texture + ColorRamp

```python
# Node: ShaderNodeTexCoord
tex_coord = nodes.new('ShaderNodeTexCoord')

# Node: ShaderNodeMapping
mapping = nodes.new('ShaderNodeMapping')

# Node: ShaderNodeTexNoise — color variation
noise_color = nodes.new('ShaderNodeTexNoise')
noise_color.inputs['Scale'].default_value = 3.0      # Low freq, broad patches
noise_color.inputs['Detail'].default_value = 4.0
noise_color.inputs['Roughness'].default_value = 0.6
noise_color.inputs['Distortion'].default_value = 0.2

# Node: ShaderNodeValToRGB (ColorRamp) — map noise to warm/cool variation
color_ramp = nodes.new('ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].position = 0.35
color_ramp.color_ramp.elements[0].color = (0.72, 0.48, 0.38, 1.0)  # Cooler
color_ramp.color_ramp.elements[1].position = 0.65
color_ramp.color_ramp.elements[1].color = (0.85, 0.58, 0.45, 1.0)  # Warmer

# Node: ShaderNodeMix (MixRGB in 4.x+) — blend variation with base
mix_color = nodes.new('ShaderNodeMix')
mix_color.data_type = 'RGBA'
mix_color.inputs[0].default_value = 0.3  # Factor — subtle blend

# Links
links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], noise_color.inputs['Vector'])
links.new(noise_color.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], mix_color.inputs['B'])
# Set mix_color input A to base skin color
links.new(mix_color.outputs['Result'], bsdf.inputs['Base Color'])
```

#### C. Roughness Variation — Noise Texture + Map Range

```python
# Node: ShaderNodeTexNoise — roughness variation
noise_rough = nodes.new('ShaderNodeTexNoise')
noise_rough.inputs['Scale'].default_value = 8.0      # Medium frequency
noise_rough.inputs['Detail'].default_value = 3.0
noise_rough.inputs['Roughness'].default_value = 0.5

# Node: ShaderNodeMapRange
map_range = nodes.new('ShaderNodeMapRange')
map_range.inputs['From Min'].default_value = 0.0
map_range.inputs['From Max'].default_value = 1.0
map_range.inputs['To Min'].default_value = 0.35       # Oily minimum
map_range.inputs['To Max'].default_value = 0.75        # Dry maximum

# Links
links.new(mapping.outputs['Vector'], noise_rough.inputs['Vector'])
links.new(noise_rough.outputs['Fac'], map_range.inputs['Value'])
links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])
```

#### D. Surface Detail — Bump from Voronoi (Pores) + Noise (Wrinkles)

```python
# Node: ShaderNodeTexVoronoi — skin pores (micro detail)
voronoi_pores = nodes.new('ShaderNodeTexVoronoi')
voronoi_pores.distance = 'EUCLIDEAN'
voronoi_pores.feature = 'F1'
voronoi_pores.inputs['Scale'].default_value = 120.0    # Fine pore detail

# Node: ShaderNodeBump — pore bump
bump_pores = nodes.new('ShaderNodeBump')
bump_pores.inputs['Strength'].default_value = 0.05     # Very subtle
bump_pores.inputs['Distance'].default_value = 0.001

# Node: ShaderNodeTexNoise — wrinkles / larger skin texture
noise_wrinkle = nodes.new('ShaderNodeTexNoise')
noise_wrinkle.inputs['Scale'].default_value = 18.0     # Medium-fine detail
noise_wrinkle.inputs['Detail'].default_value = 8.0
noise_wrinkle.inputs['Roughness'].default_value = 0.7

# Node: ShaderNodeBump — wrinkle bump (chained with pore bump)
bump_wrinkle = nodes.new('ShaderNodeBump')
bump_wrinkle.inputs['Strength'].default_value = 0.1
bump_wrinkle.inputs['Distance'].default_value = 0.005

# Links — chain bumps: wrinkle → pore → BSDF Normal
links.new(mapping.outputs['Vector'], voronoi_pores.inputs['Vector'])
links.new(mapping.outputs['Vector'], noise_wrinkle.inputs['Vector'])
links.new(noise_wrinkle.outputs['Fac'], bump_wrinkle.inputs['Height'])
links.new(bump_wrinkle.outputs['Normal'], bump_pores.inputs['Normal'])
links.new(voronoi_pores.outputs['Distance'], bump_pores.inputs['Height'])
links.new(bump_pores.outputs['Normal'], bsdf.inputs['Normal'])
```

## 7. EXACT Node Names — Blender 4.x/5.x Compatible

### Node Type IDs for `nodes.new()`

| Purpose | Node Type ID | Display Name |
|---------|-------------|--------------|
| Main shader | `ShaderNodeBsdfPrincipled` | Principled BSDF |
| Noise texture | `ShaderNodeTexNoise` | Noise Texture |
| Voronoi texture | `ShaderNodeTexVoronoi` | Voronoi Texture |
| Color ramp | `ShaderNodeValToRGB` | ColorRamp |
| Map range | `ShaderNodeMapRange` | Map Range |
| Bump | `ShaderNodeBump` | Bump |
| Mix (color) | `ShaderNodeMix` | Mix |
| Texture coord | `ShaderNodeTexCoord` | Texture Coordinate |
| Mapping | `ShaderNodeMapping` | Mapping |
| Math | `ShaderNodeMath` | Math |
| Output | `ShaderNodeOutputMaterial` | Material Output |

### Important Blender 4.x/5.x Notes

1. `ShaderNodeMixRGB` is deprecated in 4.0+ — use `ShaderNodeMix` with `data_type='RGBA'`
2. `ShaderNodeTexMusgrave` is deprecated in 4.1+ — use `ShaderNodeTexNoise` with `noise_type`
3. Principled BSDF `Subsurface Color` input does NOT exist in 4.0+ — SSS uses Base Color
4. Access inputs by NAME string, not by index (index changes between versions)

## 8. Skin Material Presets Summary

### Quick-Copy Settings

**Realistic Human (Light):**
```
Base Color: (0.79, 0.57, 0.47)    Metallic: 0.0
Roughness: 0.5 (driven)           IOR: 1.4
Subsurface Weight: 0.15           Subsurface Scale: 0.05
Subsurface Radius: (1.0, 0.2, 0.1)
```

**Stylized Cartoon:**
```
Base Color: (0.90, 0.65, 0.55)    Metallic: 0.0
Roughness: 0.6 (uniform)          IOR: 1.4
Subsurface Weight: 0.05           Subsurface Scale: 0.03
Subsurface Radius: (1.0, 0.4, 0.3)
```

**Game-Ready (Lower SSS):**
```
Base Color: (0.72, 0.52, 0.42)    Metallic: 0.0
Roughness: 0.5                    IOR: 1.4
Subsurface Weight: 0.08           Subsurface Scale: 0.03
Subsurface Radius: (1.0, 0.2, 0.1)
```
