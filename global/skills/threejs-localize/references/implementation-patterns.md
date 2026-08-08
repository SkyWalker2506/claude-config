# Implementation Patterns

## Plain Three.js Or Vite

Use a tiny runtime when no i18n library exists. For Vite projects, include locale JSON files with `import.meta.glob`, detect the user's default locale at startup, and let an explicit saved choice win:

```js
import en from './locales/en.json';

const catalogs = { en };
let currentLocale = 'en';

const steamToBcp47 = {
  english: 'en',
  turkish: 'tr',
  german: 'de',
  french: 'fr',
  schinese: 'zh-CN',
  tchinese: 'zh-TW',
  brazilian: 'pt-BR',
  latam: 'es-419',
  koreana: 'ko'
};

function normalizeLocale(locale) {
  if (!locale) return 'en';
  const normalized = steamToBcp47[String(locale).toLowerCase()] || String(locale).replace('_', '-');
  if (catalogs[normalized]) return normalized;
  return normalized.split('-')[0];
}

export function detectDefaultLocale({ steamLanguage } = {}) {
  const saved = localStorage.getItem('game.locale');
  const candidates = [saved, steamLanguage, ...navigator.languages, navigator.language].map(normalizeLocale);
  return candidates.find((locale) => catalogs[locale]) || 'en';
}

export function initLocale(options) {
  setLocale(detectDefaultLocale(options));
  return currentLocale;
}

export function setLocale(locale) {
  currentLocale = catalogs[locale] ? locale : 'en';
  localStorage.setItem('game.locale', currentLocale);
  window.dispatchEvent(new CustomEvent('localechange', { detail: { locale: currentLocale } }));
}

export function t(key, vars = {}) {
  const value = catalogs[currentLocale]?.[key] ?? catalogs.en?.[key] ?? key;
  return value.replace(/\{(\w+)\}/g, (_, name) => String(vars[name] ?? `{${name}}`));
}
```

Patch DOM text with `t('menu.start')`. For canvas/texture text, redraw after `localechange`. For `TextGeometry` or troika text, update `.text` and recompute layout/geometry when needed.

In Electron/Steam builds, pass Steam's `GetCurrentGameLanguage()` result into `initLocale({ steamLanguage })` only if a Steamworks binding already exists and is initialized. Otherwise rely on `navigator.languages`.

## React Three Fiber

If `react-i18next` already exists, use `useTranslation()`. If no library exists and the app is small, avoid adding a new dependency; create a `LocaleProvider`, `useT()`, and JSON catalogs.

Do not call translation helpers inside tight render loops when the locale has not changed. Resolve labels outside per-frame callbacks.

## Vue Or Svelte

Follow existing project idioms. Prefer `vue-i18n` or `svelte-i18n` only if already present or the app has meaningful component complexity. Keep Three.js scene object labels synced through locale-change events or reactive stores.

## Key Design

Good:

```json
{
  "menu.start": "Start",
  "settings.graphics.quality": "Graphics Quality",
  "hud.wave": "Wave {count}"
}
```

Avoid:

```json
{
  "Start": "Start",
  "text_001": "Start"
}
```

Use semantic keys because English copy changes during game polish.

## What To Extract

- Buttons, menus, HUD, settings, dialogs, tutorials.
- Player-facing error and status messages.
- Accessibility labels, tooltips, input prompts.
- Achievement names/descriptions if generated from code.
- Credits and legal copy if stored in the app.

## What To Leave

- Import paths and asset URLs.
- Object names used by loaders or scene lookup.
- CSS selectors/classes and DOM IDs.
- Shader strings, GLSL chunks, uniform names.
- Storage keys, event names, analytics identifiers.
- Debug-only logs unless release UI shows them.

## UI Safety

Localization changes layout. After integration, test:

- German or Turkish for longer Latin text.
- Japanese, Korean, or Simplified Chinese for CJK font/rendering.
- Right-to-left languages only when the UI has explicit RTL layout support.
- Small viewport and Steam Deck-like 1280x800.
- Canvas text, bitmap fonts, and text geometry for missing glyphs.
- Language selector with long native names and small screens.
