# Font Sources And Coverage

Research baseline: checked on 2026-08-08.

## Research-First Strategy

Do not default to Noto immediately. First research current free/open-source fonts that fit the game's theme and cover the required locale/script buckets. Use Noto only when a better themed family cannot satisfy coverage, readability, self-hosting, or licensing.

Useful current sources:

- Google Fonts and its Developer API metadata for categories, variants, and subsets/scripts.
- Fontsource for versioned self-hostable open-source font packages.
- The font's upstream GitHub/foundry page for license files and current releases.
- Noto Fonts as the fallback coverage family.

When researching, record:

- candidate family name and source URL,
- license and whether game bundling/self-hosting is allowed,
- scripts/subsets and missing buckets,
- available weights/styles,
- why it fits or fails the game's theme,
- whether Noto fallback is still required for specific scripts.

## Noto Fallback Set

Use this fallback set when a theme font cannot cover all required scripts safely:

- `Noto Sans`
- `Noto Sans Arabic`
- `Noto Sans SC`
- `Noto Sans TC`
- `Noto Sans JP`
- `Noto Sans KR`
- `Noto Sans Thai`

This set covers the practical script buckets used by `$threejs-localize` Steam full platform languages, but it should be the fallback layer after better theme-fit options are considered.

## Display Fonts

Use display fonts only for short theme accents. Examples to consider after checking current license and coverage:

- Sci-fi: `Orbitron`, `Rajdhani`, `Exo 2`
- Fantasy: `Cinzel`, `Alegreya`
- Cozy: `Nunito`, `Baloo 2`
- Horror: `Creepster` for title-only use
- Retro: `Press Start 2P` for very short title-only use

Most display fonts do not cover Arabic/CJK/Thai/Korean. Pair them with the Noto UI stack.

## Self-Hosting

For Steam/Electron builds, prefer self-hosted fonts:

```text
public/fonts/
```

Then use `@font-face` in `src/theme/typography.css`. Do not depend on Google Fonts CDN at runtime for a shipped Steam build.

## License Notes

- Verify the font license before shipping.
- Keep license notices in `buildable/typography/FONT_NOTICES.md`.
- If a font is under SIL OFL, do not claim ownership or rename reserved font names incorrectly.

Useful sources:

- Google Fonts: https://fonts.google.com/
- Noto Fonts: https://notofonts.github.io/
- Noto GitHub: https://github.com/notofonts
- SIL Open Font License: https://openfontlicense.org/
