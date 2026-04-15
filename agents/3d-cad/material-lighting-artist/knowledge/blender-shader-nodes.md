---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeBsdfPrincipled.html
  - https://docs.blender.org/api/current/bpy.types.ShaderNodeTexNoise.html
  - https://developer.blender.org/docs/release_notes/4.0/shading/
  - https://developer.blender.org/docs/release_notes/5.0/python_api/
  - https://devtalk.blender.org/t/feedback-on-breaking-python-api-changes-for-shader-nodes/23281
---

# Blender Shader Nodes (4.x/5.x) — Material & Lighting Artist Knowledge

## 1. Principled BSDF Input Names — Version Differences

### CRITICAL: Blender 4.0 was a breaking change for shader node input names

**The Principled BSDF was overhauled in Blender 4.0** based on the OpenPBR surface model.
Many inputs were renamed, removed, or restructured. Code using old names WILL FAIL.

### Input Name Migration Table

| Blender 3.x (LEGACY) | Blender 4.0+ (CURRENT) | Type | Default |
|-----------------------|------------------------|------|---------|
| `Subsurface` | `Subsurface Weight` | float | 0.0 |
| `Subsurface Color` | **REMOVED** — uses Base Color | — | — |
| — | `Subsurface Scale` (NEW) | float | 0.05 |
| — | `Subsurface IOR` (NEW) | float | 1.4 |
| — | `Subsurface Anisotropy` (NEW) | float | 0.0 |
| `Specular` | `Specular IOR Level` | float | 0.5 |
| `Specular Tint` (float) | `Specular Tint` (color) | color | white |
| `Clearcoat` | `Coat Weight` | float | 0.0 |
| `Clearcoat Roughness` | `Coat Roughness` | float | 0.03 |
| — | `Coat IOR` (NEW) | float | 1.5 |
| — | `Coat Tint` (NEW) | color | white |
| — | `Coat Normal` (NEW) | vector | — |
| `Sheen` | `Sheen Weight` | float | 0.0 |
| — | `Sheen Roughness` (NEW) | float | 0.5 |
| `Sheen Tint` (float) | `Sheen Tint` (color) | color | white |
| `Transmission` | `Transmission Weight` | float | 0.0 |
| — | `Thin Film Thickness` (NEW 4.2) | float | 0.0 |
| — | `Thin Film IOR` (NEW 4.2) | float | 1.33 |
| `Emission` | `Emission Color` | color | white |
| — | `Diffuse Roughness` (NEW 4.3) | float | 0.0 |

### BANNED Input Names (error in 4.0+)

These names DO NOT EXIST in Blender 4.0+. Using them will cause `KeyError`:

```python
# WILL FAIL — DO NOT USE
node.inputs['Subsurface Color']     # REMOVED — SSS uses Base Color now
node.inputs['Specular']             # RENAMED to 'Specular IOR Level'
node.inputs['Clearcoat']            # RENAMED to 'Coat Weight'
node.inputs['Clearcoat Roughness']  # RENAMED to 'Coat Roughness'
node.inputs['Sheen']                # RENAMED to 'Sheen Weight'
node.inputs['Transmission']         # RENAMED to 'Transmission Weight'
node.inputs['Emission']             # RENAMED to 'Emission Color'
```

### Blender 5.0+ Notes

Blender 5.0 uses the same input names as 4.x. No further renames.
The OpenPBR model was further refined but input socket names remain stable.

## 2. Complete Node Type Reference

### Shader Nodes

| Purpose | Node Type ID | Display Name |
|---------|-------------|--------------|
| Principled BSDF | `ShaderNodeBsdfPrincipled` | Principled BSDF |
| Diffuse BSDF | `ShaderNodeBsdfDiffuse` | Diffuse BSDF |
| Glossy BSDF | `ShaderNodeBsdfGlossy` | Glossy BSDF |
| Glass BSDF | `ShaderNodeBsdfGlass` | Glass BSDF |
| Emission | `ShaderNodeEmission` | Emission |
| Transparent | `ShaderNodeBsdfTransparent` | Transparent BSDF |
| Subsurface Scatter | `ShaderNodeSubsurfaceScattering` | Subsurface Scattering |
| Mix Shader | `ShaderNodeMixShader` | Mix Shader |
| Add Shader | `ShaderNodeAddShader` | Add Shader |

### Texture Nodes

| Purpose | Node Type ID | Display Name | Notes |
|---------|-------------|--------------|-------|
| Noise Texture | `ShaderNodeTexNoise` | Noise Texture | Includes Musgrave types in 4.1+ |
| Voronoi Texture | `ShaderNodeTexVoronoi` | Voronoi Texture | |
| Wave Texture | `ShaderNodeTexWave` | Wave Texture | |
| Checker Texture | `ShaderNodeTexChecker` | Checker Texture | |
| Gradient Texture | `ShaderNodeTexGradient` | Gradient Texture | |
| Magic Texture | `ShaderNodeTexMagic` | Magic Texture | |
| Brick Texture | `ShaderNodeTexBrick` | Brick Texture | |
| Image Texture | `ShaderNodeTexImage` | Image Texture | |
| Environment Texture | `ShaderNodeTexEnvironment` | Environment Texture | |
| Musgrave Texture | `ShaderNodeTexMusgrave` | Musgrave Texture | **DEPRECATED 4.1+ — use Noise** |

### Converter Nodes

| Purpose | Node Type ID | Display Name |
|---------|-------------|--------------|
| Color Ramp | `ShaderNodeValToRGB` | ColorRamp |
| RGB to BW | `ShaderNodeRGBToBW` | RGB to BW |
| Math | `ShaderNodeMath` | Math |
| Vector Math | `ShaderNodeVectorMath` | Vector Math |
| Map Range | `ShaderNodeMapRange` | Map Range |
| Clamp | `ShaderNodeClamp` | Clamp |
| Combine Color | `ShaderNodeCombineColor` | Combine Color |
| Separate Color | `ShaderNodeSeparateColor` | Separate Color |
| Combine XYZ | `ShaderNodeCombineXYZ` | Combine XYZ |
| Separate XYZ | `ShaderNodeSeparateXYZ` | Separate XYZ |

### Vector Nodes

| Purpose | Node Type ID | Display Name |
|---------|-------------|--------------|
| Bump | `ShaderNodeBump` | Bump |
| Normal Map | `ShaderNodeNormalMap` | Normal Map |
| Displacement | `ShaderNodeDisplacement` | Displacement |
| Vector Displacement | `ShaderNodeVectorDisplacement` | Vector Displacement |
| Mapping | `ShaderNodeMapping` | Mapping |

### Input Nodes

| Purpose | Node Type ID | Display Name |
|---------|-------------|--------------|
| Texture Coordinate | `ShaderNodeTexCoord` | Texture Coordinate |
| Object Info | `ShaderNodeObjectInfo` | Object Info |
| Geometry | `ShaderNodeNewGeometry` | Geometry |
| Camera Data | `ShaderNodeCameraData` | Camera Data |
| Fresnel | `ShaderNodeFresnel` | Fresnel |
| Layer Weight | `ShaderNodeLayerWeight` | Layer Weight |
| RGB | `ShaderNodeRGB` | RGB |
| Value | `ShaderNodeValue` | Value |

### Color Nodes

| Purpose | Node Type ID | Display Name | Notes |
|---------|-------------|--------------|-------|
| Mix | `ShaderNodeMix` | Mix | Replaces MixRGB in 4.0+ |
| RGB Curves | `ShaderNodeRGBCurve` | RGB Curves | |
| Hue Saturation | `ShaderNodeHueSaturation` | Hue/Saturation/Value | |
| Invert | `ShaderNodeInvert` | Invert | |
| Brightness/Contrast | `ShaderNodeBrightContrast` | Brightness/Contrast | |
| Gamma | `ShaderNodeGamma` | Gamma | |
| MixRGB | `ShaderNodeMixRGB` | MixRGB | **DEPRECATED 4.0+ — use ShaderNodeMix** |

### Output Nodes

| Purpose | Node Type ID | Display Name |
|---------|-------------|--------------|
| Material Output | `ShaderNodeOutputMaterial` | Material Output |

## 3. Node Creation and Linking Patterns

### Basic Node Creation

```python
import bpy

# Get or create material
mat = bpy.data.materials.new(name='SkinMaterial')
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create nodes
output = nodes.new('ShaderNodeOutputMaterial')
bsdf = nodes.new('ShaderNodeBsdfPrincipled')

# Position nodes (for readability in Shader Editor)
output.location = (400, 0)
bsdf.location = (0, 0)

# Link: BSDF → Output
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

### Link Pattern

```python
# General pattern:
links.new(source_node.outputs['OutputName'], target_node.inputs['InputName'])

# Common connections:
links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
links.new(noise.outputs['Fac'], map_range.inputs['Value'])
links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])
links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
```

### Setting Input Values

```python
# Float inputs
bsdf.inputs['Roughness'].default_value = 0.5
bsdf.inputs['Metallic'].default_value = 0.0

# Color inputs (RGBA tuple)
bsdf.inputs['Base Color'].default_value = (0.8, 0.5, 0.4, 1.0)
bsdf.inputs['Emission Color'].default_value = (0.0, 0.0, 0.0, 1.0)

# Vector inputs (XYZ tuple)
bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
```

## 4. Version-Safe Input Access Pattern

### The try/except Pattern

ALWAYS use this pattern when accessing inputs that might differ between versions:

```python
def safe_set_input(node, name, value, fallback_name=None):
    """Set a node input value with version-safe fallback.

    Args:
        node: The shader node
        name: Primary input name (Blender 4.0+)
        value: Value to set
        fallback_name: Legacy input name (Blender 3.x) for backward compatibility
    """
    try:
        node.inputs[name].default_value = value
        return True
    except KeyError:
        if fallback_name:
            try:
                node.inputs[fallback_name].default_value = value
                return True
            except KeyError:
                pass
    return False


def safe_link_input(links, source_output, node, input_name, fallback_name=None):
    """Create a link to a node input with version-safe fallback."""
    try:
        links.new(source_output, node.inputs[input_name])
        return True
    except KeyError:
        if fallback_name:
            try:
                links.new(source_output, node.inputs[fallback_name])
                return True
            except KeyError:
                pass
    return False
```

### Usage Examples

```python
bsdf = nodes.new('ShaderNodeBsdfPrincipled')

# Version-safe input setting
safe_set_input(bsdf, 'Subsurface Weight', 0.15, fallback_name='Subsurface')
safe_set_input(bsdf, 'Specular IOR Level', 0.5, fallback_name='Specular')
safe_set_input(bsdf, 'Coat Weight', 0.0, fallback_name='Clearcoat')
safe_set_input(bsdf, 'Sheen Weight', 0.0, fallback_name='Sheen')
safe_set_input(bsdf, 'Transmission Weight', 0.0, fallback_name='Transmission')
safe_set_input(bsdf, 'Emission Color', (0.0, 0.0, 0.0, 1.0), fallback_name='Emission')

# Version-safe linking
safe_link_input(links, noise.outputs['Fac'], bsdf,
    'Subsurface Weight', fallback_name='Subsurface')
```

### Version Detection

```python
import bpy

blender_version = bpy.app.version  # Tuple: (5, 1, 0)

if blender_version >= (4, 0, 0):
    # Use new input names
    sss_input = 'Subsurface Weight'
    spec_input = 'Specular IOR Level'
    coat_input = 'Coat Weight'
else:
    # Legacy names
    sss_input = 'Subsurface'
    spec_input = 'Specular'
    coat_input = 'Clearcoat'
```

## 5. Common Node Tree Templates

### Template: Skin Material

```python
def create_skin_material(name='Skin', base_color=(0.79, 0.57, 0.47)):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (800, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (400, 0)
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.5
    bsdf.inputs['IOR'].default_value = 1.4
    safe_set_input(bsdf, 'Subsurface Weight', 0.15)
    safe_set_input(bsdf, 'Subsurface Scale', 0.05)
    bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)

    # Texture Coordinate + Mapping
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])

    # Roughness variation
    noise_rough = nodes.new('ShaderNodeTexNoise')
    noise_rough.location = (-200, -200)
    noise_rough.inputs['Scale'].default_value = 8.0
    noise_rough.inputs['Detail'].default_value = 3.0
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (100, -200)
    map_range.inputs['To Min'].default_value = 0.35
    map_range.inputs['To Max'].default_value = 0.75
    links.new(mapping.outputs['Vector'], noise_rough.inputs['Vector'])
    links.new(noise_rough.outputs['Fac'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])

    # Bump: pores + wrinkles
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-200, -500)
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = 120.0
    bump = nodes.new('ShaderNodeBump')
    bump.location = (200, -400)
    bump.inputs['Strength'].default_value = 0.05
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(voronoi.outputs['Distance'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Final link
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
```

### Template: Metal Material

```python
def create_metal_material(name='Metal', base_color=(0.76, 0.78, 0.78), roughness=0.2):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0  # ALWAYS 1 for metal
    bsdf.inputs['Roughness'].default_value = roughness
    safe_set_input(bsdf, 'Subsurface Weight', 0.0)

    # Scratch/wear noise for roughness variation
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, -100)
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 4.0
    map_range = nodes.new('ShaderNodeMapRange')
    map_range.location = (-100, -100)
    map_range.inputs['To Min'].default_value = roughness * 0.5
    map_range.inputs['To Max'].default_value = roughness * 1.5
    links.new(noise.outputs['Fac'], map_range.inputs['Value'])
    links.new(map_range.outputs['Result'], bsdf.inputs['Roughness'])

    # Subtle bump for surface imperfections
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -200)
    bump.inputs['Strength'].default_value = 0.02
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
```

### Template: Fabric Material

```python
def create_fabric_material(name='Fabric', base_color=(0.3, 0.15, 0.1)):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (*base_color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.85
    safe_set_input(bsdf, 'Sheen Weight', 0.3)
    safe_set_input(bsdf, 'Sheen Roughness', 0.5)
    safe_set_input(bsdf, 'Subsurface Weight', 0.0)

    # Weave pattern using Wave Texture
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-400, -100)
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'X'
    wave.inputs['Scale'].default_value = 50.0
    wave.inputs['Detail'].default_value = 2.0
    wave.inputs['Distortion'].default_value = 0.5

    # Bump from weave
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -200)
    bump.inputs['Strength'].default_value = 0.08
    links.new(wave.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    return mat
```

## 6. Deprecated Node Migration Guide

### ShaderNodeMixRGB → ShaderNodeMix

```python
# OLD (3.x) — DEPRECATED
mix = nodes.new('ShaderNodeMixRGB')
mix.blend_type = 'MIX'
mix.inputs['Fac'].default_value = 0.5
mix.inputs['Color1'].default_value = (1, 0, 0, 1)
mix.inputs['Color2'].default_value = (0, 1, 0, 1)

# NEW (4.0+) — USE THIS
mix = nodes.new('ShaderNodeMix')
mix.data_type = 'RGBA'       # 'FLOAT', 'RGBA', 'VECTOR'
mix.blend_type = 'MIX'       # Same blend types available
mix.inputs[0].default_value = 0.5       # Factor
# For RGBA mode: A=input[6], B=input[7]
mix.inputs[6].default_value = (1, 0, 0, 1)  # Color A
mix.inputs[7].default_value = (0, 1, 0, 1)  # Color B
```

### ShaderNodeTexMusgrave → ShaderNodeTexNoise

```python
# OLD (3.x / 4.0) — DEPRECATED in 4.1
musgrave = nodes.new('ShaderNodeTexMusgrave')
musgrave.musgrave_type = 'FBM'

# NEW (4.1+) — USE THIS
noise = nodes.new('ShaderNodeTexNoise')
noise.noise_type = 'FBM'     # or 'MULTIFRACTAL', 'HYBRID_MULTIFRACTAL', etc.
noise.inputs['Lacunarity'].default_value = 2.0
noise.inputs['Roughness'].default_value = 0.5  # Replaces Dimension
```

## 7. Node Output/Input Name Quick Reference

### Commonly Used Output Names

| Node Type | Output Name | Type |
|-----------|-------------|------|
| Noise Texture | `Fac` | Float |
| Noise Texture | `Color` | Color |
| Voronoi Texture | `Distance` | Float |
| Voronoi Texture | `Color` | Color |
| Voronoi Texture | `Position` | Vector |
| Wave Texture | `Color` | Color |
| Wave Texture | `Fac` | Float |
| ColorRamp | `Color` | Color |
| ColorRamp | `Alpha` | Float |
| Map Range | `Result` | Float |
| Math | `Value` | Float |
| Bump | `Normal` | Vector |
| Normal Map | `Normal` | Vector |
| Texture Coordinate | `Object` | Vector |
| Texture Coordinate | `Generated` | Vector |
| Texture Coordinate | `UV` | Vector |
| Mapping | `Vector` | Vector |
| Principled BSDF | `BSDF` | Shader |
| Mix | `Result` | Varies |

### Commonly Used Input Names

| Node Type | Input Name | Type |
|-----------|------------|------|
| Any Texture | `Vector` | Vector |
| Any Texture | `Scale` | Float |
| Principled BSDF | `Base Color` | Color |
| Principled BSDF | `Roughness` | Float |
| Principled BSDF | `Metallic` | Float |
| Principled BSDF | `Normal` | Vector |
| Bump | `Height` | Float |
| Bump | `Normal` | Vector (chain input) |
| Bump | `Strength` | Float |
| Bump | `Distance` | Float |
| Map Range | `Value` | Float |
| Map Range | `From Min` | Float |
| Map Range | `From Max` | Float |
| Map Range | `To Min` | Float |
| Map Range | `To Max` | Float |
| ColorRamp | `Fac` | Float |
| Material Output | `Surface` | Shader |
| Material Output | `Displacement` | Vector |
