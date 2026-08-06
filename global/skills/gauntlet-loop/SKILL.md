---
name: gauntlet-loop
description: "Bir hedefi 'gauntlet loop' promptuna cevirir: gorev + fan-out build metodu + kor karsilastirmali kalite bariyeri. Sub-agent'lar uretir, ayri kritik ajanlar acimasizca reddeder, bar gecilene kadar donguyu surdurur. Triggers: gauntlet, gauntlet loop, gauntlet prompt, kor kritik, fan out ve dongu, referansa kadar dovus."
user-invocable: true
argument-hint: "[hedef] [--run] [--ref <referans>]"
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

## Adimlar

1. **Hedefi netlestir.** Belirsizse tek soru sor, sonra ilerle. Referans yoksa sen bir tane
   oner (rakip urun, mevcut ekran, sanat pegi) ve promptun icine yaz.
2. **Parcalama eksenini sec.** Ekran bazli · sistem bazli · varlik bazli. Parca sayisini
   yaz; 4-12 arasi tut. Daha fazlasi koordinasyon maliyetini kazanctan buyuk yapar.
3. **Kritik kriterini yaz.** Her parca icin "neye bakacak" bir cumle: kompozisyon, isik,
   tipografi hizasi, hissiyat, veri dogrulugu. Kritik ne olctugunu bilmezse nazik davranir.
4. **Cikis kosulunu yaz.** Kor karsilastirma sonucu + kac ardisik tur yesil kalmali (2 iyi
   bir sayidir; tek tur sans olabilir).
5. **Promptu tek blok halinde ver.** Aciklama, madde isareti, "istersen sunu da ekleyebiliriz"
   yok. Kullanici bunu kopyalayacak.
6. `--run` verildiyse promptu bu oturumda uygula: parcalari `Agent` ile fan-out et, her uretici
   icin ayri kritik ajan ac, kritik kirmizi verdikce ureticiyi geri bildirimle yeniden calistir.

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
