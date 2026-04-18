# Game Director Knowledge Index

> Lazy-load reference for A14 Game Director agent. Load files on-demand per task phase.

**Last Updated:** 2026-04-18  
**Total Topics:** 5

---

## Topics

| # | Topic | File | Phase | Purpose |
|---|-------|------|-------|---------|
| 1 | GDD Structure & Parsing | `gdd-structure.md` | Phase 1 (Parse) | Expected GDD sections, YAML + markdown dual-format, example GDD |
| 2 | Task Graph Generation | `task-graph-generation.md` | Phase 1 (DAG) | DAG building rules, wave assignment, dependency edges, parallel-safe grouping |
| 3 | Polish Score Rubric | `polish-score-rubric.md` | Phase 2–3 (Feedback) | 10-criterion scorecard, vision-agent critique drivers, acceptance threshold (≥ 8/10 avg) |
| 4 | Vision Feedback Loop | `vision-feedback-patterns.md` | Phase 2 (Critique) | Capture cadence, screenshot targets, critique templates, per-criterion scoring |
| 5 | Playtest Orchestration | `playtest-orchestration.md` | Phase 3 (Test) | Enter Play Mode, simulate inputs, profile sampling, crash detection, perf metrics |

---

## Load Order (Recommended)

1. **Start:** `gdd-structure.md` — understand GDD format before Phase 1
2. **Before DAG:** `task-graph-generation.md` — know blocking edges, waves
3. **Before Feedback:** `polish-score-rubric.md` + `vision-feedback-patterns.md` — understand scoring and capture targets
4. **Before Playtest:** `playtest-orchestration.md` — know input simulation, perf thresholds

---

## Cross-References

- **SKILL.md** (`/Users/musabkara/Projects/ccplugin-unity-craft/skills/unity-craft/SKILL.md`) — 10 tool families, dispatch protocol
- **tool/game-director.md** (`/Users/musabkara/Projects/ccplugin-unity-craft/skills/unity-craft/tools/game-director.md`) — tool signatures (Director_ParseGDD, Director_PlanGame, Director_ExecutePlan, Director_Critique, Director_Playtest, Director_Ship)
- **E9 agent** (Cinematic Director) — Cinema + PostFX presets, vision feedback capture via G13
- **G13 agent** (Vision Action Operator) — screenshot analysis, critique scoring
- **B53 agent** (Performance Analyzer) — playtest metrics, optimization dispatch

---

## Memory Files

- **`memory/sessions.md`** — Decisions per run: GDD parsed, DAG built, waves dispatched, refinement loops, final ship state
- **`memory/learnings.md`** — Insights: "Designer often misses audio direction" → add GDD validation; "Polish score rarely exceeds 8.5 without E9 revisions"
- **`memory/polish-scores.md`** — Persistent scorecard log: date, gdd_name, final_score, per-criterion breakdown, iteration count

---

## Quick Start

For a new GDD:
1. Read `gdd-structure.md` → verify input has all 9 sections
2. Read `task-graph-generation.md` → build DAG
3. Dispatch waves per DAG
4. After each wave, read `vision-feedback-patterns.md` + invoke G13 for critique
5. Read `playtest-orchestration.md` → run canonical playtest scenarios
6. If polish < 8/10, loop: refine GDD → rebuild DAG → redispatch
7. When done, log to `memory/polish-scores.md`
