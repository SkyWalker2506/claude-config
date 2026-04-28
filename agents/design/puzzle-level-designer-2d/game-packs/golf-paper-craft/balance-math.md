# Balance Math — Golf Paper Craft

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

## Design rules (distance heuristics)
`d = hole.x - ballStart.x`

- `d ≤ 325` → tutorial only, single-shot reachable
- `325 < d ≤ 570` → single-shot possible with tier-3/4 + correct angle
- `d > 570` → multi-shot mandatory (brute-force bypass naturally blocked)

## Height clearance for high-arc bypass
Tier-4 max height at steep angle ≈ v0² / (2g) ≈ ~85 px (y_above_ground). If blockers exceed this (relative to ground), high-arc bypass is blocked.

