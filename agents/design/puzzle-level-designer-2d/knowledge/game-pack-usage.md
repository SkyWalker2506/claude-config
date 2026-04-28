# Game-pack usage (Universal)

## Purpose
Keep game-specific knowledge (mechanics, constants, schemas, dimensions, upgrade tiers, naming) **out of core** while guaranteeing D14 uses it during design.

## Definitions
- **Core knowledge**: universal methodology, patterns, validation, analysis.
- **Game-pack**: one game’s authoritative rules + numbers + mechanics list + placement exceptions + validation overrides.

## Non-negotiable rule
If the game is known and a corresponding game-pack exists, D14 must:
1. Load it (mentally, by citing the pack path and key constraints), and
2. Run pack validation overrides,
before emitting any **final** level spec or review verdict.

## What “load a game-pack” means (required evidence)
In the output, include a short “Game-pack loaded” line that names:
- pack path (e.g. `game-packs/golf-paper-craft/`)
- mechanic source (`mechanics.md`)
- physics/balance source (`physics-constants.md` / `balance-math.md`)
- pack-specific overrides (`validation-overrides.md`)

Example:
```txt
Game-pack loaded: golf-paper-craft (mechanics.md, physics-constants.md, validation-overrides.md)
```

## If a game-pack does not exist
D14 may proceed only if it creates a temporary **Design Brief** section:
- assumptions
- known mechanics list (explicitly “assumed”)
- unknowns + risks
- what must be confirmed by engineering (handoff notes)

## Separation policy
- Core files must never contain game constants like `SHOT_FORCE=...`.
- Game-packs must never redefine universal principles (they only override/extend).

