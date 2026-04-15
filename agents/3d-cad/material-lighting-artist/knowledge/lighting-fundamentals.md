---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://docs.blender.org/manual/en/latest/render/lights/light_object.html
  - https://brandon3d.com/three-point-lighting-in-blender-3d/
  - https://mattepaint.com/blog/master-three-point-lighting-setup-in-blender/
  - https://www.gauravbhardwaj.in/blog/in-depth-walkthroughs-3d-2/how-to-set-up-pro-level-lighting-in-blender-a-step-by-step-guide-1
  - https://blog.yarsalabs.com/basics-of-lighting-setup-in-blender/
---

# Lighting Fundamentals — Material & Lighting Artist Knowledge

## 1. Three-Point Lighting

The foundation of all character and product lighting. Three lights working together
to reveal form, reduce harsh shadows, and create depth.

### Key Light (Main Light)
- **Purpose:** Primary illumination, defines the main shadow direction
- **Position:** Upper-left-front (45 degrees from camera, 45 degrees above)
- **Type:** AREA (soft, controllable shadows)
- **Energy:** Strongest light in the scene
- **Color:** Warm (simulates natural/studio light)
- **Shadow:** Primary shadow caster

### Fill Light
- **Purpose:** Softens shadows from key light, reveals detail in dark areas
- **Position:** Right side of camera, roughly same height or slightly lower
- **Type:** AREA (large, very soft)
- **Energy:** 30-40% of key light
- **Color:** Slightly cool (creates color contrast with warm key)
- **Shadow:** Soft or no shadow (large light size)

### Rim Light (Back Light)
- **Purpose:** Separates subject from background, defines silhouette
- **Position:** Behind and above subject, opposite side from key
- **Type:** AREA or SPOT
- **Energy:** 50-70% of key light
- **Color:** Neutral to cool white
- **Shadow:** Not visible to camera

## 2. Light Types in Blender

### Point Light
```python
bpy.ops.object.light_add(type='POINT')
light = bpy.context.active_object.data
light.energy = 100  # Watts
light.shadow_soft_size = 0.1  # meters — controls shadow softness
light.color = (1.0, 0.95, 0.85)
```
- **Emits:** In all directions from a single point
- **Use for:** Candles, light bulbs, small practical lights
- **Shadows:** Hard by default, softened by `shadow_soft_size`
- **NOT recommended for:** Main character lighting (hard to control)

### Sun Light
```python
bpy.ops.object.light_add(type='SUN')
light = bpy.context.active_object.data
light.energy = 3.0  # Irradiance (W/m^2), NOT Watts
light.angle = 0.00918  # Angular diameter in radians (default sun size)
light.color = (1.0, 0.95, 0.85)
```
- **Emits:** Parallel rays in one direction (infinite distance)
- **Use for:** Outdoor scenes, sunlight, moonlight
- **Shadows:** Parallel, uniform across scene
- **Position:** Only rotation matters, not location
- **Energy unit:** Irradiance (W/m^2), much lower numbers than other lights

### Spot Light
```python
bpy.ops.object.light_add(type='SPOT')
light = bpy.context.active_object.data
light.energy = 500     # Watts
light.spot_size = 0.785  # Cone angle in radians (~45 degrees)
light.spot_blend = 0.15  # Edge falloff (0=hard, 1=full soft)
light.shadow_soft_size = 0.1
light.color = (1.0, 1.0, 1.0)
```
- **Emits:** In a cone from a point
- **Use for:** Rim lights, theatrical effects, focused illumination
- **Shadows:** Can be very controlled
- **Good for:** Spotlighting specific areas, dramatic effects

### Area Light
```python
bpy.ops.object.light_add(type='AREA')
light = bpy.context.active_object.data
light.energy = 200     # Watts
light.shape = 'RECTANGLE'  # 'SQUARE', 'RECTANGLE', 'DISK', 'ELLIPSE'
light.size = 2.0       # Width in meters
light.size_y = 1.5     # Height (RECTANGLE/ELLIPSE only)
light.color = (1.0, 0.95, 0.85)
```
- **Emits:** From a flat surface (like a softbox)
- **Use for:** Key light, fill light — primary character lighting
- **Shadows:** Naturally soft (larger size = softer shadows)
- **RECOMMENDED for:** All character lighting setups
- **Shape recommendation:** RECTANGLE for most studio setups

## 3. Energy Values — Character Height Formula

### Base Formula

For a character at standard Blender scale (1 unit = 1 meter):

```
character_height = 1.8  # meters (average human)

# Key Light
key_energy = character_height * 200  # Range: 200-400 multiplier
# Result: 360-720W for human-sized character

# Fill Light
fill_energy = key_energy * 0.35  # Range: 0.3-0.4 of key
# Result: 108-252W

# Rim Light
rim_energy = key_energy * 0.6   # Range: 0.5-0.7 of key
# Result: 180-504W
```

### Scaling Table

| Character Height | Key Energy | Fill Energy | Rim Energy |
|-----------------|------------|-------------|------------|
| 0.3m (small creature) | 60-120W | 20-45W | 30-85W |
| 0.8m (child/goblin) | 160-320W | 50-120W | 80-225W |
| 1.0m (dwarf) | 200-400W | 60-150W | 100-280W |
| 1.5m (average female) | 300-600W | 90-225W | 150-420W |
| 1.8m (average male) | 360-720W | 108-270W | 180-504W |
| 2.5m (large orc) | 500-1000W | 150-375W | 250-700W |
| 4.0m (giant) | 800-1600W | 240-600W | 400-1120W |

### Distance Factor

Energy follows inverse-square law. If light is at distance D from subject:
- **Standard distance:** 2-3x character height
- If light is further, increase energy proportionally to distance^2
- If light is closer, decrease energy

```python
# Practical: place key light at 2x character height distance
distance = character_height * 2.0
# Adjust energy if distance differs from reference (2.0m for standard human)
energy_factor = (distance / 2.0) ** 2
adjusted_energy = base_energy * energy_factor
```

## 4. Color Temperature

### Warm/Cool Contrast

Professional lighting uses warm key + cool fill for visual depth:

```python
# Warm key light (simulates tungsten/sunset)
key_color = (1.0, 0.95, 0.85)      # Warm white
# OR more dramatically warm:
key_color_warm = (1.0, 0.90, 0.75)  # Golden

# Cool fill light (simulates sky bounce/ambient)
fill_color = (0.85, 0.90, 1.0)      # Cool white
# OR more dramatically cool:
fill_color_cool = (0.80, 0.85, 1.0)  # Blue-ish

# Neutral rim light
rim_color = (1.0, 1.0, 1.0)         # Pure white
# OR warm rim for golden rim effect:
rim_color_warm = (1.0, 0.95, 0.80)
```

### Color Temperature Reference

| Temperature (K) | RGB Approximation | Description | Use |
|-----------------|-------------------|-------------|-----|
| 2700K | (1.0, 0.83, 0.62) | Warm incandescent | Indoor, intimate |
| 3200K | (1.0, 0.87, 0.72) | Tungsten studio | Classic studio |
| 4000K | (1.0, 0.93, 0.83) | Warm white | Natural daylight (warm) |
| 5000K | (1.0, 0.96, 0.91) | Neutral white | Neutral daylight |
| 5500K | (1.0, 0.97, 0.95) | Daylight standard | Photography standard |
| 6500K | (1.0, 1.0, 1.0) | D65 white point | Monitor white |
| 7500K | (0.90, 0.92, 1.0) | Overcast sky | Cool fill |
| 10000K | (0.80, 0.85, 1.0) | Blue sky | Very cool fill |

## 5. AREA Light Size

### Shadow Softness Rule

Shadow softness is directly proportional to the light SIZE relative to the subject:
- **Larger light** = **Softer shadows** (like overcast sky)
- **Smaller light** = **Harder shadows** (like bare bulb)

### Size Guidelines

```python
# Key light — moderately soft shadows
key_size = character_height * 1.5
# For 1.8m human: 2.7m wide light

# Fill light — very soft (larger than key)
fill_size = character_height * 2.0
# For 1.8m human: 3.6m wide light

# Rim light — tighter (can be smaller)
rim_size = character_height * 0.8
# For 1.8m human: 1.44m wide light
```

### Size Table

| Character Height | Key Size | Fill Size | Rim Size |
|-----------------|----------|-----------|----------|
| 0.3m | 0.45m | 0.6m | 0.24m |
| 1.0m | 1.5m | 2.0m | 0.8m |
| 1.8m | 2.7m | 3.6m | 1.44m |
| 2.5m | 3.75m | 5.0m | 2.0m |

### Shape Recommendation

```python
light.shape = 'RECTANGLE'
light.size = key_size       # Width
light.size_y = key_size * 0.7  # Height (slightly shorter for studio look)
```

## 6. World Background

### Dark Studio Setup

For character/product rendering, use a very dark world background to prevent
uncontrolled ambient light:

```python
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new('World')
    bpy.context.scene.world = world
world.use_nodes = True
nodes = world.node_tree.nodes
bg = nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.03, 0.03, 0.03, 1.0)  # Very dark gray
    bg.inputs['Strength'].default_value = 0.1   # Very low intensity
```

### Background Recommendations

| Scene Type | BG Color (RGB) | Strength | Notes |
|------------|---------------|----------|-------|
| Dark studio | (0.02-0.05, 0.02-0.05, 0.02-0.05) | 0.05-0.1 | Minimal ambient |
| Bright studio | (0.5, 0.5, 0.5) | 0.3-0.5 | More even illumination |
| Outdoor day | (0.4, 0.6, 0.8) | 1.0-2.0 | Sky blue ambient |
| Night scene | (0.01, 0.01, 0.02) | 0.02-0.05 | Near-black with blue tint |
| Product shot | (1.0, 1.0, 1.0) | 0.3-0.5 | White background |

## 7. Shadow Settings

### Contact Shadows (EEVEE)

In EEVEE, contact shadows add small-scale shadow detail:
```python
light.use_contact_shadow = True
light.contact_shadow_distance = 0.1   # Max distance to cast contact shadows
light.contact_shadow_bias = 0.03      # Prevents self-shadowing artifacts
light.contact_shadow_thickness = 0.2  # Shadow thickness
```

### Soft Shadow Control

```python
# Cycles — shadow softness comes from light size
light.shadow_soft_size = 0.1  # Point/Spot lights only

# Area lights — shadow softness from physical size
light.size = 2.0  # Larger = softer

# EEVEE — additional shadow map settings
light.shadow_buffer_clip_start = 0.05
light.shadow_cascade_max_distance = 20.0  # Sun light only
```

## 8. Dramatic vs Even Lighting

### Dramatic Lighting (High Contrast)
- Key:Fill ratio = **4:1 to 8:1** (fill is very weak)
- Strong rim light (80-100% of key)
- Dark background, minimal ambient
- Use for: villains, horror, film noir, intense portraits

```python
# Dramatic setup
key_energy = 600
fill_energy = key_energy * 0.15   # Very weak fill = deep shadows
rim_energy = key_energy * 0.8     # Strong rim = dramatic silhouette
world_strength = 0.02             # Near-zero ambient
```

### Even Lighting (Low Contrast)
- Key:Fill ratio = **1.5:1 to 2:1** (fill is strong)
- Moderate rim
- Slightly brighter background
- Use for: heroes, beauty shots, product visualization, friendly characters

```python
# Even/beauty setup
key_energy = 400
fill_energy = key_energy * 0.5    # Strong fill = open shadows
rim_energy = key_energy * 0.4     # Subtle rim
world_strength = 0.15             # Slight ambient fill
```

### Mood-Based Presets

| Mood | Key:Fill | Rim % | World Str | Key Temp | Fill Temp |
|------|----------|-------|-----------|----------|-----------|
| Heroic | 2:1 | 50% | 0.1 | Warm | Neutral |
| Mysterious | 5:1 | 80% | 0.03 | Cool | Cool |
| Villainous | 6:1 | 90% | 0.02 | Red/warm | Cold blue |
| Friendly | 1.5:1 | 30% | 0.2 | Warm | Warm |
| Sad | 3:1 | 20% | 0.05 | Cool | Cool |
| Epic | 3:1 | 100% | 0.05 | Golden | Blue |

## 9. Complete Three-Point Setup — bpy Code Template

```python
import bpy
import math

def setup_three_point_lighting(character_height=1.8, mood='neutral'):
    """Create a complete 3-point lighting setup for character rendering."""

    # Energy calculations
    key_energy = character_height * 300
    fill_ratio = 0.35
    rim_ratio = 0.6
    distance = character_height * 2.5
    key_size = character_height * 1.5

    # Mood adjustments
    if mood == 'dramatic':
        fill_ratio = 0.15
        rim_ratio = 0.85
    elif mood == 'beauty':
        fill_ratio = 0.5
        rim_ratio = 0.4

    # --- KEY LIGHT ---
    bpy.ops.object.light_add(type='AREA', location=(
        distance * 0.7,   # X: slightly right
        -distance,         # Y: in front
        distance * 0.8    # Z: above
    ))
    key = bpy.context.active_object
    key.name = 'Key_Light'
    key.data.energy = key_energy
    key.data.shape = 'RECTANGLE'
    key.data.size = key_size
    key.data.size_y = key_size * 0.7
    key.data.color = (1.0, 0.95, 0.85)

    # Point at origin (character center)
    direction = key.location.normalized()
    rot_quat = direction.to_track_quat('-Z', 'Y')
    key.rotation_euler = rot_quat.to_euler()

    # --- FILL LIGHT ---
    bpy.ops.object.light_add(type='AREA', location=(
        -distance * 0.8,  # X: opposite side
        -distance * 0.6,  # Y: slightly forward
        distance * 0.4    # Z: lower
    ))
    fill = bpy.context.active_object
    fill.name = 'Fill_Light'
    fill.data.energy = key_energy * fill_ratio
    fill.data.shape = 'RECTANGLE'
    fill.data.size = key_size * 1.5    # Larger = softer
    fill.data.size_y = key_size * 1.0
    fill.data.color = (0.85, 0.90, 1.0)  # Cool

    direction = fill.location.normalized()
    rot_quat = direction.to_track_quat('-Z', 'Y')
    fill.rotation_euler = rot_quat.to_euler()

    # --- RIM LIGHT ---
    bpy.ops.object.light_add(type='AREA', location=(
        -distance * 0.3,  # X: slightly opposite
        distance * 0.8,   # Y: behind
        distance * 0.9    # Z: above
    ))
    rim = bpy.context.active_object
    rim.name = 'Rim_Light'
    rim.data.energy = key_energy * rim_ratio
    rim.data.shape = 'RECTANGLE'
    rim.data.size = key_size * 0.6
    rim.data.size_y = key_size * 0.4
    rim.data.color = (1.0, 1.0, 1.0)

    direction = rim.location.normalized()
    rot_quat = direction.to_track_quat('-Z', 'Y')
    rim.rotation_euler = rot_quat.to_euler()

    # --- WORLD ---
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new('World')
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.03, 0.03, 0.03, 1.0)
        bg.inputs['Strength'].default_value = 0.08

    return key, fill, rim
```
