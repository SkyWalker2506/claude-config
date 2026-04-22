# Reference Games — Puzzle/Physics Postmortem

> Senior notları. Bu oyunları yıllarca söktüm, level dosyalarını inceledim, telemetry post-mortem'lerini okudum. Aşağıdakilerin her biri Golf Paper Craft tasarımına dönük somut ders içeriyor.

---

## 1. Angry Birds (Rovio, 2009)

**Temel fikir:** Sapanla fırlatılan kuşlarla domuz kalelerini yık — destroy-everything fizik bulmacası.

**İyi tasarım:**
- **3-yıldız sistemi** kullanıcıyı aynı level'ı 3-5 kez oynamaya ikna etti; LTV'yi 2x yaptı. "Geçtim" ile "ustalaştım" arasında ayrım koydu.
- **Risk-reward** — daha az kuşla bitir = yıldız fazlası. Oyuncu optimize etmek zorunda kaldığı için skill tavanı açıldı.
- Level başı ~15 saniye; mobil "bir tur daha" döngüsü için mükemmel.

**Zayıf yönü:**
- İleri seviyelerde **yıldız eşikleri keyfi** hissettiriyor — bazı 3-yıldızlar "lucky shot"a bağımlı, beceri değil. Frustration kaynağı.

**Golf Paper Craft'a uygulama:** Par sistemine ek olarak **"sub-par bonus yıldızı"** ekle. 1 yıldız = hole'u bitirme, 2 yıldız = par, 3 yıldız = par-1 veya altı. Yıldız eşiklerini **level başına manuel playtest et**, formülle belirleme — Angry Birds'ün en büyük hatası buydu.

---

## 2. Cut the Rope (ZeptoLab, 2010)

**Temel fikir:** Om Nom'a şekeri ulaştır — ip kes, fizikle yönlendir.

**İyi tasarım:**
- **Elegance** — tek input (tap/swipe), ama 200+ level boyunca taze. Bu çok nadir.
- **Mekanik layering:** ip → balon → hava üfleyici → ışın. Her 5-10 level'da **bir tane yeni element** ekleniyor, eskiler kombine ediliyor. "Rule of one new thing."
- Clean visuals — oyun alanı **her zaman okunabilir**, dekorasyon gameplay'i ezmez.

**Zayıf yönü:**
- Geç levellerde **element yığılması** — 4-5 mekanik birden ekranda; tutorial'sız gelen oyuncu kaybolabiliyor.

**Golf Paper Craft'a uygulama:** **"Bir level, bir yeni fikir"** kuralını benimse. Level 5'te rüzgar, Level 10'da trambolin, Level 15'te hareketli delik. Yeni mekaniği tanıttıktan sonra **en az 2 level solo kullan**, ancak sonra kombine et. Yeni mekanik geldiği level'da **ekranda başka karmaşa olmasın.**

---

## 3. Desert Golfing (Captain Games, 2014)

**Temel fikir:** Sonsuz procedural çölde, ekran başı tek delik, sürekli ileri. Reset yok.

**İyi tasarım:**
- **Minimalism** — UI yok, menü yok, müzik yok. Sadece topu vur. Zen pacing.
- **Deterministik fizik** — aynı vuruş her zaman aynı sonuç. Oyuncunun öğrenmesi mümkün olur.
- Bir ekran = bir hole. **Kognitif yük sıfır.**

**Zayıf yönü:**
- Progression hissi zayıf — 5000 level sonra da aynı çöl. Retention %2-3 seviyesinde.

**Golf Paper Craft'a uygulama:** HUD'u acımasızca kes. Hole başına ekranda **sadece: vuruş sayısı + par** olsun. Menü, puan, timer, streak sayacı — hiçbiri hole sırasında görünmesin. Fizik **kesinlikle deterministik** olmalı: aynı açı + aynı güç = aynı yörünge. RNG sadece level layout'ta, runtime'da asla.

---

## 4. Getting Over It (Bennett Foddy, 2017)

**Temel fikir:** Çekiçle kazandaki adamı dağın tepesine çıkar. Düşersen başa dönersin.

**İyi tasarım:**
- **Commitment mekanizması** — her hareket geri alınamaz. Kayıp %100 gerçek, bu yüzden kazanç %100 gerçek.
- Foddy'nin sesli narration'ı — oyuncuya **"düşeceksin, bu kasıtlı"** der; beklenti yönetimi.
- Tek input (mouse), ama mastery tavanı 200 saat.

**Zayıf yönü:**
- Hedef kitle dar — toplam satış ~2.5M, ama refund oranı yüksek. **Punishing difficulty pazarlamadan filtrelenmeli**, yoksa 1-yıldız yağar.

**Golf Paper Craft'a uygulama:** **Sakın Getting Over It olma.** Ama "**mulligan yok**" modu (hardcore) opt-in olarak sun — vuruş geri alınmaz, par aşımında level fail. Ana mod forgiving kalsın (undo var). Hardcore mode için **ayrı leaderboard** — o kitle kendi ligini kursun.

---

## 5. Peggle (PopCap, 2007)

**Temel fikir:** Topu fırlat, turuncu peg'lerin hepsini temizle. Pinball + Plinko hibridi.

**İyi tasarım:**
- **Random vs skill dengesi** mükemmel — ilk vuruş çoğunlukla skill, sonra top sekmeye başlayınca luck devreye girer. Oyuncu "kazandım" hisseder, aslında %40'ı şans.
- **"Skill shot" felsefesi** — zor açıdan vurursan bonus. Ödüllendirme görsel + audio (Ode to Joy) ile şişirilmiş.
- **Power-up az ve seyrek** — 10 level'da bir unlock, oyunu sulandırmıyor.

**Zayıf yönü:**
- Son peg'i vurmak için bazen **10 deneme** gerekiyor — RNG ucunda, frustration doğurur.

**Golf Paper Craft'a uygulama:** Golf'te skill shot karşılığı: **"trick shot bonusu"** — duvardan sektirerek delme, hole-in-one, bank shot. Tespit et, **abartılı feedback** ver (slow-mo + yazı + ses). Ama gameplay'in %70'i skill kalsın; RNG sadece "cherry on top" olmalı. Son hole-out'u RNG'ye bağlama — kesin hit olmalı.

---

## 6. What the Golf? (Triband, 2019)

**Temel fikir:** "Her level farklı bir oyuna dönüşen golf" — surprise-driven parodi.

**İyi tasarım:**
- **Her level yeni şaka** — topu değil golfçüyü fırlatırsın, sonra evi, sonra arabayı. Oyuncu **sürekli gülüyor** çünkü beklenti bozuluyor.
- Her level **30-60 saniye** — şaka sürmez, hızlı servis.
- Meta-referanslar (Portal, Super Hot, Angry Birds parodileri) — gamer izleyiciye göz kırpma.

**Zayıf yönü:**
- **Yeniden oynanabilirlik düşük** — şaka bir kere komiktir. Speedrun kitlesi dışında retention zayıf.

**Golf Paper Craft'a uygulama:** Ana kampanyaya bulaştırma, ama **"Bonus World" / "Weird 9"** gibi ayrı bir set hazırla — orada kuralları boz. Ters yerçekimi, topun yerine karton uçak, hole'un kaçması. **Surprise levels** 30-60 saniyelik hızlı tüketim olsun, oyuncu "ne olacak acaba" diye açsın. Ana kampanya ise **tutarlı kurallar** üzerine kurulu kalsın — iki mod, iki beyin.

---

## 7. Super Mario Bros World 3-1 (Nintendo, 1985) — Klasik Vaka

**Temel fikir:** İlk 30 saniyede oyuncuya **sağa git, zıpla, düşmandan kaç, blok kır** kavramlarını tek satır metin kullanmadan öğret.

**İyi tasarım:**
- **Goomba, sol taraftan gelen bir delikten çıkar** — oyuncu sağa bakar, Goomba gelir, oyuncu ya zıplar ya ölür. Zıplayan üstüne basar, ezer. **Mekanik tutorial, ölümle veya zaferle öğrenildi.**
- **? bloğu, Mario'nun zıplayabileceği yükseklikte** konumlandırılmış — kaza eseri kafayla vurup coin düşürüyorsun. Discovery by accident.
- **Her element, öncekinin üstüne inşa** — pipe, pit, moving platform hep sırayla.

**Zayıf yönü:**
- Modern oyuncu için **context yok** — neden sağa gidiyorum? Shigeru Miyamoto kuşağı "sol = menü" varsayımıyla büyüdü, Gen Z için bu artık implicit değil.

**Golf Paper Craft'a uygulama:** **Tutorial metni yazma.** Level 1, tek vuruşta bitecek düz bir hole olsun — oyuncu topa dokununca sürüklenir, bırakınca fırlar. **Mekanik kendini açıklasın.** Level 2'de küçük bir engel, level 3'te rüzgar oku, level 4'te kombine. Her yeni element **önceki level'da ölümsüz ortamda** test edilebilmeli. Miyamoto kuralı: "Yeni bir şey öğret, sonra test et, sonra başka şeyle kombine et."

---

## Sentez — Golf Paper Craft Design Pillar'ları

1. **Bir level, bir yeni fikir** (Cut the Rope) — ama **zen pacing** (Desert Golfing).
2. **Deterministik fizik, procedural yok** — skill hissi bunun üstüne kurulu (Desert Golfing + Peggle).
3. **3-yıldız par sistemi** manuel tune'lu (Angry Birds'ün hatasından ders).
4. **Trick shot bonus** — skill tavanı açıcı, replayability motoru (Peggle).
5. **Metinsiz tutorial** ilk 5 level (Mario 3-1).
6. **Surprise bonus world** ayrı — ana kampanyayı bozmasın (What the Golf).
7. **Hardcore opt-in mod** — ama default forgiving (Getting Over It kitlesine göz kırp, kaybetme).
