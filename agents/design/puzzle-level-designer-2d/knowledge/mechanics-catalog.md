# Mechanics Catalog — Golf Paper Craft

Implemented ve önerilen mekaniklerin tam spec'i. Her biri için: data şeması, fizik, görsel, puzzle rolü ve tuzak uyarısı.

## Active Mechanics (15)

### 1. hill
- **Data**: `{ type: 'hill', x, y, r, character }`
- **Physics**: static circle (isStatic, friction 0.3). Restitution ball defaultı 0.52 kalır — yumuşak sekme.
- **Render**: yarım daire yeşil çim + Sleepy Guardian karakter yüzü.
- **Puzzle rolü**: yolu engelleyici, yumuşak redirect. Banka atışı mümkün.
- **Pitfall**: trajectory ekseninden >±30px uzaklaştıysa dekor olur.

### 2. tree `{ variant: normal | autumn | cherry | pine }`
- **Data**: `{ type: 'tree', x, h }` (h = toplam yükseklik)
- **Physics**: trunk (10×h), canopy circle r=30 at GY-h (solid, restitution 0.55).
- **Render**: trunk + organic canopy with variant-based color palette.
- **Rolü**: havayı kapar — high-arc bypass'ı önler. Yerden dar "geçit" yaratır.

### 3. rock
- **Data**: `{ type: 'rock', x, y?, r }` (y default yere yarı gömülü)
- **Physics**: static circle (friction 0.15, ball restitution 0.52 = sharp ricochet).
- **Rolü**: hızlı top deflect, karambol. Hill'den farkı: daha sert, daha küçük.

### 4. water
- **Data**: `{ type: 'water', x1, x2, hasCroc?: true, crocCount?: 1|2 }`
- **Physics**: zone — ball enters → reset to ballStart. Geniş ise crocCount=2 otomatik.
- **Rolü**: yol-kesici tehlike. Bridge / trampoline kombinlarıyla aşılır.

### 5. mud
- **Data**: `{ type: 'mud', x, w }`
- **Physics**: zone — ground'da vx *= 0.85 per frame. Havada etki yok.
- **Rolü**: yerden yuvarlanmayı frenler → player arc kullanmak zorunda kalır.

### 6. bridge
- **Data**: `{ type: 'bridge', x, w, gap? }` (gap varsa 2 plank)
- **Physics**: static rectangle(s) at y=GY-4. Bounce damped: `vy *= -0.18`.
- **Rolü**: su üstünden güvenli geçiş (dar hedef). gap=60-100 ise atlama puzzle.

### 7. pit
- **Data**: `{ type: 'pit', x, w }`
- **Physics**: zone — ball in zone at y > GY-2 → reset.
- **Rolü**: tepede benzer gözüken sessiz reset. Hole ile karıştırılabilir (kasıtlı).

### 8. trampoline
- **Data**: `{ type: 'trampoline', x, y, w, h, character }`
- **Physics**: static rect. Collision → mirror reflection with scaled launch `clamp(|vy|*1.25, 22, 32)`.
- **Rolü**: dikey gate. y=GY-36+ olursa "airborne pad" = arc-down-to-launch zorunlu kılar.
- **Pitfall**: y=GY-6 ise top yuvarlanırken hafif temas, gerçek boost vermez → dekor olur.

### 9. wind
- **Data**: `{ type: 'wind', x1, x2, force, character }` (force negatif=sola, pozitif=sağa)
- **Physics**: zone — apply horizontal force per frame.
- **Rolü**: headwind/tailwind. Uzaklığı uzatır veya kısaltır.

### 10. ice
- **Data**: `{ type: 'ice', x1, x2 }`
- **Physics**: zone — inIce flag, grass drag atlanır. Top slide yapar.
- **Rolü**: momentum korur → "buzdan sonra pad'e iniş" puzzle'i mümkün.

### 11. magnet
- **Data**: `{ type: 'magnet', x, y, r, strength }` (default strength 0.0005)
- **Physics**: radial attract (linear falloff) ball'a. Per-frame applyForce.
- **Rolü**: trajectory bükücü. Top yanında geçse bile çekilir.
- **Status**: implemented, **0 level'da kullanılmıyor** (feature debt).

### 12. portal
- **Data**: `{ type: 'portal', x, y, id, pair }` (pair = eşleşeceği portal id)
- **Physics**: ball within 22px of portal → teleport to matching pair, keep velocity. 20 frame cooldown.
- **Rolü**: uzun path'leri kısaltma puzzle'i. Tek atış bile olmaz, mantık gereklidir.
- **Status**: implemented, **0 level'da kullanılmıyor**.

### 13. movingHill
- **Data**: `{ type: 'movingHill', x, y, r, amp, period }`
- **Physics**: static circle, position.x sin() ile animate.
- **Rolü**: timing puzzle. Top doğru anda tepeye gelmeli.
- **Status**: implemented, **0 level'da kullanılmıyor**.

### 14. spring *(NEW 2026-04-22)*
- **Data**: `{ type: 'spring', x, y, w, h }` (default y=GY-8, w=36, h=12)
- **Physics**: static rect. Collision → `vx *= 0.35`, `vy = -SPRING_LAUNCH` (default 28). Pure vertical.
- **Render**: coil base + red pad, squish anim.
- **Rolü**: horizontal dumping + pure vertical kick. "Stop+jump" puzzles.
- **Pitfall**: açık pozisyonda trajectory kazara teğet geçerse top dikey savrulur — frustrating. Dar pencerede kullan.

### 15. fan *(NEW 2026-04-22)*
- **Data**: `{ type: 'fan', x1, x2, force, topY? }` (force +, topY default GY-220)
- **Physics**: zone — ball inside, per-frame upward force scaled by `(by - topY) / (GY - topY)` (strongest near ground).
- **Render**: base box + 3 dönen blade + yukarı akım partikülleri.
- **Rolü**: top içinde asılı kalır, yatay ilerleme tek yol. Arc-suppression puzzle'i.
- **Pitfall**: force fazla → oyuncu top'u kontrol edemez, az → etkisiz.

## Proposed (not yet implemented)

### 16. saw
Horizontal damage body, kills ball on contact.

### 17. bouncePad (angled trampoline)
Fixed angle (45° or 60°) — reflects velocity in predetermined direction.

### 18. magnetReverse
Repel force — anti-puzzle gate.

## Active Count: 15 (13 eski + spring, fan)
## Mandatory puzzle usage audit (her mekanik ≥1 level'da zorunlu olmalı)
- hill ✓, tree ✓, rock ✓, water ✓, mud ✓, bridge ✓, pit ✓, trampoline ✓, wind ✓, ice ✓
- magnet ✗, portal ✗, movingHill ✗ — BUNLAR BİR LEVELDE KULLANILMALI
- spring, fan — L18 boss'ta debut ediyor
