---
last_updated: 2026-04-14
knowledge_filled: true
total_topics: 4
sources: 20+
---

# Knowledge Index — 3D Asset Optimizer

> Bu dosya agent'in bilgi haritasidir. Gorev alirken once bunu oku; sadece ilgili dosyalari yukle.

## Temel Konular

### 1. Polygon Reduction Methods
**Dosya:** `knowledge/polygon-reduction-methods.md`

Mesh simplifikasyon teknikleri: Decimate (Collapse/Unsubdivide/Planar), retopology, quad topology. Detaylar: Blender Decimate ayarları, %50-95 azaltma hedefleri, kalite kontrol checklistesi.

**Ne zaman load et:** Mesh polygon sayisini azaltmak gerektiğinde.

**Anahtar çıktı:** Decimate ratio, target poly count, quad % korunması.

### 2. LOD Generation
**Dosya:** `knowledge/lod-generation.md`

LOD0-3 zinciri olusturma: Polygon hedefleri (LOD0: 5-10K, LOD1: 2-3.5K, LOD2: 500-1K, LOD3: 100-300), gecis mesafeleri, Blender LOD setup, visual popping avoidance.

**Ne zaman load et:** LOD sistemi tasarlamak gerektiğinde.

**Anahtar çıktı:** LOD chain distances, polygon targets per level, transition buğün.

### 3. glTF Draco Compression
**Dosya:** `knowledge/gltf-draco-compression.md`

Draco geometry compression: Ayarlar (method=EDGEBREAKER, quantization bits), gltf-transform CLI komutları, %80-95 sıkistirma, platform-bazli öneriler (web/mobile/desktop), lossy warningi.

**Ne zaman load et:** Dosya boyutu kritik veya geometry-heavy model.

**Anahtar çıktı:** Compression ratio, decode speed, file size before/after, platform uyumluluğu.

### 4. Texture Optimization
**Dosya:** `knowledge/texture-optimization.md`

Texture boyut/format optimizasyonu: Power-of-two (512-4096), mipmap chains, KTX2/Basis Universal compression, channel packing (ORM: Occlusion/Roughness/Metallic), %50-80 azaltma.

**Ne zaman load et:** Texture boyut/bandwidth optimize etmek gerektiğinde.

**Anahtar çıktı:** Resize dimensions, compression format, channel layout, final size estimate.

---

## Quick Decision Tree

| Hedef | Load Et |
|------|---------|
| Mesh polygon count ↓ | Polygon Reduction Methods |
| LOD chain olustur | LOD Generation |
| Geometry sıkıştır | glTF Draco Compression |
| Texture boyut ↓ | Texture Optimization |
| Multi-stage pipeline | Tüm 4'ü oku sirayla |

---

## Integration Workflow

**Tipik optimization pipeline:**
```
1. Polygon Reduction (Decimate to target LOD0 poly count)
2. LOD Generation (Create LOD1-3, set distances)
3. Texture Optimization (Resize, compress, pack channels)
4. Draco Compression (Final geometry encoding)
5. File size reporting (Before/after comparison)
```

---

## Sources Index

- Blender Base Camp (LOD transitions, Decimate)
- Khronos Group (glTF spec, KTX2, ORM packing)
- glTF Transform docs (CLI, Draco, meshopt)
- Basis Universal (KTX2 compression)
- meshoptimizer (geometry optimization)
- ACM Transactions (quad-dominant reduction research)
