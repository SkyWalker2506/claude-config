---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Unity Performance Profiling

## Quick Reference

| Tool | Shows |
|------|-------|
| **Profiler** | CPU/GPU, scripts |
| **Frame Debugger** | Draw calls |
| **Memory Profiler** | Allocations |

**GC:** Avoid per-frame `new` in hot paths; object pools.

## Code Examples

```text
Unity Profiler → CPU Usage → search Update() cost
Memory Profiler → capture → compare snapshots
```

## Deep Dive Sources

- [Unity — Profiler](https://docs.unity3d.com/Manual/Profiler.html)
