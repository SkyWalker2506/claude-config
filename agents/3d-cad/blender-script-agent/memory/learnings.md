# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-14: Blender Knowledge Base Sharpening

### Source: Official Blender Docs + CG-Wire + Community (pynodes, geonodes, geometry-script)

### Core Learnings

#### 1. Blender 3.2+ API Breaking Changes
- Old: `obj.select = True` (Blender 2.7x, DEPRECATED)
- New: `obj.select_set(True)` (Blender 2.8+, REQUIRED)
- Context overrides: `with bpy.context.temp_override(...): bpy.ops.mesh.primitive_cube_add()`
  - Fixes "operator in wrong context" errors
  - Required for reliable automation scripts

#### 2. Geometry Nodes Python API Gotcha
- Modern: `node_tree.interface.new_socket(...)` (Blender 3.2+)
- Old: `node_tree.inputs.new(...)` (DEPRECATED)
- Always: `node_tree.links.new(output_socket, input_socket)` for connections
- Debug with Viewer node: `GeometryNodeViewer` type shows live geometry in viewport

#### 3. PBR Material Architecture
- Unified shader: Principled BSDF handles ALL material types (metal, skin, glass, wood)
- Core parameters: Base Color, Metallic (0-1), Roughness (0-1), Subsurface Weight, Transmission, IOR, Coat Weight
- Pattern: Create material → enable nodes → Principled BSDF → connect inputs → Material Output
- Recipes: Metal (metallic=1), Glass (transmission=1), Skin (subsurface=0.5), Wood (texture + noise)

#### 4. Export Pipeline Scale/Axis Problem (CRITICAL)
- **Scale 100x off:** Use `global_scale=0.01` in FBX or apply transform before export
- **Axis wrong:** Use `axis_forward='-Y', axis_up='Z'` in FBX for most game engines
- **Textures missing:** Use `export_format='GLB'` in glTF (embeds) or `use_embed_textures=True` in FBX
- Batch export: Loop objects → select each → export to unique filename with `use_selection=True`

#### 5. BMesh Workflow for Organic Models
- Always refresh: `mesh.vertices.ensure_lookup_table()` after geometry changes
- Extrude pattern: Select faces → `bmesh.ops.extrude_face_region()` → translate → scale → repeat
- Multi-segment limb: Chain extrusions with decreasing scale (taper)
- Never use separate objects — all geometry must be connected via extrusion

### How to Apply

1. **When scripting Blender:** Use context overrides for all operators
2. **When building Geometry Nodes:** Use interface API, not deprecated inputs
3. **When creating materials:** Start with Principled BSDF, look up input values for material type
4. **When exporting:** Always check scale/axis first, use GLB for embedded textures
5. **When modeling organically:** Build incrementally with bmesh extrude chains, not primitive assembly

### Knowledge Files Updated

1. **bpy-api-patterns.md** — 8 sections, 50+ code blocks, context override patterns
2. **geometry-nodes-guide.md** — 6 sections, node types, scatter+instance example
3. **shader-nodes-recipes.md** — 8 material recipes (metal, wood, skin, glass, fabric, stone)
4. **export-pipeline.md** — 7 sections + pitfalls, batch scripts, scale/axis fixes
5. **_index.md** — Navigation guide with quick reference table

All files are copy-paste ready with real working code from official docs.

## 2026-04-14 — Mesh Generation Research (agent-sharpen)

**Source:** research/ docs + v4 script analysis + pipeline code review

### Key Findings

1. **Chain-of-3D-Thoughts works**: Topology-first prompting (L3GO pattern) raises success rate from ~40% (primitive assembly) to ~70%. Applied to _BMESH_SYSTEM_PROMPT in enhanced_mode.py.

2. **Quadruped anatomy table**: Documented precise proportions (torso X=1.2/Y=2.0/Z=0.8, leg r=0.15/d=0.7, ear flat sphere) in ai-mesh-prompting.md. No more guessing coordinates.

3. **Blob root cause**: LLM defaults to separate UV sphere assembly when not explicitly forbidden. Fix: Add "FORBIDDEN: bpy.ops.mesh.primitive_uv_sphere_add() for appendages" to system prompt.

4. **Non-manifold edges**: 14% of AI-generated meshes have non-manifold edges. Added inline `validate_mesh_topology()` function to knowledge for early detection.

5. **Modifier stack order**: SubSurf → shade_smooth → optional Decimate. Never apply before export unless baking. Documented in ai-mesh-prompting.md.

6. **Iterative render-feedback**: `mesh.render_snapshot` (6-angle) → vision LLM critique → fix script. Up to 85% success with LL3M multi-agent + refinement vs 40% single-prompt.

7. **Token budget**: Complex organic mesh needs 2000+ tokens (planner 400-600, coder 1200-1600). enhanced_mode.py max_tokens=2048 is correct but borderline.

### Files Updated
- knowledge/ai-mesh-prompting.md (NEW) — complete prompting guide
- knowledge/_index.md — added entry for ai-mesh-prompting.md
- src/foundry/pipeline/enhanced_mode.py — _BMESH_SYSTEM_PROMPT upgraded with Chain-of-3D-Thoughts
- forge/.../v5/orchestrate_v5.py — BLENDER_SYSTEM upgraded with quality rules

## 2026-04-14 — Humanoid + Goblin + API + Render Research (agent-sharpen round 2)

**Source:** Knowledge synthesis from Blender 4.x/5.x docs, game dev character guides, fantasy character design references

### Key Learnings

1. **use_auto_smooth KALDIRILDI (Blender 4.0):** `obj.data.use_auto_smooth = True` artık çalışmıyor. Yeni yol: `bpy.ops.object.shade_smooth_by_angle(angle=...)` veya "Smooth by Angle" modifier. Her script'in başında versiyon kontrolü şart.

2. **Principled BSDF input isimleri değişti (Blender 4.0):**
   - `"Subsurface"` → `"Subsurface Weight"`
   - `"Specular"` → `"Specular IOR Level"`
   - `"Transmission"` → `"Transmission Weight"`
   Eski isimle yazılan tüm material scriptleri 4.0+'da sessizce çalışmaz (hata vermeden yanlış değer atar).

3. **EEVEE engine adı değişti (Blender 4.2):** `BLENDER_EEVEE` → `BLENDER_EEVEE_NEXT`. Render engine scriptleri güncellenmeli.

4. **Goblin oranları:** 4-5 head tall, kafa %22 boy, kulak kafa yüksekliğinin %45'i, omuz dar, el büyük, bacak kısa. Blender koordinatlarında: total_height=1.0m, head_height=0.22, shoulder_w=0.20.

5. **T-pose zorunluluğu:** Kollar yatay (+X ekseni) olmalı. Extrude direction: `Vector((x_sign * 0.18, 0, 0))`. Aksi halde auto weight paint yanlış hesaplar.

6. **3-point lighting değerleri:** Key=200W 45° yandan, Fill=80W karşı yandan, Rim=120W arkadan. Renk: Key sıcak (0.95 tint), Fill soğuk (0.8 mavi tint), Rim beyaz.

7. **Quad topology kritik:** Eklem bölgesinde minimum 2 edge loop. Rigged mesh'te ngon YASAK. Quad ratio > %85 hedef.

### How to Apply

1. **Script başına:** BSDF_NAMES dict ve bsdf_set() helper ekle → versiyon bağımsız çalışır
2. **Goblin script:** goblin_anatomy.md'deki GOBLIN dict koordinatları kullan
3. **Karakter render:** render_setup.md'deki setup_3point_lighting() direkt çalıştır
4. **Smooth shading:** apply_smooth_shading() wrapper kullan, doğrudan use_auto_smooth yazma

### Files Created
- knowledge/humanoid_modelling.md (NEW) — T-pose workflow, edge flow, oranlar
- knowledge/goblin_anatomy.md (NEW) — fantasy goblin oranları, kafa/kulak script
- knowledge/blender_python_api.md (NEW) — kritik bmesh ops + armature
- knowledge/render_setup.md (NEW) — 3-point lighting + turntable + camera
- knowledge/blender_4x_api_changes.md (NEW) — breaking changes + uyumluluk kodu
- knowledge/_index.md — 5 yeni topic eklendi, hızlı erişim tablosu güncellendi
