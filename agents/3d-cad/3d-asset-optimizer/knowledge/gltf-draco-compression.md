---
last_updated: 2026-04-14
confidence: high
sources: 8
---

# glTF Draco Compression

Draco is a geometry compression library that reduces glTF file size by compressing vertex positions, normals, and texture coordinates. Typical savings: 80-95% on raw geometry data.

## Compression Parameters

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| method | EDGEBREAKER | EDGEBREAKER, SEQUENTIAL | EDGEBREAKER better for compression; SEQUENTIAL preserves vertex order |
| encodeSpeed | 5 | 0-10 | Higher = faster encode, lower compression. 7-8 good balance |
| decodeSpeed | 5 | 0-10 | Higher = faster decode. Most decoders support all speeds equally |
| quantizationBits | varies | 8-16 | Position: 10-14, Normal: 8-10, Texcoord: 10-12 |

## CLI Usage with gltf-transform

### Basic compression
```bash
gltf-transform optimize input.glb output.glb --compress draco
```

### Advanced settings
```bash
gltf-transform extensions list input.glb  # Check current extensions
gltf-transform draco input.glb output.glb \
  --method edgebreaker \
  --encodeSpeed 7 \
  --decodeSpeed 5
```

### With quantization control
```bash
gltf-transform draco input.glb output.glb \
  --quantizePosition 14 \
  --quantizeNormal 10 \
  --quantizeTexcoord 12
```

## Recommended Settings by Asset Type

| Asset Type | Encode | Decode | Quantization (Pos) | Use Case |
|-----------|--------|--------|-------------------|----------|
| Static props | 8 | 5 | 10 | Web/mobile, non-interactive |
| Hero assets | 6-7 | 5 | 14 | Detailed game characters/objects |
| Architectural | 5 | 5 | 16 | CAD models, precision required |
| Organic | 7 | 5 | 12 | Characters, creatures |

## Performance Benchmarks

- **Decode overhead**: ~1-5ms per MB on modern hardware
- **Compression ratio**: 10:1 to 95:1 depending on model complexity
- **Geometry-heavy models** (>1 MB raw): 80-95% reduction typical
- **Texture-heavy models** (<500 KB geometry): 50-70% reduction

## Critical Gotchas

1. **Lossy compression**: Repeated compress→decompress cycles lose precision. Compress only as final step.
2. **Browser support**: Modern browsers/engines support decoding. Older devices may struggle.
3. **Quantization artifacts**: Too aggressive quantization (e.g., pos=8) visible on fine details.
4. **Normal maps**: Normals quantized separately; low quantization (8 bits) causes banding.

## Decision Matrix

| When | Recommendation |
|------|-----------------|
| Web/mobile target | Use Draco with pos=14, speed=7 (80-90% reduction) |
| Desktop high-end | Use Draco with pos=16, speed=5 (higher quality) |
| Real-time streaming | Use Draco with decode speed 7-10 (faster decoding) |
| Precision critical (CAD) | Reduce quantization levels or skip Draco |
| File size critical | Use EDGEBREAKER method + aggressive quantization |

## Integration with Other Tools

**Combined optimization pipeline:**
```bash
# 1. Reduce polygons with decimate (if needed)
# 2. Apply meshopt for reordering/quantization
gltf-transform optimize model.glb output.glb \
  --draco \
  --meshopt \
  --texture-compress webp
# 3. Result: geometry compressed (Draco) + vertex cache optimized (meshopt)
```

## Tools & Commands

- **gltf-transform CLI**: Official toolchain, supports Draco compression
- **gltfpack**: Command-line tool from meshoptimizer team
- **Babylon.js Sandbox**: Web viewer with Draco support testing

## Anti-Patterns

- Compressing already-quantized data (lossy stacking)
- Using Draco without measuring before/after filesizes
- Ignoring target platform's decode capabilities
- Setting quantization too aggressive without visual testing

## Sources

- [KHRDracoMeshCompression | glTF Transform](https://gltf-transform.dev/modules/extensions/classes/KHRDracoMeshCompression)
- [Google Draco 3D Graphics Compression](https://google.github.io/draco/)
- [Optimizing 3D Models with Draco and other tools](https://www.axl-devhub.me/en/blog/optimizing-3d-models)
- [glTF Transform CLI](https://gltf-transform.dev/cli)
