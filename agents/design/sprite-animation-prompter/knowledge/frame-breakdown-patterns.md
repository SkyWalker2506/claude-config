# Frame breakdown patterns

## Goal
Each frame line must be a single clear delta from the previous — not a free narrative.

## Structural template

For N-frame loop:
```
F1: [base pose / neutral]
F2: [delta 1 — one specific change]
F3: [delta 2 — progressing]
F4: [peak / climax]
F5: [return delta]
F6: [near-base, smooth back to F1]
```

## Character action (swing/strike)

4-frame strike loop:
```
F1: weapon raised at peak position.
F2: weapon mid-arc, 45deg downswing, motion blur streak.
F3: IMPACT on target with sparks/dust.
F4: slight recoil, halfway back to raised.
```

6-frame strike loop:
```
F1: weapon at peak (raised).
F2: weapon 30deg from vertical.
F3: weapon at 60deg, accelerating.
F4: IMPACT frame with brightest sparks.
F5: weapon bouncing back ~30deg above target.
F6: halfway back to peak (smooth loop).
```

8-frame walk/run cycle:
```
F1: contact (left foot forward, right heel lifting).
F2: down (body lowest).
F3: passing (body center, legs crossing).
F4: high point.
F5: contact (mirrored — right foot forward).
F6: down.
F7: passing.
F8: high point (loops to F1).
```

## Idle breathing

4-frame breathing loop:
```
F1: rest pose.
F2: gentle inhale, shoulders up 2px, chest subtle expand.
F3: peak inhale, chest fully expanded, head tilts 1-2px.
F4: exhale, settling back to F1.
```

## FX particles (fire / smoke)

6-frame loop:
```
F1: small/base intensity.
F2: growing, slight drift.
F3: intensity 70%, sparks/wisps.
F4: PEAK — brightest/tallest.
F5: settling 60%.
F6: back to ~F1 (seamless loop).
```

## Loop closure rule
Always end FN close to F1. Explicit: "F_N is halfway back to F1 for seamless loop."

## Motion primitives to avoid
- "The character walks a few steps" (vague)
- "Swings dramatically" (no specific delta)
- "With energy" (subjective)

## Motion primitives to prefer
- "raised overhead both hands" (unambiguous pose)
- "45deg from vertical" (measurable)
- "shoulders up 2px" (delta in pixels)
- "IMPACT frame with bright sparks" (named keyframe)
