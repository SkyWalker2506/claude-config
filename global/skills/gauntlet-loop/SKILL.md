---
name: gauntlet-loop
description: "Bir hedefi 'gauntlet loop' promptuna cevirir: gorev + fan-out build metodu + kor karsilastirmali kalite bariyeri. Sub-agent'lar uretir, ayri kritik ajanlar acimasizca reddeder, bar gecilene kadar donguyu surdurur. Triggers: gauntlet, gauntlet loop, gauntlet prompt, kor kritik, fan out ve dongu, referansa kadar dovus."
user-invocable: true
argument-hint: "[hedef] [--run] [--ref <dosya yolu veya benzemesi istenen urun adi>]"
---

# /gauntlet-loop — bar gecilene kadar dovusen prompt

Bu skill **prompt uretir**, kod degil. Ciktisi tek parca, kopyala-yapistir bir gauntlet
promptudur. `--run` verilirse ureten sen ayni promptu bu oturumda calistirirsin.

> Uc parca: **Gorev** · **Build metodu (fan-out + kritik)** · **Bar (kor karsilastirma)**
> Ucu de olmayan prompt gauntlet degildir; sadece uzun bir istektir.

## Neden ise yariyor

Model kendi ciktisini "yeterince iyi" ilan eder. Ayri bir kritik ajan bu ilani elinden alir.
Fan-out ise her parcaya kendi kritigini verir — kalite tek bir genel degerlendirmeye degil,
parca sayisi kadar bagimsiz redde bagli olur. Dongu de bariyeri **cikis kosulu** yapar,
tavsiye degil.

## Uretecegin promptun iskeleti

```
[GOREV]
<tek cumle, somut cikti. "iyi bir X" degil, "su ekranlari olan, su girdiyi alan X".>

[BUILD METODU]
Hedefi mumkun olan en kucuk bagimsiz parcalara bol. Her parca icin bir alt-ajan calistir.
Her alt-ajanin AYRI bir kritik ajani olsun. Kritik ajan uretimi yapan ajan olamaz.
Kritik gorseli/ciktiyi <REFERANS> ile KOR karsilastirir: hangisi daha iyi, neden.
Kritik acimasiz olacak; "iyi olmus" yetmez, gececekse referansi gectigini gosterecek.
Kritik reddederse uretici ajan somut geri bildirimle yeniden calisir.

[BAR]
Her kritik, kor karsilastirmada ciktiyi <REFERANS>'a esit ya da ustun bulana kadar durma.
Tek bir parca bile kirmizi ise dongu devam eder.
```

`<REFERANS>` **daima somut olmali**: gercek bir urun, gercek bir ekran goruntusu, gercek
bir dosya. "AAA kalite", "profesyonel gorunsun" bar degildir — olculemez.

## Referansi nereden bulursun

Bar somut bir goruntu olmadan olculemez. Uc yol var; sirayla dene:

**1. Kullanici bir isim verdiyse → kendin arastir, sorma.**
"Call of Duty gibi", "Zelda gibi", "Linear gibi" dendiginde web'den o urunun ekran
goruntulerini bul ve indir. Internette bolca ornek var; kullaniciya "bana referans ver"
deme. Bulduklarini `refs/` altina kaydet, hangisinin ne icin oldugunu yaz.

**2. Kullanici sadece olayi anlattiysa, isim vermediyse → prompt uret, kullanici uretsin.**
Sen gorsel uretmiyorsun. Kullaniciya **kopyalanabilir gorsel uretim prompt'lari** ver;
kullanici GPT/benzeri bir araca verip goruntuleri sana geri getirir, sen onlari referans
olarak kullanirsin.

Prompt kurallari:
- Tek mesajda **en fazla 10 konu** — fazlasi tek sayfaya birlestirilip ise yaramaz hale gelir.
- Her prompt tek bir kare tarif etsin: kamera acisi, isik, palet, malzeme, kompozisyon.
- Cikti formatini yaz (en/boy orani, arka plan, UI var/yok).
- Numaralandir; kullanici geri getirdiginde hangi goruntunun hangi parcaya ait oldugu belli olsun.
- Ciktiyi tek blokta ver ki toplu kopyalanabilsin.

Kullanici goruntuleri getirdiginde `refs/` altina koy, gauntlet promptundaki `<REFERANS>`
alanina **dosya yollariyla** yaz.

**3. Ikisi de yoksa → mevcut ekran / rakip urun / eski surum** referans olur. Hicbir sey
yoksa gauntlet baslatma; olculemeyen bar, kritigi nazik yapar.

## Adimlar

1. **Hedefi netlestir ve referansi TEMIN ET** (asagidaki "Referansi nereden bulursun").
   Belirsizse tek soru sor, sonra ilerle.
2. **Parcalama eksenini sec.** Ekran bazli · sistem bazli · varlik bazli. Parca sayisini
   yaz; 4-12 arasi tut. Daha fazlasi koordinasyon maliyetini kazanctan buyuk yapar.
   **Ajan sayisi: gerekenden az degil, bir tane fazla da degil.** Parcalar ayni dosyalari
   yazacaksa birlestir; ayni gozle dogrulanacaksa tek kritik birden fazla parcaya baksin.
   Sadece **birbirinden bagimsiz basarisiz olabilen** isler ayri ajan hak eder.
3. **Kritik kriterini yaz.** Her parca icin "neye bakacak" bir cumle: kompozisyon, isik,
   tipografi hizasi, hissiyat, veri dogrulugu. Kritik ne olctugunu bilmezse nazik davranir.
4. **Cikis kosulunu yaz.** Kor karsilastirma sonucu + kac ardisik tur yesil kalmali (2 iyi
   bir sayidir; tek tur sans olabilir).
5. **Promptu tek blok halinde ver.** Aciklama, madde isareti, "istersen sunu da ekleyebiliriz"
   yok. Kullanici bunu kopyalayacak.
6. `--run` verildiyse promptu bu oturumda uygula: parcalari `Agent` ile fan-out et, her uretici
   icin ayri kritik ajan ac, kritik kirmizi verdikce ureticiyi geri bildirimle yeniden calistir.

## Calistirma bicimi

Gauntlet promptu tek bir istekle bitmez; **dongu tasiyicisina** ihtiyaci var:

- **Varsayilan: `/loop` + yuksek effort.** `/loop` bar yesillenene kadar turlari surdurur;
  kaliteyi ajan sayisi degil **effort** tasir. Uretici ajanlar `high`, en zor kritik/yargi
  adimi `max`. Mekanik parcalar (dosya tasima, isim degistirme) `low`.
- `ultracode` **varsayilan degil.** Fan-out'u acar ama ajan sayisini da patlatir; ancak
  kullanici acikca isterse veya is tek baglama sigmayacak kadar buyukse (genis migrasyon,
  coklu repo tarama) kullan.
- `/goal` de calisir ama kabul kriterini calistirilabilir hale getirmeni ister; gorsel
  kalite gibi kor-karsilastirmayla olculen barlarda `/loop` daha az surtunme uretir.

Promptun sonuna cikis kosulunu **yaz**; tasiyici durma karari icin oraya bakar.

## Uretim ortami: kritik kendi gozuyle gormeli

Kritik ajan ciktiyi kendisi yakalayabilmeli. Ortam basina yakalama yolu:

| Ortam | Kritigin gorme yolu |
|---|---|
| Web / prototip | Browser pane + `screenshot` |
| Unity | Unity CLI ile sahne screenshot'i (`docs/unity-cli.md` — GUI'yi computer-use ile surme) |
| CLI / veri | ciktinin kendisi + referans dosya diff'i |

Unity tarafinda kazanci saglayan sey ajanin **degistir → screenshot → karsilastir → duzelt**
dongusunu insan olmadan kapatabilmesi. Screenshot adimi yoksa gauntlet yoktur.

### Varlik politikasini promptta belirt

Iki mod var, ikisi de gecerli, ama **secmeden baslama**:

- **Dis varlik yok** — her sey primitive/sahne araclariyla kurulur. Zor, ama tutarli bir
  gorsel dil cikar ve lisans derdi olmaz.
- **Dis varlik serbest** — modular pack'ler kullanilir; hizli, ama kritik ozellikle
  **yanlis yonlendirilmis / ic ice gecmis** parcalari aramali (bu modun tipik hatasi budur).

Sprite gerekiyorsa uretim yolunu da promptta adlandir (orn. bir sprite uretim skill'i),
yoksa ajan placeholder ile yesil ilan eder.

## Izolasyon — sessiz kopyalama riski

Ajan, ayni makinedeki baska projelerden kod, kontrol semasi ve kamera ayari **kendiliginden**
odunc alabilir; cikti "one-shot" gorunur ama degildir. Temiz bir olcum istiyorsan prompta
sunu koy: *"Sadece bu proje dizinini kullan; baska projelerden referans alma."*
Aksi halde sonucu one-shot diye raporlama.

## Sinirlar — bunu bilmeden calistirma

- **Gauntlet sifirdan baslamaz.** Kotu bir temeli cok pahali sekilde cilalar. Once calisan,
  yonu dogru bir MVP; gauntlet ondan sonra hizlandirici olarak.
- **Pahalidir.** Saatler ve ciddi token. Kullaniciya calistirmadan once sureyi soyle.
- **Kritik gormeden karar veremez.** Gorsel isde kritige ekran goruntusu + referans goruntusu
  ver; metin tarifi kor karsilastirma degildir.
- **Sonsuz dongu riski.** Tur sayisina ust sinir koy (orn. parca basina 6). Sinira dayanan
  parcayi yesil ilan etme — **kirmizi olarak raporla**.

## Cikti

Tek fenced blok icinde gauntlet promptu. Ustunde en fazla iki satir: sectigin referans ve
parca sayisi. `--run` ile ayrica dongu ilerlemesi ve her parcanin kritik verdikti.
