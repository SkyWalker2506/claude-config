---
name: image-run
description: "ChatGPT'de gorselleri uctan uca uretir: her gorseli kendi mesajinda damgalayip gonderir, 1 dk'da bir kontrol eder, bitince teker teker indirir, sonrakine gecer. Sohbet adi verilmezse kayitli addan devam eder, o da yoksa kendi yeni sohbetini acar. Triggers: image run, gorsel uret indir, chatgpt gorsel, sohbette uret, otomatik gorsel, gorselleri indir, stil arama calistir."
user-invocable: true
argument-hint: "[sohbet adi] — opsiyonel; bos birakilirsa kayitli sohbet ya da yeni sohbet"
---

# /image-run — ChatGPT'de uctan uca gorsel uretimi

Kullanicinin kendi Chrome'unda gorselleri **teker teker** uretir ve indirir. Hangi
sohbette calisilacagini **kendisi cozer** — bkz. 0. adim. Prompt yazimi ve palet
dogrulamasi ayri bir skill'in isi:
**[/image-prompt](../image-prompt/SKILL.md)** — once oradaki "tek mesaj = tek gorsel"
formatini ve sepya/kolaj tuzaklarini oku, prompt metnini oradaki kurallara gore uret.
Bu skill o promptlari **calistirir**.

Arac: `mcp__claude-in-chrome__*` (kullanicinin gercek, oturumu acik Chrome'u).
Uygulama ici tarayici (`mcp__Claude_Browser__*`) **kullanilmaz** — ChatGPT'ye
login degil, dosya ucu 401 doner.

---

## Akis — tek mesaj, tek gorsel, seri

```
sohbeti ac  →  prompt N'i gonder  →  1 dk'da bir kontrol
                                            ↓ bitti
                              gorsel N'i INDIR + dogrula
                                            ↓
                              dosyayi tasi ve adlandir
                                            ↓
                                   prompt N+1'i gonder
```

**Arac tek seferde tek gorsel uretir.** Tek mesajda birden fazla konu istemek ciktiyi
tek birlesik tuvale cevirir — 2026-08-09'da 8 konuluk bir mesaj boyle coktu, ChatGPT'nin
kendisi *"Ilk uretim tek tuvalde birlesti; bunu teslim etmiyorum"* dedi. Prompt yazim
kurali: [/image-prompt](../image-prompt/SKILL.md) Kural 1.

**Indirmeyi bir sonraki gonderimin altina SAKLAMA.** Bu skill'in onceki surumu "once
sonrakini gonder, sonra oncekini indir" diyordu; o kural coklu-uretim icindi ve tek
gorselde **tehlikeli**: yeni gorsel senden once biterse "son paylas dugmesi" ona kayar ve
yanlis dosyayi indirirsin. Kullanicinin talimati da acik — *"birde teker teker indir"*.
Sira **gonder → bekle → indir → dogrula → sonraki**. Daha yavas, ama eslesme kaymiyor.

---

## Model ve efor — kotayi burada koru

Bu skill'in isi ikiye ayrilir ve **ayni modelle yapilmaz**:

| is | model / efor | neden |
|---|---|---|
| Prompt yazimi (`/image-prompt`) | **ana model, normal efor — asla low** | Stil blogu, kadraj dagilimi, sepya/kolaj tuzaklari muhakeme isi. Ucuzlatilan prompt tum turu cope atar; 10 gorsel yeniden uretmek her tasarrufu geri alir |
| Gonder / bekle / kontrol / indir / esle | **Sonnet 5, `effort: low`** | Mekanik: sabit DOM secicileri, sabit tiklama sirasi. Bu dosyada adim adim yazili, muhakeme gerekmiyor |

Calistirma dongusunu **arka plan `Agent`'ina devret** — tek gorselde bile:

```
Agent(subagent_type: "general-purpose", model: "sonnet", effort: "low",
      run_in_background: true)
```

Prompt metni ajana **hazir** verilir; ajan prompt yazmaz, degistirmez, "iyilestirmez".
Gorevi: sohbeti ac → yapistir → Return → 1 dk'da bir kontrol → indir → dosyalari
esle → rapor. Ana hat bu sirada proje isine devam eder.

**Haiku secme.** Composer ve sohbet secimi yanlis dugumu tiklamaya musait; bu skill'in
gecmisinde kor tiklama bir kez Reddit gonderi formunu acti, bir kez de ajan paylas
penceresinde asili kalip watchdog'a dustu. Sonnet low bu adimlari guvenle yuruturken
Opus'un maliyetinin kucuk bir kismini harcar.

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

ChatGPT bazen ada gec karar veriyor; ad henuz gelmediyse ilk gorsel bitiminde tekrar
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
kullanici hangi gorselin nerede uretildigini takip edebilir.

**Ayni projede kal.** Kayitli sohbet yalnizca **ayni proje icinde** varsayilandir; yeni
bir proje **yeni sohbet** acar. Bir kez baska projenin sanat sohbetine prompt gonderildi
ve kullanici durdurdu: *"yanlis yerden indiriyorsun sifirdan ac"*.

---

## 2. Damgali promptu gonder

Damga kim/ne zaman/hangi gorsel bilgisini tasir; kullanici kendi elle attigi
promptlarla senin gonderdiklerini ayirt edebilsin, eski gorseller yanlislikla
tekrar indirilmesin.

**Damga basta durur — ama ikinci satirda.** Kullanici sohbeti actiginda hangi
gorsele baktigini kaydirmadan gormeli; sona konan damga bu isi yapmiyor.

```
Generate one image.                                          <- ILK SATIR
[CLAUDE — 2026-08-09 16:50 — <proje>, stil arama 3/10]        <- DAMGA
<konu, bir-iki cumle>
FRAMING: ...
STYLE: ...
LIGHT: ...
<negatifler>
```

**Birinci satir pazarlik konusu degil.** Damga bir kez gercekten en basa kondu,
uretim talimati ilk satir olmaktan cikti ve model tum istegi tek bir konu gibi okuyup
**tek birlesik gorsel** uretti — 2026-08-09'da bir tur boyle kayboldu. Bu yuzden damga
**ikinci** satira gelir: hem gorunur, hem ilk satiri yerinden etmez.

Damga ile devami arasina **bos satir birakma**; bosluk modelin damgayi ayri bir
istek gibi okumasini kolaylastiriyor.

Damgaya **kart/konu id listesi yazma** — model onu tek sahnenin ogeleri sanabiliyor.
Sadece proje adi ve gorsel numarasi (N/10) yeter.

Tarihi **calistirma aninda** uret, uydurma.

**Prompt metni Ingilizce olmali** (bkz. `/image-prompt` Kural 0) — damga satiri
disinda her sey. Turkce prompt gorsel kalitesini dusuruyor.

Composer bir `contenteditable` div. `textarea.value` set etmek **calismaz**
(React state guncellenmiyor). Once `insertText` dene, tutmazsa `ClipboardEvent`:

```js
const el = document.querySelector('#prompt-textarea') || document.querySelector('div[contenteditable="true"]');
el.focus();
document.execCommand('selectAll', false, null);
document.execCommand('delete', false, null);

// 1. tercih — 2026-08-10'da guvenilir calisan yontem
document.execCommand('insertText', false, PROMPT);

// tutmazsa 2. yol:
// const dt = new DataTransfer(); dt.setData('text/plain', PROMPT);
// el.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
```

**Yapistirmayi her zaman geri okuyarak dogrula.** Ikisi de **asenkron** uygulanabiliyor;
hemen ardindan gonderirsen bos mesaj gider:

```js
await new Promise(r => setTimeout(r, 1000));
el.textContent.length          // prompt uzunlugu ile kabaca ortusmeli
```

Uzunluk sifir ya da kisaysa temizle ve tekrar yapistir. 2026-08-10'da `ClipboardEvent`
bir oturumda `length` 0 birakti ve `insertText` ile cozuldu; ayni gun baska bir ajanda
`ClipboardEvent` calisti ama gecikmeli uygulandi. Ikisi de olabilir — **dogrulama**
pazarlik konusu degil.

Sonra gonder. **Tercihen DOM'dan**, `computer` ile degil — birden fazla sekmede paralel
calisiyorsan `computer` on plandaki sekmeye vurur ve baska bir ajanin isini bozar:

```js
(document.querySelector('[data-testid="send-button"]') ||
 [...document.querySelectorAll('button')].find(x => /send|gönder/i.test(x.getAttribute('aria-label')||''))
).click();
```

---

## 3. Kontrol dongusu

Bekleme icin `Bash` + `run_in_background: true` ile `sleep 60` kullan — bittiginde
bildirim gelir, sen de kontrolu yaparsin. Onplanda `sleep` bloklu.

```js
const turns = [...document.querySelectorAll('[data-testid^="conversation-turn"], article')];
const shots = [];
for (const t of turns) {
  const im = [...t.querySelectorAll('img')]
    .filter(i => /oaiusercontent|sediment|backend-api|files/.test(i.currentSrc || i.src || ''));
  if (im.length) shots.push(im[0]);
}
const stop = [...document.querySelectorAll('button')]
  .some(b => /stop|durdur/i.test((b.getAttribute('aria-label')||'') + (b.getAttribute('data-testid')||'')));
({ stillGenerating: stop, shotCount: shots.length })
```

`stillGenerating` false **ve** `shotCount` bir artmissa bitmistir.

**`naturalWidth`'i hazir olma sinyali olarak KULLANMA.** Sekme on planda degilse Chrome
gorsel cozmeyi erteliyor: gorsel gercekten hazir oldugu halde `naturalWidth` 0 ve
`complete` false kaliyor. Paralel kosuda sekmelerin cogu arka plandadir, yani bu olcut
sonsuza kadar bekletir. Sayim **DOM'daki tur sayisina** dayanir; gercek dogrulama
indirme adimindaki `blob.type` kontroludur.

Sureyi de kucumseme: tek basina 1-2 dk, 10 sekme paralelken **2-5 dk** olcusuldu.
`sleep 60` ile birkac tur beklemeyi normal say.

"ChatGPT hata yapabilir" sayfa altyazisidir — hata sanip alarm verme.

### Kolaj kontrolu — gorursen iptal et, bastan gonder

Tek gorsel istendigi halde **izgara / contact sheet / bolunmus tuval** geldiyse o
gorsel curuktur. Bekleme, duzeltmeye calisma:

1. Uretim suruyorsa **durdur** (stop butonu).
2. Promptu **duzelt** — ilk satir `Generate one image.` olmali, damga ikinci satirda
   (bkz. 2. adim). Promptta birden fazla konu varsa boldur; her mesaj tek konu tasir.
3. Ayni promptu **bastan gonder**.

Tespit: tek gorsel istenmisken cikti birden fazla panele bolunmusse ya da en/boy orani
istenen kadrajdan sapiyorsa kolaj uretilmis demektir. Ekran goruntusuyle dogrula.

Kolaj geleni **indirmeye calisma** — bosuna tur yakar ve yanlis dosya Downloads'a
duser, sonraki eslemeyi bozar.

---

## 4. Gorseli indir — sayfa ici fetch, paylas menusune GIRME

**Dogrulanmis yontem (2026-08-10).** Paylas menusunu hic acma; gorseli sayfanin kendi
oturumuyla indir. Ad da burada verilir, sonradan eslestirme derdi kalmaz:

```js
// Gorselleri KONUSMA SIRASINA gore sec — URL'e gore ayikla DEME (bkz. asagidaki tuzak)
const turns=[...document.querySelectorAll('[data-testid^="conversation-turn"], article')];
const shots=[];
for(const t of turns){
  const im=[...t.querySelectorAll('img')]
    .filter(i=>/oaiusercontent|sediment|backend-api|files/.test(i.currentSrc||i.src) && i.naturalWidth>400);
  if(im.length) shots.push(im[0]);             // her tur en fazla bir uretilmis gorsel
}
const img = shots[shots.length-1];             // en son uretilen
const url = img.currentSrc || img.src;         // currentSrc BOS olabilir — bkz. asagi
const r = await fetch(url);
const b = await r.blob();
let saved = false;
if (b.type.startsWith('image/') && b.size > 400000) {   // KAPI: tip ve boyut
  const a = document.createElement('a');
  a.href = URL.createObjectURL(b);
  a.download = 'wildbound-03.png';             // ADI SEN VER
  document.body.appendChild(a); a.click(); a.remove();
  saved = true;
}
({ok:r.ok, type:b.type, kb:Math.round(b.size/1024), saved, shotCount:shots.length});
```

`saved:true`, makul bir `kb` **ve** `shotCount`'un bir artmis olmasi — ucu birden
olmadan sonraki adima gecme.

### Tuzak: `ok:true` gorseli geldi anlamina GELMEZ

Gorsel henuz lazy-load olmadiysa `img.currentSrc` **bos string**tir. `fetch('')` hata
vermez — sayfanin kendi URL'ine cozulur ve **ChatGPT SPA kabugunu** doner: `ok:true`,
~476 KB, ve diske `.png` adiyla yazilan bir HTML dosyasi. 2026-08-10'da iki dosya boyle
bozuldu ve checksum kontrolu bile yakalayamadi (iki HTML birbirinden farkliydi).

Uc katmanli korunma, ucu de gerekli:

1. `img.currentSrc || img.src` — currentSrc bossa src doludur.
2. `blob.type.startsWith('image/')` — `r.ok`'a **guvenme**, tipe bak.
3. Diske yazdiktan sonra: `file -b --mime-type <dosya>` → `image/png` degilse sil ve
   tekrar indir.

### Yedek: `fetch` engellenirse native indirme

Bazi oturumlarda tarayici araci imzali query string'i tasiyan istegi engelliyor
(`BLOCKED: Cookie/query string data`) ve `fetch` hic calismiyor. O zaman istegi JS'e
okutma, tarayiciya yaptir:

```js
const a = document.createElement('a');
a.href = img.currentSrc || img.src;
a.download = '';                                // cross-origin'de ad yok sayilir
document.body.appendChild(a); a.click(); a.remove();
```

Dosya `~/Downloads`'a **UUID benzeri kendi adiyla** iner (cross-origin istek `download`
adini yok sayar), sonra `mv` ile dogru ada tasinir. Bu yolda tip dogrulamasi yalnizca
diskte yapilabilir — `file -b --mime-type` adimi burada zorunludur.

### Tuzak: URL'e gore tekillestirme calismaz

Ilk surumde gorseller `src.split('?')[0]` ile tekillestiriliyordu. **Bu sessizce
coker:** ChatGPT'nin gorsel URL'leri **ayni yolu paylasir, yalnizca query string'de
ayrisir**, ustelik tarayici araci query string'i okumayi engelliyor (`[BLOCKED:
Cookie/query string data]`). Sonuc: butun gorseller tek bir kayda dusuyor ve her
indirme **ayni ilk gorseli** getiriyor. 2026-08-10'da 3. ve 4. stil boyle indi;
yalnizca checksum karsilastirmasi yakaladi.

Bu yuzden secim **DOM sirasina** dayanir, URL'e degil.

**Her indirmeden sonra checksum dogrula** — dosya adinin dogru olmasi icerigin dogru
oldugunu gostermez:

```bash
shasum ~/Projects/<proje>/art/*.png | awk '{print $1}' | sort | uniq -d
```

Cikti bossa hepsi farklidir. Tekrar eden hash varsa ayni gorsel iki kez inmistir.

**Neden paylas menusu degil:** o menude **Indir dugmesinin hemen yaninda Reddit var**
(sirasi: Baglantiyi kopyala · X · LinkedIn · Reddit · Indir). Bir kor tiklama bir kez
Reddit gonderi formunu acti, bir kez de ajan menude asili kalip watchdog'a dustu. Ayrica
o akis herkese acik bir paylasim baglantisi uretebiliyor. Sayfa ici fetch hicbirine
dokunmaz.

**Bir onceki gorseli indirmek gerekiyorsa** `uniq[uniq.length-1]` yerine indeksi degistir;
`uniq` dizisi sohbetteki sirayla gelir.

Menu yine de acildiysa (yanlis tiklama) **Escape** ya da sag ustteki X ile kapat —
composer o pencere acikken yaziyi almaz.

Onceki surumdeki "Bu seride yer alan N gorselin tamami" secenegi coklu-uretim akisindan
kalmadir; **kullanma**.

**Koordinat yerine DOM'dan tikla.** Sayfa uretim sirasinda kayiyor ve
ekran goruntusuyle alinan koordinat tiklama anina kadar geceriz oluyor. Butonlari
metniyle bul ve `.click()` et — kaymadan etkilenmez:

```js
// paylas ikonu (en sonuncusu = en son tamamlanan gorsel)
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

Inen dosya adlari anlamsiz (`ChatGPT Image ... (3).png`).

**Zaman penceresiyle dosya secme.** `son N dakikada inenler` veya `[-10:]` gibi
secimler kirilgan: baska bir uygulama ayni klasore dosya birakabilir, onceki
onceki gorselin kuyrugu pencereye girebilir. Bir kez **tam bir pozisyon kaymasina** yol
acti — infantry dusup yerine alakasiz bir grafik girdi, 10 kartin hepsi bir sira
kaydi ve build yesil kaldigi icin sessizce yanlis baglandi.

**Indirmeden once seri sayisinin ARTTIGINI dogrula.** Paylas dugmelerini
(`Bu görseli paylaş`) say; bu sayi her tamamlanmis gorsel serisi icin bir artar.
Indirmeye baslamadan onceki sayiyi hatirla:

```js
const groups = [...document.querySelectorAll('button')]
  .filter(b => /Bu görseli paylaş/i.test(b.getAttribute('aria-label') || '')).length;
```

`groups` bir artmadiysa **yeni gorsel daha bitmemistir**; `shares[son]` hala bir
onceki seriyi gosterir ve indirirsen **ayni gorselleri ikinci kez indirirsin**.
Bu bir kez oldu: 10 dosya indi, hepsi bir onceki turun birebir kopyasiydi.
Bekle, tekrar kontrol et.

**Dogru yontem: indirmeden ONCE klasorun anlik goruntusunu al, sonra farki al.**

```bash
before=$(ls ~/Downloads)                       # indirmeden once
# ... seri indirmesini yap ...
comm -13 <(echo "$before" | sort) <(ls ~/Downloads | sort)   # sadece yeni gelenler
```

Yeni dosya sayisi beklenenden **fazlaysa dur** — arada yabanci dosya var, gozle
ayikla. Eksikse indirme tamamlanmamis, bekle.

Eslemeyi mtime sirasina gore yap (prompt sirasiyla ortusuyor) ve **her zaman
icerige bakarak dogrula**:

```bash
# tekilleştir, gecerli olanlari al, kontak sayfasi yap, goz ile kontrol et
```

Yanlis eslesme sessizce yanlis karta yanlis gorsel bagliyor ve **build yesil
kalir** — hicbir test bunu yakalamaz. Baglamadan once kart adiyla etiketlenmis
bir kontak sayfasi uret ve gozle gec:

```python
# her karenin altina kart adini yaz, tek sayfada goster
ImageDraw.Draw(lab).text((4, h+4), names[card_id], fill=(210,205,185))
```

Sonra projeye tasi: WebP'ye cevir (`cwebp -q 82` — tum hatlarin ortak ayari;
olculmus: ~%80 kucultme, kart boyutunda fark gorunmuyor), hedef dizine
`<id>.webp` olarak yaz, veri dosyasina `art` alani ekle.

---

## 6. Sonraki gorsel

```
N bitti  →  N'i indir + dogrula + tasi/adlandir  →  N+1'i gonder
```

Indirmeyi bir sonrakinin altina **saklama** (sebep: "Akis"). Dosya diskte dogrulanmadan
yeni prompt gonderme — dogrulanmamis bir indirme, sonraki eslemenin tamamini kaydirir.

Tum kuyruk bitene kadar kesintisiz devam et; gorseller arasinda kullanicidan onay
bekleme — kuyruk basta bir kez onaylanir.

Her prompt kendi damgasini ve kendi stil blogunu tasir — **stil blogunu harfi harfine
ayni kopyala**, tek kelime degistirirsen set ikiye bolunur.

---

## Paralel calis — ana hat bos kalmasin

Bir gorselin uretimi 1-2 dakika suruyor. **O sure bosa harcanmaz.** Bu skill'in
bekleme adimlari ana konusma hattini asla bloklamaz:

- Bekleme her zaman `Bash` + `run_in_background: true` ile `sleep 60`. Onplanda
  `sleep` yasak; bildirim geldiginde kontrolu yaparsin.
- Zamanlayici calisirken **baska is yap**: inmis gorselleri WebP'ye cevir,
  veri dosyasina bagla, kod yaz, test kosur, commit at. Bekleme turunda
  "hala uretiyor" deyip durmak israftir.
- Kontrol turlari **sessiz** olmali. Her dakika "kontrol 3/∞, hala calisiyor"
  yazma; sadece durum degistiginde (bitti / hata / indi) konus.
- Tum dongoyu bir arka plan `Agent`'ina devret (Sonnet 5 / `effort: low` — bkz.
  "Model ve efor") ve ana hatta proje isine devam et. Tek gorselde bile boyle;
  bekleme turlarini pahali modelle harcama.

**Uyari:** Chrome MCP tek bir tarayiciyi surer. Arka plandaki bir ajan Chrome'u
kullanirken ana hat da Chrome'a dokunursa tiklamalar birbirine karisir. Ayni anda
**tek taraf** Chrome'u surmeli; diger taraf dosya/kod isi yapmali.

---

## Sinirlar

- Sadece kullanicinin **kendi** sohbetinde calisir. Paylasim linkinde
  (`/share/<id>`) dosya ucu 401 doner, indirilemez.
- **ChatGPT tek mesajda tek gorsel uretir.** Tek mesajda birden fazla konu istemek
  ciktiyi tek kolaja birlestirir — olculmus, iki kez. 10 gorsel = 10 mesaj.
- Bu, bir turu uzatir: gorsel basina ~1-2 dk uretim + ~1 dk indirme, yani 10'luk bir
  tur ~20-30 dk. Arka plan ajaniyla kosuldugunda ana hat bloklanmaz.

### Paralellik — sekme sayisinda, mesaj icinde degil

Mesaj icine ikinci konu koyarak hizlanamazsin (kolaj). Hizlanmanin tek yolu **ayri
sekmelerde ayri sohbetler**: her sekmeye bir ajan, her ajan kendi kuyrugunu seri isler.

Kurallar:

- Ajanlara **tabId ver** ve "yalnizca kendi sekmene dokun" de.
- **`computer` araci ve ekran goruntusu yasak.** Ikisi de on plandaki sekmeye bakar;
  paralelde bu, baska bir ajanin sayfasina tiklamak demektir. Her sey `javascript_tool`
  + `tabId` ile yapilir, dogrulama DOM'dan ve diskten.
- Es zamanli uretim ChatGPT'yi yavaslatir: tek basina ~1-2 dk olan uretim, 10 paralel
  sekmede **2-3,5 dk**'ya cikti (olculmus). Yine de toplam sure ciddi olcude kisalir.
- **6-8 sekmeden fazlasina cikma.** 2026-08-10'da 10 es zamanli ajanla kosuldu ve ucu
  API akis hatasiyla (`response stalled mid-stream`, `connection closed`) dustu. Olen
  ajanin isi diskte yarim kalir; bu yuzden her ajan **once diske bakip eksikleri**
  uretmeli, sonda da bir **bosluk doldurma turu** planlanmali.
- Gorsel uretimi kullanicinin ChatGPT kotasini harcar. Uzun kuyruga girmeden
  once kac gorsel olacagini soyle.

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
echo "1. /image-prompt kurallariyla promptlari yaz (tek mesaj = tek gorsel)"
echo "2. Sohbeti ac, damgali promptu gonder"
echo "3. sleep 60 (run_in_background) ile 1 dk'da bir kontrol et"
echo "4. Bitince: sayfa ici fetch + a.download ile indir (paylas menusune GIRME)"
echo "5. Dosyayi dogrula, tasi/adlandir, WebP'ye cevir, veri dosyasina bagla"
echo "6. Kalan prompt varsa 2'ye don; yeni sohbet acildiysa adini memo'ya yaz"
```
