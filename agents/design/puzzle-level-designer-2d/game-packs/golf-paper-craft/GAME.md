# Golf Paper Craft — Game Pack

## Genre
Cozy physics mini-golf (2D, canvas-based, physics puzzles).

## Camera / Perspective
2D side view, left-to-right play, wide levels with camera scrolling.

## Platform
Web (HTML5 Canvas) + mobile wrapper.

## Core loop
Aim → drag-power → release → observe physics → retry → hole-out → stars/rewards.

## Player verb set
- Aim + power (drag)
- Shoot
- Retry / reset (fast)
- Optional: upgrades affect power/precision/assist (game-specific)

## Design pillars (from project)
- Paper-craft readability & warmth
- Deterministic physics (same input → same outcome)
- “One puzzle, one lesson” progression

## Constraints
- Use only implemented mechanics listed in `mechanics.md`.
- Numeric constants must be sourced from `physics-constants.md`.
- Game-specific progression rules live in `progression.md` and `level-rules.md`.
- Game-specific playtest plan lives in `playtest-notes.md`.

