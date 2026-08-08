# Adaptive Controls

Research baseline: checked against MDN Pointer Events, MDN Gamepad API, CSS safe-area `env()`, and Apache Cordova events on 2026-08-08.

## Rule

Keep gameplay code device-agnostic. The scene should read intent:

- `moveX`: -1 left to 1 right.
- `moveY`: -1 forward/up to 1 back/down.
- `action`: primary action.
- optional `aimX`, `aimY`, `pause`, or `secondary` only when the mechanic needs them.

The input module decides how that intent is produced.

## Target Profiles

- Desktop web or Steam/Electron: keyboard first, pointer/mouse for aim or action, Gamepad API polling when a controller is connected.
- Mobile browser: Pointer Events touch overlay, large hit areas, `touch-action: none` on the game surface, no hover-only controls.
- Cordova mobile: same touch overlay plus `deviceready`, `pause`, `resume`, Android back button, safe-area CSS, orientation/resize checks.
- WebGPU/high-end web: controls should not depend on the renderer. Test the same input state on WebGPU and forced WebGL fallback.

Allow a QA override such as `?controls=desktop`, `?controls=touch`, or `?controls=gamepad`.

## Implementation Notes

- Prefer Pointer Events over separate mouse/touch handlers. Use `pointerType` only when behavior truly differs.
- Keep pointer handlers on specific game/control elements and keep them light.
- For virtual sticks, call `setPointerCapture()` on `pointerdown` and release/reset on `pointerup`, `pointercancel`, and lost capture.
- Poll gamepads inside the animation loop or an `input.update()` call; do not wait for button events for moment-to-moment movement.
- Use `navigator.maxTouchPoints`, `(pointer: coarse)`, and Cordova presence as hints, not permanent truth. Hybrid laptops exist.
- Do not hide keyboard controls just because touch exists; let the latest active input win.
- Put safe-area padding in CSS with `env(safe-area-inset-*)`.
- Pause expensive work or show a paused state on Cordova/browser `pause`/`visibilitychange`, then resume cleanly.

## QA Checklist

- Desktop: WASD/arrows, pointer action/aim, resize, fullscreen/pointer-lock if used.
- Gamepad: connect after page load, disconnect, analog deadzone, primary button, browser focus.
- Mobile browser: one-finger movement, action button, orientation change, accidental page scroll/zoom prevention.
- Cordova: `deviceready`, pause/resume, Android back button, safe areas/notches, real-device performance.
- Shipping handoff: `$threejs-steam-shipper` can copy the same `dist/` to Steam, web, or Cordova without changing gameplay input code.
