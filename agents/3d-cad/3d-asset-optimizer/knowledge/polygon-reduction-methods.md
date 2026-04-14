---
last_updated: 2026-04-14
confidence: high
sources: 6
---

# Polygon Reduction Methods

Methods for reducing polygon count while preserving shape and quality. Range: 30-95% reduction possible depending on technique and target asset.

## Decimate Modifier — Three Types

### 1. Collapse (Most Common)
**Best for:** General polygon reduction, organic shapes, game assets

```
Ratio: Set target reduction (0.5 = 50% remaining polygons)
Face Count Target: Alternative to ratio (e.g., target 2000 faces)
Vertex Group: Protect specific regions from decimation
Angle Limit: Preserve hard edges by protecting creases
```

**Results:** Reduces 50-70% polygon count with minimal quality loss on most meshes.

**Trade-offs:** Can destroy quad topology; output is triangle-heavy.

### 2. Unsubdivide (Reverse Subdivision)
**Best for:** Models with subdivision modifiers, control geometry recovery

```
Blender: Decimate → Mode: Unsubdivide
Iterations: 1-5 (more iterations = more reduction)
Face Strength: How strongly to preserve hard edges
```

**Results:** Removes subdivision levels without quality loss. Preserves original topology.

**Use case:** High-poly subdivided model → back to control cage.

### 3. Planar (Simplify Flat Regions)
**Best for:** CAD models, architectural, models with large flat surfaces

```
Angle Limit: 5-10° (regions within threshold simplified)
Use Decimated: Option to combine with Collapse
```

**Results:** 30-60% reduction on flat-heavy geometry. Keeps details on curves.

**Trade-off:** Won't help organic models without flat surfaces.

## Retopology — Manual Clean Reduction

**When to use:** Hero assets, characters, precise topology control needed

**Workflow:**
1. Duplicate high-poly reference mesh (hide but keep)
2. Create new mesh with quad topology (all 4-sided faces)
3. Model low-poly version matching high-poly silhouette
4. Transfer normals from high-poly → bake normal maps
5. Result: Clean topology, full control, best quality

**Time investment:** High (manual work), but output quality exceptional.

**Quad topology benefits:**
- Deforms cleanly when rigged/animated
- UV unwrapping simpler
- Normal map baking higher quality
- Edge loops follow anatomy/design intent

## Quad-Dominant Topology Target

**Industry standard: 80%+ quads, <20% triangles**

| Target | Quads | Triangles | Use Case |
|--------|-------|-----------|----------|
| Quad-dominant | 80%+ | <20% | Animation/rigging required |
| Triangle-OK | 60%+ | 40% | Static props, web assets |
| Triangle mesh | any | any | Export-only (final), no deform |

### Why Quads Matter
- **Deformation:** Quads subdivide evenly; triangles create pinching
- **UVs:** Quad layout easier to unwrap, fewer seams
- **Normal baking:** Quad topology bakes cleaner normals
- **LOD reduction:** Decimate preserves quad edges better on clean topology

## Recent Research (2024)

**Single Edge Collapse Quad-Dominant Reduction:**
- Academic method: Preserve quads during edge collapse (not standard Decimate)
- Result: Maintains quad topology while reducing 50-70%
- Tools: Some commercial tools (QuadriFlow variant) support this
- Blender: Stock Decimate doesn't preserve quads; output is triangle mesh

**Industry workaround:** Use stock Decimate → retopology to recover quads if critical.

## Tool Comparison

| Method | Quality | Speed | Topology | Best For |
|--------|---------|-------|----------|----------|
| Collapse | Good | Fast | Triangles | Quick reduction, non-critical |
| Unsubdivide | Excellent | Instant | Preserved | Subdivision models |
| Planar | Good | Fast | Triangles | CAD/flat geometry |
| Retopology | Excellent | Slow | Quads | Hero assets, animation |

## Before/After Checklist

**Before decimating:**
- [ ] Duplicate backup copy
- [ ] Remove modifiers (apply or hide)
- [ ] Merge duplicate vertices
- [ ] Remove isolated vertices
- [ ] Mark sharp edges if Collapse used

**After decimating:**
- [ ] Verify silhouette intact
- [ ] Check hard edge preservation
- [ ] Validate UV islands (no overlaps)
- [ ] Inspect normals (no flipped faces)
- [ ] Measure polygon count (before/after %)
- [ ] Visual test in viewport at intended distance

## Anti-Patterns

- Decimating without backup (can't undo subtle topology damage)
- Aggressive reduction on high-vertex geometry (>20k verts) without iteration
- Mixing methods without testing each independently
- Ignoring quad topology for rigged models (animation quality suffers)
- No visual validation at target distances/scales

## Sources

- [How to Unsubdivide in Blender](https://shiftychevre.com/how-to-unsubdivide-in-blender/)
- [Understanding Retopology Modifiers](https://irendering.net/understanding-retopology-modifiers-in-blender/)
- [How to Reduce Polygons in Blender](https://www.tripo3d.ai/blog/reduce-polygon-in-blender)
- [Remeshing | Blender Manual](https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html)
- [Single Edge Collapse Quad-Dominant Mesh Reduction | ACM Transactions](https://dl.acm.org/doi/10.1145/3731143)
