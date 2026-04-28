# Puzzle Dependency Graphs (Universal)

Dependency graphs prevent logic-chain errors by modeling what knowledge, state, object access, or actions must exist before a later step.

## Node types
- knowledge
- mechanic
- object_access
- spatial_access
- state_change
- lock
- key
- skill
- timing
- resource
- goal

## Edge types
- requires
- teaches
- unlocks
- blocks
- transforms
- tests

## Required per-level section

```md
## Dependency Model

### Player Already Knows
- ...

### This Level Teaches
- ...

### This Level Tests
- ...

### Required Dependencies (solve chain)
- Step 1 requires ...
- Step 2 requires ...
- Step 3 requires ...

### Invalid Dependencies Found
- None / list

### Later Levels May Depend On
- ...
```

## Validation rules
- No required step may depend on untaught knowledge.
- No circular dependency.
- No object should be required before it is reachable.
- No state change should be assumed without a trigger.
- No mechanic should be mandatory before its introduction.

## Design method
For complex levels, design backward from the goal:
1. Define final required state.
2. List prerequisites for that state.
3. Repeat until all prerequisites are already known or taught in-level.

