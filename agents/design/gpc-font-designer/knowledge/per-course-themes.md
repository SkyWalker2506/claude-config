# Per-Course Themes & Font Guidance

## Kurs Palette + Font Uyum Kuralları

Her kursun renk paleti HUD_THEMES'te tanımlı. Font seçiminde kursa ait accent renk üzerinde okunabilirlik (WCAG AA) şart.

---

## C1 — Meadow (currentCourse = 0)

| Özellik | Değer |
|---------|-------|
| bg | `#D4F5A0` (yeşil çimen) |
| accent | `#8FA14A` (koyu yeşil) |
| text | `#2B1D12` (kahverengi mürekkep) |
| Vibe | Klasik, sıcak, eğlenceli, doğal |

**Font önerileri:** Lilita One, Ranchers, Grandstander 900  
**Kaçınılacaklar:** Gotik, monospace, çizgi-film pastelı  

---

## C2 — Sky Kingdom (currentCourse = 1)

| Özellik | Değer |
|---------|-------|
| bg | `#87CEEB` (açık mavi gökyüzü) |
| accent | `#4FC3F7` (parlak mavi) |
| text | `#0D2B4B` (koyu lacivert) |
| Vibe | Havai, bulutlu, uçuşan, hafif |

**Font önerileri:** Nunito 900, Comfortaa 700, Quicksand 700  
**Kaçınılacaklar:** Sert/köşeli fontlar, monospace, ağır display  

---

## C3 — Crystal Caverns (currentCourse = 2)

| Özellik | Değer |
|---------|-------|
| bg | `#1E0A30` (koyu mor mağara) |
| accent | `#9B5DE5` (parlak mor) |
| text | `#E8D5F5` (soluk lavanta) |
| Vibe | Mistik, gotik, kristal, karanlık |

**Font önerileri:** Cinzel Decorative 700/900, Almendra SC  
**Kaçınılacaklar:** Yuvarlak/cute fontlar, neon/retro, candy hissi  
**Dikkat:** Koyu bg üzerinde küçük font okunmaz — min 16px kullan, kontrast doğrula  

---

## C4 — Neon Circuit (currentCourse = 3)

| Özellik | Değer |
|---------|-------|
| bg | `#0A0A15` (siyah devre kartı) |
| accent | `#00FFEA` (neon cyan) |
| text | `#E0F7FF` (beyaz-mavi) |
| Vibe | Sci-fi, cyberpunk, dijital, retro-tech |

**Font önerileri:** Orbitron 700/900, Share Tech Mono, VT323, Russo One  
**Kaçınılacaklar:** El yazısı, organik, fantasy, candy  
**Dikkat:** VT323 çok piksel — küçük boyutta çok iyi, büyük boyutta retro his  

---

## C5 — Candy Rush (currentCourse = 4)

| Özellik | Değer |
|---------|-------|
| bg | `#FFD6E0` (pembe şeker) |
| accent | `#FF85A1` (hot pink) |
| text | `#5A1230` (koyu kırmızı) |
| Vibe | Tatlı, çizgi-film, çocuksu, canlı |

**Font önerileri:** Baloo 2 700/800, Pacifico, Bubblegum Sans  
**Kaçınılacaklar:** Gotik, monospace, ağır display, serif  

---

## Genel Body Font — Kriter

Body font (gpc_font_body) TÜM kurslarda kullanılır. Bu yüzden:
- Tüm 5 kurs bg renginde WCAG AA geçmeli
- 9px minimum boyutta okunabilmeli (canvas küçük fontlar kullanıyor)
- Variable weight (400-700) desteklemeli
- Fredoka bu kriterlerin tamamını geçiyor — değiştirirken dikkatli ol

**Test seti:** Şu 5 string her kurs bg üzerinde okunabilmeli:
- `"3"` (shot count, 9px)
- `"★★★"` (stars, 11px)  
- `"Hole in One!"` (14px, yeşil/açık bg)
- `"Tap to continue"` (12px)

---

## Genel Title Font — Kriter

Title font (gpc_font_title) ekran başlıklarında kullanılır (COURSES, SHOP, Level Complete).  
- Minimum 20px boyutlarda kullanılır — küçük-font okunabilirliği gerekmez
- `#f5e8c8` (krem) ve `#f7c948` (altın) renklerde görünmeli
- Bold/heavy ağırlıkta görsel etki yaratmalı
