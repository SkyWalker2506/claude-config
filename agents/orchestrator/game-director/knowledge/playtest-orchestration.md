# Playtest Orchestration

## Overview

After Wave 3 (Integration), before shipping, run canonical input scenarios in Play mode to verify gameplay feel, responsiveness, stability, and performance. This playtest feeds into final polish scoring and perf optimization tasks.

---

## Canonical Scenarios

### Scenario 1: Smoke Test (2 minutes)

**Purpose:** Quick sanity check — does the game not crash immediately?

**Inputs (in order):**
1. **Menu Navigation (30s):**
   - Click "Play" button on main menu
   - Wait for scene load
   - Assert: Level scene loads without error

2. **WASD Movement Sweep (30s):**
   - Hold W for 5s (move forward)
   - Hold A for 5s (move left)
   - Hold S for 5s (move backward)
   - Hold D for 5s (move right)
   - Release all
   - Assert: Player moves in expected directions, smooth motion

3. **UI Check (20s):**
   - Pause menu (ESC key, if supported)
   - Resume game
   - Assert: Menu appears/disappears, no freeze

4. **Core Mechanic Trigger (30s):**
   - For Platformer: Jump (Spacebar)
   - For Shooter: Fire weapon (Left Mouse)
   - For RPG: Interact with NPC (E key)
   - Assert: Core action works, no hang

**Profiler Target:**
- fps_avg ≥ 55 (FPS should stay near target)
- memory_peak < 200MB
- gc_per_frame < 1MB
- Zero crashes

---

### Scenario 2: Combat / Interaction (3 minutes)

**Purpose:** Test gameplay loops — combat, enemy behavior, win/lose conditions.

**Inputs:**
1. **Spawn First Enemy (30s):**
   - Wait for enemy to spawn (or trigger manually if needed)
   - Observe: Enemy path toward player, animation playing

2. **Combat Loop (90s):**
   - Fire at enemy (or melee attack, depending on game)
   - Repeat 10–20 times until enemy dies
   - Assert: Hit detection works, enemy health decreases, animation/death triggers

3. **Multiple Enemies (30s):**
   - Spawn 2–3 enemies simultaneously
   - Combat against all
   - Assert: No pathfinding issues, audio doesn't clip, frame rate stable

4. **Win / Lose Trigger (30s):**
   - Trigger victory (defeat final enemy or reach goal)
   - Or trigger loss (let enemy kill player)
   - Assert: Game over screen appears, score displays, restart/menu available

**Profiler Target:**
- fps_avg ≥ 55
- fps_p95 ≥ 50 (worst-case frame still playable)
- memory_peak < 250MB
- gc_spike_count = 0
- Zero crashes

---

### Scenario 3: Exploration / Level Navigation (2 minutes)

**Purpose:** Test level design clarity, camera framing, no geometry traps.

**Inputs:**
1. **Traverse All Level Areas (120s):**
   - If level is linear: walk entire path start → end
   - If level is open: visit all 4 quadrants, spawn area, objective area
   - Assert: No stuck player, camera shows all action, colliders work

2. **Look for Traps (30s):**
   - Try jumping into geometry (if platformer)
   - Try moving through obstacles (if any)
   - Assert: Colliders prevent unintended movement, or intentional level design is clear

**Profiler Target:**
- Consistent fps_avg ≥ 55
- No memory leak (memory stable across traversal)

---

### Scenario 4: Menu Flow / UI Interaction (1 minute)

**Purpose:** Verify UI is interactive, buttons respond, no dead-clicks.

**Inputs:**
1. **Main Menu Actions (30s):**
   - Hover over buttons (observe visual feedback)
   - Click "Play" → load scene
   - Pause in-game → click "Resume" → game continues
   - Click "Quit" → return to main menu

2. **HUD Interaction (if applicable) (30s):**
   - Open inventory (I key)
   - Close inventory (ESC or click close button)
   - Click on HUD elements (if any are clickable)

**Profiler Target:**
- No UI lag (button click → response < 100ms)
- No memory spike on UI toggle

---

## Profiler Sampling (CRAFT Upstream Op)

**Tool:** `Craft_SampleProfileWindow(scenario, duration_sec)`

**Parameters:**
```json
{
  "scenario": "smoke" | "combat" | "exploration" | "menu",
  "duration_sec": 120,
  "stats": ["fps", "frametime", "memory_total", "memory_gc", "cpu_breakdown"],
  "sample_rate_hz": 10,
  "output": "Assets/Profiler/scenario_{name}.json"
}
```

**Output Format:**
```json
{
  "scenario": "smoke",
  "duration_sec": 120,
  "samples": [
    { "time": 0.0, "fps": 60, "frametime_ms": 16.7, "memory_mb": 150, "gc_kb": 0 },
    { "time": 0.1, "fps": 59, "frametime_ms": 16.9, "memory_mb": 150, "gc_kb": 0 },
    ...
    { "time": 120.0, "fps": 58, "frametime_ms": 17.2, "memory_mb": 153, "gc_kb": 2 }
  ],
  "aggregate": {
    "fps_avg": 59.2,
    "fps_min": 45,
    "fps_p95": 58,
    "fps_p99": 60,
    "frametime_avg_ms": 16.9,
    "frametime_max_ms": 35.4,
    "memory_peak_mb": 175,
    "memory_avg_mb": 152,
    "memory_growth_mb": 25,
    "gc_per_frame_avg_kb": 0.3,
    "gc_spike_count": 0,
    "cpu_render_pct": 42,
    "cpu_script_pct": 35,
    "cpu_physics_pct": 18,
    "cpu_other_pct": 5
  },
  "warnings": [
    "Memory growth detected (25 MB over 120s); possible leak or large allocation"
  ]
}
```

---

## Play Mode Entry Protocol

Before entering Play mode:

1. **Pre-flight Check:**
   ```json
   Craft_Validate({
     "checks": [
       "scripts_compile",
       "no_console_errors",
       "navmesh_baked",
       "physics_initialized",
       "prefabs_instantiable"
     ]
   })
   ```

2. **If any check fails → abort playtest, spawn fix task**

3. **If all pass → proceed:**
   ```
   Craft_EnterPlayMode()
   ```

4. **Monitor Console during playtest:**
   - If error appears → record timestamp, context, exit Play mode
   - If warning appears → non-blocking, continue

5. **Exit Play mode:**
   ```
   Craft_ExitPlayMode()
   → check for unsaved changes (warn user, but don't block)
   ```

---

## Playtest Flow (Pseudocode)

```
function Director_Playtest(scenario_name, duration_sec, max_retries=2):
  
  # Pre-flight
  validation = Craft_Validate(pre_flight_checks)
  if validation.failed:
    log_error(validation.failures)
    spawn_fix_task(validation.failures[0])
    return { success: false, blocker: true }
  
  # Enter Play mode
  Craft_EnterPlayMode()
  
  # Simulate inputs per scenario
  scenarios = {
    "smoke": SmokeTestInputs(120),
    "combat": CombatInputs(180),
    "exploration": ExplorationInputs(120),
    "menu": MenuFlowInputs(60)
  }
  inputs = scenarios[scenario_name]
  
  # Run with profiler sampling
  profiler_thread = Craft_SampleProfileWindow(scenario_name, duration_sec)
  console_monitor_thread = Craft_MonitorConsole()
  
  for input_event in inputs:
    SimulateInput(input_event)
    sleep(input_event.duration_sec)
    capture_screenshot(output=f"playtest_{scenario_name}_{time}.png")
  
  # Exit Play mode
  crash_detected = console_monitor_thread.error_count > 0
  profiler_data = profiler_thread.wait()
  Craft_ExitPlayMode()
  
  # Aggregate results
  return {
    success: not crash_detected,
    scenario: scenario_name,
    fps_avg: profiler_data.aggregate.fps_avg,
    fps_p95: profiler_data.aggregate.fps_p95,
    memory_peak: profiler_data.aggregate.memory_peak_mb,
    gc_per_frame: profiler_data.aggregate.gc_per_frame_avg_kb,
    crash_count: console_monitor_thread.error_count,
    console_errors: console_monitor_thread.errors,
    profiler_warnings: profiler_data.warnings,
    screenshots: [list of captured images]
  }
```

---

## Acceptance Criteria

### Performance Thresholds

| Metric | Target | Warning | Fail |
|--------|--------|---------|------|
| **fps_avg** | ≥ 55 | 45–54 | < 45 |
| **fps_p95** | ≥ 50 | 40–49 | < 40 |
| **frametime_max** | ≤ 35ms | 35–50ms | > 50ms |
| **memory_peak** | < 250MB | 250–350MB | > 350MB |
| **gc_per_frame** | < 0.5MB | 0.5–1MB | > 1MB |
| **gc_spike_count** | 0 | 1–2 | > 2 |
| **cpu_script_pct** | < 40% | 40–60% | > 60% |

### Stability Criteria

- **Console Errors:** 0 (critical fail if any)
- **Warnings:** < 5 (non-blocking)
- **Crashes:** 0 (critical fail if any)

### Gameplay Criteria

- **Input Responsiveness:** < 50ms (WASD → visible player move)
- **Menu Navigation:** All buttons clickable, no dead zones
- **Core Mechanic:** Works as designed (shoot fires, jump jumps, interact triggers)
- **AI / Enemies:** Spawn, pathfind, attack as expected

---

## Example Playtest Report: Smoke Test (Mushroom Arena)

```json
{
  "gdd": "Mushroom Arena",
  "playtest_id": "PT_001",
  "scenario": "smoke",
  "timestamp": "2026-04-18T14:45:00Z",
  "duration_sec": 120,
  "success": true,
  "pre_flight": {
    "scripts_compile": true,
    "console_errors_before": 0,
    "navmesh_baked": true,
    "physics_ready": true
  },
  "input_sequence": [
    { "action": "ClickPlayButton", "time": 0, "duration": 1 },
    { "action": "WaitSceneLoad", "time": 1, "duration": 5 },
    { "action": "HoldWASD_W", "time": 6, "duration": 5 },
    { "action": "HoldWASD_A", "time": 11, "duration": 5 },
    { "action": "HoldWASD_S", "time": 16, "duration": 5 },
    { "action": "HoldWASD_D", "time": 21, "duration": 5 },
    { "action": "PressLeftMouse", "time": 26, "duration": 0.5, "repeat": 10 },
    { "action": "WaitGameplay", "time": 36, "duration": 84 }
  ],
  "profiler_data": {
    "fps_avg": 59.7,
    "fps_min": 52,
    "fps_max": 60,
    "fps_p95": 59,
    "frametime_avg_ms": 16.8,
    "frametime_max_ms": 19.2,
    "memory_peak_mb": 165,
    "memory_avg_mb": 155,
    "memory_growth_mb": 10,
    "gc_per_frame_avg_kb": 0.1,
    "gc_spike_count": 0,
    "cpu_breakdown_pct": {
      "render": 45,
      "script": 32,
      "physics": 18,
      "other": 5
    }
  },
  "console": {
    "error_count": 0,
    "warning_count": 1,
    "warnings": ["AudioListener: No Main Listener found in scene (non-critical)"]
  },
  "gameplay_observations": {
    "menu_load": "Play button clicked, scene loaded in 2.3 seconds. ✓",
    "wasd_movement": "All directions responsive. Smooth motion, no jitter. ✓",
    "fire_input": "Fire (Left Mouse) works 10/10 times. Projectiles spawn, visible. ✓",
    "audio": "Music looped from game start. Laser sound plays on fire. ✓",
    "stability": "Zero crashes, game exited cleanly. ✓"
  },
  "perf_assessment": {
    "fps": "Excellent (59.7 avg, target 60). Stable.",
    "memory": "Good (165 MB peak, target < 200). No leak detected.",
    "cpu": "Script usage 32% (target < 40%). Room for expansion."
  },
  "acceptance": {
    "perf_passed": true,
    "stability_passed": true,
    "gameplay_passed": true,
    "overall": "PASS — Ready for next scenario"
  },
  "recommendations": [
    {
      "category": "optional",
      "note": "AudioListener warning is non-critical, but could be fixed by adding AudioListener component to MainCamera"
    }
  ]
}
```

---

## Playtest Failure Response

If any criterion fails:

1. **Crash or Error:** 
   - Log console error message
   - Exit Play mode
   - Spawn B19 (gameplay engineer) or B53 (perf analyst) fix task
   - Re-run playtest after fix applied

2. **Perf Degradation (fps_avg < 55):**
   - Identify bottleneck from profiler (cpu_script_pct, memory growth, etc.)
   - Spawn B53 optimization task
   - Re-run playtest

3. **Input Responsiveness > 50ms:**
   - Likely script issue or render lag
   - Check CPU breakdown; if script > 60%, spawn optimization
   - Or input latency issue → check B36 Input System bindings

4. **Memory Leak (memory_growth > 50MB):**
   - Spawn B53 memory profiling task
   - May need to defer some asset loads or reduce batch sizes

---

## Tips

1. **Warm-up Run:** Do a quick mental playthrough before instrumented playtest to catch obvious issues
2. **Profiler Data is Gold:** Frame drops are visible in graph; pair with console monitoring for root cause
3. **Capture Screenshots:** At least one per scenario, showing Profiler overlay, for later visual audit
4. **Test on Target Device:** If mobile target, run on actual phone (not just in Editor); memory + perf is very different
5. **Audio Monitoring:** Turn on game audio; SFX timing issues often missed by silent playtest
6. **Scenario Ordering:** Do smoke test first (quick); only run combat if smoke passes. Saves time.
