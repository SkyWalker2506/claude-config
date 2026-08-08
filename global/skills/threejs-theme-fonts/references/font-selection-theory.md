# Font Selection Theory

## Core Rule

Game fonts need two jobs:

- Fit the theme.
- Stay readable in every supported language.

When those conflict, readability wins for player-facing UI. Research theme-appropriate free/open-source fonts first, then use Noto as the fallback safety net when coverage or licensing is not good enough.

## Roles

- `--font-ui`: default menus, HUD, buttons, dialogue, settings, localization.
- `--font-display`: short logo/title/accent labels; optional.
- `--font-hud`: center-screen popups and moment-to-moment feedback.
- `--font-mono`: debug/performance overlays only.

## Theme Hints

- Sci-fi: angular, squared, compact UI/display; avoid sterile defaults if a readable futuristic family covers the locale set.
- Fantasy: high-contrast serif or humanist UI where readable; avoid ornate faces for body/localized text.
- Cozy: rounded, warm, friendly UI; prioritize soft shapes with generous metrics.
- Horror: tense, sharp, or distressed display only for titles; clean UI for actual instructions.
- Retro: pixel/display for very short labels; normal UI fallback for translations.
- Minimal/technical: use the UI font itself; avoid extra font personality.

## Candidate Order

1. Use screenshots/theme analysis to name the desired personality.
2. Search current free/open-source sources for fonts that match that personality and cover required scripts.
3. Prefer one UI font family that covers Latin, Cyrillic, Greek, and diacritics well.
4. Add script-specific companion fonts only when a single family cannot cover Arabic, CJK, Korean, Thai, or Vietnamese cleanly.
5. Use Noto families as the final fallback layer, not as the first design choice.
6. Reject fonts with unclear license, CDN-only usage, missing weights, poor small-size readability, or weak glyph coverage.

## Center HUD Popup

For text that appears in the center of the screen:

- Keep it short.
- Use stable dimensions and `max-width`.
- Use text shadow/stroke/backplate for contrast.
- Animate opacity/scale/translate, not layout.
- Avoid all caps for languages where casing is awkward.
- Use `clamp()` for size, but do not let text exceed its box.
- Retest with long translations.

Good CSS traits:

```css
.hud-popup {
  position: fixed;
  inset: 42% 16px auto;
  display: grid;
  place-items: center;
  pointer-events: none;
  text-align: center;
  font-family: var(--font-hud);
  font-size: clamp(24px, 4vw, 56px);
  line-height: 1.05;
  overflow-wrap: anywhere;
}
```

## Localization Safety

- Arabic needs correct font fallback and right-to-left layout support when used.
- CJK fonts need enough line-height and should not be squeezed into Latin metrics.
- Thai and Vietnamese need marks/diacritics to avoid clipping.
- Avoid fixed-height text boxes unless text can wrap.
- Prefer semantic CSS classes over inline style patches.

## Visual Overflow QA

Font coverage is not enough. Validate how translated text behaves inside the actual game screens:

- Capture Playwright/browser screenshots for menu, settings, pause, gameplay HUD, dialogue/tutorial, inventory/shop when present, and center-screen popup states.
- Stress the UI with default text plus longer translations such as German or Turkish, RTL Arabic, Thai/Vietnamese marks, and CJK/Korean glyph metrics.
- Treat overflow, clipped accents, button growth, unexpected wrapping, viewport escape, and locale-to-locale layout shifts as typography bugs.
- Prefer copy fixes before CSS fixes: shorten or rephrase translated strings when the meaning survives.
- If copy cannot be shortened, fix the container next: allow wrapping, flex, min/max width, or two-line labels.
- Tune line-height, padding, and font weight before reducing type size.
- Reduce font size with bounded `clamp()` only for the affected component or breakpoint.
- Use locale-specific CSS overrides only when a script has a real metric need.
