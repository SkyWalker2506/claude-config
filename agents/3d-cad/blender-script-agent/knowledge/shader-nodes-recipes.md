---
last_updated: 2026-04-14
confidence: high
sources: 7
---

# Shader Nodes Recipes

PBR material creation using Blender's Principled BSDF shader and common node patterns.
Each recipe is copy-paste ready for creating specific material types.

## Basic Material Setup

Create a new material with Principled BSDF:
```python
import bpy

# Create material
mat = bpy.data.materials.new("MyMaterial")
mat.use_nodes = True

# Clear default nodes
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

# Create Principled BSDF
bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Create output node
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
output.location = (300, 0)

# Link BSDF to output
mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

Assign material to object:
```python
obj = bpy.context.active_object
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
```

## Principled BSDF Properties (PBR Metallic-Roughness)

The core PBR workflow uses these inputs:
```python
bsdf = material.node_tree.nodes['Principled BSDF']

# Base color (diffuse/albedo)
bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.1, 1.0)  # RGBA

# Metallic (0 = dielectric, 1 = metal)
bsdf.inputs['Metallic'].default_value = 0.8

# Roughness (0 = mirror, 1 = rough)
bsdf.inputs['Roughness'].default_value = 0.3

# Subsurface scattering (for skin, wax)
bsdf.inputs['Subsurface Weight'].default_value = 0.1
bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.8, 0.6)  # RGB radius

# Coat weight (clearcoat layer)
bsdf.inputs['Coat Weight'].default_value = 0.5

# Normal map influence
bsdf.inputs['Normal Map'].default_value = (0.5, 0.5, 1.0)  # Unused in this case
```

## Load Image Texture

Load and connect an image texture:
```python
# Create Image Texture node
img_node = mat.node_tree.nodes.new(type='ShaderNodeTexImage')
img_node.location = (-300, 0)

# Load image
img = bpy.data.images.load("/path/to/texture.png")
img_node.image = img

# Get Principled BSDF node
bsdf = mat.node_tree.nodes['Principled BSDF']

# Connect image to Base Color
mat.node_tree.links.new(
    img_node.outputs['Color'],
    bsdf.inputs['Base Color']
)
```

## Procedural Noise Texture

Create a procedural base color using noise:
```python
# Create Noise Texture
noise_node = mat.node_tree.nodes.new(type='ShaderNodeTexNoise')
noise_node.location = (-300, 0)
noise_node.inputs['Scale'].default_value = 5.0
noise_node.inputs['Detail'].default_value = 2.0
noise_node.inputs['Roughness'].default_value = 0.5

# Connect to Color Ramp to control contrast
color_ramp = mat.node_tree.nodes.new(type='ShaderNodeValRamp')
color_ramp.location = (-100, 0)

# Use different interpolation for effect
color_ramp.color_ramp.interpolation = 'LINEAR'

# Connect noise to color ramp
mat.node_tree.links.new(
    noise_node.outputs['Fac'],
    color_ramp.inputs['Fac']
)

# Connect color ramp to principled
mat.node_tree.links.new(
    color_ramp.outputs['Color'],
    bsdf.inputs['Base Color']
)
```

## Voronoi Texture

Create a cellular/cracked pattern:
```python
# Voronoi texture
voronoi = mat.node_tree.nodes.new(type='ShaderNodeTexVoronoi')
voronoi.location = (-300, 0)
voronoi.inputs['Scale'].default_value = 15.0
voronoi.feature = 'DISTANCE_TO_EDGE'  # or 'CELLS', 'N_NEIGHBORS'

# Connect to roughness for variation
bsdf = mat.node_tree.nodes['Principled BSDF']
mat.node_tree.links.new(
    voronoi.outputs['Distance'],
    bsdf.inputs['Roughness']
)
```

## Metal Material Recipe

Shiny metal with microfacet roughness:
```python
mat = bpy.data.materials.new("Metal")
mat.use_nodes = True
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')

# Metal settings
bsdf.inputs['Base Color'].default_value = (0.95, 0.93, 0.88, 1.0)  # Aluminum
bsdf.inputs['Metallic'].default_value = 1.0  # Pure metal
bsdf.inputs['Roughness'].default_value = 0.2  # Slightly brushed

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

## Wood Material Recipe

Wood with directional grain:
```python
mat = bpy.data.materials.new("Wood")
mat.use_nodes = True
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')

# Create wood color from noise
noise = mat.node_tree.nodes.new(type='ShaderNodeTexNoise')
noise.location = (-300, 0)
noise.inputs['Scale'].default_value = 8.0

# Color ramp to create wood tones
ramp = mat.node_tree.nodes.new(type='ShaderNodeValRamp')
ramp.location = (-100, 0)
ramp.color_ramp.elements[0].color = (0.3, 0.15, 0.08, 1.0)  # Dark brown
ramp.color_ramp.elements[1].color = (0.6, 0.4, 0.2, 1.0)    # Light brown

# Wood material properties
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.4

# Connect
mat.node_tree.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
mat.node_tree.links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

## Skin Material Recipe

Realistic skin with subsurface scattering:
```python
mat = bpy.data.materials.new("Skin")
mat.use_nodes = True
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')

# Skin color (peachy)
bsdf.inputs['Base Color'].default_value = (0.95, 0.8, 0.75, 1.0)

# Subsurface scattering (light penetration)
bsdf.inputs['Subsurface Weight'].default_value = 0.5
bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.7, 0.5)  # Red channel strongest

# Slight metallic for wet skin
bsdf.inputs['Metallic'].default_value = 0.1

# Smooth but not shiny
bsdf.inputs['Roughness'].default_value = 0.3

# Add spec from Fresnel
bsdf.inputs['Coat Weight'].default_value = 0.2

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

## Glass Material Recipe

Transparent glass with IOR:
```python
mat = bpy.data.materials.new("Glass")
mat.use_nodes = True
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')

# Glass properties
bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # White

# Transmission (transparency)
bsdf.inputs['Transmission'].default_value = 1.0  # Full transparency

# IOR (Index of Refraction)
bsdf.inputs['IOR'].default_value = 1.45  # Glass

# Slight roughness for frosted glass effect
bsdf.inputs['Roughness'].default_value = 0.0  # Clear glass, increase for frosted

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

## Fabric Material Recipe

Soft cloth with subsurface:
```python
mat = bpy.data.materials.new("Fabric")
mat.use_nodes = True
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')

# Base color
bsdf.inputs['Base Color'].default_value = (0.5, 0.2, 0.2, 1.0)  # Red fabric

# Fabric is non-metallic
bsdf.inputs['Metallic'].default_value = 0.0

# Softer and slightly translucent
bsdf.inputs['Roughness'].default_value = 0.5
bsdf.inputs['Subsurface Weight'].default_value = 0.15

mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

## Stone Material Recipe

Rough rock/stone surface:
```python
mat = bpy.data.materials.new("Stone")
mat.use_nodes = True
mat.node_tree.nodes.clear()
mat.node_tree.links.clear()

bsdf = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')

# Create stone color variation
noise = mat.node_tree.nodes.new(type='ShaderNodeTexNoise')
noise.location = (-300, 0)
noise.inputs['Scale'].default_value = 5.0

color_ramp = mat.node_tree.nodes.new(type='ShaderNodeValRamp')
color_ramp.location = (-100, 0)
color_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)  # Dark gray
color_ramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0)  # Light gray

# Stone properties
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.7  # Very rough

# Connect
mat.node_tree.links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
mat.node_tree.links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
```

## Node Types Quick Reference

| Node | Type String |
|------|-------------|
| Principled BSDF | `ShaderNodeBsdfPrincipled` |
| Diffuse BSDF | `ShaderNodeBsdfDiffuse` |
| Glossy BSDF | `ShaderNodeBsdfGlossy` |
| Glass BSDF | `ShaderNodeBsdfGlass` |
| Transmission BSDF | `ShaderNodeBsdfTransparent` |
| Image Texture | `ShaderNodeTexImage` |
| Noise Texture | `ShaderNodeTexNoise` |
| Voronoi Texture | `ShaderNodeTexVoronoi` |
| Wave Texture | `ShaderNodeTexWave` |
| Musgrave Texture | `ShaderNodeTexMusgrave` |
| Color Ramp | `ShaderNodeValRamp` |
| Mix Shader | `ShaderNodeMix` |
| Output Material | `ShaderNodeOutputMaterial` |
| Normal Map | `ShaderNodeNormalMap` |
| Bump Map | `ShaderNodeBump` |

## Mix Multiple Materials

Blend two materials with a factor:
```python
# Create two materials first (mat1, mat2)
# Then in a third material:

bsdf1 = mat1.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf2 = mat2.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')

# Mix shader node
mix = mat.node_tree.nodes.new(type='ShaderNodeMix')
mix.data_type = 'SHADER'
mix.location = (100, 0)

# Factor controls blend (0 = mat1, 1 = mat2)
mix.inputs['Factor'].default_value = 0.5

output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
mat.node_tree.links.new(bsdf1.outputs['BSDF'], mix.inputs['A'])
mat.node_tree.links.new(bsdf2.outputs['BSDF'], mix.inputs['B'])
mat.node_tree.links.new(mix.outputs['Result'], output.inputs['Surface'])
```

## Sources

- [Blender Python API: ShaderNodeBsdfPrincipled](https://docs.blender.org/api/current/bpy.types.ShaderNodeBsdfPrincipled.html)
- [Blender Manual: Principled BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)
- [PBR and the Principled BSDF in Blender](https://artisticrender.com/physically-based-rendering-and-blender-materials/)
- [PBRify: PBR Material Generator](https://github.com/RaghavVenkat/pbrify)
- [Blender PBR Addon](https://github.com/DigiKrafting/blender_addon_pbr)
