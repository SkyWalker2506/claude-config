---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Token Optimization

## Compression Techniques

### Remove Filler
```
# BAD (wasteful)
"Please kindly read the following file and provide a comprehensive analysis"

# GOOD (compressed)
"Read file. Analyze."
```

### Use Tables Over Prose
Tables convey structured info in fewer tokens than paragraphs.

### Abbreviate Repeated Patterns
Define once, reference by name:
```
## Patterns
- SIMPLICITY CHECK: Can this be done in fewer lines?
[... then later ...]
Run SIMPLICITY CHECK.
```

## Layered Loading (L0/L1/L2)

### L0 — Always Loaded
Core rules, persona, critical constraints. Under 100 lines.
Example: CLAUDE.md top-level rules.

### L1 — On-Demand
Loaded when a specific task type is detected.
Example: skill files loaded via `/skill-name`, agent knowledge loaded at dispatch.

### L2 — Deep Reference
Loaded only when explicitly needed for a specific question.
Example: full API docs, large code files, historical data.

```
L0: CLAUDE.md (always)          ~100 lines
L1: SKILL.md (per task)         ~200 lines
L2: Full source file (per edit) ~variable
```

### Loading Strategy
1. Start with L0 only
2. Detect task type → load relevant L1
3. Need specific detail → load L2 slice (not entire file)

## Token Reduction Tactics

| Tactic | Savings |
|--------|---------|
| Short sentences (3-6 words) | 30-50% vs verbose |
| Tables instead of lists | 20-30% for structured data |
| Remove examples that add no new info | 10-40% |
| Trim context to task-relevant only | 50-80% |
| Use file references instead of inline content | Variable |

## Context Window Budget

```
System prompt:    ~2K tokens (L0)
Task context:     ~3K tokens (L1 + relevant files)
Working memory:   ~5K tokens (conversation so far)
Reserved for output: ~2K tokens
```

Total budget per turn should leave generous output room.

## Anti-Patterns

- **Loading everything** — 5000 lines of context when task needs 50
- **Repeating instructions** — saying the same rule 3 different ways
- **Inline large files** — paste entire file when only 5 lines matter
- **No pruning** — context grows unbounded across conversation turns
