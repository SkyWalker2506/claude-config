# Vision Feedback Loop Patterns

## Overview

After each wave completes, invoke G13 (Vision Action Operator) to capture screenshots, analyze game state visually, and drive polish scoring. This feedback loop ensures A14 doesn't rely on text descriptions alone — actual visuals drive refinement decisions.

---

## Capture Cadence

### Standard Schedule

- **After Wave 0 (Foundation):** Light capture — scene hierarchy only (no Game view yet; foundation not visual)
- **After Wave 1 (Structure):** Scene view + Game view (geometry visible, no decorations)
- **After Wave 2 (Polish):** Scene view + Game view + UI isolated (cinematic cam active, UI in place)
- **After Wave 3 (Integration):** Scene view + Game view + input responsiveness test (animation state machines active)
- **After Wave 4 (Playtest):** Intensive — game view from each VCam angle, UI stress test, profiler overlay

### Accelerated (If Polish Score < 7)

- Capture after every task (not just wave)
- Use multiple VCam angles in single Game view (split-screen if possible)
- Screenshot profiler window alongside game view

---

## Screenshot Targets

### 1. Scene View Hierarchy

**What to capture:**
- Full scene tree (Game objects and hierarchy)
- Focus on: GameObject count, parent-child structure, component overview

**Tool:** Craft_CaptureSceneView (upstream op)

**Parameters:**
```json
{
  "scope": "full_hierarchy" | "focus_subtree",
  "focus_path": "Level" | "Player" | "Enemies",
  "include_components": true,
  "output": "Assets/Screenshots/wave_{N}_scene_hierarchy.png"
}
```

**Why:** Verify structure matches DAG (e.g., "NavMesh GameObject should exist and be baked by Wave 1")

---

### 2. Game View (Default VCam)

**What to capture:**
- Full game screen at game resolution (e.g., 1920x1080)
- Include HUD, player, enemies, environment
- Capture once at start of frame, once mid-playtest (30s in)

**Tool:** Craft_CaptureGameView (upstream op)

**Parameters:**
```json
{
  "vCam": "MainCamera" | "VCam_TopDown",
  "resolution": [1920, 1080],
  "include_ui": true,
  "include_overlay": false,
  "output": "Assets/Screenshots/wave_{N}_game_default.png"
}
```

**Why:** Assess visual hierarchy, UI legibility, asset coherence, framing

---

### 3. Game View (Isolated UI)

**What to capture:**
- Only UI layer (HUD, buttons, scores) with 50% scene transparency behind
- Ensures UI is readable without distracting background

**Tool:** Craft_CaptureGameView with UI-only layer mask

**Parameters:**
```json
{
  "layer_mask": "UI",
  "background_opacity": 0.5,
  "output": "Assets/Screenshots/wave_{N}_ui_isolated.png"
}
```

**Why:** Check UI legibility, color contrast, font sizes at pixel level

---

### 4. Game View (Per-VCam)

**What to capture:**
- One frame from each VCam (if multiple exist: MainCamera, VCam_TopDown, VCam_Cinematic, etc.)
- Useful for verifying camera angles don't miss action

**Loop:**
```
for vCam in [MainCamera, VCam_TopDown, VCam_Cinematic]:
  Craft_CaptureGameView(vCam=vCam, output="..._{vCam_name}.png")
```

**Why:** Ensure all cameras frame action well; detect any camera misalignment

---

### 5. Profiler Overlay

**What to capture:**
- Game view with Profiler window visible (frametime, fps, memory, GC)
- Take at 3 timepoints: wave start, wave middle, wave end

**Tool:** Craft_CaptureGameView with Profiler overlay enabled

**Parameters:**
```json
{
  "profiler_enabled": true,
  "profiler_stats": ["fps", "frametime", "memory_total", "memory_gc"],
  "duration_sec": 30,
  "output": "Assets/Screenshots/wave_{N}_profiler_{time}.png"
}
```

**Why:** Correlate visual glitches with performance data (e.g., frame drop when enemy spawns)

---

## Critique Prompt Templates

### Template 1: Per-Criterion Scoring

```
Role: G13 Vision-Action Operator (visual analysis expert)

Task: Analyze these screenshots and score the game against 10 criteria.

Screenshots provided:
- Scene hierarchy: {path_scene}
- Game view default: {path_game}
- UI isolated: {path_ui}
- Profiler: {path_profiler}

Criteria (score each 0–10):
1. UI Legibility — Can player read all text? Good contrast?
2. Level Navigability — Are paths clear? Geometry coherent?
3. Asset Coherence — All visual elements feel same game?
4. Responsiveness — Input latency < 50ms? (use Profiler data)
5. Audio Presence — [from playtest audio log]
6. Cinematography — Camera framing good? Any jarring cuts?
7. Performance Stability — FPS stable? (Profiler shows ≥ 59 FPS?)
8. Stability (Crashes) — [from Console log]
9. Visual Hierarchy — Player/enemies distinct from background?
10. Shippable Feel — Overall, would you show this game to others?

For each criterion:
- Score (0–10)
- Short note explaining score
- If score < 7, suggest a fix (and which family: Design/Level/Audio/etc.)

Return JSON format:
{
  "scores": { "criterion": score, ... },
  "average": X.X,
  "notes": { "criterion": "...", ... },
  "fixes_needed": [ { "criterion": "...", "fix": "...", "family": "B26" } ]
}
```

### Template 2: Asset Coherence Deep-Dive

```
Role: G13 visual analyst

Task: Analyze asset coherence. All visual elements belong in same game?

Screenshots:
- {path_game}

Compare:
- Player character material/color vs enemy materials
- Terrain/level geometry texture/color scheme
- UI colors vs in-world colors
- Lighting tone (bright/dark/stylized)

Report:
- Coherence score 0–10
- Color palette consistency (describe)
- Any one-off mismatched assets? (list)
- Recommendation: cohesion is {good/acceptable/needs_work}
```

### Template 3: Responsive Input Verification

```
Role: G13 + profiler analyzer

Task: Verify input responsiveness.

Data:
- Profiler screenshot showing frametime during input event
- Game view at the frame input detected
- Console log of input system activity

Measure:
- Time from input event to visible response (frame count)
- Any frame hitches on input?
- Responsiveness score (0–10, scale: < 30ms = 10, > 150ms = 0)

Report:
- Latency estimate (ms)
- Responsiveness score
- If > 50ms, identify likely cause (heavy script, GC spike, etc.)
```

---

## Feedback Loop Integration with A14

### Pseudocode Flow

```
for wave in waves:
  dispatch_wave(wave)
  wait_for_completion()
  
  # Capture phase
  screenshots = {
    "scene": Craft_CaptureSceneView(),
    "game": Craft_CaptureGameView(),
    "ui": Craft_CaptureGameView(layer=UI),
    "profiler": Craft_CaptureGameView(with_profiler=true)
  }
  save_screenshots(wave_id, screenshots)
  
  # Critique phase
  critique_result = G13_Critique(
    goal="Score against 10 criteria",
    screenshots=screenshots,
    playtest_log={console, profiler},
    template="per-criterion-scoring"
  )
  
  # Decision gate
  avg_score = critique_result.average
  if avg_score >= 8.0 and min(scores) >= 5:
    → proceed to next wave (no refinement)
  elif avg_score >= 7.0:
    → optional refinement (spawn fix tasks, can continue)
  else:
    → mandatory refinement (restart wave with fixes)
    fix_tasks = critique_result.fixes_needed
    for fix_task in fix_tasks:
      spawn_dispatch(fix_task.family, fix_task.fix)
    → loop back to dispatch_wave(wave)  # re-dispatch same wave
  
  # Memory
  log_to_memory(wave, critique_result, decision)
end
```

---

## Example Output: Wave 2 Critique (Mushroom Arena)

**Captured:**
- Scene hierarchy: `Assets/Screenshots/wave_2_scene.png` (8 GameObjects, correct tree)
- Game view: `Assets/Screenshots/wave_2_game.png` (arena visible, HUD top-right)
- UI isolated: `Assets/Screenshots/wave_2_ui.png` (green text on black, readable)
- Profiler: `Assets/Screenshots/wave_2_profiler.png` (59 FPS avg, stable)

**G13 Critique Response:**

```json
{
  "analysis_timestamp": "2026-04-18T14:23:45Z",
  "screenshots_analysed": ["scene", "game", "ui", "profiler"],
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
  "notes": {
    "ui_legibility": "Score label bright green on black, excellent contrast. Wave counter clear. ✓",
    "level_navigability": "Arena geometry simple; player can move freely. One corner near enemy spawn has slightly lower ambient light, making it hard to see. Could increase light by +0.5.",
    "asset_coherence": "All sprites use 4-color gameboy palette. Enemy sprites (mushroom, slime) match style. Player (green capsule) is slightly bright green vs. darker enemy greens. Suggests material mismatch.",
    "responsiveness": "Profiler shows frametime 16.7ms (60 FPS), no input queue delay. Player moves immediately on WASD. ✓",
    "audio_presence": "Music loop audible in playtest. SFX: laser sound on fire detected. MISSING: no sound effect for enemy spawn or enemy death. This is a gap.",
    "cinematography": "Top-down camera frames entire arena nicely. No clipping. Player always center-ish. ✓",
    "performance_stability": "Profiler steady 59–60 FPS throughout 30s playtest. No frame drops. ✓",
    "stability_crashes": "Zero console errors in playtest. Clean exit from Play mode. ✓",
    "visual_hierarchy": "Green player (capsule) stands out against dark arena. Enemies (green/blue) visible. Projectiles (white spheres) visible on fire. ✓",
    "shippable_feel": "Feels intentional, complete, and fun for a game jam. Placeholder art is consistent. Would confidently show to others."
  },
  "recommendations": [
    {
      "criterion": "asset_coherence",
      "issue": "Player material color mismatch",
      "severity": "low",
      "fix_suggestion": "Adjust player material green to match enemy palette (darker #00AA00 instead of bright #00FF00)",
      "dispatch_to": "D11"
    },
    {
      "criterion": "audio_presence",
      "issue": "Missing SFX for spawn and death",
      "severity": "medium",
      "fix_suggestion": "Import 2 SFX clips: enemy_spawn_chime.wav and enemy_death_blip.wav. Bind to EnemyController.Spawn() and OnDeath().",
      "dispatch_to": "B26"
    },
    {
      "criterion": "level_navigability",
      "issue": "Dark corner near spawn",
      "severity": "low",
      "fix_suggestion": "Increase Point Light intensity in that corner by +0.5, or add a second light source.",
      "dispatch_to": "E11"
    }
  ],
  "overall_assessment": "Wave 2 polish threshold met (8.4/10 avg, all criteria >= 5). Proceed to Wave 3 or Playtest. Recommended: address audio_presence (B26 SFX import) in next iteration; others optional.",
  "confidence": "high"
}
```

---

## Profiler Data Extraction (For Responsiveness & Stability)

During each wave's playtest phase, capture Profiler data alongside screenshots:

```json
{
  "profiler_sample": {
    "duration_sec": 30,
    "fps_avg": 59.8,
    "fps_p95": 58,
    "frametime_avg_ms": 16.8,
    "frametime_max_ms": 32.1,
    "memory_peak_mb": 187,
    "memory_avg_mb": 165,
    "gc_per_frame_kb": 0.2,
    "gc_spike_count": 0,
    "cpu_time_render_pct": 45,
    "cpu_time_script_pct": 32,
    "cpu_time_physics_pct": 12,
    "errors_count": 0,
    "warnings_count": 2
  }
}
```

**Responsiveness Calculation:**
- Measure frame delta between input event (keyboard down) and response visible in Game view
- Example: WASD pressed at frame 100, player moves visibly at frame 102 → 2 frame latency → ~33ms (at 60 FPS)
- Target: < 50ms (< 3 frames)

---

## Tips

1. **Screenshot early, often** — capture at multiple timepoints in same wave to catch variation
2. **Use split-screen for VCam comparison** — if multiple cameras exist, show them side-by-side for ease of analysis
3. **Profiler overlay is crucial** — frame drops are visible as spikes; pair with G13 visual analysis
4. **Color contrast checker** — for UI, use automated contrast ratio tool if available (WCAG AAA = 7:1)
5. **Document fixes** — log which fixes were applied after Wave N critique, so you can trace improvement
6. **Iterate on audio** — audio gaps are easy to spot in G13 critique but often overlooked by developers; prioritize B26 SFX imports
