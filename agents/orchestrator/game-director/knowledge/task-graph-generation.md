# Task Graph Generation (DAG Building)

## Overview

Given a parsed GDD (JSON from `Director_ParseGDD`), build a Directed Acyclic Graph (DAG) of tasks grouped into **waves** (parallel-safe groups). Each task maps to a tool family + parameters. Dependencies are explicit: Level must complete before NavMesh bake, NavMesh before AI spawn.

---

## DAG Rules

### Blocking Edges (Hard Dependencies)

| Blocker | Blocked | Reason |
|---------|---------|--------|
| **Design/UI Library** | Screen (HUD capture) | UI must be designed before testing legibility |
| **Level Geometry** | NavMesh Bake | Level must be finalized |
| **NavMesh Bake** | AI Spawn & Behavior | Pathfinding requires baked nav |
| **Animator Setup** | Animation State Machine | Controller must exist before binding states |
| **Audio Mixer Setup** | SFX/Music Groups | Mixer must be created before adding clips |
| **Input Action Maps** | Input UI (rebind menu) | Actions must exist before UI binding |
| **Script Compilation** | Play Mode Entry | All scripts must be error-free |
| **All Geometry** | Cinematic Camera Setup | Scene must be complete before camera framing |
| **Camera Setup** | Vision Feedback (screenshot) | VCam must be active before capture |

### Parallel-Safe Edges (No Blocking)

These can run in same wave:

- **Design + Level** — UI and geometry design in parallel
- **Audio Mixer + Animation Controller** — independent subsystems
- **Input Actions + Cinematic VCam** — no dependency
- **Asset Store research + Mechanical implementation** — research informs, but doesn't block

### Wave Assignment Strategy

**Wave 0 (Foundation):**
- Level geometry (room layout, spawn points)
- Audio mixer setup (groups, snapshots)
- Input action maps
- Base AnimatorController

**Wave 1 (Structure):**
- NavMesh bake (blocked by Level from Wave 0)
- AI enemy prefabs + behavior scripts (blocked by AnimatorController)
- Player character + animator binding (blocked by AnimatorController)

**Wave 2 (Polish):**
- Cinematic VCam + PostFX presets (blocked by Level geometry)
- UI/HUD design + import (Design family, parallel to geometry from Wave 0)
- Audio clips + mixer group assignment (blocked by Mixer setup from Wave 0)

**Wave 3 (Integration & Testing):**
- Input bindings to gameplay (blocked by Input from Wave 0)
- Animator state machines (enemies + player animation flow)
- Level difficulty tuning + spawn tweaks

**Wave 4 (Playtest & Refinement):**
- Enter Play mode (blocked by script compilation + NavMesh bake)
- Canonical input simulation (WASD sweep, menu open, combat)
- Profiler sampling + perf baseline

---

## DAG JSON Schema

```json
{
  "gdd_title": "Mushroom Arena",
  "scope_minutes": 5,
  "total_duration_estimate_minutes": 25,
  "waves": [
    {
      "wave_id": 0,
      "name": "Foundation",
      "estimated_duration_minutes": 5,
      "parallel_tasks": [
        {
          "task_id": "L001",
          "family": "Level",
          "task": "CreateArenaGeometry",
          "agent": "E11",
          "parameters": {
            "geometry": "20x20m plane",
            "spawn_points": ["player_center", "enemy_random_4"],
            "lighting_preset": "bright"
          },
          "blockers": []
        },
        {
          "task_id": "A001",
          "family": "Audio",
          "task": "SetupAudioMixer",
          "agent": "B26",
          "parameters": {
            "groups": ["Music", "SFX", "Ambience"],
            "snapshots": ["Default", "Underwater"]
          },
          "blockers": []
        },
        {
          "task_id": "I001",
          "family": "Input",
          "task": "CreateActionMaps",
          "agent": "B36",
          "parameters": {
            "actions": ["Move", "Aim", "Fire"],
            "device": "keyboard"
          },
          "blockers": []
        }
      ]
    },
    {
      "wave_id": 1,
      "name": "Structure",
      "estimated_duration_minutes": 8,
      "parallel_tasks": [
        {
          "task_id": "L002",
          "family": "Level",
          "task": "BakeNavMesh",
          "agent": "E11",
          "parameters": {
            "agent_height": 2.0,
            "max_slope": 45
          },
          "blockers": ["L001"]
        },
        {
          "task_id": "AN001",
          "family": "Animation",
          "task": "CreateAnimatorController",
          "agent": "E9",
          "parameters": {
            "character_type": "enemy_mushroom",
            "states": ["Idle", "Walk", "Attack", "Death"]
          },
          "blockers": []
        }
      ]
    },
    {
      "wave_id": 2,
      "name": "Polish",
      "estimated_duration_minutes": 6,
      "parallel_tasks": [
        {
          "task_id": "C001",
          "family": "Cinematic",
          "task": "CreateCinematicVCam",
          "agent": "E9",
          "parameters": {
            "preset": "TopDown",
            "follow_target": "null",
            "framing": "fixed"
          },
          "blockers": ["L001"]
        },
        {
          "task_id": "D001",
          "family": "Design",
          "task": "ImportUIBundle",
          "agent": "D11",
          "parameters": {
            "ui_components": ["MainMenu", "HUD", "GameOver"],
            "style": "retro_green"
          },
          "blockers": []
        },
        {
          "task_id": "A002",
          "family": "Audio",
          "task": "ImportAudioClips",
          "agent": "B26",
          "parameters": {
            "clips": ["music_loop_120bpm", "sfx_laser", "sfx_chime", "ambience_cricket"],
            "mixer_group": "auto"
          },
          "blockers": ["A001"]
        }
      ]
    },
    {
      "wave_id": 3,
      "name": "Integration",
      "estimated_duration_minutes": 4,
      "parallel_tasks": [
        {
          "task_id": "I002",
          "family": "Input",
          "task": "BindInputToGameplay",
          "agent": "B36",
          "parameters": {
            "action_bindings": {
              "Move": ["Player.MovementScript.Move"],
              "Fire": ["Player.GunScript.Fire"]
            }
          },
          "blockers": ["I001"]
        },
        {
          "task_id": "AN002",
          "family": "Animation",
          "task": "CreateAnimatorStateMachine",
          "agent": "E9",
          "parameters": {
            "character": "enemy_mushroom",
            "transitions": ["Idle→Walk on speed>0", "Walk→Attack on collision"]
          },
          "blockers": ["AN001"]
        }
      ]
    },
    {
      "wave_id": 4,
      "name": "Playtest",
      "estimated_duration_minutes": 2,
      "parallel_tasks": [
        {
          "task_id": "G001",
          "family": "GameDirector",
          "task": "RunPlaytest",
          "agent": "A14",
          "parameters": {
            "scenario": "smoke",
            "inputs": ["WASD_sweep", "menu_open", "fire"],
            "duration_sec": 30
          },
          "blockers": ["L002", "AN002", "I002"]
        }
      ]
    }
  ],
  "critical_path": ["L001", "L002", "AN001", "AN002", "I001", "I002", "G001"],
  "estimated_total_duration_minutes": 25
}
```

---

## Example: Platformer GDD → 6-Wave DAG

**GDD Pitch:** "2D platformer, 3 levels, player jumps & dashes, simple enemy patrol, retro pixel art"

**Blocking Edges Identified:**
- Level geometry → NavMesh
- Animation controller → Character animator binding
- Player scripts → Play mode

**Wave Assignment:**

| Wave | Tasks | Est. Time | Blockers |
|------|-------|-----------|----------|
| 0 | Level geo (3 rooms), Audio mixer, Input maps | 6 min | — |
| 1 | NavMesh bake, Animator controller | 5 min | Wave 0 Level |
| 2 | Player character + animator, Enemy prefabs | 5 min | Wave 1 Animator |
| 3 | Cinematic camera, Design + HUD, Audio import | 6 min | Wave 0 Level, Wave 1 Animator |
| 4 | Animation state machines, Input bindings | 4 min | Wave 1 Animator, Wave 0 Input |
| 5 | Playtest + perf profile | 3 min | All prior (critical path) |

**Critical Path (longest):**  
Level → NavMesh → Animator → Character → Animation State Machine → Playtest  
**Total: 28 minutes (wall-clock estimate)**

---

## Generation Algorithm

### Step 1: Extract Tasks from GDD

```
For each GDD section (mechanics, levels, art, audio, ui, controls):
  → Identify tool family (Level → E11, Audio → B26, etc.)
  → List concrete tasks (CreateGeometry, BakeNavMesh, etc.)
  → Record parameters from GDD values
```

### Step 2: Build Dependency Graph

```
For each task:
  → Check if it blocks any other task (apply blocking rules)
  → Check what blocks it (reverse lookup)
  → Record blocker list for each task
```

### Step 3: Assign Waves (Topological Sort)

```
Wave := 0
Assigned := {}

While unassigned tasks remain:
  AvailableThisWave := [task for task if all blockers in Assigned]
  if AvailableThisWave is empty:
    ERROR: circular dependency detected
  else:
    Assign all AvailableThisWave to current Wave
    Marked assigned
    Wave += 1
```

### Step 4: Validate DAG

- [ ] No cycles (topological sort succeeds)
- [ ] All tasks assigned to exactly one wave
- [ ] Each task's blockers are in earlier waves
- [ ] Parallel tasks in same wave have no mutual dependencies

---

## Worked Example: Arena Survivor GDD

**Input GDD:**
- 3 enemy types
- 1 arena room
- Gameboy palette
- 3-minute playtime

**Task Extraction:**

| Family | Task | GDD Source | Parameters |
|--------|------|-----------|------------|
| Level | CreateArena | Levels section | 20x20m, center spawn |
| Level | BakeNavMesh | Technical section | Standard 2D settings |
| Animation | CreateEnemyAnimator | Mechanics (enemy behavior) | 3 states: Idle, Walk, Attack |
| Audio | SetupMixer | Audio Direction | 2 groups: Music, SFX |
| Audio | ImportMusic | Audio Direction | 120 BPM loop, 3 min |
| Input | MapActions | Controls section | WASD, Mouse, LeftClick |
| Design | BuildHUD | UI Style section | Score, Wave, Health |
| Cinematic | SetupVCam | Art Direction | TopDown, fixed |

**Dependencies:**
- BakeNavMesh blocks CreateEnemyAnimator (needs nav data)
- CreateArena blocks BakeNavMesh
- SetupMixer → ImportMusic (mixer must exist)
- MapActions independent

**Wave Assignment:**

```
Wave 0 (t=0–5m): CreateArena, SetupMixer, MapActions
  (parallel, no blockers)

Wave 1 (t=5–10m): BakeNavMesh, CreateEnemyAnimator
  (blocked by Wave 0 CreateArena)

Wave 2 (t=10–16m): BuildHUD, ImportMusic, SetupVCam, CreatePlayerAnimator
  (most blocked by Wave 0)

Wave 3 (t=16–20m): Integration tasks (BindInputToGameplay, CreateStateMachine)
  (blocked by Wave 1)

Wave 4 (t=20–22m): Playtest (EnterPlayMode, SimulateInput)
  (blocked by all prior)
```

---

## Tips & Gotchas

1. **Estimate conservatively** — always add 20% buffer for refinement
2. **Audio mixer setup is fast** — don't make it a blocker unnecessarily
3. **NavMesh bake can be slow** — factor in for large levels
4. **Script compilation blocks Play mode** — verify no compile errors before Wave N
5. **Vision feedback costs time** — G13 critique takes 2–3 min per wave; budget accordingly
6. **Refinement loops aren't in DAG** — if polish < 8, restart from affected wave (not atomic)

---

## Validation

Before emitting DAG JSON:

- [ ] All GDD sections mapped to tasks
- [ ] No circular dependencies
- [ ] Critical path identified
- [ ] Each task has clear parameters (extractable from GDD)
- [ ] Blockers reflect actual Unity/CRAFT constraints (not arbitrary)
- [ ] Wave estimates add up to < wall-clock budget
- [ ] Parallel tasks in each wave are safe (validated against blocking rules)
