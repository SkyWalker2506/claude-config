# Learnings

## 2026-04-14 — Knowledge Base Initial Fill (Opus 4.6)

### Key Findings from Research

1. **Metaball-to-Mesh Pipeline**: The critical step after metaball conversion is Decimate (ratio 0.5) followed by Smooth (factor 0.5, iter 3) followed by optional Voxel Remesh. Without Decimate applied, sculpt tools cannot deform the mesh.

2. **Displacement Strength Scale**: Organic character displacement lives in a narrow strength range:
   - Primary muscle: 0.08-0.20
   - Secondary detail: 0.03-0.08
   - Skin pores: 0.01-0.02
   - Anything above 0.25 looks artificial except for stone/rock creatures

3. **Musgrave vs Voronoi Division of Labor**:
   - Musgrave (FBM, scale 2-5) = muscle undulation, broad organic forms
   - Musgrave (Ridged, scale 8-15) = wrinkle lines, tendon ridges
   - Voronoi (Distance, scale 50-100) = skin pores
   - Voronoi (Distance Squared, scale 10-25) = scales, armor plates
   - Voronoi (Crackle, scale 5-12) = cracked stone/rock skin

4. **Mid-Level Strategy**: Default 0.5 is rarely optimal:
   - 0.55-0.65 for muscle (biased outward = more bulge than valley)
   - 0.5 for wrinkles (equal inward/outward)
   - 0.6 for warts/bumps (mostly raised surface)
   - 0.4 for scale patterns (raised plates with valleys between)

5. **Modifier Stack Order is Critical**:
   ```
   SubSurf > Primary Displace > Bone Displace > Multires > Secondary Displace > Pores > Wrinkles > Noise
   ```
   SubSurf MUST come before Multires. Large-scale displacement MUST come before fine-scale.

6. **Goblin Metaball Recipe**: 35 elements total; key differentiators from human:
   - Head radius 1.4x (0.065 vs human 0.04 relative)
   - Forward head offset (Y+0.04)
   - Ear elements need low stiffness (0.6-0.8) for pointed shape
   - Belly protrusion element added separately from chest
   - Spine hunch via backward upper-back element

7. **Head-Count Critical Numbers**:
   - Crotch is ALWAYS at half-height (3.75 / 7.5 for humans)
   - Elbows at navel height
   - Wrists at crotch height
   - Fingertips at mid-thigh
   - Foot length = approximately 1 head unit

8. **Form Language 70-20-10 Rule**: 70% dominant shape, 20% secondary, 10% accent. This is the key to making characters read with the intended personality.

9. **Golden Ratio Usage**: Follow Phi closely for beautiful characters (elf, angel). Break Phi deliberately for monstrous characters (goblin, troll). Partial Phi for interesting characters (orc, dwarf).

10. **Blender API Note**: `bpy.data.textures.new()` requires type as second arg. MetaElement properties: `co` (Vector), `radius` (float), `stiffness` (float), `type` (enum). DisplaceModifier: `texture` property accepts texture object directly.

### Sources Quality Assessment
- Blender API docs: Authoritative but sometimes blocked by 403; use search results + API knowledge
- Anatomy4Sculptors: Best artist anatomy resource
- Shape language articles: CG-Wire 2026 article most comprehensive
- Proportion data: Wikipedia body proportions + Proko tutorials most reliable
- Creature proportions: Synthesized from D&D references + game art conventions; less standardized than human anatomy
