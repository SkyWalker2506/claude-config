---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://physicallybased.info
  - https://marmoset.co/posts/physically-based-rendering-and-you-can-too/
  - https://learnopengl.com/PBR/Theory
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
  - https://developer.blender.org/docs/release_notes/4.0/shading/
---

# PBR Theory — Material & Lighting Artist Knowledge

## 1. Energy Conservation Principle

Energy conservation is the foundation of PBR: the total light leaving a surface cannot exceed
the light arriving at it. Reflected light and refracted (transmitted/absorbed) light are
mutually exclusive — whatever energy gets reflected will no longer be absorbed by the material.

In practice:
- As **roughness increases**, specular highlights spread out but become dimmer (total energy stays constant)
- As **metallic increases**, diffuse contribution drops to zero (metals absorb all refracted light)
- The shader automatically balances diffuse + specular based on Fresnel

Blender's Principled BSDF enforces energy conservation internally. You do NOT need to
manually balance diffuse vs specular — set physically correct values and the shader handles it.

## 2. Metallic Workflow

The metallic workflow uses a single `Metallic` parameter to distinguish between two
fundamentally different material types:

### Dielectric (Non-Metal): Metallic = 0
- Reflect ~2-5% of light at normal incidence (F0)
- Have visible diffuse color (Base Color = albedo)
- Fresnel effect is strong: reflections increase at grazing angles
- Examples: skin, wood, stone, plastic, fabric, glass

### Metal (Conductor): Metallic = 1.0
- Reflect ~50-100% of light even at normal incidence
- NO diffuse component — Base Color becomes the reflection color
- Reflected light is tinted by the metal's color
- Examples: gold, silver, copper, iron, aluminum

### CRITICAL RULE: Metallic is Binary
- **NEVER use values between 0 and 1** for the metallic parameter
- The only exception: a very thin transition zone (0.0-0.05 wide) at edges where
  metal meets non-metal (e.g., rust on metal, paint chipping)
- In procedural workflows, use a mask that outputs clean 0 or 1 values

## 3. Roughness: Physical Meaning

Roughness controls the microsurface detail of a material:
- **0.0** = perfectly smooth mirror (physically impossible — use 0.02 minimum)
- **0.5** = moderately rough, blurry reflections
- **1.0** = completely rough, fully diffuse-looking reflections

### Roughness Values by Material Type

| Material | Roughness | Notes |
|----------|-----------|-------|
| Mirror/Chrome | 0.02-0.05 | Near-perfect reflection |
| Polished metal | 0.05-0.15 | Clear but slightly soft reflections |
| Brushed metal | 0.2-0.4 | Directional blur (use anisotropy) |
| Water | 0.02-0.05 | Very smooth |
| Glass (clean) | 0.02-0.1 | Depends on surface treatment |
| Plastic (glossy) | 0.2-0.4 | Visible reflections |
| Plastic (matte) | 0.5-0.7 | Soft reflections |
| Human skin (oily) | 0.3-0.5 | Forehead, nose bridge |
| Human skin (normal) | 0.4-0.6 | Cheeks, arms |
| Human skin (dry) | 0.6-0.8 | Elbows, knees, heels |
| Wood (polished) | 0.2-0.4 | Varnished furniture |
| Wood (raw) | 0.5-0.8 | Unfinished lumber |
| Stone (polished) | 0.1-0.3 | Marble, granite countertop |
| Stone (rough) | 0.7-0.95 | Concrete, sandstone |
| Fabric (silk) | 0.5-0.7 | Has sheen, not roughness-only |
| Fabric (cotton) | 0.8-1.0 | Nearly fully diffuse |
| Leather | 0.5-0.7 | Varies with treatment |
| Rubber | 0.7-0.9 | Matte surface |

## 4. Fresnel Effect and IOR

The Fresnel effect describes how reflectivity changes with viewing angle:
- **At normal incidence** (looking straight at surface): minimum reflectivity (F0)
- **At grazing angles** (looking along surface edge): all materials approach 100% reflectivity

### F0 and IOR Relationship

F0 = ((IOR - 1) / (IOR + 1))^2

### IOR Values for Common Materials

| Material | IOR | F0 (approx) |
|----------|-----|-------------|
| Water | 1.33 | 0.02 |
| Skin | 1.36-1.44 | 0.028 |
| Glass | 1.45-1.75 | 0.035-0.074 |
| Plastic / Acrylic | 1.46-1.55 | 0.035-0.046 |
| Diamond | 2.42 | 0.172 |
| Eye cornea | 1.376 | 0.025 |
| Fabric | 1.46-1.55 | 0.035-0.046 |
| Wood | 1.5-1.55 | 0.04-0.046 |
| Stone / Concrete | 1.5-1.62 | 0.04-0.056 |

### Metal F0 (RGB — tints reflection color)

| Metal | F0 R | F0 G | F0 B |
|-------|------|------|------|
| Silver | 0.972 | 0.960 | 0.915 |
| Aluminum | 0.913 | 0.922 | 0.924 |
| Gold | 1.000 | 0.766 | 0.336 |
| Copper | 0.955 | 0.638 | 0.538 |
| Iron | 0.562 | 0.565 | 0.578 |
| Titanium | 0.542 | 0.497 | 0.449 |

## 5. Common PBR Value Tables

### Comprehensive Material Reference

| Material | Base Color (sRGB) | Metallic | Roughness | IOR | SSS |
|----------|-------------------|----------|-----------|-----|-----|
| Human skin (light) | (0.79, 0.57, 0.47) | 0 | 0.4-0.7 | 1.4 | 0.1-0.2 |
| Human skin (medium) | (0.55, 0.35, 0.25) | 0 | 0.4-0.7 | 1.4 | 0.1-0.2 |
| Human skin (dark) | (0.32, 0.18, 0.12) | 0 | 0.4-0.7 | 1.4 | 0.05-0.1 |
| Steel | (0.76, 0.78, 0.78) | 1.0 | 0.1-0.3 | — | 0 |
| Gold | (1.0, 0.77, 0.34) | 1.0 | 0.1-0.3 | — | 0 |
| Copper | (0.96, 0.64, 0.54) | 1.0 | 0.1-0.3 | — | 0 |
| Wood (oak) | (0.43, 0.29, 0.17) | 0 | 0.4-0.7 | 1.5 | 0 |
| Stone (granite) | (0.45, 0.42, 0.40) | 0 | 0.6-0.9 | 1.55 | 0 |
| Marble (white) | (0.85, 0.83, 0.80) | 0 | 0.1-0.3 | 1.55 | 0.02-0.05 |
| Cotton fabric | (varies) | 0 | 0.8-1.0 | 1.5 | 0 |
| Silk | (varies) | 0 | 0.5-0.7 | 1.5 | 0 |
| Glass (clear) | (0.95, 0.95, 0.95) | 0 | 0.02-0.1 | 1.52 | 0 |
| Rubber | (varies) | 0 | 0.7-0.9 | 1.52 | 0 |
| Bone / Tooth | (0.88, 0.84, 0.75) | 0 | 0.3-0.5 | 1.55 | 0.03-0.05 |

## 6. Blender Principled BSDF Input Names

### Version History (CRITICAL for bpy code)

**Blender 3.x (LEGACY — do not use):**
- `Subsurface` (float, 0-1)
- `Subsurface Color` (color)
- `Specular` (float, 0-1)
- `Clearcoat` (float, 0-1)
- `Clearcoat Roughness` (float)

**Blender 4.0+ (CURRENT — use these):**
- `Subsurface Weight` (float, 0-1) — replaces `Subsurface`
- `Subsurface Scale` (float, meters) — NEW, controls SSS radius scale
- `Subsurface Radius` (vector RGB) — distance light travels per channel
- `Subsurface IOR` (float) — NEW
- `Subsurface Anisotropy` (float) — NEW
- `Specular IOR Level` (float, 0-1) — replaces `Specular`
- `Specular Tint` (color) — changed from float to color
- `Coat Weight` (float, 0-1) — replaces `Clearcoat`
- `Coat Roughness` (float) — replaces `Clearcoat Roughness`
- `Coat IOR` (float) — NEW
- `Coat Tint` (color) — NEW
- `Coat Normal` (vector) — NEW
- `Sheen Weight` (float) — replaces `Sheen`
- `Sheen Roughness` (float) — NEW
- `Sheen Tint` (color) — changed from float to color
- `Transmission Weight` (float) — replaces `Transmission`
- `Emission Color` (color) — replaces `Emission`
- `Emission Strength` (float)

**Blender 4.3+:**
- `Diffuse Roughness` (float) — NEW input added

**Blender 5.0+:**
- Same input names as 4.x (OpenPBR model, no further renames)
- Subsurface Color input remains REMOVED (uses Base Color)

### BANNED Input Names (will cause errors in 4.0+)
- `Subsurface Color` — REMOVED in 4.0
- `Specular` — RENAMED to `Specular IOR Level`
- `Clearcoat` — RENAMED to `Coat Weight`
- `Clearcoat Roughness` — RENAMED to `Coat Roughness`
- `Sheen` — RENAMED to `Sheen Weight`
- `Transmission` — RENAMED to `Transmission Weight`
- `Emission` — RENAMED to `Emission Color`

### Complete Input List (Blender 4.3+ / 5.x)

```
Base Color          (color)     default: (0.8, 0.8, 0.8, 1.0)
Metallic            (float)     default: 0.0, range: 0-1
Roughness           (float)     default: 0.5, range: 0-1
IOR                 (float)     default: 1.5, range: 1-6
Alpha               (float)     default: 1.0, range: 0-1
Normal              (vector)
Weight              (float)     default: 0.0
Diffuse Roughness   (float)     default: 0.0  [4.3+]

Subsurface Weight   (float)     default: 0.0, range: 0-1
Subsurface Radius   (vector)    default: (1.0, 0.2, 0.1)
Subsurface Scale    (float)     default: 0.05
Subsurface IOR      (float)     default: 1.4
Subsurface Anisotropy (float)   default: 0.0

Specular IOR Level  (float)     default: 0.5, range: 0-1
Specular Tint       (color)     default: (1.0, 1.0, 1.0, 1.0)
Anisotropic         (float)     default: 0.0
Anisotropic Rotation (float)    default: 0.0
Tangent             (vector)

Transmission Weight (float)     default: 0.0, range: 0-1

Coat Weight         (float)     default: 0.0, range: 0-1
Coat Roughness      (float)     default: 0.03
Coat IOR            (float)     default: 1.5
Coat Tint           (color)     default: (1.0, 1.0, 1.0, 1.0)
Coat Normal         (vector)

Sheen Weight        (float)     default: 0.0, range: 0-1
Sheen Roughness     (float)     default: 0.5
Sheen Tint          (color)     default: (1.0, 1.0, 1.0, 1.0)

Emission Color      (color)     default: (1.0, 1.0, 1.0, 1.0)
Emission Strength   (float)     default: 0.0

Thin Film Thickness (float)     default: 0.0  [4.2+]
Thin Film IOR       (float)     default: 1.33 [4.2+]
```

### Version-Safe bpy Access Pattern

```python
# ALWAYS use try/except for version safety
bsdf = nodes.new('ShaderNodeBsdfPrincipled')

# Safe input access
def set_input(node, name, value, fallback_name=None):
    """Set node input with version fallback."""
    try:
        node.inputs[name].default_value = value
    except KeyError:
        if fallback_name:
            try:
                node.inputs[fallback_name].default_value = value
            except KeyError:
                pass  # Input not available in this version

# Usage
set_input(bsdf, 'Subsurface Weight', 0.15, fallback_name='Subsurface')
set_input(bsdf, 'Specular IOR Level', 0.5, fallback_name='Specular')
set_input(bsdf, 'Coat Weight', 0.0, fallback_name='Clearcoat')
```
