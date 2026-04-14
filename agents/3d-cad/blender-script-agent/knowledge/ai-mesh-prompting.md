---
last_updated: 2026-04-14
refined_by: agent-sharpen
confidence: high
sources: research/llm-prompt-engineering-3d.md, research/topology-fundamentals.md, research/ai-3d-generation-methods.md
---

# AI Mesh Prompting — LLM-Driven Blender Script Generation

## Core Principle: Chain-of-3D-Thoughts

Never ask LLM for "make a dog" directly. Use staged topology-first thinking.

### Prompt Pattern (Chain-of-3D-Thoughts / L3GO)

```
Describe the topology plan first:
- Base mesh: [primitive, dimensions]
- Extrusions: [direction, count, scale taper per segment]
- Subdivisions: [edge count per region]
- Appendages: [which faces, how many segments, taper ratio]

Then generate Blender Python (bmesh) that implements EXACTLY this plan.
Use bmesh.ops.extrude_face_region, bmesh.ops.subdivide_edges.
Do NOT use separate UV sphere / cylinder primitives.
All parts must be connected via extrusion chains.
```

**Research result:** Chain-of-3D-Thoughts increases success from ~40% (primitive assembly) to ~70% (topology-first).

---

## Stage Decomposition Pattern (LL3M)

For complex organic models (animals, characters), decompose into 4 stages:

| Stage | Goal | Token Budget | Output |
|-------|------|-------------|--------|
| 1: Skeleton | Base topology + proportions | 50-100 | Body oval, major joint positions |
| 2: Mesh | Extrude appendages via bmesh | 200-400 | Recognizable silhouette, 200-500 verts |
| 3: Detail | Subdivide + surface noise | 300-500 | Organic surface, 500-2000 verts |
| 4: Cleanup | Topology validation, merge by distance | 100-200 | Clean mesh, 2000-8000 verts after subsurf |

Each stage includes explicit "scene already has X object" context in prompt.

---

## Quadruped Anatomy Guide (Dog, Cat, Horse, Wolf)

### Body Proportions Reference

| Part | Scale (relative to body=1.0) | Position |
|------|------------------------------|----------|
| Torso | X=1.2, Y=2.0, Z=0.8 | Origin (0,0,0) |
| Head | Sphere r=0.45-0.55 | (0, 1.1-1.4, 0.4-0.6) |
| Neck | Cylinder r=0.2-0.3, d=0.4-0.6 | Connects body Y-front to head |
| Front legs | Cylinder r=0.12-0.18, d=0.6-0.8 | X=±0.35-0.45, Y=0.6-0.8 |
| Back legs | Cylinder r=0.12-0.18, d=0.6-0.8 | X=±0.35-0.45, Y=-0.6-0.8 |
| Ears | Flat sphere sx=0.2, sy=0.08, sz=0.3 | X=±0.3, Y≈head_Y, Z=head_Z+0.4 |
| Snout | Sphere r=0.15-0.2 | (0, head_Y+0.45, head_Z-0.1) |
| Tail | Cone r_base=0.12, r_top=0.04, d=0.5 | (0, -1.2-1.4, 0.2-0.4) |

### Leg Bottom Z Reference
- Bottom of body at Z = -body_Z_scale/2 = -0.4 for default
- Legs bottom = Z - leg_depth/2 ≈ -0.75
- Foot position: body_Z_bottom - leg_depth

---

## System Prompt Template for Blender Script Generation

Use this template when calling Claude CLI or Codex for mesh generation:

```
You are a Blender Python expert. Write ONLY Python code — no explanations, no markdown.
The code runs inside Blender (bpy and bmesh are available).

RULES:
1. Use bmesh.ops for all geometry (extrude_face_region, subdivide_edges, translate, scale)
2. Do NOT create separate objects for appendages — use extrusion on the existing mesh
3. Always call bm.faces.ensure_lookup_table() and bm.verts.ensure_lookup_table() after geometry changes
4. Get new verts after extrude: [e for e in result['geom'] if isinstance(e, bmesh.types.BMVert)]
5. Scale around centroid: compute center first, then offset each vert
6. Call bm.normal_update() before bm.to_mesh()
7. Add Subdivision Surface modifier (levels=2) for smooth organic result
8. Target: 1000-5000 vertices before subdivision, 2000-8000 after

FORBIDDEN:
- bpy.ops.mesh.primitive_uv_sphere_add() for appendages
- Separate objects for body parts
- Assembly of primitives without extrusion connection

OUTPUT: Only Python code, no markdown fences.
```

---

## Iterative Render-Feedback Loop

Best mesh quality comes from iterative generation + vision feedback:

1. Generate script → execute in Blender → render PNG (6 angles via `mesh.render_snapshot`)
2. Send PNG to vision-capable LLM with critique prompt:
   ```
   Analyze this 3D mesh render. Identify:
   - Missing parts (limbs, features)
   - Wrong proportions (too tall/flat/wide)
   - Surface artifacts (spikes, holes, disconnected parts)
   Output: list of specific fixes with bmesh operations to apply.
   ```
3. Generate fix script → apply → re-render
4. Repeat max 3 iterations

**Key**: Use `mesh.render_snapshot` (6-angle automatic lighting) for consistent feedback images.

---

## Topology Quality Inline Validation

Add this after each bmesh step to catch issues early:

```python
def validate_mesh_topology(bm) -> dict:
    """Quick topology health check inside bmesh context."""
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Non-manifold edges (not shared by exactly 2 faces)
    non_manifold = [e for e in bm.edges if len(e.link_faces) != 2]

    # Degenerate faces (area < threshold)
    degenerate = [f for f in bm.faces if f.calc_area() < 1e-6]

    # Valence distribution
    valence_counts = {}
    for v in bm.verts:
        n = len(v.link_edges)
        valence_counts[n] = valence_counts.get(n, 0) + 1
    quad_v = valence_counts.get(4, 0)
    total_v = len(bm.verts)
    quad_ratio = quad_v / total_v if total_v > 0 else 0

    return {
        "verts": total_v,
        "faces": len(bm.faces),
        "non_manifold_edges": len(non_manifold),
        "degenerate_faces": len(degenerate),
        "quad_valence_ratio": round(quad_ratio, 2),
        "healthy": len(non_manifold) == 0 and len(degenerate) == 0 and quad_ratio > 0.6,
    }
```

Target: `healthy == True`, `quad_valence_ratio > 0.6`, `non_manifold_edges == 0`.

---

## Modifier Stack Order (Canonical)

Always apply in this order for organic models:

1. **Subdivision Surface** (levels=2) — smooth topology
2. **Smooth by Angle** (or shade_smooth) — normals
3. **Decimate** (ratio=0.5, optional) — reduce poly count if > 10k verts
4. Never apply before export unless baking

```python
obj = bpy.context.active_object
# 1. SubSurf
ss = obj.modifiers.new("SubSurf", 'SUBSURF')
ss.levels = 2
ss.render_levels = 2
# 2. Smooth shading
bpy.ops.object.shade_smooth()
# Decimate only if needed
if len(obj.data.vertices) > 8000:
    dec = obj.modifiers.new("Decimate", 'DECIMATE')
    dec.ratio = 6000 / len(obj.data.vertices)
```

---

## Common Failure Patterns & Fixes

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| Blob result | LLM used primitive assembly without connecting | Force bmesh extrusion, add `Never create separate objects` rule |
| Missing limbs | Script timed out mid-generation | Use staged pipeline, each step < 60 tokens of code |
| Floating parts | `bpy.ops.object.join()` failed silently | Check mesh connectivity with `ensure_lookup_table()` before join |
| All faces black | Normals flipped | `bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])` |
| Mesh disappears | Active object not set before ops | Always `bpy.context.view_layer.objects.active = obj` first |
| 0 verts reported | .blend not opened for multi-step | `bpy.ops.wm.open_mainfile(filepath=blend_path)` at start of step 2+ |

---

## Sources
- research/llm-prompt-engineering-3d.md (LL3M, L3GO, Chain-of-3D-Thoughts)
- research/topology-fundamentals.md (quad dominance, non-manifold checks)
- research/ai-3d-generation-methods.md (TRELLIS, Hunyuan3D comparison)
- forge/meshes/runs/realistic_dog-20260414-105732/ (v4 generated scripts analysis)
