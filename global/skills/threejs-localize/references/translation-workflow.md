# Translation Workflow

## Locale Codes

Use BCP 47 style codes for in-game files:

- `en`, `tr`, `de`, `fr`, `es`, `it`, `pt-BR`, `ja`, `ko`, `zh-CN`, `zh-TW`, `ru`, `pl`.

Prefer one source locale, usually `en`. Keep source strings natural and complete; do not write terse pseudo-English just to save space.

## Steam Full Platform Languages

When the user asks for all Steam languages, treat Steam's Full Platform Supported Languages as the default target set because those have Steamworks API language codes. Steam also has a broader Game Support Only list; use that only when the user explicitly wants extra store-tag languages.

As of the Steamworks documentation checked on 2026-08-08, the full platform Web/API locale codes are:

```text
ar,bg,zh-CN,zh-TW,cs,da,nl,en,fi,fr,de,el,hu,id,it,ja,ko,ms,no,pl,pt,pt-BR,ro,ru,es,es-419,sv,th,tr,uk,vi
```

Before final release, verify the list against the current Steamworks "Languages Supported on Steam" page.

Steam client API language codes differ from Web/API BCP 47-ish codes for some languages. Map them explicitly:

```text
schinese -> zh-CN
tchinese -> zh-TW
koreana -> ko
brazilian -> pt-BR
latam -> es-419
```

## Translation Rules

- Preserve JSON keys exactly.
- Translate values only.
- Preserve placeholders exactly: `{count}`, `{playerName}`, `{key}`.
- Preserve inline tags/tokens if present: `<b>`, `</b>`, `[A]`, `%s`, `\n`.
- Keep button labels short where UI space is limited.
- Keep game terms consistent; create a small glossary when repeated terms appear.
- Do not translate technical product names, filenames, hotkeys, or platform names unless the project explicitly does.

## Batch Prompt Pattern

When using Codex/LLM translation, provide one locale at a time for quality:

```text
Translate this JSON locale file from English to Turkish.
Return valid JSON only.
Preserve every key, placeholder, markup token, punctuation variable, and newline escape.
Use natural game UI language, concise button labels, and consistent terminology.
```

For many languages, translate high-value languages first and keep later locales machine-translated with review flags if necessary.

For all Steam full platform languages, `sync-locale-keys.mjs --steam-full` creates `translation-batch.<locale>.json` files. Translate and write each batch back into the matching locale JSON, removing `TODO:` prefixes only after translation.

When the project will be packaged for Steam, keep translation batches and review reports in `buildable/localization/`. Do not place those files under `public/`, `dist/`, or `buildable/steam-electron/web/` because Steam packaging should copy only the production web output into the depot.

## QA

After translation:

- Parse every JSON file.
- Compare key coverage against source.
- Search for `TODO:` values.
- Check placeholder parity per key.
- Build and run the app.
- Inspect overflow in menus, HUD, settings, dialogue, and canvas/text-geometry labels.
- Launch with different `navigator.language`/machine locales or a mocked Steam language code and confirm the initial language is chosen correctly.
- If a Steam staging folder exists, run `verify-steam-shipper-localization.mjs --strict-steam` after the web build is copied and fix every reported issue before uploading a depot. If no Steam staging folder exists, skip this check or run the verifier without `--strict-steam` for standalone locale validation.

## Pseudo-Localization

For layout testing before real translations, create a pseudo locale that expands strings by 30-50 percent and wraps them with markers. Use it only for QA, never as a shipping locale.
