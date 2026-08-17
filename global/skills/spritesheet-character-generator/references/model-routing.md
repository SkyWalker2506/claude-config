# Model Routing

This skill uses built-in `imagegen` for concept/reference work and routes final spritesheet generation to external Hugging Face LoRA workflows only when the needed runtime is available.

## Routing Table

| Need | Preferred Route | Why | Notes |
| --- | --- | --- | --- |
| Small 32x32 pixel character, 4-direction walk sheet, classic RPG movement | `svntax-dev/pixel_spritesheet_4walk_small_lora_v1` | Purpose-built 4x4 pixel spritesheet LoRA for walking up/down/left/right plus extra action frames | Apache-2.0. Use FLUX.2 Klein base 4B, not distilled. Generate 512x512, then downscale to 128x128 for pixel-perfect output. |
| 2x2 multiview reference from a master character/object image | `fal/flux-2-klein-4b-spritesheet-lora` | Image-to-image model for consistent 2x2 camera views | Apache-2.0. Prompt is usually `2x2 sprite sheet`. Recommended LoRA scale is 1.1. Output has a red background by design, so cleanup is required before game integration. |
| LPC-style top-down RPG character sheet, humanoid walk/action sheet | `Mystic07/flux-lora-spritesheet` | Trained for game sprite sheets in LPC-style pixel art | Uses trigger `gmsspritesheet`. Recommended checkpoint is `gmsspritesheet1.safetensors`; 20-40 steps, guidance 3.5-5.0, 768x768 or 1024x1024. License inherits FLUX.2-klein-base-9B and is marked non-commercial on the model page, so treat as prototype-only unless rights are verified. |
| Normal/non-pixel concept, art direction exploration, master character, master pose | `imagegen` | Fastest way to establish visual identity and references inside Codex | Good for master character, neutral pose, turnaround concept, and visual target sheet. It is not a LoRA runner. |

## Selection Rules

1. Use `svntax-dev/pixel_spritesheet_4walk_small_lora_v1` when the prompt says pixel, 32x32, 4walk, four-direction, RPG, tiny character, chibi, or movement sheet.
2. Use `fal/flux-2-klein-4b-spritesheet-lora` when the user provides or needs a single master image converted into multiple views.
3. Use `Mystic07/flux-lora-spritesheet` for LPC-like humanoid top-down sheets when non-commercial/prototype use is acceptable.
4. Use `imagegen` first whenever character identity is underspecified. A strong master reference beats repeated blind spritesheet prompts.
5. If multiple routes fit, generate the master reference with `imagegen`, then create one prompt pack per candidate route and pick the route with the cleanest license/runtime fit.

## Dependency Notes

Diffusers routes require Python, PyTorch, `diffusers`, `transformers`, `accelerate`, `safetensors`, `pillow`, and model access to the needed base model and LoRA. ComfyUI routes require ComfyUI plus downloaded `.safetensors` files in `ComfyUI/models/loras/`. fal.ai routes require `fal-client` and `FAL_KEY`.

Do not silently install multi-GB model weights during a normal task. Ask or provide commands, then continue with planning files.

## License And Shipping

- Record the model repository URL and license in `generation-log.md`.
- For Steam/mobile/web shipping, prefer Apache-2.0 models where they satisfy the art direction.
- Treat non-commercial or unclear licenses as blocked for commercial shipping until the user verifies rights.
- Keep source prompts and generated references for auditability.
