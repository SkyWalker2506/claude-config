# 2D Puzzle Level Design Principles

## 1. One Puzzle, One Lesson
Her level TEK bir merkezi soru sormali. Bu soru yeni bir mekanik ya da iki tanidik mekanigin yeni bir kombinasyonu olabilir. Oyuncu level bittikten sonra "bunu ogrendim" diyebilmeli.

## 2. No Brute-Force Solution
"Full guc + duz atis" ya da benzeri lineer en basit cozum, level'i trivialize etmemeli. Engel konumlamasi bunu fiziksel olarak imkansiz kilmali (ornek: delik bir duvarin arkasinda, yukseklikte, ya da overshoot cezasi olan su dipi).

## 3. Teach → Practice → Combine → Twist
- **Teach**: Yeni mekanik izole edilmis, basit setup
- **Practice**: Ayni mekanik daha zor setup
- **Combine**: Yeni + eski mekanik birlikte
- **Twist**: Mekanigin ters/bosaltici kullanimi (ornek: trampoline genelde yukari firlatir, burada geri firlatir ki delige duselim)

## 4. Multiple Valid Paths (opsiyonel ama iyi)
Bir level'da 1 "kanonik" cozum olmali ama oyuncu deneysel yol bulabilmeli. Bu player agency yaratir.

## 5. Hole Position Variety
- Ortada (overshoot cezasi)
- Yuksek platformda (acili atis gerektirir)
- Engel arkasinda (duz cizgi imkansiz)
- Yolun sonunda + hemen sonrasi risk (hassasiyet)
- Basta/tersten (oyuncu geriye gonderecek mekanik)

## 6. Risk-Reward Density
Her level'da en az bir "risk alirsan 1 atista, guvenli oynarsan 3 atista" karari olmali.

## 7. Visual Teaching
Engel pozisyonu oyuncuya cozumu ima etmeli (ornek: trampoline bir duvardan once konulursa, "zipla" ipucu verir).

## 8. Fail State Clarity
Olum/reset tetikleyicileri (su, pit, crocodile) gorsel olarak net, sinir belirsizligi olmamali.

## 9. Upgrade-Proofing
Oyuncu power/precision/assist upgrade'leriyle geldiginde bile level cozum icin "dusunme" gerektirmeli. Upgrade'ler "rahatlama" saglar, "atlatma" degil.

## 10. Crescendo But Not Linear
Zorluk artisi monoton degil — 3 zor levelden sonra 1 "nefes" level iyi sinyaldir. Ama genel yon artan olmali.
