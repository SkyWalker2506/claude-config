---
last_updated: 2026-04-14
refined_by: knowledge-sharpener (Opus 4.6)
confidence: high
sources:
  - https://dreamfarmstudios.com/blog/color-theory-for-character-design/
  - https://characterhub.com/blog/character-resources/character-color-palette
  - https://pixune.com/blog/character-color-palette/
  - https://buzzflick.com/color-palette-theory-for-character-design/
  - https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-14-advanced-techniques-realistic-real-time-skin
  - http://gurneyjourney.blogspot.com/2017/07/relative-color-temperature-on-skin-tones.html
  - https://thearmypainter.com/blogs/explore/how-to-pick-a-colour-scheme
  - https://icolorpalette.com/fantasy/
---

# Color Theory & Palettes

## 1. Color Wheel Fundamentals

### Color Harmony Schemes

| Scheme | Definition | Character Use | Risk |
|--------|-----------|---------------|------|
| **Complementary** | Opposite on wheel (e.g. red + green) | High contrast hero/villain; makes characters pop against backgrounds | Can be garish if both colors are fully saturated |
| **Analogous** | Adjacent on wheel (e.g. green + teal + blue) | Harmonious, cohesive characters; nature-themed | Risk of looking dull/flat without value contrast |
| **Triadic** | Three colors equally spaced (e.g. red + blue + yellow) | Dynamic, energetic characters; primary hero designs | Use one dominant, one secondary, one accent — never equal amounts |
| **Split-Complementary** | Base color + two adjacent to its complement | Contrast with less tension than pure complementary | Needs careful balance of warm and cool |
| **Monochromatic** | Single hue, varied by saturation and value | Mysterious, unified, elegant characters | Needs strong value range to avoid flatness |

### The 60-30-10 Rule

Every character palette should follow this distribution:

| Percentage | Role | Where on Character |
|-----------|------|--------------------|
| **60%** | Dominant color | Main body, clothing, largest surface area |
| **30%** | Secondary color | Supporting clothing, secondary skin area, armor |
| **10%** | Accent color | Eyes, jewelry, weapon glow, trim, small details |

This ratio prevents visual chaos and creates a clear hierarchy. The accent color is the eye-catcher — use it at focal points (eyes, weapon, belt buckle).

## 2. Color Temperature

### Warm vs Cool in Practice

| Temperature | Colors | Emotional Signal | Lighting Role |
|------------|--------|-----------------|---------------|
| **Warm** | Red, orange, yellow | Energy, danger, passion, life | Highlights, direct light, fire |
| **Cool** | Blue, violet, green | Calm, mystery, death, magic | Shadows, ambient light, moonlight |
| **Neutral** | Grey, brown, desaturated earth | Grounding, realism, fatigue | Transition zones, base tones |

### Temperature in Lighting (Critical for 3D)

The standard approach for realistic character lighting:

| Zone | Temperature | Why |
|------|------------|-----|
| **Highlights** | Warm (yellow-orange tinted) | Simulates sunlight or artificial warm light |
| **Midtones** | Local color (the "true" color) | Character's actual palette |
| **Terminator** (light-shadow edge) | Warmest, most saturated | Blood near skin surface; light diffusing through tissue |
| **Shadows** | Cool (blue-purple tinted) | Ambient sky light fills shadows; opposite of warm key light |
| **Reflected light** | Opposite of key light temperature | Bounce from environment; prevents dead-flat shadows |

### Subsurface Scattering (SSS) in Skin

Only ~6% of skin reflectance is direct; **94% comes from subsurface scattering**. Light penetrates skin, scatters through blood/tissue/fat, and exits tinted warm.

| Skin Area | SSS Behavior | Color Shift |
|-----------|-------------|-------------|
| Thin skin (ears, nostrils, fingers) | Maximum SSS | Bright warm red-orange glow when backlit |
| Cheeks, nose tip | High SSS + blood flow | Warm pink-red |
| Forehead | Moderate SSS + bone proximity | Lighter, more yellow |
| Eye sockets | Low SSS, deep cavity | Cooler, more blue-purple |
| Neck/chin underside | Low light, shadow | Cool green-grey |

## 3. Color Variation Across the Body

### The Protrusion/Cavity Rule

| Surface Type | Color Behavior | Reason |
|-------------|---------------|--------|
| **Protrusions** (cheekbones, nose, brow, knuckles) | Lighter, warmer, more saturated | Catch more light + blood closer to surface |
| **Cavities** (eye sockets, under chin, armpits, crevices) | Darker, cooler, more desaturated | Ambient occlusion + less blood visibility |
| **Transition zones** (joints, fold lines) | Warmer, redder | Skin stretches thin over joints; blood visible |
| **Extremities** (ear tips, fingertips, nose tip) | Redder/pinker | Blood concentration + thin skin |

### Body Region Color Map (Human Base)

| Region | Hue Shift From Base |
|--------|-------------------|
| Forehead | +yellow, lighter |
| Cheeks | +red, +pink (warm) |
| Nose | +red at tip |
| Lips | +red, darker value |
| Chin | slightly cooler |
| Neck | cooler, more grey-green |
| Chest | close to base, slightly warm |
| Hands (dorsal) | cooler, veins show blue-green |
| Knuckles | +red, lighter |
| Elbows, knees | +dark, +warm, rougher texture |

## 4. Fantasy Race Skin Palettes

### Goblin

| Role | Hex | Description |
|------|-----|-------------|
| Base skin | `#6B8E4E` | Muted olive-green |
| Shadow | `#3D5A2E` | Dark forest green |
| Highlight | `#8FAF6E` | Light yellow-green |
| Warm accent (joints, ears) | `#7A6B3D` | Ochre-brown |
| Eye | `#C9B82E` or `#B33A2E` | Yellow or red |

### Orc

| Role | Hex | Description |
|------|-----|-------------|
| Base skin | `#5A6B3D` | Dark olive-brown-green |
| Shadow | `#3A4428` | Deep murky green |
| Highlight | `#7A8B5A` | Muted sage |
| Warm accent (scars, lips) | `#8B5A3D` | Burnt sienna |
| Eye | `#B33A2E` or `#D4A82E` | Red or amber |

### Elf

| Role | Hex | Description |
|------|-----|-------------|
| Base skin | `#E8D5C0` | Warm ivory |
| Shadow | `#C4A88E` | Soft warm brown |
| Highlight | `#F5EDE5` | Near-white warm |
| Cool shadow | `#B8A0B8` | Lavender tint in deep shadows |
| Eye | `#4A8BB8` or `#6BAF6E` | Blue or green |

### Dwarf

| Role | Hex | Description |
|------|-----|-------------|
| Base skin | `#D4A882` | Ruddy tan |
| Shadow | `#8B6B4A` | Warm dark brown |
| Highlight | `#E8C8A8` | Light peach |
| Warm accent (nose, cheeks) | `#C4684A` | Strong red (weathered/ruddy) |
| Eye | `#6B5A3D` or `#4A6B8B` | Brown or blue-grey |

### Dark Elf / Drow

| Role | Hex | Description |
|------|-----|-------------|
| Base skin | `#4A3D5A` | Deep purple-grey |
| Shadow | `#2E2840` | Near-black purple |
| Highlight | `#7A6B8B` | Lavender-grey |
| Warm accent (lips, joints) | `#6B3D5A` | Dark magenta |
| Eye | `#D42E2E` or `#F5F5F5` | Red or white |

## 5. Palette Recipes for Common Character Types

### Recipe: Dark Fantasy Warrior (5 colors)

```
Primary (60%):  #2E2E2E  — Charcoal armor/clothing
Secondary (30%): #5A3D2E  — Dark leather brown
Accent 1 (5%):  #8B2E2E  — Blood red (trim, eyes, gems)
Accent 2 (3%):  #D4A82E  — Tarnished gold (buckles, runes)
Accent 3 (2%):  #F5EDE5  — Bone white (teeth, skull motifs)
```

### Recipe: Forest Ranger / Druid (5 colors)

```
Primary (60%):  #4A5A3D  — Forest green
Secondary (30%): #8B7A5A  — Natural leather tan
Accent 1 (5%):  #2E4A2E  — Dark moss
Accent 2 (3%):  #C4A868  — Warm gold (clasps, embroidery)
Accent 3 (2%):  #D4E8D4  — Pale green glow (magic)
```

### Recipe: Fire Mage / Warlock (5 colors)

```
Primary (60%):  #3D2E4A  — Deep purple robes
Secondary (30%): #2E2E2E  — Black trim and undershirt
Accent 1 (5%):  #D44A2E  — Flame orange (runes, effects)
Accent 2 (3%):  #F5C82E  — Bright yellow (fire core)
Accent 3 (2%):  #F5EDE5  — Hot white (spell glow)
```

### Recipe: Ice / Frost Character (5 colors)

```
Primary (60%):  #C4D4E8  — Pale ice blue
Secondary (30%): #F5F5F5  — Snow white
Accent 1 (5%):  #4A8BB8  — Deep glacier blue
Accent 2 (3%):  #2E5A7A  — Dark frost
Accent 3 (2%):  #B8E8F5  — Cyan glow (magic)
```

### Recipe: Undead / Necromancer (5 colors)

```
Primary (60%):  #3D3D2E  — Decayed grey-green
Secondary (30%): #2E2E2E  — Black shroud
Accent 1 (5%):  #6BAF4A  — Sickly green glow
Accent 2 (3%):  #5A3D2E  — Dried blood brown
Accent 3 (2%):  #D4D4C4  — Exposed bone
```

## 6. Art Direction Color Checklist

- [ ] Palette follows 60-30-10 distribution
- [ ] No more than 5 distinct hues per character (excluding value/saturation variations)
- [ ] Warm highlights, cool shadows (or justified reversal)
- [ ] Skin has color variation — not a single flat tone
- [ ] Accent color placed at focal point (eyes, weapon, key accessory)
- [ ] Values read in greyscale (squint test)
- [ ] Palette matches intended mood (dark fantasy = muted/desaturated; stylized = saturated/clean)
- [ ] Character pops against intended background color
- [ ] SSS considerations included in skin shader direction
