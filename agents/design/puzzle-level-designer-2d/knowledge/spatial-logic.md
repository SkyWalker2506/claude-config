# Spatial Logic (Universal)

Goal: stop “nonsense placement” errors (unsupported objects, grounded objects on hazards, traversal objects leading nowhere).

## Object classes (taxonomy)
- grounded_object
- wall_mounted_object
- ceiling_mounted_object
- floating_object
- suspended_object
- hazard_zone
- goal_object
- traversal_object
- decorative_object
- interactive_object
- enemy
- pickup
- gate_or_lock
- platform
- cover
- trigger_zone

## Universal placement rules

### Grounded object rule
Grounded objects require valid support. They cannot be placed on/inside water, void, pit, lava, or deep hazard **unless** there is an explicit platform/island/support.

### Mounted object rule
Wall/ceiling-mounted objects require a valid wall/ceiling mount. If art implies mounting but no support exists, placement is invalid.

### Hazard zone rule
Hazard zones may contain:
- hazard-specific objects,
- bridges/platforms/islands,
- non-colliding decor,
- explicitly supported objects.

They must not contain ordinary grounded objects without support.

### Goal rule
A goal must be:
- reachable,
- readable,
- on valid destination surface,
- visually distinct from hazards,
- not overlapped by ambiguous hazards (goal-hazard confusion must be intentional and signposted).

### Traversal object rule
Traversal objects must connect meaningful spaces. A bridge that crosses nothing or a ladder that leads nowhere is invalid unless explicitly decorative and visually downgraded.

### Decorative object rule
Decor must not create false affordances. If it looks interactable, it must either be interactable or visually downgraded.

### Support declaration rule
Every physical object must declare one support type:
- ground_support
- platform_support
- wall_mount
- ceiling_mount
- suspended_support
- floating_support
- no_support_required

If none applies, invalid.

## Auto-correction ladder (in order)
If invalid placement is found:
1. Move object to valid support.
2. Add support/island/platform.
3. Replace object with compatible object.
4. Convert to non-colliding decor.
5. Remove object.

