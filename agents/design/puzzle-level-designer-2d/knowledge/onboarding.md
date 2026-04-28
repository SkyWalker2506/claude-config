# Onboarding: Ilk 5 Level Retention Sanati

> Tutorial yazan tasarimci, tasariminda basarisiz olmustur. Level **kendisi** ogretir.

## 1. Numaralar Once: Retention Cliff

Casual puzzle oyunlarinda D1 benchmark ~%35-40, D7 ~%10-15 (Quantic Foundry, 2021). **Ilk 90 saniye** D1'in yaklasik %60'ini belirler. L1'i tamamlayan oyuncunun D1'i ~%62; tamamlamayanin ~%11. Cikis tek bir yerde: L1. Sayilar tartisilmaz:

- **Time-to-first-interaction**: <15 sn (menu skip edilebilir olmali)
- **Time-to-first-success**: 15-30 sn
- **L1 completion rate**: %95+
- **L5 completion rate**: %75-80
- **Avg attempts L1-L3**: <=2
- **Mekanik introduction hizi**: 1 yeni / 2-3 level, asla L1'de 2 yeni

Bu esikleri tutmayan prototip scale'de oler. Iterasyon bu sayilari hedefler.

## 2. Tutorial-Free Teaching: Level Ogretir

**Super Mario Bros 1-1 kanonu (Miyamoto, 1985).** Mario solda spawn, sag bos. Goomba 3 saniye icinde saga girer. Oyuncu durur → oler. Ikinci denemede ziplar. Goomba'ya ustten dokunur → Goomba oler. Hareket, hasar, ezme — **tek ekranda, metinsiz**. Sol duvar kapali (pasif yonlendirme). "?" block'un konumu zipla-keşfet dongusunu tetikler. Miyamoto bu ekrani **6 ay** iterate etti.

Kurallar:
- **Obstacle placement = ok isareti.** Oyuncu yapacagini bakar bakmaz hissetmeli.
- **Text = tasarim basarisizligi.** "Drag to aim" paneli varsa, visual hook zayif demektir. Ideal: 0 kelime; max 4 kelime.
- **Ilk etkilesim odullu.** Rastgele dokunma bile bir sey yapmali (top hareket, ses, animasyon).
- **Ilk mekanik animasyonu 5 saniye icinde ekranda** (el drag jesti, top hazir pozisyon).

## 3. Safe Failure Zone — Cost-Free Learning

L1'de **olmek bile ogretmeli**. Fail uzerine:
- Instant retry (<1 sn, fade yok)
- Hayat/can/coin cezasi yok, progress kaybi yok
- maxShots L1-L3'te bol (≥5), kanonik cozum 1-2 atista
- Fail animasyonu keyif verir (Om Nom'un hayal kirikligi yuzu, Angry Birds ipoksala)

Cut the Rope L1: ip kes → seker duser → varir. Fail **imkansiz**. L2: ip yanda, oyuncu kesince seker yana duser → ilk ucretsiz lesson. Angry Birds L1: tek kus, tek blok, tek domuz; iskala = kus geri dondurulur, yeniden dene. Oyuncu "denedim, sonuc bu" yargisini cezasiz alir.

## 4. Mekanik Intro Sirasi (principles.md §3)

Mark Brown / Nintendo kanonu — her mekanik 4 asamadan gecer:

```
Teach   : izole, distraktor yok
Practice: ayni mekanik, setup sikilasir
Combine : yeni + bilinen mekanik birlikte
Twist   : mekanigin ters/bosaltici kullanimi
```

**Atlamak yasak.** Combine L4'ten, Twist L6+'dan once gelmez. Ilk 5 level tek bir mekanik seti uzerinde oturur: atis + statik zemin + statik engel. O kadar.

## 5. Hook: Ilk 30 Saniyede "Wow"

Oyuncu L1'i bitirmeden once bir kere "hah" demeli:
- Angry Birds L1: 3-4 bloklu domino cokusu — fizigin magic'i.
- What the Golf L1: top degil, golfcunun kendisi firlar — **beklenti kirilir**.
- Cut the Rope L1: 8 saniyelik satisfying loop.

Surprise = retention yakiti. Kotu hook: menu → setting → tutorial video → kural paneli → L1. 40 saniye, sifir etkilesim, quit. Iyi hook: aç → 5 sn sonra drag → 10 sn sonra shot → 15 sn sonra success FX.

**Success FX kucuk ama net.** Confetti degil, satisfying snap. Kucuk odulun tekrar ettirici gucu, buyuk gosterinin shock'undan yuksektir.

## 6. L1'de TANITILMAYACAK Mekanikler

Timing-kritik, state-aware veya ters-sezgisel olan her sey L5+'a ertelenir. Golf Paper Craft icin:

Bu “min level” tabloları game-pack’e aittir. Core onboarding dosyasında yalnız metodoloji tutulur.
Golf Paper Craft için bkz: `../game-packs/golf-paper-craft/progression.md`

Ek yasaklar L1-L5: ruzgar, hareketli engel, multi-shot combo, time limit, reverse logic, zincirleme, chain trigger.

## 7. Cut the Rope Ilk 5 Postmortem

| L | Yeni mekanik | Sure | Fail olasi | Ders |
|---|---|---|---|---|
| 1 | Rope cut (izole) | 8 sn | hayir | kes → dus → varir |
| 2 | Rope + angle | 15 sn | ilk yanal dusus | acili dusus mumkun |
| 3 | 2 rope + sira | 25 sn | timing fail | kesme sirasi onemli |
| 4 | Bubble (izole) | 30 sn | bubble patlamasi | yukari hareket |
| 5 | Bubble + rope | 45 sn | kombine fail | iki mekanik birlikte |

Tempo: +15 sn/level, 1 yeni mekanik/2-3 level, 0 text tutorial. ZeptoLab bunu 5 yil iterate etti.

## 8. Angry Birds L1 Postmortem

Tek kus, tek domuz, tek blok, tek nokta. Oyuncu sling'i geri ceker (affordance: lastik gerilir), birakir, kus ucar. Isabet sansi %30-50 — ilk shot'ta vurmama ihtimali kasitli: **dene-dene dongusu tetiklenir**. 2. veya 3. shot'ta mutlaka vurur. Rovio pazarlamadan once L1'i 200+ kisiyle test etti.

---

## Game-specific onboarding specs
Game-specific onboarding specs (L1–L5 targets, mechanic intro min-level tables, etc.) must live in the relevant game-pack.

Golf Paper Craft:
- `../game-packs/golf-paper-craft/level-rules.md`
- `../game-packs/golf-paper-craft/progression.md`
