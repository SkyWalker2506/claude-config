# Worker W1 — Orchestrator

**Scope path:** `agents/orchestrator/`

**Skip:** `jarvis/` (A0 — dokunma)

**Agent klasörleri:** `lead-orchestrator`, `task-router`, `fallback-manager`, `token-budget-manager`, `context-pruner`, `daily-health-check`, `weekly-analyst`, `manual-control`, `art-lead`, `code-lead`, `growth-lead`, `biz-lead`, `sec-lead`

**Knowledge dosya adları (mega-prompt Orchestrator tablosu — id → klasör eşleşmesini yerelde kontrol et):**

| Klasör | Örnek knowledge (4 adet) |
|--------|---------------------------|
| lead-orchestrator | `strategic-planning.md`, `risk-assessment-framework.md`, `prioritization-methods.md`, `escalation-protocols.md` |
| task-router | `task-classification.md`, `capability-matching.md`, `dag-planning.md`, `load-balancing.md` |
| … | mega-prompt tablosunun devamı |

[WORKER_PROMPT.md](WORKER_PROMPT.md) şablonunu kullan; `{SCOPE}` = yukarıdaki path; `{SKIP}` = `jarvis`.
