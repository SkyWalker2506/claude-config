---
last_updated: 2026-04-14
confidence: high
sources: 8
---

# Texture Optimization

Texture optimization reduces file size and load times through resolution sizing, mipmap chains, compression, and channel packing. Average savings: 50-80% of original texture data.

## Power-of-Two (POT) Texture Sizes

**Golden rule:** All texture dimensions must be powers of 2 for optimal GPU caching.

| Dimension | POT Sizes | Suitable For | Approx MB |
|-----------|-----------|------------|----------|
| 512×512 | 512, 1024, 2048 | Mobile, web, distant details | 1-4 |
| 1024×1024 | 1024, 2048, 4096 | Standard, mid-range hardware | 4-16 |
| 2048×2048 | 2048, 4096, 8192 | Hero assets, high-end desktop | 16-64 |
| 4096×4096 | 4096, 8192, 16384 | Ultra-high detail, CAD models | 64-256 |

**Recommended by platform:**
- **Mobile:** 512-1024 (watch memory budget: 50-200 MB)
- **Web:** 1024-2048 (load time <3s target)
- **Desktop:** 2048-4096 (GPU VRAM: 4GB+ available)

## Mipmap Chains

Mipmaps are automatically-generated half-resolution copies (2x2→1x1 → cascading).

**Benefits:**
- Reduces aliasing at distance (sharper LOD)
- Enables cache-efficient sampling
- Auto-generated, minimal overhead (~33% extra size)

**With mipmaps: 1024×1024 texture = 1.3 MB (instead of 1 MB)**

**gltf-transform command:**
```bash
gltf-transform optimize model.glb output.glb \
  --texture-resize 1024 \
  --texture-format webp
```

## Texture Compression: KTX2 & Basis Universal

### KTX2 Format Benefits
- **Specification:** Khronos standard (Feb 2024 approved)
- **Compression modes:**
  - ETC1S: Lower quality, smaller (older)
  - UASTC: High quality, larger (modern)
- **Supercompression:** Zstd/Zlib on top, minimal overhead

### Basis Universal Codec

**High-quality UASTC mode:**
```bash
basisu input.png \
  -uastc \
  -uastc_rdo_l 1.0 \
  -mipmap
```

| RDO Level | File Size | Quality | Use Case |
|-----------|-----------|---------|----------|
| 0.2-0.5 | Largest | Best | Hero assets |
| 1.0-2.0 | Medium | Good | Standard |
| 3.0+ | Smallest | Fair | Distant/mobile |

**Typical compression:** KTX2 → 20-40% of original PNG size

### CLI Usage
```bash
# Install basis_universal
npm install -g basis_universal

# Compress single texture with mipmaps
basisu texture.png -mipmap -ktx2 -quality 192

# Batch compress with quality preset
basisu *.png -mipmap -ktx2 -quality 192 -y
```

## Channel Packing Strategy (ORM Maps)

glTF uses packed textures to reduce draw calls. Standard layout:

| Channel | Property | Range | Notes |
|---------|----------|-------|-------|
| R | Occlusion (AO) | 0-1 | Darkens shadows |
| G | Roughness | 0-1 | 0=mirror, 1=rough |
| B | Metallic | 0-1 | 0=non-metal, 1=full metal |

### Why Pack?
- One texture lookup instead of three
- Reduces VRAM, bandwidth
- Smaller final file: 1 ORM (4 MB) vs 3 separate (12 MB)

### Creation in Blender
```
1. Bake Occlusion → R channel
2. Bake Roughness → G channel
3. Bake Metallic → B channel
4. Compose into single image (shader mix or compositor)
5. Export as PNG, compress to KTX2
```

### glTF Spec Compliance
Standard glTF uses metallicRoughnessTexture:
- Green channel: Roughness
- Blue channel: Metallic
- (No occlusion, handled separately)

**Extended packing (MSFT extension):** Custom arrangements (R:rough, G:metal, B:occlusion).

## Full Optimization Pipeline

```bash
# Step 1: Resize to POT
convert texture.png -resize 2048x2048 texture_resized.png

# Step 2: Compress to KTX2 with mipmaps
basisu texture_resized.png -mipmap -ktx2 -quality 192

# Step 3: Apply with gltf-transform
gltf-transform optimize model.glb output.glb

# Result: texture.basis.ktx2 (~500 KB from 4 MB PNG)
```

## Size Benchmarks

**Before → After optimization (example 4K texture):**
- Original PNG: 16 MB (4096×4096, uncompressed)
- KTX2 (ETC1S): 2.5 MB (-84%)
- KTX2 (UASTC RDO 1.0): 5 MB (-69%)
- WebP (quality 80): 3.2 MB (-80%)

## Texture Format Decision Tree

| Format | Quality | Size | Support | Best For |
|--------|---------|------|---------|----------|
| PNG | Lossless | Large | Universal | Source/archive |
| WebP | Good | Medium | Modern browsers | Web, streaming |
| KTX2 UASTC | Excellent | Medium | Khronos/games | Desktop, hero |
| KTX2 ETC1S | Good | Small | Mobile focus | Mobile, low-end |
| ASTC | Good | Small | Some GPUs | Mobile optimal |

## Anti-Patterns

- Using non-POT sizes (GPU padding wastes memory)
- Skipping mipmaps (aliasing at distance)
- Compressing to KTX2 before resizing (double-compress = quality loss)
- One-size-fits-all (no channel packing reductions)
- No before/after size measurement

## Sources

- [KTX File Format Specification](https://github.khronos.org/KTX-Specification/ktxspec.v2.html)
- [Basis Universal GPU Texture Codec](https://github.com/BinomialLLC/basis_universal)
- [glTF 2.0 Specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
- [KTX2 Texture Compression Guide](https://evergine.com/ktx2-texture-compression/)
- [Art Pipeline for glTF | Khronos](https://www.khronos.org/blog/art-pipeline-for-gltf)
