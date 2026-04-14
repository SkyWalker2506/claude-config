---
last_updated: 2026-04-14
confidence: high
sources: 7
---

# LOD (Level of Detail) Generation

LOD chains reduce GPU load by swapping high-poly geometry for lower-poly versions at increasing camera distances. Standard target: LOD0 (full detail) → LOD3 (minimal).

## Polygon Reduction Targets

| LOD Level | Poly Count | Target % of LOD0 | Use Distance | Visual Quality |
|-----------|-----------|------------------|--------------|---|
| LOD0 | 5,000-10,000 | 100% | 0-5m | Full detail, hero assets |
| LOD1 | 2,000-3,500 | 30-50% | 5-15m | Good detail, viewable |
| LOD2 | 500-1,000 | 10-20% | 15-50m | Simplified, acceptable |
| LOD3 | 100-300 | 2-5% | 50m+ | Silhouette only |

## Blender Decimate Modifier Settings

### Collapse Method (most common)
```
Collapse ratio: 0.5 = 50% reduction
Vertex group: Optional, mask for selective reduction
Face count target: Enable for specific target (e.g., 2000 faces)
```

Example workflow for LOD1 (50% reduction):
1. Duplicate base mesh → name "Mesh_LOD1"
2. Add Decimate modifier (Collapse type)
3. Set ratio: 0.5 (reduces to ~50% polygons)
4. Iterate, measure polygon count
5. Apply modifier when satisfied

### Unsubdivide Method (reverse subdivision)
- Best for subdivision-surface models
- Removes subdivision levels without destroying topology
- Useful if original had subdivision modifiers

### Planar Method (simplify flat surfaces)
- Simplifies large flat regions (walls, floors, panels)
- Keep angle threshold ~5-10 degrees
- Good for CAD/architectural models

## Transition Distances & Setup

**Distance-based LOD switching:**
- Use GameObject LOD component (game engines) or Blender LOD panel
- Visibility culling distance = draw distance + margin
- Hysteresis: Switch LODs with small distance buffer to prevent flickering

**Example Blender LOD setup:**
```
LOD0: Distance 0.0
LOD1: Distance 5.0  (switch at 5m)
LOD2: Distance 15.0 (switch at 15m)
LOD3: Distance 50.0 (switch at 50m)
```

## Quality Control

| Check | Pass Criteria |
|-------|---------------|
| Silhouette | LOD maintains recognizable shape |
| Creasing | No weird pinching at hard edges |
| UV islands | No overlaps after reduction |
| Normal maps | Behave reasonably on low poly |
| Sharp edges | Preserved (use edge weights before decimating) |

## Advanced Techniques

### Data Transfer for Detail Preservation
```
High-poly → Low-poly detail transfer:
1. Keep high-poly as sculpt reference
2. Create low-poly retopo mesh
3. Use Data Transfer modifier: transfer normals from high-poly
4. Bake normal map from high-poly → low-poly material
```

### Avoiding "Pop" Transitions
- Gradual fade: Overlap LODs in distance, blend opacity
- Soft edges: Avoid sharp silhouette changes between LODs
- Test at target distances in viewport before export

## Polygon Reduction Benchmarks

**Real-world reductions (Decimate Collapse):**
- 50% reduction: Visible only at very close range
- 30-50% reduction: Sweet spot, maintains most detail
- 70% reduction: Visual loss but acceptable for distance
- 90% reduction: Obvious simplification (LOD3 only)

## Integration with Asset Pipeline

```bash
# Multi-LOD export from Blender
# 1. Create LOD0, LOD1, LOD2, LOD3 objects
# 2. Use collection-based export (each collection = LOD)
# 3. Export as separate .glb files, import into engine
# 4. Game engine combines into single LOD chain
```

## Anti-Patterns

- No visual testing at target distances (looks OK in viewport, bad in game)
- Skipping LOD1-2, jumping straight LOD0 → LOD3 (too jarring)
- Using automatic decimate on complex topology (will trash quads)
- Ignoring UV deformation during reduction

## Sources

- [Seamless LOD Transitions in Blender](https://www.blenderbasecamp.com/seamless-lod-transitions-in-blender/)
- [Level of Detail in 3D: Impact on Gaming & XR](https://news.viverse.com/post/what-is-level-of-detail-lod-in-3d-modeling-how-it-impacts-on-gaming-and-xr-industries)
- [Creating LOD Models | FSDeveloper](https://www.fsdeveloper.com/forum/threads/creating-your-lod-models.452825/)
- [Enhancing 3D Workflows with Decimate Modifier](https://www.tripo3d.ai/blog/collect/enhancing--d-workflows-with-the-decimate-modifier-in-blender-7rj3aozgmla)
