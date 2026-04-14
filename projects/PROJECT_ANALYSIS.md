# Project Analysis — Multi-Agent Deep Audit

Bu dosya herhangi bir projede `/project-analysis` komutuyla tetiklenir. Lead hiyerarşisi içinde uzman agent'lar paralel olarak projeyi analiz eder, sonuçları tek bir master raporda birleştirir.

---

## §0 — Discovery Mode (Boş / Yeni Proje)

Bu mod, proje dizininde kaynak kod bulunmadığında otomatik tetiklenir. **A14 DiscoveryAgent** bilgi eksikliklerini tespit edip yalnızca eksik olanları sorar, `project-brief.md` oluşturur.

### A14 DiscoveryAgent — Adaptif Soru Akışı

**Önce kaynaklardan topla:** README, CLAUDE.md, project-brief.md, sohbet geçmişi, mevcut dosyalar.

Aşağıdaki 8 alanı kontrol et. Her alan için: bilgi varsa atla, yoksa sor.

| # | Alan | Kontrol et |
|---|------|-----------|
| 1 | Platform | Web/mobil/desktop/API |
| 2 | Kullanıcı tipi | B2C/B2B/internal/open source |
| 3 | Tek cümlelik tanım | Ne yapıyor? |
| 4 | Hedef kitle | Kim, kaç kişi? |
| 5 | Monetizasyon | Freemium/subscription/ücretsiz |
| 6 | Auth | Login var mı, nasıl? |
| 7 | Ölçek | Kullanıcı sayısı hedefi |
| 8 | Tech stack tercihi | Var mı, yoksa tavsiye mi? |

**Kural:** Bilinen alanlar için soru sorma. Sadece eksik/belirsiz alanları sor.
Tüm bilgi mevcutsa → direkt `project-brief.md` yaz, soru sorma.
Sorular varsa → hepsini tek mesajda, şıklı, numara ile sor.

### project-brief.md Çıktı Formatı

```markdown
# [Proje Adı] — Project Brief
> Oluşturuldu: [tarih] | A14 DiscoveryAgent

## Özet
[Tek cümle]

## Platform & Hedef Kitle
- Platform: [seçim]
- Kullanıcı tipi: [seçim]
- Hedef kitle: [cevap]
- Ölçek: [seçim]

## Özellikler & Kapsam
[Kullanıcının tanımından çıkarılan özellikler]

## Monetizasyon
[seçim + notlar]

## Auth & Veri
[seçim + notlar]

## Tech Tercihi
[seçim — varsa belirtilmiş stack, yoksa "belirsiz — TechLead önerecek"]

## Açık Sorular
[Cevaplardan çıkan belirsizlikler — TechLead veya geliştirme sırasında netleştirilecek]
```

### A15 TechLead Çalışma Akışı

`project-brief.md` okunduktan sonra:

1. **Stack araştırması** — WebSearch ile brief'e uygun güncel seçenekleri araştır
2. **Karar matrisi** oluştur:

```markdown
# [Proje Adı] — Tech Stack Kararı
> A15 TechLead | [tarih]

## Önerilen Stack

| Katman | Teknoloji | Neden | Ücretsiz Tier |
|--------|-----------|-------|---------------|
| Frontend | Flutter | Cross-platform, tek codebase | — |
| Backend | Firebase | Auth + DB + Storage | Spark plan ücretsiz |
| Hosting | Vercel | Web deploy | Ücretsiz |
| AI/API | Groq | Ücretsiz free tier | Ücretsiz tier mevcut |
| CI/CD | GitHub Actions | — | Ücretsiz |

## Alternatifler
[Her katman için 1-2 alternatif + trade-off]

## Maliyet Projeksiyonu
| Aşama | Aylık Maliyet | Not |
|-------|--------------|-----|
| MVP (0-100 kullanıcı) | $0 | Tüm free tier'lar |
| Büyüme (1K kullanıcı) | $XX | Firebase upgrade |
| Scale (10K+) | $XXX | ... |

## Kurulum Sırası
1. [adım]
2. [adım]
...
```

---

## §1 — Analiz Kategorileri

> **Model notu:** Agent'ların `primary_model`'i artık çoğunlukla `gpt-5.4` (Codex CLI üzerinden). Analiz sırasında Lead Orchestrator aşağıdaki "Analiz Modeli" kolonundaki modeli atar. Claude Code sub-agent'lar `sonnet` veya `opus` kullanır; GPT tabanlı agent'lar Codex CLI ile çalışır.

| # | Kategori | Odak | Worker Agent(lar) | Analiz Modeli |
|---|----------|------|-------------------|---------------|
| 1 | **UI/UX & Design** | Görsel tasarım, layout, renk, tipografi, responsive, dark mode, animasyon, component tutarlılığı, design system, mobile UX | B3 Frontend Coder, D1 UI/UX Researcher, D2 Design System Agent, D8 Mockup Reviewer | gpt-5.4 (Codex CLI) |
| 2 | **Performance & Core Web Vitals** | LCP, FID, CLS, bundle size, lazy loading, image optimization, caching, SSR/SSG/ISR, DB sorgu, API response time | B12 Performance Optimizer | gpt-5.4 (Codex CLI) |
| 3 | **SEO & Discoverability** | Meta tags, Open Graph, JSON-LD, sitemap, robots.txt, canonical URL, semantic HTML, mobile-friendliness, internal linking | H5 SEO Agent | gpt-5.4 (Codex CLI) |
| 4 | **Data & Scraping Infrastructure** | Veri kaynakları, scraper mimarisi, veri kalitesi, pipeline robustness, error handling, rate limiting, veri modeli | F2 Data Analyst, F4 ETL Pipeline Agent | gpt-5.4 (Codex CLI) |
| 5 | **Monetization & Business Model** | Gelir modelleri, pricing stratejisi, conversion funnel, paywall, freemium vs premium, affiliate | H3 Revenue Analyst, H4 Pricing Strategist | gpt-5.4 (Codex CLI) |
| 6 | **Growth & User Engagement** | Viral loop, gamification, social sharing, retention, onboarding, referral, push notification | H7 Social Media Agent, H9 Newsletter Agent | gpt-5.4 (Codex CLI) |
| 7 | **Security & Infrastructure** | Auth, OWASP top 10, env/secret yönetimi, CORS, rate limiting, input validation, dependency audit, SAST | B13 Security Auditor, C2 Security Scanner Hook | Opus |
| 8 | **Content & Editorial Strategy** | İçerik kalitesi, çeşitlilik, editorial flow, UGC, moderation, tone of voice | H8 Content Repurposer | gpt-5.4 (Codex CLI) |
| 9 | **Analytics & Tracking** | Event tracking, conversion, funnel analizi, A/B test altyapısı, KPI tanımlar | M3 A/B Test Agent, M4 Analytics Agent, F2 Data Analyst | gpt-5.4 (Codex CLI) |
| 10 | **Architecture & Code Quality** | Kod yapısı, modülerlik, test coverage, CI/CD, tech debt, scalability, type safety | B1 Backend Architect, B8 Refactor Agent, B10 Dependency Manager | Opus |
| 11 | **Accessibility (a11y)** | WCAG 2.1/2.2, keyboard navigation, screen reader, color contrast, focus, ARIA, form labels | D8 Mockup Reviewer, B3 Frontend Coder | gpt-5.4 (Codex CLI) |
| 12 | **Competitive Analysis** | Rakip platformlar, feature gap, pazar konumlandırma, diferansiasyon, SWOT, benchmark | H2 Competitor Analyst, K1 Web Researcher, K4 Trend Analyzer | gpt-5.4 (Codex CLI) |

---

## §2 — Lead Hiyerarşisi

```
A1 Lead Orchestrator (Opus)
│
├── [PRE-ANALYSIS] ──────────────────────────────────────
│   ├── A14 DiscoveryAgent  → Boş proje tespiti + brief
│   └── A15 TechLead        → Tech stack kararı
│
├── A9  ArtLead    → #1 UI/UX, #8 Content, #11 Accessibility
│   └── dispatches: B3, D1, D2, D8, H8
│
├── A10 CodeLead   → #2 Performance, #4 Data, #10 Architecture
│   └── dispatches: B1, B8, B10, B12, F2, F4
│
├── A11 GrowthLead → #3 SEO, #6 Growth, #9 Analytics
│   └── dispatches: H5, H7, H9, M3, M4, F2
│
├── A12 BizLead    → #5 Monetization, #12 Competitive
│   └── dispatches: H1, H2, H3, H4, K1, K4
│
└── A13 SecLead    → #7 Security
    └── dispatches: B13, C2
```

> **NOT:** "dispatches" ifadesi ayrı bir process başlatmayı değil,
> Lead'in o worker rolünün bakış açısıyla analiz yapmasını ifade eder.
> Her Lead kendi kategorilerini §5 şablonuna göre **BİZZAT** analiz eder —
> ayrı bir agent veya sub-process başlatmaz.

```
```

### Lead sorumlulukları

Her Lead agent:
1. Atanan kategorileri **sırayla** analiz eder (her kategori için ayrı sub-task)
2. Kendi departman kategorilerini worker agent rolünde çalıştırır
3. Tamamlanan kategori raporlarını `analysis/` klasörüne yazar
4. Lead Orchestrator'a kısa bir departman özeti döndürür

### Model override kuralı

Agent'ların kendi `primary_model`'i analiz bağlamında geçersizdir. Lead Orchestrator (veya kullanıcı seçimi), her kategori için §1'deki "Analiz Modeli" kolonundaki minimum modeli atar. Kota modu `Tasarruf` ise Opus → Sonnet'e düşebilir; `Kritik` ise Opus → yalnızca SecLead için kalır (tier_override).

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
       "workers": { "1": "B3+D1/Sonnet", "8": "H8/Haiku", "11": "B3/Haiku" },
       "skip": [],
       "reason": "Frontend ağırlıklı proje, UI/UX tam analiz gerekli"
     },
     "CodeLead": {
       "categories": [2, 10],
       "workers": { "2": "B12/Sonnet", "10": "B1+B8/Opus" },
       "skip": [4],
       "reason": "#4 atlandı: scraper/veri altyapısı yok"
     }
   }
   ```
3. Kullanıcıya haritayı göster, onay al
4. Lead'leri paralel başlat

**Karar kriterleri:**
- Yeni/küçük proje → SEO, Competitive, Monetization'ı atla veya Haiku'ya düşür
- Scraper/veri altyapısı yoksa → #4 atla
- Frontend-only proje → #4, #7 backend parçalarını kısalt
- Mimari/güvenlik → Opus; orta → Sonnet; tarama/içerik → Haiku

### Mod 2: Manuel

Her kategori için kullanıcıya sırayla sor:
```
[KATEGORİ_ADI] — [kısa açıklama]
1) Evet (tam analiz)  2) Hayır (atla)  3) Kısmen (hızlı tarama)
```
Kabul edilen her kategori için §1'deki varsayılan agent'ı göster, kullanıcı değiştirebilir:
```
#1 UI/UX → Varsayılan: B3 + D1 (Sonnet). Değiştir? (enter=varsayılan)
```

### Mod 3: Hızlı

Tüm 12 kategori, §1'deki varsayılan agent'lar ve analiz modelleriyle başlatılır. Kullanıcıdan onay gerekmez.

---

## §4 — Agent Registry (Proje Analizi Kapsamı)

**Model Mapping — Registry → Claude Code:**

> Agent'ların `primary_model`'i artık `gpt-5.4` (Codex CLI üzerinden). Eski modeller (`free-gemini`, `local-qwen-9b`, `free-script` vb.) `primary_model_legacy` olarak saklanıyor. Analiz sırasında `gpt-5.4` kullanılır; erişilemezse Claude Code modelleri (`sonnet`/`haiku`) fallback olur.

| Registry Modeli | Çalışma Yöntemi | Notlar |
|---|---|---|
| `gpt-5.4` | Codex CLI | Tüm worker agent'ların birincil modeli — ChatGPT Pro aboneliği ile |
| `gpt-5.4-mini` | Codex CLI | Hafif işler için (script, deterministic tarama) |
| `opus` | Claude Code native | Security (#7), Architecture (#10) — değişmedi |
| `sonnet` | Claude Code native | Fallback model — Codex CLI ulaşılamazsa |
| `haiku` | Claude Code native | Minimum fallback |

| Agent ID | İsim | Primary Model | Analiz Modeli | Kategori |
|----------|------|--------------|---------------|----------|
| A14 | Discovery Agent | gpt-5.4 | gpt-5.4 | §0 Discovery |
| A15 | TechLead | gpt-5.4 | gpt-5.4 | §0 Tech Stack |
| B1 | Backend Architect | opus | Opus | #10 Architecture |
| B3 | Frontend Coder | gpt-5.4 | gpt-5.4 | #1 UI/UX, #11 Accessibility |
| B8 | Refactor Agent | gpt-5.4 | Opus | #10 Architecture |
| B12 | Performance Optimizer | gpt-5.4 | gpt-5.4 | #2 Performance |
| B10 | Dependency Manager | gpt-5.4 | gpt-5.4 | #10 Architecture |
| B13 | Security Auditor | gpt-5.4 | Opus | #7 Security |
| C2 | Security Scanner Hook | gpt-5.4 | gpt-5.4-mini | #7 Security |
| D1 | UI/UX Researcher | gpt-5.4 | gpt-5.4 | #1 UI/UX |
| D2 | Design System Agent | gpt-5.4 | gpt-5.4 | #1 UI/UX |
| D8 | Mockup Reviewer | gpt-5.4 | gpt-5.4 | #1 UI/UX, #11 Accessibility |
| F2 | Data Analyst | gpt-5.4 | gpt-5.4 | #4 Data, #9 Analytics |
| F4 | ETL Pipeline Agent | gpt-5.4 | gpt-5.4 | #4 Data |
| H1 | Market Researcher | gpt-5.4 | gpt-5.4 | #12 Competitive |
| H2 | Competitor Analyst | gpt-5.4 | gpt-5.4 | #12 Competitive |
| H3 | Revenue Analyst | gpt-5.4 | gpt-5.4 | #5 Monetization |
| H4 | Pricing Strategist | gpt-5.4 | gpt-5.4 | #5 Monetization |
| H5 | SEO Agent | gpt-5.4 | gpt-5.4 | #3 SEO |
| H7 | Social Media Agent | gpt-5.4 | gpt-5.4 | #6 Growth |
| H8 | Content Repurposer | gpt-5.4 | gpt-5.4 | #8 Content |
| H9 | Newsletter Agent | gpt-5.4 | gpt-5.4 | #6 Growth |
| K1 | Web Researcher | gpt-5.4 | gpt-5.4 | #12 Competitive |
| K4 | Trend Analyzer | gpt-5.4 | gpt-5.4 | #12 Competitive |
| M3 | A/B Test Agent | gpt-5.4 | gpt-5.4-mini | #9 Analytics |
| M4 | Analytics Agent | gpt-5.4 | gpt-5.4-mini | #9 Analytics |

> **"Analiz Modeli"** = project-analysis çalışırken bu agent'a atanacak model. Opus kategorileri (#7, #10) değişmedi; geri kalan tüm worker'lar `gpt-5.4` kullanır.

---

## §5 — Lead Agent Prompt Şablonu

```
(Model Adı)
Sen [LEAD_ROLE]'sın. Aşağıdaki projeyi sorumlu olduğun kategorilerde analiz et.

Proje kökü: [PROJE_YOLU]
Sorumlu kategoriler: [KATEGORİ_LİSTESİ]
Atanan worker agent'lar: [AGENT_ATAMALARI]

## GÖREV

Her kategori için sırayla şu adımları uygula:

### 1. PROJE TARAMASI (Read, Grep, Glob — max 15 tool call / kategori)
- Proje yapısını incele
- Kategoriye ilgili dosyaları bul ve oku
- Mevcut durumu değerlendir

### 2. DIŞ DÜNYA ARAŞTIRMASI (WebSearch, WebFetch — max 10 tool call / kategori)
- Güncel best practice'leri araştır
- Rakip/benchmark örneklerini bul

### 3. RAPOR OLUŞTUR → [PROJE_YOLU]/analysis/[NN_kategori].md

Rapor formatı:

## [KATEGORİ] Analiz Raporu
> Lead: [LEAD_ROLE] | Worker: [AGENT_ID] [AGENT_NAME] | Model: [MODEL]

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

## MODEL DISPATCH KURALLARI
- `model: gpt-5.4` → Codex CLI üzerinden çalışır
- `model: gpt-5.4-mini` → Hafif tarama/script işleri için Codex CLI
- `model: opus` / `sonnet` / `haiku` → Claude Code native sub-agent
- Codex CLI ulaşılamazsa → `sonnet` fallback olarak kullanılır

## KURALLAR
- Kod yazma, dosya düzenleme YAPMA — sadece oku ve raporla
- Somut, actionable öneriler sun
- Her öneri için etki (High/Med/Low) ve efor (S/M/L/XL) belirt
- Raporu Türkçe yaz
- Tüm kategorileri bitirdikten sonra Lead Orchestrator'a departman özeti döndür

## DEPARTMAN ÖZETİ FORMATI
Tüm kategorilerin tamamlanınca döndür:
[LEAD_ROLE] Departman Özeti:
- #[N] [Kategori]: X/10 — [1 cümle]
- ...
Kritik bulgular: [en önemli 2-3 madde]
Cross-departman not: [başka Lead'in ilgi alanına giren tespit varsa belirt]
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
| Kategori | Lead | Worker Agent | Model | Puan | Kritik | İyileştirme |
(tablo)

## Departman Özetleri
### A9 ArtLead (UI/UX, Content, Accessibility)
### A10 CodeLead (Performance, Data, Architecture)
### A11 GrowthLead (SEO, Growth, Analytics)
### A12 BizLead (Monetization, Competitive)
### A13 SecLead (Security)

## Top 20 Öncelikli Aksiyonlar
| # | Aksiyon | Kategori | Lead | Etki | Efor | Öncelik |
(tablo — kategoriler arası, etki/efor matrisine göre sıralanmış)

## Cross-Cutting Insights
- Cross-departman notlardan derlenen kategoriler arası bağlantılar
- Lead'lerin birbirlerine eskalasyon notları

## Methodology & Cost Report
| Kategori | Lead | Worker | Model | Süre (dk) | Tool Call | Token | Maliyet ($) |
(her kategori bir satır)

- **Toplam süre:** X dk
- **Toplam tahmini maliyet:** $X
- **En pahalı kategori:** ...
- **En verimli kategori (puan/token):** ...
- **Model override notları:** Hangi agent'lar yükseltildi, neden
```

---

## §7 — Agent Erişilebilirlik & Fallback Protokolü

> Bu protokol, Lead'ler başlatılmadan **önce** çalışır. Her "free" veya "local" model tipi için erişilebilirlik kontrol edilir; ulaşılamazsa kullanıcıya seçenek sunulur.

### Kontrol Adımları (Analiz başlamadan önce)

`scripts/check-agent-availability.sh` çalıştır. Çıktıdaki `UNAVAILABLE:` satırlarını işle.

Her ulaşılamayan agent tipi için kullanıcıya şunu göster:

```
⚠️  [AGENT_ID] [AGENT_NAME] — model: [MODEL_TIPI] ulaşılamıyor.

Ne yapalım?
  1) Kurulum yap   — [MODEL_TIPI için kurulum talimatı]
  2) Alternatif kullan — [FALLBACK_MODEL] ile devam et
  3) Bu agent'ı atla — kategori [#N] analiz edilmez
  4) Tüm ulaşılamazlar için [2] uygula (bu oturum için)

Seçiminiz (1/2/3/4):
```

### Model Tipi → Kontrol & Fallback Tablosu

| Model Tipi | Kontrol Yöntemi | Kurulum Talimatı | Fallback Modeli |
|---|---|---|---|
| `gpt-5.4` | Codex CLI login check | `codex login` ile giriş yap | `sonnet` |
| `gpt-5.4-mini` | Codex CLI login check | Aynı oturum ile çalışır | `haiku` |
| `opus` / `sonnet` / `haiku` | Claude Code native — her zaman mevcut | — | — |
| `free-web` | Herhangi bir URL fetch başarılı mı? | MCP fetch server aktif mi? (`/mcp` ile kontrol) | `haiku` |

### Kullanıcı Seçim Sonuçları

| Seçim | Aksiyon |
|---|---|
| **1 — Kurulum yap** | Talimatı kullanıcıya göster, kurulum tamamlanınca yeniden kontrol et |
| **2 — Alternatif kullan** | Agent'ın modelini fallback ile override et, analizi başlat |
| **3 — Bu agent'ı atla** | Agent'ın kategorisi `skip` listesine eklenir, Lead atama haritasında gösterilir |
| **4 — Tümüne alternatif** | Oturum boyunca tüm ulaşılamayan agent'lar fallback modelle çalışır, onay sorulmaz |

### Atama Haritasında Gösterim

Ulaşılamayan agent'lar Lead Orchestrator haritasında işaretlenir:

```
ArtLead — #1 UI/UX:
  B3 Frontend Coder   → Sonnet ✅
  D1 UI/UX Researcher → free-gemini ❌ → sonnet (fallback, kullanıcı onaylı)
  D2 Design System    → Haiku ✅
```

---

## §8 — Dosya Yapısı

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
- Agent'ların "Kendi Modeli" ile "Analiz Modeli" farklıdır — §4'teki tabloya bak
