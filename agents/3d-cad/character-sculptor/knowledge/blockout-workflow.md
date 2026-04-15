---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/manual/en/latest/modeling/metas/index.html
  - https://artisticrender.com/how-to-use-metaballs-in-blender/
  - https://cgian.com/blender-metaball-to-mesh/
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html
  - https://docs.blender.org/api/current/bpy.types.MetaBall.html
  - https://docs.blender.org/api/current/bpy.types.MetaElement.html
  - https://docs.blender.org/api/current/bpy.types.DisplaceModifier.html
  - https://docs.blender.org/api/current/bpy.types.MultiresModifier.html
---

# Blockout Workflow for Character Sculpting

## Overview

The blockout workflow is a 4-phase process that progressively builds detail from coarse volumes to fine surface detail. Each phase has specific goals, tools, and quality gates.

```
Phase 1: Silhouette    → Metaballs (major volumes only)
Phase 2: Primary Forms  → Displacement (large muscle groups, bone landmarks)
Phase 3: Secondary Forms → Multiresolution + Displacement (individual muscles, tendons)
Phase 4: Tertiary Detail → Fine displacement + sculpt (wrinkles, pores, scars)
```

## Phase 1: Silhouette Blocking (Metaballs)

### Goal
Establish the character's overall shape so it reads correctly as a silhouette from all 4 cardinal directions (front, side, back, 3/4).

### What to Block
- **Head**: Overall cranium volume + jaw
- **Torso**: Chest, abdomen, pelvis as 2-3 large volumes
- **Limbs**: Each arm segment, each leg segment as single elements
- **Distinguishing features**: Ears (goblin), tusks (orc), tail (dragon)

### What NOT to Do
- Do NOT add individual muscles
- Do NOT worry about topology
- Do NOT add surface detail
- Do NOT add fingers/toes (simple paddle shapes for hands/feet)

### Blender Metaball Settings

| Parameter | Value | Reason |
|-----------|-------|--------|
| `resolution` | 0.10-0.20 | Lower = smoother but slower; 0.15 is good balance |
| `render_resolution` | 0.05 | Higher quality for final evaluation |
| `threshold` | 0.5-0.8 | Controls how aggressively elements merge; higher = tighter |

### Element Guidelines

| Body Part | Element Count | Radius Range | Stiffness |
|-----------|--------------|-------------|-----------|
| Head | 2-4 | 0.04-0.07 | 1.5-2.0 |
| Neck | 1 | 0.02-0.03 | 1.5 |
| Torso | 3-5 | 0.04-0.07 | 1.8-2.0 |
| Upper arm | 1-2 | 0.02-0.04 | 1.5 |
| Forearm | 1-2 | 0.015-0.03 | 1.5 |
| Hand | 1 | 0.015-0.025 | 1.2-1.5 |
| Thigh | 1-2 | 0.03-0.05 | 1.8 |
| Shin | 1-2 | 0.02-0.03 | 1.5 |
| Foot | 1-2 | 0.015-0.025 | 1.2-1.5 |

### Stiffness Guide
- **1.0**: Very soft merge; elements blend heavily into neighbors
- **1.5**: Medium merge; elements maintain some individuality
- **2.0**: Firm; elements stay more distinct
- **3.0+**: Very firm; nearly separate unless very close

### Quality Gate: Silhouette Test
Before proceeding to Phase 2:
1. Render 4 views (front, right, back, 3/4) as solid black silhouettes
2. Character type must be recognizable from silhouette alone
3. No limbs merging into torso (adjust stiffness or positions)
4. Head-to-body ratio matches target head-count

### Phase 1 Code Pattern

```python
# Conceptual — E2 (Blender Script Agent) implements
import bpy
from mathutils import Vector

def phase1_metaball_blockout(character_type, elements_list, scale=1.0):
    """
    Phase 1: Create metaball blockout from element definitions.
    
    Args:
        character_type: str, e.g. 'goblin', 'orc', 'human'
        elements_list: list of (name, x, y, z, radius, stiffness) tuples
        scale: float, overall scale factor
    
    Returns:
        bpy.types.Object: The metaball object
    """
    mb = bpy.data.metaballs.new(f'{character_type}_blockout')
    obj = bpy.data.objects.new(f'{character_type}_BlockoutMB', mb)
    bpy.context.collection.objects.link(obj)
    
    # Metaball settings
    mb.resolution = 0.15
    mb.render_resolution = 0.05
    mb.threshold = 0.6
    
    for name, x, y, z, radius, stiffness in elements_list:
        elem = mb.elements.new()
        elem.co = Vector((x * scale, y * scale, z * scale))
        elem.radius = radius * scale
        elem.stiffness = stiffness
    
    return obj
```

## Phase 2: Primary Forms (Displacement)

### Goal
Add the large anatomical forms that give the character mass and structure: major muscle groups, ribcage suggestion, pelvis shape, bone landmarks.

### Prerequisites
1. Convert metaball to mesh: `Object > Convert > Mesh`
2. Clean up topology with Decimate if needed
3. Apply initial Smooth modifier to remove metaball artifacts

### Conversion Process

```python
# Conceptual — E2 implements
def phase2_convert_and_prepare(metaball_obj):
    """Convert metaball to mesh and prepare for displacement."""
    # Select the metaball object
    bpy.context.view_layer.objects.active = metaball_obj
    metaball_obj.select_set(True)
    
    # Convert to mesh
    bpy.ops.object.convert(target='MESH')
    mesh_obj = bpy.context.active_object
    mesh_obj.name = mesh_obj.name.replace('BlockoutMB', 'Mesh')
    
    # Step 1: Decimate to clean topology
    dec = mesh_obj.modifiers.new('CleanDecimate', type='DECIMATE')
    dec.ratio = 0.5  # Remove excess verts from metaball conversion
    bpy.ops.object.modifier_apply(modifier=dec.name)
    
    # Step 2: Smooth to remove artifacts
    smooth = mesh_obj.modifiers.new('ArtifactSmooth', type='SMOOTH')
    smooth.factor = 0.5
    smooth.iterations = 3
    bpy.ops.object.modifier_apply(modifier=smooth.name)
    
    # Step 3: Remesh for clean quad topology (optional but recommended)
    remesh = mesh_obj.modifiers.new('CleanRemesh', type='REMESH')
    remesh.mode = 'VOXEL'
    remesh.voxel_size = 0.01  # Adjust based on character scale
    remesh.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=remesh.name)
    
    return mesh_obj
```

### Primary Form Displacement

Add displacement modifiers with vertex group masks to target specific body areas.

```python
# Conceptual — E2 implements
def phase2_add_primary_forms(mesh_obj):
    """Add displacement for large muscle groups and bone landmarks."""
    
    # --- Muscle Definition (overall) ---
    tex_muscle = bpy.data.textures.new('PrimaryMuscle', type='MUSGRAVE')
    tex_muscle.musgrave_type = 'FBM'
    tex_muscle.noise_scale = 3.0      # Large-scale forms
    tex_muscle.dimension_max = 1.2
    tex_muscle.lacunarity = 2.0
    tex_muscle.octaves = 3.0          # Low octaves = broad shapes
    
    mod_muscle = mesh_obj.modifiers.new('PrimaryMuscle', type='DISPLACE')
    mod_muscle.texture = tex_muscle
    mod_muscle.strength = 0.12        # Moderate displacement
    mod_muscle.mid_level = 0.5
    mod_muscle.direction = 'NORMAL'
    mod_muscle.texture_coords = 'LOCAL'
    
    # --- Bone Landmarks (subtle) ---
    tex_bone = bpy.data.textures.new('BoneLandmarks', type='MUSGRAVE')
    tex_bone.musgrave_type = 'RIDGED_MULTIFRACTAL'
    tex_bone.noise_scale = 5.0        # Medium detail
    tex_bone.dimension_max = 0.8
    tex_bone.lacunarity = 2.5
    tex_bone.octaves = 4.0
    
    mod_bone = mesh_obj.modifiers.new('BoneLandmarks', type='DISPLACE')
    mod_bone.texture = tex_bone
    mod_bone.strength = 0.06          # Subtle
    mod_bone.mid_level = 0.55         # Slightly biased outward
    mod_bone.direction = 'NORMAL'
    mod_bone.texture_coords = 'LOCAL'
    
    return mesh_obj
```

### What to Add in Phase 2

| Form | Displacement Type | Strength | Target Area |
|------|------------------|----------|-------------|
| Pectoral mass | Musgrave FBM, scale=3 | 0.10-0.15 | Upper chest |
| Deltoid caps | Musgrave FBM, scale=2.5 | 0.08-0.12 | Shoulder tops |
| Trapezius slope | Musgrave FBM, scale=4 | 0.06-0.10 | Neck to shoulder |
| Latissimus taper | Musgrave FBM, scale=4 | 0.08-0.12 | Mid-back sides |
| Quadriceps mass | Musgrave FBM, scale=3 | 0.10-0.15 | Front thigh |
| Gluteus shape | Musgrave FBM, scale=3.5 | 0.08-0.12 | Buttocks |
| Clavicle ridge | Ridged Multi, scale=6 | 0.04-0.06 | Collarbone area |
| Scapula edge | Ridged Multi, scale=5 | 0.03-0.05 | Upper back |
| Iliac crest | Ridged Multi, scale=5 | 0.04-0.06 | Hip bones |

### Quality Gate: Form Check
- Major muscle groups create visible contour changes
- Bone landmarks (clavicle, scapula edge, iliac crest) are indicated
- Character still passes silhouette test
- No sharp artifacts or unnatural bumps

## Phase 3: Secondary Forms (Multiresolution + Displacement)

### Goal
Add individual muscles, tendons, fat pads, and refine bone landmark details.

### Modifier Stack at Phase 3

The correct modifier stack order is critical:

```
1. [Applied] Decimate        — already applied in Phase 2
2. [Applied] Smooth           — already applied in Phase 2
3. [Applied] Remesh           — already applied in Phase 2
4. [Live]    SubSurf (1-2)    — clean subdivision base
5. [Live]    Displace (primary) — Phase 2 muscle forms
6. [Live]    Displace (bone)   — Phase 2 bone landmarks
7. [Live]    Multires (2-3)    — Phase 3 sculpt surface
8. [Live]    Displace (secondary) — Phase 3 muscle detail
```

### Adding Multiresolution

```python
# Conceptual — E2 implements
def phase3_add_secondary_forms(mesh_obj):
    """Add multiresolution and secondary displacement."""
    
    # Subdivision base (must come before multires)
    sub = mesh_obj.modifiers.new('SubBase', type='SUBSURF')
    sub.levels = 1
    sub.render_levels = 2
    sub.subdivision_type = 'CATMULL_CLARK'
    
    # Multiresolution for sculpting
    multires = mesh_obj.modifiers.new('SculptDetail', type='MULTIRES')
    
    # Subdivide 3 times for secondary detail
    for i in range(3):
        bpy.ops.object.multires_subdivide(
            modifier=multires.name,
            mode='CATMULL_CLARK'
        )
    
    multires.sculpt_levels = 3
    multires.levels = 2          # Viewport efficiency
    multires.render_levels = 3
    
    # Secondary muscle displacement (finer detail)
    tex_secondary = bpy.data.textures.new('SecondaryMuscle', type='MUSGRAVE')
    tex_secondary.musgrave_type = 'MULTIFRACTAL'
    tex_secondary.noise_scale = 6.0     # Finer scale than Phase 2
    tex_secondary.dimension_max = 0.9
    tex_secondary.lacunarity = 2.2
    tex_secondary.octaves = 5.0
    
    mod_sec = mesh_obj.modifiers.new('SecondaryDetail', type='DISPLACE')
    mod_sec.texture = tex_secondary
    mod_sec.strength = 0.05             # Subtle refinement
    mod_sec.mid_level = 0.5
    mod_sec.direction = 'NORMAL'
    mod_sec.texture_coords = 'LOCAL'
    
    return mesh_obj
```

### What to Add in Phase 3

| Form | Detail Level | Technique | Notes |
|------|-------------|-----------|-------|
| Individual quad heads | Multires sculpt Lv2 | Smooth + inflate | Separate VMO, VL, RF, VI |
| Serratus fingers | Multires sculpt Lv2 | Crease brush equivalent | Interdigitating with obliques |
| Deltoid heads | Multires sculpt Lv2 | Separate anterior/lateral/posterior | 3-head separation |
| Achilles tendon | Multires sculpt Lv2 | Crease + smooth | Sharp vertical line at heel |
| Kneecap detail | Multires sculpt Lv2 | Inflate + crease | Define patella and surrounding fat pads |
| Elbow detail | Multires sculpt Lv2 | Crease | Olecranon and epicondyle bumps |
| Rib suggestion | Displacement mask | Ridged Musgrave, scale=8 | Subtle rib shadows on lean builds |
| Fat pads | Multires sculpt Lv1 | Smooth + inflate | Soften transitions at joints |

### Multiresolution Level Guide

| Level | Vertex Multiplier | Use For | When |
|-------|------------------|---------|------|
| 0 | 1x | Base mesh editing | Adjusting overall proportions |
| 1 | ~4x | Large form adjustments | Moving muscle masses |
| 2 | ~16x | Individual muscle shapes | Phase 3 main work |
| 3 | ~64x | Tendons, creases | Phase 3 refinement |
| 4 | ~256x | Wrinkles, veins | Phase 4 only |
| 5 | ~1024x | Pores, micro-detail | Phase 4, render only |

### Quality Gate: Anatomy Check
- Individual muscles identifiable in directional light
- Joints have proper landmark bumps (elbow, knee, wrist, ankle)
- Tendons visible at insertion points
- Fat pads soften hard transitions appropriately

## Phase 4: Tertiary Detail (Fine Displacement + Sculpt)

### Goal
Add surface micro-detail: skin texture, wrinkles, pores, scars, veins.

### Techniques

```python
# Conceptual — E2 implements
def phase4_add_tertiary_detail(mesh_obj):
    """Add fine surface detail for final quality."""
    
    # --- Skin Pores ---
    tex_pores = bpy.data.textures.new('SkinPores', type='VORONOI')
    tex_pores.noise_scale = 80.0      # Very fine scale
    tex_pores.distance_metric = 'DISTANCE'
    
    mod_pores = mesh_obj.modifiers.new('Pores', type='DISPLACE')
    mod_pores.texture = tex_pores
    mod_pores.strength = 0.015        # Very subtle
    mod_pores.mid_level = 0.5
    mod_pores.direction = 'NORMAL'
    
    # --- Wrinkle Lines ---
    tex_wrinkle = bpy.data.textures.new('Wrinkles', type='MUSGRAVE')
    tex_wrinkle.musgrave_type = 'RIDGED_MULTIFRACTAL'
    tex_wrinkle.noise_scale = 12.0    # Fine directional detail
    tex_wrinkle.dimension_max = 0.5
    tex_wrinkle.lacunarity = 3.0
    tex_wrinkle.octaves = 6.0
    
    mod_wrinkle = mesh_obj.modifiers.new('Wrinkles', type='DISPLACE')
    mod_wrinkle.texture = tex_wrinkle
    mod_wrinkle.strength = 0.025
    mod_wrinkle.mid_level = 0.5
    mod_wrinkle.direction = 'NORMAL'
    
    # --- General Surface Variation ---
    tex_noise = bpy.data.textures.new('SurfaceNoise', type='NOISE')
    
    mod_noise = mesh_obj.modifiers.new('SurfaceVar', type='DISPLACE')
    mod_noise.texture = tex_noise
    mod_noise.strength = 0.008        # Extremely subtle
    mod_noise.mid_level = 0.5
    mod_noise.direction = 'NORMAL'
    
    return mesh_obj
```

### Phase 4 Detail Types

| Detail | Texture | Scale | Strength | Vertex Group Mask |
|--------|---------|-------|----------|------------------|
| Skin pores | Voronoi F1 | 50-100 | 0.01-0.02 | All skin areas |
| Forehead wrinkles | Ridged Musgrave | 10-15 | 0.02-0.04 | Forehead group |
| Crow's feet | Ridged Musgrave | 8-12 | 0.02-0.03 | Eye corner group |
| Nasolabial folds | Ridged Musgrave | 6-10 | 0.03-0.05 | Mouth area group |
| Veins (forearm) | Distorted Noise | 3-5 | 0.02-0.03 | Forearm group |
| Scars | Voronoi Crackle | 5-15 | 0.03-0.06 | Specific area group |
| Calluses | Musgrave FBM | 20-30 | 0.02-0.04 | Hands/feet group |
| Stretch marks | Ridged Musgrave | 8-12 | 0.01-0.02 | Specific area |

### Quality Gate: Surface Quality
- Pores visible at close-up render distance
- Wrinkles follow natural skin tension lines
- No tiling artifacts in displacement textures
- Vertex count within game-ready budget (check target platform)
- All modifiers can be collapsed for export

## Complete Modifier Stack Order (All Phases)

```
Phase 1 (applied):
  [Applied] Metaball conversion
  
Phase 2 (applied during transition):
  [Applied] Decimate (ratio=0.5)
  [Applied] Smooth (factor=0.5, iter=3)
  [Applied] Remesh/Voxel (size=0.01)

Phase 2-4 (live modifiers, top to bottom):
  1. SubSurf          type=CATMULL_CLARK, levels=1, render=2
  2. PrimaryMuscle     type=DISPLACE, strength=0.12, Musgrave FBM scale=3
  3. BoneLandmarks     type=DISPLACE, strength=0.06, Ridged Multi scale=5
  4. SculptDetail      type=MULTIRES, sculpt=3, viewport=2, render=3
  5. SecondaryDetail   type=DISPLACE, strength=0.05, Multifractal scale=6
  6. Pores             type=DISPLACE, strength=0.015, Voronoi scale=80
  7. Wrinkles          type=DISPLACE, strength=0.025, Ridged Multi scale=12
  8. SurfaceVar        type=DISPLACE, strength=0.008, Noise
```

### Modifier Order Rules
1. SubSurf must come BEFORE Multires
2. Large-scale displacements come BEFORE fine-scale
3. Multires should be in the middle of the stack
4. Fine detail (pores, wrinkles) goes AFTER Multires
5. Smooth modifiers go at the beginning (applied early)

## Vertex Count Budget by Phase

| Phase | Approx Verts | Notes |
|-------|-------------|-------|
| Phase 1 (metaball) | 1,000-5,000 | Raw conversion, pre-decimate |
| Phase 2 (after cleanup) | 2,000-8,000 | Post-decimate + remesh |
| Phase 3 (with multires Lv3) | 50,000-200,000 | Sculpt resolution |
| Phase 4 (with multires Lv5) | 500,000-2,000,000 | Render only; bake for game |

### Game-Ready Export Target
- **Mobile**: 2,000-5,000 tris
- **Desktop/Console**: 10,000-50,000 tris
- **Cinematic**: 100,000+ tris
- Use Decimate or Retopology to hit targets after Phase 3-4 work
