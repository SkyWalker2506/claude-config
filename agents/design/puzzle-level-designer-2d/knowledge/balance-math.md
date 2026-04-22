# Balance Math — Golf Paper Craft

Menzil ve kuvvet hesapları. Level tasarlarken bu tabloyu referans al.

## Constants (2026-04-22)
- `SHOT_FORCE` = 0.156 (daha önceden 0.26'ydı, %40 indirildi)
- `DRAG_TIERS` = `[140, 170, 200, 230]` (Power Control tier 1-4, px)
- `gravity` = 1.3 (engine.gravity.y)
- ball: `density: 0.003`, `restitution: 0.52`, `friction: 0.04`, `frictionAir: 0.014`, radius 16 → mass ≈ 2.413
- Trampoline launch: `clamp(|vy_in| * 1.25, 22, 32)` px/frame
- Bridge bounce: `vy_out = vy_in × -0.18` (heavy damp)
- Ball grass drag: `vx *= 0.965` per frame while on grass

## Impulse → velocity
```
v0 = (SHOT_FORCE × drag_px) / mass
   ≈ drag × 0.0647   (px/frame at 60fps)
```
- Tier-1: v0 ≈ 9.06
- Tier-4: v0 ≈ 14.88

## Empirical range (45° flat ground with air friction)
| Tier | Drag | v0    | Range    |
|------|------|-------|----------|
| 1    | 140  | 9.06  | ~325 px  |
| 2    | 170  | 11.00 | ~400 px  |
| 3    | 200  | 12.94 | ~485 px  |
| 4    | 230  | 14.88 | ~570 px  |

## Design rules
`d = hole.x - ballStart.x` (level horizontal distance)

- `d ≤ 325` → tutorial only, tek atışla geçilebilir
- `325 < d ≤ 570` → skill-required single-shot possible (tier-3/4 + doğru açı)
- `d > 570` → multi-shot mandatory (PASSes brute-force check automatically)

## Height clearance for high-arc bypass
Tier-4 max height at steep angle ≈ v0² / (2g) ≈ 85 px (y_above_ground). Engellerin top-of-viewport height'ı:
- Hill r=30: top at GY − 30
- Tree canopy: top at GY − h (varsayılan 120)
- Tramp airborne y=GY-36: top at GY-42

Player tier-4 arc yukseltisinin ~85px üstündeki engeller geçilemez → bypass-proof.

## Single-shot worst case
Tier-4 + optimum 45°: ~570 px net. Bunun üstüne tepe/ağaç eklersen gerçek geçiş ≤ 500 px olur. Puzzle dizaynında bunu hesaba kat.
