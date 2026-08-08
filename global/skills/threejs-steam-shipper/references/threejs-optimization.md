# Three.js Optimization Notes

Use this when the project contains sizable models/textures, slow startup, frame drops, shader stalls, or large bundles. Optimize only after measuring or identifying obvious waste.

## Asset Pipeline

For glTF/GLB assets, prefer reproducible CLI transforms over manual exports. Good first pass:

```bash
npx @gltf-transform/cli inspect input.glb
npx @gltf-transform/cli optimize input.glb output.glb --compress meshopt --texture-compress webp
```

Consider KTX2/Basis texture compression when GPU memory or download size matters:

```bash
npx @gltf-transform/cli optimize input.glb output.glb --compress meshopt --texture-compress ktx2
```

Use Meshopt for fast decompression and runtime-friendly geometry. Use Draco only when stronger geometry compression is worth slower decode and loader complexity. Test both on the target scene before converting every asset.

Keep original art sources outside the Steam depot. Store optimized runtime assets in `public/`, `assets/`, or the project's established runtime asset folder.

## Texture Rules

- Cap texture dimensions to the smallest acceptable size for gameplay camera distance.
- Generate mipmaps for minified textures.
- Prefer KTX2/Basis or WebP for runtime assets, but verify loader support in the project.
- Do not compress normal maps blindly; check visual quality and tangent-space behavior.
- Use atlases where it reduces material count and draw calls without harming streaming.

## Runtime Rules

- Reduce draw calls before obsessing over triangle count.
- Share geometries, materials, and textures.
- Dispose unused geometries, textures, render targets, and materials.
- Lazy-load heavy scenes and models; keep the first interactive frame small.
- Avoid per-frame allocations in animation loops.
- Avoid expensive shadows on every light; tune shadow map size and caster count.
- Pause or reduce work when menus/settings overlays are open.
- Use object pooling for repeated projectiles, particles, and temporary meshes.
- Budget mobile WebView builds separately: lower default pixel ratio, cap shadow quality, and test texture memory on real devices.
- Keep WebGPU enhancements progressive. If WebGL fallback is required, avoid compute-only gameplay logic or materials that cannot render acceptably on WebGL2.

## Bundle And Loading

- Build production mode only.
- Remove sourcemaps from release unless explicitly needed.
- Split large optional scenes/routes when the existing bundler supports it.
- Ensure assets are addressed with relative URLs compatible with Electron `file://`.
- If using workers/WASM/decoders, verify packaged paths for `draco/`, `basis/`, `meshopt_decoder`, and similar files.

## Measurement

Record before/after:

- initial package size,
- largest assets,
- startup time to first rendered frame,
- average FPS and worst frame time in the heaviest scene,
- renderer info such as draw calls, triangles, textures, and shader programs.
- WebGPU vs forced-WebGL FPS, startup, memory, and visual parity when the WebGPU path is enabled.
- mobile device FPS, context loss behavior, texture memory, and resume-after-background behavior for Cordova exports.

Prefer a small, documented optimization pass over sweeping asset rewrites that may break names, animations, or material assumptions.
