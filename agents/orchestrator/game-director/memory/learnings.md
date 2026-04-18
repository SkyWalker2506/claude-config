# Game Director — Learnings & Insights

## Overview

Cross-session learnings: patterns observed, optimizations, common pitfalls, GDD design tips.

---

## Format

Each entry:
```
### Insight: [Topic]

**Observed in:** Session N (GDD: Title)  
**Pattern:** [What was observed]  
**Root cause:** [Why it happened]  
**Recommendation:** [How to avoid next time]  
**Impact:** [High/Medium/Low] — affects polish score, iteration count, wall-clock time
```

---

## Template Entries

(Leave empty — populated after first few runs)

### Insight: Audio Direction Often Incomplete

**Pattern:** Music present but SFX missing for key events (spawn, collision, death)  
**Root cause:** GDD audio section lists music + ambience but doesn't detail SFX per mechanic  
**Recommendation:** Add SFX audit step to GDD parsing; verify ≥ 3 SFX defined for mechanics  
**Impact:** High — audio presence is criterion 5; missing SFX costs 2–3 polish points

### Insight: NavMesh Bake Timing Critical

**Pattern:** Wave dependencies showed NavMesh bake can block both AI and pathfinding optimizations  
**Root cause:** If bake omitted from Wave 0, entire Wave 1+ slips  
**Recommendation:** Make NavMesh bake mandatory Wave 0 task if any enemy AI or navigation exists  
**Impact:** Medium — affects wave schedule; adds 3–5 minutes if delayed

### Insight: Vision Feedback is Worth the Time

**Pattern:** G13 critique catches visual issues (asset mismatches, UI contrast) that would fail playtest  
**Root cause:** Developer's eye becomes blind to accumulating visual debt  
**Recommendation:** Run G13 critique after every wave (not just failures); worth 2–3 min per wave  
**Impact:** High — prevents failed polish scores; saves iteration loops

---

## Key Patterns

(To be filled after runs)

- Polish score rarely exceeds 8.5 without E9 (cinematic director) involvement
- Mobile playtest perf often fails on texture compression step (B53); do early
- Placeholder art coherence improves dramatically with unified color palette
- Audio presence + responsive input are highest-ROI improvements for polish
