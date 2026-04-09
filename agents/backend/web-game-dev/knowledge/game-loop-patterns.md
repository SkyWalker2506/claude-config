---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Game Loop Patterns

## Quick Reference

| Pattern | Description |
|---------|-------------|
| **Fixed timestep** | Physics at 60Hz; render interpolates |
| **Variable** | Simple; unstable physics |
| **requestAnimationFrame** | Browser sync to display |

**Accumulator pattern:** Catch up capped steps to avoid spiral of death.

## Code Examples

```typescript
const FIXED = 1000 / 60;
let acc = 0;
function frame(now: number) {
  acc += now - last; last = now;
  while (acc >= FIXED) { updatePhysics(FIXED); acc -= FIXED; }
  render();
  requestAnimationFrame(frame);
}
```

## Deep Dive Sources

- [Fix Your Timestep — Glenn Fiedler](https://gafferongames.com/post/fix_your_timestep/)
