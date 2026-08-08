# Prototype Pattern

## File Responsibilities

- `index.html`: root DOM only; load `src/main.js`.
- `src/main.js`: renderer, camera, resize, animation loop, module wiring.
- `src/scene.js`: Three.js scene creation, gameplay objects, update function.
- `src/input.js`: adaptive input state for keyboard, pointer/touch, and gamepad.
- `src/ui.js`: DOM text, HUD updates, restart/help buttons.
- `src/styles.css`: page/HUD styling.

## Do

- Make one mechanic playable first.
- Use simple geometry and material colors.
- Keep UI text centralized.
- Keep gameplay input as intent (`moveX`, `moveY`, `action`) instead of platform checks.
- Use Pointer Events for mouse/touch/pen and show virtual controls only for touch/mobile targets.
- Use `public/assets/` for images/models/audio.
- Keep Vite `base: './'`.
- Build often with `npm run build`.

## Avoid

- React/Vue/Svelte for the first draft unless the user asks.
- Entity-component systems.
- Complex routers, stores, menus, saves, accounts, or installers.
- Premature asset pipelines.
- Large class hierarchies.
- Separate mobile and desktop gameplay branches.
- Hidden global constants scattered across files.

## Good First Mechanics

- Move/jump/dash feel.
- Camera orbit or chase behavior.
- Physics toy.
- Puzzle interaction.
- Procedural layout.
- Enemy steering.
- Visual shader or particle experiment.
- Satisfying loop suitable for a GIF hook.
