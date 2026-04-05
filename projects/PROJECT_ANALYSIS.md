# Project Analysis — Multi-Agent Deep Audit

Bu dosya herhangi bir projede `/project-analysis` komutuyla tetiklenir. Lead hiyerarşisi içinde uzman agent'lar paralel olarak projeyi analiz eder, sonuçları tek bir master raporda birleştirir.

---

## §1 — Analiz Kategorileri

| # | Kategori | Odak | Varsayılan Agent |
|---|----------|------|-----------------|
| 1 | **UI/UX & Design** | Görsel tasarım, layout, renk, tipografi, responsive, dark mode, animasyon, component tutarlılığı, design system, mobile UX | B3 Frontend Coder (Sonnet) |
| 2 | **Performance & Core Web Vitals** | LCP, FID, CLS, bundle size, lazy loading, image optimization, caching, SSR/SSG/ISR, DB sorgu, API response time | B12 Performance Optimizer (Sonnet) |
| 3 | **SEO & Discoverability** | Meta tags, Open Graph, JSON-LD, sitemap, robots.txt, canonical URL, semantic HTML, mobile-friendliness, internal linking | H2 SEO Agent (Haiku) |
| 4 | **Data & Scraping Infrastructure** | Veri kaynakları, scraper mimarisi, veri kalitesi, pipeline robustness, error handling, rate limiting, veri modeli | F1 Data Analyst + F4 ETL Pipeline (Sonnet) |
| 5 | **Monetization & Business Model** | Gelir modelleri, pricing stratejisi, conversion funnel, paywall, freemium vs premium, affiliate | H5 Revenue Analyst + H6 Pricing Strategist (Opus) |
| 6 | **Growth & User Engagement** | Viral loop, gamification, social sharing, retention, onboarding, referral, push notification | H4 Social Media Agent + H8 Newsletter Agent (Sonnet) |
| 7 | **Security & Infrastructure** | Auth, OWASP top 10, env/secret yönetimi, CORS, rate limiting, input validation, dependency audit | B13 Security Auditor (Opus) |
| 8 | **Content & Editorial Strategy** | İçerik kalitesi, çeşitlilik, editorial flow, UGC, moderation, tone of voice | H7 Content Repurposer (Haiku) |
| 9 | **Analytics & Tracking** | Event tracking, conversion, funnel analizi, A/B test altyapısı, KPI tanımlar | M4 Analytics Agent + F1 Data Analyst (Sonnet) |
| 10 | **Architecture & Code Quality** | Kod yapısı, modülerlik, test coverage, CI/CD, tech debt, scalability, type safety | B1 Backend Architect + B10 Refactor Agent (Opus) |
| 11 | **Accessibility (a11y)** | WCAG 2.1/2.2, keyboard navigation, screen reader, color contrast, focus, ARIA, form labels | B3 Frontend Coder (Haiku) |
| 12 | **Competitive Analysis** | Rakip platformlar, feature gap, pazar konumlandırma, diferansiasyon, SWOT, benchmark | H3 Competitor Analyst (Sonnet) |

---

## §2 — Lead Hiyerarşisi

```
A1 Lead Orchestrator (Opus)
├── ArtLead    → #1 UI/UX, #8 Content, #11 Accessibility
├── CodeLead   → #2 Performance, #4 Data, #10 Architecture
├── GrowthLead → #3 SEO, #6 Growth, #9 Analytics
├── BizLead    → #5 Monetization, #12 Competitive
└── SecLead    → #7 Security
```

### Lead sorumlulukları

Her Lead agent:
1. Atanan kategorileri **paralel** olarak çalıştırır (her kategori için ayrı sub-task)
2. Kendi departman kategorilerini analiz eder (worker agent rolünü de üstlenir)
3. Tamamlanan kategori raporlarını `analysis/` klasörüne yazar
4. Lead Orchestrator'a kısa bir departman özeti döner

---

## §3 — Agent Atama Modları

### Mod 1: Lead Orchestrator (Önerilen)

A1 Lead Orchestrator şu adımları izler:
1. `__PROJECT_ROOT__` dizinini tarar (max 10 tool call)
2. Her Lead için atama kararı verir:
   ```json
   {
     "ArtLead": {
       "categories": [1, 8, 11],
       "agents": { "1": "B3/Sonnet", "8": "H7/Haiku", "11": "B3/Haiku" },
       "skip": []
     },
     "CodeLead": { ... },
     "GrowthLead": { ... },
     "BizLead": { ... },
     "SecLead": { ... }
   }
   ```
3. Kullanıcıya haritayı göster, onay al
4. Lead'leri paralel başlat

**Karar kriterleri:**
- Yeni/küçük proje → SEO, Competitive, Monetization'ı atla veya Haiku'ya düşür
- Scraper/veri altyapısı yoksa → #4 atla
- Frontend-only proje → #4, #7 backend parçalarını kısalt
- Mimari/güvenlik/rekabet → Opus; orta → Sonnet; UI tarama/içerik → Haiku

### Mod 2: Manuel

Her kategori için kullanıcıya sırayla sor:
```
[KATEGORİ_ADI] — [kısa açıklama]
1) Evet (tam analiz)  2) Hayır (atla)  3) Kısmen (hızlı tarama)
```
Kabul edilen her kategori için önerilen agent'ı göster, kullanıcı değiştirebilir.

### Mod 3: Hızlı

Tüm 12 kategori, §1'deki varsayılan agent'lar ile başlatılır. Kullanıcıdan onay gerekmez.

---

## §4 — Agent Registry (Proje Analizi Kapsamı)

Kullanılabilir agent'lar ve rolleri:

| Agent ID | İsim | Model | Kategori |
|----------|------|-------|----------|
| B1 | Backend Architect | Opus | Architecture (#10) |
| B3 | Frontend Coder | Sonnet | UI/UX (#1), Accessibility (#11) |
| B10 | Refactor Agent | Sonnet | Architecture (#10) |
| B12 | Performance Optimizer | Sonnet | Performance (#2) |
| B13 | Security Auditor | Opus | Security (#7) |
| F1 | Data Analyst | Sonnet | Data (#4), Analytics (#9) |
| F4 | ETL Pipeline Agent | Sonnet | Data (#4) |
| H2 | SEO Agent | Haiku | SEO (#3) |
| H3 | Competitor Analyst | Sonnet | Competitive (#12) |
| H4 | Social Media Agent | Sonnet | Growth (#6) |
| H5 | Revenue Analyst | Opus | Monetization (#5) |
| H6 | Pricing Strategist | Sonnet | Monetization (#5) |
| H7 | Content Repurposer | Haiku | Content (#8) |
| H8 | Newsletter Agent | Haiku | Growth (#6) |
| M4 | Analytics Agent | Sonnet | Analytics (#9) |

---

## §5 — Lead Agent Prompt Şablonu

```
(Model Adı)
Sen [LEAD_ROLE]'sın. Aşağıdaki projeyi sorumlu olduğun kategorilerde analiz et.

Proje kökü: [PROJE_YOLU]
Sorumlu kategoriler: [KATEGORİ_LİSTESİ]
Atanan agent'lar: [AGENT_ATAMALARI]

## GÖREV

Her kategori için sırayla şu adımları uygula:

### 1. PROJE TARAMASI (Read, Grep, Glob — max 15 tool call)
- Proje yapısını incele
- Kategoriye ilgili dosyaları bul ve oku
- Mevcut durumu değerlendir

### 2. DIŞ DÜNYA ARAŞTIRMASI (WebSearch, WebFetch — max 10 tool call)
- Güncel best practice'leri araştır
- Rakip/benchmark örneklerini bul

### 3. RAPOR OLUŞTUR → [PROJE_YOLU]/analysis/[NN_kategori].md

Rapor formatı:

## [KATEGORİ] Analiz Raporu
> Lead: [LEAD_ROLE] | Agent: [AGENT_ID] | Model: [MODEL]

### Mevcut Durum
- Ne yapılmış (güçlü yanlar)
- Puan: X/10

### Kritik Eksikler (hemen yapılmalı)
| # | Sorun | Etki | Çözüm | Efor |
(tablo)

### İyileştirme Önerileri (planlı)
| # | Öneri | Etki | Çözüm | Efor |
(tablo)

### Kesin Olmalı (industry standard)
### Kesin Değişmeli (mevcut sorunlar)
### Nice-to-Have (diferansiasyon)
### Referanslar

## KURALLAR
- Kod yazma, dosya düzenleme YAPMA — sadece oku ve raporla
- Somut, actionable öneriler sun
- Her öneri için etki (High/Med/Low) ve efor (S/M/L/XL) belirt
- Raporu Türkçe yaz
- Tüm kategorileri bitirdikten sonra Lead Orchestrator'a departman özeti döndür
```

---

## §6 — Master Rapor Yapısı

Tüm Lead'ler tamamlandığında bir **Opus agent** başlatılır:

```markdown
# [Proje Adı] — Master Analysis Report
> Generated: [tarih] | Leads: 5 | Categories: [N] | Mode: [mod]

## Executive Summary
- Genel puan: X/10
- En güçlü alan: ...
- En zayıf alan: ...
- Acil aksiyon sayısı: N

## Puan Kartı
| Kategori | Lead | Agent | Model | Puan | Kritik | İyileştirme |
(tablo)

## Departman Özetleri
### ArtLead (UI/UX, Content, Accessibility)
### CodeLead (Performance, Data, Architecture)
### GrowthLead (SEO, Growth, Analytics)
### BizLead (Monetization, Competitive)
### SecLead (Security)

## Top 20 Öncelikli Aksiyonlar
| # | Aksiyon | Kategori | Lead | Etki | Efor | Öncelik |
(tablo — kategoriler arası, etki/efor matrisine göre sıralanmış)

## Cross-Cutting Insights
- Kategoriler arası bağlantı ve sinerjiler

## Methodology & Cost Report
| Kategori | Lead | Agent | Model | Süre (dk) | Tool Call | Token | Maliyet ($) |
(her kategori bir satır)

- **Toplam süre:** X dk
- **Toplam tahmini maliyet:** $X
- **En pahalı kategori:** ...
- **En verimli kategori (puan/token):** ...
```

---

## §7 — Dosya Yapısı

```
[PROJE]/
  analysis/
    MASTER_ANALYSIS.md
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

- Lead'ler paralel çalışır; her Lead kendi kategorilerini sırayla işler
- Master rapor için ayrı bir Opus agent kullanılır
- Toplam süre: ~3-7 dakika (5 paralel Lead)
- Projeye özgü içerik otomatik tespit edilir (framework, dil, stack)
- Bu dosya tüm projeler için geçerlidir; analiz çıktıları her projenin `analysis/` klasörüne yazılır
