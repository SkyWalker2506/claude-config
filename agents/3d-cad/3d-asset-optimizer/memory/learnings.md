# Learnings

> Web'den, deneyimden veya diger agentlardan ogrenilenler.
> Format: tarih + kaynak + ogrenilen + nasil uygulanir

## 2026-04-14 | Knowledge Documentation Sharpening

### Draco Compression Insights

**Source:** KHRDracoMeshCompression, Google Draco docs, gltf-transform CLI

**Learned:**
- EDGEBREAKER method provides higher compression ratios than SEQUENTIAL (important for file size critical scenarios)
- Decode speed is independent of encode speed settings — most modern decoders support all speeds equally
- Quantization bits control quality-to-size tradeoff per attribute (position, normal, texcoord separately)
- Repeated compress→decompress cycles lose precision — Draco must be final step in pipeline

**Application:**
- Use EDGEBREAKER (method=edgebreaker) by default for web/mobile targets
- Position quantization: 14 bits for hero assets, 10-12 for distance/mobile
- Normal quantization: 8-10 bits (lower causes visible banding)
- Always measure file size before/after; compress is lossy even if visually acceptable

---

## 2026-04-14 | LOD Generation Standards

**Source:** Blender Base Camp, FSDeveloper forums, Blender Manual

**Learned:**
- Standard 4-level LOD chain: LOD0 (full), LOD1 (30-50%), LOD2 (10-20%), LOD3 (2-5%)
- Decimate Collapse achieves 50-70% reduction while maintaining visual integrity
- Data Transfer modifier preserves high-poly details via normal maps on low-poly meshes
- Distance-based LOD switching prevents "pop" visual artifacts if hysteresis applied (small buffer between LOD transitions)
- Planar method specifically for CAD/flat surfaces (not general-purpose)

**Application:**
- Always create 4 LODs minimum; each with specific polygon targets
- Use Collapse method 90% of time; Unsubdivide for subdivision models only
- Plan LOD transitions at camera distances (5m, 15m, 50m typical)
- Test LOD transitions in-engine at intended distances before shipping

---

## 2026-04-14 | Quad-Dominant Topology & Decimate Behavior

**Source:** ACM Transactions on Graphics (2024), Blender community

**Learned:**
- Stock Blender Decimate Collapse preserves triangles only; does NOT maintain quad topology
- Quad-dominant retention requires academic algorithms (single-edge-collapse) or manual retopology
- Industry target: 80%+ quads for rigged models; 60%+ acceptable for static props
- Quad topology essential for clean deformation, UV unwrapping, and normal map baking quality
- Workaround: If quads critical after decimation → retopology step required

**Application:**
- Document poly reduction limitations when quads mandatory (e.g., character models for animation)
- Recommend retopology for hero assets; decimation + normal map transfer for distance LODs
- Use Decimate freely for static props/exports; mention quad loss for rigged assets

---

## 2026-04-14 | Texture Optimization Ecosystem

**Source:** Khronos KTX2 spec (Feb 2024), Basis Universal, glTF Transform, glTF 2.0 spec

**Learned:**
- Power-of-two requirement is GPU cache optimization (not strict, but recommended)
- KTX2 with Basis Universal UASTC RDO (Rate-Distortion Optimization) achieves best quality-to-size ratio (20-40% of original PNG)
- glTF metallicRoughness packing standard: Green=Roughness, Blue=Metallic (no occlusion in standard)
- ORM texture convention (R=Occlusion, G=Roughness, B=Metallic) is vendor extension pattern; use MSFT_packing_occlusionRoughnessMetallic for custom arrangements
- Mipmaps add ~33% size overhead but enable cache-efficient sampling (minimal tradeoff for benefits)

**Application:**
- Always resize to POT (512, 1024, 2048, 4096) before compression
- Use KTX2 UASTC with RDO 1.0-2.0 for production (good quality/size balance)
- Document channel packing strategy explicitly (standard glTF vs ORM extension)
- Include mipmap generation in optimization pipeline (gltf-transform handles auto)

---

## 2026-04-14 | Pipeline Integration Best Practices

**Source:** gltf-transform docs, meshoptimizer, industry workflows

**Learned:**
- Sequential optimization order matters: Geometry reduction → LOD generation → Texture optimization → Draco/Meshopt compression
- Meshopt quantize + EXT_meshopt_compression complements Draco; can be stacked for additional gains
- Quantization before Draco compression improves final size (quantize explicitly, then Draco)
- File size reporting (before/after comparison tables) critical for stakeholder decision-making

**Application:**
- Document optimization pipeline as sequential steps with intermediate size checkpoints
- Use gltf-transform optimize command for quick wins; --draco + --meshopt when control needed
- Always measure: original size → after LOD → after Draco → after meshopt (show each delta)
- Provide platform-specific recommendations (web: 1024 res + KTX2, mobile: 512 res + ETC1S, desktop: 2048-4096)
