# Mechanics — Golf Paper Craft (Implemented + Proposed)

This file is game-specific. D14 must not invent mechanics not listed here.

## Implemented mechanics (from prior catalog)

### hill
- **Data**: `{ type: 'hill', x, y, r, character }`
- **Role**: blocker/redirect.
- **Pitfall**: off the trajectory axis → decorative.

### tree
- **Data**: `{ type: 'tree', x, h, variant? }`
- **Role**: air blocker / gate.

### rock
- **Data**: `{ type: 'rock', x, y?, r }`
- **Role**: sharp ricochet.

### water
- **Data**: `{ type: 'water', x1, x2, hasCroc?: true, crocCount?: 1|2 }`
- **Role**: reset hazard.

### mud
- **Data**: `{ type: 'mud', x, w }`
- **Role**: ground speed tax.

### bridge
- **Data**: `{ type: 'bridge', x, w, gap? }`
- **Role**: safe traversal over hazard; precision target.

### pit
- **Data**: `{ type: 'pit', x, w }`
- **Role**: silent reset hazard.

### trampoline
- **Data**: `{ type: 'trampoline', x, y, w, h, character }`
- **Role**: vertical gate / bounce requirement.

### wind
- **Data**: `{ type: 'wind', x1, x2, force, character }`
- **Role**: horizontal force zone.

### ice
- **Data**: `{ type: 'ice', x1, x2 }`
- **Role**: momentum preservation.

### magnet
- **Data**: `{ type: 'magnet', x, y, r, strength }`
- **Role**: trajectory bending.

### portal
- **Data**: `{ type: 'portal', x, y, id, pair }`
- **Role**: teleport; non-euclidean routing.

### movingHill
- **Data**: `{ type: 'movingHill', x, y, r, amp, period }`
- **Role**: timing puzzle.

### spring
- **Data**: `{ type: 'spring', x, y, w, h }`
- **Role**: pure vertical kick with horizontal dump.

### fan
- **Data**: `{ type: 'fan', x1, x2, force, topY? }`
- **Role**: upward force channel.

## Proposed (not implemented)
- `saw`
- `bouncePad`
- `magnetReverse`

