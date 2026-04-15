---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html
  - https://docs.blender.org/api/current/bpy.types.DisplaceModifier.html
  - https://docs.blender.org/api/current/bpy.types.MultiresModifier.html
  - https://docs.blender.org/api/current/bpy.types.MusgraveTexture.html
  - https://docs.blender.org/api/current/bpy.types.Texture.html
  - https://en.fmyly.com/article/what-replaced-the-musgrave-texture-in-blender/
  - https://artisticrender.com/how-to-use-displacement-in-blender/
  - https://artisticrender.com/how-to-use-vertex-groups-in-blender/
---

# Displacement Techniques for Character Sculpting

## 1. Blender Displacement Modifier — Complete Reference

### 1.1 Core Properties

| Property | Type | Default | Range | Description |
|----------|------|---------|-------|-------------|
| `direction` | enum | `'NORMAL'` | X, Y, Z, NORMAL, CUSTOM_NORMAL, RGB_TO_XYZ | Displacement direction |
| `mid_level` | float | `0.5` | 0.0 - 1.0 | Texture value treated as zero displacement |
| `strength` | float | `1.0` | -inf to +inf | Multiplier for final displacement |
| `texture` | Texture | None | — | The texture driving displacement |
| `texture_coords` | enum | `'LOCAL'` | LOCAL, GLOBAL, OBJECT, UV | Coordinate system for texture sampling |
| `texture_coords_object` | Object | None | — | Object to use for OBJECT coordinates |
| `texture_coords_bone` | str | `""` | — | Bone name for bone coordinates |
| `vertex_group` | str | `""` | — | Vertex group to limit displacement area |
| `invert_vertex_group` | bool | False | — | Invert vertex group influence |
| `space` | enum | `'LOCAL'` | LOCAL, GLOBAL | Coordinate space for displacement |

### 1.2 Direction Modes Explained

| Mode | Use Case | Character Sculpting Application |
|------|----------|-------------------------------|
| `NORMAL` | Most common; pushes along vertex normal | Muscle bulges, skin pores, wrinkles |
| `X/Y/Z` | Axis-aligned displacement | Rarely used for organic; good for hair cards |
| `RGB_TO_XYZ` | Vector displacement maps | Professional sculpt detail transfer |
| `CUSTOM_NORMAL` | Uses custom normals | Specialized normal-map based displacement |

### 1.3 Mid-Level Strategy

The `mid_level` value determines the zero-displacement threshold:
- **0.5 (default)**: Texture values below 0.5 push inward, above 0.5 push outward. Balanced displacement.
- **0.0**: All texture values push outward. Use for adding volume only (muscle bumps).
- **1.0**: All texture values push inward. Use for creating cavities only (wrinkle lines).
- **0.55-0.65**: Bias toward outward displacement. Good for organic forms that should mostly bulge out with some subtle valleys.

### 1.4 Strength Guidelines for Characters

| Application | Strength Range | Notes |
|------------|---------------|-------|
| Primary muscle forms | 0.08 - 0.20 | Large, visible displacement |
| Secondary muscle detail | 0.03 - 0.08 | Moderate, refining detail |
| Bone landmarks | 0.03 - 0.06 | Subtle but sharp |
| Skin wrinkles | 0.02 - 0.04 | Fine lines |
| Skin pores | 0.01 - 0.02 | Nearly invisible, adds micro-detail |
| Scars/damage | 0.03 - 0.08 | Varies with scar depth |
| Veins | 0.02 - 0.04 | Thin, raised lines |
| Creature warts/bumps | 0.04 - 0.10 | Pronounced organic bumps |
| Rocky/stony skin | 0.10 - 0.25 | Heavy displacement for trolls, golems |

## 2. Procedural Textures for Organic Detail

### 2.1 Musgrave Texture — Muscle Definition

The Musgrave texture generates fractal Perlin noise. It is the primary tool for organic muscle and skin displacement.

#### Musgrave Types

| Type | Character | Best Use |
|------|-----------|----------|
| `FBM` | Smooth, homogenous fractal | General muscle undulation, soft organic forms |
| `MULTIFRACTAL` | Uneven, varied | Weathered skin, aged creature texture |
| `RIDGED_MULTIFRACTAL` | Sharp peaks and valleys | Wrinkle lines, scar tissue, tendon ridges |
| `HYBRID_MULTIFRACTAL` | Mix of smooth and sharp | Leathery skin, mixed organic texture |
| `HETERO_TERRAIN` | Terrain-like variation | Rocky/stony creature skin |

#### Musgrave Properties

| Property | Type | Range | Default | Notes |
|----------|------|-------|---------|-------|
| `musgrave_type` | enum | see above | `'MULTIFRACTAL'` | Noise algorithm |
| `noise_scale` | float | 0.0001 - 100 | 0.25 | Controls pattern size; lower = larger patterns |
| `dimension_max` | float | 0.0001 - 2.0 | 1.0 | Fractal dimension; higher = more detail between octaves |
| `lacunarity` | float | 0.0 - 6.0 | 2.0 | Gap between successive octave frequencies |
| `octaves` | float | 0.0 - 8.0 | 2.0 | Number of noise layers; more = more detail |
| `offset` | float | 0.0 - 6.0 | 1.0 | Offset for Ridged/Hybrid types |
| `gain` | float | 0.0 - 6.0 | 1.0 | Gain for Hybrid/Hetero types |
| `noise_intensity` | float | 0.0 - 10.0 | 1.0 | Overall intensity multiplier |
| `noise_basis` | enum | various | `'BLENDER_ORIGINAL'` | Base noise algorithm |

#### Musgrave Recipes for Character Sculpting

**Recipe 1: General Muscle Definition**
```python
tex = bpy.data.textures.new('MuscleForm', type='MUSGRAVE')
tex.musgrave_type = 'FBM'
tex.noise_scale = 3.0          # Scale 2-5: muscle-sized undulations
tex.dimension_max = 1.2        # Moderate detail between octaves
tex.lacunarity = 2.0           # Standard frequency gap
tex.octaves = 4.0              # Enough detail without noise
tex.noise_intensity = 1.0
# Displacement: strength=0.10-0.15, mid_level=0.5
```

**Recipe 2: Wrinkle Lines**
```python
tex = bpy.data.textures.new('WrinkleLines', type='MUSGRAVE')
tex.musgrave_type = 'RIDGED_MULTIFRACTAL'
tex.noise_scale = 10.0         # Scale 8-15: fine line detail
tex.dimension_max = 0.5        # Low dimension = sharper features
tex.lacunarity = 3.0           # Higher frequency separation
tex.octaves = 6.0              # High octaves for sharp lines
tex.offset = 1.0
tex.noise_intensity = 1.0
# Displacement: strength=0.02-0.04, mid_level=0.5
```

**Recipe 3: Aged/Weathered Skin**
```python
tex = bpy.data.textures.new('AgedSkin', type='MUSGRAVE')
tex.musgrave_type = 'HYBRID_MULTIFRACTAL'
tex.noise_scale = 6.0          # Scale 4-8: mixed detail
tex.dimension_max = 0.8        # Moderate sharpness
tex.lacunarity = 2.5
tex.octaves = 5.0
tex.offset = 0.8
tex.gain = 1.2
# Displacement: strength=0.05-0.10, mid_level=0.5
```

**Recipe 4: Goblin/Creature Warty Skin**
```python
tex = bpy.data.textures.new('WartySkin', type='MUSGRAVE')
tex.musgrave_type = 'RIDGED_MULTIFRACTAL'
tex.noise_scale = 4.0          # Scale 3-6: prominent bumps
tex.dimension_max = 1.0
tex.lacunarity = 2.5
tex.octaves = 5.0
tex.offset = 1.2
# Displacement: strength=0.06-0.12, mid_level=0.5
```

### 2.2 Voronoi Texture — Skin Pores & Cell Patterns

Voronoi generates cell-like patterns. Excellent for skin pores, scales, and cracked surfaces.

#### Voronoi Properties

| Property | Type | Range | Default | Notes |
|----------|------|-------|---------|-------|
| `distance_metric` | enum | see below | `'DISTANCE'` | How cell distance is calculated |
| `noise_scale` | float | 0.0001 - 100 | 0.25 | Pattern scale; higher = finer |
| `noise_intensity` | float | 0.0 - 10.0 | 1.0 | Output intensity |
| `color_source` | enum | POSITION, CELL | `'CELL'` | What drives the output |

#### Distance Metrics

| Metric | Result | Best Use |
|--------|--------|----------|
| `DISTANCE` | Smooth cell boundaries | Skin pores, organic cells |
| `DISTANCE_SQUARED` | Sharper cell edges | Scales, armor plates |
| `MANHATTAN` | Grid-like cells | Tiled patterns |
| `CHEBYCHEV` | Square-ish cells | Block-like patterns |
| `MINKOVSKY_HALF` | Rounded cells | Soft organic patterns |
| `MINKOVSKY_FOUR` | Sharp-edged cells | Crystal-like patterns |
| `MINKOVSKY` | Adjustable sharpness | Versatile |

#### Voronoi Recipes

**Recipe 1: Skin Pores**
```python
tex = bpy.data.textures.new('SkinPores', type='VORONOI')
tex.noise_scale = 80.0         # Scale 50-100: very fine for pores
tex.distance_metric = 'DISTANCE'
tex.color_source = 'CELL'
tex.noise_intensity = 1.0
# Displacement: strength=0.01-0.02, mid_level=0.5
```

**Recipe 2: Reptile/Dragon Scales**
```python
tex = bpy.data.textures.new('DragonScales', type='VORONOI')
tex.noise_scale = 15.0         # Scale 10-25: visible scale pattern
tex.distance_metric = 'DISTANCE_SQUARED'
tex.color_source = 'CELL'
tex.noise_intensity = 1.2
# Displacement: strength=0.04-0.08, mid_level=0.4 (mostly raised)
```

**Recipe 3: Cracked Stone (Troll/Golem)**
```python
tex = bpy.data.textures.new('CrackedStone', type='VORONOI')
tex.noise_scale = 8.0          # Scale 5-12: visible crack pattern
tex.distance_metric = 'DISTANCE'
tex.color_source = 'POSITION'
tex.noise_intensity = 1.5
# Displacement: strength=0.08-0.15, mid_level=0.6 (valleys dominant)
```

**Recipe 4: Wart Bumps**
```python
tex = bpy.data.textures.new('WartBumps', type='VORONOI')
tex.noise_scale = 15.0         # Scale 10-20: scattered bumps
tex.distance_metric = 'MINKOVSKY_HALF'
tex.color_source = 'CELL'
tex.noise_intensity = 1.0
# Displacement: strength=0.03-0.06, mid_level=0.6
```

### 2.3 Noise Texture — General Surface Variation

The basic Noise texture adds randomized surface variation. Use it as a final layer to break up uniformity.

```python
tex = bpy.data.textures.new('SurfaceVariation', type='NOISE')
# Noise has minimal settings — it's purely random
# Displacement: strength=0.005-0.01, mid_level=0.5
```

### 2.4 Clouds Texture — Organic Blotching

Clouds generate soft, organic blobs. Good for subtle anatomical variation and fat distribution patterns.

```python
tex = bpy.data.textures.new('OrganicBlotch', type='CLOUDS')
tex.noise_scale = 4.0          # Scale 3-8: body-scale variation
tex.noise_depth = 3             # Depth 2-5: complexity
tex.noise_type = 'SOFT_NOISE'  # SOFT_NOISE or HARD_NOISE
tex.noise_basis = 'BLENDER_ORIGINAL'
# Displacement: strength=0.03-0.08, mid_level=0.5
```

### 2.5 Distorted Noise — Veins & Tendons

Distorted noise creates elongated, flowing patterns. Excellent for veins and tendon lines.

```python
tex = bpy.data.textures.new('VeinPattern', type='DISTORTED_NOISE')
tex.noise_scale = 4.0          # Scale 3-6: vein-sized
tex.distortion = 2.0           # Distortion 1.5-3.0: more = more twisted
tex.noise_distortion = 'IMPROVED_PERLIN'
tex.noise_basis = 'IMPROVED_PERLIN'
# Displacement: strength=0.02-0.04, mid_level=0.45 (slight raise)
```

## 3. Texture Masking with Vertex Groups

Vertex groups allow you to limit displacement to specific body areas, enabling different textures for different regions.

### 3.1 Creating Vertex Groups Programmatically

```python
# Conceptual — E2 implements
def create_region_vertex_groups(mesh_obj):
    """Create vertex groups for body region masking."""
    regions = {
        'torso_front': [],
        'torso_back': [],
        'arms': [],
        'legs': [],
        'head': [],
        'hands': [],
        'feet': [],
    }
    
    mesh = mesh_obj.data
    
    for name in regions:
        if name not in mesh_obj.vertex_groups:
            mesh_obj.vertex_groups.new(name=name)
    
    # Assign vertices based on position
    # (Simplified — real implementation uses spatial queries)
    for v in mesh.vertices:
        x, y, z = v.co
        weight = 0.0
        
        # Head: above z=0.40 (normalized)
        if z > 0.40:
            vg = mesh_obj.vertex_groups['head']
            vg.add([v.index], 1.0, 'REPLACE')
        
        # Torso front: z between 0.05-0.40, y > 0
        elif 0.05 < z < 0.40 and abs(x) < 0.12 and y > 0:
            vg = mesh_obj.vertex_groups['torso_front']
            vg.add([v.index], 1.0, 'REPLACE')
        
        # ... similar for other regions
    
    return mesh_obj
```

### 3.2 Assigning Vertex Group to Displacement

```python
def mask_displacement_to_region(mesh_obj, modifier_name, group_name, invert=False):
    """Limit a displacement modifier to a vertex group region."""
    mod = mesh_obj.modifiers[modifier_name]
    mod.vertex_group = group_name
    mod.invert_vertex_group = invert
```

### 3.3 Gradient Texture Masking

Use a gradient texture mapped to an object coordinate to create smooth transitions between displacement regions.

```python
def create_gradient_mask(mesh_obj, axis='Z', blend_type='LINEAR'):
    """Create a gradient-based displacement mask."""
    # Create gradient texture
    tex_grad = bpy.data.textures.new('GradientMask', type='BLEND')
    tex_grad.progression = blend_type  # LINEAR, QUADRATIC, EASING, etc.
    
    # Create empty object for coordinate control
    empty = bpy.data.objects.new('GradientControl', None)
    bpy.context.collection.objects.link(empty)
    empty.empty_display_type = 'ARROWS'
    
    # Set up displacement with gradient
    mod = mesh_obj.modifiers.new('GradientDisplace', type='DISPLACE')
    mod.texture = tex_grad
    mod.texture_coords = 'OBJECT'
    mod.texture_coords_object = empty
    mod.strength = 0.1
    
    return mod, empty
```

### 3.4 Common Masking Patterns

| Pattern | Technique | Use Case |
|---------|-----------|----------|
| Upper body only | Z-gradient + vertex group | Orc musculature emphasis |
| Face wrinkles | Vertex group for face | Age lines on forehead, around eyes |
| Joint creases | Vertex groups at elbows/knees | Skin fold detail at joints |
| Scar area | Painted vertex group | Localized scar displacement |
| Fade at edges | Gradient texture + Object coords | Smooth transition between regions |

## 4. Multiresolution Modifier — Complete Reference

### 4.1 Properties

| Property | Type | Range | Notes |
|----------|------|-------|-------|
| `levels` | int | 0-255 | Viewport subdivision level |
| `sculpt_levels` | int | 0-255 | Sculpt mode subdivision level |
| `render_levels` | int | 0-255 | Render subdivision level |
| `total_levels` | int | readonly | Total subdivisions stored |
| `subdivision_type` | enum | CATMULL_CLARK, SIMPLE | Subdivision algorithm |
| `quality` | int | 1-10 | Quality of render normals |
| `show_only_control_edges` | bool | — | Display optimization |
| `use_creases` | bool | — | Use edge creases from base mesh |

### 4.2 When to Use Multiresolution vs SubSurf

| Scenario | Use Multires | Use SubSurf |
|----------|-------------|-------------|
| Sculpting detail at multiple levels | Yes | No |
| Smooth subdivision only | No | Yes |
| Need to bake displacement map | Yes | No |
| Need to go back to lower detail | Yes | No |
| Simple mesh smoothing | No | Yes |
| Game-ready LOD generation | Yes | No |

### 4.3 Level Recommendations by Character Type

| Character Type | Sculpt Level | Viewport Level | Render Level | Base Verts |
|---------------|-------------|---------------|-------------|------------|
| Game character (mobile) | 2-3 | 1-2 | 2-3 | 1,000-3,000 |
| Game character (PC) | 3-4 | 2-3 | 3-4 | 3,000-8,000 |
| Cinematic character | 4-6 | 2-3 | 5-6 | 5,000-15,000 |
| Hero close-up | 5-7 | 2-3 | 6-7 | 8,000-20,000 |

### 4.4 Multiresolution Code Patterns

```python
# Conceptual — E2 implements

def add_multiresolution(mesh_obj, subdivisions=3, mode='CATMULL_CLARK'):
    """Add and subdivide a multiresolution modifier."""
    # Ensure object is active
    bpy.context.view_layer.objects.active = mesh_obj
    mesh_obj.select_set(True)
    
    # Add modifier
    mod = mesh_obj.modifiers.new('Multires', type='MULTIRES')
    
    # Subdivide
    for i in range(subdivisions):
        bpy.ops.object.multires_subdivide(
            modifier=mod.name,
            mode=mode  # 'CATMULL_CLARK' or 'SIMPLE'
        )
    
    # Set levels
    mod.sculpt_levels = subdivisions
    mod.levels = max(1, subdivisions - 1)  # Viewport 1 less for performance
    mod.render_levels = subdivisions
    
    return mod


def reshape_multires_base(mesh_obj, modifier_name):
    """Reshape base mesh to match current sculpt state."""
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.multires_reshape(modifier=modifier_name)


def bake_displacement_from_multires(mesh_obj, modifier_name):
    """Bake multires sculpt data to displacement map."""
    bpy.context.view_layer.objects.active = mesh_obj
    # Requires proper UV map
    bpy.ops.object.bake(type='DISPLACEMENT')
```

## 5. Complete Displacement Pipeline — Putting It All Together

### 5.1 Full Character Displacement Stack

```python
# Conceptual — E2 implements the complete pipeline
def build_full_displacement_stack(mesh_obj, character_type='human'):
    """
    Build the complete displacement modifier stack for a character.
    Call AFTER metaball conversion and cleanup.
    """
    
    # === Layer 1: Subdivision Base ===
    sub = mesh_obj.modifiers.new('SubBase', type='SUBSURF')
    sub.levels = 1
    sub.render_levels = 2
    sub.subdivision_type = 'CATMULL_CLARK'
    
    # === Layer 2: Primary Muscle Forms ===
    tex_muscle = bpy.data.textures.new(f'{character_type}_Muscle', type='MUSGRAVE')
    tex_muscle.musgrave_type = 'FBM'
    tex_muscle.noise_scale = 3.0
    tex_muscle.dimension_max = 1.2
    tex_muscle.lacunarity = 2.0
    tex_muscle.octaves = 4.0
    
    mod_muscle = mesh_obj.modifiers.new('L2_Muscle', type='DISPLACE')
    mod_muscle.texture = tex_muscle
    mod_muscle.strength = 0.12
    mod_muscle.mid_level = 0.5
    mod_muscle.direction = 'NORMAL'
    mod_muscle.texture_coords = 'LOCAL'
    
    # === Layer 3: Bone Landmarks ===
    tex_bone = bpy.data.textures.new(f'{character_type}_Bone', type='MUSGRAVE')
    tex_bone.musgrave_type = 'RIDGED_MULTIFRACTAL'
    tex_bone.noise_scale = 5.0
    tex_bone.dimension_max = 0.8
    tex_bone.lacunarity = 2.5
    tex_bone.octaves = 4.0
    
    mod_bone = mesh_obj.modifiers.new('L3_Bone', type='DISPLACE')
    mod_bone.texture = tex_bone
    mod_bone.strength = 0.06
    mod_bone.mid_level = 0.55
    mod_bone.direction = 'NORMAL'
    mod_bone.texture_coords = 'LOCAL'
    
    # === Layer 4: Multiresolution Sculpt Surface ===
    multires = mesh_obj.modifiers.new('L4_Multires', type='MULTIRES')
    bpy.context.view_layer.objects.active = mesh_obj
    for i in range(3):
        bpy.ops.object.multires_subdivide(
            modifier=multires.name,
            mode='CATMULL_CLARK'
        )
    multires.sculpt_levels = 3
    multires.levels = 2
    multires.render_levels = 3
    
    # === Layer 5: Secondary Muscle Detail ===
    tex_sec = bpy.data.textures.new(f'{character_type}_SecMuscle', type='MUSGRAVE')
    tex_sec.musgrave_type = 'MULTIFRACTAL'
    tex_sec.noise_scale = 6.0
    tex_sec.dimension_max = 0.9
    tex_sec.lacunarity = 2.2
    tex_sec.octaves = 5.0
    
    mod_sec = mesh_obj.modifiers.new('L5_Secondary', type='DISPLACE')
    mod_sec.texture = tex_sec
    mod_sec.strength = 0.05
    mod_sec.mid_level = 0.5
    mod_sec.direction = 'NORMAL'
    
    # === Layer 6: Skin Pores ===
    tex_pore = bpy.data.textures.new(f'{character_type}_Pores', type='VORONOI')
    tex_pore.noise_scale = 80.0
    tex_pore.distance_metric = 'DISTANCE'
    
    mod_pore = mesh_obj.modifiers.new('L6_Pores', type='DISPLACE')
    mod_pore.texture = tex_pore
    mod_pore.strength = 0.015
    mod_pore.mid_level = 0.5
    mod_pore.direction = 'NORMAL'
    
    # === Layer 7: Wrinkles ===
    tex_wrinkle = bpy.data.textures.new(f'{character_type}_Wrinkle', type='MUSGRAVE')
    tex_wrinkle.musgrave_type = 'RIDGED_MULTIFRACTAL'
    tex_wrinkle.noise_scale = 12.0
    tex_wrinkle.dimension_max = 0.5
    tex_wrinkle.lacunarity = 3.0
    tex_wrinkle.octaves = 6.0
    
    mod_wrinkle = mesh_obj.modifiers.new('L7_Wrinkle', type='DISPLACE')
    mod_wrinkle.texture = tex_wrinkle
    mod_wrinkle.strength = 0.025
    mod_wrinkle.mid_level = 0.5
    mod_wrinkle.direction = 'NORMAL'
    
    # === Layer 8: Surface Noise ===
    tex_noise = bpy.data.textures.new(f'{character_type}_Noise', type='NOISE')
    
    mod_noise = mesh_obj.modifiers.new('L8_SurfNoise', type='DISPLACE')
    mod_noise.texture = tex_noise
    mod_noise.strength = 0.008
    mod_noise.mid_level = 0.5
    mod_noise.direction = 'NORMAL'
    
    return mesh_obj
```

### 5.2 Creature-Specific Displacement Adjustments

| Creature | Muscle Strength | Skin Type | Extra Layer | Notes |
|----------|---------------|-----------|-------------|-------|
| Human | 0.12 | Smooth pores | — | Baseline settings |
| Goblin | 0.06 | Warty (Voronoi 15) | Ridged wrinkles | Less muscle, more skin texture |
| Orc | 0.18 | Leathery (FBM 5) | Heavy muscle | More muscle displacement |
| Elf | 0.08 | Smooth (pores only) | — | Minimal displacement, clean forms |
| Dwarf | 0.15 | Weathered (Hybrid 6) | Calluses | Dense muscle, work-worn skin |
| Troll | 0.22 | Rocky (Voronoi crackle 8) | Stone plates | Maximum displacement |
| Dragon | 0.14 | Scales (Voronoi squared 15) | Ridge plates | Scale pattern dominant |
