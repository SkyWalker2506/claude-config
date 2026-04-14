---
last_updated: 2026-04-14
confidence: high
sources: ["Blender Lighting Docs", "3-Point Lighting Theory", "Cinematography & Photography Standards", "PBR Rendering Practices"]
---

# Lighting Setup Guide

Professional lighting isolates subject, creates mood, and guides viewer attention. Proper setup is foundation of hero shots and product visualization.

## Quick Reference: Light Types in Blender

| Type | Range | Energy | Best For | Notes |
|------|-------|--------|----------|-------|
| **Sun** | Infinite | 2-4 | Natural daylight, key light | Parallel rays, no decay |
| **Area** | Local | 200-500W | Fill/rim, detailed fill | Soft shadows, studio standard |
| **Spot** | Local | 300-800W | Focused key, rim accent | Hard edges, controllable cone |
| **Point** | Local | 100-300W | Ambient fill | Omnidirectional |
| **HDRI** | Image-based | 0-2 (multiplier) | Environment, indirect | Image-based global lighting |

## 3-Point Lighting Foundation

Industry-standard setup: Key + Fill + Rim.

### 1. Key Light (Main/Hero Light)

**Role:** Primary light that reveals subject, creates shadow structure.

**Setup:**
- **Position:** 45° front-side, ~2-3m distance, slight above eye level
- **Angle:** Creates defined shadows on far side of face/object
- **Energy:** Strongest (Sun: 3.0, Area: 300W, Spot: 500W)
- **Shadow:** Hard (Spot) or soft (Area)
- **Color:** Warm (2700-3500K) for flattering; cool (5000K) for dramatic

Blender example:
```python
import bpy

# Create key light
key_light = bpy.data.lights.new(name="Key_Light", type='AREA')
key_light.energy = 300  # Watts
key_light.size = 2.0  # Soft shadow (increase for softer)
key_light.color = (1.0, 0.95, 0.85)  # Warm ~3000K

key_obj = bpy.data.objects.new("Key_Light_Obj", key_light)
bpy.context.collection.objects.link(key_obj)

# Position: 45° to subject, 2.5m distance, elevated
key_obj.location = (2.5, 2.5, 2.0)
key_obj.rotation_euler = (1.1, 0.79, 0)  # 45° pitch, 45° yaw
```

### 2. Fill Light (Secondary)

**Role:** Softens shadows, reveals detail in shadow areas, reduces contrast.

**Setup:**
- **Position:** Opposite side from key (or front-center for even fill)
- **Energy:** 30-50% of key light (Sun: 1.2, Area: 100-150W)
- **Shadow:** Soft (Area light) or no shadow (infinite distance)
- **Color:** Neutral (5000K) or slightly cool
- **Goal:** Fill shadows without casting competing shadows

Blender example:
```python
# Create fill light (opposite from key)
fill_light = bpy.data.lights.new(name="Fill_Light", type='AREA')
fill_light.energy = 120  # 40% of key
fill_light.size = 3.0  # Soft
fill_light.color = (0.9, 0.95, 1.0)  # Neutral-cool ~5000K

fill_obj = bpy.data.objects.new("Fill_Light_Obj", fill_light)
bpy.context.collection.objects.link(fill_obj)

# Position: opposite side, lower energy
fill_obj.location = (-2.0, 0, 1.5)
fill_obj.rotation_euler = (0.9, -0.79, 0)
```

### 3. Rim Light (Accent)

**Role:** Separates subject from background, adds dimension, creates halo/rim effect.

**Setup:**
- **Position:** Behind subject, side-to-side angle (camera can't see it directly)
- **Energy:** 50-100% of key light (Sun: 1.5-2.0, Area: 150-300W)
- **Shadow:** Hard edges preferred (Spot or small Area)
- **Color:** Warm (3000K) or complementary color (e.g., cool rim on warm subject)
- **Goal:** Rim that catches edge of subject, not full-body backlight

Blender example:
```python
# Create rim light (behind subject, off to side)
rim_light = bpy.data.lights.new(name="Rim_Light", type='SPOT')
rim_light.energy = 200  # 67% of key
rim_light.spot_size = 0.8  # ~45° cone
rim_light.spot_blend = 0.2  # Hard edge
rim_light.color = (1.0, 0.8, 0.7)  # Warm rim ~2800K

rim_obj = bpy.data.objects.new("Rim_Light_Obj", rim_light)
bpy.context.collection.objects.link(rim_obj)

# Position: Behind and to side, higher than subject
rim_obj.location = (-1.5, 3.0, 2.8)
rim_obj.rotation_euler = (0.4, 1.57, 0)  # Aim toward subject
```

## Color Temperature & Mood

| Color (Kelvin) | Feel | Best Used |
|---|---|---|
| **2000-3000K** | Warm, intimate, candlelit | Key light for characters, dusk scenes |
| **3500-4000K** | Natural, friendly | Fill light, neutral environments |
| **5000-5600K** | Daylight, cool, professional | Overcast, studio standard, product |
| **6500-7000K** | Cool, morning, medical | Technical, surgical, clinical mood |
| **10000K+** | Extremely blue, alien | Special effects, sci-fi only |

**Setup rule:** Key light warmer → Rim warmer → Fill cooler (creates depth).

## HDRI Lighting (Image-Based Lighting)

For environment-integrated lighting:

Blender HDRI setup:
```python
import bpy
from bpy import context

# Enable HDRI in World Shader Editor
world = context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
nodes.clear()

# Add Background + HDRI Texture
link = world.node_tree.links
output = nodes.new(type='ShaderNodeOutputWorld')
background = nodes.new(type='ShaderNodeBackground')
hdr_tex = nodes.new(type='ShaderNodeTexEnvironment')
mapping = nodes.new(type='ShaderNodeMapping')
coord = nodes.new(type='ShaderNodeTexCoord')

# Connect nodes
link.new(hdr_tex.outputs[0], background.inputs[0])
link.new(mapping.outputs[0], hdr_tex.inputs[0])
link.new(coord.outputs[2], mapping.inputs[0])
link.new(background.outputs[0], output.inputs[0])

# Load HDRI (replace path with your file)
hdr_tex.image = bpy.data.images.load(filepath="/path/to/hdri.exr")

# Adjust intensity
background.inputs[1].default_value = 1.5  # Brightness multiplier
mapping.inputs[2].z = 0.5  # Rotation (0-1 normalized)
```

**HDRI benefits:**
- Realistic reflections & indirect lighting
- No manual light setup required
- Quick mood changes (swap HDRI)
- Professional results with minimal tweaking

**HDRI sources:**
- Polyhaven (free, high-quality 16K)
- HDRI Haven (curated, industry standard)
- Substance Source (professional, subscription)

## Lighting for Different Asset Types

### Character Lighting

**Goal:** Flattering, reveals anatomy, soft shadows.

- **Key:** 45° angle, eye-level or slightly above, warm (3000K)
- **Fill:** Opposite side, 40% intensity, 5000K
- **Rim:** Side-back, narrow, warm (2800K), 70% key intensity
- **Energy levels:** Key 300W, Fill 120W, Rim 200W

### Product/Object Lighting

**Goal:** Shows form, material, clean shadows, isolated.

- **Key:** 45° angle, reveals surface detail, warm (3500K)
- **Fill:** Front-center or opposite, 50% intensity, neutral (5000K)
- **Rim:** Behind, creates separation from background, 60% key
- **Background light:** Optional separate light on background to prevent shadow crushing

### Vehicle Lighting

**Goal:** Emphasizes curves, showcases design lines.

- **Key:** Lower angle (30° from horizontal), side-mounted, warm (3500K)
- **Fill:** Opposite side, 35% intensity (less fill for dramatic)
- **Rim:** Side-back at 90°, very bright (100% key), sharp edges
- **Environment:** Often HDRI for realistic reflections

### Environment/Scene Lighting

**Goal:** Establishes time of day, mood, layered depth.

- **Sky light (Sun):** Main directional, color varies by time (blue dawn → orange sunset)
- **Bounce/Fill:** HDRI or large Area lights to fill shadows
- **Accent:** Spot lights for focal areas (windows, fires, etc.)

## Lighting Setup Workflow

1. **Add key light**
   - Place 45° front-side, above eye level
   - Set warmth (2700-3500K)
   - Adjust energy until subject reads clearly

2. **Add fill light**
   - Place opposite side or front-center
   - Set to 30-50% key intensity
   - Ensure shadows are visible but not black

3. **Add rim light**
   - Place behind/side, out of camera view
   - Set to 50-100% key intensity
   - Adjust angle to catch subject edge only

4. **Render preview** (Shift+Z or F12)
   - Check shadow definition
   - Verify rim separates from background
   - Confirm fill softens shadows adequately

5. **Fine-tune**
   - Adjust positions for optimal shadow placement
   - Tweak color temperatures for mood
   - Increase/decrease energy for desired contrast ratio

6. **Add environment** (optional HDRI)
   - Load high-quality HDRI
   - Set to 0.5-1.5 intensity multiplier
   - Rotate for desired lighting direction

## Anti-Patterns

- **Single light source:** Creates harsh, unnatural shadows (always use 3-point minimum)
- **All same color temperature:** Flat, lifeless (use warm key + cool fill)
- **Rim light visible to camera:** Breaks realism (position off-camera)
- **Over-bright fill:** Kills shadow detail, flattens form (limit to 40-50%)
- **No rim separation:** Subject merges with background (always add rim)
- **Inconsistent shadow density:** Some shadows black, some gray (balanced fill ratio)

## Verification Checklist

- [ ] Key light reveals form with clear shadow structure
- [ ] Fill light softens shadows without creating competing shadows
- [ ] Rim light visible only as edge accent, not full glow
- [ ] Color temperature progression: warm key → cool fill → warm rim
- [ ] Shadow ratio: bright areas 3-4x brighter than shadow areas (film standard)
- [ ] Background separated from subject via rim light
- [ ] Render shows no blown-out highlights (unless intentional)
- [ ] All light sources positioned realistically (not inside objects)
