---
last_updated: 2026-04-14
knowledge_filled: true
total_topics: 4
coverage: complete
confidence: high
---

# Knowledge Index — 3D Concept Planner

Concept planning bilgisi. Her dosya copy-paste hazir kod, profesyonel standartlar, ve karar matrisleri icerir.

## Topics

### 1. [3D Scene Composition](3d-scene-composition.md)
**Scope:** Rule of thirds, focal point, depth layering, negative space, composition checklists.

**Key skills:**
- Rule-of-thirds grid placement (intersection vs. grid lines)
- Depth plane separation (foreground/subject/background)
- Visual hierarchy via size, light, color, detail
- Silhouette testing for instant read
- Blender guide overlays (composition guides, frame selected)

**When to use:** Scene layout planning, camera framing before render, composition troubleshooting.

**Outputs:** Composition checklist, depth layer assignments, focal point placement confirmed.

---

### 2. [Camera Angle Patterns](camera-angle-patterns.md)
**Scope:** FOV/focal length decision matrix, hero shot patterns, turntable setup, orthographic vs. perspective.

**Key skills:**
- Focal length selection (35mm wide → 85mm portrait → 135mm telephoto)
- Hero shot patterns (low angle + side light, eye level + 3/4, elevated + tilt, closeup + DoF)
- 360° orbital turntable setup with timing (8 sec @ 24fps = 192 frames)
- Camera positioning decision tree (hero type → emotion → constraint)
- Blender camera setup: focal length, depth of field, frame preview

**When to use:** Camera planning before staging, hero shot design, product viz setup.

**Outputs:** Camera angle diagram, focal length specs, depth-of-field settings, frame preview approved.

---

### 3. [Lighting Setup Guide](lighting-setup-guide.md)
**Scope:** 3-point lighting (key/fill/rim), Blender light types, color temperature, HDRI setup, lighting for character/product/vehicle/environment.

**Key skills:**
- 3-point lighting math (key 300W, fill 120W = 40%, rim 200W = 67%)
- Key light positioning (45° front-side, warm 3000K)
- Fill light (opposite/center, 30-50% key, neutral 5000K)
- Rim light (behind/side, hard edges, 50-100% key)
- Color temp progression: warm key → cool fill → warm rim
- HDRI setup with node tree (Texture → Mapping → Background → Output)
- Asset-specific setups: character (soft, flattering), product (clean, isolated), vehicle (curves showcase), environment (HDRI primary)

**When to use:** Lighting plan before rendering, mood/tone establishment, shadow definition checks.

**Outputs:** 3-point light diagram, energy values, color temps, HDRI selection, shadow ratio confirmed (3-4:1).

---

### 4. [Reference Gathering](reference-gathering.md)
**Scope:** Platform comparison (Sketchfab/ArtStation/Pinterest), anatomy proportions, material analysis, color palette extraction, lighting refs.

**Key skills:**
- Sketchfab workflow: search, filter by likes/polycount, inspect topology, capture 3-angles
- ArtStation mood boards: extract 5 colors (primary/secondary/accent1/accent2/neutral in hex)
- Pinterest assembly: 3-5 refs per category (color/silhouette/material/lighting/environment)
- Anatomy proportions: head-height units (adult 7.5, child 6, creature 4-6)
- PBR material analysis: albedo, roughness, metallic, normal, AO
- Lighting analysis: sketch light positions, estimate color temp, shadow depth

**When to use:** Pre-production research, style direction confirmation, color palette review, proportions validation.

**Outputs:** Reference set (3-5 per category), mood board, color palette (hex codes), proportions documented, citation file.

---

## Usage Pattern

1. **Read this file** — understand available topics
2. **Load relevant knowledge file** — based on current task
3. **Extract decision matrix or checklist** — for hands-on guidance
4. **Use code examples** — copy-paste Blender Python when applicable
5. **Document decisions** — update memory/sessions.md with outcomes

## Quick Search

| Need | Read |
|------|------|
| Composition framing | 3d-scene-composition.md § Rule of Thirds, Focal Point Hierarchy |
| Camera FOV/angle | camera-angle-patterns.md § Focal Length Decision Tree |
| Lighting setup | lighting-setup-guide.md § 3-Point Lighting Foundation + Code Examples |
| Style/mood/colors | reference-gathering.md § Color Palette Extraction, ArtStation Workflow |
| Anatomy proportions | reference-gathering.md § Anatomy & Proportions |
| Material specs | reference-gathering.md § Material & Texture Reference Gathering |

## Coverage Status

- [x] 3D Scene Composition — complete, 600+ words, decision matrix, code examples
- [x] Camera Angle Patterns — complete, 700+ words, hero patterns, Blender setup code
- [x] Lighting Setup Guide — complete, 900+ words, 3-point + HDRI, Blender Python examples
- [x] Reference Gathering — complete, 1000+ words, platform workflows, color extraction, checklists

**Total:** 3200+ words, 20+ decision matrices/checklists, 8+ Blender code examples, professional standards throughout.
