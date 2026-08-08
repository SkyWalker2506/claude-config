# Language Selector Assets

## Principles

Flags are country symbols, not language symbols. Use them only as optional compact visual hints next to native language names, and avoid implying that a language belongs to one country. For languages with multiple regions, prefer text-first labels:

- `English`
- `Português`
- `Português-Brasil`
- `Español-España`
- `Español-Latinoamérica`
- `简体中文`
- `繁體中文`

## Asset Source

When internet is available, verify the current license before downloading. Good default sources:

- `flag-icons` by lipis: SVG country flags, MIT license.
- `circle-flags` by HatScripts: circular SVG flags, MIT license.

Do not hotlink CDN assets in a shipped game. Copy only required SVGs into:

```text
public/localization/flags/
```

This path is intentionally compatible with Steam packaging: Vite/static builds copy `public/` into `dist/`, and any later packager can copy `dist/` into its app/depot staging folder. If `$threejs-steam-shipper` is also used, its `copy:web` step preserves this layout.

Write attribution/license notes to:

```text
buildable/localization/THIRD_PARTY_NOTICES.localization.md
```

## Mapping

Use conservative default flag hints:

```json
{
  "en": "gb",
  "tr": "tr",
  "de": "de",
  "fr": "fr",
  "es": "es",
  "es-419": "mx",
  "pt": "pt",
  "pt-BR": "br",
  "ja": "jp",
  "ko": "kr",
  "zh-CN": "cn",
  "zh-TW": "tw",
  "ar": null
}
```

Use `null` when a flag would be misleading. Arabic is a good example: use native text or a neutral globe/language icon unless the project explicitly chooses a region.

## UI Rules

- Keep the native language name visible; do not make a flag-only picker.
- Use small icons with fixed dimensions, usually 18-24 px.
- Set `alt=""` on decorative flag images and put the accessible language name on the button.
- Match the existing UI: use the same radius, border, shadows, focus ring, and hover style.
- Avoid layout shifts by giving each option stable height and icon width.
- Test long labels, CJK glyphs, RTL labels, controller focus, and Steam Deck-like 1280x800.
