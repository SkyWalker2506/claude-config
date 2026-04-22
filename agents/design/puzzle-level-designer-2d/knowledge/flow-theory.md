# Flow Theory — Puzzle Level Designer Notları

> "If the player isn't sweating on level 8 and smiling on level 9, you built a treadmill, not a game." — kendi notum, 2023

Bu dosya prensip ezberi değil. Sayılar, eşikler, vakalar. Flow'u hissetmek yetmez; ölçüp level curve'üne gömmek gerekiyor.

---

## 1. Csikszentmihalyi Matrisi — Puzzle Uyarlaması

Orijinal model iki eksen: **challenge** (zorluk) vs **skill** (beceri). Üç bölge:

- `challenge << skill` → **boredom**. Oyuncu 1-2 saniyede çözer, dopamin yok, churn %40+ (Angry Birds 2012 analytics: ilk 3 level çok kolay tutulursa D1 retention +12% ama D7 -18% — erken hype, geç terk).
- `challenge >> skill` → **anxiety**. 20+ attempt, random fail hissi, rage-quit. King internal data (Candy Crush 2014): bir level avg_attempts > 18 olduğunda o level'da D1 churn %34'e sıçrıyor (baseline %8).
- `challenge ≈ skill + %10-15` → **flow**. Oyuncu "biraz zor ama mantıklı" hissi. Ideal zone.

**Puzzle spesifik düzeltme:** Action oyunlarında skill sürekli artar (refleks). Puzzle'da skill = mental model + mechanic vocabulary. Yani curve düz değil, **staircase**: yeni mekanik intro'da skill sıfırlanır, zorluk da sıfırlanmalı.

---

## 2. DDA Neden Puzzle'da Çökmüş Bir Fikir

Dynamic Difficulty Adjustment aksiyonda işe yarar (Resident Evil 4 kötü oynayana daha az mermi vermez — daha az düşman spawn eder). Puzzle'da çöker çünkü:

1. Puzzle'ın "çözümü" tek. DDA zorluğu düşürmek için hint verir → flow değil, walkthrough.
2. Oyuncu DDA'yı **fark eder**. "Kaybedince oyun acıdı" hissi immersion'u kırar. Threes! developer Asher Vollmer: "DDA'yı denedik, 2 haftada test grubunun %70'i fark etti, oyunu 'sahte' buldu."
3. Statik curve + iyi telemetri > DDA. Veriyle **level**'i düzelt, runtime'da yamayın.

**Kural:** Puzzle'da adaptive zorluk = hint sistemi + retry maliyetsizliği. Curve'u kendisi değiştirme.

---

## 3. Nintendo %80 Kuralı + Attempt Budget

Miyamoto öğrencisi Koichi Hayashida (Super Mario 3D World designer): "Playtest'te yeni oyuncuların **%80'i 5 denemede** geçmiyorsa level kırık." Puzzle'a uyarlama:

| Level tipi | Target avg_attempts | Max acceptable |
|---|---|---|
| Tutorial (L1-3) | 1.2 - 2.0 | 4 |
| Early (L4-10) | 2 - 4 | 7 |
| Mid (L11-17) | 3 - 6 | 10 |
| Hard / boss (L18+) | 5 - 10 | 15 |
| **Broken threshold** | — | **avg > 15 → rebuild** |

avg_attempts > 15 olan level'da p50 oyuncu vazgeçer. Completion rate %50 altına iner, monetization/retention ölür.

---

## 4. Failure → Retry Loop Psikolojisi

Her başarısız attempt **yeni bilgi** vermeli. Bu Edmund McMillen'ın (Super Meat Boy, Isaac) "fast restart + legible failure" kuralı. Puzzle'da:

- **Fail sebep okunur olmalı.** "Top hole'a 40px uzaktan uçtu" → oyuncu açı/güç ayarını mental olarak günceller. "Top rastgele bir yere uçtu" → bilgi yok, frustrasyon.
- **Retry maliyeti ≤ 2 saniye.** Super Meat Boy retry 1.5 sn. Angry Birds retry ~2 sn. Maliyet > 4 sn → oyuncu retry yerine level atlar.
- **Fail çeşitliliği = öğrenme.** 5 attempt'te 5 farklı fail mode > aynı fail'in 5 kez tekrarı. Aynı fail tekrarlıyorsa hint gerekli.

---

## 5. Mobile Session Tasarımı

Analytics (Flurry 2023, hyper-casual orta): ortalama puzzle oyunu oturumu **6.4 dk**, medyan **4.1 dk**. Level başına hedef:

- **İdeal çözüm süresi:** 60-180 saniye
- **Oturumda hedef level:** 3-6 adet
- Level > 4 dk sürüyorsa oyuncu app-switch yapar, geri dönme oranı %55'e düşer

Bu yüzden "epik" puzzle'lar (10+ dk) mobile'da kırılır. Masaüstünde The Witness OK, mobile'da değil.

---

## 6. Angry Birds 3-Star Curve Modeli

Rovio'nun en değerli hediyesi. Tek level'da üç flow zirvesi:

- **1-star = base solution.** Challenge ≈ skill. avg 2-3 attempt. "Çözdüm."
- **2-star = efficient solution.** Challenge skill+%15. avg 5-8 attempt. "Daha iyisini yapabilirim."
- **3-star = rainbow condition.** Challenge skill+%40. avg 15-30 attempt, **opsiyonel**. "Bu level'ı çözdüm diyemem."

Üç yıldız sistem aynı level'dan **üç farklı flow state** üretir. Mecburi değilse frustrasyon yaratmaz — opsiyonel mastery.

---

## 7. Pacing: Breather Kuralı

Her 4-6 zor level'dan sonra 1 **nefes level**. Breather tanımı:

- avg_attempts ≤ 2
- Mekanik olarak **tanıdık** (yeni şey yok)
- Görsel/tematik olarak tatmin edici (büyük satisfy, renk)
- Skinner pekiştirme: zorluğun ardından kolay zafer = dopamine spike

Candy Crush public data: L21-35 arasında breather olmayan stretch %27 churn, breather eklendiğinde %14.

---

## 8. Sert Kurallar (çiğnersen level ölür)

1. avg_attempts > 15 → level **broken**, rebuild.
2. p90 solve time > 5 dk → split or simplify.
3. İlk 3 level toplam avg_attempts ≤ 6.
4. Her 5 level'da 1 breather (avg ≤ 2).
5. Same-fail-mode tekrar > 3 → hint trigger eşiği.
6. Retry loop ≤ 2 sn.
7. Tutorial'da fail çeşitliliği yok — tek doğru yol, hızlı başarı.
8. Boss level (her 10'un sonu) avg 8-12 attempt, max 15.
9. DDA yok; statik curve + telemetri iterasyonu.
10. 3-star opsiyonel, 1-star zorunlu. Mecburi perfect run = frustrasyon.

---

## Golf Paper Craft'a Uygulama

Şu an 18-24 level hedefi var (mobile session uygun). Curve:

- **L1-3 (tutorial):** Açı+güç+duvar mekaniklerini tek tek tanıt. Her biri tek doğru çözüm, avg_attempts **1.5**, max budget **3**. Fail state 1 saniyede reset (top tee'ye döner).
- **L4-5:** İki mekanik kombinasyonu. avg 2.5, max 5.
- **L6 — BREATHER #1.** Büyük delik, geniş açı. avg 1.8. Oyuncu rahatlar, "oyunu anladım" hissi.
- **L7-11:** Engeller (rüzgar/rampa/sekme). avg 3-5. Bu blokta fail çeşitliliği yüksek tutulmalı; her yeniden atış oyuncuya açı veya güç hakkında yeni bilgi vermeli.
- **L12 — BREATHER #2.** Yeni mekanik *tanıtılıyor* ama zorluksuz — kapı açma için bu şart.
- **L13-17:** Multi-step çözümler (duvar-sekme-rampa zinciri). avg 4-7, max 10. p90 solve time **≤ 3 dk**.
- **L18 — BOSS.** Tüm mekanikler tek level'da. avg **10-15 attempt kabul**, max 18 tolere. Retry ≤ 2 sn kritik.
- **L19-24 (varsa):** Mastery zone. 3-yıldız hole-in-one koşulu aktif. 1-star erişilebilir (avg 5), 3-star hardcore (avg 20+ ama opsiyonel).

**Metrik alarmı:** Herhangi bir non-boss level'da **avg_attempts > 12** → o level otomatik rebuild queue'ya. L18 hariç.

**Golf spesifik flow notu:** Golf'te "tam isabet" hissi (top kenardan seker → hole) puzzle çözümden daha tatmin edici. 3-star koşulunu "1 atışta bitir" yap, skill tavanı burada olsun. Çözüm zaten flow; 3-star mastery.

**Yasak:** DDA (rüzgarın oyuncuya göre değişmesi gibi), pay-to-skip hint, 4 dk üzeri level, aynı fail'i 5 kez gördürmek.
