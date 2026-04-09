---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Workflow Patterns

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

## Sequential

Tasks execute one after another. Output of step N feeds step N+1.

```
specify → plan → tasks → implement → review → ship
```

**When to use:** Dependencies between steps are strict; each step needs prior output.

## Parallel

Independent tasks run simultaneously, merge at a sync point.

```
[T005 model] ──┐
[T006 service]─┤→ integration
[T007 UI] ─────┘
```

**Mark with `[P]`** in task lists. Constraint: tasks must touch different files.

## Gated (Checkpoint)

Execution pauses at a gate until validation passes.

```
build → [GATE: tests pass?] → deploy → [GATE: smoke test?] → release
```

Real example from spec-kit: checklists must all PASS before `/implement` proceeds.

## Iterative (Loop)

Repeat a cycle until exit condition is met.

```
implement → test → fail? → debug → implement → test → pass ✓
```

The increment cycle: implement → test → verify → commit → next slice.
Max iterations should be bounded (e.g., 3 retries for validation).

## Event-Driven

Hooks fire on events rather than following a fixed sequence.

```
before_specify → [specify runs] → after_specify
before_implement → [implement runs] → after_implement
```

Extension hooks in `.specify/extensions.yml` follow this pattern.
Hooks can be mandatory (auto-execute) or optional (user-triggered).

## Hybrid Patterns

Most real workflows combine patterns:

```
sequential phases → parallel tasks within phase → gated phase transition
```

Example: Setup (sequential) → User Stories (parallel per story) → Polish (sequential) → Review (gated).

## Selection Criteria

| Pattern | Use When |
|---------|----------|
| Sequential | Strict data dependency between steps |
| Parallel | Independent tasks, different files |
| Gated | Quality/safety checkpoints needed |
| Iterative | Fix-verify loops, refinement cycles |
| Event-driven | Extensible pipelines, plugin systems |
