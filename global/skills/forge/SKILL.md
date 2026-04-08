---
name: forge
description: "Tam otonom gelistirme dongusu — analysis, sprint, parallel tasks, PR/review loop, merge, summary. Kendi repeat'i dahil. Triggers: forge, forge all, tam dongü, full cycle."
argument-hint: "[N=1] [proje]"
---

# /forge — Full Development Cycle

Projeyi analiz et, sprint plan, paralel task'lari calistir, PR/review/merge dongusu, ozet ve dersler cikar. Tek komutla uçtan uca.

## Kullanim

```
/forge                     # tek run, CWD projesi
/forge 3                   # 3 run, CWD projesi
/forge CoinHQ              # tek run, CoinHQ
/forge 5 CoinHQ            # 5 run, CoinHQ
/forge all                 # tek run, tum projeler (projects.json)
/forge 2 all               # 2 run, tum projeler
```

## Arguman cozumu

| Input | N | Proje |
|-------|---|-------|
| `/forge` | 1 | CWD |
| `/forge 3` | 3 | CWD |
| `/forge CoinHQ` | 1 | CoinHQ |
| `/forge 5 CoinHQ` | 5 | CoinHQ |
| `/forge all` | 1 | tum projeler |
| `/forge 2 all` | 2 | tum projeler |

**Proje tespiti (CWD):**
1. CLAUDE.md veya .claude/index.md oku → proje adi
2. Yoksa klasor adi kullan
3. `projects.json`'dan path dogrula

**`all` modu:**
- `~/Projects/ClaudeHQ/projects.json`'dan aktif projeleri oku
- Her projeyi sirayla forge et (proje arasi paralel degil — kaynak yonetimi icin)

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
  Phase 6: Handoff to next run
━━ Forge Run [1/N] Complete ✓ ━━━━━━━━━━━━━━━
```

---

### Phase 0 — Pre-flight Checks

Run baslamadan once tum bagimliliklari kontrol et. Biri bile fail ederse **durur ve kullaniciya bildirir**.

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

---

### Phase 1 — Project Analysis

`/project-analysis` skill'ini calistir. Ancak interaktif sorulari otomatik cevapla:

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
━━ Sprint 1 — Task Pipeline ━━━━━━━━━━━━━━━━━━━━━━━━━━
  Task         Agent     Model          Gorev
  ──────────   ──────    ───────────    ──────────
  KEY-101      Coder     Sonnet 4.6     Branch + code + PR
  KEY-101      Reviewer  Opus 4.6       Review + merge
  KEY-102      Coder     Sonnet 4.6     Branch + code + PR
  KEY-102      Reviewer  Opus 4.6       Review + merge
  ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

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

---

## `forge all` modu

Tum projeleri sirayla forge et:

```
/forge all        # her proje 1 run
/forge 2 all      # her proje 2 run
```

Akis:
1. `~/Projects/ClaudeHQ/projects.json` oku
2. Her aktif proje icin sirayla forge calistir
3. Proje arasi ozet goster:

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
│   ├── MASTER_ANALYSIS.md       # Phase 1 ciktisi
│   └── SPRINT_PLAN.md           # Phase 2 ciktisi
├── forge/
│   ├── run-1-summary.md         # Run ozeti
│   ├── run-1-lessons.md         # Cikarilan dersler
│   ├── run-2-summary.md
│   ├── run-2-lessons.md
│   └── ...
└── .jira-state/                 # Lock dosyalari
```

`forge/` klasorunu `.gitignore`'a ekle.

---

## Kurallar

1. **Lead kararlari otomatik kabul** — forge sifir soru sorar (analysis haric: orada sadece oto-cevap)
2. **Max 5 concurrent task** — bellek ve CPU yonetimi
3. **Max 5 fix retry per PR** — sonsuz dongu onlemi
4. **Max 10 run** — `/forge 10` max, daha fazlasi icin uyari
5. **Secret'lar koda yazilmaz** — `.env.example` + fallback
6. **Destructive git islemleri yasak** — `push --force`, `reset --hard`, `rm -rf` yok
7. **Her task worktree'de calisir** — main branch'e direkt commit yok
8. **Sprint sirasi korunur** — Sprint 1 bitmeden Sprint 2 baslamaz
9. **Baska projeden cagirilabilir** — proje adi veya `all` ile herhangi bir dizinden calistir
