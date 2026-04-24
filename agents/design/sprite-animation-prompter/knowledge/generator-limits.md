# Generator limits — when to NOT use DALL-E/GPT

## Known failures (do NOT ask generator for these — use script fallback)

### Rotation (wheels, gears, turbines)
- GPT cannot produce consistent rotation across frames. Tested 3x at MedievalFactory (cart_wheels_8f) — all frames looked identical OR the generator added extra wheels.
- **Fallback**: render a single wheel PNG, then ImageMagick rotate + append.
  ```bash
  for a in 0 45 90 135 180 225 270 315; do
    magick wheel.png -rotate $a frame_$a.png
  done
  magick frame_*.png +append cart_wheels_8f.png
  ```

### Pixel-perfect loops (seamless treadmill scrolling tiles)
- Continuous tiling requires sub-pixel accuracy. Use a script to tile a single tile.

### Text/numbers/signs
- Ask for shapes, never text. Negative: "NO text, NO numbers, NO letters".

### Anatomical precision (individual fingers in action)
- DALL-E hand quality is inconsistent. Frame-to-frame hand coherence is worse.
- Workaround: describe the hand as gloved/fist/wrapped — simpler silhouette.

### 3D parallax / depth-changing
- Walking INTO the frame or angle changes confuse the model.
- Keep a single camera angle (isometric 3/4 or profile) and only move limbs.

## Safe territory (DALL-E usually nails)

- Fire/smoke/particles (6-8 frame loops)
- Slight body-pose deltas (breathing, breathing-at-rest)
- Impact flashes (a single IMPACT frame with sparks)
- Color/brightness changes (day/night, torch glow pulse)

## Decision rule

Before writing the prompt, ask:
1. Does the animation require a mechanical rotation? -> SCRIPT
2. Does it require coherent rigid transforms? -> SCRIPT
3. Does it require text/numbers? -> SCRIPT (or asset with rendered text overlay)
4. Otherwise -> GPT/DALL-E, with strict framing + body-identical rules.

If SCRIPT path, output the ImageMagick/script command INSTEAD of a prompt, plus a short README on what source image is needed.
