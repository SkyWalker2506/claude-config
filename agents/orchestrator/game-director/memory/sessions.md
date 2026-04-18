# Game Director — Session Log

## Overview

Log of each Director_Ship execution: GDD parsed, DAG built, waves dispatched, refinement loops, final state, decisions.

---

## Session Format

```
## Session {N} — {GDD Title}

**Date:** YYYY-MM-DD HH:MM:SS  
**GDD Path:** /path/to/gdd.md  
**Final Polish Score:** X.X/10

### GDD Summary
- Pitch: [1-liner]
- Scope: [micro/short/medium/long]
- Key mechanics: [list]
- Art style: [retro/modern/etc.]

### DAG & Waves
- Total waves: N
- Critical path length: M minutes
- Estimated build time: T minutes

### Execution Log

#### Wave 0 — Foundation
- Tasks: [list]
- Status: ✓ PASS | ✗ FAIL
- Notes: [key observations]
- Duration: Tm

#### Wave 1 — Structure
- Tasks: [list]
- Status: ✓ PASS
- Notes: [key observations]
- Duration: Tm

...

### Refinement Loops
- Loop 1: [criterion failed] → [fix applied by family X] → [new score]
- Loop 2: ...

### Final Playtest Results
- Scenario: smoke | combat | exploration
- fps_avg: XX
- Crashes: 0
- Stability: PASS

### Decisions & Learnings
- Decision 1: [what, why, outcome]
- Insight 1: [for memory/learnings.md]

### Artifacts
- Scene path: Assets/Scenes/...
- Build: /Builds/...
- Screenshots: Assets/Screenshots/session_{N}_...

---
```

## Previous Sessions

(Leave empty — filled on first run)
