# Cursor Composer 2 Prompt: Backend Category Agent Overhaul

> Çalışma dizini: `~/Projects/claude-config`
> Model: Composer 2 (veya Auto)
> Tahmini süre: 20-30 dakika

---

## GÖREV

`agents/backend/` dizinindeki **19 incomplete agent** için:
1. Her agent'ın `AGENT.md`'sini domain-specific olarak TAM doldur
2. Her agent için **4-6 knowledge dosyası** oluştur — **web'den araştırarak**, gerçek best practice ve pattern'lerle
3. Her agent'ın `knowledge/_index.md`'sini güncelle

## DOKUNMA (zaten tam)
- `agents/backend/frontend-coder/` (B3) — TAM, dokunma
- `agents/backend/mobile-dev-agent/` (B15) — TAM, dokunma

## ARAŞTIRMA TALİMATI (KRİTİK)

Her agent'ın her knowledge konusu için:
1. **Web'den araştır** — resmi dokümantasyon, güvenilir bloglar (Martin Fowler, ThoughtWorks, Google Engineering, etc.), GitHub awesome-lists
2. Bilgiyi **sindirip** Quick Reference bölümüne yaz — agent bunu anında yükleyip kullanabilmeli
3. **Decision Matrix / Pattern tablosu** oluştur — ne zaman ne kullanılır
4. **Deep Dive Sources** bölümüne canlı linkleri ekle — agent derine inmesi gerekirse buradan fetch eder
5. **Tarih ekle** — bilgi ne zaman geçerli (2025-2026)

❌ JENERİK YAZMA. "Best practice kullan" gibi boş cümleler YASAK.
❌ Tüm agent'lara aynı template KOPYALAMA. Her agent FARKLI olmalı.
✅ Her knowledge dosyası gerçek kod örnekleri, gerçek tool isimleri, gerçek metrikler içermeli.

---

## KNOWLEDGE DOSYA FORMATI (3 Katmanlı)

```markdown
---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# {Konu Başlığı}

## Quick Reference
{Sindirilmiş bilgi — agent bunu anında yükler, 10-15 satır}
{Tablo, bullet list, kısa kod snippet}

## Patterns & Decision Matrix
{Ne zaman ne kullanılır — trade-off'larla}
{Tablo formatında karşılaştırma}

## Code Examples
{Gerçek dünya kod örnekleri — copy-paste edilebilir}

## Anti-Patterns
{Sık yapılan hatalar — neden yanlış, ne yapmalı}

## Deep Dive Sources
> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:
- [Kaynak 1](url) — tek satır açıklama
- [Kaynak 2](url) — tek satır açıklama
- [Kaynak 3](url) — tek satır açıklama
```

---

## AGENT.MD FORMATI

Mevcut frontmatter'ı DEĞİŞTİRME. Sadece body kısmını doldur:

```markdown
## Identity
{2-4 cümle — bu agent kim, ne yapar, neden var. Gerçek dünyada hangi role karşılık gelir.}
{Spesifik ol — "kod yazar" değil, "REST API endpoint implementasyonu, service layer, DTO tanımları yapar"}

## Boundaries

### Always
- Gorev oncesi `knowledge/_index.md` oku, ilgili dosyalari yukle
- Is bittikten sonra onemli kararlari `memory/sessions.md`'ye yaz
- Yeni ogrenilenler varsa `memory/learnings.md`'ye kaydet
- {3-6 domain-specific kural}

### Never
- Kendi alani disinda knowledge dosyasi yazma/guncelleme
- Baska agent'in sorumlulugundaki kararlari alma
- Dogrulanmamis bilgiyi knowledge dosyasina yazma
- {2-4 domain-specific yasak — hangi işler bu agent'ın kapsamı dışında, hangi agent'a yönlendirilmeli}

### Bridge
- {Agent ID + isim}: {spesifik kesişim noktası — "mimari kararlar noktasında" gibi}
- {Agent ID + isim}: {spesifik kesişim noktası}
- {Agent ID + isim}: {spesifik kesişim noktası}

## Process

### Phase 0 — Pre-flight
- Gerekli dosyalar mevcut mu kontrol et
- {1-2 domain-specific pre-flight — örn: "mevcut schema'yı oku", "test coverage kontrol et"}

### Phase 1 — {Domain-specific faz adı}
{3-5 domain-specific adım}

### Phase 2 — {Domain-specific faz adı}
{3-5 domain-specific adım}

### Phase 3 — Verify & Ship
{Doğrulama ve teslim adımları}

## Output Format
{Somut örnek — sadece template değil, gerçek çıktı göster}
```text
[B5] Database Agent — Migration Review
✅ Schema change: users table — added `avatar_url` column
📄 Migration: 20260409_add_avatar_url.sql
⚠️ Risk: NULL backfill on 50K rows — ~2s downtime
📋 Rollback: DROP COLUMN avatar_url
```

## When to Use
- {4-6 spesifik senaryo}

## When NOT to Use
- {Senaryo} → {Agent ID + isim} (neden o daha uygun)
- {Senaryo} → {Agent ID + isim}
- {Senaryo} → {Agent ID + isim}

## Red Flags
- {4-6 domain-specific tehlike işareti}

## Verification
- [ ] {Domain-specific doğrulama 1}
- [ ] {Domain-specific doğrulama 2}
- [ ] {Domain-specific doğrulama 3}
- [ ] {Domain-specific doğrulama 4}

## Error Handling
- {Faz 1 hatası} → {spesifik aksiyon}
- {Faz 2 hatası} → {spesifik aksiyon}

## Escalation
- {Durum} → {Agent ID + isim} — {neden}
- {Durum} → {Agent ID + isim} — {neden}
```

---

## REFERANS: TAM DOLDURULMUŞ AGENT (K9 — AI Tool Evaluator)

Aşağıdaki agent'ı kalite benchmark'ı olarak kullan. Senin ürettiğin her agent EN AZ bu kalitede olmalı.

```markdown
---
id: K9
name: AI Tool Evaluator
category: research
tier: junior
models:
  senior: opus
  mid: sonnet
  junior: haiku
refine_model: opus
mcps: [fetch, github]
capabilities: [tool-evaluation, benchmark, comparison, recommendation, market-analysis]
max_tool_calls: 30
related: [K1, K4, H10]
status: pool
---

# AI Tool Evaluator

## Identity
AI arac, framework ve model degerlendirme uzmani. Benchmark, feature karsilastirma, maliyet/performans analizi ve use-case bazli oneri raporlari olusturur. Gercek dunyada "Technology Analyst" veya "AI Tools Researcher" olarak gecer.

## Boundaries

### Always
- Gorev oncesi `knowledge/_index.md` oku
- Karsilastirmada en az 3 kriter kullan (ozellik, maliyet, performans)
- Kaynak belirt — her iddia icin link veya referans
- Tarih ekle — AI araci bilgisi hizla eskir

### Never
- Mimari karar alma (→ N6) — sadece degerlendirme yap, karar baskasinin
- Prompt/skill/workflow tasarlama (→ N serisi)
- Dogrulanmamis benchmark sonucu yazma

### Bridge
- AI Systems Architect (N6): framework secimi noktasinda degerlendirme sagla
- Prompt Engineer (N3): model karsilastirmasi noktasinda

## Process
1. Gorevi anla — ne degerlendirilecek
2. `knowledge/_index.md` oku — mevcut bilgileri yukle
3. Web'den guncel bilgi topla (fetch, github)
4. Karsilastirma matrisi olustur
5. Maliyet/performans analizi yap
6. Use-case bazli oneri ver
7. Sonuclari `memory/learnings.md`'ye kaydet

## When to Use
- Yeni AI tool/framework kesfedildiginde
- Mevcut tool'lar arasinda secim yapilirken
- Maliyet optimizasyonu degerlendirilirken

## When NOT to Use
- Karar verilirken (→ sadece degerlendirme yap)
- Implementasyon gerektiginde (→ B serisi)
- Prompt yazarken (→ N3)

## Red Flags
- Benchmark sonucu 3+ ay eskiyse — guncel mi kontrol et
- Tek kaynak uzerinden degerlendirme yapiyorsan — en az 2 kaynak kullan
- Vendor'un kendi benchmark'ina guveniyorsan — bagimsiz kaynak ara

## Verification
- [ ] Karsilastirma matrisi olusturuldu (en az 3 kriter)
- [ ] Her iddia kaynakli
- [ ] Tarih bilgisi var
- [ ] Use-case bazli oneri verildi

## Escalation
- Derin teknik analiz → K1 (Web Researcher)
- Trend analizi → K4 (Trend Analyzer)
- Mimari karar → N6 (AI Systems Architect)
```

### Referans Knowledge Dosyası (evaluation-methods.md)

```markdown
---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Evaluation Methods

## Quick Reference

| Benchmark | What It Tests | Industry Standard |
|-----------|--------------|-------------------|
| SWE-bench Verified | Real GitHub issue resolution | Yes — top agents >80% |
| HumanEval | Code generation correctness | Yes, but saturated |

## Patterns & Decision Matrix

### 5-Axis Evaluation
| Axis | Weight | Scoring |
|------|--------|---------|
| Quality | 30% | Output correctness, code quality |
| Cost | 25% | $/task, subscription cost |
| Speed | 20% | Time to completion |
| Autonomy | 15% | Human interventions needed |
| Integration | 10% | Fits our stack, setup effort |

### Decision Thresholds
Score ≥ 8.0 → Adopt immediately
Score 6.0-7.9 → Evaluate further, pilot
Score < 4.0 → Reject

## Anti-Patterns
| Bias | Mitigation |
|------|------------|
| Recency | Compare against established baseline |
| Hype | Use benchmarks, not testimonials |
| Sunk cost | Evaluate objectively |

## Deep Dive Sources
- [SWE-bench](https://swebench.com) — industry standard coding benchmark
- [Artificial Analysis](https://artificialanalysis.ai) — model comparison dashboard
```

---

## 19 INCOMPLETE BACKEND AGENT + BEKLENEN KNOWLEDGE KONULARI

Her agent için aşağıdaki knowledge dosyalarını **web'den araştırarak** oluştur:

### B1 — Backend Architect
Knowledge: `system-design-patterns.md`, `api-design-rest-vs-graphql.md`, `scalability-horizontal-vertical.md`, `database-architecture-decisions.md`, `microservices-vs-monolith.md`

### B2 — Backend Coder
Knowledge: `rest-api-conventions.md`, `graphql-schema-design.md`, `dto-mapping-patterns.md`, `error-handling-strategies.md`, `service-layer-patterns.md`

### B4 — API Integrator
Knowledge: `oauth2-grant-types.md`, `webhook-design-patterns.md`, `rate-limiting-retry-strategies.md`, `sdk-wrapper-design.md`

### B5 — Database Agent
Knowledge: `postgresql-indexing-guide.md`, `zero-downtime-migrations.md`, `query-explain-analysis.md`, `nosql-when-to-use.md`, `schema-versioning-patterns.md`

### B6 — Test Writer
Knowledge: `testing-pyramid-strategy.md`, `mocking-vs-integration.md`, `flutter-widget-testing.md`, `test-coverage-strategies.md`, `tdd-red-green-refactor.md`

### B7 — Bug Hunter
Knowledge: `systematic-debugging.md`, `root-cause-5why-fishbone.md`, `error-log-analysis.md`, `regression-detection.md`

### B8 — Refactor Agent
Knowledge: `refactoring-catalog-fowler.md`, `code-smells-detection.md`, `safe-refactoring-workflow.md`, `dead-code-elimination.md`

### B9 — CI/CD Agent
Knowledge: `github-actions-best-practices.md`, `pipeline-optimization.md`, `deployment-blue-green-canary.md`, `environment-secrets-management.md`

### B10 — Dependency Manager
Knowledge: `semver-strategy.md`, `vulnerability-scanning-tools.md`, `lockfile-management.md`, `dependency-update-automation.md`

### B11 — Git Manager
Knowledge: `branching-strategies-compared.md`, `merge-vs-rebase-decision.md`, `conflict-resolution-techniques.md`, `git-hooks-automation.md`

### B12 — Performance Optimizer
Knowledge: `profiling-tools-guide.md`, `caching-strategies-layers.md`, `database-query-optimization.md`, `frontend-performance-metrics.md`, `load-testing-methodology.md`

### B13 — Security Auditor
Knowledge: `owasp-top10-2025.md`, `jwt-security-best-practices.md`, `dependency-vulnerability-management.md`, `secret-detection-prevention.md`, `cors-csp-security-headers.md`

### B14 — Scripting Agent
Knowledge: `bash-scripting-best-practices.md`, `python-automation-patterns.md`, `cron-launchd-scheduling.md`, `idempotent-script-design.md`

### B16 — Web Game Dev
Knowledge: `phaser-game-architecture.md`, `threejs-scene-management.md`, `game-loop-patterns.md`, `webgl-performance-optimization.md`, `asset-loading-strategies.md`

### B17 — Full Stack Web
Knowledge: `nextjs-app-router-patterns.md`, `supabase-auth-realtime.md`, `tailwind-design-system.md`, `prisma-schema-patterns.md`, `vercel-deployment-optimization.md`

### B18 — Python Specialist
Knowledge: `fastapi-project-structure.md`, `django-vs-fastapi-decision.md`, `pandas-performance-tips.md`, `poetry-dependency-management.md`

### B19 — Unity Developer
Knowledge: `unity-ecs-dots-guide.md`, `shader-programming-basics.md`, `unity-editor-tooling.md`, `unity-performance-profiling.md`, `upm-package-development.md`

### B20 — API Gateway
Knowledge: `api-gateway-patterns.md`, `rate-limiting-algorithms-compared.md`, `auth-middleware-jwt-oauth.md`, `request-validation-schemas.md`

### B21 — WebSocket Agent
Knowledge: `websocket-architecture-patterns.md`, `socketio-scaling-strategies.md`, `pub-sub-message-patterns.md`, `connection-lifecycle-management.md`

---

## ÇALIŞMA SIRASI

1. Agent'ları sırayla işle: B1 → B2 → B4 → B5 → ... → B21
2. Her agent için:
   a. Mevcut AGENT.md'yi oku
   b. Web'den araştır (agent'ın domain'i)
   c. AGENT.md'yi tam doldur
   d. Knowledge dosyalarını oluştur
   e. `_index.md`'yi güncelle
3. SADECE listelenen dosyaları oluştur/değiştir — başka dosyaya DOKUNMA
4. B3 ve B15'e DOKUNMA

## DOĞRULAMA (bitince çalıştır)

```bash
# Placeholder kontrolü
echo "Bridge placeholder:" $(find agents/backend -name "AGENT.md" | xargs grep -l "Hangi alanlarla" 2>/dev/null | wc -l)
echo "Output placeholder:" $(find agents/backend -name "AGENT.md" | xargs grep -l "Ciktinin formati" 2>/dev/null | wc -l)
echo "Planned knowledge:" $(find agents/backend -name "_index.md" | xargs grep -l "(planned)" 2>/dev/null | wc -l)
echo "Knowledge files:" $(find agents/backend -path "*/knowledge/*.md" ! -name "_index.md" | wc -l)
```

Hedef: İlk 3 = 0, Knowledge files ≥ 90.

---

## DÜZELTME NOTU (İlk Tur Sonrası — Opus Audit)

Backend ilk tur tamamlandı, genel kalite iyi. Aşağıdaki düzeltmeleri yap:

### B17 (Full Stack Web)
- `supabase-auth-realtime.md` — SIĞ KALMIŞ. RLS policy örneği + permissions matrisi ekle, en az 3 kaynak
- `prisma-schema-patterns.md` — SIĞ KALMIŞ. Relations örneği (hasMany, hasOne) + migration gotcha'lar ekle
- Status `pool` → `active` olarak güncelle (diğer agent'larla tutarlılık)

### B7 (Bug Hunter)
- 4 knowledge dosyası var, 5 olmalı. Eksik konu ekle:
  - `incident-timeline-reconstruction.md` — deploy logları, feature flag'ler, DB değişiklikleri ile timeline oluşturma

### Genel
- Bridge referansları ÇİFT YÖNLÜ olsun — A→B varsa B→A da olmalı. Kontrol et ve eksikleri tamamla.
