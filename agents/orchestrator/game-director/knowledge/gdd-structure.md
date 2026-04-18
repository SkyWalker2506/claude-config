# GDD Structure & Parsing

## Overview

A Game Design Document (GDD) for A14 Game Director must follow dual format: **YAML front-matter + Markdown sections**. This enables structured parsing + human-readable design rationale.

Director_ParseGDD ingests this format and emits structured JSON for DAG building.

---

## Expected Sections

### Front-Matter (YAML)

```yaml
---
title: "Game Title"
genre: "Platformer | Action | Puzzle | Adventure | etc."
scope: "micro (5 min) | short (15 min) | medium (30 min) | long (60+ min)"
target_audience: "casual | core | accessibility-focused"
platform: "desktop | mobile | console | web"
placeholder_art_ok: true
tech_constraints:
  - "single-threaded CPU target"
  - "no DOTS"
  - "URP only"
---
```

### 1. Pitch (1–3 sentences)

One-liner that captures the essence:

```markdown
## Pitch

Top-down arena survivor: you defend a shrine against 3 waves of 
mushroom enemies. One gun, auto-targeting. 3-minute playtime. 
Art direction: retro gameboy palette.
```

### 2. Core Mechanics (bullet list)

What the player does:

```markdown
## Mechanics

- **Player Movement:** WASD, speed 5 m/s, can move during aim
- **Weapon:** Fixed gun, auto-targets nearest enemy within 10m, fires every 0.3s
- **Enemy Behavior:** Walk toward player, melee attack on collision
- **Score System:** Kill points + time survived = final score
- **Waves:** 3 enemy types spawn in order (mushroom → slime → boss), each wave lasts 60 seconds
```

### 3. Levels / Scenes (structure)

Describe each playable scene:

```markdown
## Levels

**Hub (00–5s):** Shrine room, 20x20 ground plane, 1 spawn point center, 
1 enemy spawn trigger at 5s. Post-ProcessVolume: desaturated.

**Arena Wave 1 (5–65s):** Same geometry, mushrooms spawn (8 total), 
randomized positions. Score tracker visible top-right.

**Arena Wave 2 (65–125s):** Slimes spawn (6 total), move faster, split on death.

**Boss Arena (125–180s):** Boss mushroom, 4x HP, area attack every 10s. 
Victory screen triggered on kill.
```

### 4. Art Direction (style, palette, mood)

```markdown
## Art Direction

- **Style:** Retro gameboy (4-color palette: white, green, dark-green, black)
- **Aesthetic:** Minimalist, grid-aligned
- **Lighting:** No real-time, use placeholder sprites
- **Camera:** Fixed orthographic, framing entire arena
- **UI Theme:** Green monochrome, sans-serif font (Arial/Roboto)
- **Asset Placeholder:** Unity default primitives (Cube for mushroom, Sphere for projectile)
```

### 5. Audio Direction (music, SFX, ambience)

```markdown
## Audio Direction

- **Music:** Single looping track, 8-bit chiptune, 120 BPM, matches wave pacing
- **Ambience:** Forest crickets, low volume (−10dB)
- **SFX:**
  - Gun fire: short beep (retro laser sound)
  - Enemy spawn: chime
  - Wave complete: ascending chord
- **Audio Mixer:** 2 groups (Music, SFX), Music ducking on SFX priority
- **Spatial:** No 3D audio; all sounds 2D stereo
```

### 6. UI / UX Style

```markdown
## UI Style

- **Main Menu:** Title + "Play" button, centered, green text on black background
- **HUD (In-Game):** Score (top-right), Wave counter (top-left), Enemy count (bottom-right)
- **Game Over:** "Final Score: 1250" + "Restart" / "Quit" buttons, centered, no animation
- **Font:** Roboto Mono 32px for score, 24px for labels
- **Color:** Text #00FF00 (green), Background #000000 (black)
```

### 7. Control Scheme

```markdown
## Controls

- **Keyboard (PC):**
  - W/A/S/D: Move
  - Mouse: Aim direction
  - Left Click: Fire (hold to maintain aim)
  - ESC: Pause (optional)
  
- **Gamepad (if console target):**
  - Left Stick: Move
  - Right Stick: Aim
  - Right Trigger: Fire
  - B Button: Pause

- **Mobile (if target):**
  - Joystick overlay: left side move, right side aim
  - Button: fire (fixed center-bottom)
```

### 8. Technical Constraints

```markdown
## Technical Constraints

- **Target Platform:** Windows desktop, 1920x1080, 60 FPS target
- **Engine:** Unity 6.0.x, URP, no Netcode
- **Physics:** 2D (Rigidbody2D, CircleCollider2D for enemies/bullets)
- **Scripting:** C# only, no visual scripting
- **Performance Budget:** < 200MB memory, < 50ms frame time
- **Build Size:** < 500MB (no AAA assets)
- **Known Limits:** No high-res textures (placeholder art), no advanced VFX, single-threaded simulation
```

### 9. Playtest Criteria (acceptance)

```markdown
## Playtest Criteria

- **Gameplay Feel:** Player feels responsive, no input lag > 50ms
- **Level Progression:** Each wave is visually distinct and increasingly challenging
- **Audio Cohesion:** Music matches pacing; SFX doesn't overlap confusingly
- **Visual Clarity:** Player, enemies, projectiles all clearly visible; no overlapping UI
- **Stability:** No crashes in canonical 3-minute playthrough; no console errors
- **Scope Met:** Game completable in 3 ± 0.5 minutes; all mechanics functional
```

---

## Example GDD (Complete)

```yaml
---
title: "Mushroom Arena"
genre: "Action / Arena Survival"
scope: "micro (5 min)"
target_audience: "casual"
platform: "desktop"
placeholder_art_ok: true
tech_constraints:
  - "URP only"
  - "2D physics"
  - "no advanced VFX"
---

# Mushroom Arena — Game Design Document

## Pitch

Top-down arena survivor: defend a shrine against 3 waves of mushroom enemies. 
One auto-targeting gun. 3-minute total playtime. Retro gameboy aesthetic.

## Mechanics

- **Player:** WASD move, mouse aim, left-click fire. Speed 5 m/s, health 100 HP.
- **Gun:** Auto-targets nearest enemy within 10m radius, fires every 0.3s, 10 damage per hit.
- **Enemies:**
  - Mushroom: 20 HP, 1 m/s walk speed, 1 spawn per second (8 total wave 1)
  - Slime: 10 HP, 1.5 m/s, splits into 2 smaller slimes on death (6 spawn wave 2)
  - Boss: 100 HP, slow (0.5 m/s), area attack every 10s, 1 spawn wave 3
- **Score:** +10 per enemy kill, +1 per second survived. Win: defeat boss.

## Levels

**Wave 1 (5–65s):** Arena 20x20m, player spawns center, 8 mushrooms spawn randomly.  
**Wave 2 (65–125s):** Same arena, 6 slimes spawn.  
**Wave 3 (125–180s):** Boss spawn, defeat to win.

## Art Direction

- **Style:** Retro gameboy (4-color: white, 2 greens, black)
- **Sprites:** Unity primitives (Cube = mushroom, Sphere = projectile, Capsule = player)
- **Camera:** Fixed ortho, framing 22x22m
- **UI:** Green monochrome, Roboto Mono font, all text centered

## Audio Direction

- **Music:** Single 8-bit chiptune loop, 120 BPM (3-minute duration)
- **SFX:** Laser beep (fire), chime (spawn), chord (wave end)
- **Ambience:** Forest cricket loop, −10dB
- **Mixer:** Music + SFX groups, Music −6dB during SFX

## UI Style

- **HUD:** Score (top-right), Wave (top-left), Enemy count (bottom-right), Health bar (bottom-left)
- **Game Over:** Final score centered, "Restart" and "Quit" buttons
- **Font:** Roboto Mono 32px score, 24px labels

## Controls

- **Move:** WASD
- **Aim:** Mouse
- **Fire:** Left Click (hold to maintain)

## Technical Constraints

- **Target:** Win/Linux desktop, 1920x1080, 60 FPS
- **Physics:** 2D only
- **Memory:** < 150MB
- **Build:** < 300MB

## Playtest Criteria

1. Player can move and fire within 50ms response time
2. All 3 enemy types spawn correctly with proper behavior
3. Score tracking is accurate and visible
4. Music loop syncs to wave timer
5. Game completes in 3 ± 0.5 minutes
6. Zero crashes; clean console (0 errors)
```

---

## Parsing Rules

### Director_ParseGDD(gddPath) → JSON

```json
{
  "title": "Mushroom Arena",
  "pitch": "Top-down arena survivor: defend shrine against 3 waves...",
  "mechanics": [
    { "name": "Player Movement", "description": "WASD, speed 5 m/s..." },
    { "name": "Gun", "description": "Auto-targets, fires every 0.3s..." }
  ],
  "levels": [
    {
      "name": "Wave 1",
      "duration_sec": 60,
      "geometry": "20x20m arena",
      "spawns": ["8x Mushroom"],
      "objectives": ["Survive 60s"]
    }
  ],
  "art_direction": {
    "style": "Retro gameboy",
    "palette": ["white", "#00FF00", "#008000", "#000000"],
    "camera_type": "fixed orthographic"
  },
  "audio_direction": {
    "music_tempo_bpm": 120,
    "music_duration_sec": 180,
    "sfx": ["fire", "spawn", "wave_end"],
    "ambience": "forest crickets"
  },
  "ui_style": {
    "font": "Roboto Mono",
    "color_primary": "#00FF00",
    "color_background": "#000000"
  },
  "controls": {
    "move": "WASD",
    "aim": "Mouse",
    "fire": "Left Click"
  },
  "technical_constraints": {
    "platform": "desktop",
    "target_fps": 60,
    "memory_budget_mb": 150,
    "build_size_mb": 300
  },
  "playtest_criteria": [
    "Input responsiveness < 50ms",
    "All enemy types functional",
    "Score tracking accurate",
    "Game length 3 ± 0.5 minutes",
    "Zero crashes"
  ]
}
```

---

## Validation Checklist

Before emitting DAG:

- [ ] GDD has all 9 sections (or LLM-extracted equivalent)
- [ ] Pitch is 1–3 sentences, clear mechanic summary
- [ ] Mechanics list has player actions + enemy behaviors
- [ ] Levels section lists all scenes with spawn/objective
- [ ] Art direction has style + palette + camera type
- [ ] Audio direction has music BPM + duration + mixer groups
- [ ] UI style specifies fonts, colors, layouts
- [ ] Controls map inputs to actions (no ambiguity)
- [ ] Technical constraints name platform, target FPS, memory budget
- [ ] Playtest criteria are measurable (not vague like "fun" or "looks good")

If any section is missing or vague → ask user to clarify before DAG build.
