---
name: image-run
description: "ChatGPT'de gorsel batch'lerini uctan uca uretir: promptu damgalayip gonderir, 1 dk'da bir kontrol eder, biten seriyi toplu indirir, sonrakine gecer. Sohbet adi verilmezse kayitli addan devam eder, o da yoksa kendi yeni sohbetini acar. Triggers: image run, gorsel uret indir, chatgpt batch, sohbette uret, otomatik gorsel, batch calistir, gorselleri indir."
user-invocable: true
argument-hint: "[sohbet adi] — opsiyonel; bos birakilirsa kayitli sohbet ya da yeni sohbet"
---

# /image-run — ChatGPT'de uctan uca gorsel uretimi

Kullanicinin kendi Chrome'unda gorsel batch'lerini uretir ve indirir. Hangi
sohbette calisilacagini **kendisi cozer** — bkz. 0. adim. Prompt yazimi ve palet
dogrulamasi ayri bir skill'in isi:
**[/image-prompt](../image-prompt/SKILL.md)** — once oradaki 10'luk batch formatini
ve sepya/kolaj tuzaklarini oku, prompt metnini oradaki kurallara gore uret. Bu
skill o promptu **calistirir**.

Arac: `mcp__claude-in-chrome__*` (kullanicinin gercek, oturumu acik Chrome'u).
Uygulama ici tarayici (`mcp__Claude_Browser__*`) **kullanilmaz** — ChatGPT'ye
login degil, dosya ucu 401 doner.

---

## Akis

```
sohbeti ac  →  batch N'i gonder  →  1 dk'da bir kontrol
                                            ↓ bitti
                        batch N+1'i HEMEN gonder        (uretim baslar)
                                            ↓
                        batch N'i indir + esle          (N+1 uretilirken)
                                            ↓
                                    N+1 icin kontrole don
```

**Sira onemli: once sonraki promptu gonder, sonra oncekini indir.** Indirme ve
dosya isi 1-2 dakika suruyor; bunu bos beklemek yerine bir sonraki uretimin
altina sakla. Boylece her batch icin indirme suresi sifira iner.

---

## Model ve efor — kotayi burada koru

Bu skill'in isi ikiye ayrilir ve **ayni modelle yapilmaz**:

| is | model / efor | neden |
|---|---|---|
| Prompt yazimi (`/image-prompt`) | **ana model, normal efor — asla low** | Stil blogu, kadraj dagilimi, sepya/kolaj tuzaklari muhakeme isi. Ucuzlatilan prompt tum batch'i cope atar; 10 gorsel yeniden uretmek her tasarrufu geri alir |
| Gonder / bekle / kontrol / indir / esle | **Sonnet 5, `effort: low`** | Mekanik: sabit DOM secicileri, sabit tiklama sirasi. Bu dosyada adim adim yazili, muhakeme gerekmiyor |

Calistirma dongusunu **arka plan `Agent`'ina devret** — tek batch'te bile:

```
Agent(subagent_type: "general-purpose", model: "sonnet", effort: "low",
      run_in_background: true)
```

Prompt metni ajana **hazir** verilir; ajan prompt yazmaz, degistirmez, "iyilestirmez".
Gorevi: sohbeti ac → yapistir → Return → 1 dk'da bir kontrol → indir → dosyalari
esle → rapor. Ana hat bu sirada proje isine devam eder.

**Haiku secme.** Indirme akisi (paylas ikonu → seri secenegi → Indir) yanlis
dugumu tiklamaya musait; bu skill'in gecmisinde kor tiklama bir kez Reddit gonderi
formunu acti. Sonnet low bu adimlari guvenle yuruturken Opus'un maliyetinin
kucuk bir kismini harcar.

**Efor'u yukselt** sadece su iki durumda: kolaj geldi ve promptun neden bozuldugunu
teshis etmek gerekiyor, ya da indirme akisi UI degisikligi yuzunden tutmuyor.
Teshis ana hatta yapilir, duzeltilmis prompt yine low ajana verilir.

---

## 0. Sohbet adini coz — kullaniciya sorma

Sohbet adi **hicbir zaman** bloklayan bir soru degildir. Su sirayla coz:

| oncelik | kaynak | aksiyon |
|---|---|---|
| 1 | Bu calistirmada argüman olarak verildi | Onu kullan **ve kaydet** (asagi) |
| 2 | Kayitli sohbet adi var | Sessizce onu kullan, kullaniciya tek satir bildir |
| 3 | Hicbiri yok | **Kendin yeni bos sohbet ac** ve orada uret |

**Kayit yeri:** `~/.claude/projects/-Users-musabkara/memory/reference_image-run-chat.md`
(`metadata.type: reference`). `MEMORY.md` indeksine tek satir pointer ekle.

```bash
CHAT_MEMO=~/.claude/projects/-Users-musabkara/memory/reference_image-run-chat.md
[ -f "$CHAT_MEMO" ] && grep -m1 '^chat:' "$CHAT_MEMO"
```

Kullanici yeni bir sohbet adi verdiginde bu dosyayi **uzerine yaz** — iki farkli
ad birikirse sonraki calistirma yanlis sohbete yazar. Kullanici "artik su sohbette
uret" derse yeni ad kazanir.

**Onceki adi kullandiginda bunu tek satirla soyle**, sessizce baska sohbete yazma:
`Kayitli sohbette devam ediyorum: "<ad>".`

### 3. durum — kendi sohbetini ac

Kullaniciya "hangi sohbette ureteyim?" diye **sorma.** Yeni sekme ac, `chatgpt.com`
kokune git, dogrudan promptu gonder — ChatGPT ilk mesajdan sonra sohbete kendi
adini verir.

```
navigate → https://chatgpt.com/
composer'a promptu yapistir (bkz. 2. adim) → Return
ilk yanit basladiktan sonra sohbet adini kenar cubugundan oku
```

Ad olustugunda:
1. Kullaniciya bildir: `Yeni sohbet actim: "<ad>" — bundan sonra burada uretecegim.`
2. Adi yukaridaki memo dosyasina yaz ki sonraki calistirma ayni yerde devam etsin.

ChatGPT bazen ada gec karar veriyor; ad henuz gelmediyse batch bitiminde tekrar
oku. Ad okunana kadar uretimi bekletme.

---

## 1. Sohbeti ac

0. adimda cozulen ad icin kenar cubugundan **ada gore** bul ve tikla — URL tahmin
etme, isim tek dogruluk kaynagi:

```js
const name = 'SOHBET ADI';
const el = [...document.querySelectorAll('a, li, div')]
  .find(n => n.textContent.trim().startsWith(name) && n.closest('nav'));
el?.scrollIntoView({block:'center'});
```

Ad kayitliydi ama sohbet listede yoksa (silinmis, arsivlenmis) → 0. adimin 3.
durumuna dus: yeni sohbet ac, memo'yu yeni adla guncelle. **Benzer isimli baska
bir sohbete yazma.**

Ayni sohbette devam etmek surekliligi saglar: stil blogu ayni yerde birikir,
kullanici hangi batch'in nerede uretildigini takip edebilir.

---

## 2. Damgali promptu gonder

Damga kim/ne zaman/hangi batch bilgisini tasir; kullanici kendi elle attigi
promptlarla senin gonderdiklerini ayirt edebilsin, eski batch'ler yanlislikla
tekrar indirilmesin.

**Damga promptun EN SONUNA konur, basina degil.**

```
Generate 10 separate images, one for each numbered subject below.      <- ILK SATIR
IMPORTANT: output each as its OWN separate image file. ...
STYLE (applies to all 10): ...
1. ...
10. ...

[CLAUDE — 2026-08-09 16:50 — <proje>, batch 3/4]                        <- SON SATIR
```

**Neden:** damgayi basa koyunca `Generate 10 separate images` ilk satir olmaktan
cikti ve model tum istegi tek bir konu gibi okuyup **tek birlesik gorsel** uretti
(2026-08-09'da bir batch boyle kayboldu). Ilk satir her zaman "10 ayri gorsel
uret" olmali.

Damgaya **kart/konu id listesi yazma** — model onu tek sahnenin ogeleri sanabiliyor.
Sadece proje adi ve batch numarasi yeter.

Tarihi **calistirma aninda** uret, uydurma.

**Prompt metni Ingilizce olmali** (bkz. `/image-prompt` Kural 0) — damga satiri
disinda her sey. Turkce prompt gorsel kalitesini dusuruyor.

Composer bir `contenteditable` div. `textarea.value` set etmek **calismaz**
(React state guncellenmiyor). Calisan yontem:

```js
const el = document.querySelector('#prompt-textarea') || document.querySelector('div[contenteditable="true"]');
el.focus();
document.execCommand('selectAll', false, null);
document.execCommand('delete', false, null);
const dt = new DataTransfer();
dt.setData('text/plain', PROMPT);
el.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
```

Sonra `computer` ile **Return**. Gonderildigini ekran goruntusuyle dogrula.

---

## 3. Kontrol dongusu

Bekleme icin `Bash` + `run_in_background: true` ile `sleep 60` kullan — bittiginde
bildirim gelir, sen de kontrolu yaparsin. Onplanda `sleep` bloklu.

```js
const stop = [...document.querySelectorAll('button')]
  .some(b => /stop|durdur/i.test((b.getAttribute('aria-label')||'') + (b.getAttribute('data-testid')||'')));
const big = [...document.querySelectorAll('img')]
  .filter(i => /oaiusercontent|sediment|backend-api|files/.test(i.currentSrc||i.src) && i.naturalWidth > 400);
({ stillGenerating: stop, ready: big.length })
```

`stillGenerating` false **ve** `ready` beklenen sayida ise bitmistir. Gorseller
gec decode olabiliyor; sayfayi biraz kaydirip 1-2 sn bekle, sonra tekrar say.

"ChatGPT hata yapabilir" sayfa altyazisidir — hata sanip alarm verme.

### Kolaj kontrolu — gorursen iptal et, bastan baslat

Prompt 10 ayri gorsel istedigi halde **tek birlesik gorsel / izgara / contact
sheet** geldiyse o batch curuktur. Bekleme, duzeltmeye calisma:

1. Uretim suruyorsa **durdur** (stop butonu).
2. Promptu **duzelt** — en sik sebep damganin basta olmasi (bkz. 2. adim); ilk
   satir `Generate N separate images...` olmali.
3. Ayni batch'i **bastan gonder**.

Tespit: bitmis bir yanitta `ready` sayisi beklenenin cok altindaysa (orn. 10
istenip 1-2 geldiyse) ya da tek gorselin en/boy orani seri formatindan sapiyorsa
kolaj uretilmis demektir. Ekran goruntusuyle dogrula, sonra iptal et.

Kolaj gelen batch'i **indirmeye calisma** — bosuna tur yakar ve yanlis dosya
Downloads'a duser, sonraki eslemeyi bozar.

---

## 4. Seriyi indir

**Dogrulanmis tek yol** (10/10 basarili):

```
onizlemenin sag altindaki PAYLAS ikonu
  → "Bu seride yer alan N gorselin tamami"
  → acilan pencerede sag uctaki "Indir"
```

Dosyalar `~/Downloads`'a tam boyutta PNG olarak iner.

**Koordinat yerine DOM'dan tikla.** Onceki batch uretilirken sayfa kayiyor ve
ekran goruntusuyle alinan koordinat tiklama anina kadar geceriz oluyor. Butonlari
metniyle bul ve `.click()` et — kaymadan etkilenmez:

```js
// paylas ikonu (en sonuncusu = en son tamamlanan batch)
const shares = [...document.querySelectorAll('button')]
  .filter(b => /Bu görseli paylaş/i.test(b.getAttribute('aria-label') || ''));
shares[shares.length - 1].click();

// seri secenegi — en az ic ogeye sahip olani gercek menu satiri
const item = [...document.querySelectorAll('[role="menuitem"], button, div')]
  .filter(n => (n.textContent || '').trim() === 'Bu seride yer alan 10 görselin tamamı')
  .sort((a, b) => a.querySelectorAll('*').length - b.querySelectorAll('*').length)[0];
item.click();

// indir
[...document.querySelectorAll('button, a')].find(n => (n.textContent||'').trim() === 'İndir').click();
```

Metin eslesmesinde **en az ic ogeye sahip** dugumu sec — ayni metin hem sarmalayici
kapsayicida hem gercek satirda geciyor, sarmalayiciya tiklamak ise yaramiyor.

**Uc kural:**

1. **Her adimda once ekran goruntusu al, sonra tikla.** Bir dugmeye basip diske
   bakma — arada menu aciliyor. Bu hata bir kez "indirilemiyor" yanlis sonucuna
   goturdu.
2. **Asla kuyruga alinmis kor tiklama yapma.** Pencere acildiktan sonra ayni
   koordinat baska bir butona denk gelebiliyor; bir kez **Reddit** gonderi formu
   acildi (gonderilmedi, kapatildi). Tek `browser_batch` icinde "tikla + ayni
   yere tekrar tikla" dizisi kurma.
3. **"Bu gorsel" degil, seri secenegini sec.** Tek gorsel yolu ayni paylasim
   penceresini aciyor, sadece isi uzatiyor.

Bu akis gorsel(ler) icin **herkese acik bir baglanti uretebiliyor**
(`chatgpt.com/s/m_...`). Is bitince kullaniciya hatirlat: Ayarlar > Veri
kontrolleri > Paylasilan baglantilar'dan silinebilir.

---

## 5. Dosyalari esle

Inen dosya adlari anlamsiz (`ChatGPT Image ... (3).png`). Eslemeyi **mtime
sirasina** gore yap — prompt sirasiyla ortusuyor — ama **icerige bakarak
dogrula**, varsayma:

```bash
# tekilleştir, gecerli olanlari al, kontak sayfasi yap, goz ile kontrol et
```

Yanlis eslesme sessizce yanlis karta yanlis gorsel bagliyor; bir kere gozle bak.

Sonra projeye tasi: WebP'ye cevir (`quality 84, method 6`), hedef dizine
`<id>.webp` olarak yaz, veri dosyasina `art` alani ekle.

---

## 6. Sonraki batch — pipeline

Batch N bittigi anda **once batch N+1'i gonder**, ancak ondan sonra N'i indir.
Uretim arka planda donerken indirme, WebP cevirme ve veri baglama isini yap.

```
N bitti  →  N+1 gonder  →  N'i indir/esle/bagla  →  N+1 kontrol dongusu
```

Tum kuyruk bitene kadar kesintisiz devam et; her batch arasinda kullanicidan
onay bekleme — kuyruk basta bir kez onaylanir.

Her batch kendi damgasini ve kendi stil blogunu tasir — **stil blogunu harfi
harfine ayni kopyala**, tek kelime degistirirsen set ikiye bolunur.

Son batch'te gonderilecek yeni prompt kalmaz; o zaman dogrudan indir.

---

## Paralel calis — ana hat bos kalmasin

Bir batch'in uretimi 2-5 dakika suruyor. **O sure bosa harcanmaz.** Bu skill'in
bekleme adimlari ana konusma hattini asla bloklamaz:

- Bekleme her zaman `Bash` + `run_in_background: true` ile `sleep 60`. Onplanda
  `sleep` yasak; bildirim geldiginde kontrolu yaparsin.
- Zamanlayici calisirken **baska is yap**: inen onceki batch'i WebP'ye cevir,
  veri dosyasina bagla, kod yaz, test kosur, commit at. Bekleme turunda
  "hala uretiyor" deyip durmak israftir.
- Kontrol turlari **sessiz** olmali. Her dakika "kontrol 3/∞, hala calisiyor"
  yazma; sadece durum degistiginde (bitti / hata / indi) konus.
- Tum dongoyu bir arka plan `Agent`'ina devret (Sonnet 5 / `effort: low` — bkz.
  "Model ve efor") ve ana hatta proje isine devam et. Tek batch'te bile boyle;
  bekleme turlarini pahali modelle harcama.
- **Indirmeyi bir sonraki uretimin altina sakla** (bkz. 6. adim). Indirme bos
  beklemede degil, uretim donerken yapilir.

**Uyari:** Chrome MCP tek bir tarayiciyi surer. Arka plandaki bir ajan Chrome'u
kullanirken ana hat da Chrome'a dokunursa tiklamalar birbirine karisir. Ayni anda
**tek taraf** Chrome'u surmeli; diger taraf dosya/kod isi yapmali.

---

## Sinirlar

- Sadece kullanicinin **kendi** sohbetinde calisir. Paylasim linkinde
  (`/share/<id>`) dosya ucu 401 doner, indirilemez.
- ChatGPT tek turda ~10 gorsel uretir; fazlasi tek kolaja birlesir. 10'ar bol.
- Gorsel uretimi kullanicinin ChatGPT kotasini harcar. Uzun kuyruga girmeden
  once kac batch olacagini soyle.

---

## Calistir

```bash
CHAT_MEMO=~/.claude/projects/-Users-musabkara/memory/reference_image-run-chat.md
CHAT="${1:-}"
if [ -z "$CHAT" ] && [ -f "$CHAT_MEMO" ]; then
  CHAT=$(sed -n 's/^chat: *//p' "$CHAT_MEMO" | head -1)
  [ -n "$CHAT" ] && echo "Kayitli sohbet: $CHAT"
fi
if [ -z "$CHAT" ]; then
  echo "Sohbet adi yok — yeni bos sohbet acilacak (chatgpt.com), ad sonra kaydedilecek"
else
  echo "Hedef sohbet: $CHAT"
fi
echo ""
echo "0. Sohbeti coz: argüman > kayitli ad > yeni sohbet ac. Kullaniciya SORMA"
echo "1. /image-prompt kurallariyla batch promptlarini yaz"
echo "2. Sohbeti ac, damgali promptu gonder"
echo "3. sleep 60 (run_in_background) ile 1 dk'da bir kontrol et"
echo "4. Bitince: paylas ikonu > seri > Indir  (her adimda ekrana bak)"
echo "5. Dosyalari icerikle esle, WebP'ye cevir, veri dosyasina bagla"
echo "6. Kalan batch varsa 2'ye don; yeni sohbet acildiysa adini memo'ya yaz"
```
