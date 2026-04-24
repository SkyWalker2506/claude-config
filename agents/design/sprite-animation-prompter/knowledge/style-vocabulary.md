# Style vocabulary — MedievalFactory + generic game sprite projects

## MedievalFactory target style

Always include both reference game names:
> "Manor Lords + Kingdom Rush aesthetic"

Palette descriptors (copy into prompts):
- "warm earth tones"
- "warm red-orange-yellow gradient" (for fire)
- "soft gray-brown palette" (for smoke)
- "terracotta + cream stone + warm brown wood + deep forest green" (for buildings)
- "metallic copper highlights" (for copper assets)

Technique descriptors:
- "hand-drawn painterly"
- "cross-hatched shading"
- "soft edges"
- "subtle top-left lighting"
- "isometric 3/4 view" (for buildings/objects)
- "side view" (for side-scrolling sprites)

## Anti-patterns (always in negative)

Cut from every prompt:
- "pixel art" (unless explicitly requested)
- "anime / manga / chibi / big eyes"
- "outline / line art / black edges"
- "cel shaded" (unless explicitly requested)
- "photorealistic" (for this project)
- "3D render / CGI" (for this project)
- "cartoon / simpsons style"
- "text / labels / captions / watermarks"

## Reference-webp pattern

When a character has an existing static asset, reference it BY FILENAME:
```
Match exactly the style, palette, proportions and line weight of BlackSmithCharacter.webp.
```

Known MedievalFactory reference files:
- `BlackSmithCharacter.webp` — blacksmith in apron
- `MinerCharacter.webp` — miner with cap
- `MerchantCharacter.webp`
- `IronMine.webp`, `CoalMine.webp`, etc. — building refs
- `CargoCart.webp`, `CoalMineCart.webp` — cart refs
- `SmokeCloud.png` — smoke FX ref
- `Fire.webp` — fire FX ref

Note: referencing existing files in text is what transfers style. The GPT Sources tab is confirmed non-functional for DALL-E output — never rely on it.

## Lighting convention

All assets use "soft top-left lighting" unless the asset is self-emissive (fire, torches, glow FX). Keep consistent across batch.
