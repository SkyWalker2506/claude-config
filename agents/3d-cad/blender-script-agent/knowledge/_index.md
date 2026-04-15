---
last_updated: 2026-04-14
knowledge_filled: true
total_topics: 12
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

### 7. [Humanoid Modelling](humanoid_modelling.md)
Blender'da humanoid karakter modelleme — T-pose, edge flow, modifier stack.
- Box modelling vs sculpting karşılaştırması
- T-pose base mesh script (torso, kol, bacak extrude)
- Eklem bölgeleri için edge loop kuralları
- Quad topology zorunluluğu + kontrol kodu
- Normal insan oranları (7.5 head) tablosu
- Game-ready vertex count hedefleri
- Metaball → mesh workflow (4.x, doğrulanmış adımlar)
- Voxel remesh sonrası ince geometri kurtarma (parmak stratejileri)
- Subdivision level önerileri (mobile/game/cinematic)

**Uygun görevler:** Humanoid character base mesh oluşturma, rigging-ready mesh, T-pose setup.

### 8. [Goblin Anatomy](goblin_anatomy.md)
Fantasy goblin karakteri oranları ve modelleme rehberi.
- Head count sistemi (goblin: 4-5 head tall)
- Goblin oranları tablosu (kafa, kulak, omuz, el, bacak)
- Blender koordinatlarında goblin boyut sabitleri
- Kafa ve kulak extrude script
- Goblin PBR renk paleti
- Poly count hedefleri (LOD0/1/2)
- Silüet kontrol listesi
- Metaball element tablosu (38 element, 1m boy, koordinatlarla)
- Parmak anatomisi (4 parmak, segment uzunlukları)
- Diş/fang anatomisi (konum, boyut, script)
- Silhouette kuralları (4 yön görünüm + kontrol scripti)

**Uygun görevler:** Goblin/fantasy karakter, çizgi film karakteri, büyük kafalı creature.

### 9. [Blender Python API](blender_python_api.md)
Karakter modelleme için kritik bmesh ve bpy operatörleri.
- extrude_face_region tam kullanım
- subdivide_edges seçici ve genel
- smooth_vert parametreleri
- Metaball → mesh convert workflow
- Voxel remesh optimal karakter ayarları
- Modifier stack sırası (doğru/yanlış)
- Armature oluşturma ve auto weight paint
- Non-manifold tespit ve fix

**Uygun görevler:** Karakter mesh operasyonları, rig kurma, mesh kalite kontrolü.

### 10. [Render Setup](render_setup.md)
Karakter showcase render pipeline.
- EEVEE vs Cycles — karakter için karşılaştırma
- 3-point lighting setup (key, fill, rim) + değerleri
- Turntable 360° render script
- Portrait camera (full body, bust, yüz shot)
- EEVEE Next ayarları (4.2+)
- Cycles render kalite ayarları
- Studio world/environment

**Uygun görevler:** Karakter render, showcase, portfolio, turntable animasyon.

### 11. [Blender 4.x API Changes](blender_4x_api_changes.md)
Blender 4.0/4.2/4.3/5.x breaking changes ve migration guide. Live test (5.1.0) ile güncellendi.
- use_auto_smooth kaldırıldı → alternatif
- Principled BSDF input isim değişimleri (5.1 tam listesi dahil)
- EEVEE engine adı: 4.2-4.x = EEVEE_NEXT, 5.x = EEVEE (geri döndü)
- Geometry Nodes socket API değişimi
- Armature slot sistemi (4.3+)
- Runtime versiyon tespiti
- Evrensel uyumluluk kod bloğu (4.x + 5.x)

**Uygun görevler:** Script portability, 4.x/5.x migration, backward-compatible code.

### 12. [Goblin Script Template](goblin_script_template.md)
Goblin üretimi için tam çalışan Blender 5.1 şablonu — kopyala-yapıştır kullan.
- Metaball → mesh convert pipeline
- 38 element, 1.2m goblin, live-tested proportions
- Sivri kulaklar, şişkin dizler, geniş kafa
- Noise tabanlı yeşil goblin skin material
- 3-point portrait lighting (key/fill/rim)
- Portrait kamera (tüm vücut, 1024x1536)
- EEVEE render + blend kayıt

**Uygun görevler:** Goblin mesh üretimi, versiyon iterasyonu, referans script.

---

## Hızlı Erişim (Güncel)

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
| Humanoid T-pose | humanoid_modelling.md |
| Goblin oranları | goblin_anatomy.md |
| Goblin kafa script | goblin_anatomy.md §Goblin Kafa Modelleme |
| Goblin tam şablon (5.1) | goblin_script_template.md |
| extrude_face_region | blender_python_api.md |
| Armature rig | blender_python_api.md §Armature |
| 3-point lighting | render_setup.md |
| Turntable render | render_setup.md §Turntable |
| use_auto_smooth hatası | blender_4x_api_changes.md |
| BSDF input değişti | blender_4x_api_changes.md |
| EEVEE engine adı (5.1 dahil) | blender_4x_api_changes.md |
| Modifier apply sırası | blender_4x_api_changes.md §Modifier Apply Sırası |
| convert() poll hatası | blender_4x_api_changes.md §Metaball Context |
| Shadow catcher zemin | render_setup.md §Shadow Catcher |
| Portrait kamera (tüm vücut) | render_setup.md §Portrait Kamera |
| 3-nokta ışık (HDRI yok) | render_setup.md §HDRI Olmadan |
| Goblin metaball element tablosu | goblin_anatomy.md §Metaball Element |
| Goblin parmak ölçüleri | goblin_anatomy.md §Parmak Anatomisi |
| Goblin diş/fang | goblin_anatomy.md §Dişler |
| Metaball→mesh workflow | humanoid_modelling.md §Metaball Workflow |
| Parmak remesh kurtarma | humanoid_modelling.md §Parmak Kurtarma |
| Subdivision level tablosu | humanoid_modelling.md §Subdivision Level |
| Versiyon uyumluluk kodu | blender_4x_api_changes.md §Özet |

---

## Kaynaklar

Tüm bilgiler resmi Blender API dokümantasyonu ve GitHub repository'lerinden toplanmıştır:
- [Blender Python API](https://docs.blender.org/api/current/)
- [Blender Manual](https://docs.blender.org/manual/en/)
- Community libraries: pynodes, geonodes, geometry-script
