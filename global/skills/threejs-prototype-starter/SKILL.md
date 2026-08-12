---
name: threejs-prototype-starter
description: Create and iterate simple playable Three.js prototypes with index.html, separate ESM JavaScript modules, and adaptive desktop/mobile controls. Use when Codex is asked to quickly prototype a Three.js game/mechanic/visual idea, scaffold a minimal playable browser prototype, add PC keyboard/mouse/gamepad controls, add mobile/Cordova touch controls, keep code lightweight, or prepare an early prototype that can later work with localization and threejs-steam-shipper Steam/web/mobile export skills.
---

# Three.js Prototype Starter

## Goal

Create a tiny playable Three.js prototype quickly, without overengineering. Start with `index.html` and separate ESM modules, keep the code easy to iterate, and leave a clean path toward `$threejs-localize` and `$threejs-steam-shipper` Steam/web/mobile exports if the idea becomes serious.

## Before You Scaffold — Read The Brief, Do Not Assume

Three.js is the *renderer*, not the art direction. Never infer a 3D game from
the fact that this skill is Three.js.

1. **Perspective and art style come from the brief/GDD, never from a default.**
   If the GDD says "2D", "2.5D", "top-down", "isometric", "pixel art",
   "sprites", "low-res painted sprites", or names sprite resolutions
   (e.g. `64x64`), the prototype is a **sprite** game: textured quads /
   `THREE.Sprite` / billboards on an orthographic camera. Boxes and meshes are
   NOT an acceptable stand-in for sprites — they change the whole read of the
   game.
2. **Only build meshes/3D geometry when the brief explicitly asks for it.**
   If the brief is silent about perspective and style, ask one short question
   before scaffolding. Do not "pick something sensible and move on".
3. **Placeholder art still has to be the right kind of art.** For a sprite
   game, generate placeholder sprite textures (canvas-drawn or generated
   images) instead of substituting primitives.
4. **Show concept art first when the brief has an art direction section.**
   Use the image-generation skill (`$image-prompt` / `$image-run`) to produce
   concept frames in the stated style and confirm the look with the user
   *before* writing gameplay code. Wiring a whole prototype in the wrong
   visual language wastes the run.

## Default Shape

Use this structure for new prototypes:

```text
target-project/
  index.html
  package.json
  vite.config.js
  src/
    main.js
    scene.js
    input.js
    ui.js
    styles.css
  public/
    assets/
```

This is intentionally small:

- `index.html` only loads `src/main.js`.
- JavaScript files use ESM imports/exports.
- Vite handles dev server and production `dist/`.
- `vite.config.js` uses `base: './'` so future Electron/Steam packaging can load assets from `file://`.
- Input uses one gameplay intent shape (`moveX`, `moveY`, `action`) while `input.js` chooses keyboard/mouse/gamepad or mobile touch controls from device capability and target.
- UI text lives in `ui.js` constants/functions first, so `$threejs-localize` can later extract it cleanly.

## Workflow

1. **Scaffold if needed.**

   ```bash
   node <skill>/scripts/scaffold-threejs-prototype.mjs <target-project> --name "Prototype Name"
   ```

   The script creates missing files only. It does not overwrite existing prototype code.

2. **Implement the idea directly.**
   - Put renderer/camera/bootstrap in `main.js`.
   - Put scene objects and update loop logic in `scene.js`.
   - Put keyboard, pointer/touch, and gamepad state in `input.js`.
   - Put DOM labels/buttons/help text in `ui.js`.
   - Put CSS in `styles.css`.
   - Keep scene code platform-agnostic: consume `input.state.moveX`, `input.state.moveY`, and action flags instead of checking `window`, `cordova`, keyboard keys, or touch state inside gameplay.

3. **Keep iteration fast.**
   - Prefer one playable mechanic over menus, settings, save systems, assets, or polish.
   - Use primitives and simple materials before importing models.
   - Add only the controls needed to test the idea.
   - Keep functions small and obvious; avoid frameworks until the prototype earns them.

4. **Run locally.**

   ```bash
   npm install
   npm run dev
   ```

   If another server is already running, use Vite's next available port.

5. **Make it future-compatible.**
   - Use relative asset URLs and `public/assets/`.
   - Keep player-facing text centralized in `ui.js` or a small object, not scattered across render code.
   - Avoid build-only or draft files under `public/`.
   - Keep source code clean enough that `$threejs-localize` can scan it and `$threejs-steam-shipper` can build/package `dist/` for Steam, web, or Cordova mobile.
   - Add target override query params for QA when useful: `?controls=desktop`, `?controls=touch`, `?controls=gamepad`.
   - For Cordova/mobile, use touch controls, safe-area CSS, pause/resume hooks, and real-device checks before treating the prototype as shippable.
   - For PC/Steam/web desktop, keep keyboard/mouse usable and poll the Gamepad API when a controller is connected.

6. **Check controls on target devices.** Load `references/adaptive-controls.md` before adding or changing controls. Verify desktop keyboard/mouse, optional gamepad, mobile browser touch, and Cordova touch behavior according to the target the user wants to build.

7. **When the prototype grows.** Load `references/grow-up-path.md` before restructuring toward a bigger app/game. Move deliberately: introduce folders, state management, asset pipelines, localization, and Steam/web/mobile packaging only when the prototype needs them.

## Compatibility

This skill works standalone. It does not require `$threejs-localize` or `$threejs-steam-shipper`.

If those skills are later used:

- `$threejs-localize` can extract UI strings from `src/ui.js`.
- `$threejs-steam-shipper` can run the Vite production build and copy `dist/` into `buildable/steam-electron/web/`, `buildable/web/dist/`, or `buildable/mobile-cordova/www/`.
- `base: './'` avoids common Electron `file://`, static subfolder, and Cordova `www/` asset path failures.
- The adaptive input layer lets each export target use the right controller without changing gameplay code: PC uses keyboard/mouse/gamepad, mobile/Cordova uses touch controls.

## References

- Read `references/prototype-pattern.md` for file responsibilities and anti-overengineering rules.
- Read `references/adaptive-controls.md` before implementing controls for PC, web, mobile browser, or Cordova.
- Read `references/grow-up-path.md` before turning a prototype into a more serious project.
