---
name: animate
description: "Statik AI gorselini hareket ettirmenin yolunu secer ve kurar: katmanli cutout + motor animasyonu (varsayilan), image-to-video flipbook (nadir anlar), shader (son care). Sprite sheet uretmeye calismaz — tutarliligi modelden degil hattan alir. Triggers: animate, animasyon, karakter animasyonu, sprite sheet, sprite animasyon, flipbook, rig, rigle, kart animasyonu, hareket ekle, idle animasyon, nefes animasyonu."
user-invocable: true
argument-hint: "[hedef: karakter | kart | ui | efekt]  (bos birakilirsa projeden cikarilir)"
---

# /animate — statik gorseli hareket ettir

Elde tek bir AI gorseli var, hareket etmesi isteniyor. Bu skill **hangi yolun
secilecegini** ve secilen yolun **nasil kurulacagini** anlatir.

> Tutarlilik modelden degil hattan gelir · Animasyon veri, gorsel degil · Ölçüm > goruntu

---

## Degismeyen kural: sprite sheet uretmeye calisma

AI ile sprite sheet zor, cunku sorun prompt kalitesi degil **temporal tutarlilik**.
Gorsel modeli her kareyi bagimsiz uretir; 6 kare istersin, 6 farkli karakter gelir —
kulak boyu, goz mesafesi, renk tonu, siluet kayar. Grid halinde tek gorselde istersen
hucre hizalamasi ve pivot kaymasi bozuk gelir; kesip motora koydugunda karakter ziplar.

Daha iyi prompt bunu bir miktar iyilestirir, **cozmez**. Iki gecerli strateji var:

1. **Hic cok kare uretme.** Tek gorsel uret, hareketi motor tarafinda yap.
2. **Tutarliligi isi olan modeli kullan.** Image-to-video zaten tutarli hareket uretir;
   sonra kare cikarirsin.

"Bir daha deneyelim, belki bu sefer tutar" **dongusune girme.** Uc denemede tutmadiysa
yol yanlis, prompt degil.

---

## Yol secimi

| Yol | Tutarlilik | Dongu maliyeti | Kontrol | Ne zaman |
|---|---|---|---|---|
| Prompt ile sprite sheet | Dusuk | Yuksek | Yok | **Hicbir zaman** |
| Referansla kare kare uretim | Orta | Yuksek | Az | Hicbir zaman |
| **Katmanli cutout + motor animasyonu** | **Tam** | **Dusuk** | **Tam** | **Varsayilan** |
| 2D iskelet rig (Sprite Skinning) | Tam | Orta | Tam | SpriteRenderer dunyasi, agir karakter |
| Image-to-video -> flipbook | Yuksek | Orta | Az | 1-2 "hero" an |
| Shader deformasyon | Tam | Dusuk | Orta | Son care (asagidaki mayinlar) |

**Varsayilan katmanli cutout'tur.** Digerine gecmek icin gerekce yaz.

---

## 1 · Katmanli cutout (varsayilan yol)

Karakteri tek poz olarak degil, **ayri parcalar** olarak uret. Her parca **bir kez**
uretilir, sonsuza kadar kullanilir — "ayni karakteri tekrar uret" demek zorunda
kalmadigin icin kimlik kaymasi diye bir sey kalmaz.

### Katman listesi (karakter icin taban set)

| Katman | Pivot | Neden ayri |
|---|---|---|
| govde | alt orta | nefes olcegi buradan |
| kafa | boyun tabani | hafif gecikmeli takip |
| kulak (L/R ayri) | kulak tabani | flick, faz kaymali |
| kuyruk | kok | salinim |
| on kol (L/R ayri) | omuz | tepki, tutma |
| goz kapagi | goz ust kenari | kirpma |
| aksesuar (fincan, tabak) | temas noktasi | bagimsiz hareket |
| overlay (buhar, parilti) | serbest | dongusel kayma + fade |

Parca sayisini sismele. **8-10 katman** cogu kart karakteri icin yeter. Her ek katman
hem uretim hem hizalama borcudur.

### Hareket katalogu (baslangic degerleri)

| Hareket | Ne | Sure | Not |
|---|---|---|---|
| nefes | govde `scale(1, 1.02)` | 1.6-2.0s | ease-in-out, sonsuz |
| kafa takibi | `translateY` 1-2px | nefesle ayni sure | **faz kaymali**, aksi halde blok gibi hareket eder |
| kuyruk | `rotate` ±5-8° | 2.2-2.8s | nefesle ayni sure OLMASIN |
| kulak flick | `rotate` -12° tek atim | 90ms | 4-7s'de bir rastgele |
| goz kirpma | goz kapagi `scaleY` 0->1->0 | 110-130ms | 3-6s'de bir rastgele |
| buhar | `translateY` -20px + `opacity` 0.6->0 | 2.5-3.5s | dongusel, birden fazla kopya faz kaymali |
| kart tepkisi | butun kart `scale(1.03)` + golge katmani offset | 120ms | hover/play |

**Faz kaymasi hayati.** Butun katmanlar ayni periyotta ayni yonde hareket ederse
karakter canlanmaz, tek parca gibi salinir. Her katmana farkli periyot **ve** farkli
baslangic gecikmesi ver.

### Unity UI Toolkit gercegi (once oku, sonra yaz)

- **USS'de `@keyframes` / `animation` YOK.** Sadece `transition-*` var. Donguyu
  kendin surmen gerekir:
  - `element.schedule.Execute(...).Every(ms)` ile class toggle -> transition ping-pong, veya
  - `element.experimental.animation.Start(from, to, ms, cb)` ve `cb` icinde tekrar baslat, veya
  - `TransitionEndEvent` ile ping-pong.
  Bunu bilmeden USS'e `animation:` yazarsan **sessizce hicbir sey olmaz.**
- `transform-origin`, `translate`, `rotate`, `scale`, `opacity` USS'de var ve calisir.
  Pivot'u `transform-origin` ile ver, parcayi kaydirarak taklit etme.
- **`transform` olcumu sisirir.** `resolvedStyle`/`worldBound` donusum uygulanmis
  dikdortgeni verir; animasyon sirasinda olcum alma.
- Katman sirasi UXML sirasidir; `position: absolute` + `transform-origin` ile ustuste bindir.
- Font/gorsel her Label/Element sinifi icin ayri set edilir, kokte tek sefer yetmez.

Web/Three.js hedefinde ayni katman mantigi gecerli, orada `@keyframes` gercekten var —
dongu icin kod yazmana gerek yok.

### Neden bu yol

1. Tutarlilik **uretimden degil yapidan** gelir.
2. Animasyon **veri**dir: zamanlamayi begenmedin, sayiyi degistir, 5 saniye.
   Sprite sheet'te ayni degisiklik = yeniden uret + yeniden kes + yeniden import.
3. Motor-native: shader yok, filter yok, RenderTexture yok.
4. Olceklenir: 40 kart icin 40 sheet degil, tek rig sablonu + 40 parca seti.

---

## 2 · Image-to-video -> flipbook (nadir anlar)

Transform'la taklit edilemeyen hareketler icin: squash-stretch'li zipla, kart oynanma
reaksiyonu, yikilis. Tek referans gorselden image-to-video uret, **6-10 kare** sec.

- **Her karta degil**, sadece nadir ve dikkat cekilen anlara uygula. Maliyeti ve
  tutarlilik riskini o birkac yere hapset.
- Sheet sart degil: UITK'da `background-position` ile atlas kirpabilir ya da kod
  tarafinda tek tek gorsel degistirebilirsin. **Tek tek gorsel daha az tuzakli.**
- Kare secerken **ilk ve son kare ayni poza donmeli**, yoksa dongu ziplar.

---

## 3 · Shader (son care)

Shader'i **karakteri deforme etmek icin degil, ambiyans icin** dusun: isik supurmesi,
foil parlamasi, sicak-soguk renk nefesi.

Ve bunlari once **katmanli PNG + transform** ile dene — isik supurmesi, ustte duran bir
gradient katmanin `translateX` animasyonundan baska bir sey degildir.

**UITK'da shader mayinlari (olculmus):**
- Built-in RP'de UI icin Shader Graph yok.
- UITK filter'lari custom shader ister; custom filter style traversal'i cokertiyor.
- UITK overlay kamera tarafindan yakalanmiyor — ekran goruntusuyle dogrulama yaniltir.

Shader'a ancak **USS + katmanin yetmedigi kanitlandiginda** gec. Gerekcesiz gecme.

> Oyun ici (UI degil) sprite'larda shader ve oyun hissi katmani ayri bir skill:
> **`/juice`** — squash/yuruyus, hit flash, vurus kenari, hitstop, kamera
> sarsintisi, havuzlanmis efekt katmani, aura, cozulme. Bu skill karakteri
> parcalara boler; `/juice` o parcalara (ve tek sprite'lara) tepki verdirir.

---

## Uretim promptlari

- **Arka plan seffaf istenir.** Parcalar ustuste binecegi icin varsayilan budur.
- **Tek istisna:** konu beyaz/cok acik renkliyse seffaf isteme — model beyaz bolgeleri
  de siler. O parcada duz koyu zemin iste, kodda kes.
- Her prompt **tek basina calisir** — ortak stil basligina yaslanma, stil cumlesini
  her prompta tekrar yaz.
- Tek mesajda **en fazla 10** prompt. Fazlasi tek sayfaya birlesip geliyor.
- Parcalar **tek tek** istenir, "tum parcalari tek gorselde ver" denmez.

Sablon:

```
[parca adi] — [karakter tanimi], [poz/aci], [karakteristik detay]
Stil: [tam stil cumlesi — her promptta tekrar yazilir]
Arka plan: seffaf
Kadraj: parca merkezde, kenarlarda %10 pay, kirpma yok
Pivot referansi: [nereden baglanacagi — orn. "kulak tabani alt kenarda"]
Cozunurluk: kare, en az 1024
Metin, yazi, imza, watermark YOK
```

**Pivot referansini prompta yaz.** Bagli kenar kadrajin disinda kalirsa parca motorda
dogru donmez ve yeniden uretim gerekir.

---

## Kanit kurali

Animasyon iddiasi **tek kareden kanitlanamaz.** "Ekledim" kanit degildir.

| Iddia | Kanit |
|---|---|
| Katman hareket ediyor | Dongunun iki ucundan kare al, farki goster |
| Faz kaymasi var | Iki katmanin ayni anki degerini logla, esit olmasin |
| Dongu akici | Kare suresi medyani, once/sonra |
| Efekt gorunur | Efekt kapali/acik iki kayit, yan yana |

USS'e yazip hicbir sey olmamasi UITK'da **sessiz** basarisizliktir — `animation:`
ozelligi yok sayilir, hata vermez. Her animasyonu calisirken dogrula.

---

## Anti-pattern'ler

- Sprite sheet prompt'unu ucuncu kez denemek.
- Butun katmanlara ayni periyodu vermek (canlanmaz, salinir).
- Parca sayisini 20'ye cikarmak (hizalama borcu uretim kazancini yer).
- USS'e `animation` / `@keyframes` yazip calistigini varsaymak.
- Beyaz konuda seffaf arka plan istemek.
- Karakteri deforme etmek icin dogrudan shader'a atlamak.
- Animasyonu ekran goruntusuyle "dogrulamak".
