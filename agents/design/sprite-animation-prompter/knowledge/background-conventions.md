# Background conventions

## Rule: always solid MAGENTA (#FF00FF)

DALL-E and GPT image tool ignore "transparent background" even when it's the core requirement. Two generations tested at MedievalFactory; both returned opaque light backgrounds.

## What to write in the prompt

```
Solid MAGENTA (#FF00FF) background. Do NOT make transparent — render as solid fill color.
```

## Why magenta

- Unambiguous: no natural object is #FF00FF.
- Saturation-mask post-processing cleanly removes it in ImageMagick / Photoshop.
- Leaves no "halo" around the figure like a white bg would on dark objects.

## Avoid black or white backgrounds for post-processing

- Black bg: loses dark hair, shadows, iron.
- White bg: loses bright sparks, flames, light clothing.
- Solid green/blue can conflict with clothing/nature colors.

Only magenta is safe.

## Post-processing (downstream, not this agent's concern)
The asset-browser pipeline (magick script) handles the cleanup:
```
magick input.png -fuzz 15% -transparent "#FF00FF" output.png
```

## Exception: FX particles on already-transparent output
For fire/smoke/sparks where DALL-E historically does succeed at partial transparency: still request magenta bg. Post-process is cheap; failed transparency is expensive.
