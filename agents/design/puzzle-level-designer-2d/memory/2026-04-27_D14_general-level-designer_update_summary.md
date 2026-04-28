# D14 Update Summary — General Level Designer + Game-pack Enforcement

**Date:** 2026-04-27  
**Source roadmap:** `D14_General_Level_Designer_Roadmap_v1.md` (v1.1)  
**Canonical agent path (unchanged):**  
`~/Projects/claude-config/agents/design/puzzle-level-designer-2d/`

---

## 1) High-level outcome

D14 is refactored from “2D Puzzle Physics Level Designer” into a **General Level Designer** with:
- **Core vs game-specific separation** (game-packs)
- **Validator-first workflow**
- Mandatory **spatial logic** and **dependency** reasoning
- Pattern-based design (anti “random obstacle pile”)
- Enforced **game-pack usage** when a pack exists (Golf Paper Craft included)

---

## 2) Key rules added (new system behavior)

### 2.1 Core vs game-pack separation
- Core knowledge must not contain game-specific numeric constants.
- All game-specific mechanics/constants/rules live under `game-packs/<game>/`.

### 2.2 Game-pack enforcement (must use during design)
If a game-pack exists for the identified game:
- D14 must include **Game-pack loaded evidence** in the output (pack path + key files).
- D14 must apply `validation-overrides.md` before any **final** spec/verdict.

If a game-pack does NOT exist:
- D14 must write a **Design Brief** (assumptions + unknowns + handoff risks).
- Any “final” output must be labeled **provisional**.

### 2.3 Mandatory workflow (validator-first)
Workflow is defined in D14’s `AGENT.md` and requires:
- design intent
- player knowledge state
- intended solve path + obvious wrong path
- purpose audit (remove test)
- spatial logic validation
- dependency validation
- readability + difficulty validation
- game-pack validation overrides

---

## 3) Files changed / added

### 3.1 D14 definition updated
- **Updated:** `AGENT.md`  
  Path: `agents/design/puzzle-level-designer-2d/AGENT.md`  
  - name: **General Level Designer**
  - capabilities updated
  - boundaries updated
  - mandatory workflow included
  - game-pack enforcement included

### 3.2 Core knowledge (universal) — added
Added these files under `knowledge/`:
- `knowledge/level-design-principles.md`
- `knowledge/spatial-logic.md`
- `knowledge/puzzle-dependency-graphs.md`
- `knowledge/pattern-library.md`
- `knowledge/validation-checklists.md`
- `knowledge/game-pack-usage.md`

Also:
- **Updated:** `knowledge/_index.md` (new core entries + “core vs game-pack” guidance)

### 3.3 Core de-golf (remove game constants from core)
- **Updated:** `knowledge/balance-math.md`  
  Converted into **universal methodology only** and redirected numeric constants to game-pack.

### 3.4 Golf Paper Craft game-pack — added
Created folder:
`game-packs/golf-paper-craft/`

Added:
- `GAME.md`
- `physics-constants.md`
- `balance-math.md`
- `mechanics.md`
- `placement-matrix.md`
- `validation-overrides.md`

### 3.5 Agent-readable JSON schemas — added
Folder: `data/`
- `data/placement_legality_matrix.json`
- `data/dependency_graph_schema.json`
- `data/pattern_library.json`
- `data/validation_checklists.json`

### 3.6 Output templates — added/updated
Folder: `templates/`
- `templates/new-level-template.md` (updated: **game-pack loaded evidence** line)
- `templates/level-review-template.md` (updated: **game-pack evidence** section)
- `templates/validation-report-template.md`

### 3.7 Registry alignment
- **Updated:** `~/Projects/claude-config/config/agent-registry.json`  
  - D14 name → **General Level Designer**
  - version → **1.1**
  - capability list updated to match new scope

---

## 4) What stayed intentionally unchanged

- Canonical D14 path remains: `agents/design/puzzle-level-designer-2d/`
- D14 boundaries remain strict: **design/spec/validate only**, no code implementation, no Unity scene building.

---

## 5) Notes / follow-ups (optional)

- Legacy files should not carry game-specific mechanics/constants. If any legacy “mechanics catalog” exists, remove it and keep mechanics only in game-packs.

