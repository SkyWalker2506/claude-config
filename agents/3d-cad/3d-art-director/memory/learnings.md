# Learnings

## 2026-04-14 — Knowledge Base Initial Fill (6 Topics)

### Key Findings During Research

1. **Shape language is universal** — Circle/square/triangle emotional mapping is consistent across all major design resources. The 60-70% dominant + 30-40% secondary shape blend is the practical rule for character design.

2. **Head-count system is the universal proportion language** — Every character type maps to a specific head count (goblin 3.5-4.5, dwarf 4.5-5.5, human 7-7.5, heroic 8, elf 8-9). This is the single most important number for art direction.

3. **The 60-30-10 color rule** translates directly to character palette design — 60% dominant body/clothing, 30% secondary, 10% accent at focal points. No more than 5 distinct hues per character.

4. **94% of skin reflectance is from subsurface scattering** (NVIDIA GPU Gems) — this means flat single-tone skin in 3D always looks wrong. Color variation across the body (warmer on protrusions, cooler in cavities) is not optional.

5. **SPMLC priority order for critique** (Silhouette > Proportions > Materials > Lighting > Composition) — fixing items out of order wastes iterations. No point polishing materials on broken proportions.

6. **AI-generated 3D has 5 consistent failure modes** — blobby forms, flat materials, bad topology, primitive assembly, dead lighting. These are predictable and each has specific fix directions.

7. **Polycount budgets vary 10x between mobile and AAA** — mobile hero character: 5K-10K tris; AAA hero: 80K-150K tris. Art direction must set budget before any work starts.

8. **The 4-direction silhouette test is non-negotiable** — a character that only reads from the front is incomplete. Minimum score 7/10 across all 4 directions (front, side, back, 3/4).

9. **Dark fantasy style has specific material rules** — everything weathered, nothing clean; roughness values 0.5+ for metals, 0.7+ for organics; magic effects are the ONLY high-saturation elements.

10. **Style consistency requires an art bible** — shared shader library, texel density standard, proportion relationships between races, and a color palette constraint. Without these, multi-asset projects drift visually.

### Cross-References Between Knowledge Files

- character-design-principles.md Section 5 (Fantasy Archetypes) references proportion-systems.md head counts
- color-theory.md Section 4 (Fantasy Race Palettes) provides hex codes for races defined in character-design-principles.md
- art-critique.md Section 2 (Proportions check) references proportion-systems.md for landmarks
- style-guides.md Section 4 (Game-Ready) defines polycount budgets referenced in art-critique.md
- silhouette-analysis.md Section 5 (Race Silhouettes) maps to shape language in character-design-principles.md
