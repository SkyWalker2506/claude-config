---
last_updated: 2026-04-14
knowledge_filled: true
total_topics: 6
confidence: high
---

# Knowledge Index

Agent bilgi haritası. Görev alırken önce bunu oku; sadece ilgili dosyaları yükle.

## Core Knowledge Files

### 1. [Bpy API Patterns](bpy-api-patterns.md)
Blender Python (bpy) temel pattern'ler ve API kullanımı.
- Nesne oluşturma, seçme, silme
- Mod değiştirme (OBJECT/EDIT/SCULPT)
- Context override (Blender 3.2+)
- Collection yönetimi
- Mesh veri erişimi (vertices, edges, faces, loops)
- Modifier stack yönetimi
- Keyframe işlemleri
- Operator patterns

**Uygun görevler:** Blender automation, object manipulation, mesh editing, modifier setup.

### 2. [BMesh Organic Modeling](bmesh-organic-modeling.md)
Organik mesh oluşturma: hayvan, karakter, canlı modelleme.
- Phase-based pipeline (base form → extrude appendages → detail → finalize)
- BMesh API kullanımı
- Yüz seçimi pattern'leri
- Multi-segment extrude limb tekniği
- Ölçü tablosu ve hata çözümleri
- Kod örnekleri (başlangıçtan sona)

**Uygun görevler:** Organik model oluşturma, animal mesh, character modeling.

### 3. [Geometry Nodes Guide](geometry-nodes-guide.md)
Prosedural geometri oluşturma Geometry Nodes modifier ile.
- Node tree oluşturma
- Temel node'lar (cube, sphere, line, circle)
- Distribute Points on Faces
- Instance on Points
- Math node'ları
- Attribute capture ve reuse
- Viewer node debugging
- Tam scatter + instance örneği

**Uygun görevler:** Prosedural model oluşturma, scatter, array, procedural placement.

### 4. [Shader Nodes Recipes](shader-nodes-recipes.md)
PBR material setup ve shader node oluşturma.
- Principled BSDF kurulumu
- Image texture yükleme
- Procedural texture (Noise, Voronoi, Wave, Musgrave)
- PBR material recipes:
  - Metal (shiny, brushed)
  - Wood (grain, color variation)
  - Skin (subsurface scattering)
  - Glass (transparency, IOR)
  - Fabric (soft, translucent)
  - Stone (rough, cellular)
- Node type quick reference

**Uygun görevler:** Material setup, PBR oluşturma, shader node connecting.

### 5. [Export Pipeline](export-pipeline.md)
Batch ve single-object export (glTF, FBX, OBJ).
- glTF 2.0 export (recommended)
- FBX export (Unreal, Unity)
- OBJ export (basic format)
- Batch export scripts
- Scale fix (100x problem)
- Axis conversion (Z-up vs Y-up)
- Texture embedding
- Common pitfalls & fixes
- Settings karşılaştırması

**Uygun görevler:** Model export, batch processing, engine preparation.

## Hızlı Erişim

| Ne arıyorsun | Dosya |
|-------------|-------|
| Nesne oluştur/sil | bpy-api-patterns.md |
| Modifier ekle | bpy-api-patterns.md |
| Mesh vertex değiştir | bpy-api-patterns.md |
| Organik model (hayvan) | bmesh-organic-modeling.md |
| Prosedural geometri | geometry-nodes-guide.md |
| Material setup | shader-nodes-recipes.md |
| Export model | export-pipeline.md |
| 100x scale fix | export-pipeline.md #Pitfall 1 |

## Kullanım Talimatı

1. **Görev alırken:** Önce bu index'i oku, hangi dosya uygun bak
2. **Code örnekleri:** Hepsi copy-paste ready, doğrudan kullan
3. **Hata çıkarsa:** "Common Pitfalls" bölümüne bak
4. **Kaynak referans:** Her dosyanın sonunda kaynakları bul

### 6. [AI Mesh Prompting](ai-mesh-prompting.md)
LLM ile yüksek kaliteli Blender mesh scripti üretme teknikleri.
- Chain-of-3D-Thoughts prompt pattern (topology-first)
- LL3M staged decomposition (skeleton → mesh → detail → cleanup)
- Quadruped anatomy proportions table (dog, cat, horse)
- System prompt template for Claude CLI / Codex
- Iterative render-feedback loop (render → vision critique → fix)
- Topology inline validation (non-manifold, quad ratio)
- Canonical modifier stack order
- Common failure patterns & fixes (blob, missing limbs, flipped normals)

**Uygun görevler:** LLM-driven mesh generation, staged pipeline, organic model quality improvement.

| Ne arıyorsun | Dosya |
|-------------|-------|
| Quadruped proportions | ai-mesh-prompting.md §Quadruped Anatomy |
| Blob/assembly fix | ai-mesh-prompting.md §Common Failure Patterns |
| Vision feedback loop | ai-mesh-prompting.md §Iterative Render-Feedback |
| Topology validation code | ai-mesh-prompting.md §Topology Quality Inline Validation |

---

## Kaynaklar

Tüm bilgiler resmi Blender API dokümantasyonu ve GitHub repository'lerinden toplanmıştır:
- [Blender Python API](https://docs.blender.org/api/current/)
- [Blender Manual](https://docs.blender.org/manual/en/)
- Community libraries: pynodes, geonodes, geometry-script
