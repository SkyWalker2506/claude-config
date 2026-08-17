# Spritesheet Art Direction

## Master Character First

Before spritesheet generation, define the character as if it were a tiny production bible:

- Role and fantasy: player hero, enemy, NPC, vehicle, mascot, boss, companion.
- Silhouette: head/body ratio, stance, readable weapon/tool, distinctive outline.
- Palette: 3-6 key colors, contrast priority, team/faction colors.
- Materials: cloth, armor, slime, stone, neon, leather, glass, fur, metal.
- Camera: top-down, 3/4 isometric, side-view platformer, orthographic, UI portrait.
- Scale: intended in-game frame size and final export scale.
- Animation needs: idle, walk, run, attack, cast, jump, hurt, death, interact.

Use `imagegen` to create the master character when there is no strong reference image. The master image should be clean, readable, full body, uncropped, and close to the game camera.

## Master Pose And Turnaround

When consistency matters, create a master pose sheet before the final animation sheet:

- Neutral stance, front/side/back or isometric directions.
- Same outfit and colors in every view.
- No dramatic lighting that hides shape.
- Plain removable background.
- No weapon crossing important body landmarks unless required.

For pixel art, ask for crisp sprite pixels, limited palette, orthographic camera, no anti-aliased blur, and clear frame boundaries.

## Prompt Pattern

Use this pattern and adapt it to the selected route:

```text
<route trigger if required>, <grid description>, <character bible summary>,
<camera/view>, <motion/state>, <art style>, <palette>, <game genre>,
consistent proportions, consistent outfit, centered in every frame, clean frame grid,
plain removable background
```

Negative constraints:

```text
extra limbs, duplicate character in one frame, cropped head, cropped weapon,
inconsistent costume, perspective mismatch, blurry pixels, uneven frame size,
text labels, watermark, noisy background, overlapping frames
```

## State Layout

Write row/column expectations explicitly. Examples:

- 4x4 walk sheet: row 1 down, row 2 left, row 3 right, row 4 up/back.
- 2x2 multiview: top-left isometric front-right, top-right isometric front-left, bottom-left side-left, bottom-right top-down.
- Platformer strip: columns are sequential frames left-to-right for one motion state.

If the target game already has a JSON atlas format, match it instead of inventing a new layout.

## Validation Pass

After generation, inspect the sheet:

- Does each cell contain exactly one complete character?
- Are all frames the same size and aligned to the same baseline?
- Does the camera angle match each requested row?
- Does the outfit remain the same?
- Are transparent pixels/background cleanup acceptable?
- Does a test preview animate without position popping?
- Is the final sheet saved in the game asset folder and documented in metadata?

If a generated sheet fails only one row or state, regenerate that state with tighter instructions rather than discarding a good master character.
