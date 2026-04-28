# Physics Constants — Golf Paper Craft

Only Golf Paper Craft-specific numeric values belong here.

## Constants (2026-04-22)
- `SHOT_FORCE` = 0.156
- `DRAG_TIERS` = `[140, 170, 200, 230]` (Power Control tier 1–4, px)
- `gravity` = 1.3 (engine.gravity.y)
- ball: `density: 0.003`, `restitution: 0.52`, `friction: 0.04`, `frictionAir: 0.014`, radius 16 → mass ≈ 2.413
- Trampoline launch: `clamp(|vy_in| * 1.25, 22, 32)` px/frame
- Bridge bounce: `vy_out = vy_in × -0.18` (heavy damp)
- Ball grass drag: `vx *= 0.965` per frame while on grass

