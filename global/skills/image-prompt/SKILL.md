---
name: image-prompt
description: "Gorsel uretim promptlarini dogrulanmis formatta yazar: tek mesaj = tek gorsel, bir tur 10 ayri prompt. Cikan paleti olcerek dogrular; sepya-yikama ve kolaj tuzaklarini prompt seviyesinde onler. Triggers: image prompt, gorsel prompt, resim promptu, asset prompt, kart gorseli, art prompt, 10 resim, stil arama."
user-invocable: true
argument-hint: "[konu/proje] — orn. 'kart gorselleri' veya 'ikon seti'"
---

# /image-prompt — Image Prompt Generator

Illustration, key art, ikon ve prop promptlarini **tek mesaj = tek gorsel** formatinda
yazar; bir tur tipik olarak 10 ayri prompttur. Uretim sonrasi paleti olcup dogrular.

**Promptu yazdirmakla kalmayip uretimi de calistirmak istiyorsan:**
`/image-run <sohbet adi>` — adi verilen ChatGPT sohbetinde promptu gonderir,
1 dk'da bir kontrol eder, biten gorseli indirir, sonrakine gecer.
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

## Kural 1 — Tek mesaj, TEK gorsel

**Bu kural bir kez tersine cevrildi. Eski hali "tek istekte 10 sahne" diyordu; olcum
onu curuttu.** 2026-08-09'da tek mesajda 8 konu istendi ve cikti **tek birlesik tuval**
oldu — ChatGPT'nin kendisi *"Ilk uretim tek tuvalde birlesti; bunu teslim etmiyorum"*
deyip bastan uretmeye basladi. Kullanicinin talimati net: *"birde teker teker indir"*.
2026-08-10'da ayni sey tekrar dogrulandi: **arac tek seferde tek gorsel uretiyor.**

Dogru format — **her gorsel kendi mesajinda, kendi basina calisan tam bir prompt**:

```
Generate one image.
[CLAUDE — <tarih> — <proje>, <tur adi> N/10]
<konu, bir-iki cumle>
FRAMING: <kadraj notu>
STYLE: <stil blogu — bu promptta TAM haliyle tekrar eder>
LIGHT: <isik dili>
<negatifler>
```

**Ortak stil basligi YOK.** Onceki surumun "STYLE (applies to all 10)" blogu, ancak tek
mesajda 10 gorsel isterken anlamliydi. Artik her prompt tek basina gonderildigi icin stil
blogu **her promptta harfi harfine tekrar eder**. Tek kelime degistirirsen set ikiye
bolunur — tekrar bir israf degil, tutarliligin tek mekanizmasidir.

**Damga yine ikinci satirda.** Ilk satir uretim talimati olmali; damgayi en basa koymak
bir kez modelin tum istegi tek konu gibi okumasina yol acti. Damgaya konu/id listesi
yazma.

**"10" hala gecerli ama artik tur demek, batch degil.** Bir turda 10 gorsel istemek
dogru olcek; ama bu **10 ayri mesaj** demek, tek mesajda 10 konu degil. 10'dan fazlasi
icin turu ikiye bol.

**Her gorseli gonderdikten sonra, sonrakini gondermeden ONCE indir.** Toplu "seri indir"
akisina guvenme — indirmeyi bekletmek dosyalari birbirine karistiriyor ve bir kez tam
bir pozisyon kaymasina yol acti.

Yine de kolaj/izgara gelirse tek satir duzeltme:
`Please output this as a single standalone image. No grid, no contact sheet, no collage.`

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
3. Ayni paleti turun tumune tasi (stil blogu her promptta harfi harfine ayni), ama **sahnelerin
   kendi tonu olsun** — magara sicak, nehir soguk. Toplam ton bandini kendin dengele.

Doygunlugu "canli" diye yukseltme; ton *ayrimi* aradigin sey, sat% degil.

---

## Kural 3 — Tek yone asiri duzeltme yapma

Palet duzeltmesi isterken "olabildigince mavi" dedigimizde model **her kareyi gokyuzune**
cevirdi. Bir sonraki tur "abartma" geldi.

Ayni tuzak doygunlukta da var: sepyayi kovalarken "vivid saturated" yazip her kareyi
ciglastirmak da tek yone asiri duzeltmedir ve o da AI ciktisi gibi durur. Kural 2'deki
palet bolumu bunun icin var.

**Cozum:** kadraji sahne bazinda acikca yaz, dagilimi kendin dengele. 10'luk bir tur icin
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

Turun gorselleri **arasindaki** ton farkina da bak: 10 farkli konu 15° bandina
sikismissa palet tasarlanmamis, filtrelenmis demektir. Genis ton bandi da tek basina
hedef degil — proje bilincli olarak dar bir palet secmis olabilir; o zaman **kare ici**
spread ve sicaklik ayrimina bak.

Kurtarma: `check_palette.py --grade` split-tone uygular (golgeleri soguga ayirir, cast'i
kaldirir, vibrance ekler). Ama **var olmayan rengi icat edemez** — baştan tek tonda uretilmis
kareyi ancak cilalar. Yapisal olarak bozuk olani yeniden uret.

---

## Teslim formati

- Her gorsel icin **ayri fenced blok**, icinde o gorselin tam ve kendi basina calisan promptu
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
echo "1. Konuyu 10'luk turlara bol (goruntuleme sikligina gore onceliklendir)"
echo "2. Stil blogunu yaz — Kural 2'deki yasak kelimeleri kullanma"
echo "3. Kadraj dagilimini Kural 3'teki tabloya gore dengele"
echo "4. Tek fenced blok halinde teslim et, dosya eslemesini disinda ver"
echo "5. Cikti gelince: python3 ~/.claude/skills/image-prompt/check_palette.py <dosyalar>"
```
