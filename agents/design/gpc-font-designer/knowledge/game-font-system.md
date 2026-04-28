# GPC Game Font System

## Proje Yapısı
- Oyun: `www/src/game.js` — tek büyük canvas oyun dosyası (~12000+ satır)
- HTML: `www/index.html` — Google Fonts preload buraya eklenir
- Font picker: `www/fonts.html` — ayrı sayfa, localStorage üzerinden game.js ile konuşur

## game.js ctx.font Yapısı

### Mevcut Font Dağılımı
- `Fredoka, sans-serif` — ~50+ kullanım, tüm HUD/UI body metinleri
- `"Luckiest Guy", Fredoka, sans-serif` — 2 kullanım (menü logosu 68px, skor tabelası)
- `Bungee, Fredoka, sans-serif` — 5 kullanım (COURSES/SHOP/ekran başlıkları 24-26px)
- `Bungee, sans-serif` — 1 kullanım (badge değeri)
- `monospace` — 2 kullanım (debug, ruler)

### Canvas'ın Bulunduğu Satır
```
const canvas = document.getElementById('c'); // line 127
const ctx = canvas.getContext('2d');          // line 128
```

## Font Interceptor Pattern

Game.js'de canvas init'in hemen ardından (`line ~130`) eklenecek:

```js
// Runtime font switching via localStorage
(function patchCanvasFonts() {
  const body  = localStorage.getItem('gpc_font_body')  || 'Fredoka';
  const title = localStorage.getItem('gpc_font_title') || 'Luckiest Guy';
  if (body === 'Fredoka' && title === 'Luckiest Guy') return; // no-op if defaults
  const d = Object.getOwnPropertyDescriptor(CanvasRenderingContext2D.prototype, 'font');
  if (!d || !d.set) return;
  Object.defineProperty(CanvasRenderingContext2D.prototype, 'font', {
    set(v) {
      v = v
        .replace(/\bFredoka\b/g, body)
        .replace(/"Luckiest Guy"/g, `"${title}"`)
        .replace(/\bBungee\b/g, `"${title}"`);
      d.set.call(this, v);
    },
    get() { return d.get.call(this); },
    configurable: true
  });
})();
```

**Neden prototype intercept?** — 60+ satırı tek tek düzenlemek yerine, tüm canvas ctx.font set'lerini tek noktadan yakalar.

**Sınır:** `monospace` ve `sans-serif` (fallback) replacelenmez — sadece named Google Fonts.

## Per-Course Font Helper

```js
const _GPC_FONT_C = [0,1,2,3,4].map(i => localStorage.getItem('gpc_font_c' + i));
function _courseFont(size, weight) {
  const f = _GPC_FONT_C[currentCourse];
  return f ? `${weight||700} ${size}px "${f}", sans-serif` : null;
}
```

Kullanım: `ctx.font = _courseFont(26, 400) || '400 26px Bungee, Fredoka, sans-serif';`

Per-course font SADECE şu yerlerde kullanılır:
- `drawLevelSelect()` — kurs adı büyük başlığı
- `drawLevelComplete()` — kurs/level tamamlandı ekranı başlığı  
- `drawLevelFailed()` — başarısız ekranı başlığı

HUD (shot count, gem badge, coin badge, minimap, star count) → per-course font ASLA uygulanmaz.

## localStorage Key Şeması

| Key | Default | Açıklama |
|-----|---------|----------|
| `gpc_font_body` | `Fredoka` | Tüm body/HUD metinleri |
| `gpc_font_title` | `Luckiest Guy` | Ekran başlıkları, büyük başlıklar |
| `gpc_font_c0` | null | C1 Meadow kurs override |
| `gpc_font_c1` | null | C2 Sky Kingdom kurs override |
| `gpc_font_c2` | null | C3 Crystal Caverns kurs override |
| `gpc_font_c3` | null | C4 Neon Circuit kurs override |
| `gpc_font_c4` | null | C5 Candy Rush kurs override |

Note: `currentCourse` 0-based index (0=C1, 1=C2, ... 4=C5).

## Storage Event — Canlı Güncelleme

Game.js'e eklenir (başlangıç bloğu sonunda):

```js
window.addEventListener('storage', e => {
  if (e.key && e.key.startsWith('gpc_font')) {
    location.reload();
  }
});
```

Fonts.html localStorage.setItem yapınca game tab'ı otomatik reload olur (same-origin tabs arası storage event tetiklenir).

## Cache Versiyonu

Her değişiklikte `index.html`'deki `game.js?v=N` bumplanmalı (SW cache bypass için).
