# /project-analysis

> **ÖNEMLİ — skill başlamadan önce:**
> Kullanıcıya şunu göster:
>
> ```
> Analiz başlamadan önce /compact önerilir (agent'lar çok token tüketir).
>
>   1) /compact çalıştır, sonra devam et
>   2) Geç ve devam et
> ```
>
> Kullanıcı "1" yazarsa → `/compact` çalıştırmasını hatırlat, çalıştırdıktan sonra devam et.
> Kullanıcı "2" veya sadece Enter basarsa → direkt devam et.

Bu skill tetiklendiğinde aşağıdaki adımları izle:

## Referans

Tam protokol: `__PROJECTS_ROOT__/PROJECT_ANALYSIS.md`

O dosyayı oku ve içindeki talimatlara **harfiyen** uy. Özetle:

---

## Adım 1 — Model seçimi sor

```
Analiz için agent model tipini seç:
  1) Opus   — en detaylı, en pahalı
  2) Sonnet — dengeli
  3) Haiku  — hızlı, ekonomik
  4) Karışık — her kategori için ayrı sorarım
  5) Lead Orchestrator — A1 kategori karmaşıklığına göre model seçer

Seçiminiz (1/2/3/4/5):
```

**5 seçilirse:** Her kategori için A1 (Lead Orchestrator) şu kurala göre model atar:
- Mimari, güvenlik, rekabet analizi → Opus
- Performans, SEO, büyüme, analitik → Sonnet
- UI tarama, içerik, erişilebilirlik → Haiku

## Adım 2 — Kategori seçimi (tek tek sor)

Her kategoriyi tek tek sor, kullanıcı 1/2/3 ile yanıt verir:

```
[KATEGORİ_ADI] — [kısa açıklama]
1) Evet (tam analiz)  2) Hayır (atla)  3) Kısmen (hızlı tarama)
```

Kategoriler:
1. UI/UX & Design
2. Performance & Core Web Vitals
3. SEO & Discoverability
4. Data & Scraping Infrastructure
5. Monetization & Business Model
6. Growth & User Engagement
7. Security & Infrastructure
8. Content & Editorial Strategy
9. Analytics & Tracking
10. Architecture & Code Quality
11. Accessibility (a11y)
12. Competitive Analysis

Tüm kategoriler sorulduktan sonra seçilenleri özetle ve onayla.

## Adım 3 — Agent'ları başlat (paralel, background)

Her seçilen kategori için ayrı bir Agent başlat (`run_in_background=true`).

Agent prompt şablonu (`PROJECT_ANALYSIS.md` §4'teki şablonu kullan):
- Proje kökünü otomatik tespit et (mevcut çalışma dizini)
- Model: kullanıcının seçtiği model
- Max 25 tool call (tarama: 15, araştırma: 10)
- Çıktı: `[PROJE]/analysis/[NN_kategori].md`

## Adım 4 — Master rapor

Tüm agent'lar tamamlanınca bir **Opus agent** başlat:
- Kategori raporlarını oku
- `[PROJE]/analysis/MASTER_ANALYSIS.md` oluştur
- `PROJECT_ANALYSIS.md` §5'teki master rapor yapısını kullan
- Cross-cutting insights + top 20 aksiyon listesi + maliyet tablosu

## Adım 5 — Kullanıcıya göster

1. Master rapor özeti
2. Dosya konumları
3. En kritik 5 aksiyon
