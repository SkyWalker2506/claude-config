# Game Director — Polish Scores Archive

## Overview

Persistent log of final polish scores per GDD shipped. Tracks score distribution and trends over time.

---

## Schema

```json
{
  "date": "YYYY-MM-DD",
  "gdd_name": "Game Title",
  "gdd_path": "/path/to/gdd.md",
  "final_score": 8.4,
  "iteration_count": 2,
  "wall_clock_minutes": 22,
  "per_criterion": {
    "ui_legibility": 9,
    "level_navigability": 8,
    "asset_coherence": 7,
    "responsiveness": 10,
    "audio_presence": 6,
    "cinematography": 8,
    "performance_stability": 9,
    "stability_crashes": 10,
    "visual_hierarchy": 9,
    "shippable_feel": 8
  },
  "lowest_criterion": "audio_presence (6)",
  "highest_criterion": "responsiveness (10)",
  "refined_criteria": [
    "audio_presence (spawn SFX added)"
  ]
}
```

---

## Scores

(Leave empty — populated after first run)

H1 (Header): Date | GDD Name | Score | Iterations | Wall-Clock | Lowest Criterion
---|---|---|---|---|---
2026-04-18 | Mushroom Arena | 8.4 | 2 | 22m | Audio (6)
... | ... | ... | ... | ... | ...

---

## Analysis (Auto-Updated)

**Total Shipped:** N  
**Average Score:** X.X/10  
**Score Distribution:**
- 9–10: N%
- 8–8.9: N%
- 7–7.9: N%
- < 7: N%

**Most Common Lowest Criterion:** [criterion] (appears in M% of runs)  
**Average Iterations:** X  
**Average Wall-Clock Time:** Y minutes

---

## Notes

All scores target ≥ 8.0/10 for "shippable demo" status.  
Iterate on scores < 5 (threshold fail) or < 7 (optional refinement).
