---
name: prototype
description: "Bir GDD'den 30 dakikada oynanabilir prototip. Iskelet once donar, sonra tek dalgada paralel doldurulur. Test yok, mutasyon yok, cok dalga yok. Triggers: prototype, prototip uret, gdd den prototip, hizli prototip, 30 dakikada prototip, playable prototype."
user-invocable: true
argument-hint: "[GDD dosya yolu veya hedef tanimi]"
---

# /prototype — 30 dakikada oynanabilir

Bu skill **tek bir sayiyi** hedefler: fikirden oynanabilir builde **30 dakika**. Kalite hedefi
"dogru" degil, **"oynanir ve tasarim sorusunu cevaplar"**.

Olculmus gerekce: ayni GDD'den bir referans model 18 dakikada 2.588 satirla calisan bir
prototip cikardi. Ayni GDD'yi 19 pakete bolup 14 ajanla kosturmak 5 saat 6 dakika ve 19.801
satir surdu — **7,7 kat kod, ayni icerik** (7 gun, 10 kart, 5 kaynak, 3 tren, ikisinde de).
Paralellik **1,04x** hizlandirdi. Bu skill o farkin nedenlerini kapatir.

## Bütçe — pazarlik degil, kisit

| Faz | Sure | Kim | Paralel mi |
|---|---:|---|---|
| 0 · Kapsam sozlesmesi | 2 dk | sen | hayir — karar tektir |
| 1 · Iskelet | 5 dk | 1 Fable **+** sen, ayni anda | **evet, iki kol** |
| 2 · Doldurma dalgasi | 15 dk | 4-6 Opus | **evet, tek dalga** |
| 3 · Kablola + duman + bak | 4 dk | sen | hayir — duman Faz 2'de yazildi |
| 4 · Kompozisyon gecisi | 2 dk | sen | hayir — goz tektir |

### Nerede paralellestirilir, nerede paralellestirilmez

**Paralellestir:** birbirinin **ciktisini beklemeyen** isler. Faz 1'in iki kolu (veri+sozlesme
ile kabuk+duman) ayni GDD'yi okur ama birbirini okumaz. Faz 2'nin dilimleri iskelet dondugu
icin birbirini beklemez.

**Paralellestirme:** kapsam karari (tek karar), iskelet dogrulamasi (20 satir, delege etmek
yazmaktan uzun surer), kablolama (tek dosya), ekran goruntusu degerlendirmesi (tek goz).
Olculmus: recon'u delege etmek plani tahmine dayandirir.

**Dilimleri boyuta gore dengele, konuya gore degil.** Dalga bitis suresi **en yavas dilimin**
suresidir. Olculmus: uc ajanli bir dalgada en yavasi 48 dk, digerleri 13 ve 19 dk surdu —
**26 dakika bos bekleme.** Bir dilim digerlerinin iki kati gorunuyorsa ikiye bol; alti kucuk
dilim, dort dengesiz dilimden hizlidir.

**Saat 30'u gecerse duran sey kapsamdir, sure degil.** Fazla kalani "bilinen eksikler" diye
yaz ve teslim et. Yarim biten bir sistem, hic baslamamis bir sistemden pahalidir.

---

## Faz 0 — Kapsam sozlesmesi (3 dk)

GDD'yi oku ve **uc soruyu cevapla**, kullaniciya sorma:

1. **Bu prototip hangi tek tasarim sorusunu cevapliyor?** (or. "ray dosemek tatmin edici mi")
   Cevaplamayan her sistem kesilir.
2. **Kesilenler ne?** Acikca listele. Tipik kesikler: tutorial, save/load, ayarlar paneli,
   erisilebilirlik, ses, 7 gunun 7'si (2 gun yeter), 10 kartin 10'u (4 yeter).
3. **Neyi kesmiyorsun?** Cekirdek dongu + onu okunur kilan minimum UI.

Bunu 10 satirlik bir `SCOPE.md` olarak yaz. **Kesilenler yaziliysa eksik degil, karardir.**

> GDD "kabul kriterleri" bolumu tasiyorsa: o bolum **urun hattinindir, prototipin degil.**
> Prototip icin tek kriter Faz 3'teki duman kontrolu.

## Faz 1 — Iskelet dondurma (5 dk, **iki kol paralel**) — bu skill'in tek gercek fikri

**Paralellik zinciri kisaltmaz; zinciri once yok etmelisin.** Ajanlar birbirinin arayuzunu
kesfetmeyi beklerse dalgalar seri olur. O yuzden **hicbir ajan baslamadan** sen sunlari yazarsin:

1. **`data/*.json` — tamami, gercek degerlerle.** Kucuktur (referans olcum: 94 satir). Boylece
   her ajan **gercek veriye** kod yazar, fixture uydurmaz. Sema catismasi diye bir sey kalmaz.
2. **`index.html` + `src/main.js`** — tum `install*()` cagrilari **bugunden** yazili, henuz
   olmayan modulleri import eden satirlar dahil. Ajan bitirdiginde kablolama zaten orada.
3. **`CONTRACT.md` — bir sayfa.** Her dosyanin: yolu, export ettigi `install(game, opts)`
   imzasi, okuyacagi nesnelerin **alan adlari**, yayinlayacagi olay adlari.

Bu adimi atlarsan skill calismaz. Olculmus: sema catismasi tek basina ~50 dakika ve bir
paketin bastan kosulmasi demekti. Ornek JSON'u olan tipte (`resource`) hic catisma cikmadi,
olmayan iki tipte (`production-site`, `settlement`) ikisinde de cikti.

### Iki kol, ayni anda

| Kol A — 1 Fable ajani (`effort: medium`) | Kol B — sen |
|---|---|
| `data/*.json` tamami, gercek dengelenmis degerlerle | `index.html` + `src/main.js` (tum `install*()` cagrilari bugunden yazili) |
| `docs/CONTRACT.md` — dosya yollari, `install` imzalari, alan adlari, olay adlari | `tools/smoke.mjs` — Faz 3'te kosacak duman kontrolu |

Ikisi ayni GDD'yi okur, birbirini okumaz. Kol B'nin `main.js`'i henuz var olmayan modulleri
import eder; bu kasitli — ajan bitirdiginde kablolama zaten yerindedir.

Kol A donunce **sen dogrularsin**, delege etme (20 satir, delege etmek yazmaktan uzun surer):
her dosyanin tek sahibi var mi, her `install` imzasi `CONTRACT.md`'de var mi, `data/*.json`
gercek degerlerle mi dolu, `main.js`'in import ettigi her modul `owns` listelerinden birinde mi.

## Faz 2 — Tek paralel dalga (15 dk)

**Tek dalga. Ikinci dalga yok.** Bagimlilik varsa iskelet eksiktir; geri don, dalga ekleme.

- **4-6 ajan**, hepsi ayni mesajda, `model: "opus"`, **`effort: "low"` ya da `"medium"`**.
  `high` yasak — olculmus: `high` paketler 24-38 dakika surdu, `medium` olanlar 7-19.
- Her ajanin `owns` listesi ayrik, her ajan **~5-8 dakikalik** is alir.
- Bolme **dikey dilimlere** gore: "dunya + render", "ekonomi + tren", "kart + UI",
  "kampanya + HUD". Katmana gore bolme — katman bolmesi zincir uretir.
- `description` alani model ve effort tasir: `dunya+render · opus · low`.

### Paket prompt'u — kisa tut, dusunmeye sebep olma

```
PAKET: {ad}   MODEL: opus · EFFORT: {low|medium}
SURE HEDEFI: ~6 dakika. Bitmiyorsa calisani teslim et, mukemmeli degil.

OKU: docs/CONTRACT.md (imzalar + alan adlari), data/*.json (gercek veri)
YAZ: {owns — tam liste}
KABLOLAMA: src/main.js zaten seni cagiriyor. Dokunma.

YAPMA
- Test yazma. Kapi yazma. Mutasyon testi yazma.
- Kendi fixture'ini uydurma — data/*.json gercek.
- owns disina cikma. Eksik bir sey varsa DUR ve tek cumleyle rapor et.
- Yeniden mimari tartisma. CONTRACT.md karardir.
- Commit atma.

BITTI: modul import edildiginde hata atmadan yukleniyor ve gorevini yapiyor.
```

**"YAPMA" listesi sure tasarrufunun yarisidir.** Olculmus: mutasyon testleri ~60 dakika,
ajanlarin kendi kapilarini yazmasi ~5.000 satir.

## Faz 3 — Kablola, duman, bak (4 dk)

Duman kontrolu Faz 1 Kol B'de zaten yazildi; burada yalnizca **kosar**. Kosarken bakacagin sey:

```
headless Chrome ile ac -> sifir console error, canvas var, bir frame render edildi,
dunya nesneleri var, 60 saniye ilerlet -> oyun ilerliyor.
```

Tek dosya, ~40 satir, puppeteer-core + kurulu Chrome (buyuk indirme yok). **Kriter listesi
yazma.** Duman gecmiyorsa duzelt; gectiyse devam.

Sonra **ekran goruntusu al ve KENDIN BAK.** Ajan raporu gorsel kanit degildir.

## Faz 4 — Tek kompozisyon gecisi (2 dk)

Ekran goruntusune bak ve **yalnizca su uc soruyu** sor:

1. **Olcek okunuyor mu?** Oyuncunun bakmasi gereken sey (bina, birim, kart) kadrajda **ayirt
   edilebilir buyuklukte mi?** Olculmus hata: dunyayi 30-40 birim, binalari 1,2 birim yapmak;
   kasabalar nokta gibi okundu. Referans model dunyayi kucuk tutarak ayni sorunu hic yasamadi.
2. **Varsayilan kamera dogru cerceveliyor mu?** Her ekran goruntusunu elle zoomlamak zorunda
   kaliyorsan varsayilan yanlistir.
3. **Ust uste binen UI var mi?**

**En fazla 3 duzeltme. Yuzey detayina (sis, dalga, kiyi katmani, golge) dokunma** — okunabilirlik
kazandirmaz ve butceyi yer. Olculmus hata: uc katmanli kiyi yapip olcegi kacirmak.

---

## Yapma listesi — her biri olculmus bir maliyet

| Yapma | Olculmus maliyet |
|---|---|
| Kabul kriteri seti yazma (8 kriter, tarayici surucu) | ~5.000 satir kapi + kirmizilarin yarisi kapinin kendi hatasi |
| Pakete mutasyon testi yazdirma | ~60 dk |
| Cok dalga (8 dalga) kurma | zincir seri kalir, paralellik 1,04x |
| `effort: high` kullanma | 24-38 dk/paket, `medium` 7-19 dk |
| Plan defekt gunlugu tutma | prototipte okuyan yok |
| Determinizm/digest kaniti | GDD'nin tasarim sorusu bu degilse gereksiz |
| Ajanlarin kendi fixture'ini uydurmasi | iki ajan iki sema uydurdu, ~50 dk |
| Ekran goruntusune bakmadan "polish yapildi" demek | kompozisyon hatasi sonuna kadar tasinir |

## Teslim

1. `SCOPE.md` — ne var, **ne yok** (kesilenler acikca)
2. Calisan build + calistirma komutu
3. Bir ekran goruntusu
4. **"Bilinen eksikler"** — 5 madde, tek satir her biri

Kullanici daha fazlasini isterse **o zaman** urun hattina gec (`plan-build`). Prototip
sorusunu cevapladiginda isini bitirmistir.
