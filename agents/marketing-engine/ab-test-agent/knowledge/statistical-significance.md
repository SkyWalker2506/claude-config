---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Statistical Significance for Experiments

## Quick Reference

- **Significance** answers: “If there were no real difference, how surprising is this data?”—not “probability B is better.”
- **α (alpha):** False positive rate you tolerate—often 0.05 two-sided for exploratory; stricter for irreversible launches.
- **β / power:** `1 - β` = probability of detecting effect of size MDE if it exists—80% common minimum.
- **Bridge to M4:** Conversion counts come from **M4** event pipelines—validate deduplication (`transaction_id`, `user_pseudo_id`) before trusting rates.
- **Bridge to M2:** If metric is *form submits*, ensure **M2** didn’t change field validation mid-test.

| Metric type | Typical model | Notes |
|-------------|----------------|-------|
| Conversion rate | Binomial / z-test | Watch variance if cluster by user |
| Revenue per user | Bootstrap / t-test | Heavy tails—robust stats |
| Count data | Poisson / negative binomial | Rare events |

## Patterns & Decision Matrix

| Situation | Approach |
|-----------|----------|
| Low base rate | Need larger n; consider composite metric |
| Network effects | User-level diversion may be biased—cluster or geo holdouts |
| Multiple comparisons | Bonferroni, BH-FDR, or pre-register hierarchy |

**Confidence interval reporting**

> Report point estimate **and** 95% CI—e.g. “+3.1% relative lift, 95% CI [−0.4%, +6.8%]”—communicates uncertainty to PMs.

## Code Examples

**1) Pooled two-proportion (Python sketch)**

```python
from math import sqrt

def pooled_z(p1, n1, p2, n2):
    p = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return (p1 - p2) / se
```

**2) Relative lift**

```text
lift_rel = (p_treat - p_ctrl) / p_ctrl
```

## Anti-Patterns

- **Declaring winner** when CI crosses zero—noise.
- **Ignoring multiple testing** across 20 metrics—one will “win” by chance.
- **Segment mining** post hoc without correction—false discoveries.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Evan Miller — Chi-squared](https://www.evanmiller.org/ab-testing/chi-squared.html) — proportions intuition
- [Statsig — Stats engine docs](https://docs.statsig.com/stats_engine) — modern platform framing
- [OpenIntro Statistics — Inference](https://www.openintro.org/book/os/) — free textbook foundation
- [Wasserman — All of Statistics](https://www.stat.cmu.edu/~larry/all-of-statistics/) — rigorous backup
