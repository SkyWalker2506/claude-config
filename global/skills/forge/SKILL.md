---
name: forge
description: "Tam otonom gelistirme dongusu — analysis, sprint, parallel tasks, PR/review loop, merge, summary. Focus mode ile belirli alanlara odaklanir. Kendi repeat'i dahil. Triggers: forge, forge all, tam dongü, full cycle."
argument-hint: "[N=1] [proje] [-focus]"
---

# /forge — Full Development Cycle

Projeyi analiz et, sprint plan, paralel task'lari calistir, PR/review/merge dongusu, ozet ve dersler cikar. Tek komutla uçtan uca.

## Kullanim

```
/forge                          # tek run, CWD projesi, tüm kategoriler
/forge 3                        # 3 run, CWD projesi
/forge CoinHQ                   # tek run, CoinHQ
/forge 5 CoinHQ                 # 5 run, CoinHQ
/forge all                      # tek run, tum projeler (projects.json)
/forge 2 all                    # 2 run, tum projeler
/forge choose                   # proje seçim menüsü — listeden seç, müsaitlik göster, forge et

# Focus modları (-ile ayrilir, birden fazla verilebilir):
/forge -optimize                # Performans ve teknik borç
/forge -feature                 # Yeni özellik geliştirme
/forge -backend                 # Sadece backend/API
/forge -frontend                # Sadece UI/UX
/forge -security                # Güvenlik açıkları ve hardening
/forge -test                    # Test coverage artırma
/forge -refactor                # Kod temizliği ve yeniden yapılandırma
/forge -docs                    # Dokümantasyon
/forge 3 CoinHQ -backend -security    # Kombinasyon: 3 run, iki focus
/forge all -frontend            # Tüm projeler, sadece frontend
```

## Arguman cozumu

| Input | N | Proje | Focus |
|-------|---|-------|-------|
| `/forge` | 1 | CWD | tümü |
| `/forge 3` | 3 | CWD | tümü |
| `/forge CoinHQ` | 1 | CoinHQ | tümü |
| `/forge 5 CoinHQ` | 5 | CoinHQ | tümü |
| `/forge all` | 1 | tüm projeler | tümü |
| `/forge 2 all` | 2 | tüm projeler | tümü |
| `/forge -backend` | 1 | CWD | backend |
| `/forge 3 CoinHQ -frontend -test` | 3 | CoinHQ | frontend + test |
| `/forge choose` | — | seçilen projeler | tümü |
| `/forge choose -backend` | — | seçilen projeler | backend |

**Focus parsing:** `-` ile başlayan her token focus flag'idir. Sayı token → N, bilinen proje adı → proje, geri kalan `-xxx` → focus listesi.

## Focus Modları

| Flag | Kapsam | Phase 1'e etki | Phase 2'ye etki |
|------|--------|---------------|-----------------|
| `-optimize` | Performans, cache, DB query, bundle size | Perf + Arch analizi | Task önceliği: hız metrikleri |
| `-feature` | Yeni özellik, PRD'deki backlog | Growth + Biz analizi | Yeni feature task'ları |
| `-backend` | API, DB, server logic, auth | Data + Arch + Sec analizi | Backend-only task'lar |
| `-frontend` | UI, UX, responsive, animasyon | UI/UX + A11y + Content analizi | Frontend-only task'lar |
| `-security` | Auth güvenliği, injection, secrets, deps | Sec analizi (Opus ile) | Security task'ları önce |
| `-test` | Unit, widget, integration, e2e testler | Tüm kategorilerde test gaps | Test task'ları |
| `-refactor` | Dead code, duplication, complexity | Arch + Perf analizi | Refactor task'ları |
| `-docs` | README, API docs, in-code comments | Content analizi | Docs task'ları |

**Kombinasyon:** Birden fazla focus verilirse sadece o alanların kesişim task'ları seçilir.

**Focus yok:** Tüm kategoriler analiz edilir, öncelik metriklere göre doğal sıralanır.

**Focus başlığı:**
```
━━ Forge Run [1/3] — CoinHQ [-backend -security] ━━━━━━━━
```

**Proje tespiti (CWD):**
1. CLAUDE.md veya .claude/index.md oku → proje adi
2. Yoksa klasor adi kullan
3. `projects.json`'dan path dogrula

**`all` modu:**
- `~/Projects/ClaudeHQ/projects.json`'dan aktif projeleri oku
- Her projeyi **paralel** forge et — her proje bağımsız background agent olarak başlatılır (max 12 concurrent)
- **Aktif session tespiti yapilir** — kullanicinin baska terminalde calistigi projeler atlanir (bkz. "Aktif Session Tespiti" bolumu)

## `forge choose` — Proje Seçim Modu

`/forge choose` çalıştırıldığında:

**Adım 1 — Proje Listesi:**  
`projects.json`'dan projeleri oku, numaralı liste olarak göster:

```
━━ Forge — Proje Seç ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   #   Proje               Durum
  ───  ──────────────────  ──────────────────────────────
   1   ar-research         ✅ boşta  (session: 4sa önce)
   2   ByteCraftHQ         ✅ boşta  (git: clean)
   3   CoinHQ              ⚠️  belirsiz (session: 18dk önce)
   4   Gardirop            ⏭  meşgul  (forge.lock + dirty)
   5   KnightOnlineAI      ✅ boşta
   6   ProjeBirlik         ✅ boşta
   7   trading-bot         ✅ boşta
   8   transcriptr         ✅ boşta
   9   VocabLearningApp    ✅ boşta
  10   Viralyze            ✅ boşta
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Seçim (örn: 1,3,5-8 veya hepsi için "all", iptal "0"):
```

**Durum sütunu** Aktif Session Tespiti'nden gelir — proje listesi gösterilmeden önce tüm projeler için müsaitlik skorları hesaplanır:
- `✅ boşta` — skor 0  
- `⚠️ belirsiz` — skor 1 (seçilebilir ama uyarı gösterilir)
- `⏭ meşgul` — skor ≥ 2 (seçilemez, gri gösterilir)

**Adım 2 — Seçim Parse:**

| Giriş | Anlamı |
|-------|--------|
| `1,3,5` | 1, 3, 5 numaralı projeler |
| `2-6` | 2'den 6'ya kadar |
| `1,4-7,9` | Kombine |
| `all` | Tüm boşta projeler (meşgullar hariç) |
| `0` | İptal |

**Adım 3 — Onay:**

```
Seçilen projeler: ar-research, CoinHQ, transcriptr
  ⚠️  CoinHQ belirsiz durumda — dahil et? [Y/n]:
Forge edilecek: ar-research, CoinHQ (onaylandı), transcriptr
Focus? (boş bırak = tümü, ya da -backend -security gibi gir):
```

**Adım 4 — Forge:**  
Seçilen projeleri `forge all --only` ile paralel olarak forge et. Bundan sonra normal `forge all` akışı geçerlidir.

---

## Preset Menüsü

Argüman verilmeden `/forge` çalıştırıldığında aşağıdaki menüyü göster ve kullanıcının seçim yapmasını bekle:

```
━━ Forge — Focus Seç ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1) Quick Fix         -security -optimize
  2) Feature Sprint    -feature
  3) Full Cycle        (tüm kategoriler)
  4) Deep Clean        -refactor -test
  5) Backend Hardening -backend -security
  6) Frontend Polish   -frontend -docs
  7) Custom…           argüman gir (örn: -backend -test)
  0) İptal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Seçim (1-7, 0=iptal):
```

Kullanıcı seçim yapınca:
- **1-6**: Focus flag'lerini uygula, proje = CWD, N = 1, Phase 0'a geç
- **7**: "Focus flag'leri gir:" diye sor, parse et, Phase 0'a geç
- **0**: İptal et, dur

> Not: `all` modu ve run sayısı argümanla verilir — `/forge all`, `/forge 3`, `/forge 2 all -backend` gibi. Menü sadece focus seçimi içindir.

Argüman **verilmişse** (`/forge 3 CoinHQ -backend` gibi) menü **gösterilmez**, direkt Phase 0'a geç.

---

## Forge Run Akisi

Her run 7 fazdan olusur:

```
━━ Forge Run [1/N] — CoinHQ ━━━━━━━━━━━━━━━━
  Phase 0: Pre-flight Checks
  Phase 1: Analysis
  Phase 2: Sprint Plan
  Phase 3: Sprint Creation
  Phase 4: Parallel Task Execution
  Phase 5: Summary & Lessons
  Phase 7: Forge Analysis (otomatik — metrik + optimizasyon)
  Phase 6: Handoff to next run
━━ Forge Run [1/N] Complete ✓ ━━━━━━━━━━━━━━━
```

---

### Phase 0 — Pre-flight Checks

Run baslamadan once tum bagimliliklari kontrol et. Biri bile fail ederse **durur ve kullaniciya bildirir**.

**`all` modunda ilk is: Aktif Session Tespiti** — forge baslamadan once hangi projelerin atlanacagini belirle (detay asagida).

```
━━ Pre-flight Checks ━━━━━━━━━━━━━━━━━━
  [✓] Git           — clean working tree, on main
  [✓] GitHub CLI    — gh auth status OK
  [✓] Jira          — Atlassian MCP aktif, proje KEY gecerli
  [✓] Flutter/Node  — proje stack'ine gore build tool mevcut
  [✓] Secrets       — secrets.env yuklu, gerekli key'ler var
  [✓] Disk          — min 1GB bos alan
  [✓] Agent Models  — Sonnet (kod) + Opus (review) erisilebilir
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

| Kontrol | Nasil | Fail durumu |
|---------|-------|-------------|
| **Git clean** | `git status --porcelain` bos mu | "Uncommitted changes var. Commit veya stash et." |
| **Git branch** | `git branch --show-current` = main/master | "main branch'te degilsin. `git checkout main` yap." |
| **gh auth** | `gh auth status` | "GitHub CLI giris yapmamis. `gh auth login` calistir." |
| **Jira MCP** | Atlassian MCP tool'larini cagir (getVisibleJiraProjects) | "Jira baglantisi yok. MCP kontrol et." |
| **Jira KEY** | Proje KEY'i Jira'da var mi | "Proje KEY '{KEY}' Jira'da bulunamadi." |
| **Build tool** | `pubspec.yaml` → flutter, `package.json` → node, vb. | "Flutter/Node bulunamadi. Yukle." |
| **Secrets** | `source secrets.env`, gerekli key'ler set mi | "SUPABASE_URL eksik. secrets.env kontrol et." |
| **Disk** | `df -h .` kontrol | "Disk alani yetersiz." |
| **Models** | Sonnet + Opus API erisilebilir mi (basit test) | "Model erisimi yok. API key kontrol et." |

Tum kontroller gecerse:
```
✅ Pre-flight OK — forge basliyor
```

**Project Index (Pre-flight sonu):**  
Pre-flight geçtikten hemen sonra, Phase 1 başlamadan projeyi jCodeMunch ile indexle:

```
[CoinHQ] indexing…
```

`mcp__jcodemunch__index_repo` çağır — path: `{proje_path}`. Bu sayede Phase 1 analizinde ve task agentlarında sembol araması hızlı olur. Index zaten güncel bile olsa yenile (değişmiş dosyaları yakalar).

---

### Phase 1 — Project Analysis

Focus varsa `/project-analysis {focus_flags}` olarak calistir (ornek: `/project-analysis -backend -security`). Focus yoksa sadece `/project-analysis`. Interaktif sorulari otomatik cevapla:

| Soru | Otomatik cevap |
|------|----------------|
| compact onerisi | 2 (gec) |
| Agent atama modu | 1 (Lead Orchestrator) |
| Brief olustur mu | Y (evet) |
| Agent kullanilabilirlik | 4 (tum alternatifleri uygula) |

Analiz tamamlaninca `analysis/MASTER_ANALYSIS.md` olusur.

**Sonraki run'larda:** Onceki run'in `lessons_learned` dosyasini analysis'e feed et:
```
Bu projenin onceki forge run'inda su dersler cikarildi:
[lessons_learned.md icerigi]
Bunlari goz onunde bulundurarak analiz et.
```

---

### Phase 2 — Sprint Plan (Lead kararlari otomatik kabul)

`/sprint-plan` skill'ini calistir.

Lead'lerin tum onerilerini **otomatik kabul et** — soru sormadan:
- Task oncelikleri → kabul
- Sprint sirasi → kabul
- Efor tahminleri → kabul
- Jira girisi → yap

Cikti: `analysis/SPRINT_PLAN.md` + Jira'da epic/task'lar

---

### Phase 3 — Sprint Creation

Sprint plan'daki task'lari Jira'da olustur (Phase 2'de yapilmadiysa).

Her sprint icin:
1. Epic olustur
2. Task'lari olustur (summary, description, priority, story points)
3. Sprint 1'i aktif yap

---

### Phase 4 — Parallel Task Execution

Sprint sprint ilerle (Sprint 1 bitince Sprint 2, vs.):

```
━━ Sprint 1/3 — Security & Critical Fixes ━━━
  Task 1: [KEY-101] ▶ branch → code → PR → review → merge ✓
  Task 2: [KEY-102] ▶ branch → code → PR → review → fix → review → merge ✓
  Task 3: [KEY-103] ▶ branch → code → PR → review → merge ✓
━━ Sprint 1 Complete ━━━━━━━━━━━━━━━━━━━━━━━━
```

Sprint baslamadan once dispatch tablosu goster:

```
━━ Sprint 1 — Task Pipeline ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Task         Agent     Model          Gorev              Durum
  ──────────   ──────    ───────────    ──────────         ───────
  KEY-101      Coder     Sonnet 4.6     Branch + code + PR  ⏳
  KEY-101      Reviewer  Opus 4.6       Review + merge       ⏳
  KEY-102      Coder     Sonnet 4.6     Branch + code + PR  ⏳
  KEY-102      Reviewer  Opus 4.6       Review + merge       ⏳
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Agent 1-Kelime Durum Etiketi:**  
Her agent (Coder ve Reviewer) aktif olarak çalışırken her adım başında tek satır durum etiketi yazar:

```
[KEY-101] branching
[KEY-101] coding
[KEY-101] testing
[KEY-101] pr
[KEY-101] reviewing
[KEY-101] fixing
[KEY-101] merging
[KEY-101] done ✓
```

Format: `[{JIRA_KEY}] {eylem}` — eylem tam olarak 1 kelime. Proje forge agentı için:
```
[CoinHQ] indexing
[CoinHQ] analyzing
[CoinHQ] planning
[CoinHQ] coding
[CoinHQ] reviewing
[CoinHQ] done ✓
```

Bu etiketler her adım **başında** yazılır (bitmeden önce) — bu sayede paralel çalışan agentların durumu gerçek zamanlı izlenebilir.

Her task icin `/jira-start-new-task` pipeline'ini kullan:

1. **Branch olustur** — `feat/{key}-xxx`
2. **Kod yaz** — Sonnet model (worktree izolasyonu)
3. **PR ac** — `gh pr create`
4. **Review** — Opus model
5. **Sorun varsa → Fix Loop:**
   ```
   review fail → fix → commit → push → re-review
   Max 5 iterasyon. 5'te cozulmediyse:
     - PR'a yorum birak: "Forge: max retry reached, needs manual review"
     - Sonraki task'a gec
   ```
6. **Merge** — `gh pr merge --squash --delete-branch`
7. **Jira Done** — transition

**Paralel calisma:**
- Ayni sprint icerisindeki task'lar paralel calisir (max 5 concurrent)
- Farkli sprint'ler sirayla calisir
- Dosya lock sistemi cakismayi onler (`.jira-state/file-locks/`)

---

### Phase 5 — Summary & Lessons Learned

Tum sprint'ler tamamlaninca:

1. **Ozet raporu olustur** — `forge/run-{N}-summary.md`:
   ```markdown
   # Forge Run N Summary — CoinHQ

   ## Stats
   - Sprints completed: 3/3
   - Tasks completed: 12/14
   - Tasks failed: 2 (manual review needed)
   - Total commits: 34
   - PRs merged: 12

   ## Agent Execution
   - Coder agents: Sonnet 4.6 (12 tasks)
   - Reviewer agents: Opus 4.6 (12 reviews, 3 fix loops)
   - Analysis: Sonnet 4.6 (5 leads) + Opus 4.6 (master)
   - Total agent time: 45m

   ## Completed Tasks
   - [KEY-101] Add rate limiting to API endpoints ✓
   - [KEY-102] Fix SQL injection in search ✓
   ...

   ## Failed Tasks
   - [KEY-113] Migrate auth to OAuth2 — max retry reached
   - [KEY-114] Add E2E tests — flutter test timeout

   ## Changes by Category
   - Security: 4 tasks
   - Performance: 3 tasks
   - Architecture: 2 tasks
   - UI/UX: 3 tasks
   ```

2. **Lessons learned** — `forge/run-{N}-lessons.md`:
   ```markdown
   # Lessons Learned — Run N

   ## What worked
   - Worktree isolation prevented merge conflicts
   - Security fixes were straightforward

   ## What failed and why
   - OAuth2 migration too complex for single task — should be split
   - E2E tests need running emulator — skip in CI-only env

   ## Recommendations for next run
   - Split large tasks (XL) into smaller subtasks
   - Add emulator setup to prerequisites
   - Focus on test coverage gaps
   ```

---

### Phase 7 — Forge Analysis (Otomatik)

Phase 5 tamamlanır tamamlanmaz `/forge-analysis` skill'ini çalıştır. Argüman olarak mevcut run'ın summary dosya yolunu geç:

```
/forge-analysis forge/run-{N}-summary.md {proje}
```

Bu phase:
- Run metriklerini ölçer (task success rate, fix loop ratio, vb.)
- Cross-run trend analizi yapar (birden fazla run varsa)
- Bottleneck'leri tespit eder
- Memory ve skill dosyalarını otomatik optimize eder
- `forge/analysis-{tarih}-run-{N}.md` raporunu oluşturur

**Forge Analysis sonucu Phase 6'ya feed edilir** — handoff önerileri analysis raporundan gelir.

---

### Phase 6 — Handoff (N > 1 ise)

Sonraki run icin:
1. `lessons_learned` dosyasini Phase 1'e feed et
2. Completed task'lari filtrele — ayni task tekrar yapilmaz
3. Yeni analysis onceki run'in cikarimlarini icerir

```
━━ Forge Run [1/3] Complete ✓ ━━━━━━━━━━━━
  12/14 tasks merged, 2 failed
  Lessons saved → forge/run-1-lessons.md
  Starting Run 2 with lessons fed back...
━━ Forge Run [2/3] Starting ━━━━━━━━━━━━━
```

**Son run tamamlaninca (run N = toplam):**

`/forge-analysis --final {N} {proje}` calistir — tum run'lari kapsayan Final Meta-Analiz baslatilir.

```
━━ All Runs Complete — Final Meta-Analysis ━━━━━━━━━
  /forge-analysis --final 5 CoinHQ
  → forge/meta-analysis-2026-04-08-runs-1-to-5.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## `forge all` modu

Tum projeleri **paralel** forge et — her proje bağımsız background agent:

```
/forge all        # her proje 1 run, hepsi paralel
/forge 2 all      # her proje 2 run, paralel
```

Akis:
1. `~/Projects/ClaudeHQ/projects.json` oku
2. Aktif session tespiti yap — atlanacakları belirle
3. Kalan projelerin hepsini tek seferde paralel background agent olarak başlat:
   - Her agent kendi projesini tam forge eder (analysis → tasks → PR → merge → Jira)
   - Agent'lar birbirini beklemez
   - Max 12 concurrent agent
4. Tüm agent'lar tamamlanınca özet göster:

```
━━ Forge All Summary ━━━━━━━━━━━━━━━━━
  CoinHQ:      3 sprints, 12/14 tasks ✓
  ArtLift:     2 sprints, 8/8 tasks ✓
  Viralyze:    3 sprints, 10/13 tasks ✓ (3 failed)
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Dosya yapisi

```
{proje}/
├── analysis/
│   ├── MASTER_ANALYSIS.md                  # Phase 1 ciktisi
│   └── SPRINT_PLAN.md                      # Phase 2 ciktisi
├── forge/
│   ├── run-1-summary.md                    # Run ozeti (Phase 5)
│   ├── run-1-lessons.md                    # Cikarilan dersler (Phase 5)
│   ├── analysis-2026-04-08-run-1.md        # Verimlilik analizi (Phase 7)
│   ├── run-2-summary.md
│   ├── run-2-lessons.md
│   ├── analysis-2026-04-09-run-2.md
│   └── ...
└── .jira-state/                            # Lock dosyalari
```

`forge/` klasorunu `.gitignore`'a ekle.

---

---

## Aktif Session Tespiti (`all` modu)

`forge all` calistiginda her projeyi forge etmeden once **kullanicinin o anda o projede calisip calismadigi** kontrol edilir. Aktif projeler forge'dan cikarilir — o projede hata yapmaktan kacilir, cakisma olmaz.

### Tespit Yontemi

Bir proje "aktif" sayilir eger asagidaki sinyallerden **en az ikisi** positif:

| Sinyal | Kontrol | Komut |
|--------|---------|-------|
| **Claude session** | Son 30 dakikada `.jsonl` aktivitesi var mi | `find ~/.claude/projects/{proje-slug}/ -name "*.jsonl" -newer /tmp/forge-check-ts 2>/dev/null` |
| **Git dirty** | Uncommitted degisiklik var mi | `git -C {path} status --porcelain` |
| **Git lock** | `.git/index.lock` mevcut mu | `test -f {path}/.git/index.lock` |
| **Forge lock** | `.jira-state/forge.lock` mevcut mu (baska forge calisiyor) | `test -f {path}/.jira-state/forge.lock` |
| **Recent file change** | Son 15 dakikada kaynak dosya degisti mi | `find {path}/lib {path}/src -newer /tmp/forge-check-ts -name "*.dart" -o -name "*.ts" -o -name "*.py" 2>/dev/null | head -1` |

**Proje slug** cikarsimi:
- `/Users/musabkara/Projects/CoinHQ` → `-Users-musabkara-Projects-CoinHQ`
- `~/.claude/projects/-Users-musabkara-Projects-CoinHQ/` dizini kontrol edilir

**Ozel kural — Forge'u calistiran proje:** `forge all` hangi CWD'den calisiyorsa o projeyi aktif tespitinden **muaf tut** — o session forge'un kendisidir, false positive olusur. (Ornek: ClaudeHQ'dan `forge all` calistirilinca ClaudeHQ kendini atlamamali.)

### Kontrol Adımlari

```bash
# 1. Timestamp olustur
touch /tmp/forge-check-ts  # 30dk gecmisini simule etmek icin: touch -t $(date -v-30M +%Y%m%d%H%M) /tmp/forge-check-ts

# 2. Her proje icin skor hesapla (0-5 arasi)
for proje in projects.json'daki aktif projeler:
  skor = 0
  skor += 1 if claude session aktif (son 30dk jsonl)
  skor += 1 if git dirty
  skor += 1 if git lock
  skor += 1 if forge lock
  skor += 1 if recent file change (son 15dk)
  
  if skor >= 2:
    → SKIP (aktif proje)
  elif skor == 1:
    → WARN (muhtemelen aktif, kullaniciya sor)
  else:
    → FORGE (guvenli)
```

### Cikti Formati

```
━━ Forge All — Aktif Session Tespiti ━━━━━━━━━━━━━━━━━━━━━━━
  CoinHQ       → ✅ Guvenli    (session: 3sa once, git: clean)
  ArtLift      → ⏭  Atlaniyor  (session: 2dk once + git dirty)
  Gardirop     → ⏭  Atlaniyor  (forge.lock mevcut)
  Viralyze     → ⚠️  Belirsiz   (session: 18dk once)
    → Viralyze'i forge etsek mi? [Y/n]:
  RefinUp      → ✅ Guvenli    (session: 45dk once, git: clean)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Forge edilecek: CoinHQ, Viralyze (onay bekleniyor), RefinUp
Atlanan: ArtLift, Gardirop
```

**"Belirsiz" projeler (skor=1):** Kullaniciya sor. Cevap:
- Y → forge et
- N → atla
- `--force` flag verilmisse → sor, direkt forge et

### `--force` ve `--skip` Flags

```
/forge all --force          # Aktif tespiti atla, hepsini forge et
/forge all --skip ArtLift   # Belirli projeyi manuel atla
/forge all --only CoinHQ,Viralyze  # Sadece bu projeleri forge et
```

### Forge Lock

Her forge baslayinca o projeye lock koy, bitince kaldir:

```bash
# Forge baslangicinda:
mkdir -p {path}/.jira-state && touch {path}/.jira-state/forge.lock

# Forge bitince (Phase 7 sonunda):
rm -f {path}/.jira-state/forge.lock
```

Bu sayede iki ayri `forge all` ayni projeye cakismaz.

---

## Kurallar

1. **Lead kararlari otomatik kabul** — forge sifir soru sorar (analysis haric: orada sadece oto-cevap)
2. **`all` modunda projeler paralel** — her proje bağımsız background agent, max 12 concurrent proje
2a. **Tek projede max 5 concurrent task** — sprint içi paralel task limiti
3. **Max 5 fix retry per PR** — sonsuz dongu onlemi
4. **Max 10 run** — `/forge 10` max, daha fazlasi icin uyari
5. **Secret'lar koda yazilmaz** — `.env.example` + fallback
6. **Destructive git islemleri yasak** — `push --force`, `reset --hard`, `rm -rf` yok
7. **Her task worktree'de calisir** — main branch'e direkt commit yok
8. **Sprint sirasi korunur** — Sprint 1 bitmeden Sprint 2 baslamaz
9. **Baska projeden cagirilabilir** — proje adi veya `all` ile herhangi bir dizinden calistir
10. **Phase 7 atlanamazz** — her forge run'inda `/forge-analysis` otomatik calisir, skip edilemez
11. **Verimlilik skoru < 50 ise dur** — kullaniciya bildir, sonraki run'i baslatma
12. **`all` modunda aktif session tespiti zorunlu** — skor ≥ 2 projeyi forge etme, kullaniciya bildir
13. **Forge lock** — her forge baslayinca `.jira-state/forge.lock` yaz, bitince sil
15. **forge choose** — `choose` argümanı verilince önce müsaitlik kontrolü yap, sonra kullanıcı proje seçsin, seçilenleri paralel forge et
16. **Project index zorunlu** — Phase 0 sonunda `mcp__jcodemunch__index_repo` ile projeyi indexle; bu adım atlanamaz
17. **Agent 1-kelime durum etiketi** — her agent her adım başında `[PROJE/KEY] eylem` formatında tek satır yazar (branching, coding, reviewing, merging, done); sessiz çalışma yasak
14. **9+ puan eşiği — başta sor, 9'da dur:**
    - Forge **başlamadan önce** (Phase 0 sonrası, Phase 1 öncesi) şunu sor:
      ```
      Proje skoru tahmini ≥9/10 görünüyor. Seçenek:
        1) 9.0 puana ulaşınca dur  (verimli, polish değil gerçek iş)
        2) Sonuna kadar git        (küçük kazanımlar da olsa devam)
      Seçim (1/2):
      ```
    - Bu soru sadece önceki run summary'de skor **≥ 8.5** ise veya analysis'te "diminishing returns" / "polish" ifadeleri geçiyorsa gösterilir. İlk run'da veya skor belli değilse gösterilmez.
    - Kullanıcı **1** seçerse: her run sonunda Phase 5'te skor **≥ 9.0** ise loop'u durdur, kullanıcıya bildir:
      ```
      ⏹ Forge durdu — proje skoru 9.2/10 eşiği aştı.
      Kalan açıklar polish/OSS formality kategorisinde — gerçek kullanıcı değeri düşük.
      Devam etmek için: /forge 1 --force-continue
      ```
    - Kullanıcı **2** seçerse veya `--force-continue` flag'i varsa: normal akış, skor limiti yok.
