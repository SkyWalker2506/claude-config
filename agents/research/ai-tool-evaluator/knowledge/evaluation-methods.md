---
last_updated: 2026-04-09
refined_by: opus
confidence: high
---

# Evaluation Methods

## Benchmark Methodology

### Standard Benchmarks

| Benchmark | What It Tests | Industry Standard |
|-----------|--------------|-------------------|
| SWE-bench Verified | Real GitHub issue resolution | Yes — top agents >80% |
| HumanEval | Code generation correctness | Yes, but saturated |
| LongMemEval | Memory system accuracy | Emerging |
| MMLU | General knowledge | Yes, but less relevant for coding |

### Custom Benchmarks (Our Approach)

**Hi-Test:** Quick model health check
- Send Turkish greeting
- Score response quality, latency, availability
- Run periodically to track model status

**Task-Based Eval:** Real-world task completion
- Pick 5 representative tasks from recent sprints
- Run each with candidate tool/model
- Score: correctness, time, cost, human intervention needed

## Scoring Rubric

### 5-Axis Evaluation (for tools/agents)

| Axis | Weight | Scoring |
|------|--------|---------|
| Quality | 30% | Output correctness, code quality |
| Cost | 25% | $/task, subscription cost |
| Speed | 20% | Time to completion |
| Autonomy | 15% | Human interventions needed |
| Integration | 10% | Fits our stack, setup effort |

Score each axis 1-10, apply weights, total out of 10.

### Decision Thresholds

```
Score ≥ 8.0  → Adopt immediately
Score 6.0-7.9 → Evaluate further, pilot
Score 4.0-5.9 → Monitor, don't adopt yet
Score < 4.0  → Reject
```

## Bias Prevention

### Common Evaluation Biases

| Bias | Description | Mitigation |
|------|------------|------------|
| Recency | Favoring newest tool | Compare against established baseline |
| Hype | Social media influence | Use benchmarks, not testimonials |
| Sunk cost | Keeping current tool despite better alternatives | Evaluate objectively |
| Cherry-picking | Testing only favorable scenarios | Use standardized task set |
| Anchor | First impression dominates | Evaluate over multiple sessions |

### Mitigation Strategies

1. **Standardized test set** — same tasks for all candidates
2. **Blind evaluation** — score output quality without knowing which tool produced it
3. **Multiple evaluators** — don't rely on one person's opinion
4. **Time-boxed trials** — 1-week pilot before commitment
5. **Document reasoning** — write down WHY you scored each axis

## Evaluation Template

```markdown
# Tool Evaluation: [Name]

**Date:** [YYYY-MM-DD]
**Evaluator:** [who]
**Category:** [coding agent / framework / memory / model]

## Scores
- Quality: X/10 — [justification]
- Cost: X/10 — [justification]
- Speed: X/10 — [justification]
- Autonomy: X/10 — [justification]
- Integration: X/10 — [justification]
- **Weighted Total: X.X/10**

## Verdict: [Adopt / Pilot / Monitor / Reject]
## Notes: [key observations]
```
