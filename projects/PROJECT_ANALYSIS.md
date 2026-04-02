# Project Analysis — Multi-Agent Deep Audit

Bu dosya herhangi bir projede `/project-analysis` komutuyla tetiklenir. Birden fazla uzman agent paralel olarak projeyi analiz eder, sonuclari tek bir master raporda birlestirir.

---

## Analiz Kategorileri

| # | Kategori | Odak | Agent gorevi |
|---|----------|------|-------------|
| 1 | **UI/UX & Design** | Gorsel tasarim, layout, renk paleti, tipografi, responsive, dark mode, animasyon, component tutarliligi, design system, erisilebilirlik (a11y), mobile UX | Projeyi tarayip UI/UX kalitesini degerlendir, eksikleri ve iyilestirmeleri listele |
| 2 | **Performance & Core Web Vitals** | LCP, FID, CLS, bundle size, lazy loading, image optimization, caching, SSR/SSG/ISR stratejisi, DB sorgu performansi, API response time | Performans darbogazlarini bul, olcum onerileri sun |
| 3 | **SEO & Discoverability** | Meta tags, Open Graph, structured data (JSON-LD), sitemap, robots.txt, canonical URL, semantic HTML, page speed, mobile-friendliness, internal linking | SEO eksiklerini tespit et, arama motoru gorunurlugunu artir |
| 4 | **Data & Scraping Infrastructure** | Veri kaynaklari, scraper mimarisi, veri kalitesi, veri guncelligi, pipeline robustness, error handling, rate limiting, veri modeli, Prisma schema | Veri altyapisini degerlendir, yeni kaynaklar ve iyilestirmeler oner |
| 5 | **Monetization & Business Model** | Gelir modelleri (premium, ads, sponsorship, API), pricing stratejisi, conversion funnel, paywall, freemium vs premium, affiliate | Monetizasyon firsatlarini analiz et, uygulanabilir modeller oner |
| 6 | **Growth & User Engagement** | Viral loop, gamification, social sharing, notification, retention, onboarding, community, user journey, referral, push notification | Kullanici kazanimi ve tutma stratejilerini degerlendir |
| 7 | **Security & Infrastructure** | Auth, OWASP top 10, env/secret yonetimi, CORS, rate limiting, input validation, dependency audit, error handling, logging, monitoring | Guvenlik aciklari ve altyapi eksiklerini tespit et |
| 8 | **Content & Editorial Strategy** | Icerik kalitesi, icerik cesitliligi, editorial flow, UGC (user-generated content), moderation, icerik guncelligi, tone of voice | Icerik stratejisini degerlendir, yeni icerik turleri oner |
| 9 | **Analytics & Tracking** | Event tracking, conversion tracking, funnel analizi, heatmap, A/B test altyapisi, user behavior, dashboard, KPI tanimlar | Analitik altyapisini degerlendir, olcum stratejisi oner |
| 10 | **Architecture & Code Quality** | Kod yapisi, modulerlik, test coverage, CI/CD, dependency management, tech debt, scalability, error boundaries, type safety | Kod kalitesini ve mimariyi degerlendir, refactor onerileri sun |
| 11 | **Accessibility (a11y)** | WCAG 2.1/2.2, keyboard navigation, screen reader, color contrast, focus management, ARIA, alt text, form labels | Erisilebilirlik standartlarina uyumu degerlendir |
| 12 | **Competitive Analysis** | Rakip platformlar, feature gap, pazar konumlandirma, diferansiasyon, SWOT, benchmark | Rakipleri arastir, projenin pazar konumunu degerlendir |

---

## Kullanim

### 1. Skill tetikleme

Kullanici `/project-analysis` yazdiginda:

### 2. Model secimi sor

```
Analiz icin agent model tipini sec:
  1) Opus    — en detayli, en pahali
  2) Sonnet  — dengeli
  3) Haiku   — hizli, ekonomik
  4) Karisik — her kategori icin ayri sorarim
  5) Otomatik — Opus her kategori icin en uygun modeli secer

Seciminiz (1/2/3/4/5):
```

- 1/2/3 secilirse tum agentlar o modeli kullanir
- 4 secilirse her kategori icin ayri model sorulur
- 5 secilirse: **kategori secimi adimi atlanir.** Bir Opus agent direkt projeyi tarayarak her kategori icin iki karar verir:
  1. **Gerekli mi?** — Bu projeye uygun mu, atlansın mı? (ornegin yeni bir proje icin SEO erken olabilir, scraping altyapisi yoksa kategori 4 anlamsiz olabilir)
  2. **Hangi model?** — Karmasik/kritik → Opus, orta → Sonnet, yuzeysel/hizli → Haiku
  Sonucta her kategori icin `{ include: true/false, model: opus/sonnet/haiku, reason: "..." }` cikarir, kullaniciya ozetler ve onay alir, sonra ana analiz o atamayla baslar

### 3. Kategori secimi sor (tek tek)

Her kategoriyi tek tek sor. Kullanici 1, 2 veya 3 ile yanit verir.

```
[KATEGORI_ADI] — [kisa aciklama]
1) Evet  2) Hayir  3) Kismen
```

- **1 (Evet):** Tam derinlikte analiz — max tool call, detayli rapor
- **2 (Hayir):** Bu kategori atlanir
- **3 (Kismen):** Hafif analiz — sadece proje taramasi (web arastirmasi yok), kisa rapor, yarisina yakin tool call limiti. "Baksın ama cok onemli degil" seviyesi. Master raporda ayri isaretlenir.

Tum kategoriler sorulduktan sonra secilenleri ozetle ve onayla.

### 4. Agent'lari baslat

Her kabul edilen kategori icin ayri bir Agent baslat (`run_in_background=true`, paralel).

Her agent su siralamayla calisir:
1. **Proje taramasi** — Read, Grep, Glob ile projeyi incele (max 15 tool call)
2. **Dis dunya arastirmasi** — WebSearch, WebFetch ile guncel bilgi topla (max 10 tool call)
3. **Rapor olustur** — Markdown formatinda detayli rapor yaz

#### Watchdog

Tum agentlar baslatildiktan sonra ana oturum **watchdog** gorevi ustlenir:

- Agentlar tamamlandikca bildirim gelir (background agent completion)
- Her 3 dakikada bir tamamlanan vs bekleyen kategori listesini goster:
  ```
  Analiz durumu (X/Y tamamlandi):
  ✅ UI/UX Design
  ✅ Security
  ⏳ Performance (calisıyor...)
  ⏳ SEO (calisıyor...)
  ```
- Bir agent 8 dakika icinde tamamlanmazsa **takili kabul et**:
  1. Kullaniciya bildir: `⚠️ [KATEGORİ] agent takıldı görünüyor. Yeniden başlatayım mı? (e/h)`
  2. Onay gelirse o kategoriyi ayni parametrelerle tek basina yeniden baslat
  3. Onceki agent'in ciktisi yoksa temiz baslat; kismi cikti varsa devam et
- Tum agentlar bitince (veya maksimum 20 dk sonra) master rapor asamasina gec

Her agent'in prompt'u asagidaki sablonu kullanir:

```
(Model Adi)
Sen bir [KATEGORI] uzmanissin. Asagidaki projeyi [KATEGORI] perspektifinden analiz et.

Proje koku: [PROJE_YOLU]

## ADIMLAR

### 1. PROJE TARAMASI (Read, Grep, Glob — max 15 tool call)
- Proje yapisini incele
- [KATEGORI] ile ilgili dosyalari bul ve oku
- Mevcut durumu degerlendir

### 2. DIS DUNYA ARASTIRMASI (WebSearch, WebFetch — max 10 tool call)
- Guncel best practice'leri arastir
- Rakip/benchmark orneklerini bul
- Sektordeki trendleri incele

### 3. RAPOR OLUSTUR

## [KATEGORI] Analiz Raporu

### Mevcut Durum
- Ne yapilmis (guclu yanlar)
- Puan: X/10

### Kritik Eksikler (hemen yapilmali)
| # | Sorun | Etki | Cozum | Efor |
(tablo)

### Iyilestirme Onerileri (planli)
| # | Oneri | Etki | Cozum | Efor |
(tablo)

### Kesin Olmali (industry standard)
- ...

### Kesin Degismeli (mevcut sorunlar)
- ...

### Nice-to-Have (diferansiasyon)
- ...

### Referanslar
- Arastirma kaynaklari

## KURALLAR
- Kod yazma, dosya duzenleme YAPMA — sadece oku ve raporla
- Somut, actionable oneriler sun
- Her oneri icin etki (High/Med/Low) ve efor (S/M/L/XL) belirt
- Raporu Turkce yaz
- Max 25 toplam tool call
```

### 5. Master rapor olustur

Tum agent'lar tamamlandiginda bir **Opus agent** baslat:
- Tum kategori raporlarini oku
- Tek bir master dosyada birlestir: `[PROJE]/analysis/MASTER_ANALYSIS.md`
- Kategori raporlarini ayri dosyalarda sakla: `[PROJE]/analysis/[kategori].md`
- Cross-cutting insights (kategoriler arasi baglantilar) ekle
- Oncelikli eylem plani olustur (top 20 item, kategoriler arasi)
- Genel puan karti olustur

Master dosya yapisi:

```markdown
# [Proje Adi] — Master Analysis Report
> Generated: [tarih] | Categories: [N] | Model: [model]

## Executive Summary
- Genel puan: X/10
- En guclu alan: ...
- En zayif alan: ...
- Acil aksiyon sayisi: N

## Puan Karti
| Kategori | Puan | Kritik | Iyilestirme | Nice-to-Have |
(tablo)

## Top 20 Oncelikli Aksiyonlar
| # | Aksiyon | Kategori | Etki | Efor | Oncelik |
(tablo — kategoriler arasi, etki/efor matrisine gore siralanmis)

## Cross-Cutting Insights
- Kategoriler arasi baglanti ve sinerjiler

## Kategori Detaylari
→ Her kategori icin ozet + link

## Methodology & Cost Report
| Kategori | Model | Baslangic | Bitis | Sure (dk) | Tool Call | Input Token | Output Token | Toplam Token | Maliyet ($) | Toplama Orani (%) |
|----------|-------|-----------|-------|-----------|-----------|-------------|--------------|--------------|-------------|-------------------|
(her agent bir satir)

- **Toplam sure:** X dk
- **Toplam token:** X (input: X, output: X)
- **Toplam tahmini maliyet:** $X
- **En pahali kategori:** ...
- **En verimli kategori (puan/token):** ...
- **Notlar:** Gelecek analizler icin hangi kategoriler Sonnet'e dusurulebilir, hangilerinde Opus fark yaratti
```

### 6. Cikti

Kullaniciya goster:
1. Master rapor ozeti
2. Dosya konumlari
3. En kritik 5 aksiyon

---

## Dosya Yapisi

```
[PROJE]/
  analysis/
    MASTER_ANALYSIS.md          ← Birlestirilmis master rapor
    01_ui_ux_design.md
    02_performance.md
    03_seo.md
    04_data_scraping.md
    05_monetization.md
    06_growth_engagement.md
    07_security_infrastructure.md
    08_content_strategy.md
    09_analytics_tracking.md
    10_architecture_code.md
    11_accessibility.md
    12_competitive_analysis.md
```

---

## Notlar

- Her agent bagimsiz calisir, birbirini beklemez
- Agent sayisi secilen kategori sayisina esittir (max 12)
- Master rapor icin ayri bir Opus agent kullanilir (birlesim + cross-cutting)
- Toplam sure: ~2-5 dakika (paralel agent'lar)
- Projeye ozel icerik otomatik tespit edilir (framework, dil, stack)
- Bu dosya (`PROJECT_ANALYSIS.md`) parent folder'da durur, tum projeler icin gecerlidir
- Analiz ciktilari her zaman projenin kendi `analysis/` folder'inda olusturulur
