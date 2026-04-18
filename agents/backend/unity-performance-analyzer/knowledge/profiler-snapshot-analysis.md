---
last_updated: 2026-04-18
confidence: high
sources: 3
---

# Profiler Snapshot Analysis

## Quick Reference
| Konu | Aciklama |
|------|----------|
| ProfilerRecorder | Real-time metric capture, low-overhead sampling |
| Frame Debugger | Draw-call visualization, GPU state introspection |
| Hot-path | Calisiklarinin %80'ini tutan fonksiyonlar |
| Markerlar | Custom ProfilerMarker ile user-code profiling |

## ProfilerRecorder API

### Setup
```csharp
using Unity.Profiling;

// FPS metric
var fpsRecorder = new ProfilerRecorder(ProfilerCategory.Rendering, "FPS");
fpsRecorder.Start();

// Memory
var memRecorder = new ProfilerRecorder(ProfilerCategory.Memory, "Total Used Memory");
memRecorder.Start();

// GC Alloc
var gcRecorder = new ProfilerRecorder(ProfilerCategory.Memory, "GC.Alloc");
gcRecorder.Start();

// Vertex count
var vertexRecorder = new ProfilerRecorder(ProfilerCategory.Rendering, "Vertices");
vertexRecorder.Start();

// Draw-call count
var drawCallRecorder = new ProfilerRecorder(ProfilerCategory.Rendering, "Draw Calls");
drawCallRecorder.Start();
```

### Read Value
```csharp
if (fpsRecorder.Valid)
{
    var fps = (int)fpsRecorder.LastValue;
    Debug.Log($"FPS: {fps}");
}

if (drawCallRecorder.Valid)
{
    var drawCalls = (int)drawCallRecorder.LastValue;
    Debug.Log($"Draw Calls: {drawCalls}");
}
```

## Frame Debugger Patterns

### Mobile Frame Analysis (URP)
1. Window → Frame Debugger
2. Frame Debugger'i ac
3. Draw calls secis:
   - Opaque objects (önce renderlenirler)
   - Transparent objects (son)
   - UI Overlays
4. Her bir draw call'da:
   - Geometry (vertex/triangle sayisi)
   - Shader (variant bilgisi)
   - Material batching status
   - Texture bindings

### Hot-path Identification
```
Profiler kategorileri:
├── Rendering (Draw Calls, GPU time, Batching efficiency)
├── Memory (GC Alloc, Heap usage, Fragmentation)
├── Physics (Raycasts, Colliders, Constraints)
├── Scripts (C# time, coroutines)
└── UI (Canvas, Layout rebuilds, Draw calls)
```

## Anti-Patterns
- Profiler'i production build'te kapali birakmak — release build'te overhead en dusuk
- Tek frame snapshot'ina dayanmak — 100+ frame'i incelemek
- GC alloc'lari ignore etmek — heap fragmentation'a yol acar
- Asset memory'yi kontrol etmeden GPU memory'ye odaklanmak

## Decision Matrix

| Senaryo | Araclar | Aci |
|---------|--------|-----|
| FPS dusuk | ProfilerRecorder (draw calls, GPU time) + Frame Debugger | GPU bound |
| Bellek yuksek | Memory profiler, GC alloc histogram | CPU bound |
| Jank spikes | ProfilerRecorder + Frame Debugger, zaman serisi | Timing variance |
| Draw-call fazla | Batching audit, SRP Batcher check | Submission overhead |

## Deep Dive Sources
- [Unity Profiler Docs](https://docs.unity3d.com/Manual/Profiler.html)
- [ProfilerRecorder API](https://docs.unity3d.com/ScriptReference/Unity.Profiling.ProfilerRecorder.html)
- [Frame Debugger](https://docs.unity3d.com/Manual/FrameDebugger.html)
