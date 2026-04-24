# Framing Rules (MUST appear in every character/creature prompt)

## The rule
```
FRAMING (CRITICAL): Entire figure including full top of head must fit inside the NxN frame. Top of head at least 20px below the top edge. Feet at least 10px above the bottom edge. Character height max ~220px for a 256-tall frame (scale proportionally for other heights: ~85% of frame height). If the figure does not fit, shrink the whole composition — do NOT crop.
```

## Why it matters
- DALL-E/GPT default composition fills the canvas; heads routinely clip at top.
- "Full body" alone is insufficient — the model still crops top/bottom often.
- Explicit pixel margins + height cap reduce regeneration rate significantly.

## Overhead motion edge case
If the motion requires arms/tools ABOVE the head (hammer raised, sword overhead, pickaxe up):
- Add: "If tool would extend past top edge at peak, lower the peak pose to 45deg instead of vertical."
- OR: "Anchor the tool to still fit inside frame — tool tip at least 10px below top edge."

## Width margin
Usually less critical for single-frame figures, but if the asset moves horizontally across frames:
- Add: "Figure centered horizontally within each frame cell. Lateral margin at least 15px each side."

## Verification (visual)
When reviewing generated strip:
- [ ] Top of head visible (hair/helmet/cap fully rendered)?
- [ ] Feet visible (not cut at ankle)?
- [ ] Tool at peak pose not clipped?
- [ ] Any shadow below figure inside frame (not cut off)?
If any fail -> reject, revise prompt.
