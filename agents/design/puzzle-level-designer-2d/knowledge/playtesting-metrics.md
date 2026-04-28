# Playtesting Metrics — Senior Not Defteri

> Sayi yoksa opinion var. Designer'in gorusu degil, oyuncunun parmagi konusur. Asagidaki esikler negotiable degil — altina dusersen level bozuk, ustune cikarsan cilali.

## 1. Key Metrikler (hepsi per-level)

| Metrik | Tanim | Neyi Olcer |
|--------|-------|------------|
| `avg_attempts` | Level'i tamamlayana kadar ortalama deneme sayisi | Zorluk |
| `fail_rate` | (fail eden try / toplam try) % | Frustration proxy |
| `time_to_solve` | Level'e ilk girisle ilk win arasi sure (median) | Kavrama hizi |
| `completion_rate` | Level'e giren oyuncunun % kaci bitiriyor | Retention cikisi |
| `quit_after_level` | Bu level'i bitirip oyunu birakan oyuncu % | Fatigue / closure |

`median` kullan, `mean` degil — tek bir 400 denemelik outlier ortalamayi bozar. Her metrigi en az **n=30 oyuncu** ile olc; altinda istatistiksel gurultu.

## 2. Rage-Quit Thresholdlari (rakamli, tartisilmaz)

- `avg_attempts > 15` → **level kirik**, yeniden tasarla (patch degil, rework).
- Erken level (ilk 5) `fail_rate > 70%` → **difficulty curve yanlis**, oyuncu onboarding'te kaybediliyor.
- `quit_after_level > 25%` → **blocker level**. Hemen sonraki patch'te dusur.
- `time_to_solve > 180s` (casual / mobile) → oyuncu hedefi anlamiyor, **readability problemi** (puzzle zor degil, gorsel muglak).
- `completion_rate < 40%` → level listede kalmamali.

Bu esikler "hissetmek" icin degil, build-reject kriterleri. PR'da bu sayi varsa merge yok.

## 3. Nintendo "%80 first-try success" ve Attempt Budget

Nintendo'nun Mario tasariminda icsel kurali: **tutorial / onboarding levellarinda ilk denemede gecme orani ≥ %80 olmali**. Mekanik ogretmek, zorluk test etmek degil hedefin. Bu rakami ilk 3-5 level icin benimse.

Attempt budget — level tier'ina gore hedef `avg_attempts` bandi:

| Tier | Hedef avg_attempts | Hedef fail_rate | Hedef time_to_solve |
|------|--------------------|-----------------|----------------------|
| Tutorial (L1-L3) | 1.2 – 2 | < 20% | < 30s |
| Early (L4-L7) | 2 – 4 | 20-40% | 30-60s |
| Mid (L8-L14) | 5 – 8 | 40-55% | 60-120s |
| Late (L15-L17) | 7 – 12 | 50-65% | 90-180s |
| Boss (L18+) | 10 – 15 | 60-75% | 120-300s |

**15 ustune cikan boss levelleri** "hatirlanan boss" degil, "silinme sebebi"dir. Dark Souls'u taklit etmiyorsun — casual puzzle'sin.

## 4. Heartbeat Funnel (L1→Lson)

Her level bir filtre. Beklenen kayip orani:

- L1 → L2: max **%5 drop** (eger daha fazlaysa onboarding kirik)
- L2 → L10: her levelde **%2-4 drop** kabul edilebilir
- L10 → boss: her levelde **%5-7 drop**
- Boss completion: toplam install'in **%15-25'i** ulasmali

Funnel grafigi cizdiginde "duz inen egim" istersin. **Dikey cikis** (bir levelde %20 drop) → acil rework. Yatay plato + sonra cakilis → **fatigue**, level sayisini azalt ya da pacing ekle.

## 5. Analytics Yoksa: Designer Self-Test Protokolu

Backend yok, telemetri yok, tek kisilik studio — sorun degil. Protokol:

1. **10 bagimsiz run** yap. Her level icin attempt sayisi ve sureyi kaydet.
2. Level'i bitirdikten sonra **15 dakika bekle, sonra tekrar oyna** — muscle memory'yi bozmak icin.
3. Her 3 run'da bir **yanindakine oynat** (1 esitlenmis cold-player = 5 senin run).
4. Cold player ilk 30 saniyede hedefi anlayamadiysa → UX fail, zorluk fail degil.
5. Kendi avg_attempts'ini **2x yap** gercek oyuncu projeksiyonu icin (designer bias factor).

10 run + 3 cold player = minimum gecer not. Daha azi "umuyorum iyidir" demektir.

## 6. Hidden Metrics (loglamadan fark edilmeyen)

- **Input heatmap**: oyuncu nereye bastı / nereyi surukledi. Solution alani disinda %40+ input varsa **yanlis affordance**.
- **Attempt angle/power distribution**: golf/angle tabanli oyunda oyuncular hangi acida kumelenyor? Dar kume = levelde tek cozum var, oyuncu bunu buldu. Genis kume = kesfetme saglikli.
- **Retry cadence**: fail sonrasi reset suresi. < 2sn = oyuncu sabirli / engaged. > 10sn = oyuncu dusunuyor (iyi) ya da menude kayboldu (kotu).
- **Undo / reset count**: yuksekse oyuncu "commit etmekten korkuyor" — risk readability dusuk.

## 7. Dead Drop — Sessiz Olum

Oyuncu level'i gecti ama **cozmedi**. Semptomlar:

- avg_attempts dusuk AMA time_to_solve anormal kisa → **speedrun cheese** / exploit.
- completion_rate yuksek ama `quit_after_level` da yuksek → oyuncu kazandi ama **tatmin olmadi** (lucky overshoot, fiziksel sanslilik).
- Hidden: win pozisyonu ile "intended solution" pozisyonu arasinda > 1.5x tolerance → oyuncu yanlisliktan kazandi.

Dead drop **rage-quit'ten daha tehlikeli**, cunku analytics'te iyi gorunur. Sadece manuel replay ile yakalanir. Her 5 level'de bir **win replay'lerinden rastgele 5 tane izle**.

## 8. Regression Testing (balance patch sonrasi)

Bir mekanik / paramtre degisti → hangi leveller etkilendi?

1. **Dependency graph tut**: her level icin kullandigi mekanik + parametre listesi.
2. Parametre degisince graph'tan etkilenen tum levelleri cikar — bunlar regression pool.
3. Regression pool'daki her level icin **3 run minimum** (yeni parametreyle).
4. Onceki `avg_attempts` ± %25 disina cikanlari flag'le.
5. Boss levellari **her patch'te tekrar test et**, bagli olsun olmasin.

"Kucuk degisiklik, test etmeye gerek yok" cumlesi patch note'larin en tehlikelisidir.

## 9. Concrete Kurallar (yazili tahta)

1. `avg_attempts > 15` olan level shipable degil.
2. Tutorial levellarinda fail_rate > %30 → onboarding rework.
3. `quit_after_level` > %25 → next patch must-fix.
4. Her level mekanigi en az **2 level** boyunca kullanilmali (ogret → pekistir), tek kullan-at mekanik yok.
5. Zorluk monotonik artmali: `avg_attempts[n+1] >= avg_attempts[n] - 1` (kucuk nefes ok, cakilma yok).
6. Boss level fail_rate %75'i gecmeyecek — caydirici, asilmaz degil.
7. Time_to_solve ortalamasi 180sn asti → **checkpoint / partial progress** ekle.
8. Cold player 30sn icinde hedefi anlayamadi → visual redesign, level degil.
9. 10 self-test + 3 cold player geçmeden level ship edilmez.
10. Her patch sonrasi boss levellari yeniden test — bagimsiz mi, bagimli mi fark etmez.

---

## Game-specific playtesting notes
Any game-specific thresholds, boss numbers, or level IDs belong in the relevant game-pack.

Golf Paper Craft:
- `../game-packs/golf-paper-craft/playtest-notes.md`
