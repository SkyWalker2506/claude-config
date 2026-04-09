# Mega rollout — batch manifest

Kaynak: [mega-prompt.md](mega-prompt.md). **Frontmatter / status dokunma.** Sadece `AGENT.md` body + `knowledge/*.md` + `_index.md`.

## DOKUNMA (değiştirme)

| ID | Path |
|----|------|
| A0 | `agents/orchestrator/jarvis/` |
| B3 | `agents/backend/frontend-coder/` |
| B15 | `agents/backend/mobile-dev-agent/` |
| D1 | `agents/design/ui-ux-researcher/` |
| D2 | `agents/design/design-system-agent/` |
| D10 | `agents/design/motion-graphics-agent/` |
| J10 | `agents/devops/github-manager/` |
| K9 | `agents/research/ai-tool-evaluator/` |
| N1 | `agents/prompt-engineering/prompt-engineer/` |
| N6 | `agents/prompt-engineering/ai-systems-architect/` |
| N7 | `agents/prompt-engineering/skill-design-specialist/` |
| N8 | `agents/prompt-engineering/workflow-engineer/` |
| B22 | `agents/backend/unity-shader-developer/` |
| B23 | `agents/backend/unity-multiplayer/` |
| E6 | `agents/3d-cad/unity-vfx-animation/` |
| E7 | `agents/3d-cad/unity-technical-artist/` |
| C7 | `agents/code-review/unity-code-reviewer/` |

---

## Paralel worker (15 Composer oturumu — her biri ayrı chat)

Şablon: [mega-workers/WORKER_PROMPT.md](mega-workers/WORKER_PROMPT.md) · İndeks: [mega-workers/README.md](mega-workers/README.md)

| Worker | Prompt dosyası | Klasörler (repo kökü `~/Projects/claude-config`) | Tahmini agent |
|--------|----------------|---------------------------------------------------|---------------|
| **W1** | [W1-orchestrator.md](mega-workers/W1-orchestrator.md) | `agents/orchestrator/*` **hariç** `jarvis/` | 13 |
| **W2** | [W2-code-review.md](mega-workers/W2-code-review.md) | `agents/code-review/*` **hariç** `unity-code-reviewer/` | 6 |
| **W3** | [W3-design.md](mega-workers/W3-design.md) | `agents/design/*` **hariç** `ui-ux-researcher`, `design-system-agent`, `motion-graphics-agent` | 10 |
| **W4** | [W4-devops.md](mega-workers/W4-devops.md) | `agents/devops/*` **hariç** `github-manager/` | 11 |
| **W5** | [W5-data-analytics.md](mega-workers/W5-data-analytics.md) | `agents/data-analytics/` | 13 |
| **W6** | [W6-ai-ops.md](mega-workers/W6-ai-ops.md) | `agents/ai-ops/` | 12 |
| **W7** | [W7-jira-pm.md](mega-workers/W7-jira-pm.md) | `agents/jira-pm/` | 10 |
| **W8** | [W8-research.md](mega-workers/W8-research.md) | `agents/research/*` **hariç** `ai-tool-evaluator/` | 14 |
| **W9** | [W9-market-research.md](mega-workers/W9-market-research.md) | `agents/market-research/` | 16 |
| **W10** | [W10-marketing-engine.md](mega-workers/W10-marketing-engine.md) | `agents/marketing-engine/` | 4 |
| **W11** | [W11-productivity.md](mega-workers/W11-productivity.md) | `agents/productivity/` | 6 |
| **W12** | [W12-agent-builder.md](mega-workers/W12-agent-builder.md) | `agents/prompt-engineering/agent-builder/` (N2) | 1 |
| **W13** | [W13-sales-bizdev.md](mega-workers/W13-sales-bizdev.md) | `agents/sales-bizdev/` | 5 |
| **W14** | [W14-3d-cad.md](mega-workers/W14-3d-cad.md) | `agents/3d-cad/*` **hariç** `unity-vfx-animation`, `unity-technical-artist` | 10 |
| **W15** | [W15-unity-backend-skeleton.md](mega-workers/W15-unity-backend-skeleton.md) | `agents/backend/unity-*` (B3/B15/B22/B23 hariç) | ~27 |

**Not:** Repo’daki orchestrator ID eşlemesi mega tablodan farklı olabilir (`art-lead` = A9, `code-lead` = A10, …). Her zaman `AGENT.md` frontmatter `id` alanına güven.

---

## Sıralı batch (tek oturumda sırayla)

| Batch | İçerik |
|-------|--------|
| 1 | W1 Orchestrator |
| 2 | W2 Code review |
| 3 | W3 Design |
| 4 | W4 DevOps |
| 5 | W5 Data analytics |
| 6 | W6 AI Ops |
| 7 | W7 Jira/PM |
| 8 | W8 Research |
| 9 | W9 Market research |
| 10 | W10 Marketing |
| 11 | W11 Productivity |
| 12 | W12 Agent builder (N2) |
| 13 | W13 Sales |
| 14 | W14 3D/CAD |
| 15 | W15 Unity backend iskelet |

---

## Doğrulama (bitiş)

```bash
~/Projects/claude-config/bin/mega-rollout.sh verify
```

---

## Knowledge dosya adları

Her agent için tam dosya listesi [mega-prompt.md](mega-prompt.md) içindeki tablolarda (Orchestrator → … → Unity).
