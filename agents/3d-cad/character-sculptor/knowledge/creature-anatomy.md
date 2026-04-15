---
last_updated: 2026-04-14
refined_by: opus-4.6
confidence: high
sources:
  - https://conceptartempire.com/orc-goblin-gallery/
  - https://blog.kongregate.com/design-tips-for-in-game-character-proportions/
  - https://tvtropes.org/pmwiki/pmwiki.php/Main/OurOrcsAreDifferent
  - https://www.quora.com/Which-of-these-mythical-monsters-is-the-largest-trolls-ogres-orcs-or-goblins
  - https://blog.cg-wire.com/character-shape-language/
  - https://docs.blender.org/api/current/bpy.types.MetaElement.html
---

# Creature Anatomy for Character Sculpting

## 1. Fantasy Creature Proportions Table

All measurements use "head-count" (total height / head height). Human baseline = 7.5 heads.

| Creature | Head-Count | Height (m) | Shoulder Width (heads) | Leg Ratio | Key Shape | Shape Language |
|----------|-----------|------------|----------------------|-----------|-----------|---------------|
| Goblin | 3.5-4.5 | 0.9-1.2 | 1.2-1.5 | 0.35 (short) | Angular/pointy | Triangle-dominant |
| Dwarf | 4.5-5.5 | 1.2-1.5 | 2.5-3.0 | 0.35 (short) | Wide/blocky | Square-dominant |
| Elf | 8.0-9.0 | 1.8-2.1 | 1.3-1.5 | 0.50 (long) | Elongated/elegant | Circle+triangle |
| Orc | 6.0-7.0 | 1.8-2.2 | 2.5-3.0 | 0.42 (normal) | Massive/blocky | Square+triangle |
| Troll | 5.0-6.0 | 2.5-3.5 | 2.5-3.0 | 0.45 (long arms) | Hulking/uneven | Square-dominant |
| Ogre | 5.5-6.5 | 2.5-3.0 | 2.5-3.5 | 0.40 (thick) | Bloated/round | Circle+square |
| Dragon (humanoid) | 7.0-8.0 | 2.0-2.5 | 2.0-2.5 | 0.45 | Reptilian/angular | Triangle-dominant |
| Fairy/Pixie | 5.0-6.0 | 0.15-0.3 | 1.0-1.2 | 0.48 | Delicate/slight | Circle-dominant |
| Undead | 7.0-8.0 | 1.7-1.9 | 1.3-1.5 | 0.47 | Gaunt/skeletal | Triangle-dominant |

### Leg Ratio
Ratio of leg length (hip to sole) vs total height. Normal human = 0.47.

## 2. Key Differentiators Per Creature Type

### 2.1 Goblin
**What makes it recognizable:**
- Oversized head relative to body (~25% of height; range 1/3.5 to 1/4.5)
- Large, pointed ears (extend above skull top, angled back 30-45 deg)
- Prominent, sharp nose (elongated, hooked or upturned)
- Small, sunken eyes with large brow ridge
- Hunched posture with forward head carriage
- Narrow shoulders (1.2-1.5 head-widths)
- Thin, wiry limbs with knobby joints
- Disproportionately large hands and feet relative to limbs
- Exaggerated finger length (1.5x human ratio)
- Wide, thin-lipped mouth with underbite or protruding teeth

**Silhouette test:** Small, crouching, angular profile with prominent ears and nose.

### 2.2 Orc
**What makes it recognizable:**
- Massive jaw with protruding lower canines (tusks)
- Very wide shoulders (2.5-3x head width)
- Short, thick neck (nearly nonexistent in some designs)
- Heavy brow ridge creating deep eye sockets
- Broad, flat nose with flared nostrils
- Thick, trunk-like limbs with visible musculature
- Barrel chest, thick torso
- Slightly shorter legs relative to torso (stocky build)
- Green/grey skin with rough, leathery texture

**Silhouette test:** Wide, powerful, top-heavy triangle. Tusks and jaw define head.

### 2.3 Elf
**What makes it recognizable:**
- Elongated proportions (8-9 heads tall)
- Pointed ears (smaller than goblin, elegant, 10-20 deg angle)
- High cheekbones, narrow jaw, delicate features
- Long neck (1.2-1.5x human proportions)
- Narrow shoulders with graceful musculature
- Long, slender limbs with minimal bulk
- Small, defined hands with tapered fingers
- Almond-shaped eyes, slightly larger than human
- Smooth, unblemished skin

**Silhouette test:** Tall, willowy, vertical emphasis. Ears create distinctive head shape.

### 2.4 Dwarf
**What makes it recognizable:**
- Very wide shoulders relative to height (2.5-3.0 heads)
- Barrel chest, deep ribcage
- Short, powerful legs (about 35% of height)
- Large hands, thick fingers (built for labor)
- Prominent, wide nose
- Heavy brow with deep-set eyes
- Strong jaw, often hidden by beard
- Thick, stocky neck
- Dense musculature throughout

**Silhouette test:** Wide rectangle, almost as wide as tall. Compact, grounded stance.

### 2.5 Troll
**What makes it recognizable:**
- Long arms reaching below knees (ape-like proportions)
- Small head relative to massive body
- Hunched or stooped posture
- Enormous hands with club-like fingers
- Thick, warty or stony skin texture
- Disproportionately large feet
- Minimal neck; head sits directly on shoulders
- Pronounced spine and vertebrae visible through skin
- Underbite with sparse, large teeth

**Silhouette test:** Massive, hunched, arms dominate. Gorilla-like stance.

### 2.6 Dragon (Humanoid/Dragonborn)
**What makes it recognizable:**
- Scaled skin texture across entire body
- Elongated skull with snout/muzzle
- Horns or ridges from skull
- Thick, muscular neck (longer than human)
- Clawed hands and feet (4 digits typical)
- Tail extending from base of spine
- Optional wing structure from shoulder blades
- Ridged brow and jaw plates
- Slit pupils

**Silhouette test:** Humanoid but with horns, tail, and broader stance. Neck distinguishes from human.

## 3. Exaggerated Features Per Creature Type

### Exaggeration Multipliers (vs Human Baseline = 1.0)

| Feature | Goblin | Orc | Elf | Dwarf | Troll |
|---------|--------|-----|-----|-------|-------|
| Head size | 1.4x | 1.1x | 0.9x | 1.2x | 0.7x |
| Ear length | 2.5x | 1.2x | 1.8x | 1.0x | 1.3x |
| Nose size | 1.8x | 1.5x | 0.8x | 1.4x | 1.6x |
| Jaw width | 0.8x | 1.8x | 0.7x | 1.5x | 1.3x |
| Shoulder width | 0.7x | 1.6x | 0.8x | 1.5x | 1.4x |
| Hand size | 1.3x | 1.4x | 0.9x | 1.5x | 1.8x |
| Foot size | 1.3x | 1.3x | 0.9x | 1.4x | 1.6x |
| Arm length | 1.1x | 1.0x | 1.1x | 0.8x | 1.4x |
| Leg length | 0.7x | 0.9x | 1.1x | 0.7x | 0.9x |
| Finger length | 1.5x | 1.0x | 1.2x | 0.8x | 1.3x |
| Neck length | 0.8x | 0.5x | 1.3x | 0.6x | 0.3x |
| Brow ridge | 1.5x | 2.0x | 0.5x | 1.5x | 1.8x |

## 4. How to Modify a Human Base into Each Creature Type

### 4.1 Human to Goblin
1. **Scale head** up to 1.4x; shift forward (hunched posture)
2. **Scale torso** down to 0.7x height; narrow shoulders
3. **Scale legs** down to 0.7x length; keep feet large
4. **Elongate ears**: extrude from temporal bone area, angle back 30-45 deg
5. **Elongate nose**: scale 1.8x, add hook or upturn
6. **Enlarge hands**: scale 1.3x, lengthen fingers
7. **Reduce muscle mass**: wiry, lean; emphasize tendons and joints
8. **Forward head posture**: shift head 0.05 units forward in Y
9. **Widen mouth**: scale mouth width 1.3x, thin the lips
10. **Add brow ridge**: push supraorbital area forward 0.01 units

### 4.2 Human to Orc
1. **Widen shoulders** to 1.6x; thicken neck
2. **Enlarge jaw**: scale mandible 1.8x width, add protruding lower canines
3. **Barrel the chest**: scale ribcage 1.3x in Y (depth)
4. **Thicken limbs**: scale arms and legs 1.3x in XY
5. **Flatten nose**: scale 1.5x width, reduce bridge height
6. **Deepen brow ridge**: push forward 0.02 units
7. **Reduce neck length** to 0.5x; merge visually into trapezius
8. **Add muscle mass**: exaggerate deltoids, traps, pectorals, forearms
9. **Thicken hands**: scale 1.4x, blunt finger tips
10. **Texture**: rough, leathery; displacement strength 1.3x human

### 4.3 Human to Elf
1. **Elongate proportions**: scale height to 1.1x, narrow everything 0.85x
2. **Sharpen features**: narrow jaw to 0.7x, raise cheekbones
3. **Add pointed ears**: smaller than goblin, elegant angle
4. **Lengthen neck**: scale 1.3x
5. **Elongate fingers**: scale 1.2x, taper tips
6. **Reduce muscle mass**: lean but defined; dancer/swimmer build
7. **Enlarge eyes slightly**: 1.1x, almond shape
8. **Smooth skin**: reduce all displacement roughness by 50%
9. **Narrow shoulders**: graceful, not broad
10. **Extend limbs**: legs and arms 1.1x length

### 4.4 Human to Dwarf
1. **Compress height**: scale legs to 0.7x length
2. **Widen torso**: scale shoulders 1.5x, chest depth 1.3x
3. **Enlarge hands**: scale 1.5x, thick fingers
4. **Thicken neck**: scale 1.3x diameter
5. **Barrel chest**: deeper ribcage, wider
6. **Shorten arms slightly**: 0.8x length but thick
7. **Widen nose**: scale 1.4x
8. **Deepen brow**: push forward, create shadowed eyes
9. **Add mass**: dense, compact musculature everywhere
10. **Thicken feet**: wide, stable base

## 5. Goblin Metaball Elements (Primary Test Case)

Complete metaball specification for a goblin character. Scale = 1.0 = roughly 1 meter tall.

```python
# Conceptual — E2 (Blender Script Agent) implements
import bpy
from mathutils import Vector

def create_goblin_blockout(scale=1.0):
    """Metaball blockout for a goblin character."""
    mb = bpy.data.metaballs.new('Goblin')
    obj = bpy.data.objects.new('GoblinBlockout', mb)
    bpy.context.collection.objects.link(obj)
    
    mb.resolution = 0.12
    mb.threshold = 0.6
    
    # Goblin characteristics:
    # - Large head (1.4x), hunched posture
    # - Wiry body, thin limbs, knobby joints
    # - Big ears, long nose, large hands/feet
    
    elements = [
        # === HEAD (large, forward) ===
        ("cranium",       0,     0.04,  0.85, 0.065, 2.0),
        ("jaw",           0,     0.06,  0.81, 0.035, 1.5),
        ("brow_ridge",    0,     0.07,  0.87, 0.025, 1.2),
        ("nose",          0,     0.10,  0.84, 0.015, 1.0),
        
        # Ears (large, pointed, angled back)
        ("ear_R",         0.06,  0.00,  0.86, 0.025, 0.8),
        ("ear_tip_R",     0.09, -0.02,  0.90, 0.012, 0.6),
        ("ear_L",        -0.06,  0.00,  0.86, 0.025, 0.8),
        ("ear_tip_L",    -0.09, -0.02,  0.90, 0.012, 0.6),
        
        # === NECK (thin, forward-leaning) ===
        ("neck",          0,     0.02,  0.76, 0.022, 1.5),
        
        # === TORSO (thin, hunched) ===
        ("chest",         0,     0.01,  0.65, 0.055, 2.0),
        ("belly",         0,     0.02,  0.55, 0.050, 1.8),  # Slightly pot-bellied
        ("pelvis",        0,     0.00,  0.45, 0.045, 2.0),
        
        # Spine hunch (push upper back backward)
        ("upper_back",    0,    -0.04,  0.68, 0.040, 1.5),
        
        # === RIGHT ARM (thin, long fingers) ===
        ("shoulder_R",    0.08,  0.00,  0.70, 0.022, 1.5),
        ("upper_arm_R",   0.12,  0.00,  0.62, 0.018, 1.5),
        ("elbow_R",       0.14,  0.00,  0.56, 0.015, 1.2),  # Knobby
        ("forearm_R",     0.14,  0.02,  0.50, 0.016, 1.5),
        ("hand_R",        0.14,  0.04,  0.43, 0.020, 1.2),  # Large hand
        
        # === LEFT ARM (mirror) ===
        ("shoulder_L",   -0.08,  0.00,  0.70, 0.022, 1.5),
        ("upper_arm_L",  -0.12,  0.00,  0.62, 0.018, 1.5),
        ("elbow_L",      -0.14,  0.00,  0.56, 0.015, 1.2),
        ("forearm_L",    -0.14,  0.02,  0.50, 0.016, 1.5),
        ("hand_L",       -0.14,  0.04,  0.43, 0.020, 1.2),
        
        # === RIGHT LEG (short, thick joints) ===
        ("thigh_R",       0.04,  0.00,  0.36, 0.025, 1.8),
        ("knee_R",        0.04,  0.01,  0.26, 0.018, 1.2),  # Knobby
        ("shin_R",        0.04,  0.01,  0.18, 0.020, 1.5),
        ("ankle_R",       0.04,  0.01,  0.10, 0.015, 1.2),
        ("foot_R",        0.04,  0.05,  0.05, 0.022, 1.2),  # Large foot
        
        # === LEFT LEG (mirror) ===
        ("thigh_L",      -0.04,  0.00,  0.36, 0.025, 1.8),
        ("knee_L",       -0.04,  0.01,  0.26, 0.018, 1.2),
        ("shin_L",       -0.04,  0.01,  0.18, 0.020, 1.5),
        ("ankle_L",      -0.04,  0.01,  0.10, 0.015, 1.2),
        ("foot_L",       -0.04,  0.05,  0.05, 0.022, 1.2),
    ]
    
    for name, x, y, z, radius, stiffness in elements:
        elem = mb.elements.new()
        elem.co = Vector((x * scale, y * scale, z * scale))
        elem.radius = radius * scale
        elem.stiffness = stiffness
    
    return obj
```

### 5.1 Goblin Post-Conversion Modifier Stack

After converting metaball to mesh:

```python
# Conceptual — E2 implements
def setup_goblin_modifiers(obj):
    """Post-conversion modifier stack for goblin refinement."""
    
    # 1. Decimate: Clean up metaball topology
    dec = obj.modifiers.new('Cleanup', type='DECIMATE')
    dec.ratio = 0.5  # Reduce excess geometry
    
    # 2. Smooth: Remove metaball artifacts  
    smooth = obj.modifiers.new('SmoothBase', type='SMOOTH')
    smooth.factor = 0.5
    smooth.iterations = 5
    
    # 3. Subdivision Surface: Clean topology base
    sub = obj.modifiers.new('SubBase', type='SUBSURF')
    sub.levels = 1
    sub.render_levels = 2
    
    # 4. Displacement: Wrinkly skin texture
    tex_skin = bpy.data.textures.new('GoblinSkin', type='MUSGRAVE')
    tex_skin.musgrave_type = 'RIDGED_MULTIFRACTAL'
    tex_skin.noise_scale = 4.0
    tex_skin.dimension_max = 1.0
    tex_skin.lacunarity = 2.5
    tex_skin.octaves = 5.0
    
    disp = obj.modifiers.new('SkinTexture', type='DISPLACE')
    disp.texture = tex_skin
    disp.strength = 0.08
    disp.mid_level = 0.5
    disp.direction = 'NORMAL'
    
    # 5. Displacement: Warty bumps
    tex_warts = bpy.data.textures.new('GoblinWarts', type='VORONOI')
    tex_warts.noise_scale = 15.0
    tex_warts.distance_metric = 'DISTANCE'
    
    warts = obj.modifiers.new('Warts', type='DISPLACE')
    warts.texture = tex_warts
    warts.strength = 0.04
    warts.mid_level = 0.6  # Mostly inward, bumps outward
    warts.direction = 'NORMAL'
    
    return obj
```

## 6. Creature Anatomy Comparison Chart

### Skeletal Differences from Human

| Feature | Goblin | Orc | Elf | Dwarf | Troll |
|---------|--------|-----|-----|-------|-------|
| Skull shape | Elongated back | Wide, heavy | Narrow, tall | Wide, thick | Small, flat |
| Spine curvature | Pronounced kyphosis | Slight kyphosis | Straight/lordosis | Normal | Heavy kyphosis |
| Ribcage | Narrow, shallow | Wide, deep | Narrow, deep | Very wide, deep | Massive |
| Pelvis | Narrow | Wide | Narrow | Very wide | Wide |
| Femur angle | Bowed outward | Straight, thick | Straight, long | Short, thick | Massive, bowed |
| Clavicle length | Short | Long, thick | Long, slender | Short, thick | Massive |

### Muscle Mass Distribution

| Region | Goblin | Orc | Elf | Dwarf | Troll |
|--------|--------|-----|-----|-------|-------|
| Upper body | 20% | 45% | 30% | 40% | 50% |
| Core | 25% | 25% | 30% | 30% | 20% |
| Lower body | 25% | 30% | 40% | 30% | 30% |
| Overall density | Low | Very High | Low-Med | High | Very High |

### Skin Texture Characteristics

| Creature | Texture Type | Displacement Strength | Scale | Notes |
|----------|-------------|----------------------|-------|-------|
| Goblin | Wrinkled, warty | 0.06-0.10 | 3-6 | Ridged Musgrave + Voronoi bumps |
| Orc | Leathery, rough | 0.08-0.15 | 4-8 | FBM Musgrave, high octaves |
| Elf | Smooth, fine | 0.01-0.03 | 10-20 | Fine noise, minimal displacement |
| Dwarf | Weathered, tough | 0.05-0.10 | 5-10 | Hybrid Musgrave, medium detail |
| Troll | Rocky, cracked | 0.10-0.20 | 2-5 | Voronoi crackle + heavy Musgrave |
