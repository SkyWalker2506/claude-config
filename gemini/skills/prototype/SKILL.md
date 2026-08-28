---
name: prototype
description: >-
  Bir GDD'yi ya da oyun fikrini Three.js + Web Audio ile oynanabilir, juicy bir
  prototipe cevirir. Tasarim bastan kilitlenir, plan onaylandiktan sonra SORU
  SORMADAN sonuna kadar uygulanir. Kullan: "prototip uret", "gdd'den prototip",
  "oyun prototipi", "playable prototype", "three.js prototip", "prototype".
metadata:
  version: v1
  publisher: musab
---

# prototype — fikrin ise yaradiginin kaniti

Oyun yapmiyorsun. **Oyun fikrinin ise yaradiginin kanitini** yapiyorsun.

> Hiz > Mimari · His > Icerik · Oynanir > Mukemmel

**Hedef:** tarayiciyi ac -> tikla -> **saniyeler icinde oyna.** Yukleme ekrani, giris
akisi, menu labirenti yok.

---

## 0. Calisma sozlesmesi — bu bolum pazarlik disi

### Derin dusun, sonra hizli yaz

Bu ortamda ayri bir "Deep Think" modeli yok. Onun yerine **sen** derinlestir:

- Oturumu **`gemini-3.7-flash-high`** ve **`--effort high`** ile kos. Ortamda daha
  derin bir muhakeme secenegi varsa (Deep Think, extended thinking, ust reasoning
  kademesi) **onu ac** — varsa her zaman en yuksegini kullan.
- **Kod yazmadan once** sessizce sunlari cozumle ve `PLAN.md`'ye yaz: cekirdek
  dongunun tam akisi, hangi anlarin gorsel geri bildirim istedigi, veri modeli,
  dosya sinirlari, hangi sayilarin `data/config.js`'e gidecegi, ilk 3 muhtemel
  kirilma noktasi ve her birinin karsi tedbiri.
- Bu cozumleme **bir kez** yapilir, derinlemesine. Sonra kodlama fazinda muhakemeyi
  kis: makul olani yaz, ekrana bak, duzelt. Her satirda yeniden dusunmek prototipi
  oldurur.

### Ne zaman sorarsin, ne zaman sormazsin

| Asama | Davranis |
|---|---|
| Baslangic, GDD/fikir belirsiz | **TEK mesajda** en fazla 4 soru sor: tur ve referans oyun · ton · kamera/bakis acisi · oyuncunun ana eylemi. Cevabi bekle. Kapsam gercekten bulanıksa `/grill-me` ile tek tur mulakat yap — ama **bir tur**, sonra kes. |
| GDD verildi ama supheli | Tek paragraf ozet + tek soru: "boyle mi anladim?" Onay bekle. |
| GDD/plan onaylandi | **Bu noktadan sonra HICBIR SEY icin sorma.** |

Plan onaylandiktan sonra: karar gerektiginde **en makul varsayimi sec, secimini
`PLAN.md`'ye tek satirla yaz ve devam et.** Onay bekleme, secenek listesi sunma,
"devam edeyim mi" deme. Kullanici zaten "yap" dedi.

Tek istisna: **veri kaybi riski** (dosya silme, force push, repo sifirlama) ve
**para harcayan** islemler. Onlari sor.

### Bitene kadar surdur

Bu skill `goal` skill'i ile birlikte calisir. Faz 1 biter bitmez `goal` kriterlerini
yaz ve **kriterler yesillenene kadar durma**. "Bir sonraki adima geceyim mi" diye
sorma — gec. Uc ardisik turda hicbir kriter degismezse dur ve neden tutmadigini yaz.

### Paralellik

Kod tek akista yazilir — **isi paketlere bolme.** Olculmus: 19 pakete bolunmus bir
kosu, tek akisin ayni ciktisini 17 kat surede uretti; paketler birbirinin arayuzunu
beklerken zaman gitti ve iki paket ayni nesne icin iki ayri sema uydurdu.

`teamwork-preview` / `define_subagent` / `invoke_subagent` **yalnizca su ucu** icindir:

1. **Sanat / asset uretimi** — `generate_image` turlarini burada kos. Ajanin kod ile
   tek temas noktasi `data/art.js` manifestidir; `src/` altina dokunmaz.
2. Prototip **KOSTUKTAN SONRA** hata ayiklama ve optimizasyon
3. Tek seferlik arastirma (kutuphane secimi, API sekli)

Bunlarin disinda subagent acma. Cekirdek dongu, ses, UI, juice — hepsini sen yaz.
Sanat ajanini `define_subagent` ile tanimlarsan sistem promptuna sunu koy:
"assets/ ve data/art.js disinda hicbir dosyaya yazma".

---

## 1. Teknoloji — sabit, tartisilmaz

- **Three.js** (ESM, import map). Baska 3D/oyun motoru yok.
- **Web Audio API** ile prosedurel ses. Harici ses dosyasi yok.
- Framework yok, build step yok, bundler yok. `index.html` ac, calissin.
- Harici partikul/tween kutuphanesi yok — kendin yaz, 40 satirdir.

Cevrimdisi calismasi gerekiyorsa `vendor/three.module.js` ile vendor'la; yoksa CDN.
**Karari sen ver, yaz, gecme.** Sonradan degistirmek dagitim adimini yeniden yazmaktir.

---

## 2. Fazlar

Sure tablosu bir **planlama kisitidir**, kesme sayaci degil. Kapsami 30 dakikaya gore
sec; is tasarsa **calisir hale gelene kadar devam et**, sonra dur.

| Faz | Sure | Cikti |
|---|---:|---|
| 0 · Tasarim kilidi | 2 dk | tek sayfa GDD **onaylanmis** — tek bloklayan adim |
| 1 · Analiz + plan | 5 dk | `PLAN.md`, `SCOPE.md`, `ART.md`, `.goal/criteria.json` |
| 2 · Iskelet | 5 dk | `index.html`, `data/config.js`, bos sahne, kamera, input |
| 3 · Cekirdek dongu | 12 dk | oyuncu eylemi -> geri bildirim -> odul |
| 4 · Juice + ses | 6 dk | partikul, shake, punch, prosedurel ses |
| 5 · Bak ve duzelt | 4 dk | ekran goruntusu, en yuksek etkili duzeltmeler |
| 6 · goal dongusu | acik | kriterler yesillenene kadar |

**Asla kesilmeyen uc sey:** cekirdek dongunun calisir olmasi, juice katmani, teslim
edilenin hatasiz acilmasi. Bunlar bitmeden sure bahane degildir.

### Faz 0 — Tasarim kilidi

Tek sayfa GDD'nin alti basligi: **tur ve referans oyun · cekirdek dongu · oyuncunun
ana eylemi · kazanma/kaybetme · ton (cozy/gergin/komik/agir) · kamera ve bakis acisi.**

GDD dosyasi verildiyse oku, bir paragrafla ozetle, onay al. Sadece fikir verildiyse
GDD'yi sen yaz, goster, onay al. **Onaydan sonra hicbir sey icin durma.**

### Faz 1 — Analiz + plan

Cekirdek donguyu cikar:

```
oyuncu eylemi -> geri bildirim -> odul -> ilerleme -> tekrar
```

Dort soruyu cevapla: ana oyuncu eylemi ne · kazanma sarti ne · kaybetme sarti ne ·
**hangi anlar gorsel geri bildirim istiyor**.

`SCOPE.md` — 10 satir:
- **Olmali:** cekirdek mekanik, oyuncu etkilesimi, minimum UI, kazan/kaybet, geri bildirim
- **Olsa iyi:** ikincil sistemler, ekstra icerik
- **Yok:** save, tutorial, ayarlar, coklu oyuncu, ECS, backend

**Ilk prototip 1-3 dakikalik oynanis.** GDD 7 gun istiyorsa 2 gun yap; 10 kart
istiyorsa 4 kart.

`ART.md` — kesilmis kapsamda ekranda gorunen her sey, id + tek cumle:

```
hero          oyuncu karakteri, 3/4 acidan, tek poz
enemy_wolf    dusman, yandan
tile_grass    zemin karosu, tileable
ui_panel      HUD paneli, 9-slice
```

Sonra `.goal/criteria.json` yaz (bkz. `goal` skill'i) ve **beklemeden Faz 2'ye gec.**

### Faz 2 — Iskelet

```
index.html          tek giris, import map ile three
src/main.js         boot + dongu
src/Game.js         game.state = { score:0, day:1, coins:0 }   <- duz nesne
src/systems/        Effects.js, Audio.js, Input.js, Art.js
src/entities/       oyuna ozgu olanlar
data/config.js      TUM ayarlanabilir sayilar, tek dosya
data/art.js         asset manifesti — sanat hattinin dokundugu TEK kod dosyasi
```

Basit tut: Redux yok, DI yok, her yere EventBus yok. Kalitim yerine kompozisyon.

**Iki sozlesme zorunlu, Faz 2'de kurulur, sonradan eklenmez:**

**a) `game.advance(seconds)`** — simulasyonu gercek zaman beklemeden sabit adimlarla
ilerletir. Bunsuz 7 gunluk kampanyayi test etmek 35 dakika surer; bununla saniyenin
alti. `advance()` yalniz oyun mantigini degil **simulasyonun dokundugu her saati**
sanallastirmali: ses saati, `performance.now()`, animasyon zamani. Bir saat gercek
kalirsa sim sessizce hicbir sey yapmaz.

**b) Placeholder sozlesmesi** — `src/` icinde **hicbir yerde** `assets/...` yazmaz:

```js
// data/art.js
export const ART = { hero: 'assets/hero.webp' }

// kullanim
Art.get('hero')   // manifestte varsa texture; yoksa prosedurel placeholder
```

Yukleme basarisiz olursa placeholder'a dus. Eksik dosya yuzunden siyah sahne almak
bu hattin en pahali hatasidir.

**Girdi soyutlamasi:** oynanis kodu asla DOM olayina baglanmaz.
`input.isPressed('ACTION')`, `input.position()`. Masaustunde mouse+klavye, mobilde touch.

**Kamera:** 3D aksiyon/platform -> `PerspectiveCamera`. Strateji/izometrik/cozy ->
`OrthographicCamera`. Zoom, yumusak takip ve shake her ikisinde de olmali.

### Faz 3 — Cekirdek dongu

Sirasiyla: oyuncu bir sey yapabiliyor -> dunya tepki veriyor -> odul goruluyor ->
tekrar edilebiliyor. **Her adim calisir halde birak.** Yarim sistem, hic olmayan
sistemden pahalidir.

Asset onceligi: prosedurel geometri > basit texture > placeholder > gercek asset.
Agac = silindir govde + kure yaprak. Ev = kutu + egik cati. Once oynanisi dogrula.

### Faz 4 — Juice + ses — bu faz atlanamaz

Bu prototipin varlik sebebi: fikrin eglenceli olup olmadigi **hisden** anlasilir.

| Katman | Zorunlu |
|---|---|
| Hareket | smooth interpolation, ease, kamerada yumusama |
| Etki | scale punch (1.2x), kucuk rotasyon shake, partikul burst, ses |
| Kamera | zoom, yumusak hareket, shake **tek kanaldan** (`camera.setShakeOffset(x,y)`) |
| Partikul | hit (kucuk, rastgele hiz, fade) · collect (yukari, altin his) · level up (halka + shake) |

Partikuller **havuzlanir**, tavan koy (300 iyi bir sayi).

**Ses — Web Audio, harici dosya yok.** `AudioManager`: oscillator + frequency sweep +
gain fade. Collect = yukselen sweep. Hit = noise burst + dusuk frekans. Hata =
alcalan sawtooth. Basari = uc notali arpeggio. **Pitch varyasyonu ekle.**
AudioContext'i ilk kullanici etkilesiminde resume et.

### Faz 5 — Bak ve duzelt

**Ekran goruntusu al ve KENDIN BAK.** Rapor gorsel kanit degildir. Konsolu oku;
tek bir `Uncaught` bile teslim engelidir.

Okunabilirlik olcumu: ayirt edilmesi gereken sey viewport genisliginin **>= %6'si** mi?

### Faz 6 — goal dongusu

`goal` skill'ini devreye al. Kriterler yesillenene kadar OLC -> TESHIS -> DUZELT ->
TEKRAR OLC. Bu asamada kullaniciya soru yok, sadece tur raporu.

---

## 3. Sanat hatti — arka planda, seni bekletmez

Faz 1 biter bitmez baslar, Faz 2-6 boyunca arkada calisir. **Ana isi asla bloklamaz.**

1. **Stil arama:** ayni sahne, 10 farkli stil, TEK mesajda 10 numarali konu. Sahne
   **oyunun en yogun ANI** olmali ve oyun ici goruntu gibi kadrajlanmali — menu,
   kapak gorseli, "kazandin" ekrani yanlis secimdir. "Bu kareyi oyunun magaza
   sayfasina koyar miydim?" Cevap hayirsa yanlis sahne.
2. **Onay:** 10 kareyi numaralayarak goster, sec dedirt. Bu **tek bloklayan sanat
   adimidir** ama seni bloklamaz — sen bu sirada cekirdek donguyu yaziyorsun.
3. **Kilit:** secilen stil blogu harfi harfine sabittir. Tek kelime degistirirsen
   set ikiye bolunur.
4. **Turlar:** `ART.md` listesini 10'arli turlara bol, goruntuleme sikligina gore sirala.
5. **Entegrasyon:** her gorsel indikce -> WebP (`cwebp -q 82`) -> `assets/<id>.webp`
   -> `data/art.js`'e tek satir. `src/` altina dokunulmaz.
6. **Begenilmezse:** tum seti degil, **sadece o id'yi** yeniden uret, prompta neyin
   yanlis oldugunu tek cumleyle ekle. Stil turu en fazla iki kez tekrarlanir.

### Arac kullanimi

- **Gorsel uretimi: `generate_image`.** Stil arama turunu ve asset turlarini bununla
  kos. En-boy oranini sahneye gore sec (oyun ici kare icin `16:9`, kart/portre icin
  `3:2` ya da `1:1`). Var olan bir kareyi referans vererek (`ImagePaths`) varyasyon
  uretebilirsin — **stil kilidi icin bunu kullan**: secilen stil karesini referans
  gecerek sonraki asset'leri ayni dunyada tut.
- **Video uretimi YOK.** Text-to-video motoru bu ortamda yok. Hareket gerekiyorsa
  Three.js + Web Audio ile **gercek, calisan** sahne yap — sahte video yerine
  oynanan sey daha iyi cevap verir zaten.
- Uretim hatti tikanirsa **placeholder ile devam et** ve `README.md`'de hangi
  asset'in placeholder oldugunu yaz. Asset eksikligi prototipi durdurmaz.

---

## 4. Nerede biter

Prototip "bu fikir eglenceli mi" sorusunu cevapladiginda isini bitirmistir. Su ucu
birden saglaninca **dur**:

1. Cekirdek dongu oynaniyor
2. Kullanici oynadi ve cevap verdi
3. Gelen istekler yeni mekanik degil, var olani derinlestirme

Shader katmani, ses kimligi ve aranjman, konfor ayarlari, instancing, sprite animasyon
hatti — bunlar bu skill'in isi degildir. Yeni sistem/mekanik de degildir.

## 5. Basari olcutu: DOGRULUK degil HIS

Sorulan soru "dogru mu" degil, **"guzel mi, oynanir mi, tekrar etmek istiyor muyum"**.
Kapi suiti, mutasyon testi, determinizm kaniti yok. Dogrulama: `goal` kriterleri +
ekran goruntusu + 60 saniye oynamak. Calismiyorsa goreceksin; calisiyor ama sikici
ise hicbir test bunu soylemez.

## 6. Teslim

`README.md`: nasil calistirilir · kontroller · ne yapildi · **ne YAPILMADI ve neden**
· hangi asset gercek hangisi placeholder. Kesilen her sey burada gorunur olur.

## 7. Rapor

Is bitiminde `docs/runs/<YYYY-MM-DD-HHMM>-prototype-<oyun>.md` yaz: gorev · yapilanlar
(dosya yollariyla) · degisen dosyalar (`git diff --stat`) · dogrulama (hangi goal
kriterleri yesil, ekran goruntusu alindi mi) · yapilmayanlar. Kendi scratch/brain
dizinine degil, **repo icine**.
