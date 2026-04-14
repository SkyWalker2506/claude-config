# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-14 — Knowledge Sharpening Session

### Composition & Framing
**Source:** Film & TV Production Standards, 3D Art Direction Best Practices

**Learned:**
- Rule of thirds is not "subject at center" — subject goes on intersection points (1,3,7,9) or grid lines (2,4,6,8)
- Depth layering math: foreground 0.5-2m, subject 2-5m (in focus), background 5m+ (DoF blur)
- Focal point isolation via 5 channels: size (40-50%), light (brightest), color (saturated), detail (high poly), silhouette (unique)

**Application:** When planning composition, always use 3+ depth planes and check silhouette test (wireframe view). Verify focal point placement vs. rule-of-thirds grid overlay in Blender viewport.

---

### Camera & Lens Standards
**Source:** Cinematography Standards, Blender Documentation

**Learned:**
- Focal length directly affects perceived scale and distortion
- 50mm is portrait standard (minimal distortion) vs. 85mm for closeup vs. 35mm for wide context
- Hero shot low-angle formula: 30° below eye level + side key light = imposing read
- Depth-of-field F-stop scale: 2.8 (shallow, intimate) → 5.6 (moderate) → 16 (deep, technical)
- Turntable timing: 8 seconds @ 24fps = 192 frames for smooth 360° orbit

**Application:** Always specify focal length in camera plan (50mm default, 85mm+ for product detail). Validate hero shot angle + key light position pairing. Blender orbital keyframe setup: frame 1→0°, frame 192→360°, linear interpolation.

---

### Professional Lighting Setup
**Source:** 3-Point Lighting Theory, PBR Rendering, Cinematography

**Learned:**
- Key + Fill + Rim math is strict: Key (300W) → Fill (120W = 40%) → Rim (200W = 67%)
- Color temp progression creates depth: warm key (3000K) → cool fill (5000K) → warm rim (2800K)
- Shadow ratio rule: bright areas 3-4x brighter than shadows (film standard for visual depth)
- HDRI workflow: Texture → Mapping → Background → Output node setup in World Shader Editor
- Asset-specific setups vary: character (soft fill, flattering) vs. product (clean isolation, 50% rim) vs. vehicle (curve showcase, bright rim)

**Application:** Use Blender Area lights for 3-point setup (soft shadows). Verify shadow ratio with rendered preview (Shift+Z). Document color temps in hex for consistency. HDRI multiplier typically 0.5-1.5 for balanced indirect lighting.

---

### Reference Gathering Workflows
**Source:** Sketchfab Asset Database, ArtStation Industry Standards, Color Theory

**Learned:**
- Sketchfab filters: likes 1000+, verified creator, polycount visible = quality refs
- ArtStation 5-color palette rule: Primary (40%) + Secondary (30%) + Accent1 (15%) + Accent2 (10%) + Neutral (5%)
- Anatomy proportions: adult 7.5 head-heights, child 6, creature 4-6 (measure from ref, don't guess)
- PBR analysis framework: albedo (base color) → roughness (0=mirror, 1=matte) → metallic (0/1) → normal (scratch direction) → AO (crevice darkness)
- Material documentation template: name + RGB values + roughness/metallic values + wear pattern + real-world example

**Application:** Create reference sets organized by category (anatomy/lighting/materials/color). Extract color hex codes to verify palette coherence. Document proportions in head-height units for anatomy refs. Screenshot 3 angles of Sketchfab models (front/side/3/4 view).

---

### Platform Specialization
**Learned:**
- Sketchfab = topology study, polycount validation, artist credit tracing
- ArtStation = style direction, concept exploration, mood precedent
- Pinterest = quick color palettes, silhouette patterns, composition examples
- Professional sources: CG-focused (Behance 3D collections), anatomy (AnimationMentor, 12principles.com), lighting (Blender Manual → Lighting)

**Application:** Route research tasks by goal. Texture detail? Sketchfab closeups. Character pose ideas? ArtStation artist portfolios. Quick mood assembly? Pinterest collections. Never rely on single platform.

---

### Decision Trees & Anti-Patterns
**Learned:**
- Composition anti-pattern: dead-center subject = boring, use rule-of-thirds
- Lighting anti-pattern: single light source = harsh, unnatural (always 3+ lights)
- Camera anti-pattern: extreme FOV <20mm or >200mm for character unless intentional (distorts proportions)
- Reference anti-pattern: too many refs paralyzes (limit to 3-5 per category)
- Tone coherence anti-pattern: mismatched styles (photorealism + stylization) = confused direction

**Application:** Use decision trees before execution (Q1: what's hero? Q2: emotional tone? Q3: constraint?). Review anti-patterns list before finalizing plans. Enforce 3-5 ref limit per category to accelerate decision-making.
