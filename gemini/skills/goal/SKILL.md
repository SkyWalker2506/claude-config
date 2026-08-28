---
name: goal
description: >-
  Bir hedefi calistirilabilir kabul kriterlerine cevirir ve kriterler yesillenene
  kadar OLC -> TESHIS -> DUZELT -> TEKRAR OLC dongusunu durmadan dondurur.
  Kullan: "bitene kadar devam et", "hedefe kadar calis", "kriter yesillenene kadar",
  "goal", "hedef kilidi". Kriter olmadan hicbir uzun kosu baslatma.
metadata:
  version: v1
  publisher: musab
---

# goal — kriter yesillenene kadar durma

"Bitene kadar devam et" tek basina calistirilamaz bir emirdir, cunku **bitti**nin ne
oldugunu soylemez. Once onu soylet: hedefi **calistirilabilir kabul kriterlerine**
cevir, sonra o kriterler yesillenene kadar dongu don.

Kriter yoksa dongu iki sekilde bozulur: ya ilk makul cikti gorulunce erken durur, ya
da hicbir zaman durmaz. Ikisi de ayni koktenlik: olculemeyen hedef.

## Faz 1 — Hedefi kritere cevir

Hedef cumlesinden **3-8 kabul kriteri** cikar. Her kriter su testi gecmeli:

> Bir baskasi bu kriteri, benim ne yaptigimi bilmeden, tek komutla calistirip
> yesil/kirmizi diyebilir mi?

| Kotu kriter | Neden kotu | Iyi karsiligi |
|---|---|---|
| "Oyun duzgun gorunuyor" | "Duzgun" olculemez | `npx playwright screenshot ... && ekranda >= 3 ayri varlik bbox'i var` |
| "Testler yaziliyor" | Faaliyet, sonuc degil | `npm test -> exit 0, >= 12 test` |
| "Performans iyi" | Esik yok | `500 partikulde frame time < 16ms` |
| "Calisiyor" | Neyin? | `node -e "import('./src/main.js')" -> 0 hata; konsolda 0 adet "Uncaught"` |

`.goal/criteria.json` yaz:

```json
{
  "goal": "Prototip tarayicida acilir ve cekirdek dongu oynanir",
  "criteria": [
    {"id":"C1","check":"http sunucu ac, sayfayi yukle, konsolda 0 error","why":"acilmayan sey oynanmaz"},
    {"id":"C2","check":"screenshot al, oyuncu + en az 1 dusman + HUD gorunuyor","why":"bos sahne dongu degildir"},
    {"id":"C3","check":"advance(60) cagir -> skor degisti","why":"dongu gercekten ilerliyor mu"}
  ],
  "blocked_by_human": []
}
```

**Kriteri sonradan gevsetme.** Kirmizi kriteri yesillendirmek icin esigi dusurmek,
hedefi degistirmektir; yapilacaksa kullaniciya **acikca** soylenir, sessizce degil.

## Faz 2 — Dongu

Her tur ayni dort adim:

```
OLC -> TESHIS -> DUZELT -> TEKRAR OLC
```

1. **Olc.** Butun kriterleri calistir. Kismi degil, hepsini — bir duzeltme baska bir
   kriteri kirabilir ve bunu ancak hepsini kosarak gorursun.
2. **Teshis.** Kirmizi kriterlerden **birini** sec: en cok digerini acan hangisiyse o.
   Kirmizinin sebebini yaz. Sebep yazilmadan yapilan duzeltme tahmindir.
3. **Duzelt.** Sadece o sebebe yonelik. Yoldayken gordugun ilgisiz seyi duzeltme —
   kaydet, gec.
4. **Tekrar olc.** Ayni turda. Yesillendiyse sonraki tura; yesillenmediyse teshis
   yanlisti, yeni teshis yaz, eskisini tekrarlama.

Her tur sonunda `.goal/log.jsonl`'e bir satir: tur no, kriter durumlari, ne degisti,
hangi dosyalar.

## Faz 3 — Ne zaman durur

| Durum | Kosul | Ne yapilir |
|---|---|---|
| **Basari** | Tum kriterler ayni turda yesil | Commit, ozet yaz, dur |
| **Ilerleme yok** | 3 ardisik turda hicbir kriter durum degistirmedi **ve** yeni bilgi cikmadi | DUR. Kullaniciya: hangi kriter, uc teshisin neydi, neden tutmadi |
| **Insan kilidi** | Kriter senin uretemeyecegin bir girdiye bagli (sanat varligi, kimlik bilgisi, urun karari) | O kriteri `blocked_by_human`'a tasi, **kalan kriterlerle devam et**, sonda acikca listele |

"Ilerleme yok" kurali `durmasin` emrinin karsiti degil, kosuludur: ayni duvara
dorduncu kez kosmak devam etmek degil, donmektir.

## Rapor etme kurali

Her tur sonunda tek satir yaz: `tur N — C1 yesil, C2 kirmizi (sebep: ...), C3 yesil`.
Sessizce calisma; ama her tur icin kullaniciya **soru sorma** — sadece durum bildir.
