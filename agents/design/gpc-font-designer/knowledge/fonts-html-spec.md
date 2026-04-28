# fonts.html — Interactive Picker Specification

## Amaç
Kullanıcının her kurs için font seçip oyunda canlı görebileceği, deploy gerektirmeyen lokal araç.

## Sayfa Yapısı

```
┌─────────────────────────────────────────────────────────┐
│ GOLF · PAPER CRAFT — Font Seç                           │
│ Body font, başlık fontu ve her kurs için override seç.  │
├─────────────────────────────────────────────────────────┤
│ [GENEL FONTLAR]  Body Font sekmesi                      │
│ [GENEL FONTLAR]  Başlık Fontu sekmesi                   │
│ [C1 MEADOW]      ...                                    │
│ [C2 SKY KINGDOM] ...                                    │
│ [C3 CRYSTAL]     ...                                    │
│ [C4 NEON]        ...                                    │
│ [C5 CANDY]       ...                                    │
├─────────────────────────────────────────────────────────┤
│ STICKY BOTTOM: Seçimlerim + Oyunu Güncelle butonu       │
└─────────────────────────────────────────────────────────┘
```

## Font Kartı Yapısı (Her Kart)

```html
<div class="font-card" data-font="Lilita One" data-key="gpc_font_c0">
  <!-- Başlık satırı: font adı + MEVCUT badge (varsa) -->
  <div class="font-name">Lilita One</div>
  <!-- Preview: büyük başlık -->
  <div class="ex-title" style="font-family:'Lilita One',sans-serif; font-size:36px;">
    Meadow
  </div>
  <!-- Preview: HUD satırı -->
  <div class="ex-hud" style="font-family:'Lilita One',sans-serif; font-size:20px;">
    Level 7 · ★★★
  </div>
  <!-- Preview: küçük metin -->
  <div class="ex-small" style="font-size:13px; font-family:'Lilita One',sans-serif;">
    Hole in One!
  </div>
  <!-- SEÇ butonu -->
  <button class="select-btn">Seç</button>
</div>
```

## Seçim Davranışı

```js
// Her section için radio davranışı
document.querySelectorAll('.font-card').forEach(card => {
  card.querySelector('.select-btn').addEventListener('click', () => {
    const key   = card.dataset.key;    // e.g. 'gpc_font_c0'
    const font  = card.dataset.font;   // e.g. 'Lilita One'
    
    // Aynı section'daki tüm kartların selected class'ını kaldır
    document.querySelectorAll(`[data-key="${key}"]`).forEach(c => c.classList.remove('selected'));
    
    // Bu kartı seç
    card.classList.add('selected');
    
    // localStorage'a yaz (game tab storage event ile reload olur)
    localStorage.setItem(key, font);
    
    // Bottom bar güncelle
    updateSummaryBar();
  });
});
```

## Sayfa Yüklenirken Mevcut Seçimleri Restore Et

```js
document.addEventListener('DOMContentLoaded', () => {
  ['gpc_font_body','gpc_font_title','gpc_font_c0','gpc_font_c1','gpc_font_c2','gpc_font_c3','gpc_font_c4']
    .forEach(key => {
      const val = localStorage.getItem(key);
      if (val) {
        const card = document.querySelector(`[data-key="${key}"][data-font="${val}"]`);
        if (card) card.classList.add('selected');
      }
    });
  updateSummaryBar();
});
```

## Sticky Bottom Bar

```html
<div id="summary-bar">
  <div class="summary-items">
    <span>Body: <strong id="sum-body">Fredoka</strong></span>
    <span>Başlık: <strong id="sum-title">Luckiest Guy</strong></span>
    <span>C1: <strong id="sum-c0">—</strong></span>
    <span>C2: <strong id="sum-c1">—</strong></span>
    <span>C3: <strong id="sum-c2">—</strong></span>
    <span>C4: <strong id="sum-c3">—</strong></span>
    <span>C5: <strong id="sum-c4">—</strong></span>
  </div>
  <button id="open-game-btn" onclick="window.open('http://127.0.0.1:8001/index.html','gpc-game')">
    Oyunu Aç / Yenile
  </button>
  <button id="reset-btn" onclick="resetAll()">Sıfırla</button>
</div>
```

## Reset Fonksiyonu

```js
function resetAll() {
  ['gpc_font_body','gpc_font_title','gpc_font_c0','gpc_font_c1','gpc_font_c2','gpc_font_c3','gpc_font_c4']
    .forEach(k => localStorage.removeItem(k));
  document.querySelectorAll('.font-card.selected').forEach(c => c.classList.remove('selected'));
  updateSummaryBar();
}
```

## Canlı Güncelleme Mekanizması

1. fonts.html: `localStorage.setItem(key, font)` → her tıklamada
2. game.js (storage listener): `window.addEventListener('storage', e => { if (e.key?.startsWith('gpc_font')) location.reload(); })`
3. Storage event cross-tab tetikler (aynı origin, farklı tab) — otomatik çalışır

**Önemli:** Storage event sadece FARKLI tab'da tetikler. Aynı tab'da localStorage.setItem yapınca kendi tab'ın storage event almaz. Bu yüzden "Oyunu Aç/Yenile" butonu game tab'ı refresh eder.

## Görsel Tasarım Rehberi

- Arka plan: `#1a1208` (oyunla aynı koyu kahve)
- Seçili kart: yeşil kenarlık `#8fa14a` veya kurs rengiyle renklendi
- Her kurs section'ı kendi accent rengiyle vurgulanır (C2=mavi, C3=mor, C4=cyan, C5=pembe)
- Sticky bar: yarı saydam `rgba(26,18,8,0.95)` + blur backdrop
- "Seç" butonu: küçük, yuvarlak, kurs accent rengi arka planı
- "Seçildi" durumu: kart border highlight + "Seç" → "✓ Seçildi"
