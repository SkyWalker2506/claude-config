# Unity Asset Store Taxonomy

## Top 20 Categories

1. **3D Models** — Characters, Environments, Props, Complete Scenes
2. **2D** — Sprites, Backgrounds, Icons, Animations
3. **Animation** — Character animations, cutscenes, motion capture
4. **Audio** — Music, SFX, voice packs, FMOD integration
5. **Complete Projects** — Full game demos, starter kits, templates
6. **Editor Extensions** — Tools, inspectors, window utilities
7. **Essentials** — Core packages, frameworks, runtime utilities
8. **GUI Skins** — UI themes, icon packs, UI components
9. **Particle Systems** — VFX, magic effects, environmental particles
10. **Props** — Modular 3D assets, decorative objects
11. **Scripting** — C# utilities, systems, libraries
12. **Services** — Analytics, networking, backend APIs
13. **Shaders** — Custom shaders, material packs, visual effects
14. **Templates** — Game templates, project bootstraps
15. **Textures Materials** — PBR textures, material libraries, texture packs
16. **Tools** — Development utilities, asset processors, debug tools
17. **VFX** — Visual effects, particle packs, post-processing
18. **Add-Ons** — Plugin enhancements, integration packs
19. **Environments** — Complete environments, terrain assets, biomes
20. **Characters** — Character models, rigs, animations

## URL Patterns

Search base: `https://assetstore.unity.com/packages/search`

Query parameters:
- `q=search_term` — text search
- `category=CATEGORY_ID` — filter by category (numeric ID)
- `price=0-0` — free assets only
- `price=1-` — paid assets only
- `price=MIN-MAX` — price range
- `unity_version=UNITY_VERSION` — filter by Unity version (e.g., `2022.2`, `6`)
- `sort=trending` | `rating` | `most-recent`

Example: Filter free 3D characters for Unity 6:
```
https://assetstore.unity.com/packages/search?q=character&category=3D/Characters&price=0-0&unity_version=6&sort=rating
```

## Typical Subcategories

| Category | Subcategories | Example Assets |
|----------|---------------|-----------------|
| 3D Models | Characters, Environments, Props, Vehicles | Synty Studios POLYGON, Kenney Assets, POLYHAVEN |
| 2D | Sprites, Icons, Backgrounds, GUI | Kenny Assets 2D, Pixel Art Packs |
| Animation | Character Motion, Cutscenes, VFX | Mixamo, Motion Captured Animations |
| Audio | Music, SFX, Ambient | Wwise, FMOD Studio, Epidemic Sound |
| Complete Projects | Demos, Shooters, RPGs, Puzzles | Complete Game Templates |
| Editor Extensions | Editors, Inspectors, Asset Tools | Odin Inspector, PlayMaker, Bolt |
| Textures Materials | PBR, Stylized, 2D Sprites | Quixel Megascans, Texturepacker |

## Programmatic Search

To query Asset Store programmatically for e16-dispatch:
1. Construct URL with filters (category, price, unity_version)
2. Fetch listing page (HTML)
3. Parse product cards: extract name, rating, price, publisher, url
4. Return top 5-10 results ranked by rating + review count

Rate limit: ~10 requests/minute (no official API); consider caching.
