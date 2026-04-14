---
last_updated: 2026-04-14
confidence: high
sources: ["Sketchfab Asset Database", "ArtStation Industry Standards", "Color Theory & Mood Boards", "Reference Anatomy Resources"]
---

# Reference Gathering

Strategic reference gathering accelerates concept planning. Effective refs convey style direction, proportion standards, material palettes, and lighting precedents without building from scratch.

## Reference Platform Comparison

| Platform | Best For | Quality | Cost | Search |
|----------|----------|---------|------|--------|
| **Sketchfab** | 3D models, topology study | High | Free/paid | Excellent filters |
| **ArtStation** | Concept art, lighting, style | Excellent | Free | Artist portfolios |
| **Pinterest** | Mood boards, color, composition | Variable | Free | Visual search |
| **CGTalk** | Professional workflows, technical | High | Free | Forum archives |
| **Behance** | Design direction, branding | Excellent | Free | Curated collections |
| **Google Images** | Quick photographic refs | Variable | Free | Limited filters |
| **Photo libraries** (Unsplash, Pexels) | Real-world texture, lighting | Good | Free | Limited 3D |

## Sketchfab Reference Workflow

**Strategic search for topology/proportions:**

1. **Search query examples:**
   - "high poly human character male"
   - "mechanical hand rigged"
   - "product design render"
   - "animal anatomy quad topology"

2. **Filter by quality:**
   - Likes: 1000+ (popular, community-vetted)
   - Verified creator: prioritize
   - Polycount: review stat for complexity
   - Downloads: 100+ indicates professional use

3. **Inspect model:**
   - View wireframe (check topology flow)
   - Rotate 360° (check all angles)
   - Check vertex count (compare to budget)
   - Read model description (rigging info, optimization tips)

4. **Capture references:**
   - Screenshot 3 key angles (front, side, 3/4)
   - Note polycount, bone count, material count
   - Save artist credit for citations

**Sketchfab link structure:**
```
https://sketchfab.com/models/{id}-{name}
# Example: https://sketchfab.com/models/abc123xyz-character-knight
```

## ArtStation Style & Mood Research

**For concept direction, not modeling reference:**

1. **Search by style:**
   - "photorealistic character"
   - "stylized cartoon vehicle"
   - "sci-fi environment"
   - "fantasy prop design"

2. **Collection strategy:**
   - Create mood board (save 3-5 key artworks per mood)
   - Extract color palettes (use color picker tool)
   - Note lighting angles & composition
   - Screenshot 1x1080 resolution for reference

3. **Artist follow-up:**
   - Review artist CV for relevant expertise
   - Check their asset store (may offer usable props)
   - Note their software stack (Maya, Blender, etc.)

## Pinterest Mood Board Assembly

**Quick visual language building:**

1. **Create board:** e.g., "Character Design — Cyberpunk Detective"
2. **Pin categories:**
   - **Color**: 3-5 color swatch pins (palette extraction)
   - **Silhouette**: 3-4 character poses showing profile
   - **Material**: fabric, leather, metal textures
   - **Lighting**: hero shot examples showing desired light quality
   - **Environment**: background context

3. **Analysis pass:**
   - Identify dominant colors (primary, secondary, accent)
   - Note silhouette repeats (e.g., "all have defined waist")
   - Extract material priority (leather > metal > fabric)
   - Lighting pattern (3-point, rim-heavy, backlit)

4. **Export:**
   - Screenshot full board
   - Save individual 1080px pins as reference set
   - Document color hex codes from swatches

## Reference Analysis: Anatomy & Proportions

**For character/creature design:**

1. **Download anatomy reference:**
   - Male: Androgynous adult (7.5 head heights)
   - Female: Idealized adult (7.5-8 head heights)
   - Child: 6-6.5 head heights (head larger proportionally)
   - Creature: 4-6 head heights (varies by species)

2. **Measure key proportions:**
   - Head height: normalize to 1 unit
   - Torso: 2.5 units (neck to hips)
   - Legs: 3.5-4 units (hip to feet)
   - Arms: 3 units (shoulder to fingertips)
   - Hand: ~0.75 head height
   - Feet: ~1 head height

3. **Document variations:**
   - Note gender differences (wider hips, narrower shoulders on female)
   - Age variations (larger head on children, narrower legs on elderly)
   - Style variations (stylized: 6 heads; realistic: 8 heads)

4. **Create reference sheet:**
   - Front view (standing neutral pose)
   - Side view (same scale)
   - Detail views (hands, feet, face if relevant)
   - Proportion grid overlay (head-height units marked)

## Material & Texture Reference Gathering

**For color & surface planning:**

1. **Identify material types:**
   - Fabric (cotton, wool, leather, silk)
   - Metal (steel, aluminum, gold, bronze)
   - Plastic (matte, glossy, transparent)
   - Organic (skin, hair, plant)
   - Weathered variants (rust, patina, fading)

2. **Collect reference photos:**
   - Close-up 1-2 feet distance (shows texture detail)
   - Medium shot 3-5 feet (shows color in context)
   - Lighting variation (bright & shadow areas)
   - At least 2 examples per material type

3. **Analyze PBR channels:**
   - **Albedo/Diffuse:** Base color (no lighting)
   - **Roughness:** 0 = mirror, 1 = matte (observe specularity)
   - **Metallic:** 0 = non-metal, 1 = fully metal (check reflection behavior)
   - **Normal:** Surface detail (note micro-scratch direction)
   - **Ambient Occlusion:** Crevice darkness (check fold shadows)

4. **Document specifications:**
   ```
   Material: Worn Leather
   Albedo: RGB(139, 90, 50) — brownish-tan
   Roughness: 0.6 (slightly scuffed, not shiny)
   Metallic: 0.0 (not metallic)
   Normal detail: Light scratches, uniform grain
   Wear pattern: Darker in creases, lighter on raised edges
   Real-world example: Vintage leather jacket
   ```

## Lighting Reference Collection

**For mood & technical setup:**

1. **Screenshot hero shot lighting:**
   - Capture 3-view render (front, side, 3/4)
   - Note shadow direction (indicates light position)
   - Estimate color temperature (warm/cool ratio)
   - Measure shadow depth (high-key vs. dramatic)

2. **Reference catalog:**
   - **Product lighting:** Apple, luxury brands (studio setup refs)
   - **Character lighting:** AAA game trailers (cinematic standards)
   - **Environment lighting:** Architectural viz firms (HDRI+key light)
   - **VFX:** Blender benchmark files, Cycles documentation

3. **Analyze lighting setup:**
   - Estimate key light angle (where is shadow falling?)
   - Fill intensity (shadow details visible = softer fill)
   - Rim presence (is edge of subject highlighted?)
   - Background handling (is background lit or dark?)

## Color Palette Extraction Workflow

**From reference images:**

1. **Tool:** Use color picker (Chrome DevTools, Photoshop eyedropper, online color.adobe.com)
2. **Extract 5 colors:**
   - Primary: dominant color (40% of palette)
   - Secondary: 2nd most common (30%)
   - Accent 1: detail highlight (15%)
   - Accent 2: shadow or contrast (10%)
   - Neutral: black/white/gray (5%)

3. **Document in Hex:**
   ```
   Primary:   #8B5A32 (warm brown)
   Secondary: #2C3E50 (cool dark)
   Accent 1:  #D4A574 (warm light)
   Accent 2:  #4A6FA5 (cool medium)
   Neutral:   #F5F5F5 (near-white)
   ```

4. **Test in Blender:**
   - Create 5 material spheres with extracted colors
   - Render under standard 3-point lighting
   - Verify palette feels cohesive

## Reference Organization System

**Keep refs organized & accessible:**

```
Project_Name/
├── references/
│   ├── anatomy/
│   │   ├── male_front.jpg
│   │   ├── male_side.jpg
│   │   └── male_detail_hands.jpg
│   ├── lighting/
│   │   ├── hero_shot_example.jpg
│   │   ├── 3point_setup.jpg
│   │   └── hdri_comparison.jpg
│   ├── materials/
│   │   ├── leather_worn.jpg
│   │   ├── metal_brushed_steel.jpg
│   │   └── fabric_cotton_white.jpg
│   ├── color_palettes/
│   │   ├── mood_dark_scifi.txt  # hex codes
│   │   └── mood_warm_fantasy.txt
│   └── mood_board.jpg  # final compiled mood
├── color_extraction.txt  # Primary, Secondary, Accents 1-2, Neutral
└── reference_citations.txt  # Artist credits, source URLs
```

## Anti-Patterns in Reference Gathering

- **Too many references:** Paralyzes decision-making (limit to 3-5 per category)
- **Mismatched styles:** Mixing photorealism with stylization (pick ONE direction)
- **Ignoring proportions:** Assuming proportions without measuring (always document key ratios)
- **Oversaturated mood board:** Too many colors dilutes palette (stick to 5-color rule)
- **No lighting analysis:** Copying renders without understanding light setup (always sketch light position)
- **Using copyrighted art as base:** Trace/copy without understanding (learn from refs, create original)

## Reference Gathering Checklist

- [ ] 3-5 style refs (ArtStation, Pinterest mood board)
- [ ] 2-3 anatomy refs with proportions documented (front + side)
- [ ] 2-3 material refs per key surface (close-up, medium, lit variants)
- [ ] 1-2 lighting setup refs (note angles, color temp, shadows)
- [ ] Color palette extracted (5 colors, hex codes)
- [ ] Reference folder organized & cited
- [ ] Wireframe/topology refs downloaded (Sketchfab high-poly examples)
- [ ] Final mood board compiled & approved by stakeholder

## Professional Reference Sources

- **High-end 3D:** Sketchfab Verified Creator, Artstation (search by industry: "film", "game", "vfx")
- **Photography:** Unsplash, Pexels (free), Shutterstock/Getty (professional)
- **Concept Art:** Artstation, Behance, CTG (Character Design Research)
- **Technical Standards:** Blender Manual, Maya Documentation, Autodesk Tutorials
- **Animation Principles:** AnimationMentor video library, 12principles.com
