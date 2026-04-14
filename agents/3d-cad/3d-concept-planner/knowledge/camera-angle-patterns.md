---
last_updated: 2026-04-14
confidence: high
sources: ["Blender Camera Documentation", "Cinematography Standards", "3D Rendering Best Practices"]
---

# Camera Angle Patterns

Camera choice defines viewer perspective, emotional impact, and asset readability. Different focal lengths and angles serve different narrative purposes.

## Quick Reference: Common Angles

| Angle | Use Case | Emotion | Hero Shot? |
|-------|----------|---------|-----------|
| Eye Level (0°) | Neutral, relatable | Calm, equal | Medium (depend on composition) |
| High Angle (30-45° down) | Vulnerable subject, overhead view | Power over subject | Rarely |
| Low Angle (30-45° up) | Imposing subject, empowerment | Power, grandeur | Excellent |
| Dutch Angle (5-15° tilt) | Tension, action | Unease, dynamic | Context-dependent |
| Bird's Eye (90° down) | Map, top-down view | Omniscient | No |

## Focal Length & Field of View (FOV)

**Rule:** FOV directly impacts perceived scale and distortion.

| Focal Length | FOV | Use Case | Distortion | Depth Feel |
|--------------|-----|----------|------------|-----------|
| **35mm** | ~54° | Natural, default | None | Realistic |
| **50mm** | ~47° | Portrait, product (film standard) | Minimal | Moderate |
| **85mm** | ~28° | Character closeup, detailed hero | None | Compressed (intimate) |
| **24mm** | ~74° | Wide environment, action | Heavy barrel | Exaggerated depth |
| **135mm** | ~18° | Telephoto, distant detail | None | Flattened (compressed depth) |

**Blender setup:**
```python
# Camera properties:
# Camera > Lens > Focal Length (mm)
# Or use Lens Presets (35mm, 50mm, 85mm, etc.)

# Quick FOV calc from focal length:
# FOV ≈ 2 * atan(sensor_width / (2 * focal_length))
# Blender does this automatically via Focal Length field
```

**Decision matrix:**
- **Product/Hero shot:** 50-85mm (minimal distortion, flattering proportions)
- **Wide environment:** 24-35mm (context, scale, drama)
- **Distant detail:** 100-135mm (compression, isolation)
- **Avoid:** <20mm or >200mm for character unless intentional (sci-fi, distortion effect)

## Hero Shot Patterns

**Pattern 1: Low Angle + Side Light**
- Camera 30° below eye level
- Subject fills 40-50% frame height
- Key light from 45° side-front
- Creates: Imposing, powerful read
- Industries: Character, vehicle, product premium

**Pattern 2: Eye Level + 3/4 View**
- Camera at subject torso height
- 45° rotation (3/4 view, not dead side)
- Leading lines behind (architecture, perspective)
- Creates: Relatable, confident, heroic
- Industries: Game trailers, character concepts, product demos

**Pattern 3: Elevated + Slight Downward Tilt**
- Camera 1-2m above eye level
- 10-15° downward tilt (not 90°)
- Subject off-center (rule of thirds)
- Creates: Cinematic, professional, editorial
- Industries: Fashion, automotive, architectural

**Pattern 4: Close-Up + Depth Cue**
- Focal length 85-135mm
- Subject 1-2m from lens
- Foreground/background depth blur
- Creates: Intimate, focused, premium
- Industries: Jewelry, beauty, detail showcase

## Turntable/Orbital Setup

For product visualization & 360° view:
- **Camera path:** Circular orbit around subject
- **Distance:** Subject fills 30-40% frame
- **Rotation:** Constant height, 360° revolution
- **Speed:** 6-12 frames per 360° (or 48 frames @ 60fps = 8 sec/rotation)

Blender orbital path:
```python
# Method 1: Follow Path constraint
# 1. Add Bezier circle path
# 2. Camera > Constraints > Follow Path
# 3. Set target: the circle
# 4. Set fixed axis, animate offset 0→1 over duration

# Method 2: Track To constraint (simpler)
# 1. Add empty sphere at scene center
# 2. Camera > Constraints > Track To
# 3. Set target: empty
# 4. Rotate empty/camera manually or use armature
```

Keyframe setup (24fps, 8 second orbit):
```python
# Frame 1: set camera rotation = 0°
# Frame 192: set camera rotation = 360°
# Interpolation: linear
# Result: smooth 360° rotation in 8 seconds @ 24fps
```

## Camera Positioning Decision Tree

**Q1: What's the hero?**
- Character → Eye level or low angle (flattering)
- Vehicle → 3/4 view, slightly elevated
- Architecture → Leading lines, vanishing point emphasis
- Product → 50-85mm, clean isolation
- Environment → Wide FOV, leading lines

**Q2: Emotional tone?**
- Heroic/powerful → Low angle + side-front key light
- Intimate/detailed → 85-135mm, close depth
- Cinematic/grand → 35mm wide, high vantage
- Neutral/professional → Eye level, 50mm

**Q3: Technical constraint?**
- VR/360 → Orbital, equirectangular projection
- Game engine → Typical FOV 60-70° (depends on engine)
- Cinema/marketing → 50mm default, varies per shot
- Orthographic → 0° tilt, parallel projection (no perspective)

## Perspective Modes

### Perspective (Standard)
```python
# Camera > Lens > Type = Perspective
# Mimics human eye, converging lines
# Used for: Almost all hero shots, cinematic
```

### Orthographic
```python
# Camera > Lens > Type = Orthographic
# Parallel projection, no vanishing point
# Used for: Technical drawing, orthogonal views, game UI
# Set focal distance to match your viewing distance
```

### Panoramic (Optional)
```python
# Compositor node-based or external stitching
# Useful for environment ref capture (not hero shots)
```

## Anti-Patterns

- **Perfectly centered subject:** Kills compositional tension (use rule of thirds)
- **Extreme FOV without reason:** <20mm distorts proportions (ugly on characters)
- **Camera too close:** Perspective distortion (large nose, exaggerated features)
- **Flat 2D angle:** Subject parallel to camera = boring depth (rotate 45°)
- **Horizon through head:** Cuts off character awkwardly
- **No depth blur:** Flat background competes with subject (use DoF)

## Blender Camera Setup Workflow

1. **Place subject** in scene (origin at feet for characters)
2. **Add camera** — Shift+A > Camera
3. **Position camera:**
   - Distance: ~2-4 body-heights from subject
   - Height: eye level (or chosen angle)
   - Angle: 45° rotation (3/4 view) or as planned
4. **Set focal length:**
   - Measurement: 50mm (default) for portrait
   - Adjust: 35mm for wider context, 85mm+ for closeup
5. **Enable frame:**
   - View > Viewport > Camera as Active (Numpad 0)
   - Check subject placement vs rule-of-thirds guide
6. **Optional: Add depth of field (DoF)**
   ```python
   # Camera > Depth of Field
   # Focus distance: 3.5m (adjust to subject)
   # F-stop: 2.8 (shallow) to 5.6 (moderate) to 16 (deep)
   ```
7. **Preview render** — Shift+Z (Material Preview) or F12 (render)
