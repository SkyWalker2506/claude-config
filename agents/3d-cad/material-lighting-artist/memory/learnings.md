# Learnings

## 2026-04-14 — Knowledge Base Initial Fill (opus-4.6)

### Blender Version Differences (CRITICAL)

1. **Principled BSDF Breaking Changes in 4.0:**
   - `Subsurface` -> `Subsurface Weight`
   - `Subsurface Color` -> REMOVED (uses Base Color)
   - `Specular` -> `Specular IOR Level`
   - `Clearcoat` -> `Coat Weight`
   - `Sheen` -> `Sheen Weight`
   - `Transmission` -> `Transmission Weight`
   - `Emission` -> `Emission Color`
   - New inputs: Subsurface Scale, Subsurface IOR, Coat IOR, Coat Tint, Sheen Roughness
   - Blender 4.3 added: Diffuse Roughness
   - Blender 4.2 added: Thin Film Thickness, Thin Film IOR

2. **Musgrave Merger in 4.1:**
   - `ShaderNodeTexMusgrave` deprecated, merged into `ShaderNodeTexNoise`
   - Use `noise_type` property: 'FBM', 'MULTIFRACTAL', 'HYBRID_MULTIFRACTAL', 'RIDGED_MULTIFRACTAL', 'HETERO_TERRAIN'
   - Dimension parameter replaced by Roughness (Roughness = Lacunarity^(-Dimension))

3. **EEVEE engine name history:**
   - 4.0-4.1: `BLENDER_EEVEE` (old EEVEE)
   - 4.2-4.x: `BLENDER_EEVEE_NEXT` (EEVEE Next rewrite with ray-tracing)
   - 5.x: `BLENDER_EEVEE` (EEVEE Next renamed back; BLENDER_EEVEE_NEXT removed)
   - Some settings APIs changed between old and new EEVEE

4. **MixRGB Deprecation in 4.0:**
   - `ShaderNodeMixRGB` -> `ShaderNodeMix` with `data_type='RGBA'`

### PBR Best Practices

- Metallic MUST be binary (0 or 1) — never intermediate values
- Minimum roughness: 0.02 (no perfect mirrors in reality)
- SSS Weight for skin: 0.1-0.2 (higher looks waxy/unreal)
- Subsurface Radius always R > G > B for organic skin (blood scatters red)
- Default SSS radius (1.0, 0.2, 0.1) is physically motivated

### Lighting Guidelines

- Character key light energy formula: height_meters * 200-400 watts
- Fill = key * 0.3-0.4, Rim = key * 0.5-0.7
- Area light size = character_height * 1.5 for natural softness
- Warm key (1.0, 0.95, 0.85) + cool fill (0.85, 0.90, 1.0) creates depth
- World background: 0.02-0.05 gray at 0.05-0.1 strength for studio look

### Version-Safe Code Pattern

Always use try/except when accessing shader node inputs:
```python
def safe_set_input(node, name, value, fallback_name=None):
    try:
        node.inputs[name].default_value = value
    except KeyError:
        if fallback_name:
            try:
                node.inputs[fallback_name].default_value = value
            except KeyError:
                pass
```

### Texture Scale Reference

- Skin pores: 80-200 (Voronoi F1)
- Wrinkles: 10-30 (Noise FBM)
- Muscle definition: 2-8 (Noise FBM)
- Color patches: 2-6 (Noise FBM)
- Metal scratches: 20-50 (Noise RIDGED)
