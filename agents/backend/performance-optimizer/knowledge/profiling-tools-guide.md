---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 4
---

# Profiling Tools Guide

## Quick Reference

| Domain | Tools |
|--------|-------|
| **Node.js** | `node --inspect`, Chrome DevTools, clinic.js, 0x |
| **JVM** | async-profiler, VisualVM |
| **Browser** | Performance tab, Lighthouse |
| **Go** | pprof |

**CPU vs wall time:** Hot loops vs waiting on I/O.

**2025–2026:** Continuous profiling in prod (Parca, Pyroscope) — sampling overhead low.

## Patterns & Decision Matrix

| Symptom | Profile |
|---------|---------|
| High CPU | CPU flame graph |
| Slow requests, low CPU | I/O, DB, locks |

## Code Examples

```bash
node --inspect dist/server.js
# Chrome: chrome://inspect → Open dedicated DevTools
```

## Anti-Patterns

| Bad | Why |
|-----|-----|
| Optimizing without profile | Wrong bottleneck |

## Deep Dive Sources

- [Node.js — Profiling](https://nodejs.org/en/docs/guides/simple-profiling)
- [Google — Profiling Go programs](https://go.dev/blog/pprof)
