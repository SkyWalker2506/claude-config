# Asset Pipeline

## Route Summary

Use `imagegen` to create master character and master pose references. Use TRELLIS.2 only for image-to-3D generation when its runtime is ready. Use Blender MCP when connected, otherwise Blender Python/CLI or manual Blender. Use Make-It-Animatable for humanoid rigging when installed, and Mixamo when the user can complete Adobe login/upload/download steps.

## TRELLIS.2 Notes

TRELLIS.2 is an image-to-3D model that outputs textured meshes with PBR materials. Its official model is MIT licensed, but it is heavy: the public requirements mention Linux, NVIDIA GPUs with at least 24GB memory, CUDA, Conda, and Python 3.8+.

Do not run or download TRELLIS.2 silently. If `TRELLIS2_PATH` is missing or the machine is not suitable, create imagegen references and the plan, then list install/run steps.

Good TRELLIS input:

- Neutral full-body character, front 3/4 or orthographic-ish view.
- Plain background, full silhouette, visible hands/feet/headgear.
- No dramatic lens distortion, motion blur, text, watermark, or heavy shadow.
- For game characters: clear material zones and readable costume colors.

## Optimization Targets

Pick a budget based on camera distance and platform:

- Mobile/background NPC: 2k-8k triangles, 512-1024 textures.
- Desktop stylized hero: 10k-35k triangles, 1k-2k textures.
- Close-up hero/cinematic: 35k-80k triangles, 2k-4k textures, then make LODs.

Preserve deformation loops around shoulders, elbows, hips, knees, neck, jaw, and any tail/wings. Avoid over-decimating hands and face if animations need them.

## Blender Cleanup

Use Blender MCP if reachable. If not, ask the user to open Blender and enable the addon, or use Blender CLI scripts.

Required cleanup:

- Apply scale and transforms.
- Set origin at feet/center or project convention.
- Normalize forward/up orientation for Three.js: Y-up in glTF, character visually facing project forward.
- Remove hidden junk, duplicate meshes, non-renderable helper pieces, and tiny floaters.
- Merge or keep materials intentionally; rename meshes/materials/armature with stable names.
- Export GLB with animations, skinning, tangents when needed, and embedded or adjacent textures.

## Rigging Routes

Use this order for humanoid characters:

1. Make-It-Animatable if installed and suitable for the mesh.
2. Mixamo if the user can upload FBX/OBJ/ZIP and download rigged FBX/animations.
3. Blender manual/auto-rig fallback when AI rigging is unavailable.

For Make-It-Animatable, treat it as an external ML dependency: check repo/model weights before claiming success. It targets fast rigging/skinning/pose transforms for humanoid 3D models.

For Mixamo:

- Upload FBX for rigged assets, or FBX/OBJ/ZIP for unrigged custom characters.
- Use embedded media for FBX textures; ZIP OBJ/MTL/textures together if using OBJ.
- Place markers carefully on wrists, elbows, knees, and groin.
- Download the rigged character and selected animations.
- Import into Blender, retarget/bake if needed, then export GLB.

## Animation QA

Check idle, walk, run, jump, attack, and any requested clips:

- Feet do not slide badly unless intentionally stylized.
- Shoulders/elbows/knees bend cleanly.
- Weapon/tool attachments stay aligned.
- Root motion is either intentionally preserved or removed.
- Animation names are readable in Three.js.
- Loop clips loop; one-shot clips stop or clamp as expected.
