---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Chain-of-Thought Prompting

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

## Standard CoT

Force the model to reason step-by-step before answering.

```
Think step by step:
1. What is the current state?
2. What needs to change?
3. What are the risks?
4. What is the minimal change?
→ Then provide your answer.
```

**When to use:** Complex reasoning, math, multi-step logic, debugging.

**When NOT to use:** Simple lookups, formatting tasks, direct retrieval — CoT adds latency with no benefit.

## Tree-of-Thought

Explore multiple reasoning paths, evaluate each, pick the best.

```
Consider 3 approaches:
Approach A: [description] → Pros: ... Cons: ...
Approach B: [description] → Pros: ... Cons: ...
Approach C: [description] → Pros: ... Cons: ...
Best: [selected approach with reasoning]
```

Use for: design decisions, architecture choices, ambiguous requirements.

## Structured Reasoning Templates

### Triage Pattern
```
Symptom: [what's observed]
Hypothesis: [what might cause it]
Test: [how to verify]
Result: [what happened]
Conclusion: [root cause + fix]
```

### Planning Pattern
```
Goal: [what we're achieving]
Constraints: [what limits us]
Steps: [ordered actions]
Risks: [what could go wrong]
Mitigations: [how to handle risks]
```

### Decision Pattern
```
CONFUSION: [the ambiguity]
Options: A) ... B) ... C) ...
Trade-offs: [comparison]
Recommendation: [best option + why]
```

## Implicit vs Explicit CoT

- **Explicit:** "Let me think through this step by step..." (visible in output)
- **Implicit:** Extended thinking / internal reasoning (hidden from output)

For agent systems, prefer **implicit** CoT — users care about results, not reasoning. Use explicit only when the reasoning IS the deliverable (e.g., code review findings).

## CoT Triggers

Phrases that activate step-by-step reasoning:
- "Think step by step"
- "Before answering, consider..."
- "Walk through your reasoning"
- "Analyze this systematically"

## Anti-Patterns

| Anti-Pattern | Problem |
|-------------|---------|
| CoT on trivial tasks | Wastes tokens, adds latency |
| Unbounded reasoning | Model rambles without converging |
| No conclusion after reasoning | Steps listed but no answer given |
| CoT without structure | Random thoughts instead of systematic analysis |
