# Polish Score Rubric

## Overview

A 10-criterion scorecard for evaluating demo polish. Target: **≥ 8/10 average** across all criteria, with **no single criterion < 5**. Vision agent (G13) drives most scoring via screenshot analysis + design critique.

---

## The 10 Criteria

### 1. UI Legibility (0–10)

**Definition:** Can the player read all on-screen text and understand UI purpose?

| Score | Indicator |
|-------|-----------|
| 10 | All text clear, good contrast, appropriate font size for distance, no overlaps |
| 8–9 | Text mostly clear; minor contrast issue or one label hard to read at distance |
| 6–7 | Text readable but requires attention; some contrast issues; font size inconsistent |
| 4–5 | Text hard to read; poor contrast; font sizes vary wildly |
| 0–3 | Text illegible; invisible labels; no UI hierarchy |

**Vision Check:** Capture HUD screenshot at game resolution, check fonts at pixel level, assess contrast ratios.

---

### 2. Level Navigability (0–10)

**Definition:** Can the player move through level geometry intuitively? Are obstacles clear? Spawn points obvious?

| Score | Indicator |
|-------|-----------|
| 10 | Clear paths, obstacles well-lit, spawn point obvious, no confusing dead ends |
| 8–9 | Mostly clear; one small navigation confusion or dim corner |
| 6–7 | Generally navigable but has confusing areas; needs learning curve |
| 4–5 | Player can navigate but gets stuck; multiple confusing corners; unclear spawn |
| 0–3 | Unplayable; player stuck in level frequently; geometry blocking progression |

**Vision Check:** Capture game view from multiple VCam angles, check lighting, measure sightlines to key objectives.

---

### 3. Asset Coherence (0–10)

**Definition:** Do all visual elements (models, textures, colors, materials) feel like they belong in the same game?

| Score | Indicator |
|-------|-----------|
| 10 | Cohesive color palette, consistent style (all retro or all modern), texture coherence |
| 8–9 | Mostly cohesive; one asset style mismatch (e.g., one HD texture in pixel game) |
| 6–7 | Generally cohesive; a few mismatches that don't break immersion |
| 4–5 | Noticeable style clashes; mix of art eras (80s + 2020s); jarring |
| 0–3 | Chaotic; no unified aesthetic; looks like random asset dump |

**Vision Check:** Screenshot scene view, analyze color histogram, check material assignments, compare style across prefabs.

---

### 4. Responsiveness (0–10)

**Definition:** How quickly does the game react to player input? Is there lag?

| Score | Indicator |
|-------|-----------|
| 10 | < 30ms input-to-action latency; snappy feel |
| 8–9 | 30–50ms latency; minor delay but acceptable |
| 6–7 | 50–100ms latency; noticeable but playable |
| 4–5 | 100–150ms latency; gameplay affected; frustrating |
| 0–3 | > 150ms latency; unplayable; player can't control character |

**Playtest Check:** Use Profiler InputQueue timing; simulate inputs during canonical playtest, measure frame time on input.

---

### 5. Audio Presence (0–10)

**Definition:** Is audio present, mixed well, and enhancing gameplay/mood?

| Score | Indicator |
|-------|-----------|
| 10 | Music + SFX + ambience all present, well-balanced mix, no clipping, matches mood |
| 8–9 | Most audio present; one element missing or slightly off-balance |
| 6–7 | Core audio (music + key SFX) present; some gaps or mix issues |
| 4–5 | Minimal audio; only music or only SFX; awkward mix |
| 0–3 | Silent or broken audio; no music loop; SFX absent |

**Vision Check:** In-game playtest, listen for music loop, SFX on key events (spawn, fire, death), check volume levels in AudioMixer.

---

### 6. Cinematography (0–10)

**Definition:** Is the camera framing appealing? Does it show the action well? Any jarring cuts or poor composition?

| Score | Indicator |
|-------|-----------|
| 10 | Framing always shows key action, composition balanced, smooth camera transitions |
| 8–9 | Good framing; minor composition quirk or one awkward cut |
| 6–7 | Action generally visible; camera occasionally misses important moment; transitions adequate |
| 4–5 | Action sometimes off-screen; poor composition; jerky transitions |
| 0–3 | Camera broken; player off-screen; unplayable camera |

**Vision Check:** Capture game view from active VCam, assess framing of player + enemies, check for clipping into geometry.

---

### 7. Performance Stability (0–10)

**Definition:** Does the game maintain target FPS without stuttering or frame drops?

| Score | Indicator |
|-------|-----------|
| 10 | Maintains 60 FPS (desktop) or 30 FPS (mobile) consistently; no frame drops |
| 8–9 | Mostly stable; occasional frame dip (1–2 frames) |
| 6–7 | Generally stable; periodic frame dips (3–5 frames); playable |
| 4–5 | Frequent stuttering; frame drops every 5–10 seconds |
| 0–3 | Unstable; constant frame drops; unplayable |

**Playtest Check:** Run Profiler during canonical 30s scenario, sample fps_avg and fps_p95.

---

### 8. Stability (Crashes / Errors) (0–10)

**Definition:** Does the game run without crashing? Are console errors minimal?

| Score | Indicator |
|-------|-----------|
| 10 | Zero crashes, zero console errors in 5-minute canonical playthrough |
| 8–9 | Zero crashes; 1–3 minor warnings (non-functional) |
| 6–7 | Zero crashes; < 5 errors (some may affect minor features) |
| 4–5 | Occasional crash (once per 5 playthroughs) or consistent errors affecting gameplay |
| 0–3 | Frequent crashes or breaking errors |

**Playtest Check:** Monitor Console during full playthrough, note error count and severity.

---

### 9. Visual Hierarchy (0–10)

**Definition:** Can the player easily distinguish important elements (player, enemies, objectives) from background?

| Score | Indicator |
|-------|-----------|
| 10 | Player/enemies/objectives all clearly distinct; perfect contrast and scale |
| 8–9 | Mostly clear; one element slightly hard to pick out |
| 6–7 | Generally distinguishable; takes a moment to spot all key elements |
| 4–5 | Difficult to distinguish player from enemies or find objective |
| 0–3 | Indistinguishable; can't tell what's what |

**Vision Check:** Screenshot game view, apply edge-detection filter, assess whether key actors stand out.

---

### 10. Shippable Feel (0–10)

**Definition:** Overall, does this feel like a polished (even if placeholder-art) demo you'd show to others?

| Score | Indicator |
|-------|-----------|
| 10 | Feels complete, cohesive, and intentional; would share without apology |
| 8–9 | Mostly polished; feels intentional; minor rough edges acceptable |
| 6–7 | Playable and fun; rough around edges but core vision clear |
| 4–5 | Rough prototype; works but feels incomplete |
| 0–3 | Unfinished; feels like work-in-progress; not ready to show |

**Holistic Check:** Play through once as a user, assess overall feel. Can you describe what this game *is* to someone else?

---

## Scoring Workflow

### Step 1: Vision Agent Critique (G13)

After each wave, invoke G13 with:

```
goal: "Critique the current game state against these 10 criteria"
scope: ["UI Legibility", "Level Navigability", "Asset Coherence", "Responsiveness", "Audio Presence", "Cinematography", "Performance Stability", "Stability (Crashes)", "Visual Hierarchy", "Shippable Feel"]
targets:
  - scene_view_screenshot: "Assets/Screenshots/wave_{N}_scene.png"
  - game_view_screenshot: "Assets/Screenshots/wave_{N}_game.png"
  - playtest_profiler: "Profiler data from canonical scenario"
```

**Response Format:**

```json
{
  "scores": {
    "ui_legibility": 8,
    "level_navigability": 7,
    "asset_coherence": 8,
    "responsiveness": 9,
    "audio_presence": 6,
    "cinematography": 8,
    "performance_stability": 9,
    "stability_crashes": 10,
    "visual_hierarchy": 8,
    "shippable_feel": 7
  },
  "average_score": 7.9,
  "per_criterion_notes": {
    "audio_presence": "Missing SFX for enemy spawn events; only music present"
  },
  "recommendation": "Audio presence below threshold; spawn B26 to add SFX library import"
}
```

### Step 2: Threshold Check

```
avg_score = sum(scores.values()) / 10

if avg_score < 5 or min(scores.values()) < 2:
  → CRITICAL: Halt wave dispatch, escalate to A1
  
if avg_score < 7 or any score < 4:
  → REFINEMENT: Spawn fix tasks, restart affected wave
  
if avg_score >= 8 and all scores >= 5:
  → POLISH: Ship candidate (pending playtest)
```

### Step 3: Iterate (if needed)

If refinement triggered:

1. Analyze which criteria failed
2. Match failures to tool families (e.g., "Audio Presence" → B26 Audio Engineer)
3. Spawn specialized fix task: "B26 ImportSFXForEnemySpawn" with parameters
4. Re-run wave starting from fix point
5. Re-invoke G13 critique
6. Loop until avg ≥ 8

---

## Example Scorecard: Wave 2 (Polish) after Mushroom Arena GDD

```json
{
  "gdd": "Mushroom Arena",
  "wave": 2,
  "timestamp": "2026-04-18T14:23:00Z",
  "scores": {
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
  "average_score": 8.4,
  "detailed_notes": {
    "ui_legibility": "Score label clear, wave counter visible, health bar proportional. ✓",
    "level_navigability": "Arena geometry intuitive; spawn point obvious. One corner slightly dark. → Increase ambient light +1",
    "asset_coherence": "Gameboy palette perfect; enemy sprites consistent. Player sprite slightly mismatched color. → Adjust player material",
    "responsiveness": "Input-to-action 28ms (excellent). No latency felt.",
    "audio_presence": "Music loop syncs perfectly to waves. SFX missing: no sound for enemy spawn or collision. → Spawn B26 ImportEnemySpawnSFX",
    "cinematography": "Top-down framing shows all action; composition balanced. ✓",
    "performance_stability": "Steady 60 FPS, no drops in canonical 30s playtest. ✓",
    "stability_crashes": "Zero crashes, zero console errors. ✓",
    "visual_hierarchy": "Player (green capsule) stands out; enemies clearly visible; projectiles visible. ✓",
    "shippable_feel": "Feels intentional and complete for a game jam. Placeholder art acceptable."
  },
  "refinement_tasks": [
    {
      "task": "AdjustPlayerMaterialColor",
      "family": "Design",
      "priority": "low",
      "blocker": false
    },
    {
      "task": "ImportEnemySpawnSFX",
      "family": "Audio",
      "priority": "medium",
      "blocker": false,
      "spawn_to": "B26"
    },
    {
      "task": "IncreaseAmbientLight",
      "family": "Level",
      "priority": "low",
      "blocker": false
    }
  ],
  "recommendation": "Polish threshold met (8.4/10). Proceed to playtest. Refinement tasks optional (address in next iteration if time permits)."
}
```

---

## Target Thresholds

| Scenario | Avg Score Target | Min Single Score | Interpretation |
|----------|------------------|------------------|-----------------|
| **Shippable Demo** | ≥ 8.0 | ≥ 5 | Polished, intentional, ready to share |
| **Playable Prototype** | 6.5–7.9 | ≥ 4 | Works, fun, but rough edges visible |
| **Early Playtest** | 5.0–6.4 | ≥ 2 | Functional but incomplete; feedback-gathering phase |
| **Broken / Unplayable** | < 5.0 | < 2 | Halt, escalate, redesign needed |

---

## Tips

1. **Score conservatively** — use 7–8 range for "good", reserve 9–10 for truly polished features
2. **Per-criterion notes matter** — "8/10 because X is missing" is more actionable than just "8/10"
3. **Shippable Feel is subjective** — calibrate to your target audience (casual game-jam = lower bar; premium indie = higher)
4. **Playtest data drives scoring** — don't guess "performance stable" without Profiler data
5. **Audio is often overlooked** — music + 3 key SFX push score 2–3 points; invest in it early
