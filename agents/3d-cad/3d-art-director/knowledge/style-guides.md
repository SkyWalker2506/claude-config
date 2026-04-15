---
last_updated: 2026-04-14
refined_by: knowledge-sharpener (Opus 4.6)
confidence: high
sources:
  - https://aesthetics.fandom.com/wiki/Dark_Fantasy
  - https://medium.com/@ivotenvoorde/mastering-dark-fantasy-art-bbd0a53c4e61
  - https://www.inferaurum.com/epic-dark-realism/
  - https://www.whizzystudios.com/post/maintaining-consistency-across3d-character-lineups
  - https://opengameart.org/forumtopic/maintaining-a-consistent-art-style
  - https://dvnc.itch.io/art-bible-template
  - https://threedium.io/3d-model/game-ready
  - https://3d-ace.com/blog/polygon-count-in-3d-modeling-for-game-assets/
  - https://polycount.com/discussion/152508/how-many-polygons-should-a-game-ready-assets-have
---

# Style Guides

## 1. Dark Fantasy Style

### Visual DNA

| Attribute | Specification |
|-----------|--------------|
| **Color palette** | Muted, desaturated; blacks, greys, deep reds, sickly greens, dark blues |
| **Saturation** | Low (30-50% of max); only magic effects get high saturation |
| **Value range** | High contrast — deep darks and selective highlights, not uniformly dark |
| **Lighting** | Dramatic chiaroscuro; single strong key light, deep shadows |
| **Light sources** | Torches (warm orange), moonlight (cold blue), magic (accent color), embers |
| **Texture quality** | Gritty, worn, weathered — nothing looks new or clean |
| **Surface detail** | Battle damage, rust, dirt, blood stains, patina, moss growth |
| **Material feel** | Rough metals, cracked leather, tattered cloth, pitted stone |
| **Proportions** | Semi-realistic to realistic (7-8 heads); slight exaggeration allowed |
| **Mood** | Ominous, oppressive, dangerous, ancient |

### Dark Fantasy Material Rules

| Material | Roughness | Reflectivity | Detail Notes |
|----------|-----------|-------------|--------------|
| Iron/steel armor | 0.5-0.8 | Low-medium | Scratched, dented, rust at edges |
| Leather | 0.7-0.9 | Very low | Cracked, stained, stitched with thick thread |
| Cloth/fabric | 0.85-1.0 | None | Frayed edges, muted dyes, dirt accumulation |
| Skin (human) | 0.4-0.6 | Low (SSS) | Scars, dirt, sunburn, weathering |
| Skin (undead) | 0.6-0.8 | Very low | Grey-green base, visible veins, decay |
| Bone | 0.6-0.8 | Low | Yellowed, cracked, stained |
| Gold/jewelry | 0.2-0.4 | Medium-high | Tarnished, not polished; scratched, age patina |
| Magic effects | 0.0-0.1 | High emission | The ONLY bright, saturated color in scene |

### Dark Fantasy Color Ranges

```
Armor/metal:    #2E2E2E to #5A5A5A  (charcoal to mid grey)
Leather:        #3D2E1E to #5A4A3D  (dark brown range)
Cloth:          #2E2E3D to #4A3D3D  (dark blue-grey to dark red-grey)
Skin (human):   #A88B6B to #D4A882  (desaturated warm — less pink than normal)
Blood/accent:   #6B1E1E to #8B2E2E  (dark desaturated red)
Magic glow:     Style-dependent (green=necromancy, blue=arcane, red=blood)
Environment:    #1E2E1E to #3D3D3D  (murky greens and greys)
```

## 2. Stylized / Cartoon Style

### Visual DNA

| Attribute | Specification |
|-----------|--------------|
| **Color palette** | Bright, saturated; clear primary and secondary colors |
| **Saturation** | High (60-90%); flat fills with minimal gradient |
| **Value range** | Medium contrast; shadows are lighter than realistic, darks are not pure black |
| **Lighting** | Soft, even; 2-step or 3-step cel shading; minimal harsh shadows |
| **Texture quality** | Clean, smooth; hand-painted look or flat color |
| **Surface detail** | Minimal — rely on shape and color, not surface noise |
| **Material feel** | Smooth plastics, clean fabrics, polished metals |
| **Proportions** | Exaggerated (4-6 heads); big heads, big hands, small waists |
| **Mood** | Cheerful, energetic, whimsical |

### Stylized Material Rules

| Material | Roughness | Reflectivity | Detail Notes |
|----------|-----------|-------------|--------------|
| Skin | 0.6-0.8 | Very low | 2-3 tones only; crisp shadow edge |
| Metal | 0.3-0.5 | Medium | Clean with subtle spec highlight, not photorealistic |
| Cloth | 0.8-1.0 | None | Flat color with painted fold hints |
| Hair | 0.5-0.7 | Low | Chunky planes, not individual strands |
| Eyes | 0.1-0.2 | High | Large, expressive, anime-influenced |
| Wood | 0.7-0.9 | Very low | Hand-painted grain, exaggerated rings |

### Stylized Color Rules

- Maximum 4-5 colors per character (including skin)
- Each color at 60-80% saturation
- Shadows = base color shifted toward complement (not just darkened)
- No pure black outlines in 3D (use dark desaturated version of local color)
- Highlight = base color + white + slight warm shift

## 3. Realistic Style

### Visual DNA

| Attribute | Specification |
|-----------|--------------|
| **Color palette** | Natural, true-to-life; reference photography |
| **Saturation** | Moderate (40-60%); matches real-world observation |
| **Value range** | Full range with natural falloff; no crushed blacks or blown highlights |
| **Lighting** | Physically based; HDR environment + directional |
| **Texture quality** | High-resolution (4K+); scanned or photo-referenced |
| **Surface detail** | All three form levels: primary, secondary, tertiary |
| **Material feel** | Accurate PBR values per real-world material |
| **Proportions** | 7-7.5 heads; anatomically correct |
| **Mood** | Neutral — driven by lighting and context, not stylization |

### Realistic PBR Reference Values

| Material | Albedo Range | Roughness | Metallic | IOR |
|----------|-------------|-----------|----------|-----|
| Human skin | 0.35-0.6 (value) | 0.3-0.5 | 0.0 | 1.4 |
| Steel | 0.5-0.7 (metallic albedo) | 0.2-0.5 | 1.0 | N/A |
| Leather | 0.05-0.3 (dark brown range) | 0.5-0.8 | 0.0 | 1.5 |
| Cotton fabric | 0.2-0.6 (varies by dye) | 0.8-1.0 | 0.0 | 1.5 |
| Wood | 0.1-0.4 | 0.5-0.8 | 0.0 | 1.5 |
| Gold | 1.0, 0.76, 0.34 (RGB) | 0.1-0.3 | 1.0 | N/A |
| Gemstone | 0.05-0.2 | 0.0-0.1 | 0.0 | 1.5-2.4 |

### Realistic Skin Shader Checklist

- [ ] SSS enabled with warm scatter color (~red-orange)
- [ ] SSS radius: 1.0-3.0mm for realistic scale
- [ ] Separate diffuse, specular, and SSS components
- [ ] Micro-normal map for skin pores (tertiary detail)
- [ ] Color variation map (see color-theory.md, Section 3)
- [ ] Cavity/AO map darkening crevices
- [ ] Specular map brighter on oily zones (forehead, nose)

## 4. Game-Ready Constraints

### Polycount Budgets by Platform

| Platform | Character LOD0 (Hero) | Character LOD0 (NPC) | Background Prop | Notes |
|----------|----------------------|---------------------|-----------------|-------|
| **Mobile (low)** | 5K-10K tris | 2K-5K tris | 500-1K tris | Minimal bone count (30-50) |
| **Mobile (high)** | 10K-20K tris | 5K-10K tris | 1K-3K tris | Modern phones (2024+) |
| **PC / Console (indie)** | 15K-30K tris | 5K-15K tris | 2K-5K tris | Standard Unity/UE budget |
| **PC / Console (AA)** | 30K-60K tris | 15K-30K tris | 5K-10K tris | Mid-budget production |
| **AAA** | 80K-150K tris | 30K-60K tris | 10K-30K tris | Unreal Engine 5 / Nanite |
| **Cinematic** | 200K+ tris | 100K+ tris | Unlimited | Offline rendering only |

### Texture Size Standards

| Asset Type | Minimum | Standard | High Quality |
|-----------|---------|----------|-------------|
| Hero character (full body) | 1024x1024 | 2048x2048 | 4096x4096 |
| NPC character | 512x512 | 1024x1024 | 2048x2048 |
| Weapon / held prop | 512x512 | 1024x1024 | 2048x2048 |
| Environment prop | 256x256 | 512x512 | 1024x1024 |
| Texture sets per character | 1-2 | 2-4 | 4-6 |

### LOD (Level of Detail) Tiers

| LOD Level | Distance | Tri Reduction | Notes |
|-----------|----------|---------------|-------|
| LOD0 | Close-up / hero | 100% (full) | All detail visible |
| LOD1 | Mid-range (5-15m) | 50% of LOD0 | Remove tertiary detail |
| LOD2 | Far (15-30m) | 25% of LOD0 | Simplified silhouette only |
| LOD3 | Very far (30m+) | 10% of LOD0 | Billboard or impostor |

### Texture Map Checklist (Game-Ready)

- [ ] Albedo / Base Color (sRGB)
- [ ] Normal Map (tangent space, OpenGL or DirectX per engine)
- [ ] Roughness / Smoothness (inverted between Unity and Unreal)
- [ ] Metallic (binary for most surfaces: 0 or 1)
- [ ] Ambient Occlusion (baked from high-poly)
- [ ] Emissive (if character has glowing elements)
- [ ] SSS / Thickness map (for skin, ears, thin geometry)

## 5. Style Consistency Across Multiple Assets

### The Art Bible Approach

An art bible defines the visual rules all assets in a project must follow. Key sections:

| Section | Defines | Why |
|---------|---------|-----|
| **Color palette** | Max hue range, saturation limits, value range | Prevents visual chaos between assets |
| **Proportion standard** | Head count, limb ratios, size relationships | A goblin next to a dwarf must look correct |
| **Detail density** | Texel density (px/cm), polycount range | All assets feel same "resolution" |
| **Material library** | Shared shaders, roughness ranges, reflection models | Same lighting behavior across all characters |
| **Edge treatment** | Hard vs soft edges, outline thickness, bevel width | Consistent stylization level |
| **Shape language** | Dominant shapes per faction/race | Visual grouping (all goblins share triangle language) |

### Consistency Checklist

| Test | How |
|------|-----|
| Scale test | Place all characters in same scene — do sizes feel correct? |
| Lighting test | Render all characters under identical lighting — do materials match? |
| Texel density test | All characters have same pixel density on equivalent surfaces |
| Silhouette lineup | Black silhouettes side by side — each one distinct? |
| Color harmony | All palettes plotted on same color wheel — do they work together? |
| Style match | Place stylized and realistic together — any outliers? |

### Cross-Asset Proportion Rules

| Relationship | Rule |
|-------------|------|
| Goblin : Human | 0.5-0.6x height; 1.2x relative head size |
| Dwarf : Human | 0.6-0.7x height; 1.5x shoulder width |
| Elf : Human | 1.05-1.15x height; 0.85x shoulder width |
| Orc : Human | 0.9-1.1x height; 1.4x shoulder width, 1.3x overall mass |
| Dragon-kin : Human | 1.2-2.0x height (highly variable) |
