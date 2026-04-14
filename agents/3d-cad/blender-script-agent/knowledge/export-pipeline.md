---
last_updated: 2026-04-14
confidence: high
sources: 6
---

# Export Pipeline

Batch and single-object export patterns for glTF 2.0, FBX, and OBJ formats.
Includes common pitfalls and how to fix them.

## glTF 2.0 Export (Recommended for Game Engines)

Export a single object as glTF 2.0:
```python
import bpy
import os

obj = bpy.context.active_object
filepath = "/path/to/export/model.glb"

# Select only this object
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Export as GLB (embedded)
bpy.ops.export_scene.gltf(
    filepath=filepath,
    check_existing=True,
    export_format='GLB',  # GLB = binary, GLTF_SEPARATE = separate files
    use_selection=True,
    use_visible=False,
    use_renderable=False,
    mesh_type='MESH',
    export_materials=True,
    export_colors=True,
    export_normals=True,
    export_draco_mesh_compression_level=0,
    export_image_format='AUTO',
)

print(f"Exported to {filepath}")
```

Export multiple objects as glTF:
```python
import bpy

objects_to_export = [bpy.data.objects['Object1'], bpy.data.objects['Object2']]
output_dir = "/path/to/exports"

for obj in objects_to_export:
    # Select only this object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Create filename from object name
    filepath = f"{output_dir}/{obj.name}.glb"
    
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        check_existing=True,
        export_format='GLB',
        use_selection=True,
        export_materials=True,
        export_colors=True,
    )
    
    print(f"Exported {obj.name}")
```

## glTF Export Parameters

Common glTF export settings:
```python
bpy.ops.export_scene.gltf(
    filepath="model.glb",
    
    # Format: GLB (binary), GLTF_SEPARATE (files), GLTF_EMBEDDED
    export_format='GLB',
    
    # Selection options
    use_selection=True,        # Only export selected objects
    use_visible=False,         # Export only visible objects
    use_renderable=False,      # Include non-renderable objects
    
    # Geometry options
    export_apply_modifiers=True,
    export_animations=True,
    export_deformation_bones_only=False,
    
    # Material options
    export_materials=True,
    export_colors=True,        # Vertex colors
    export_normals=True,
    export_image_format='AUTO',  # AUTO, JPEG, PNG
    
    # Draco compression (reduces file size)
    export_draco_mesh_compression_level=7,  # 0-7, higher = smaller but slower
    
    # Extra options
    export_tangents=True,
    export_extras=True,
    export_yup=False,  # True for Y-up, False for Z-up
)
```

## FBX Export

Export as FBX (good for game engines and Unreal):
```python
import bpy

obj = bpy.context.active_object
filepath = "/path/to/export/model.fbx"

# Select object
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bpy.ops.export_scene.fbx(
    filepath=filepath,
    check_existing=True,
    
    # Selection
    use_selection=True,
    use_visible=False,
    use_active_collection=False,
    
    # Scale (important: Blender uses different units)
    global_scale=1.0,  # Change to 100 if scale is wrong in engine
    
    # Rotation axis (Z-up vs Y-up)
    axis_forward='-Y',  # -Y, -X, Y, X
    axis_up='Z',        # Z, Y
    
    # What to export
    object_types={'MESH', 'ARMATURE', 'EMPTY', 'LIGHT', 'CAMERA'},
    
    # Mesh options
    use_mesh_modifiers=True,
    use_deform_bones=True,
    
    # Animation
    bake_anim=True,
    bake_anim_use_nla_strips=True,
    bake_anim_use_all_actions=False,
    bake_anim_force_startend_keying=False,
    bake_anim_step=1,
    bake_anim_simplify_factor=1.0,
    
    # Materials
    use_materials=True,
    
    # Smoothing
    use_smooth_groups=False,
    use_smooth_groups_bitflags=False,
    group_by_material=False,
    use_tspace=False,
    
    # Embedding
    use_embed_textures=True,  # Embed images in FBX
    
    # Batch mode
    batch_mode='OFF',
)

print(f"Exported to {filepath}")
```

## OBJ Export

Export as OBJ (basic 3D format, no animation):
```python
import bpy

obj = bpy.context.active_object
filepath = "/path/to/export/model.obj"

# Select object
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bpy.ops.export_scene.obj(
    filepath=filepath,
    check_existing=True,
    
    # Selection
    use_selection=True,
    use_visible=False,
    use_animation=False,  # OBJ doesn't support animation well
    
    # Scale
    global_scale=1.0,
    
    # Rotation
    axis_forward='-Y',
    axis_up='Z',
    
    # Geometry
    use_mesh_modifiers=True,
    use_nurbs=False,
    
    # MTL file
    use_materials=True,
    use_uvs=True,
    use_normals=True,
    
    # Baking
    use_triangles=False,  # Triangulate faces
    use_edge_groups=False,
    use_smooth_groups=False,
    use_smooth_groups_bitflags=False,
    use_object_groups=False,
    use_blen_objects=False,
    group_by_material=False,
    keep_edge_order=False,
    use_vertex_groups=False,
    use_vertex_groups_groups=False,
)

print(f"Exported to {filepath}")
```

## Batch Export Script

Export all objects in a collection to individual files:
```python
import bpy
import os
from pathlib import Path

def batch_export_glb(collection_name, output_dir, format='GLB'):
    """Export all objects in a collection to separate GLB files."""
    
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"Collection '{collection_name}' not found")
        return
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    
    # Export each object
    for obj in collection.objects:
        if obj.type == 'MESH':
            # Select only this object
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # Create filename
            filename = f"{obj.name}.glb"
            filepath = os.path.join(output_dir, filename)
            
            try:
                bpy.ops.export_scene.gltf(
                    filepath=filepath,
                    check_existing=True,
                    export_format='GLB',
                    use_selection=True,
                    export_materials=True,
                    export_colors=True,
                )
                print(f"Exported: {filename}")
            except Exception as e:
                print(f"Error exporting {filename}: {e}")
            
            # Deselect for next iteration
            obj.select_set(False)

# Usage
batch_export_glb("Assets", "/path/to/exports")
```

## Batch Export with Scale Fix

Common issue: Model is 100x too large or 100x too small in target engine:
```python
import bpy

def export_with_scale(obj, filepath, scale_factor=1.0, format='FBX'):
    """Export object with scale adjustment."""
    
    # Save original scale
    original_scale = obj.scale.copy()
    
    try:
        # Apply scale
        obj.scale = (scale_factor, scale_factor, scale_factor)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Apply transform
        bpy.ops.object.transform_apply(scale=True)
        
        # Export
        if format == 'FBX':
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                use_selection=True,
                global_scale=1.0,  # Already applied above
                axis_forward='-Y',
                axis_up='Z',
            )
        elif format == 'GLB':
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                use_selection=True,
                export_format='GLB',
            )
        
        print(f"Exported with scale {scale_factor}x")
        
    finally:
        # Restore original scale
        obj.scale = original_scale
        bpy.ops.object.transform_apply(scale=True)

# Usage: export with 100x scale to fix tiny model
export_with_scale(bpy.context.active_object, "model.fbx", scale_factor=100.0, format='FBX')
```

## Common Pitfalls & Fixes

### Pitfall 1: Model is 100x too large in engine

**Cause:** Blender uses cm, engines use m. Or scale wasn't applied.

**Fix:**
```python
obj = bpy.context.active_object

# Option 1: Apply scale before export
bpy.ops.object.transform_apply(scale=True)
# Then export normally

# Option 2: Use global_scale in FBX
bpy.ops.export_scene.fbx(
    filepath="model.fbx",
    use_selection=True,
    global_scale=0.01,  # Scale down by 100x
    axis_forward='-Y',
    axis_up='Z',
)

# Option 3: Use scale_factor with custom function (see above)
```

### Pitfall 2: Axis is wrong (model rotated in engine)

**Cause:** Different axis conventions (Blender uses Z-up, some engines use Y-up)

**Fix:**
```python
# Check which axis your engine uses
# Unity/Unreal: Y-up, Z-forward
# Standard glTF: Y-up, Z-backward

# For Y-up engine:
bpy.ops.export_scene.fbx(
    filepath="model.fbx",
    axis_forward='-Y',  # Points back
    axis_up='Z',        # Points up
)

# Alternatively, rotate object 90 degrees before export:
import math
obj.rotation_euler = (math.radians(90), 0, 0)
bpy.ops.object.transform_apply(rotation=True)
```

### Pitfall 3: Textures not exported

**Cause:** Textures aren't embedded or image paths are broken

**Fix:**
```python
# For FBX, embed textures
bpy.ops.export_scene.fbx(
    filepath="model.fbx",
    use_materials=True,
    use_embed_textures=True,  # Embed images in FBX
)

# For glTF, images are separate by default
bpy.ops.export_scene.gltf(
    filepath="model.glb",
    export_format='GLB',  # GLB embeds everything
    export_materials=True,
    export_image_format='AUTO',
)
```

### Pitfall 4: Modifiers not applied

**Cause:** Modifiers are non-destructive; export doesn't apply them automatically

**Fix:**
```python
obj = bpy.context.active_object

# Apply all modifiers before export
for mod in obj.modifiers[:]:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)

# Or use export_apply_modifiers (glTF)
bpy.ops.export_scene.gltf(
    filepath="model.glb",
    use_selection=True,
    export_apply_modifiers=True,
)

# Or use use_mesh_modifiers (FBX)
bpy.ops.export_scene.fbx(
    filepath="model.fbx",
    use_selection=True,
    use_mesh_modifiers=True,
)
```

## Export Settings Comparison

| Feature | glTF | FBX | OBJ |
|---------|------|-----|-----|
| Animation | Yes | Yes | No |
| Materials | Yes (PBR) | Yes | Basic (MTL) |
| Textures | Separate or embedded | Embedded | Separate |
| Compression | Draco | None | None |
| File size | Small | Medium | Large |
| Game engines | Unity, Godot | Unreal, Unity | All |
| Rigging | Yes | Yes | Limited |

## Quick Reference

| Task | Command |
|------|---------|
| Export single as glTF | `bpy.ops.export_scene.gltf(filepath, use_selection=True)` |
| Export single as FBX | `bpy.ops.export_scene.fbx(filepath, use_selection=True)` |
| Fix scale (100x) | `global_scale=0.01` in FBX or apply scale transform |
| Fix axis (Z-up) | `axis_forward='-Y', axis_up='Z'` in FBX |
| Embed textures | `use_embed_textures=True` in FBX or `export_format='GLB'` in glTF |
| Apply modifiers | `export_apply_modifiers=True` in glTF or use `bpy.ops.object.modifier_apply()` |

## Sources

- [Blender Python API: Export Scene Operators](https://docs.blender.org/api/current/bpy.ops.export_scene.html)
- [Blender Batch Export Guide](https://robertshenton.co.za/blog/blender-batch-export/)
- [glTF Tutorials: Blender glTF Converter](https://github.khronos.org/glTF-Tutorials/BlenderGltfConverter/)
- [Blender Artists: Batch Export](https://blenderartists.org/t/batch-export-for-different-formats-using-bpy-ops-export-scene/1219994)
