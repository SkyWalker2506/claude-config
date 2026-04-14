---
last_updated: 2026-04-14
confidence: high
sources: [farm-architecture, render-distribution, gpu-patterns, tile-rendering]
---

# Render Farm Patterns

## Overview

Distributed rendering architectures: parallel frame rendering, tile-based split, GPU vs CPU clustering,
and work distribution patterns for scaling beyond single-machine limits.

## Single-Machine Baseline

### Sequential Frame Rendering
```bash
# Simplest: one frame at a time
blender -b scene.blend -o /renders/frame_####.png -s 1 -e 100
```

**Characteristics:**
- Blender uses all available CPU threads automatically
- Memory bottleneck: holds entire scene in RAM
- 1920x1080 typically 2-5 min per frame on modern CPU

### Multi-threaded CPU
```bash
# Force thread count (0 = auto)
blender -b scene.blend -t 8 -o /renders/frame_####.png -s 1 -e 100
```

## Tile-Based Rendering (Single Machine)

### Concept
Split single frame into tiles (64x64, 128x128, 256x256).
Each tile renders independently, reassembled at end.
Reduces per-tile memory, enables progressive output.

### Configuration
```python
import bpy

scene = bpy.context.scene

# Enable tiling for Cycles
scene.render.use_tile_x = True
scene.render.use_tile_y = True
scene.render.tile_x = 128
scene.render.tile_y = 128

# Tile sample mode (Adaptive)
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01
```

### Tile Pattern
```
Frame 1920x1080 → Tile 128x128
┌─────────────┐
│ T01 T02 T03 │
│ T04 T05 T06 │  (15 × 8 tiles)
│ ... ... ... │
└─────────────┘
```

### Blender Compositor → EXR Sequence
```python
# Render each tile to separate EXR
scene.render.filepath = "/renders/tile_" + str(tile_id) + "_####.exr"

# Compositor reassembles in post-process
bpy.ops.render.render(write_still=False)
```

## GPU Rendering Patterns

### CUDA (NVIDIA)
```bash
# Check GPU availability
blender -b scene.blend --engine CYCLES -p check_gpu.py

# Force CUDA
blender -b scene.blend -p set_cuda.py -o /renders/frame_####.png -s 1 -e 100
```

**set_cuda.py:**
```python
import bpy

prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'CUDA'
prefs.compute_device = 0  # First GPU

scene = bpy.context.scene
scene.render.device = 'GPU'
scene.cycles.device = 'GPU'
```

### OptiX (NVIDIA, newer)
```python
prefs.compute_device_type = 'OPTIX'
# High-level acceleration, similar to CUDA
```

### HIP (AMD)
```python
prefs.compute_device_type = 'HIP'
prefs.compute_device = 0
```

### Multi-GPU (Linked)
```python
# Multiple GPUs in single system
for i, device in enumerate(prefs.devices):
    if 'NVIDIA' in device.name:
        device.use = True  # Enable all NVIDIA GPUs
```

**Performance:** ~2-3x speedup with 2 GPUs, diminishing returns beyond 3.

## Distributed Render Patterns

### Pattern 1: Frame-Level Distribution (Farm)
```
Job Queue → Frame 1-20 → Worker A (GPU 0)
         → Frame 21-40 → Worker B (GPU 1)
         → Frame 41-60 → Worker C (GPU 2)
```

**Python Queue Coordinator:**
```python
import json
import subprocess

jobs = [
    {"id": "w1", "frames": [1, 20], "worker": "192.168.1.10"},
    {"id": "w2", "frames": [21, 40], "worker": "192.168.1.11"},
    {"id": "w3", "frames": [41, 60], "worker": "192.168.1.12"},
]

for job in jobs:
    cmd = [
        "ssh", job["worker"],
        "blender -b scene.blend -o /net/renders/ -s", str(job["frames"][0]),
        "-e", str(job["frames"][1])
    ]
    subprocess.Popen(cmd)
```

### Pattern 2: Tile-Level Distribution (Heavy Scenes)
```
Frame 1 → Tile A → Worker 1
       → Tile B → Worker 2
       → Tile C → Worker 3
       → Tile D → Worker 4
          (reassemble)
```

**Setup:**
- Split frame into 128x128 tiles
- Distribute tiles across workers
- Each renders subset, outputs tile EXR
- Compositor stitches back

### Pattern 3: Render Segments (Layer/Pass Split)
```
Frame 1 → Render Pass 1 (Diffuse) → Worker A
       → Render Pass 2 (Specular) → Worker B
       → Render Pass 3 (Normal) → Worker C
          (composite in post)
```

## Farm Architecture Decisions

| Scenario | Pattern | Workers | Notes |
|----------|---------|---------|-------|
| <100 frames, 1 scene | Frame distribution | 2-4 | Simplest, scalable |
| 1000+ frames | Frame + queue manager | 8+ | Job queuing, failover |
| 4K+ resolution | Tile distribution | 16+ | Memory-efficient |
| Multi-pass (VFX) | Render passes | 4-6 | Split by layer/pass |

## Work Queue Pattern (JSON)

```json
{
  "queue": [
    {
      "job_id": "shot_001_001",
      "blend_file": "s1_001.blend",
      "frames": {
        "start": 1,
        "end": 250
      },
      "assigned_worker": "gpu-01",
      "status": "in_progress",
      "created_at": "2026-04-14T10:00:00Z"
    },
    {
      "job_id": "shot_001_002",
      "blend_file": "s1_002.blend",
      "frames": {
        "start": 1,
        "end": 250
      },
      "assigned_worker": "gpu-02",
      "status": "pending",
      "created_at": "2026-04-14T10:05:00Z"
    }
  ],
  "workers": [
    {"id": "gpu-01", "type": "GPU", "device": "NVIDIA RTX 4090", "status": "busy"},
    {"id": "gpu-02", "type": "GPU", "device": "NVIDIA RTX 4080", "status": "idle"}
  ]
}
```

## Failure Handling

### Timeout + Retry
```python
import time

def render_with_retry(blend_file, frames, max_retries=3):
    for attempt in range(max_retries):
        try:
            subprocess.run(
                ["blender", "-b", blend_file, "-s", str(frames[0]), "-e", str(frames[1])],
                timeout=3600  # 1 hour timeout
            )
            return True
        except subprocess.TimeoutExpired:
            print(f"Attempt {attempt + 1} timeout, retrying...")
            time.sleep(5)
    return False  # Failed after retries
```

### Partial Frame Recovery
```python
# Check which frames already rendered
import os

def get_missing_frames(output_dir, total_frames):
    existing = set()
    for f in os.listdir(output_dir):
        if f.endswith('.png'):
            frame_num = int(f.split('_')[1])
            existing.add(frame_num)
    
    missing = set(range(1, total_frames + 1)) - existing
    return sorted(list(missing))

# Re-render only missing frames
missing = get_missing_frames("/renders", 250)
if missing:
    print(f"Missing frames: {missing}")
    subprocess.run(["blender", "-b", "scene.blend", "-s", str(missing[0]), "-e", str(missing[-1])])
```

## Network Storage Considerations

### NFS / SMB Mount Points
```bash
# Render to shared farm storage
blender -b scene.blend -o /mnt/farm/renders/shot_001_####.exr -s 1 -e 100
```

**Optimization:**
- Use `-o` with local SSD first, then batch-copy to NAS
- Reduces network I/O during render
- Faster feedback loop

### Bandwidth Estimate
```
1 frame (1920x1080, EXR 32-bit) ≈ 30-50 MB
100 frames = 3-5 GB transfer
1000 frames = 30-50 GB

At 1 Gbps network: 100 frames ≈ 5 min write time
```

## Optimization Tips

| Challenge | Solution |
|-----------|----------|
| Network bottleneck | Local cache + batch copy |
| GPU memory full | Lower resolution tile-render |
| CPU cache miss | Pin worker to NUMA nodes |
| Disk I/O contention | Separate render + storage disks |
| Frame wait time | Prioritize short-running frames first |

## Verification Checklist

- [ ] All workers have identical Blender version
- [ ] Blend files accessible from all workers (NFS/SMB verified)
- [ ] GPU drivers installed and tested on each worker
- [ ] Job queue tracks in-progress and failed renders
- [ ] Partial frame recovery implemented (missing frame detection)
- [ ] Network bandwidth sufficient for output throughput
- [ ] Load balancing spreads jobs evenly
