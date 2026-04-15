---
last_updated: 2026-04-14
knowledge_filled: true
total_topics: 6
confidence: high
---

# Knowledge Index — Material & Lighting Artist

| # | Topic | File | Status | Confidence |
|---|-------|------|--------|------------|
| 1 | PBR Theory | pbr-theory.md | filled | high |
| 2 | Skin Shader Techniques | skin-shader.md | filled | high |
| 3 | Procedural Textures | procedural-textures.md | filled | high |
| 4 | Lighting Fundamentals | lighting-fundamentals.md | filled | high |
| 5 | Blender Shader Nodes | blender-shader-nodes.md | filled | high |
| 6 | Render Settings | render-settings.md | filled | high |

## Coverage Notes

All 6 topics researched and written on 2026-04-14 by opus-4.6.

Key research findings:
- Blender 4.0 was a breaking change for Principled BSDF input names (Subsurface Weight, Specular IOR Level, etc.)
- Blender 4.1 merged Musgrave Texture into Noise Texture (noise_type property)
- Blender 4.2-4.x replaced EEVEE with EEVEE Next (engine name: BLENDER_EEVEE_NEXT)
- Blender 5.x renamed EEVEE Next back to BLENDER_EEVEE; shader input names unchanged from 4.x
- All knowledge files include version-safe bpy code patterns with try/except fallbacks
