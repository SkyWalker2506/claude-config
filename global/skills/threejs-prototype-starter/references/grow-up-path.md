# Grow-Up Path

Use this only after the prototype proves the idea.

## Stage 1: Playable Prototype

Keep the default scaffold. Make the loop fun. Do not add systems that do not improve the playable test.

## Stage 2: Small Game Slice

Add structure only as pressure appears:

```text
src/
  core/
  game/
  assets/
  ui/
```

Move update loop helpers into `core/`, gameplay objects into `game/`, asset loading into `assets/`, and player-facing UI into `ui/`.

## Stage 3: Localization

When text grows beyond a few labels, use `$threejs-localize`. Centralized UI text from `ui.js` should be easy to extract into JSON catalogs.

## Stage 4: Shipping

When the game has a stable production build, use `$threejs-steam-shipper`. Keep:

- `npm run build` producing `dist/`,
- Vite `base: './'`,
- runtime assets copied from `public/`,
- adaptive controls that can switch between desktop keyboard/mouse/gamepad and mobile touch/Cordova,
- no secrets or draft files in `public/`.

Do not convert to Electron, Cordova, or Steam packaging until the browser build works cleanly.
