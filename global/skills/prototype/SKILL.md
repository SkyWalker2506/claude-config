---
name: prototype
description: "Bir GDD'yi Three.js + Web Audio ile oynanabilir, juicy bir prototipe cevirir. TEK ajan, dalga yok, test yok. Oyunun eglenceli olup olmadigini kanitlar, oyunu bitirmez. Triggers: prototype, prototip uret, gdd den prototip, hizli prototip, playable prototype, three.js prototip, oyun prototipi."
user-invocable: true
argument-hint: "[GDD dosya yolu veya oyun fikri]"
---

# /prototype — fikrin ise yaradiginin kaniti

Oyun yapmiyorsun. **Oyun fikrinin ise yaradiginin kanitini** yapiyorsun.

> Hiz > Mimari · His > Icerik · Oynanir > Mukemmel

**Hedef:** tarayiciyi ac -> tikla -> **saniyeler icinde oyna.** Yukleme ekrani, giris akisi,
menu labirenti yok.

## Tek ajan kurali — olculmus, tercih degil

**Isi bolme. Sen yaz.** Ayni GDD, iki kosu:

| | tek akis | 19 pakete bolunmus, 14 ajan |
|---|---:|---:|
| Sure | **18 dk** | 5 sa 6 dk |
| `src/` satir | 2.588 | 19.801 (7,7x) |
| Icerik | 7 gun · 10 kart · 5 kaynak · 3 tren | **birebir ayni** |
| Paralellik kazanci | — | **1,04x** |

Paralellik zinciri kisaltmaz. Her paket bir oncekinin arayuzunu **kesfetmeyi** bekledi; iki paket
ayni nesne icin iki sema uydurdu ve ~50 dakika gitti. Prototipte koordinasyon maliyeti,
paralellik kazancindan buyuktur.

**Mikro ajan yalnizca su ucu icin, ve yalnizca prototip KOSTUKTAN sonra:**
sanat prompt'u uretme · hata ayiklama · optimizasyon. Temel kodlama, ses, UI, asset icin
**asla ajan bekleme**.

## Butce

| Faz | Sure | Cikti |
|---|---:|---|
| 1 · GDD analizi | 3 dk | cekirdek dongu + kesikler |
| 2 · Iskelet | 5 dk | `index.html`, `data/config.js`, bos sahne, kamera |
| 3 · Cekirdek dongu | 12 dk | oyuncu eylemi -> geri bildirim -> odul |
| 4 · Juice + ses | 6 dk | partikul, shake, punch, procedural ses |
| 5 · Bak ve tek gecis | 4 dk | ekran goruntusu, **en yuksek etkili tek** duzeltme |

**30 dakikayi asan sey kapsam olmali, sure degil.** Tasan kismi "eksikler" diye yaz ve teslim et.

---

## Faz 1 — GDD analizi (3 dk)

Kod yazmadan once **cekirdek donguyu** cikar:

```
oyuncu eylemi -> geri bildirim -> odul -> ilerleme -> tekrar
```

Ve dort soruyu cevapla: ana oyuncu eylemi ne · kazanma sarti ne · kaybetme sarti ne ·
**hangi anlar gorsel geri bildirim istiyor**.

Sonra `SCOPE.md` — 10 satir:

- **Olmali:** cekirdek mekanik, oyuncu etkilesimi, minimum UI, kazan/kaybet, geri bildirim efektleri
- **Olsa iyi:** ikincil sistemler, ekstra icerik
- **Yok:** save, tutorial, ayarlar, erisilebilirlik, coklu oyuncu, ECS, backend

**Ilk prototip 1-3 dakikalik oynanis.** GDD 7 gun istiyorsa 2 gun yap; 10 kart istiyorsa 4 kart.
GDD'nin "kabul kriterleri" bolumu varsa o **urun hattinindir**, seni baglamaz.

## Faz 2 — Iskelet (5 dk)

```
index.html          tek giris, import map ile three
src/main.js         boot + dongu
src/Game.js         game.state = { score:0, day:1, coins:0 }   <- duz nesne
src/systems/…       Effects.js, Audio.js, Input.js
src/entities/…      oyuna ozgu olanlar
data/config.js      TUM ayarlanabilir sayilar, tek dosya
```

**Basit tut.** Redux benzeri sistem yok, dependency injection yok, her yere EventBus yok.
Kalitim yerine kompozisyon: `entity.addComponent(new Health())`.

**`data/config.js` bastan doldur, gercek degerlerle.** Sayilar koda gomulurse her ayar bir
kod degisikligi olur ve iterasyon durur.

**Bir sozlesme sart:** `game.advance(seconds)` — simulasyonu **gercek zaman beklemeden**
sabit adimlarla ilerletir. Bunsuz 7 gunluk bir kampanyayi test etmek 35 dakika surer; bununla
saniyenin altinda. Olculmus.

### three.js: vendor mi CDN mi

Cevrimdisi calismasi ya da tek dosya paylasilmasi gerekiyorsa **vendor'la**
(`vendor/three.module.js`, import map). Yoksa CDN daha hizli. **Bunu bastan sor ya da karar
verip yaz** — sonradan degistirmek dagitim adimini yeniden yazmak demek.

### Kamera tipi — bastan sec, sonra degistirme
3D aksiyon/platform -> `PerspectiveCamera`. Strateji, izometrik, cozy -> `OrthographicCamera`.
Zoom, yumusak hareket ve shake **her ikisinde de** olmali. **Kamera eylemi anlatir**, sadece
gostermez.

### Girdi — `InputManager` soyutlamasi
Oynanis kodu **asla** DOM olayina dogrudan baglanmaz:

```js
input.isPressed('ACTION')   //  klavye, mouse ya da touch — cagiran bilmez
input.position()            //  ekran ya da dunya konumu
```

Masaustunde mouse+klavye, mobilde touch. Bu soyutlama olmadan mobil destegi eklemek her
oynanis dosyasina dokunmak demektir.

## Faz 3 — Cekirdek dongu (12 dk)

Sirasiyla: oyuncu bir sey yapabiliyor -> dunya tepki veriyor -> odul goruluyor -> tekrar
edilebiliyor. **Her adim calisir halde birak.** Yarim sistem, hic olmayan sistemden pahalidir.

**Asset onceligi:** procedural geometri > uretilmis basit texture > placeholder > gercek asset.
Agac = silindir govde + kure yaprak + partikul. Ev = kutu + egik cati. **Once oynanisi dogrula**,
sanat sonra gelir ve prototipin sorusunu degistirmez.

## Faz 4 — Juice + ses (6 dk) — bu faz atlanamaz

**Her onemli eylem gorsel VE isitsel karsilik alir.** Bu prototipin varlik sebebi: fikrin
eglenceli olup olmadigi hissten anlasilir.

| Katman | Zorunlu |
|---|---|
| Hareket | smooth interpolation, ease, kamera takibinde yumusama |
| Etki | scale punch (1.2x), kucuk rotasyon shake, partikul burst, ses |
| Kamera | zoom, yumusak hareket, **shake tek kanaldan** (`camera.setShakeOffset(x,y)`) |
| Girdi | mouse + klavye + **touch**; oynanis DOM olayina baglanmaz |
| Partikul | hit (kucuk, rastgele hiz, fade) · collect (yukari, altin his) · level up (halka + shake) |

Partikuller **havuzlanir**, tek tek olusturulup yok edilmez. Tavan koy (300 iyi bir sayi).
Harici partikul kutuphanesi yok.

**Ses — Web Audio API, harici dosya yok.** `AudioManager`: oscillator + frequency sweep +
gain fade. Collect = yukselen sweep. Hit = noise burst + dusuk frekans. Hata = alcalan
sawtooth. Basari = uc notali arpeggio. **Pitch varyasyonu ekle**, ayni ses ust uste calinca
yorucu olur. AudioContext'i **ilk kullanici etkilesiminde** resume et.

> Juice oyuna ozgu degildir. Bir onceki prototipten `Effects.js` ve `AudioManager.js`
> kopyalanabiliyorsa **kopyala**. Olculmus: kodun %32'si oyundan bagimsizdi.

## Faz 5 — Bak ve tek gecis (4 dk)

**Ekran goruntusu al ve KENDIN BAK.** Rapor gorsel kanit degildir.

Sonra **iki sayiyi olc**, goz karariyla karar verme:

1. **Okunabilirlik.** Oyuncunun ayirt etmesi gereken sey (birim, bina, kart) varsayilan
   kamerada viewport genisliginin **>= %6'si** olmali. Olcum: mesh'in kose noktalarini
   kameraya projekte et, ekran genisligini piksel olarak al.
   *Neden kural:* bir kosuda "olcek yanlis, kasabalar nokta gibi" diye teshis koydum;
   olcunce 1280 px'de **129 piksel (%10)** cikti — teshis yanlisti ve bir ajani dunyayi
   yeniden olceklemeye gonderecektim. **"Yanlis gorunuyor" olculmeden teshis degildir.**
2. **Bosluk.** Varsayilan kameranin gosterdigi her "yer"de bir sey olmali. Olculmus hata:
   5 ada uretip 3 yerlesim koymak — iki ada bombos kaldi ve ekran bos gorundu.
   Kural: **yer sayisi <= icerik sayisi.**

Sonra dort soruyu sor ve **yalnizca en yuksek etkili olani** duzelt:

- Cekirdek dongu 10 saniyede anlasiliyor mu?
- Geri bildirim tatmin edici mi?
- Tekrar etmek icin sebep var mi?
- En buyuk eksik eglence unsuru ne?

**En fazla 3 duzeltme. Yuzey detayina dokunma** — sis, dalga, cok katmanli kiyi, gun ici isik
tonu. Olculmus: bunlara 25 dakika harcadim ve ekran goruntusunde hicbiri oyunu daha oynanir
yapmadi. Ayirt edici soru: *bu efekt oyuncunun bir seyi ANLAMASINA yardim ediyor mu, yoksa
sadece guzel mi?* Teslimat yayi anlatiyor; sis anlatmiyor.

---

## Yapma — her biri olculmus bir maliyet

| Yapma | Maliyet |
|---|---|
| Isi 19 pakete bolmek, 8 dalga | 1,04x hizlanma, 5 saat |
| Kabul kriteri suiti + tarayici surucu kapilar | ~5.000 satir; kirmizilarin yarisi kapinin kendi hatasiydi |
| Pakete mutasyon testi yazdirmak | ~60 dk |
| `effort: high` | 24-38 dk/paket; `medium` 7-19 dk |
| Ajanlarin kendi fixture'ini uydurmasi | iki sema, ~50 dk |
| Save/tutorial/ayarlar/erisilebilirlik | GDD istese bile prototip disi |
| Determinizm/digest kaniti | GDD'nin tasarim sorusu bu degilse gereksiz |
| Ekran goruntusune bakmadan "polish yapildi" demek | kompozisyon hatasi sona kadar tasinir |

**Test yazma.** Tek istisna: prototip kostuktan sonra, 40 satirlik bir duman kontrolu —
sifir console error, canvas var, bir frame render edildi, 60 saniye ilerlet ve oyun ilerliyor.

## Teslim

1. Calisan build + tek satirlik calistirma komutu
2. `README.md`: nasil calistirilir · kontroller · cekirdek oynanis · **yapilanlar** ·
   **yapilmayanlar** · sonraki iterasyon fikirleri
3. Bir ekran goruntusu
4. Iki olcum: okunabilirlik yuzdesi ve "her yerde bir sey var mi"

Kullanici daha fazlasini isterse **o zaman** urun hattina gec (`plan-build`). Prototip,
"bu fikir eglenceli mi" sorusunu cevapladiginda isini bitirmistir.
