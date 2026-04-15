---
last_updated: 2026-04-14
refined_by: knowledge-sharpener (Opus 4.6)
confidence: high
sources:
  - https://vero.agency/blog/how-to-evaluate-high-quality-renderings
  - https://endesign.co/how-to-evaluate-the-quality-of-3d-renderings/
  - https://vrayschool.com/appealing-3d-render-checklist/
  - https://alpha3d.io/news/why-most-ai-generated-3d-models-fail-in-real-time-engines
  - https://geometryos.com/blog/101-why-ai-generated-3d-assets-fail-in-production/
  - https://www.sloyd.ai/blog/common-mistakes-when-creating-3d-models-from-images
  - https://learn.ncartmuseum.org/wp-content/uploads/2019/01/Feldman-Method-of-Art-Criticism_0.pdf
  - https://www.meshy.ai/blog/ai-texture-editing
---

# Art Critique Methodology

## 1. The SPMLC Evaluation Framework

Evaluate every 3D character render in this exact order. Higher-priority items must be fixed before lower ones — there is no point polishing materials on a character with broken proportions.

### Priority Order (Fix From Top Down)

| # | Category | Weight | Fix First? |
|---|----------|--------|------------|
| 1 | **S**ilhouette | 25% | YES — everything else fails if silhouette is unreadable |
| 2 | **P**roportions | 25% | YES — wrong proportions make everything else look wrong |
| 3 | **M**aterials & Surface | 20% | After silhouette + proportions are correct |
| 4 | **L**ighting & Mood | 15% | After materials — bad lighting hides good work |
| 5 | **C**omposition & Presentation | 15% | Final polish — camera angle, background, framing |

## 2. Detailed Critique Checklist

### S — Silhouette (25%)

| Check | Pass Criteria | How to Test |
|-------|--------------|-------------|
| Recognizability | Character type identifiable from black silhouette | Screenshot > fill with black > can you tell what it is? |
| 4-direction read | Clear from front, side, back, 3/4 | Rotate model, screenshot each angle |
| Negative space | Visible gaps between arms and torso, between legs | No "blob" shapes — limbs separated |
| Unique feature read | Signature element (horns, weapon, tail) visible in outline | Check that key features break the silhouette |
| Scale at distance | Readable at 64px thumbnail | Resize screenshot to 64px and squint |

**Scoring:**
- 9-10: Instantly recognizable from any angle at any size
- 7-8: Readable but could use more distinction
- 5-6: Generic silhouette, could be multiple characters
- 1-4: Blob, no clear reads, broken outline

### P — Proportions (25%)

| Check | Pass Criteria | How to Test |
|-------|--------------|-------------|
| Head count | Matches intended character type (see proportion-systems.md) | Overlay head-unit grid on front view |
| Shoulder width | Matches personality (wide=strong, narrow=agile) | Measure in head-widths |
| Limb lengths | Arms reach mid-thigh, elbows at waist, knees at mid-leg | Compare against reference |
| Symmetry | Intentional asymmetry only | Mirror-flip test |
| Bone landmarks | Visible at correct positions | Check clavicle, acromion, elbow, knee, ankle |
| Muscle placement | Origins and insertions correct | Compare against ecorche reference |
| Weight & balance | Character looks like it can stand | Center of gravity over feet |

**Scoring:**
- 9-10: Anatomically sound for the style, all landmarks correct
- 7-8: Minor proportion issues (one limb slightly off)
- 5-6: Multiple proportion problems visible
- 1-4: Fundamentally broken anatomy

### M — Materials & Surface (20%)

| Check | Pass Criteria | How to Test |
|-------|--------------|-------------|
| Surface detail | Primary, secondary, and tertiary forms present | Zoom in: large shapes (primary), muscle/clothing folds (secondary), pores/scratches (tertiary) |
| Material variety | Different surfaces read differently (skin vs metal vs cloth) | Each material has distinct roughness/reflection |
| Color variation | No flat single-tone surfaces | Zoom into skin: hue shifts visible? |
| Texture resolution | No visible pixelation or stretching | Check UV seams and texture density |
| PBR correctness | Metals reflect environment, non-metals diffuse light | Metal test: is it reflective? Dielectric test: no pure black/white in albedo? |
| SSS in skin | Warm glow at thin areas (ears, nostrils, fingers) | Backlight test: does light bleed through thin geometry? |
| Wear and storytelling | Surface tells a story (scratches on armor, dirt on boots) | Does the character look lived-in or factory-fresh? |

**Scoring:**
- 9-10: Rich, varied surfaces with clear material separation
- 7-8: Good materials, minor flatness in some areas
- 5-6: Basic materials, lacks variation or detail
- 1-4: Flat, plastic-looking surfaces with no variation

### L — Lighting & Mood (15%)

| Check | Pass Criteria | How to Test |
|-------|--------------|-------------|
| Key light direction | Clear primary light source, consistent shadows | All shadows point same direction? |
| Fill light | Shadow areas not pure black (unless stylistic) | Can you see detail in shadows? |
| Rim/back light | Edge definition separating character from background | Character pops from background? |
| Color temperature | Warm highlights, cool shadows (or justified alternate) | Highlights warm-tinted, shadows cool-tinted? |
| Mood match | Lighting supports intended emotion | Dark fantasy = dramatic, high contrast; Friendly = soft, even |
| Shadow quality | Clean edges for hard light, soft edges for ambient | No jagged or artifacted shadows? |
| Focal point | Light draws eye to character's face/center of interest | Brightest area at the right spot? |

**Scoring:**
- 9-10: Cinematic lighting that enhances mood and form
- 7-8: Competent lighting, clear reads
- 5-6: Flat or default lighting, no mood
- 1-4: Contradictory light sources, blown out or too dark

### C — Composition & Presentation (15%)

| Check | Pass Criteria | How to Test |
|-------|--------------|-------------|
| Camera angle | Flattering angle for the character type | Hero = low angle; Creature = eye-level; Boss = extreme low |
| Framing | Character fills frame appropriately | Not too much dead space, not clipped |
| Background | Supports but doesn't compete with character | Background value/saturation lower than character? |
| Pose | Dynamic and personality-appropriate | Does the pose tell you who this character is? |
| Read direction | Viewer's eye flows through the composition | Test: where does your eye go first, second, third? |

## 3. How to Give Actionable Critique

### The Formula

Every critique item must follow this structure:

```
[WHAT] is wrong + [WHERE] specifically + [HOW MUCH] to change + [WHY] it matters
```

### Bad vs Good Critique Examples

| Bad (Vague) | Good (Actionable) |
|-------------|-------------------|
| "The head looks weird" | "Brow ridge needs 2cm more forward protrusion to match orc archetype; currently reads as human" |
| "Proportions are off" | "Legs are 0.5 head-units too long for a dwarf — reduce from 2.5 to 2.0 head-units" |
| "Materials look flat" | "Skin albedo needs 15% more saturation in the reds on cheeks and nose; currently reads as rubber" |
| "Lighting is bad" | "Key light is 45 degrees too high — move from 80 degrees to 35 degrees above eye level to avoid skull-like shadows under eyes" |
| "It doesn't look right" | "Silhouette reads as generic humanoid — add asymmetric shoulder armor (left side only, 20% larger than head) to break outline" |
| "Colors are wrong" | "Primary green (#4A5A3D) is too saturated for dark fantasy — reduce saturation by 20% to match muted palette target" |

### Critique Quantity Rules

| Iteration Stage | Max Critique Items | Focus |
|----------------|-------------------|-------|
| First review | 3 items maximum | Only SPMLC priorities 1-2 (silhouette + proportions) |
| Second review | 3 items maximum | Remaining proportion fixes + start materials |
| Third review | 2-3 items | Materials + lighting |
| Fourth review | 1-2 items | Polish: composition, fine details |
| Fifth review (final) | Accept or 1 critical item | Ship it or identify the one blocking issue |

## 4. Common Mistakes in AI-Generated 3D

### The Big 5 AI Failure Modes

| Problem | What It Looks Like | Root Cause | Fix Direction |
|---------|-------------------|------------|---------------|
| **Blobby forms** | Soft, melted geometry; no sharp edges or clear planes | AI averaging geometry; no bony landmarks | Add edge loops at anatomical landmarks; sharpen planes of the face |
| **Flat materials** | Single-tone surfaces, no roughness variation, plastic look | Uniform shader values; no hand-painted detail | Add roughness variation map; break up albedo with color zones |
| **Bad topology** | Shading artifacts, pinching at joints, triangles visible | AI mesh generation produces non-quad topology | Retopologize with quad-dominant flow; prioritize edge loops at deformation zones |
| **Primitive assembly** | Character looks like spheres + cylinders snapped together | AI builds from primitives without organic blending | Bridge primitives with smooth topology; add secondary forms between volumes |
| **Dead lighting** | Flat, shadowless renders; no sense of depth | Default scene lighting with no art direction | Set up 3-point light rig; add HDRI for reflections; adjust exposure |

### AI-Specific Texture Problems

| Problem | Fix Direction |
|---------|---------------|
| UV seams visible in texture | Reproject textures with seam blending |
| Tiling artifacts | Break tiling with secondary detail layer |
| Over-painted detail | Reduce painted detail, let geometry + lighting do the work |
| Color banding | Add noise/dithering to gradient areas |
| Inconsistent detail density | Establish texel density standard per material type |

## 5. The Iteration Flow

### Maximum 5 Iterations

```
Iteration 1:  SILHOUETTE + PROPORTIONS  →  "Is this the right character?"
Iteration 2:  PROPORTIONS refinement     →  "Does the anatomy work?"
Iteration 3:  MATERIALS + SURFACE        →  "Does it feel real/stylized correctly?"
Iteration 4:  LIGHTING + MOOD            →  "Does it evoke the right emotion?"
Iteration 5:  COMPOSITION + POLISH       →  "Is it presentation-ready?"
```

### Decision Points

| After Iteration | Decision |
|----------------|----------|
| 1 | If silhouette is fundamentally broken → restart from scratch |
| 2 | If proportions are 80%+ correct → proceed to materials |
| 3 | If materials read correctly → proceed to lighting |
| 4 | Score the render 1-10 in each category |
| 5 | Accept (score >= 7 average) or accept-with-notes (score 5-6) |

### Final Score Card Template

```
Character: [Name]
Style: [Dark Fantasy / Stylized / Realistic]
Iteration: [#/5]

| Category | Score (1-10) | Notes |
|----------|-------------|-------|
| Silhouette | _ | |
| Proportions | _ | |
| Materials | _ | |
| Lighting | _ | |
| Composition | _ | |
| **Overall** | **_** | |

Verdict: [APPROVED / NEEDS REVISION / ACCEPTABLE WITH NOTES]
Remaining issues: [if any]
```
