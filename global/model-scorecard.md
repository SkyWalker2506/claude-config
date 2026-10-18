# Model kullanım karnesi — oturumlar arası (2026-10-18)

Bu karne dört oturumun kendi işlerinden çıkan sonuçları birleştiriyor: BoxSim (web oyunu), YouTube/NWB outreach, Assetler (asset pipeline) ve Survival (Unity HDRP). Puanlar 1–5 arası ve "bu iş için ne kadar uygundu" anlamına geliyor. Token sayıları yaklaşık ve alt-ajanın kendi toplamı. Gemini çağrıları Claude kotası harcamıyor.

## Puan tablosu

| İş tipi | Model / effort | Sonuç | Token | Puan | Kaynak |
|---|---|---|---|---|---|
| Kişiye özel kısa yazı (creator yanıtı) | Gemini Flash high + kural bloğu | ilk denemede doğru | 0 | 5 | YouTube |
| Aynı iş | Flash medium | iyi ama kalıp | 0 | 4 | YouTube |
| Aynı iş | Flash low / Haiku medium / Sonnet (kuralsız) | kural ihlali, uydurma, bağlam-kör | ~89K (Haiku) | 2 | YouTube |
| Gelen mail sınıflandırma (192) | Flash high, tek çağrı | doğru (örneklemle doğrulandı) | 0 | 4 | YouTube |
| Kişi toplama | LLM'siz script (API) | en verimli | 0 | 5 | YouTube |
| Kişi toplama | paralel Claude alt-ajanları | çok pahalı, az sonuç (bir tanesi 290K token, 34 kişi) | 290K | 1 | YouTube |
| Web araştırma taslağı | Flash high (agy) | iyi taslak, kaynak zayıf, olgu hatası | 0 | 4 | BoxSim |
| Derin araştırma | 3 paralel Claude alt-ajanı | iyi sentez, pahalı | 3×120K | 3 | YouTube |
| Katalog arama, LOD dönüştürme | sadece kod | sorunsuz | ~0 | 5 | Assetler |
| Asset kopyalama, liste, test verisini yeniden üretme | Haiku medium | başarılı | 118–180K | 4 | BoxSim |
| Asset + yerleşim kararı | Haiku medium | yarım kaldı, Sonnet bitirdi | 211K | 2 | BoxSim |
| IK / poz / animasyon düzeltmesi | Haiku medium | başarısız, Sonnet çözdü | 207K | 1 | BoxSim |
| IK / poz / animasyon düzeltmesi | Sonnet medium | çözdü; bir seferinde birim test yeşildi ama gerçek oyunda çalışmadı | 145–168K | 4 | BoxSim |
| Sistem / gameplay (yaya kaçışı, mesafe, oyuncu boksu) | Sonnet medium | çözdü, uzun sürdü | 195–440K | 4 | BoxSim |
| Layout / generator / mağaza içleri | Sonnet medium | çözdü | 130–250K | 4 | BoxSim |
| Motor güncellemesi + fizik testi | Sonnet medium | çözdü, gerçek motor hatasını buldu | 311K | 5 | BoxSim |
| Headless oyun botu (soak testi) | Sonnet medium | çözdü, gerçek bug buldu | 176K | 5 | BoxSim |
| Pitch deck taslağı | Sonnet medium | iyi | 114K | 4 | BoxSim |
| Unity küçük bug / perf düzeltmesi | Sonnet (varsayılan) | ilk denemede | 125–150K | 5 | Survival |
| Unity çok sistemli kök neden | Sonnet (varsayılan) | doğru, test eşiği gevşetildi | 208K | 4 | Survival |
| Unity PlayMode test yazımı | Sonnet (varsayılan) | 1 küçük hata (yöneticinin elle düzeltmesi gerekti) | 177K | 4 | Survival |
| Prosedürel Blender modelleme | Sonnet medium | çalıştı, ikinci tur gerekti | 240–340K | 3.5–4 | Assetler |
| Ses toplama (kulak kontrolü yok) | Sonnet medium | metadata ile seçildi | 240K | 3 | Assetler |
| Görsel iş (kamera, sinematik, framing) | Sonnet (tek ajan) | karanlık/uzak çekim, 2 tur | 430–490K | 2–3 | Survival |
| WhatsApp okuma (JS bloklu, 1 ekran görüntüsü) | Haiku low | her seferinde doğru | ~90K sabit | 4 | BoxSim |

## Çıkarımlar
1. Kod yazılabilecekse LLM kullanma. Katalog, toplama, dönüştürme gibi işler script ile 0 token ve 5 puan.
2. Gemini Flash high + açık kural bloğu yazı, sınıflandırma ve araştırma taslağında en iyi fiyat/performansı verdi. Kural bloğu olmadan kalite düşüyor. Her iddiayı doğrula.
3. Haiku medium dar ve mekanik işte iyi: kopyala, listele, yeniden üret. Karar, IK/poz ya da bağlam gerektiren yazıda zayıf. Bağlamı da hızla 100K'yı geçiyor.
4. Sonnet medium sistem, IK, layout, upgrade ve kök neden işlerinin neredeyse hepsini tek seferde kapattı. Büyük işleri bölmek gerekiyor.
5. Görsel değerlendirmeyi alt-ajana bırakma. Kamera, ışık ve framing kararını yönetici oturum contact sheet'e bakarak versin. Alt-ajan en fazla bir tur yapsın.
6. Birim test yeşil olması yetmez. Brief'e "gerçek oyun/sim yolundan test" ve rapor sonunda "test edilmemiş varsayımlar" bölümü şart.
7. Paralel Claude alt-ajanı çoğaltmak pahalı. Önce script, sonra Gemini, sonra tek ajan.
8. En büyük kota yakıcı uzun ana oturum, çünkü her mesajda tüm bağlam yeniden işleniyor. Bağlam 100–200K'ya gelince özetle ya da yeni oturum aç.

## Sırada denenecek
- Haiku high ile Sonnet medium'u aynı iş tipinde kıyaslamak (kesişme testi). İlk aday: bilinen dosyada küçük bug düzeltmesi.
- Flash medium ile log/test çıktısı özeti ve contact-sheet QA.
- Haiku low ile katalog, manifest ve lisans denetimi.
- Haiku medium ile "X'i N dosyaya bağla" tipi işler.
- Asset teslimatından önce otomatik geometri QA: non-manifold, ters normal, boyut.
- Unity: opt-in testlerde [Explicit]/[Ignore] yerine bayrak dosyası kullanmak. Görüntü kaydı headless değil, pencereli Unity'de (GPU'yu bloklar).
