---
last_updated: 2026-04-14
confidence: high
sources: 8
---

# Bpy API Patterns

Core Blender Python patterns for object creation, selection, deletion, mode switching, collection management,
mesh data access, and operator usage.

## Object Creation & Linking

Create a new mesh object and link it to the scene:
```python
import bpy

# Create mesh data-block
mesh = bpy.data.meshes.new("MyMesh")

# Create object with mesh data
obj = bpy.data.objects.new("MyObject", mesh)

# Link object to active collection
bpy.context.collection.objects.link(obj)

# Make it active and select it
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
```

Create a light object:
```python
light_data = bpy.data.lights.new("MyLight", type='SUN')
light_obj = bpy.data.objects.new("MyLightObject", light_data)
bpy.context.collection.objects.link(light_obj)
bpy.context.view_layer.objects.active = light_obj
```

## Object Selection & Deletion

Select all objects:
```python
for obj in bpy.data.objects:
    obj.select_set(True)
```

Select one object and make it active:
```python
target_obj = bpy.data.objects["ObjectName"]
bpy.context.view_layer.objects.active = target_obj
target_obj.select_set(True)
```

Deselect all:
```python
bpy.ops.object.select_all(action='DESELECT')
```

Delete selected objects (Blender 3.2+):
```python
bpy.ops.object.delete(use_global=False, confirm=False)
```

Delete specific objects using context override (recommended):
```python
with bpy.context.temp_override(selected_objects=[obj_to_delete]):
    bpy.ops.object.delete()
```

## Mode Switching

Switch to Edit Mode:
```python
bpy.ops.object.mode_set(mode='EDIT')
```

Switch to Object Mode:
```python
bpy.ops.object.mode_set(mode='OBJECT')
```

Switch to Sculpt Mode:
```python
bpy.ops.object.mode_set(mode='SCULPT')
```

Switch with context override (more reliable):
```python
with bpy.context.temp_override(object=my_obj):
    bpy.ops.object.mode_set(mode='EDIT')
```

## Context Overrides (Blender 3.2+)

Override context to create objects in a specific window:
```python
# Add cube to a different window
win = bpy.context.window_manager.windows[1]
with bpy.context.temp_override(window=win):
    bpy.ops.mesh.primitive_cube_add()
```

Override active object:
```python
with bpy.context.temp_override(active_object=target_obj):
    bpy.ops.object.mode_set(mode='EDIT')
```

Multiple context overrides:
```python
with bpy.context.temp_override(
    object=obj,
    active_object=obj,
    selected_objects=[obj]
):
    bpy.ops.mesh.select_all(action='SELECT')
```

## Collection Management

Create a new collection:
```python
collection = bpy.data.collections.new("MyCollection")
bpy.context.scene.collection.children.link(collection)
```

Add object to specific collection:
```python
obj = bpy.data.objects["ObjectName"]
# Remove from current collections
for coll in obj.users_collection:
    coll.objects.unlink(obj)
# Add to new collection
new_coll = bpy.data.collections["MyCollection"]
new_coll.objects.link(obj)
```

Move object to collection:
```python
def move_object_to_collection(obj, collection):
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    collection.objects.link(obj)
```

## Mesh Data Access

Access mesh geometry:
```python
obj = bpy.context.active_object
mesh = obj.data

# Iterate vertices
for vert in mesh.vertices:
    print(vert.co)  # Vector position
    print(vert.normal)  # Normal direction

# Iterate edges
for edge in mesh.edges:
    print(edge.vertices)  # (v1_idx, v2_idx)

# Iterate faces
for face in mesh.polygons:
    print(face.vertices)  # Tuple of vertex indices
    print(face.normal)  # Face normal
    print(face.area)  # Face area
    print(face.center)  # Face centroid

# Iterate loops (corner attributes)
for loop in mesh.loops:
    print(loop.vertex_index)
    print(loop.normal)
```

Transform mesh vertices:
```python
for vert in mesh.vertices:
    vert.co.x += 0.1
    vert.co.y *= 0.8

# Recalculate derived data
mesh.update()
```

Add vertex group:
```python
vgroup = mesh.vertex_groups.new(name="MyGroup")
vgroup.add([0, 1, 2], 1.0, 'REPLACE')  # Add verts 0,1,2 with weight 1.0
```

## Modifier Stack Management

Add a modifier:
```python
obj = bpy.context.active_object
mod = obj.modifiers.new(name="SubSurf", type='SUBSURF')
mod.levels = 2
mod.render_levels = 3
```

Add multiple common modifiers:
```python
# Subdivision Surface
subsurf = obj.modifiers.new("SubSurf", 'SUBSURF')
subsurf.levels = 2

# Smooth Shading + Smooth modifier
smooth = obj.modifiers.new("Smooth", 'SMOOTH')
smooth.factor = 1.0
smooth.iterations = 2

# Bevel
bevel = obj.modifiers.new("Bevel", 'BEVEL')
bevel.width = 0.01
bevel.segments = 3

# Remesh
remesh = obj.modifiers.new("Remesh", 'REMESH')
remesh.voxel_size = 0.05
```

Apply a modifier:
```python
bpy.context.view_layer.objects.active = obj
bpy.ops.object.modifier_apply(modifier=mod.name)
```

Remove a modifier:
```python
obj.modifiers.remove(mod)
```

Apply all modifiers:
```python
for mod in obj.modifiers[:]:  # Copy list to avoid iteration issues
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
```

## Keyframe Insertion

Set location keyframe:
```python
obj.location = (1.0, 2.0, 3.0)
obj.keyframe_insert(data_path="location", frame=10)
```

Set rotation keyframe (Euler):
```python
obj.rotation_euler = (0.1, 0.2, 0.3)
obj.keyframe_insert(data_path="rotation_euler", frame=20)
```

Set scale keyframe:
```python
obj.scale = (1.5, 1.5, 1.5)
obj.keyframe_insert(data_path="scale", frame=30)
```

Set custom property keyframe:
```python
obj["custom_prop"] = 0.5
obj.keyframe_insert(data_path='["custom_prop"]', frame=5)
```

## Operator Patterns

Common mesh operators:
```python
# Select all in Edit Mode
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.select_all(action='DESELECT')

# Delete selection (in Edit Mode)
bpy.ops.mesh.delete(type='VERT')  # type: VERT, EDGE, FACE, EDGE_FACE, ONLY_FACE

# Extrude (in Edit Mode)
bpy.ops.mesh.extrude_region()
bpy.ops.transform.translate(value=(0, 0, 0.5))

# Subdivide (in Edit Mode)
bpy.ops.mesh.subdivide(number=2)

# Shade smooth
bpy.ops.object.shade_smooth()

# Shade flat
bpy.ops.object.shade_flat()
```

Object operators:
```python
# Duplicate object
bpy.ops.object.duplicate()

# Join objects
bpy.ops.object.join()

# Apply transforms
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
```

## Anti-Patterns

**Don't:** Use deprecated `obj.select = True` (Blender 2.7x)
```python
# OLD - DON'T USE
obj.select = True  # Deprecated in Blender 2.8+
```

**Do:** Use `obj.select_set(True)` (Blender 2.8+)
```python
# NEW - USE THIS
obj.select_set(True)
```

**Don't:** Iterate mesh while modifying
```python
# BAD - modifying while iterating
for vert in mesh.vertices:
    if vert.co.z < 0:
        # ... add or remove something
```

**Do:** Copy and iterate separately
```python
# GOOD - copy list first
verts_to_delete = [v for v in mesh.vertices if v.co.z < 0]
for vert in verts_to_delete:
    # ... now safe to modify
```

**Don't:** Forget to refresh lookups after geometry changes
```python
# BAD - will crash
for face in bm.faces:
    bmesh.ops.extrude_face_region(bm, geom=[face])
    # Now faces list is stale!
```

**Do:** Call ensure_lookup_table()
```python
# GOOD - refresh after changes
bmesh.ops.extrude_face_region(bm, geom=[face])
bm.faces.ensure_lookup_table()
for face in bm.faces:
    # Now safe to use
```

## Quick Reference

| Task | Function |
|------|----------|
| Create mesh object | `bpy.data.meshes.new()` + `bpy.data.objects.new()` |
| Select object | `obj.select_set(True)` |
| Make active | `bpy.context.view_layer.objects.active = obj` |
| Delete object | `bpy.ops.object.delete()` |
| Enter Edit Mode | `bpy.ops.object.mode_set(mode='EDIT')` |
| Add modifier | `obj.modifiers.new(name, type)` |
| Access vertices | `obj.data.vertices` |
| Access faces | `obj.data.polygons` |
| Update mesh | `mesh.update()` |
| Insert keyframe | `obj.keyframe_insert(data_path, frame)` |

## Sources

- [Blender Python API: Object](https://docs.blender.org/api/current/bpy.types.Object.html)
- [Blender Python API: Operators](https://docs.blender.org/api/current/bpy.ops.html)
- [Blender Python API: Context Access](https://docs.blender.org/api/current/bpy.context.html)
- [Context Overriding in Blender 3.2+](https://b3d.interplanety.org/en/context-overriding-in-blender-3-2-and-later/)
- [Blender Python API: Export Scene Operators](https://docs.blender.org/api/current/bpy.ops.export_scene.html)
