# Common Pitfalls in Level Design

Bu kuralları Level yaparken her biri için check yap. Yaygın tuzaklar:

## 1. Decorative trampoline
Pad yerde (y ≈ GY) + trajectory üzerinde değil → player pad'i kullanmadan düz atışla geçer.

**Kural**: trampoline ya `y ≤ GY - 28` airborne (top ARCsıyla üstüne düşmek zorunda), ya da **iki tehlike arasında gate** pozisyonunda (tek yol).

## 2. Brute-force bypass
Level distance `< tier-4 range (570 px)` ve engel max yüksekliği `< ~90px` → player yüksek arc ile tek atışta geçer.

**Kural**: `d > 570` VEYA engel canopy/hill ≥ 90px → arc tavanını aşmalı.

## 3. Unbalanced tier design
Level yalnız tier-4 ile geçilebiliyorsa, tier-1/2 oyuncu takılır → frustrating.

**Kural**: her level `≥ 2 farklı tier` ile çözülebilir olmalı (parçalı multi-shot).

## 4. Redundant obstacle (dekor)
Engel ball'un trajectory hat üstünde değilse dekor olur.

**Mental model**: topun center-line'ını `ballStart → hole` ekseninde çiz; engel bu ekseni `±30 px` içinde kesmeli. Aksi halde dekor sayılır.

## 5. Mechanic-without-puzzle
Data'da `portal`/`magnet`/`movingHill` TANIMLI ama `LEVELS` array'inde kullanılmıyorsa → **feature debt**. Her implemented mekanik ≥1 level'da mandatory olmalı.

## 6. Crescendo violation
Boss level'da mekanik sayısı `< önceki level + 2` → anticlimactic.

**Kural**: Boss (L18) `≥ 7 distinct mekanik` içermeli. Yeni mekanik varsa boss'ta debut.

## 7. Breather spacing
Her 6 level'da bir "breather" — tanıdık parça tekrarı, yeni mekanik yok, kolay tempo. 

**Kural**: L6, L12 breather pozisyonlarında. Course 2'ye geçişte L19 breather.

## 8. Trampoline over water visibility
Pad su üstünde `y=GY-6` ise su yüzeyi ile görsel olarak karışır; oyuncu "ada" gibi algılar → raft pozisyonunda `y=GY-20` yarı-airborne ideal.

## 9. Pit–hole confusion (kasıtlı olmalı)
Pit ve hole benzer görünüyor → bu tasarımın amacı. Ama pit yerleşimi hole'dan min 200 px uzakta olsun → kasıtlı karıştırma değil, tasarım kazası olmamalı.

## 10. Spring safety zone
Spring pozisyonu yatay rolling trajectory'de olursa top teğet geçerken dikey fırlatılır → player irrite olur. 

**Kural**: spring'i ya tek-yönlü darlık içinde koy (ball sadece üstten düşer), ya da ball trajectory'den en az 40px ötede (yan teğet olmayacak).
