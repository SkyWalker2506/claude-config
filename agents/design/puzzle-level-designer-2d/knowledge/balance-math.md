# Balance Math (Universal Method)

This file is **universal methodology only**.

All game-specific numeric constants (e.g. `SHOT_FORCE`, drag tiers, gravity, friction, empirical ranges) must live under:

`../game-packs/<game>/physics-constants.md` and/or `../game-packs/<game>/balance-math.md`

## What to compute (per game-pack)
- Max-power / max-upgrade shot envelope (range + height) for the player verb set.
- Typical ranges for tiers (if tiers exist) and angle sensitivity.
- “Bypass checks”: can the player brute-force a level with max power/precision?

## How to use it in level design
1. Compute the **baseline shot envelope**.
2. Place blockers so “full power + flat shot” does not trivialize the level (unless tutorial by intent).
3. If using tiers/upgrades, ensure multi-shot alternatives exist for low tiers.
4. Ensure any “hard gate” is readable (player can understand why they failed).

## Required outputs (when writing a level spec)
- Brute-force check result (flat max power).
- High-arc bypass check result (max-tier steep arc).
- Upgrade bypass check result (if upgrades exist).
