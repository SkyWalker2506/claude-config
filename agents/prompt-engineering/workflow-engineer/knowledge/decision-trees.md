---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Decision Trees

## If/Then Rules

Simplest form — binary branching based on a condition.

```
Can reproduce the failure?
├── YES → Proceed to localize
└── NO → Gather more context, try minimal environment
```

Best for: triage flows, error handling, prerequisite checks.

## Scoring-Based Routing

Assign numeric scores, route based on threshold.

```
Review Score:
  correctness: 8/10
  readability: 7/10
  security: 9/10
  average: 8.0 → PASS (threshold: 7.0)
```

Use when: multiple dimensions matter, need weighted decisions.

## Threshold-Based Routing

Single metric gates the path forward.

```
Test coverage
├── ≥ 80% → proceed to deploy
├── 60-79% → warn, allow override
└── < 60% → block deployment
```

## LLM-Based Classification

When rules are too complex for static trees, use LLM judgment.

```
CONFUSION:
Spec says REST, codebase uses GraphQL.
Options:
A) Follow spec (REST)
B) Follow existing pattern (GraphQL)
C) Ask human
→ Surface options, let human decide
```

## Multi-Level Decision Trees

Chain decisions for complex routing.

```
Task type?
├── Bug fix
│   ├── Severity critical? → hotfix branch, skip queue
│   └── Normal → standard flow
├── Feature
│   ├── Has spec? → plan → implement
│   └── No spec → specify first
└── Refactor
    └── Has tests? → proceed : write tests first
```

## Practical Rules

1. **Exhaust static rules first** — LLM judgment is expensive
2. **Max 3-4 levels deep** — deeper trees are hard to maintain
3. **Always have a fallback/else** — unhandled cases cause silent failures
4. **Document thresholds** — magic numbers without context are tech debt
5. **Prefer explicit options over open-ended** — "A, B, or C?" beats "what should we do?"
