# Three.js Character Previewer

The previewer is a local QA tool, not the production game scene.

It should support:

- Drag/drop `.glb` and `.gltf` files into the browser.
- OrbitControls mouse drag rotation, wheel zoom, and pan.
- Animation list from `gltf.animations`.
- Play, pause, stop, previous/next clip, and time scrub.
- Playback speed control.
- SkeletonHelper toggle.
- Wireframe toggle.
- Auto-frame camera after model load.
- Basic environment lighting, grid, and axes.

Validation checklist:

- Model appears upright and centered.
- Materials and textures render.
- Animation clips are detected by name.
- Scrub slider follows playback and can seek.
- Skeleton helper aligns with mesh.
- No console errors after repeated drag/drop loads.
