---
last_updated: 2026-04-14
confidence: high
sources: 6
---

# Geometry Nodes Guide

Procedural geometry creation via Geometry Nodes modifier. Can be created via Python using node trees
and the Geometry Nodes modifier.

## Creating a Geometry Nodes Modifier

Create a new object with a Geometry Nodes modifier:
```python
import bpy

# Create a mesh object
mesh = bpy.data.meshes.new("ProceduralMesh")
obj = bpy.data.objects.new("ProceduralObject", mesh)
bpy.context.collection.objects.link(obj)

# Create Geometry Nodes modifier
mod = obj.modifiers.new(name="GeometryNodes", type='NODES')

# Create a new node tree
node_tree = bpy.data.node_groups.new("MyGeoTree", 'GeometryNodeTree')

# Link node tree to modifier
mod.node_group = node_tree
```

## Basic Node Tree Setup

Create input and output sockets:
```python
# Clear default nodes
node_tree.nodes.clear()
node_tree.links.clear()

# Create input node (Group Input)
input_node = node_tree.nodes.new(type='NodeGroupInput')
input_node.location = (0, 0)

# Create output node (Group Output)
output_node = node_tree.nodes.new(type='NodeGroupOutput')
output_node.location = (500, 0)

# Add custom inputs/outputs if needed
node_tree.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
node_tree.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
```

## Common Geometry Nodes

Create a primitive cube:
```python
cube_node = node_tree.nodes.new(type='GeometryNodeMeshCube')
cube_node.location = (100, 0)
cube_node.inputs['Size'].default_value = 2.0
```

Create a UV sphere:
```python
sphere_node = node_tree.nodes.new(type='GeometryNodeMeshUVSphere')
sphere_node.location = (100, -200)
sphere_node.inputs['Radius'].default_value = 1.5
sphere_node.inputs['Segments'].default_value = 32
sphere_node.inputs['Rings'].default_value = 16
```

Create a line:
```python
line_node = node_tree.nodes.new(type='GeometryNodeCurveLine')
line_node.location = (100, -400)
line_node.inputs['Start'].default_value = (0, 0, 0)
line_node.inputs['End'].default_value = (5, 0, 0)
line_node.inputs['Resolution'].default_value = 10
```

## Distribute Points on Faces

Common pattern: scatter points on a surface:
```python
# Distribute Points on Faces node
scatter_node = node_tree.nodes.new(type='GeometryNodeDistributePointsOnFaces')
scatter_node.location = (300, 0)
scatter_node.inputs['Density'].default_value = 10.0
scatter_node.inputs['Distance Min'].default_value = 0.1

# Link cube geometry to scatter
node_tree.links.new(cube_node.outputs['Mesh'], scatter_node.inputs['Mesh'])
```

## Instance on Points

Create instances at point locations:
```python
# Instance on Points node
instance_node = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')
instance_node.location = (500, 0)

# Use a sphere as instance
sphere_obj = bpy.data.objects['Sphere']

# Link scatter points to instance node
node_tree.links.new(scatter_node.outputs['Points'], instance_node.inputs['Points'])

# For object instance, create Object Info node
obj_info_node = node_tree.nodes.new(type='GeometryNodeObjectInfo')
obj_info_node.inputs['Object'].default_value = sphere_obj
node_tree.links.new(obj_info_node.outputs['Geometry'], instance_node.inputs['Instance'])

# Link to output
node_tree.links.new(instance_node.outputs['Instances'], output_node.inputs['Geometry'])
```

## Math Nodes for Procedural Control

Random value node:
```python
random_node = node_tree.nodes.new(type='FunctionNodeRandomValue')
random_node.location = (200, 200)
random_node.inputs['Min'].default_value = 0.5
random_node.inputs['Max'].default_value = 2.0
```

Math node (add, multiply, etc):
```python
math_node = node_tree.nodes.new(type='ShaderNodeMath')
math_node.location = (300, 150)
math_node.operation = 'MULTIPLY'
math_node.inputs[1].default_value = 2.0  # Multiply by 2
```

## Attribute Capture Pattern

Capture and reuse vertex attributes:
```python
# Capture Attribute node
capture_node = node_tree.nodes.new(type='GeometryNodeCaptureAttribute')
capture_node.location = (400, 100)
capture_node.data_type = 'FLOAT'
capture_node.inputs['Value'].default_value = 1.0

# Link input geometry
node_tree.links.new(input_node.outputs['Geometry'], capture_node.inputs['Geometry'])

# Use captured attribute later
attr_statistic = node_tree.nodes.new(type='GeometryNodeAttributeStatistic')
attr_statistic.location = (500, 100)
attr_statistic.data_type = 'FLOAT'
attr_statistic.inputs['Attribute'].default_value = capture_node.outputs['Attribute'].name
```

## Complete Scatter + Instance Example

```python
import bpy

# Create object with modifier
mesh = bpy.data.meshes.new("Scattered")
obj = bpy.data.objects.new("ScatteredObject", mesh)
bpy.context.collection.objects.link(obj)

mod = obj.modifiers.new(name="GeometryNodes", type='NODES')
node_tree = bpy.data.node_groups.new("ScatterTree", 'GeometryNodeTree')
mod.node_group = node_tree

# Clear and setup
node_tree.nodes.clear()
node_tree.links.clear()

input_node = node_tree.nodes.new(type='NodeGroupInput')
output_node = node_tree.nodes.new(type='NodeGroupOutput')

# Create base mesh (plane)
plane_node = node_tree.nodes.new(type='GeometryNodeMeshPlane')
plane_node.inputs['Size X'].default_value = 10.0
plane_node.inputs['Size Y'].default_value = 10.0

# Scatter points on plane
scatter = node_tree.nodes.new(type='GeometryNodeDistributePointsOnFaces')
scatter.inputs['Density'].default_value = 50.0

# Create small spheres at each point
sphere_node = node_tree.nodes.new(type='GeometryNodeMeshUVSphere')
sphere_node.inputs['Radius'].default_value = 0.2
sphere_node.inputs['Segments'].default_value = 8

# Instance spheres
instance = node_tree.nodes.new(type='GeometryNodeInstanceOnPoints')

# Create object info for sphere
obj_info = node_tree.nodes.new(type='GeometryNodeObjectInfo')
obj_info.inputs['Object'].default_value = bpy.data.objects.get('Sphere')

# Connect nodes
node_tree.links.new(plane_node.outputs['Mesh'], scatter.inputs['Mesh'])
node_tree.links.new(scatter.outputs['Points'], instance.inputs['Points'])
node_tree.links.new(obj_info.outputs['Geometry'], instance.inputs['Instance'])
node_tree.links.new(instance.outputs['Instances'], output_node.inputs['Geometry'])
```

## Node Types Quick Reference

| Node | Type String |
|------|-------------|
| Mesh Cube | `GeometryNodeMeshCube` |
| Mesh UV Sphere | `GeometryNodeMeshUVSphere` |
| Mesh Line | `GeometryNodeMeshLine` |
| Mesh Circle | `GeometryNodeMeshCircle` |
| Distribute Points on Faces | `GeometryNodeDistributePointsOnFaces` |
| Instance on Points | `GeometryNodeInstanceOnPoints` |
| Geometry to Instance | `GeometryNodeGeometryToInstance` |
| Capture Attribute | `GeometryNodeCaptureAttribute` |
| Object Info | `GeometryNodeObjectInfo` |
| Bounding Box | `GeometryNodeBoundBox` |
| Boolean | `GeometryNodeBoolean` |
| Scale | `GeometryNodeScale` |
| Transform | `GeometryNodeTransform` |
| Random Value | `FunctionNodeRandomValue` |
| Math | `ShaderNodeMath` |

## Linking Nodes

Basic node connection:
```python
# Get output socket and input socket
output_socket = source_node.outputs['Output Name']
input_socket = target_node.inputs['Input Name']

# Create link
link = node_tree.links.new(output_socket, input_socket)
```

## Debugging Geometry Nodes

Viewer node (shows geometry in viewport):
```python
viewer = node_tree.nodes.new(type='GeometryNodeViewer')
viewer.location = (600, 0)
viewer.inputs['Geometry'].default_value = instance.outputs['Instances']
```

## Common Pitfalls

**Don't:** Forget to add input/output sockets to node tree
```python
# BAD - nodes can't connect
node_tree = bpy.data.node_groups.new("Tree", 'GeometryNodeTree')
```

**Do:** Create proper interface
```python
# GOOD
node_tree.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
node_tree.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
```

**Don't:** Try to modify node_tree.inputs/outputs directly
```python
# OLD - doesn't work in newer Blender
node_tree.inputs.new(...)
```

**Do:** Use node_tree.interface
```python
# NEW - correct way
node_tree.interface.new_socket(...)
```

## Sources

- [CG Wire Blender Geometry Nodes Scripting Guide](https://blog.cg-wire.com/blender-scripting-geometry-nodes-2/)
- [Geonodes Python Library](https://github.com/al1brn/geonodes)
- [Geometry Script Python API](https://github.com/carson-katri/geometry-script)
- [PyNodes Blender Library](https://github.com/iplai/pynodes)
- [Blender Developer: Geometry Nodes Design](https://developer.blender.org/T74967)
