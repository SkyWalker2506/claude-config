# Cursor Mega-Prompt: Agent Knowledge-First Overhaul

> Bu promptu Cursor Composer'a (Agent Mode, Cmd+I) yapıştır. Çalışma dizini: `~/Projects/claude-config`

---

## GÖREV

Bu repodaki `agents/` dizininde 144 AI agent tanımı var. 12 tanesi TAM doldurulmuş, **133 tanesi template kopyası** — placeholder'ları var, knowledge dosyaları oluşturulmamış. Senin görevin:

1. **Her incomplete agent için AGENT.md'yi domain-specific olarak TAM doldur**
2. **Her agent için 3-6 knowledge dosyası oluştur** (domain best practices, patterns, anti-patterns)
3. **Her agent'ın `knowledge/_index.md`'sini güncelle** — "(planned)" satırlarını kaldır, gerçek dosyalara link ver

## KURALLAR

### Dokunma (TAM olan agent'lar)
Bu 12 agent'a ASLA dokunma — zaten tam doldurulmuş:
- `orchestrator/jarvis/` (A0)
- `backend/frontend-coder/` (B3)
- `backend/mobile-dev-agent/` (B15)
- `design/design-system-agent/` (D2)
- `design/motion-graphics-agent/` (D10)
- `design/ui-ux-researcher/` (D1)
- `devops/github-manager/` (J10)
- `research/ai-tool-evaluator/` (K9)
- `prompt-engineering/ai-systems-architect/` (N6)
- `prompt-engineering/prompt-engineer/` (N1)
- `prompt-engineering/skill-design-specialist/` (N7)
- `prompt-engineering/workflow-engineer/` (N8)

### Dil
- AGENT.md içeriği: **Türkçe** (ASCII-safe, özel karakter yok: ı→i, ş→s, ç→c, ğ→g, ü→u, ö→o)
- Knowledge dosyaları: **İngilizce** (teknik referans oldukları için)
- Frontmatter (YAML): İngilizce

### Frontmatter'a Dokunma
Mevcut YAML frontmatter'ı (id, name, category, tier, models, mcps, capabilities, related, status) DEĞİŞTİRME. Sadece body kısmını doldur.

### Kategori Bazlı Çalış
Tüm agent'ları bir anda yapmak yerine **kategori bazlı** ilerle. Sıra:
1. `orchestrator/` (13 agent, 1 tam)
2. `backend/` (21 agent, 2 tam)
3. `code-review/` (6 agent)
4. `design/` (10 agent, 3 tam)
5. `devops/` (10 agent, 1 tam)
6. `data-analytics/` (10 agent)
7. `ai-ops/` (10 agent)
8. `jira-pm/` (10 agent)
9. `research/` (13 agent, 1 tam)
10. `market-research/` (15 agent)
11. `marketing-engine/` (4 agent)
12. `productivity/` (6 agent)
13. `prompt-engineering/` (5 agent, 4 tam)
14. `sales-bizdev/` (5 agent)
15. `3d-cad/` (5 agent)

---

## TEMPLATE

Her incomplete AGENT.md'yi aşağıdaki yapıya göre doldur. `{...}` olan her yeri domain-specific içerikle değiştir.

```markdown
---
(mevcut frontmatter — DEĞİŞTİRME)
---

# {Agent Name}

## Identity
{2-4 cümle — bu agent kim, ne yapar, neden var. Genel değil, SPESIFIK yaz. Gerçek dünyada hangi rol/unvana karşılık gelir ekle.}

## Boundaries

### Always
- Gorev oncesi `knowledge/_index.md` oku, ilgili dosyalari yukle
- Is bittikten sonra onemli kararlari `memory/sessions.md`'ye yaz
- Yeni ogrenilenler varsa `memory/learnings.md`'ye kaydet
- {3-6 domain-specific "her zaman yap" kuralı}

### Never
- Kendi alani disinda knowledge dosyasi yazma/guncelleme
- Baska agent'in sorumlulugundaki kararlari alma
- Dogrulanmamis bilgiyi knowledge dosyasina yazma
- {2-4 domain-specific "asla yapma" kuralı — hangi işler bu agent'ın kapsamı dışında}

### Bridge
- {Agent1 (ID)}: {hangi noktada kesişim — tek cümle}
- {Agent2 (ID)}: {hangi noktada kesişim — tek cümle}
- {Agent3 (ID)}: {hangi noktada kesişim — tek cümle}

## Process

### Phase 0 — Pre-flight
- Gerekli dosyalar mevcut mu kontrol et (AGENT.md, knowledge/_index.md)
- Varsayimlarini listele — sessizce yanlis yola girme
- Eksik veri varsa dur, sor
- {1-2 domain-specific pre-flight check}

### Phase 1 — {İlk faz adı}
{Bu agent'ın işinin ilk aşaması — 3-5 adım}

### Phase 2 — {İkinci faz adı}
{İkinci aşama — 3-5 adım}

### Phase 3 — Finalize
{Son aşama — doğrulama, kayıt, teslim}

## Output Format
{Bu agent ne üretir: dosya, rapor, commit, PR, terminal output, JSON, tablo vb. Kısa örnek göster.}

## When to Use
- {4-6 spesifik kullanım senaryosu}

## When NOT to Use
- {3-5 "bu agent değil, şu agent" yönlendirmesi — ID ile}

## Red Flags
- {4-6 domain-specific tehlike işareti — bu agent yanlış yolda olduğunun göstergeleri}

## Verification
- [ ] {Domain-specific doğrulama 1}
- [ ] {Domain-specific doğrulama 2}
- [ ] {Domain-specific doğrulama 3}
- [ ] {Domain-specific doğrulama 4}

## Error Handling
- {Faz 1 başarısız} → {ne yap}
- {Faz 2 başarısız} → {ne yap}
- {Genel hata} → {fallback veya escalation}

## Escalation
- {Durum 1} → {Agent ID + isim}
- {Durum 2} → {Agent ID + isim}
- {Son çare} → kullaniciya sor

## Knowledge Index
> `knowledge/_index.md` dosyasina bak — ihtiyacin olan konuyu yukle
```

---

## KNOWLEDGE DOSYALARI

Her agent için **3-6 knowledge dosyası** oluştur. Knowledge dosyaları İngilizce, teknik referans niteliğinde.

### Knowledge dosya formatı

```markdown
---
last_updated: 2026-04-09
refined_by: cursor
confidence: medium
---

# {Topic Title}

## {Section 1}
{Best practices, patterns, örnekler — kod snippet'leri dahil}

## {Section 2}
{Anti-patterns, common mistakes}

## {Section 3}
{Decision framework veya checklist}
```

### Knowledge konu seçimi

Agent'ın `capabilities` array'inden ve domain bilgisinden çıkar. Örnekler:

| Agent | Knowledge Dosyaları |
|-------|-------------------|
| Bug Hunter (B7) | `debugging-strategies.md`, `root-cause-analysis.md`, `error-patterns.md`, `regression-testing.md` |
| Database Agent (B5) | `query-optimization.md`, `migration-patterns.md`, `schema-design.md`, `indexing-strategies.md` |
| Sprint Planner (I2) | `capacity-planning.md`, `estimation-techniques.md`, `sprint-anti-patterns.md`, `velocity-tracking.md` |
| SEO Agent (H5) | `technical-seo.md`, `keyword-research.md`, `content-optimization.md`, `structured-data.md` |

### _index.md güncelleme

```markdown
---
last_updated: 2026-04-09
total_topics: {N}
---

# Knowledge Index

- [Topic Title](filename.md) — tek satırlık açıklama
- [Topic Title](filename.md) — tek satırlık açıklama
...
```

`(planned)` satırlarını SİL, gerçek dosya linkleriyle değiştir.

---

## REFERANS AGENT'LAR

Aşağıdaki 3 agent TAM doldurulmuş referans. Kalite ve derinlik seviyesini bunlardan al.

### Referans 1: AI Tool Evaluator (K9) — research/ai-tool-evaluator/

**AGENT.md kalitesi:** Identity 3 cümle, Bridge spesifik agent ID ile, Process domain-specific fazlar, When NOT to Use spesifik yönlendirme, Red Flags domain-specific.

**Knowledge dosyaları (6 adet):**
- `ai-coding-agents.md` — Devin, Cursor, Windsurf, Codex, Claude Code karşılaştırması
- `agent-frameworks.md` — CrewAI, AutoGen, LangGraph, Swarm değerlendirme
- `memory-systems.md` — MemPalace, Mem0, Zep, LangMem karşılaştırması
- `free-models.md` — OpenRouter, Groq, HuggingFace free tier
- `evaluation-methods.md` — benchmark metodolojisi, scoring rubric
- `competing-agent-systems.md` — rakip agent mimarileri karşılaştırması

Her knowledge dosyası 40-80 satır, tablo + kod snippet + karar çerçevesi içerir.

### Referans 2: Frontend Coder (B3) — backend/frontend-coder/

**Knowledge dosyaları (5 adet):**
- `flutter-widget-patterns.md` — composition, separation of concerns, reusable widgets + kod örnekleri
- `state-management.md` — Riverpod, Provider, BLoC karşılaştırma
- `responsive-layout.md` — LayoutBuilder, MediaQuery, adaptive breakpoints
- `component-architecture.md` — atomic design, smart/dumb separation
- `form-patterns.md` — validation, error handling, multi-step forms

### Referans 3: Jarvis (A0) — orchestrator/jarvis/

**Knowledge dosyaları (5 adet):**
- `agent-dispatch-rules.md` — routing tablosu, tier→model eşleme, cascade kuralları
- `project-ecosystem.md` — tüm projeler, tech stack, Jira key'leri
- `user-preferences.md` — çalışma tercihleri, iletişim stili
- `session-management.md` — oturum kontrolleri, context yönetimi
- `cross-project-patterns.md` — ortak tech stack, git kuralları

---

## AGENT ROUTING HARİTASI

Agent'lar arası Bridge ve Escalation yazarken bu haritayı kullan:

### Kategori Prefix'leri
| Prefix | Kategori |
|--------|----------|
| A | Orchestrator & Sistem |
| B | Kod / Backend / Frontend |
| C | Code Review |
| D | Design / 2D |
| E | 3D / CAD |
| F | Data & Analytics |
| G | AI Ops / Workflow |
| H | Market Research & Growth |
| I | Jira & PM |
| J | DevOps & Infrastructure |
| K | Research & Learning |
| L | Productivity |
| M | Marketing Engine |
| N | Prompt Engineering & Agent Design |
| O | Sales & BizDev |

### Kilit Agent'lar (sık referans edilen)
- **A0 Jarvis** — ana orchestrator, tüm session'ların giriş noktası
- **A1 Lead Orchestrator** — stratejik kararlar, proje yönü
- **A2 Task Router** — görev sınıflandırma ve yönlendirme
- **B1 Backend Architect** — mimari kararlar (Opus tier)
- **B2 Backend Coder** — API/CRUD implementasyon
- **B3 Frontend Coder** — React/Flutter UI
- **B13 Security Auditor** — güvenlik denetimi (Opus tier)
- **B15 Mobile Dev** — Flutter mobil geliştirme
- **D2 Design System** — design token, theme
- **I1 Jira Router** — Jira issue yönetimi
- **K1 Web Researcher** — web araştırma
- **N6 AI Systems Architect** — agent mimarisi (Opus tier)

---

## İŞ AKIŞI

1. `agents/_template/AGENT.md` oku — yapıyı anla
2. Referans agent'ları oku — kalite seviyesini anla
3. Kategori kategori ilerle (yukarıdaki sıra)
4. Her agent için:
   a. Mevcut AGENT.md'yi oku
   b. Agent'ın domain'i hakkında **web'den araştırma yap** — best practices, industry standards, common patterns
   c. AGENT.md'yi tam doldur (tüm placeholder'ları kaldır)
   d. 3-6 knowledge dosyası oluştur (İngilizce, teknik, detaylı)
   e. `_index.md`'yi güncelle
5. Her kategori bitince commit at: `docs: overhaul {category} agents — AGENT.md + knowledge`

## KALİTE KRİTERLERİ

- ❌ Placeholder kalmamalı (`{...}`, `(planned)`)
- ❌ Jenerik/template cümle kalmamalı ("Gorev scope disindaysa → Escalation'a gore dogru agenta yonlendir")
- ❌ Aynı Red Flags / Verification 2+ agent'ta tekrarlanmamalı (domain-specific olmalı)
- ✅ Identity en az 2 cümle, gerçek dünya rol karşılığı ile
- ✅ Bridge en az 2 agent referansı (ID + isim + kesişim noktası)
- ✅ When NOT to Use en az 3 spesifik yönlendirme (agent ID ile)
- ✅ Red Flags en az 4 domain-specific işaret
- ✅ Verification en az 4 domain-specific checklist item
- ✅ Process en az 3 faz (Phase 0 + 2 execution phase)
- ✅ Knowledge dosyaları en az 30 satır, tablo/snippet/checklist içermeli
- ✅ Output Format somut örnek ile (sadece "{format}" değil)

## DOĞRULAMA (bitince çalıştır)

```bash
# Placeholder kontrolü
echo "=== Placeholder Check ==="
echo "Bridge placeholder:" $(find agents -name "AGENT.md" | xargs grep -l "Hangi alanlarla" 2>/dev/null | wc -l)
echo "Output placeholder:" $(find agents -name "AGENT.md" | xargs grep -l "Ciktinin formati" 2>/dev/null | wc -l)
echo "Planned knowledge:" $(find agents -name "_index.md" | xargs grep -l "(planned)" 2>/dev/null | wc -l)
echo "Knowledge files:" $(find agents -path "*/knowledge/*.md" ! -name "_index.md" | wc -l)
```

Hedef: İlk 3 satır = 0, son satır ≥ 400.
