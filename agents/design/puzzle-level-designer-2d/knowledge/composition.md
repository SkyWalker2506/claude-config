# Composition — Level'da Görsel Kompozisyon

> Senior not defteri. Level ekranı bir kompozisyondur; engeller figür, boşluk zemin. Kaotik görünen her level, kompozisyon kuralı ihlalinin sonucudur.

## 1. Gestalt — Oyuncunun beyni ne görüyor

Oyuncu level'a baktığı ilk 400ms'de engelleri **grup** olarak okur, tek tek değil. Bu gruplama kuralları:

- **Proximity (yakınlık):** Birbirine yakın engeller tek bir "duvar" gibi algılanır. 2 tree 60px aralıkta = kapı. 4 tree 60px aralıkta = bariyer, çözümsüz hissi verir. Engel grupladıysan niyetli yap, kazara değil.
- **Similarity (benzerlik):** Aynı tipten 3 engel yan yana "ritim" kurar — oyuncu 4.'yü bekler. Bu beklentiyi kırmak (4.'yü farklı tip yapmak) sürpriz yaratır, ama seyrek kullan; her level sürpriz = hiçbiri sürpriz değil.
- **Continuation (süreklilik):** Engellerin oluşturduğu hayali çizgi, gözü yönlendirir. 3 bush hafif yay yapıyorsa, oyuncu "top bu yaydan geçecek" hisseder. Süreklilik = ipucu.
- **Closure (kapanma):** Yarım çember engel dizilimi, oyuncuya "içine sokma" der. Kullanıldığında güçlü — ama closure'ı kırıp içinden geçirtirsen cheat hissi verir.

## 2. Negatif Alan — Engelin olmadığı yer de tasarımdır

Acemi designer engel yerleştirir; senior **boşluk** yerleştirir. Trajectory'nin geçeceği koridor senin figür'ün, engeller bu koridoru çerçeveleyen zemin.

Kural: Kanonik trajectory ekseninin ±40px'inde hiçbir engel olamaz (çarpışma yarıçapı + nefes payı). Eğer bir engel koridoru daraltıyorsa, bu niyetli zorluktur — log'la.

## 3. Leading Lines — Oyuncunun gözü nereden geçer

BallStart'tan hole'a oyuncunun gözü **düz gitmez**. Engeller, obje siluetleri, canopy eğrileri gözü yönlendirir. İyi tasarım: gözün takip ettiği yol ≈ topun izleyeceği yol.

- Ağaç gövdelerinin dikey çizgileri → göz aşağı/yukarı gider
- Platform üst kenarı → göz yatay akar
- Water glint yansıması → göze "burada dikkat" der
- Cloud dizilimi sola eğimliyse → göz sola kaydırır (sağa atış level'ıysa bu kötü)

Kural: Dekor elementleri trajectory ile **aynı yönde** akmalı, zıt değil.

## 4. Foreground vs Background — Hiyerarşi

3 katman, net ayrılmış:
- **Background:** dağlar, bulutlar, uzak ağaçlar. Alpha 0.4-0.6, desatüre. Dokunulmaz, dikkat çekmez.
- **Midground:** zemin, water, platformlar. Tam renk ama düşük kontrast.
- **Foreground:** obstacles, ball, hole. En yüksek kontrast, en satüre renk, gerekirse outline.

Yaygın hata: Dekoratif ağacı obstacle ağacıyla aynı renk/boyutta çizmek. Oyuncu "buna çarpıyor muyum?" diye düşünmek zorunda kalır. Bu **cognitive tax**, level'a katkı değil kayıp.

## 5. Composition Triangle — 3 engel kuralı

Insan gözü 3'e kadar paralel işler, 4+'da sayar. Levele 3 engel koyarsan oyuncu bir anda kavrar. 4 koyarsan "bakayım" moduna geçer — bu hoş bir zorluk değil, overload.

- Level 1-10: 1-2 engel
- Level 11-30: 2-3 engel
- Level 31-60: 3 engel, maks
- Boss level: 4-5 engel **bilinçli kaotik**, istisna

## 6. Chekhov's Gun — Her engel sebepli

"Duvardaki silahın ateşlenmesi gerekir." Her engel ya trajectory'yi etkiler, ya karar yaratır, ya risk ekler. Etkisiz engel = dekor. **Dekor yasak.**

Test: Engeli sil → level değişiyor mu? Hayırsa, at.

## 7. Kötü Kompozisyon Kalıpları — Görür görmez tespit et

- **Lineer serpinti:** Engeller düz çizgide. Görsel olarak ölü, tek karar noktası.
- **Symmetry trap:** Perfect simetri. Estetik ama puzzle olarak sıkıcı — simetri çözümü tekleştirir.
- **Overcrowding:** 5+ engel. Oyuncu hangisine çarpacağını bilemez, rastgele deneme yapar.
- **Obstacle grid:** Engeller eşit aralıklı ızgarada. Organik değil, level değil, editör açık unutulmuş gibi.
- **Echo wall:** Aynı tipten 3+ engel aynı hizada. Çeşitlilik yok, karar yok.

## 8. Cluster Kuralı

**Max 2 engel 80px yarıçap içinde.** 3. engel girdiyse, ortadaki "obstacle wall" olur — oyuncu duvar gördüğünü sanar, çözüm yolunu göremez. Ayrık tut.

İstisna: Niyetli "kapı" — 2 tree tam 80px aralıkta, topun sığması için. Bu cluster değil, gate.

## 9. Kanonik Yol Visibility — Gerilim

İyi level: Oyuncu çözümü **görür ama kolay bulmaz.** Kötü level: Çözüm gizli (frustrating) veya aşikâr (boring).

Test: Level'ı 3 sn göster, kapat. Oyuncu trajectory'yi eliyle çizebiliyor mu? Çizebildiyse çok kolay. Hiçbir fikri yoksa çok zor. "Sanırım böyle" diyorsa — altın nokta.

## 10. Görsel İpucu Tasarımı

Engeller oyuncuya **pasif olarak konuşmalı**:
- **Canopy yüksekliği:** Alçak canopy = altından geçmek zor, üstten öner. Yüksek canopy = üstten imkansız, altı ve kenar.
- **Tramp rengi:** Parlak kırmızı = yüksek bounce, pembe = orta. Oyuncu dokunmadan gücünü tahmin eder.
- **Water derinliği:** Koyu mavi = ölüm, açık mavi = sığ (bazı variant'lerde sekme). Renk = risk sinyali.
- **Wind vane:** Okun uzunluğu güç, yönü yön. İkon yeterli değil — net vektör.

Kural: Mekanik değişirse görsel değişmeli. Aynı sprite, farklı davranış = oyuncuya yalan.

## 11. Concrete Kurallar

1. Her level tam olarak 1 kanonik trajectory'ye sahip olmalı, koridoru ±40px.
2. Max 3 engel (boss istisna).
3. 80px içinde max 2 engel (gate istisna).
4. Hiçbir engel trajectory ekseninin ±30px'inde durmaz (kolizyon payı için).
5. Dekor yasak — her obje ya mekanik ya ipucu.
6. Foreground kontrastı background'tan en az 2x.
7. Leading line yönü = trajectory yönü.
8. Eşit aralık yasak — ritmi kır.
9. Simetri sadece boss'ta.
10. Silüet testi: siyah dolu görsel, engel tiplerini ayırt edebiliyor musun? Hayırsa yeniden çiz.

---

## Golf Paper Craft'a Uygulama

Bu projede kamera 480x800, trajectory genelde parabolik soldan-sağa. Somut kurallar:

1. **Trajectory ekseni ±30px içinde engel yok.** Level generator'da ilk pass: kanonik arc hesapla, her engelin merkezini arc'a olan dik mesafesini ölç. <30px ise reddet.
2. **3-engel limiti.** Level.config.obstacles.length ≤ 3. Level.tags içinde `"boss"` varsa ≤ 5.
3. **Cluster kontrolü:** Engel çiftleri için distance hesapla. `dist < 80 && count > 2` → reject.
4. **ballStart-hole hayali çizgisi:** Engeller bu çizginin aynı tarafında toplanmasın; en az 1 engel her iki yarıda olsun (boss hariç). Aksi halde "çözüm tek tarafta" hissi.
5. **Dekor yok.** config'te sadece oyuncuya çarpan/etkileyen obje. Bulut, dağ = background layer, collision yok, alpha 0.5.
6. **Obstacle silueti unique:** tree/bush/rock/tramp/windmill — her biri farklı bounding shape. Aynı level'da iki "yuvarlak" (bush + rock) yan yana koyma, oyuncu karıştırır.
7. **Wind indicator UI overlay:** kompozisyona dahil değil — HUD katmanında.
8. **Water body:** trajectory'nin altında minimum 60px mesafede başlasın; yakın water "eminim düşecek" paniği yaratır.
9. **Hole konumu:** ekran kenarlarından minimum 40px içeride, sağ alt çeyrek tercih (doğal okuma yönü).
10. **Silüet testi script'le:** level'ı siyah dolu render et, engel tipleri ayırt edilebiliyor mu — ayırt edilemezse sprite varyasyonu ekle veya pozisyon kaydır.

Generator test fonksiyonu: `validateComposition(level)` — yukarıdaki 10 kuralı geçmeyen level'ı reject eder. Bu olmadan üretilen her level bir gün oyuncuya "ne oluyor burada" dedirtir.
