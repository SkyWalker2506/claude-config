---
name: animate
description: "Tek bir duragan karakter gorselinden oyuna girecek sprite animasyonu uret (Wan 2.2 I2V + olc-ve-karar ver dongusu). Triggers: animate, animasyon, sprite animasyon, karakter animasyonu, idle, yuruyus, saldiri animasyonu, sprite sheet, i2v, wan, animation-creator."
user-invocable: true
---

# Animate — Duragan Gorselden Sprite Animasyonu

Tek bir karakter gorselini image-to-video ile canlandirip sprite sheet'e cevirir.
Uretimi `animation-creator` yapiyor; bu belge **operatorun** ne yapmasi
gerektigini anlatir. Modelin ne yaptigini zaten repo'daki rehber anlatiyor —
pahaliya patlayan hatalarin hepsi operator tarafinda oldu.

- Repo: `~/Projects/animation-creator`
- Inceleme sitesi: https://animation-review-skywalker2506s-projects.vercel.app
- Kuyrugu suren surec: GPU'lu makinede `python -m animcreator.agent --watch`

---

## Isin akisi

**Sprite ekle** — kaynak gorseli yukler ve karaktere baglar. Once
[hazirla](#2-kaynagi-hazirla--ajan-bunu-yapmaz), sonra:

```bash
python -m animcreator.cli add-character --project necrobeat \
    --name "Crypt Spider" --image "D:/Projects/necrobeat/art/raw/spider-p.png"
```

**Istedigin animasyonlari kuyruga ver** — `--anim` tekrarlanabilir, her biri bir
yuva. Prompt'u yazmazsan o yuvanin preset'i kullanilir.

```bash
python -m animcreator.cli queue --character crypt-spider \
    --anim idle --anim walk.side --anim attack.melee
```

**Prompt'u kendin yaz** — preset yerine geceni istiyorsan:

```bash
python -m animcreator.cli queue --character crypt-spider --anim attack.melee \
    --prompt "the spider rears back on its hind legs and strikes forward once, \
black background, side view"
```

Preset'te `{subject}` gecen yerleri doldurmak icin `--subject "a bone spider"`
yeter; prompt'un tamamini yeniden yazmaya gerek yok.

**Bir surunu birden** — plan dosyasiyla:

```bash
python -m animcreator.cli batch --file plan.json
```

**Ayarlar**: `--frames` uretim karesi (17/25/33/49/65/81, Wan 4n+1),
`--width/--height` (sprite icin 512×512, sahne icin 832×480),
`--variants N` ayni yuvadan N farkli seed, `--dry-run` once ne gidecegini goster.

Sheet karesi diye ayri bir ayar **yok** ve olmamali — sheet uretilen her kareyi
tasir. Kisa animasyon istiyorsan `--frames` dusur.

### Yuva anahtari

`<action>[.<kind>][.<direction>][.<variant>]` — siralamasi onemli degil,
`attack.melee.right` ile `attack.right.melee` ayni yuvadir.

| | |
|---|---|
| action | idle, walk, run, attack, hurt, death, jump, cast, block, dodge, play, scene |
| kind | melee, range, magic, unarmed |
| direction | left, right, forward, back, side |

Ayni karakterin butun animasyonlari **ayni kaynak gorselden** uretilmeli, yoksa
birinde kapsonlu birinde kel cikar. Karakter bir kez eklenir, yuvalar uzerine
binir.

### Nerede gorulur

Uretilenler inceleme sitesinde belirir: izle, **Onayla** / **Reddet**, ya da
"neyin degismesi gerekiyor" kutusuna yalnizca degisikligi yazip revize iste.
Her videonun altinda **indir** ve **paylas** var; paylas videonun kendi acik
adresini verir, karsi tarafin giris yapmasi gerekmez.

Onaylananlarin listesi ve oyuna verilecek manifest:

```bash
python -m animcreator.cli kabul --olc --json kabul.json
```

### Ciktiyi almak

Sprite sheet her zaman lazim olmuyor — bazen videonun kendisi kullaniliyor
(fragman, sunum, bir sahnenin oldugu gibi girmesi).

```bash
# yalnizca adresler, indirme yok — gomecek olan icin dosya gereksiz
python -m animcreator.cli download --project necrobeat --what all --json adresler.json

# gercekten indir
python -m animcreator.cli download --clip gitarci --what video --takes latest --out out/
```

`--what` video / sheet / atlas / poster / all, `--takes` approved (varsayilan) /
latest / all. Dosya adi klip anahtarindan kurulur (`gitarci_calma_v1.mp4`);
depodaki ad `take_<hash>.<hash>.mp4` ve hangi klip oldugu anlasilmiyor.

### Yeni proje

Proje satiri olmadan o projenin isi kuyruga giremez (`anim_jobs.project_id`
foreign key; eksikse yirmi isin yirmisi de 23503 ile duser). Proje acmak
servis anahtarinin isi ama beklemek zorunda degilsin:

```bash
python -m animcreator.cli add-project --name "World Dominion" --note "kart sanati"
```

Istek depoya birakilir, GPU makinesindeki ajan saniyeler icinde projeyi acar,
komut proje gorunene kadar bekler. Donunce is basabilirsin.

---

## 1. Kollarin nerede oldugunu bil

Iki anahtar var ve hangisinin neyi yapabildigini bilmeden baslarsan bir saatini
`42501` hatasina yatirirsin.

| | anon anahtar | service anahtar |
|---|---|---|
| nerede | web sayfasi, CLI, herkes | **yalnizca GPU'lu makine** |
| yapabildigi | `sources/` altina gorsel yukle, is kuyruga ekle (`pending`), karar yaz | proje olustur, is sil, preset yaz, take/onay yaz |

Kural: sayfadan gelen her sey yalnizca **niyet ekler**. Onayin kendisi bir kayit;
onu duruma ceviren ajandir. Bir yazma denemesi `42501` ya da "row-level security"
diyorsa yanlis anahtarla dogru isi yapmaya calisiyorsundur — anahtari degistir,
politikayi degil.

## 2. Kaynagi hazirla — ajan bunu yapmaz

Yukledigin gorsel ne ise model onu canlandirir. Hazirlik senin isin:

1. Alfa kutusuna kirp
2. Kare tuvale otur, kenarda ~%6 pay birak
3. Alfayi **duz siyah** zemine duzlestir
4. 512×512'ye LANCZOS ile indir

Olculdu: ham RGBA sanat eserleri oldugu gibi yuklendiginde **39 klip kullanilmaz
cikti** — model siyah zemin yerine turuncu/yesil/mavi studyo fonu uydurdu ve
figurun basi ile ayaklari kadraj disina tasti. Sebep prompt degil, girdinin
bicimiydi.

Saydam PNG'yi oldugu gibi verme. Model boslugu karakterin renkleriyle doldurur.

## 3. Tam uzunluk iste, dongu icin kisaltma

Varsayilan **33 kare** (Wan 4n+1 disini sessizce yuvarlar: 17, 25, 33, 49, 65).

Dongu bozuksa kare sayisini dusurme. Olculdu: 46 klip 25 kareye indirildi, **55
tanesi hala sinirda kaldi** ve onay orani degismedi. Kisa cikti uretimden degil,
**dongu kirpicisindan** geliyor: az hareketli kliplerde gurultuyu "en iyi kesim
noktasi" sanip klibin yarisini atiyor. 8 kare @ 16 fps = 0.50 saniye; bir olcumde
219 sheet'in 97'si bir saniyenin altindaydi.

Duzeltmeyi orada yap: kirpici ancak **en iyi dikis kalintisi medyanin %60'inin
altindaysa** kessin. Uretim hattinda kirpma varsayilan olarak kapali
(`--loop-trim` ile acilir) ve `--keyframes 0` uretilen her kareyi tutar.

Dikis raporlanirken hangi sayinin okundugu onemli: **kesilmeyen** bir sheet'te
dogru sayi son karedeki kalintidir, en iyi kesim noktasindaki degil. Ikisi
karistirilirsa dongular oldugundan iyi gorunur (olculdu: ayni klipte 12.66'ya
karsi 15.96).

## 4. Yuva siluete uymali

Model verilen kareyi canlandirir; icerigini degistiremez.

- **Bacagi gorunmeyen, yere kadar cuppeli bir figure yuruyus verme.** Olculdu:
  yatay yer degistirme 5 px — gercek bir adimda 17 px. Prompt'u ne kadar
  duzeltirsen duzelt degismiyor, cunku sorun yapisal.
- **Elinde kilic olan karaktere "silahsiz saldiri" verme.** Kilic karede duruyor;
  model onu silemez. Nesneyi once gorselden cikarman gerekir.
- Arkasi donuk hali de ayni sebeple uretilemez: karakteri dondurmek yeni
  iceriktir, o acinin kendi gorseli gerekir.

Yeni bir nesne istiyorsan onu **hareket olarak** yaz: "ates ekle" calismaz,
"egilip feneri yere birakiyor, onunde ates yaniyor, elini uzatiyor" calisir.
