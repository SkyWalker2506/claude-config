---
name: image-prompt
description: "Gorsel uretim promptlarini dogrulanmis 10'luk batch formatinda yazar ve cikan paleti olcerek dogrular. Sepya-yikama ve kolaj tuzaklarini prompt seviyesinde onler. Triggers: image prompt, gorsel prompt, resim promptu, asset prompt, kart gorseli, batch gorsel, art prompt, 10 resim."
user-invocable: true
argument-hint: "[konu/proje] — orn. 'kart gorselleri' veya 'ikon seti'"
---

# /image-prompt — Batch Image Prompt Generator

Illustration, key art, ikon ve prop promptlarini **tek istekte 10 ayri gorsel** formatinda
yazar. Uretim sonrasi paleti olcup dogrular.

**Promptu yazdirmakla kalmayip uretimi de calistirmak istiyorsan:**
`/image-run <sohbet adi>` — adi verilen ChatGPT sohbetinde promptu gonderir,
1 dk'da bir kontrol eder, biten seriyi toplu indirir, sonraki batch'e gecer.
Bu skill promptu **yazar**, `/image-run` onu **calistirir**; ikisi birlikte kullanilir.

**Bu skill degil, sunun icin:** sprite strip / animasyon / asset-browser hattina asset
uretiyorsan `/asset-prompt-gen` kullan — o config-driven, magenta BG'li, 1×8 strip mantigi.
Bu skill tek kare illustrasyon ve kart gorselleri icin.

---

## Kural 0 — Prompt her zaman Ingilizce

Gorsel uretim modelleri Ingilizce promptta belirgin sekilde daha iyi sonuc veriyor:
sahne tarifi daha isabetli, negatifler daha guclu tutuyor, stil terimleri
("gouache", "alla prima", "atmospheric perspective") karsiligini buluyor.

**Prompt metninin tamami Ingilizce yazilir** — stil blogu, sahne cumleleri,
negatifler, hepsi. Kullaniciyla sohbet Turkce kalir; sadece ChatGPT'ye giden
metin Ingilizcedir. Turkce sahne tarifi yazma, ceviri de yaptirma.

---

## Kural 1 — Tek istek, 10 sahne, tek stil blogu

Hedef aracin (ChatGPT gorsel uretimi) tek turda ~10 gorsel uretebiliyor. Format:

```
Generate 10 separate images, one for each numbered scene below.
IMPORTANT: output each as its OWN separate image file. Do not combine them into a
grid, contact sheet, collage or single canvas.

STYLE (applies to all 10): <stil blogu, ~60-70 kelime>

1. <sahne bir cumle + kadraj notu>
2. ...
10. ...
```

**Neden boyle:** "her prompt tek basina, stil blogu 10 kez tekrar" formati bu arac icin
yanlis. Uzun tekrar GPT'yi seri anlatimina sokuyor ("simdi sadece 2. gorseli uretiyorum,
digerini yok sayiyorum") ve 10'u tamamlamadan kesiyor.

**Ilk satir yuk tasiyor.** `Generate N separate images...` promptun **birinci**
satiri olmali. Onune bir damga, baslik veya aciklama koyarsan model istegi tek bir
konu gibi okuyup tek birlesik gorsel uretiyor. Damga gerekiyorsa **en sona** koy ve
icine konu/id listesi yazma.

**Prompt metninin icine batch iskelesi YAZMA.** `--- 1/10 -> dosya.png ---` gibi basliklar
modele "bu bir seri isi" dedirtiyor ve anlatmaya basliyor. Dosya adlari prompt'un
disinda, sohbet metninde numarali liste olarak verilir.

**10'dan fazla isteme.** Fazlasi tek contact sheet'e birlesiyor. 11+ konu varsa 10'arli
bol; her batch kendi stil blogunu tasir.

**Inen dosyalarin sirasi prompt sirasiyla uyusmaz.** Eslemeyi dosya adina degil
**goruntu icerigine** bakarak yap; kullaniciya da sirayi ayrica yaz.

Kolaj gelirse tek satir duzeltme:
`Please separate these into individual image files. Do not use a grid, contact sheet or collage.`

---

## Kural 2 — Sepya-yikama tuzagi

En sik ve en sinsi failure mode. Su kelimeler **birlikte** yazildiginda model resmi
boyamak yerine ustune tek renk filtre geciyor:

> ❌ `aged paper tint over the whole image` · `warm dust haze` · `low contrast` ·
> `desaturated` · `muted` · `overcast diffused light` · `faded` · `vintage`

Sonuc: tum kareler 35-45° ton bandinda, gorsel *ici* ton yayilimi 5°, golge tonu = isik
tonu. Konusu ne olursa olsun — colde piyade, acik denizde gemi, karanlik sunucu odasi —
hepsi ayni kahverengi. **"AI ciktisi gibi durmak" dedigimiz sey teknik olarak budur.**

**Hastalik doygunluk eksikligi degil, tek filtre.** Karsiti "her seyi ciglastir"
degil; **paleti tasarlamak.** Solgun, tozlu, kirli yesil, gri-mavi, neredeyse tek
renkli bir palet — *secilmisse* ve kendi icinde ton/isi ayrimi tasiyorsa — tamamen
saglikli. Bozuk olan, konu ne olursa olsun ayni kahverengiyi ustune geciren
otomatik filtre.

Yerine yaz — uc parcali:

> ✅ **Isik:** `HDR tone mapping: luminous highlights, deep shadows that still hold
> detail, strong local contrast`
> ✅ **Palet:** projenin kendi paletini **acikca say** — hakim aile, aksan, ne
> olmayacagi. Orn. `a cool grey-green and slate palette, rust and bone as the only
> warm accents` ya da `sun-bleached ochre and chalk white, with deep teal shadow`.
> ✅ **Negatif:** `NO single-hue filter over the whole image, NO sepia or amber
> overlay, shadows must differ in temperature from the lights`

Negatif cumleyi **her zaman** ekle; pozitif tarif tek basina yetmiyor.

### Palet projeye aittir — sablon degil

Bu skill bir oyunun ihtiyacindan cikti ve o oyunun paleti (`vivid saturated colour
led by cool blues and greens`) ornekten cok kural gibi okunmaya basladi. **Oyle
degil.** Her yeni is icin paleti bastan sec:

1. Isin ne oldugunu sor — cozy oyun mu, karanlik survival mi, teknik illustrasyon mu?
2. Referansi varsa oradan cikar; yoksa 3-4 renkten olusan bir aile + 1 aksan yaz.
3. Ayni paleti tum batch'e tasi (stil blogu harfi harfine ayni), ama **sahnelerin
   kendi tonu olsun** — magara sicak, nehir soguk. Toplam ton bandini kendin dengele.

Doygunlugu "canli" diye yukseltme; ton *ayrimi* aradigin sey, sat% degil.

---

## Kural 3 — Tek yone asiri duzeltme yapma

Palet duzeltmesi isterken "olabildigince mavi" dedigimizde model **her kareyi gokyuzune**
cevirdi. Bir sonraki tur "abartma" geldi.

Ayni tuzak doygunlukta da var: sepyayi kovalarken "vivid saturated" yazip her kareyi
ciglastirmak da tek yone asiri duzeltmedir ve o da AI ciktisi gibi durur. Kural 2'deki
palet bolumu bunun icin var.

**Cozum:** kadraji sahne bazinda acikca yaz, dagilimi kendin dengele. 10'luk bir batch icin
saglikli dagilim:

| kadraj | adet |
|---|---|
| gok agirlikli (konu zaten gokte) | 2 |
| ic mekan / gok yok | 2 |
| yer seviyesi, ufuk 1/3, gok ust bant | 4-5 |
| yakin plan, ozne kadraji dolduruyor | 1-2 |

Her sahne cumlesine ufuk cizgisinin nerede duracagini yaz: `Horizon one third up; sky only
the top third.`

---

## Kural 4 — Arka plan: konuya gore karar ver

| icerik | arka plan |
|---|---|
| kart illustrasyonu, key art, sahne | **full-bleed** — seffaf degil. Kart plakasi opak, resim icine gomulu duruyor |
| ikon, amblem, kesme obje, portre, prop | **seffaf**: `transparent background, alpha channel, cut out, no backdrop, no shadow on the ground` |
| beyaz/acik VFX (shine, glow, burn, smoke) | **siyah zeminde maske** olarak iste, alpha'yi parlakliktan turet — seffaf isteyince model bosluga uydurma dolgu yapiyor |

Magenta chroma-key **isteme** — bu arac gercek alpha veriyor, magenta gereksiz ara adim.

---

## Kural 5 — Metin yok

Hicbir promptta baslik, wordmark, birlik isareti, rakam, logo, watermark isteme. Model
harfleri bozuyor, cikti kullanilamiyor. Wordmark ayri compositing adimi.

Her stil blogunun sonuna:
`Absolutely no text, letters, numbers, unit markings, logos or watermarks.`

---

## Kural 6 — Ictirik politikasi tetikleyicileri

`/asset-prompt-gen` icindeki tetikleyici kelime tablosu burada da gecerli — `battle damage`
→ `surface wear`, `muzzle flash` → `ignition flare`, `scorched` → `soot stain` vb. Askeri
konularda promptun tamami reddedilebiliyor; gorsel/mekanik dilde kal.

---

## Uretim sonrasi — olc, goz karari verme

Cikti geldiginde paleti **olc**. Goz "iyi gibi" der, sayi yalan soylemez.

```bash
python3 ~/.claude/skills/image-prompt/check_palette.py ~/Downloads/*.png
```

Ciktidaki dort sayi:

| olcum | saglikli | bozuk |
|---|---|---|
| ton yayilimi (spread) | 30-60° | **< 10° = tek renk filtre** |
| golge tonu vs isik tonu | belirgin fark | **ayni = sicak/soguk ayrimi yok** |
| gok B−R (ust ucte) | pozitif (mavi) | **negatif = gok kirmizi, sepya** |
| deger araligi | > 55 | < 40 = duz |

**`sat%` bir kapi degil.** Tabloda yok cunku gecme sarti degil; sadece bilgi. Solgun
bir palet dusuk sat% verir ve bu **basarisizlik degildir** — spread ve sicaklik ayrimi
tutuyorsa palet saglamdir. Doygunlugu sirf sayi yukselsin diye artirma.

**`WARM-SKY` sahnede gok varsa anlamlidir.** Bayrak karenin ust seridini olcer; magara
ici, yakin plan ve altin saat sahnelerinde ust serit zaten sicaktir. Once "bu karede gok
var mi?" diye sor, sonra bayragi ciddiye al.

Batch icindeki gorseller **arasindaki** ton farkina da bak: 10 farkli konu 15° bandina
sikismissa palet tasarlanmamis, filtrelenmis demektir. Genis ton bandi da tek basina
hedef degil — proje bilincli olarak dar bir palet secmis olabilir; o zaman **kare ici**
spread ve sicaklik ayrimina bak.

Kurtarma: `check_palette.py --grade` split-tone uygular (golgeleri soguga ayirir, cast'i
kaldirir, vibrance ekler). Ama **var olmayan rengi icat edemez** — baştan tek tonda uretilmis
kareyi ancak cilalar. Yapisal olarak bozuk olani yeniden uret.

---

## Teslim formati

- Tek sohbet mesaji, **tek fenced blok**, icinde tam prompt (kullanici bir kez kopyalar)
- Prompt **Ingilizce**; sohbet Turkce
- Blogun disinda numarali dosya adi eslemesi: `1 push, 2 resupply, 3 mobilize, ...`
- Kullaniciya sirayi ve "icerige bakarak esle" notunu hatirlat

---

## Cikti bir prototipe baglanacaksa

Gorseller geldiginde: WebP'ye cevir, veri dosyasina `art` alani olarak bagla, tek-dosya
build'de base64 goml. Harici istek birakma.

```bash
cwebp -q 82 in.png -o out.webp     # ~%80 kucultme, kart boyutunda fark gorunmuyor
```

---

## Calistir

```bash
echo "Konu: ${1:-<belirtilmedi>}"
echo ""
echo "1. Konuyu 10'luk gruplara bol (goruntuleme sikligina gore onceliklendir)"
echo "2. Stil blogunu yaz — Kural 2'deki yasak kelimeleri kullanma"
echo "3. Kadraj dagilimini Kural 3'teki tabloya gore dengele"
echo "4. Tek fenced blok halinde teslim et, dosya eslemesini disinda ver"
echo "5. Cikti gelince: python3 ~/.claude/skills/image-prompt/check_palette.py <dosyalar>"
```
