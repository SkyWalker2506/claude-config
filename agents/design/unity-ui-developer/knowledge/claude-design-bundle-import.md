---
last_updated: 2026-04-18
confidence: high
sources: 5
---

# Claude Design Bundle Import

## Quick Reference

| Kavram | Not |
|--------|-----|
| Bundle format | `styles.css` (CSS custom properties) + `index.html` (React/HTML) |
| Mapping hedefi | HTML → UXML, CSS vars → USS :root variables, CSS rules → USS selectors |
| Font handling | Google Fonts → kaldır, Unity font asset referansı için flag at |
| Caching strateji | SHA256(styles.css + index.html) tabanlı cache |
| Risk | CSS Grid yok, box-shadow yok, font-family → Unity asset gerekir |

## Gercek Bundle Formati (Claude Design, Nisan 2026)

Claude Design **web-first** bir araçtır. Native UXML/Unity export yoktur. "Handoff to Claude Code" aşağıdaki dosyaları üretir:

- **`styles.css`** — CSS custom properties (`:root` token'ları) + component class kuralları
- **`index.html`** — React/HTML component tree; class referansları `styles.css`'e bağlı
- **Interaction notes** — HTML comment'leri veya `interactions.md` olarak; click/hover/focus aksiyonları
- **Asset references** — Google Fonts `@import` URL'leri, `<img src>` yolları

"Handoff to Claude Code" = yapılandırılmış bundle URL + prompt; REST API değil.

### Örnek `styles.css`

```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel&display=swap');

:root {
  --color-blood: #8b0000;
  --color-bone: #f5f5dc;
  --color-shadow: #1a1a1a;
  --font-display: 'Cinzel', serif;
  --font-body: 'Inter', sans-serif;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --radius-sm: 4px;
  --radius-md: 8px;
}

.menu-container {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-lg);
  background-color: var(--color-shadow);
}

.btn-primary {
  background-color: var(--color-blood);
  color: var(--color-bone);
  font-family: var(--font-display);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
}

.btn-primary:hover {
  opacity: 0.85;
}
```

### Örnek `index.html`

```html
<body>
  <div class="menu-container">
    <h1 class="menu-title">Dark Realm</h1>
    <button class="btn-primary" id="start-btn">Start Game</button>
    <button class="btn-secondary" id="settings-btn">Settings</button>
  </div>
</body>
```

## CSS Custom Property → USS Variable Mapping

Claude Design `--color-*`, `--font-*`, `--spacing-*` convention kullanır. USS değişkenleri doğrudan karşılık gelir:

| Claude Design CSS Var | USS Var | Not |
|-----------------------|---------|-----|
| `--color-blood: #8b0000` | `--color-blood: #8b0000` | Doğrudan map; rename yok |
| `--color-bone: #f5f5dc` | `--color-bone: #f5f5dc` | Doğrudan map |
| `--color-shadow: #1a1a1a` | `--color-shadow: #1a1a1a` | Doğrudan map |
| `--font-display: 'Cinzel'` | `--font-display: 'Cinzel'` | Değer = font asset ref; fontWarnings'a ekle |
| `--font-body: 'Inter'` | `--font-body: 'Inter'` | Değer = font asset ref; fontWarnings'a ekle |
| `--spacing-md: 16px` | `--spacing-md: 16px` | Doğrudan map |
| `--radius-md: 8px` | `--radius-md: 8px` | Doğrudan map |

Token'lar `tokens.uss` dosyasındaki `:root` block'una yazılır. Component USS'leri `var(--token-name)` ile referans eder.

## HTML Tag → UXML Element Mapping Tablosu (Tam)

| HTML | UXML | Not |
|------|------|-----|
| `<div class="...">` | `<VisualElement class="...">` | Genel konteyner |
| `<span class="...">` | `<VisualElement class="...">` | Inline konteyner; sadece metin ise `<Label>` kullan |
| `<span>` (text-only) | `<Label>` | Inline text |
| `<button>` | `<Button>` | İnteraktif buton |
| `<input type="text">` | `<TextField>` | Tek satır metin |
| `<input type="password">` | `<TextField is-password-field="true">` | Şifreli giriş |
| `<input type="checkbox">` | `<Toggle>` | Onay kutusu |
| `<input type="range">` | `<Slider>` | Aralık sürgüsü |
| `<textarea>` | `<TextField multiline="true">` | Çok satır metin |
| `<label>` | `<Label>` | Statik metin etiketi |
| `<h1>` ... `<h6>` | `<Label class="heading-N">` | Başlık; boyutu USS ile ayarla |
| `<p>` | `<Label class="body">` | Paragraf metni |
| `<img src="...">` | `<Image>` | Explicit asset için `<Image>` tercih et |
| `<img>` (arka plan) | `<VisualElement style="background-image: url(...)">` | Dekoratif görseller için |
| `<ul><li>` | `<ListView>` | Dinamik liste; C# ile bağla |
| `<ol><li>` | `<ListView>` | Sıralı liste; numaralama C#'ta |
| `<select>` | `<DropdownField>` | Açılır menü |
| `<form>` | `<VisualElement class="form">` | Form sarmalayıcı |
| `<section>` | `<VisualElement class="section">` | Semantik bölüm |
| `<article>` | `<VisualElement class="article">` | Makale bloğu |
| `<header>`, `<nav>` | `<VisualElement class="header">` | Navigasyon konteyneri |
| `<footer>` | `<VisualElement class="footer">` | Alt bilgi konteyneri |
| `<main>` | `<VisualElement class="main">` | Ana içerik alanı |

## CSS Property → USS Property Farkları

### Desteklenen (doğrudan map)

| CSS | USS | Not |
|-----|-----|-----|
| `display: flex` | (varsayılan) | USS'de `display` property yoktur; tüm elementler flex'tir |
| `flex-direction: row/column` | `flex-direction: row/column` | Aynı |
| `flex-wrap: wrap` | `flex-wrap: wrap` | Aynı |
| `flex: 1` | `flex-grow: 1` | USS longhand kullanır |
| `align-items: center` | `align-items: center` | Aynı |
| `justify-content: center` | `justify-content: center` | Aynı |
| `padding: 16px` | `padding: 16px` | Aynı |
| `margin: 8px` | `margin: 8px` | Aynı |
| `width / height` | `width / height` | Aynı |
| `min-width / max-width` | `min-width / max-width` | Aynı |
| `background-color` | `background-color` | Aynı |
| `color` | `color` | Text rengi |
| `font-size: 14px` | `font-size: 14px` | Sadece px; rem/em desteklenmez |
| `font-style: italic` | `font-style: italic` | Aynı |
| `font-weight: bold` | `-unity-font-style: bold` | USS'de `-unity-font-style` kullanılır |
| `border-radius: 8px` | `border-radius: 8px` | Aynı |
| `border: 1px solid #ccc` | `border-width: 1px; border-color: #ccc` | USS longhand; shorthand desteklenmez |
| `opacity: 0.85` | `opacity: 0.85` | Aynı |
| `overflow: hidden` | `overflow: hidden` | Aynı |
| `position: absolute` | `position: absolute` | Desteklenir |
| `top/left/right/bottom` | `top/left/right/bottom` | `position: absolute` ile birlikte |
| `var(--token)` | `var(--token)` | CSS custom properties USS'de çalışır |

### Desteklenmeyen (warnings'a ekle)

| CSS | USS Alternatifi | Not |
|-----|----------------|-----|
| `display: grid` | Flex nesting | USS'de CSS Grid yok |
| `display: inline-flex` | `flex-direction: row` | Inline layout yok |
| `display: block/inline` | (varsayılan) | Block/inline layout yok |
| `z-index` | Hierarchy sırası | Son child en üstte render edilir |
| `backdrop-filter` | Desteklenmez | Blur efekti yok |
| `box-shadow` | Desteklenmez (native) | Custom mesh veya workaround gerekir |
| `text-shadow` | Desteklenmez | |
| `@media` queries | `Panel.onSizeChange` C# | Runtime media query yok |
| `transform: rotate` | `rotate` (Unity 2022.1+) | Unity sürümüne bağlı |
| `transition` | Desteklenmez | C# animation veya DoTween kullan |
| `animation / @keyframes` | Desteklenmez | C# veya DoTween kullan |
| `calc()` | Desteklenmez | Sabit px değerleri kullan |
| `rem / em` birimleri | `px`'e çevir | USS sadece px |
| `vh / vw` birimleri | `%` (parent-relative) | Viewport birimleri yok |

## Interaction Notes → USS Pseudo-class Dönüşümü

Claude Design interaction notları şu şekilde USS'e dönüştürülür:

| Interaction | USS | C# gerekli mi? |
|-------------|-----|----------------|
| `hover` | `.class:hover { ... }` | Hayır (pure CSS) |
| `focus` | `.class:focus { ... }` | Hayır |
| `active` (press) | `.class:active { ... }` | Hayır |
| `click → navigate` | USS desteklemiyor | Evet — C# `.clicked +=` |
| `click → show/hide` | USS desteklemiyor | Evet — C# `.style.display =` |
| `checked state` | `.class:checked { ... }` | Hayır (Toggle) |
| `disabled state` | `.class:disabled { ... }` | Hayır |

Interaction notları `metadata.interactions` olarak raporlanır; C# gerektirenler ayrıca belirtilir.

## Font Handling

Claude Design Google Fonts kullanır. USS font sistemi farklı çalışır:

### Dönüşüm adımları

1. `styles.css`'deki `@import url('https://fonts.googleapis.com/...')` satırlarını kaldır
2. Her font family için `fontWarnings`'a ekle:
   ```
   "Cinzel → assign Unity font asset to --font-display manually"
   ```
3. `tokens.uss`'de font token değerlerini string olarak koru (geliştirici dolduracak):
   ```uss
   :root {
     --font-display: resource('Fonts/Cinzel SDF');  /* TODO: assign font asset */
   }
   ```
4. Component USS'de `-unity-font-definition: var(--font-display)` kullan

### Unity Font Asset Referans Formatları

```uss
/* TextMeshPro font asset (önerilen) */
-unity-font-definition: url('project://database/Assets/Fonts/Cinzel SDF.asset');

/* Legacy font */
-unity-font: url('project://database/Assets/Fonts/Cinzel.ttf');
```

## Color Token Pattern: Claude Design → USS Kuralı

Claude Design convention: `--color-*` prefix.

USS convention: aynı prefix korunur — rename YAPMA.

```
Claude Design: --color-blood: #8b0000
USS:           --color-blood: #8b0000   ✓ (doğrudan kopyala)
```

`--unity-*` prefix zorunluluğu yoktur; Unity built-in USS değişkenleri `--unity-` ile başlar, custom değişkenler herhangi bir prefix alabilir.

## Component Dönüşüm Örneği

### Claude Design çıktısı

`styles.css`:
```css
:root {
  --color-blood: #8b0000;
  --color-bone: #f5f5dc;
  --spacing-md: 16px;
  --radius-md: 8px;
}
.card {
  display: flex;
  flex-direction: column;
  padding: var(--spacing-md);
  background-color: var(--color-bone);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.card-title { font-size: 24px; color: var(--color-blood); }
.card .btn { background-color: var(--color-blood); color: white; }
.card .btn:hover { opacity: 0.85; }
```

`index.html`:
```html
<div class="card">
  <h2 class="card-title">Dark Realm</h2>
  <button class="btn">Play</button>
</div>
```

### D11 çıktısı

`tokens.uss`:
```uss
:root {
  --color-blood: #8b0000;
  --color-bone: #f5f5dc;
  --spacing-md: 16px;
  --radius-md: 8px;
}
```

`Card.uxml`:
```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
  <VisualElement class="card">
    <Label text="Dark Realm" class="card-title" />
    <Button text="Play" class="btn" />
  </VisualElement>
</ui:UXML>
```

`Card.uss`:
```uss
.card {
  flex-direction: column;
  padding: var(--spacing-md);
  background-color: var(--color-bone);
  border-radius: var(--radius-md);
  /* box-shadow: desteklenmez — atlandı */
}

.card-title {
  font-size: 24px;
  color: var(--color-blood);
}

.card .btn {
  background-color: var(--color-blood);
  color: white;
}

.card .btn:hover {
  opacity: 0.85;
}
```

`metadata`:
```json
{
  "componentCount": 1,
  "tokenCount": 4,
  "fontWarnings": [],
  "warnings": ["box-shadow on .card not supported in USS — removed"]
}
```

## D11 Prompt Template

```
You are the Unity UI Developer (D11).

Task: Convert Claude Design web export (styles.css + index.html) to UXML + USS.

Input:
--- styles.css ---
{stylesCss}

--- index.html ---
{indexHtml}

Output format (JSON):
{
  "components": [
    {
      "name": "ComponentName",
      "uxml": "<ui:UXML xmlns:ui=\"UnityEngine.UIElements\">...</ui:UXML>",
      "uss": "/* USS rules */"
    }
  ],
  "tokens.uss": ":root { /* all CSS custom properties */ }",
  "metadata": {
    "componentCount": 1,
    "tokenCount": 8,
    "fontWarnings": ["Cinzel → assign Unity font asset to --font-display manually"],
    "warnings": ["box-shadow not supported — removed"]
  }
}

Rules:
1. Parse :root CSS custom properties from styles.css → USS :root variables (same names, same values)
2. Remove @import url() Google Fonts lines; add fontWarnings entry per font family
3. Parse HTML tag structure → UXML elements (see mapping table above)
4. CSS class rules → USS selectors (same class names)
5. :hover/:focus/:active → USS pseudo-classes (direct map)
6. Unsupported CSS (grid, box-shadow, backdrop-filter, transition, rem/em, calc()) → remove + add to warnings
7. font-weight: bold → -unity-font-style: bold
8. font-family values → flag in fontWarnings, keep as placeholder string
9. Do NOT generate C# event handlers
10. Return valid Unity-formatted XML and USS
```

## Proje Cache Stratejisi

```
<project>/.unity-craft/design-cache/
  ├── sha256-<hash>/
  │   ├── bundle/
  │   │   ├── styles.css          # Orijinal
  │   │   ├── index.html          # Orijinal
  │   │   ├── components/
  │   │   │   ├── Card.uxml
  │   │   │   └── Card.uss
  │   │   └── tokens.uss
  │   └── metadata.json
  └── metadata.json               # Tüm bundle'ların indeksi
```

Cache key: `SHA256(styles.css içeriği + index.html içeriği)`

## Sık Karşılaşılan Hatalar

| Hata | Çözüm |
|------|-------|
| CSS Grid → flex dönüşümü | `display: grid` → flex nesting; `grid-template-columns: 1fr 1fr` → iki `VisualElement` yan yana `flex-direction: row` ile |
| Z-Index eksikliği | USS hiyerarşiye dayalı; element sırasını yeniden düzenle veya parent'ı yeniden yapılandır |
| Font bulunamadı | Google Font'u indirip Unity Font Asset oluştur; `-unity-font-definition` ile bağla |
| `rem`/`em` birim sorunu | Tüm `rem`/`em` değerlerini `px`'e çevir (base 16px varsay) |
| `box-shadow` yok | Warnings'a ekle; gerekirse özel VisualElement overlay ile simüle et |
| Hover state çalışmıyor | USS `:hover` pseudo-class kullanıldığından emin ol; C# event listener gerekmez |
| Media query yok | `Panel.onSizeChange` event'i ile runtime viewport değişikliklerini yakala |

## Kaynaklar

- [UI Toolkit USS Reference](https://docs.unity3d.com/Manual/UIE-USS-Selectors.html) — selector ve pseudo-class syntax
- [UXML Manual](https://docs.unity3d.com/Manual/UIE-UXML.html) — element mapping
- [UI Toolkit Supported Properties](https://docs.unity3d.com/Manual/UIE-USS-SupportedProperties.html) — tam desteklenen property listesi
- [ImportDesignBundle Tool Spec](../../../../../ccplugin-unity-craft/skills/unity-craft/tools/import-design-bundle.md) — pipeline detayı
