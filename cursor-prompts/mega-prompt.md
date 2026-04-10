# Cursor Composer 2 — Tüm Agent Overhaul (Mega Prompt)

> Çalışma dizini: `~/Projects/claude-config`
> Model: Composer 2 (Standard)
> Tahmini süre: Uzun — agent sayısı çok, sabırlı ol

---

## GÖREV

Aşağıdaki **165 incomplete agent** için:
1. Her agent'ın `AGENT.md`'sini domain-specific olarak TAM doldur
2. Her agent için **4-6 knowledge dosyası** oluştur — **web'den araştırarak**, gerçek best practice ve pattern'lerle
3. Her agent'ın `knowledge/_index.md`'sini güncelle

## DOKUNMA (zaten tam — bu agent'ların dosyalarını DEĞİŞTİRME)
- `agents/orchestrator/jarvis/` (A0)
- `agents/backend/frontend-coder/` (B3)
- `agents/backend/mobile-dev-agent/` (B15)
- `agents/design/ui-ux-researcher/` (D1)
- `agents/design/design-system-agent/` (D2)
- `agents/design/motion-graphics-agent/` (D10)
- `agents/devops/github-manager/` (J10)
- `agents/research/ai-tool-evaluator/` (K9)
- `agents/prompt-engineering/prompt-engineer/` (N1)
- `agents/prompt-engineering/ai-systems-architect/` (N6)
- `agents/prompt-engineering/skill-design-specialist/` (N7)
- `agents/prompt-engineering/workflow-engineer/` (N8)
- `agents/backend/unity-shader-developer/` (B22) — TAM
- `agents/backend/unity-multiplayer/` (B23) — TAM
- `agents/3d-cad/unity-vfx-animation/` (E6) — TAM
- `agents/3d-cad/unity-technical-artist/` (E7) — TAM
- `agents/code-review/unity-code-reviewer/` (C7) — TAM

---

## KALİTE KURALLARI (KRİTİK — backend audit'ten çıkan dersler)

1. **Knowledge dosyaları arasında derinlik TUTARLI olsun** — bazıları 4 kaynak + detaylı örnek, bazıları 1 kaynak + basit örnek olmasın. HER dosya en az 3 kaynak + 2 gerçek kod örneği içersin.
2. **Status alanını DEĞİŞTİRME** — frontmatter'daki status olduğu gibi kalsın.
3. **Her agent EN AZ 4 knowledge dosyası olsun.** Konu az bile olsa alt konulara böl.
4. **Bridge referansları ÇİFT YÖNLÜ olsun** — A→B varsa B→A da olmalı.
5. **Frontmatter'ı DEĞİŞTİRME** — sadece `---` altındaki body kısmını doldur.

❌ JENERİK YAZMA. "Best practice kullan" gibi boş cümleler YASAK.
❌ Tüm agent'lara aynı template KOPYALAMA. Her agent FARKLI olmalı.
❌ Aynı Red Flags, Verification, Error Handling tüm agent'lara YAPIŞTIRILMASI YASAK.
✅ Her knowledge dosyası gerçek kod örnekleri, gerçek tool isimleri, gerçek metrikler içermeli.
✅ Her agent'ın Identity'si o agent'ın gerçek dünya karşılığını açıkça belirtmeli.
✅ Output Format gerçek dosya yolları ve somut örnekler içermeli.

---

## ARAŞTIRMA TALİMATI (KRİTİK)

Her agent'ın her knowledge konusu için:
1. **Web'den araştır** — resmi dokümantasyon, güvenilir bloglar (Martin Fowler, ThoughtWorks, Google Engineering, Unity docs, AWS blogs, etc.), GitHub awesome-lists
2. Bilgiyi **sindirip** Quick Reference bölümüne yaz — agent bunu anında yükleyip kullanabilmeli
3. **Decision Matrix / Pattern tablosu** oluştur — ne zaman ne kullanılır
4. **Deep Dive Sources** bölümüne canlı linkleri ekle — agent derine inmesi gerekirse buradan fetch eder
5. **Tarih ekle** — bilgi ne zaman geçerli (2025-2026)

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
- {2-4 domain-specific yasak}

### Bridge
- {Agent ID + isim}: {spesifik kesişim noktası}
- {Agent ID + isim}: {spesifik kesişim noktası}

## Process

### Phase 0 — Pre-flight
- Gerekli dosyalar mevcut mu kontrol et
- {1-2 domain-specific pre-flight}

### Phase 1 — {Domain-specific faz adı}
{3-5 domain-specific adım}

### Phase 2 — {Domain-specific faz adı}
{3-5 domain-specific adım}

### Phase 3 — Verify & Ship
{Doğrulama ve teslim adımları}

## Output Format
{Somut örnek — gerçek çıktı göster, template değil}

## When to Use
- {4-6 spesifik senaryo}

## When NOT to Use
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

## Knowledge Index
> `knowledge/_index.md` dosyasina bak — ihtiyacin olan konuyu yukle
```

---

## REFERANS AGENT (K9 — AI Tool Evaluator — KALİTE BENCHMARK)

```markdown
---
id: K9
name: AI Tool Evaluator
category: research
tier: junior
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
- Mimari karar alma (→ N6) — sadece degerlendirme yap
- Prompt/skill/workflow tasarlama (→ N serisi)
- Dogrulanmamis benchmark sonucu yazma

### Bridge
- AI Systems Architect (N6): framework secimi noktasinda degerlendirme sagla
- Prompt Engineer (N3): model karsilastirmasi noktasinda

## Process
1. Gorevi anla — ne degerlendirilecek
2. `knowledge/_index.md` oku — mevcut bilgileri yukle
3. Web'den guncel bilgi topla
4. Karsilastirma matrisi olustur
5. Maliyet/performans analizi yap
6. Use-case bazli oneri ver
7. Sonuclari `memory/learnings.md`'ye kaydet

## Output Format
```text
[K9] AI Tool Evaluator — Claude vs GPT Comparison
✅ Benchmark: SWE-bench Verified — Claude 72%, GPT 68%
📊 Cost: Claude $15/MTok, GPT $30/MTok
⚠️ Caveat: GPT excels at multi-modal, Claude at long-context
📋 Recommendation: Claude for code tasks, GPT for vision tasks
```

## When to Use
- Yeni AI tool/framework kesfedildiginde
- Mevcut tool'lar arasinda secim yapilirken
- Maliyet optimizasyonu degerlendirilirken

## When NOT to Use
- Karar verilirken → sadece degerlendirme yap
- Implementasyon gerektiginde → B serisi
- Prompt yazarken → N3

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
- Mimari karar → N6 (AI Systems Architect)
```

Senin ürettiğin her agent EN AZ bu kalitede olmalı.

---

## BACKEND DÜZELTMELERİ (ÖNCELİKLİ)

Backend zaten Cursor'da dolduruldu ama birkaç düzeltme lazım:

### B17 (Full Stack Web) — `agents/backend/full-stack-web/`
- `knowledge/supabase-auth-realtime.md` — SIĞ. RLS policy örneği + permissions matrisi ekle, en az 3 kaynak olsun
- `knowledge/prisma-schema-patterns.md` — SIĞ. Relations örneği (hasMany, hasOne) + migration gotcha'lar ekle

### B7 (Bug Hunter) — `agents/backend/bug-hunter/`
- 4 knowledge dosyası var, 5 olmalı. Ekle:
  - `knowledge/incident-timeline-reconstruction.md` — deploy logları, feature flag'ler, DB değişiklikleri ile timeline oluşturma

---

## TÜM INCOMPLETE AGENT LİSTESİ + KNOWLEDGE KONULARI

### ORCHESTRATOR (12 agent) — `agents/orchestrator/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| A1 | lead-orchestrator | `strategic-planning.md`, `risk-assessment-framework.md`, `prioritization-methods.md`, `escalation-protocols.md` |
| A2 | task-router | `task-classification.md`, `capability-matching.md`, `dag-planning.md`, `load-balancing.md` |
| A3 | fallback-manager | `model-health-monitoring.md`, `fallback-chains.md`, `graceful-degradation.md`, `circuit-breaker-patterns.md` |
| A4 | token-budget | `token-counting-methods.md`, `cost-optimization-strategies.md`, `context-window-management.md`, `model-pricing-comparison.md` |
| A5 | context-pruner | `summarization-techniques.md`, `context-compression.md`, `state-transfer-patterns.md`, `memory-hierarchy.md` |
| A6 | daily-health-check | `health-check-patterns.md`, `monitoring-metrics.md`, `alerting-thresholds.md`, `daily-report-format.md` |
| A7 | weekly-analyst | `trend-reporting.md`, `kpi-tracking.md`, `weekly-digest-format.md`, `data-visualization-patterns.md` |
| A8 | manual-control | `emergency-procedures.md`, `human-handoff-protocol.md`, `kill-switch-design.md`, `rollback-procedures.md` |
| A9 | backend-lead | `backend-dispatch-rules.md`, `code-quality-gates.md`, `pr-review-routing.md`, `tech-debt-tracking.md` |
| A10 | design-lead | `design-dispatch-rules.md`, `design-review-gates.md`, `brand-consistency.md`, `ux-metrics.md` |
| A11 | research-lead | `research-dispatch-rules.md`, `source-quality-criteria.md`, `research-methodology.md`, `knowledge-freshness.md` |
| A12 | devops-lead | `devops-dispatch-rules.md`, `incident-severity-matrix.md`, `deployment-gates.md`, `infrastructure-standards.md` |
| A13 | pm-lead | `pm-dispatch-rules.md`, `sprint-health-metrics.md`, `stakeholder-communication.md`, `scope-management.md` |

**ÖNEMLİ — Lead vs Orchestrator Ayrımı:**
- **A0 (Jarvis)** = Üst düzey orchestrator. Kullanıcıyla doğrudan konuşur, görev kabul eder, üst seviye karar verir.
- **A1 (Lead Orchestrator)** = Jarvis'in altında stratejik planlama ve risk yönetimi. Büyük görevleri parçalar, önceliklendirir.
- **A2 (Task Router)** = Görev → agent eşleştirme. DAG planlama, capability matching.
- **A9-A13 (Category Leads)** = Her kategori için dispatch yöneticisi. Kendi kategorisindeki agent'ları tanır, görev dağıtır.
  - A9 Backend Lead → B1-B52 arası agent'ları yönetir
  - A10 Design Lead → D1-D13 arası
  - A11 Research Lead → K1-K15 arası
  - A12 DevOps Lead → J1-J12 arası
  - A13 PM Lead → I1-I10 arası

**Routing akışı:** Kullanıcı → A0 → A1 (strateji) → A2 (routing) → Category Lead (A9-A13) → Spesifik agent

Her Lead agent'ın Bridge bölümünde A0, A1, A2 ve diğer lead'lerle çift yönlü referans olmalı.

### CODE REVIEW (6 agent) — `agents/code-review/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| C1 | lint-format-hook | `eslint-prettier-config.md`, `dart-analysis-options.md`, `pre-commit-hook-setup.md`, `auto-fix-strategies.md` |
| C2 | security-scanner-hook | `secret-scanning-tools.md`, `sast-integration.md`, `dependency-audit-automation.md`, `trivy-snyk-comparison.md` |
| C3 | local-ai-reviewer | `ai-review-prompts.md`, `review-checklist-patterns.md`, `severity-classification.md`, `false-positive-handling.md` |
| C4 | code-rabbit-agent | `coderabbit-configuration.md`, `review-rule-customization.md`, `ci-integration-patterns.md`, `review-comment-format.md` |
| C5 | ci-review-agent | `github-pr-review-api.md`, `review-automation-workflow.md`, `merge-criteria.md`, `status-check-patterns.md` |
| C6 | human-review-coordinator | `review-routing-rules.md`, `reviewer-expertise-matching.md`, `review-sla-tracking.md`, `escalation-criteria.md` |

### DESIGN (10 agent) — `agents/design/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| D3 | stitch-coordinator | `design-to-code-workflow.md`, `tailwind-component-patterns.md`, `responsive-breakpoints.md`, `css-grid-flexbox-decision.md` |
| D4 | figma-assistant | `figma-api-patterns.md`, `design-token-extraction.md`, `component-inventory.md`, `figma-to-code-pipeline.md` |
| D5 | presentation-builder | `slide-design-principles.md`, `keynote-powerpoint-api.md`, `data-visualization-slides.md`, `storytelling-frameworks.md` |
| D6 | image-prompt-generator | `midjourney-prompt-syntax.md`, `stable-diffusion-parameters.md`, `negative-prompt-patterns.md`, `style-reference-guide.md` |
| D7 | icon-asset-agent | `svg-optimization.md`, `sprite-sheet-generation.md`, `responsive-image-formats.md`, `favicon-manifest-setup.md` |
| D8 | mockup-reviewer | `ux-audit-checklist.md`, `accessibility-wcag-guide.md`, `contrast-ratio-tools.md`, `touch-target-guidelines.md` |
| D9 | brand-identity-agent | `brand-guide-structure.md`, `color-theory-palettes.md`, `typography-pairing.md`, `voice-tone-framework.md` |
| D11 | unity-ui-developer | `ui-toolkit-vs-ugui.md`, `uss-uxml-patterns.md`, `responsive-layout-strategies.md`, `runtime-data-binding.md` |
| D12 | unity-ux-flow | `game-ux-patterns.md`, `tutorial-system-design.md`, `menu-flow-architecture.md`, `player-onboarding.md` |
| D13 | unity-hud-minimap | `hud-design-patterns.md`, `minimap-implementation.md`, `damage-indicator-systems.md`, `waypoint-compass-systems.md` |

### DEVOPS (11 agent) — `agents/devops/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| J1 | docker-agent | `dockerfile-best-practices.md`, `docker-compose-patterns.md`, `multi-stage-builds.md`, `container-security.md` |
| J2 | cloud-deploy-agent | `cloud-deployment-strategies.md`, `terraform-patterns.md`, `cloud-provider-comparison.md`, `zero-downtime-deploy.md` |
| J3 | ssl-dns-agent | `ssl-certificate-management.md`, `dns-configuration-patterns.md`, `lets-encrypt-automation.md`, `cdn-dns-setup.md` |
| J4 | server-monitor | `uptime-monitoring-tools.md`, `health-check-endpoints.md`, `alerting-best-practices.md`, `dashboard-design.md` |
| J5 | cost-optimizer | `cloud-cost-optimization.md`, `right-sizing-strategies.md`, `reserved-vs-spot-instances.md`, `cost-monitoring-tools.md` |
| J6 | firebase-agent | `firestore-data-modeling.md`, `firebase-auth-patterns.md`, `cloud-functions-best-practices.md`, `firebase-hosting-rules.md` |
| J7 | incident-responder | `incident-response-playbook.md`, `root-cause-analysis-framework.md`, `rollback-strategies.md`, `post-mortem-template.md` |
| J8 | infrastructure-planner | `capacity-planning-methods.md`, `infrastructure-as-code.md`, `scaling-strategies.md`, `disaster-recovery.md` |
| J9 | performance-load-tester | `k6-load-testing.md`, `artillery-patterns.md`, `stress-test-methodology.md`, `performance-baseline.md` |
| J11 | unity-devops | `gameci-github-actions.md`, `unity-cloud-build.md`, `addressables-ci-pipeline.md`, `build-size-optimization.md`, `platform-build-matrix.md` |
| J12 | unity-version-control | `plastic-scm-guide.md`, `unity-lfs-strategies.md`, `merge-prefab-scene.md`, `lock-file-patterns.md` |

### DATA & ANALYTICS (13 agent) — `agents/data-analytics/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| F1 | data-cleaner | `pandas-cleaning-patterns.md`, `data-normalization.md`, `missing-value-strategies.md`, `data-type-conversion.md` |
| F2 | data-analyst | `statistical-analysis-methods.md`, `hypothesis-testing.md`, `correlation-causation.md`, `insight-reporting.md` |
| F3 | visualization-agent | `matplotlib-seaborn-guide.md`, `plotly-interactive-charts.md`, `chart-type-selection.md`, `color-accessibility.md` |
| F4 | etl-pipeline-agent | `etl-design-patterns.md`, `airflow-dagster-comparison.md`, `data-pipeline-monitoring.md`, `incremental-load.md` |
| F5 | report-generator | `report-template-design.md`, `pdf-generation-tools.md`, `automated-reporting.md`, `executive-summary-format.md` |
| F6 | sql-agent | `sql-query-optimization.md`, `window-functions-guide.md`, `cte-recursive-patterns.md`, `sql-antipatterns.md` |
| F7 | spreadsheet-agent | `excel-formula-patterns.md`, `google-sheets-api.md`, `pivot-table-design.md`, `spreadsheet-automation.md` |
| F8 | jupyter-agent | `jupyter-best-practices.md`, `notebook-reproducibility.md`, `ipywidgets-interactive.md`, `notebook-to-production.md` |
| F9 | data-quality-agent | `data-validation-rules.md`, `data-profiling-tools.md`, `consistency-checks.md`, `data-lineage-tracking.md` |
| F10 | statistics-agent | `hypothesis-testing-guide.md`, `regression-analysis.md`, `bayesian-methods.md`, `ab-test-statistics.md` |
| F11 | unity-analytics | `unity-analytics-setup.md`, `custom-event-design.md`, `player-funnel-analysis.md`, `ab-testing-games.md` |
| F12 | unity-performance-profiler | `unity-profiler-guide.md`, `frame-debugger-analysis.md`, `memory-profiler-workflow.md`, `gpu-cpu-bound-diagnosis.md` |
| F13 | unity-playtesting-analyst | `playtest-data-collection.md`, `heatmap-generation.md`, `player-behavior-metrics.md`, `session-replay-tools.md` |

### AI OPS (12 agent) — `agents/ai-ops/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| G1 | agent-coordinator | `multi-agent-orchestration.md`, `parallel-dispatch-patterns.md`, `agent-communication.md`, `task-dependency-graph.md` |
| G2 | model-monitor | `model-health-metrics.md`, `latency-tracking.md`, `quality-degradation-detection.md`, `model-comparison-live.md` |
| G3 | mcp-health-agent | `mcp-connectivity-testing.md`, `server-health-checks.md`, `tool-availability-monitoring.md`, `mcp-error-patterns.md` |
| G4 | config-manager | `config-sync-strategies.md`, `settings-schema-validation.md`, `environment-config.md`, `feature-flag-patterns.md` |
| G5 | log-analyzer | `log-pattern-detection.md`, `structured-logging.md`, `log-aggregation-tools.md`, `anomaly-detection.md` |
| G6 | backup-agent | `backup-strategies.md`, `restore-testing.md`, `incremental-backup.md`, `disaster-recovery-plan.md` |
| G7 | update-checker | `version-tracking-methods.md`, `changelog-parsing.md`, `breaking-change-detection.md`, `update-notification.md` |
| G8 | cron-scheduler | `cron-expression-guide.md`, `launchd-patterns.md`, `scheduled-task-monitoring.md`, `idempotent-scheduling.md` |
| G9 | performance-monitor | `token-usage-tracking.md`, `response-time-metrics.md`, `cost-per-task-analysis.md`, `performance-budgets.md` |
| G10 | deployment-agent | `vercel-deployment-guide.md`, `firebase-deploy-patterns.md`, `github-pages-setup.md`, `preview-deployments.md` |
| G11 | unity-ml-agents | `ml-agents-setup.md`, `reinforcement-learning-unity.md`, `training-environment-design.md`, `curriculum-learning.md` |
| G12 | unity-sentis | `sentis-model-import.md`, `onnx-optimization.md`, `on-device-inference.md`, `npc-ai-with-sentis.md` |

### JIRA & PM (10 agent) — `agents/jira-pm/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| I1 | jira-router | `jira-workflow-automation.md`, `issue-triage-criteria.md`, `custom-field-patterns.md`, `jql-query-recipes.md` |
| I2 | sprint-planner | `sprint-planning-methodology.md`, `capacity-calculation.md`, `velocity-tracking.md`, `sprint-goal-framework.md` |
| I3 | task-decomposer | `task-splitting-patterns.md`, `subtask-templates.md`, `definition-of-done.md`, `estimation-techniques.md` |
| I4 | status-reporter | `burndown-chart-analysis.md`, `sprint-progress-metrics.md`, `dashboard-design-jira.md`, `stakeholder-reporting.md` |
| I5 | waiting-decision-agent | `decision-framework.md`, `priority-matrix.md`, `blocker-escalation.md`, `decision-log-format.md` |
| I6 | backlog-groomer | `backlog-prioritization-methods.md`, `story-mapping.md`, `backlog-hygiene.md`, `epic-decomposition.md` |
| I7 | burndown-tracker | `burndown-vs-burnup.md`, `velocity-calculation.md`, `scope-creep-detection.md`, `sprint-health-indicators.md` |
| I8 | standup-generator | `standup-format-patterns.md`, `async-standup-tools.md`, `blocker-detection.md`, `daily-summary-template.md` |
| I9 | retrospective-agent | `retrospective-formats.md`, `action-item-tracking.md`, `team-health-metrics.md`, `continuous-improvement.md` |
| I10 | estimation-agent | `story-point-estimation.md`, `planning-poker.md`, `relative-estimation.md`, `estimation-accuracy.md` |

### RESEARCH (14 agent) — `agents/research/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| K1 | web-researcher | `web-search-strategies.md`, `source-credibility.md`, `fact-checking-methods.md`, `research-synthesis.md` |
| K2 | paper-summarizer | `academic-paper-structure.md`, `abstract-extraction.md`, `citation-tracking.md`, `literature-review.md` |
| K3 | documentation-fetcher | `api-doc-navigation.md`, `library-version-tracking.md`, `changelog-analysis.md`, `doc-freshness-check.md` |
| K4 | trend-analyzer | `technology-radar-method.md`, `adoption-curve-analysis.md`, `hype-cycle-assessment.md`, `market-timing.md` |
| K5 | video-summarizer | `youtube-transcript-extraction.md`, `video-summarization-patterns.md`, `timestamp-navigation.md`, `key-takeaway-format.md` |
| K6 | tutorial-finder | `tutorial-quality-criteria.md`, `learning-path-design.md`, `resource-curation.md`, `skill-level-matching.md` |
| K7 | knowledge-base-agent | `rag-patterns.md`, `knowledge-retrieval.md`, `memory-query-optimization.md`, `knowledge-graph-basics.md` |
| K8 | skill-recommender | `skill-gap-analysis.md`, `tool-recommendation-framework.md`, `learning-roadmap.md`, `competency-matrix.md` |
| K10 | regulatory-compliance-agent | `gdpr-compliance-checklist.md`, `kvkk-guide.md`, `data-protection-patterns.md`, `privacy-by-design.md` |
| K11 | asset-scraper | `3d-asset-sources.md`, `license-compliance.md`, `asset-quality-criteria.md`, `batch-download-patterns.md` |
| K12 | resource-collector | `font-sources-guide.md`, `texture-libraries.md`, `icon-pack-curation.md`, `stock-resource-licenses.md` |
| K13 | dataset-finder | `kaggle-navigation.md`, `huggingface-datasets.md`, `data-discovery-methods.md`, `dataset-quality-assessment.md` |
| K14 | unity-asset-store-researcher | `asset-store-evaluation.md`, `package-comparison-framework.md`, `license-risk-assessment.md`, `integration-complexity.md` |
| K15 | unity-tech-researcher | `unity-roadmap-tracking.md`, `beta-package-evaluation.md`, `deprecation-migration.md`, `version-upgrade-guide.md` |

### MARKET RESEARCH (16 agent) — `agents/market-research/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| H1 | market-researcher | `market-analysis-framework.md`, `competitor-research-methods.md`, `trend-analysis-tools.md`, `market-sizing.md` |
| H2 | competitor-analyst | `competitor-swot-template.md`, `benchmark-methodology.md`, `feature-comparison-matrix.md`, `competitive-positioning.md` |
| H3 | revenue-analyst | `revenue-model-patterns.md`, `unit-economics.md`, `pricing-strategy-framework.md`, `financial-projection.md` |
| H4 | pricing-strategist | `pricing-psychology.md`, `ab-test-pricing.md`, `tier-pricing-design.md`, `value-based-pricing.md` |
| H5 | seo-agent | `seo-audit-checklist.md`, `keyword-research-tools.md`, `meta-tag-optimization.md`, `technical-seo-guide.md` |
| H6 | geo-agent | `geo-seo-strategies.md`, `ai-visibility-optimization.md`, `structured-data-markup.md`, `llm-seo-patterns.md` |
| H7 | social-media-agent | `social-media-post-templates.md`, `linkedin-content-strategy.md`, `twitter-engagement.md`, `scheduling-tools.md` |
| H8 | content-repurposer | `content-atomization.md`, `multi-channel-adaptation.md`, `repurpose-workflow.md`, `format-conversion.md` |
| H9 | newsletter-agent | `newsletter-design-patterns.md`, `email-copywriting.md`, `segmentation-strategies.md`, `deliverability-guide.md` |
| H10 | new-tool-scout | `tool-discovery-methods.md`, `model-update-tracking.md`, `evaluation-criteria.md`, `early-adopter-strategy.md` |
| H11 | mcp-distribution-agent | `mcp-server-creation.md`, `npm-publish-guide.md`, `directory-submission.md`, `mcp-marketplace-strategy.md` |
| H12 | viral-output-agent | `viral-content-patterns.md`, `gamification-mechanics.md`, `shareable-design.md`, `engagement-hooks.md` |
| H13 | social-media-strategist | `content-calendar-design.md`, `platform-algorithm-guide.md`, `engagement-metrics.md`, `hashtag-strategy.md` |
| H14 | community-manager-agent | `community-moderation-guide.md`, `discord-server-setup.md`, `engagement-playbook.md`, `faq-management.md` |
| H15 | influencer-research-agent | `influencer-discovery-tools.md`, `audience-analysis.md`, `collaboration-framework.md`, `micro-influencer-strategy.md` |
| H16 | unity-market-analyst | `game-market-trends.md`, `unity-vs-unreal-comparison.md`, `platform-store-analysis.md`, `genre-revenue-analysis.md` |

### MARKETING ENGINE (4 agent) — `agents/marketing-engine/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| M1 | free-tool-builder | `lead-gen-tool-patterns.md`, `calculator-builder-guide.md`, `free-tool-seo.md`, `conversion-optimization.md` |
| M2 | landing-page-agent | `landing-page-anatomy.md`, `conversion-copywriting.md`, `ab-test-landing.md`, `hero-section-patterns.md` |
| M3 | ab-test-agent | `ab-test-methodology.md`, `statistical-significance.md`, `variant-design.md`, `test-documentation.md` |
| M4 | analytics-agent | `ga4-setup-guide.md`, `mixpanel-patterns.md`, `event-tracking-design.md`, `attribution-models.md` |

### PRODUCTIVITY (6 agent) — `agents/productivity/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| L1 | email-summarizer | `email-triage-patterns.md`, `action-item-extraction.md`, `priority-classification.md`, `reply-draft-templates.md` |
| L2 | calendar-agent | `calendar-management.md`, `scheduling-optimization.md`, `timezone-handling.md`, `meeting-preparation.md` |
| L3 | daily-briefing-agent | `briefing-format-design.md`, `information-aggregation.md`, `priority-filtering.md`, `digest-delivery.md` |
| L4 | note-organizer | `note-classification-methods.md`, `tagging-taxonomy.md`, `obsidian-patterns.md`, `knowledge-linking.md` |
| L5 | file-organizer | `file-naming-conventions.md`, `folder-structure-patterns.md`, `automated-cleanup.md`, `duplicate-detection.md` |
| L6 | meeting-notes-agent | `meeting-note-templates.md`, `action-item-tracking.md`, `transcript-processing.md`, `follow-up-automation.md` |

### PROMPT ENGINEERING (1 agent) — `agents/prompt-engineering/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| N2 | agent-builder | `agent-design-patterns.md`, `mcp-integration-guide.md`, `skill-creation-workflow.md`, `agent-testing-strategies.md` |

### SALES & BIZDEV (5 agent) — `agents/sales-bizdev/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| O1 | sales-proposal-agent | `proposal-structure.md`, `rfp-response-guide.md`, `pricing-presentation.md`, `pitch-deck-design.md` |
| O2 | crm-agent | `hubspot-patterns.md`, `pipeline-management.md`, `lead-scoring.md`, `follow-up-sequences.md` |
| O3 | outreach-agent | `cold-email-patterns.md`, `linkedin-outreach-guide.md`, `personalization-at-scale.md`, `sequence-design.md` |
| O4 | pricing-calculator | `cost-estimation-models.md`, `margin-calculation.md`, `bundle-pricing-strategies.md`, `quote-generation.md` |
| O5 | client-onboarding-agent | `onboarding-checklist-design.md`, `welcome-sequence.md`, `handoff-protocol.md`, `client-documentation.md` |

### 3D / CAD (10 agent) — `agents/3d-cad/`

| ID | Dizin | Knowledge |
|----|-------|-----------|
| E1 | 3d-concept-planner | `3d-scene-composition.md`, `reference-gathering.md`, `lighting-setup-guide.md`, `camera-angle-patterns.md` |
| E2 | blender-script-agent | `bpy-api-patterns.md`, `geometry-nodes-guide.md`, `shader-nodes-recipes.md`, `export-pipeline.md` |
| E3 | cad-automation | `autocad-scripting.md`, `parametric-design-patterns.md`, `technical-drawing-standards.md`, `stl-export-optimization.md` |
| E4 | render-pipeline | `render-queue-management.md`, `batch-render-setup.md`, `render-farm-patterns.md`, `output-format-guide.md` |
| E5 | 3d-asset-optimizer | `polygon-reduction-methods.md`, `texture-optimization.md`, `gltf-draco-compression.md`, `lod-generation.md` |
| E8 | unity-level-designer | `terrain-tools-guide.md`, `probuilder-patterns.md`, `tilemap-2d-3d.md`, `scene-management-strategies.md` |
| E9 | unity-cinematic-director | `timeline-advanced-patterns.md`, `cinemachine-rig-recipes.md`, `cutscene-pipeline.md`, `unity-recorder-guide.md` |
| E10 | unity-lighting-artist | `lightmap-baking-guide.md`, `light-probe-placement.md`, `reflection-probe-setup.md`, `volumetric-effects.md` |
| E11 | unity-terrain-specialist | `terrain-sculpting-tools.md`, `vegetation-system.md`, `terrain-streaming.md`, `grass-rendering-optimization.md` |
| E12 | unity-rigging-skinning | `avatar-humanoid-setup.md`, `animation-rigging-package.md`, `ik-constraint-patterns.md`, `blend-shape-workflow.md` |

### UNITY İSKELET AGENT'LAR (Kalan 27) — çeşitli kategoriler

| ID | Dizin | Knowledge |
|----|-------|-----------|
| B24 | backend/unity-ai-navigation | `navmesh-setup-guide.md`, `behavior-tree-patterns.md`, `state-machine-ai.md`, `pathfinding-algorithms.md` |
| B25 | backend/unity-ar-xr | `arfoundation-guide.md`, `xr-interaction-toolkit.md`, `meta-quest-development.md`, `hand-tracking-patterns.md` |
| B26 | backend/unity-audio | `audio-mixer-architecture.md`, `fmod-wwise-comparison.md`, `spatial-audio-guide.md`, `adaptive-music-system.md` |
| B27 | backend/unity-physics | `physx-configuration.md`, `collision-layer-matrix.md`, `joint-types-guide.md`, `raycast-patterns.md` |
| B28 | backend/unity-save-serialization | `save-system-architecture.md`, `json-binary-serialization.md`, `cloud-save-patterns.md`, `playerprefs-alternatives.md` |
| B29 | backend/unity-localization | `localization-package-guide.md`, `string-table-management.md`, `rtl-support.md`, `asset-localization.md` |
| B30 | backend/unity-editor-tooling | `custom-inspector-guide.md`, `editor-window-patterns.md`, `property-drawer-recipes.md`, `scriptable-wizard.md` |
| B31 | backend/unity-procedural-generation | `noise-algorithms.md`, `wave-function-collapse.md`, `dungeon-generation.md`, `seed-based-generation.md` |
| B32 | backend/unity-mobile-optimizer | `il2cpp-optimization.md`, `adaptive-performance.md`, `thermal-throttling.md`, `mobile-memory-budget.md` |
| B33 | backend/unity-console-platform | `platform-abstraction-layer.md`, `trc-xr-compliance.md`, `input-remapping-guide.md`, `platform-specific-code.md` |
| B34 | backend/unity-ecs-dots | `entities-component-guide.md`, `system-lifecycle.md`, `burst-compiler-guide.md`, `job-system-patterns.md` |
| B35 | backend/unity-2d-specialist | `sprite-renderer-guide.md`, `2d-physics-patterns.md`, `spine-animation.md`, `pixel-perfect-setup.md` |
| B36 | backend/unity-input-system | `input-action-maps.md`, `rebinding-ui.md`, `multi-device-support.md`, `touch-gesture-patterns.md` |
| B37 | backend/unity-camera-systems | `cinemachine-advanced-rigs.md`, `split-screen-setup.md`, `camera-stacking.md`, `custom-camera-controller.md` |
| B38 | backend/unity-memory-manager | `memory-profiler-workflow.md`, `gc-optimization.md`, `native-containers-guide.md`, `object-pooling-patterns.md` |
| B39 | backend/unity-testing | `playmode-test-guide.md`, `editmode-test-patterns.md`, `performance-test-framework.md`, `test-automation-ci.md` |
| B40 | backend/unity-cloud-services | `remote-config-guide.md`, `cloud-save-setup.md`, `unity-economy-package.md`, `leaderboard-implementation.md` |
| B41 | backend/unity-monetization | `iap-implementation.md`, `unity-ads-integration.md`, `ad-mediation.md`, `receipt-validation.md` |
| B42 | backend/unity-security-anticheat | `code-obfuscation-tools.md`, `memory-protection.md`, `server-side-validation.md`, `cheat-detection-patterns.md` |
| B43 | backend/unity-accessibility | `screen-reader-unity.md`, `colorblind-mode.md`, `input-accessibility.md`, `subtitle-system.md` |
| B44 | backend/unity-dialogue-system | `dialogue-tree-patterns.md`, `ink-integration.md`, `yarn-spinner-guide.md`, `localized-dialogue.md` |
| B45 | backend/unity-inventory-crafting | `inventory-system-design.md`, `item-database-scriptableobject.md`, `crafting-recipe-system.md`, `drag-drop-ui.md` |
| B46 | backend/unity-combat-system | `hitbox-hurtbox-system.md`, `damage-calculation.md`, `combo-system-design.md`, `status-effect-framework.md` |
| B47 | backend/unity-quest-mission | `quest-tracking-system.md`, `objective-framework.md`, `reward-distribution.md`, `quest-graph-editor.md` |
| B48 | backend/unity-game-economy | `virtual-currency-design.md`, `reward-loop-patterns.md`, `gacha-probability.md`, `progression-curve.md` |
| B49 | backend/unity-state-machine | `fsm-patterns-unity.md`, `hierarchical-state-machine.md`, `scriptableobject-states.md`, `game-state-management.md` |
| B50 | backend/unity-dependency-injection | `zenject-guide.md`, `vcontainer-patterns.md`, `service-locator-vs-di.md`, `testability-patterns.md` |
| B51 | backend/unity-asset-workflow | `addressables-advanced.md`, `asset-bundle-strategies.md`, `asset-postprocessor.md`, `import-preset-management.md` |
| B52 | backend/unity-streaming-open-world | `scene-streaming-patterns.md`, `additive-scene-loading.md`, `world-partitioning.md`, `async-loading-strategies.md` |

---

## ÇALIŞMA SIRASI

1. Önce backend düzeltmelerini yap (B7, B17)
2. Sonra kategorileri sırayla işle: Orchestrator → Code Review → Design → DevOps → Data → AI Ops → Jira → Research → Market Research → Marketing → Productivity → Prompt Eng → Sales → 3D/CAD → Unity iskeletler
3. Her agent için:
   a. Mevcut AGENT.md'yi oku
   b. Web'den araştır (agent'ın domain'i)
   c. AGENT.md body'sini doldur (frontmatter'a DOKUNMA)
   d. Knowledge dosyalarını oluştur (3 katmanlı format)
   e. `knowledge/_index.md`'yi güncelle
4. SADECE listelenen dosyaları oluştur/değiştir
5. DOKUNMA listesindeki agent'lara DOKUNMA

## DOĞRULAMA (bitince çalıştır)

```bash
# Placeholder kontrolü — hepsi 0 olmalı (`agents/_template` hariç)
echo "Bridge placeholder:" $(find agents -name AGENT.md ! -path "*/_template/*" | xargs grep -l "Hangi alanlarla" 2>/dev/null | wc -l)
echo "Output placeholder:" $(find agents -name AGENT.md ! -path "*/_template/*" | xargs grep -l "Ciktinin formati" 2>/dev/null | wc -l)
echo "Identity placeholder:" $(find agents -name AGENT.md ! -path "*/_template/*" | xargs grep -l "Cursor dolduracak" 2>/dev/null | wc -l)

# Knowledge dosya sayısı — en az ~660 hedef (agent başına ≥4 konu); güncel repo 800+ olabilir
echo "Knowledge files:" $(find agents -path "*/knowledge/*.md" ! -name "_index.md" | wc -l)

# 3 katmanlı format kontrolü
echo "With Quick Reference:" $(find agents -path "*/knowledge/*.md" ! -name "_index.md" | xargs grep -l "Quick Reference" 2>/dev/null | wc -l)
echo "With Deep Dive:" $(find agents -path "*/knowledge/*.md" ! -name "_index.md" | xargs grep -l "Deep Dive Sources" 2>/dev/null | wc -l)
```

Hedef: İlk 3 = 0 (template hariç), Knowledge files ≥ 660 ve büyüyen envanterle uyumlu, Quick Reference ve Deep Dive = Knowledge files ile aynı. Coverage özeti: `python3 scripts/agent_coverage_audit.py`.
