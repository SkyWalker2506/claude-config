# Learnings

Durable rules distilled from actual outcomes. Add only what a future session MUST know.

## Hard-learned
- **DALL-E/GPT will crop figures at the top of the frame unless you explicitly cap the character height AND give a pixel margin above the head.** (blacksmith_swing_6f + blacksmith_idle_4f, Apr 2026)
- **"Transparent background" is silently ignored by DALL-E.** Always magenta (#FF00FF) bg + downstream magick post-process. (Confirmed 2x at MedievalFactory, Apr 2026.)
- **GPT Sources tab does NOT affect DALL-E output.** Style reference must be encoded entirely in text. (Two live tests.)
- **Rotation-based animation (wheels, gears) cannot be produced by GPT/DALL-E.** Always fallback to ImageMagick rotate+append. (cart_wheels_8f failed 3 times.)
- **Without "body IDENTICAL across frames, feet anchored at same y" the character silhouette drifts.** Make it a fixed prompt block.

## Meta
- The cost of a strict prompt is one paragraph; the cost of a rejected generation is a full GPT cycle + human review. Lean heavily on the strict side.
- ASCII-only in copyable prompts. Smart quotes and em-dashes break when user pastes into other tools. (feedback_ascii_prompts memory.)
