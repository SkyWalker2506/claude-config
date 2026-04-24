# Knowledge Index — Sprite Animation Prompter

Lazy-load. Read only what the current task needs.

| File | When to read |
|------|--------------|
| [framing-rules.md](framing-rules.md) | Every character or creature sprite prompt |
| [failure-modes.md](failure-modes.md) | Before writing — avoid known traps |
| [frame-breakdown-patterns.md](frame-breakdown-patterns.md) | When designing frames for a new motion |
| [background-conventions.md](background-conventions.md) | Always (magenta vs transparent) |
| [generator-limits.md](generator-limits.md) | When asset type is mechanical/rotational or needs pixel precision |
| [style-vocabulary.md](style-vocabulary.md) | Matching existing game art style |

## Bootstrap checklist (every task)
1. Read `framing-rules.md` + `background-conventions.md` (always).
2. If character/creature: read `frame-breakdown-patterns.md`.
3. If mechanical (wheels, gears, rotation): read `generator-limits.md` first — may need script fallback.
4. If style-matching to existing game: read `style-vocabulary.md`.
