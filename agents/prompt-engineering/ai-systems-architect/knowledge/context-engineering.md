---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Context Engineering

## Quick Reference
| Kavram | Not |
|--------|-----|
| Özet | Aşağıdaki bölümlerde bu konunun detayı ve örnekleri yer alır. |
| Bağlam | Proje sürümüne göre güncelleyin. |

## Patterns & Decision Matrix
| Durum | Öneri |
|-------|-------|
| Karar gerekiyor | Bu dosyadaki tablolar ve alt başlıklara bakın |
| Risk | Küçük adım, ölçüm, geri alınabilir değişiklik |

## Code Examples
Bu dosyanın devamındaki kod ve yapılandırma blokları geçerlidir.

## Anti-Patterns
- Bağlam olmadan dışarıdan kopyalanan desenler.
- Ölçüm ve doğrulama olmadan prod'a taşımak.

## Deep Dive Sources
- Bu dosyanın mevcut bölümleri; resmi dokümantasyon ve proje kaynakları.

---

> Context is the single biggest lever for agent output quality — too little and the agent hallucinates, too much and it loses focus.

## The Context Hierarchy (from agent-skills)

```
Layer 1: Rules Files (CLAUDE.md)        — Always loaded, project-wide
Layer 2: Spec / Architecture Docs       — Loaded per feature/session
Layer 3: Relevant Source Files           — Loaded per task
Layer 4: Error Output / Test Results     — Loaded per iteration
Layer 5: Conversation History            — Accumulates, compacts
```

## Layered Loading Strategy

### L0 — Bootstrap (zero-cost)
- Global CLAUDE.md redirector → reads config CLAUDE.md
- Project CLAUDE.md with conventions, commands, boundaries
- Cost: ~500-1000 tokens, always worth it

### L1 — On-Demand Project Context
- `_index.md` files listing available knowledge topics
- Agent reads index, loads only relevant files
- Cost: Index ~100 tokens; each topic ~200-500 tokens

### L2 — Task-Specific Loading
- Read only files relevant to current task
- Use `jCodeMunch` or grep to find related symbols
- Never dump entire codebase — load surgical slices

### L3 — Iterative Refinement
- Test output, error messages, diff results
- Compact: only include failing test name + error, not full stack

## Token Budget Management

| Model | Context Window | Usable Budget | Reserve |
|-------|---------------|---------------|---------|
| Opus 4 | 200K | ~150K effective | 50K for output |
| Sonnet 4 | 200K | ~150K effective | 50K for output |
| Haiku 3.5 | 200K | ~150K effective | 50K for output |

**Rule of thumb**: Keep active context under 40K tokens for best quality. Quality degrades as context grows — the "lost in the middle" effect.

## Lazy-Load Patterns

### Pattern: Knowledge Index
```markdown
# knowledge/_index.md
- [Topic A](topic-a.md) — one-line description
- [Topic B](topic-b.md) — one-line description
```
Agent reads index (~100 tokens), loads only needed files.

### Pattern: Progressive Disclosure
1. Start with summary/overview
2. Agent requests detail only when needed
3. Never pre-load "just in case"

### Pattern: Context Compaction
- After N iterations, summarize conversation so far
- Replace verbose output with key findings
- Archive resolved threads

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Dump entire repo | Blows budget, loses focus | Surgical file loading |
| Repeat instructions every message | Wastes tokens | Put in CLAUDE.md (loaded once) |
| Include full stack traces | Noise | Extract error message + line |
| Load all docs "just in case" | Dilutes signal | Index + lazy-load |
| No rules file | Agent reinvents conventions | Write CLAUDE.md on day one |

## Context Quality Signals

- **Agent follows conventions**: Context is working
- **Agent hallucmates APIs**: Missing L1 (rules) or L2 (source)
- **Agent loses thread**: Context too large — compact or split task
- **Agent asks redundant questions**: Missing persistent context (CLAUDE.md)

## 2026 Context Engineering Advances

### Manus Context Engineering (5 principles)

1. KV-cache hit rate is #1 metric — stable system prompts, append-only contexts
2. Mask tools (don't remove) — cache stability while controlling behavior
3. Filesystem as extended memory — `working_memory.json`, `todo.md` instead of compressing
4. `todo.md` recitation — agent rewrites `todo.md` continuously, keeps plan in attention window
5. Preserve error traces — don't hide failures, models learn from visible mistakes

### NLH Three-Layer Separation (Tingua, March 2026)

- Layer 1: Harness Logic — task-family control (roles, stages, verification gates)
- Layer 2: Runtime Charter — shared execution semantics and policies
- Layer 3: Deterministic Scripts — tools, tests, adapters (file-backed)
- Representation change alone: +16.8 benchmark points, runtime 361→141 min, LLM calls 1200→34

### Execution Contracts

- Required outputs (file paths, artifacts)
- Token/tool-call budgets
- Completion conditions (gates)
- Permissions and artifact output paths
- Like function signatures for agent calls

### AgentSpec Safety DSL

- Declarative rules: trigger → check → enforce
- Prevented 90%+ unsafe executions with millisecond overhead
