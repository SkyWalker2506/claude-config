---
last_updated: 2026-04-14
knowledge_filled: true
total_topics: 4
status: sharpened
---

# Knowledge Index

> Bu dosya agent'in bilgi haritasidir. Gorev alirken once bunu oku; sadece ilgili dosyalari yukle.

## Core Topics

### 1. Batch Render Setup
[Details](batch-render-setup.md)

**Scope:** Blender CLI headless rendering, frame ranges, Python scripts, render engines
**Key Commands:**
- `blender -b file.blend -o /output/frame_####.png -s 1 -e 100`
- `blender -b file.blend -p script.py --engine CYCLES`
**Use When:** Setting up basic render jobs, frame sequences, CLI configuration

---

### 2. Output Format Guide
[Details](output-format-guide.md)

**Scope:** PNG vs EXR vs JPEG, color depth (8/16/32-bit), transparency, compression
**Key Decisions:**
- PNG: 8/16-bit, RGBA, web-friendly, lossless
- EXR: 32-bit float, full HDR, VFX pipelines
- JPEG: 8-bit, smallest, lossy, no alpha
**Use When:** Choosing output format, configuring color depth, pipeline integration

---

### 3. Render Farm Patterns
[Details](render-farm-patterns.md)

**Scope:** Distributed rendering, tile-based splitting, GPU clustering, work distribution
**Patterns:**
- Frame-level distribution (workers render different frames)
- Tile-level distribution (split heavy scenes across workers)
- Render passes (split by layer/pass)
**Use When:** Scaling to 8+ workers, heavy scenes, render optimization

---

### 4. Render Queue Management
[Details](render-queue-management.md)

**Scope:** Job submission, progress tracking, error handling, retry logic, metrics
**Key Classes:** RenderQueue (JSON-based), FailedJobQueue (DLQ), progress logging
**Use When:** Batch job submission, failure recovery, status reporting, ETA calculation

---

## Quick Navigation

| Task | File | Section |
|------|------|---------|
| Run first test render | Batch Render Setup | Blender CLI Core Commands |
| Choose output format | Output Format Guide | Format Selection Decision Tree |
| Submit 100 frame job | Render Queue Management | Queue Management Patterns |
| Scale to 16 GPUs | Render Farm Patterns | Distributed Render Patterns |
| Debug render timeout | Batch Render Setup | Common Pitfalls |
| Check file sizes | Output Format Guide | Color Depth Explained |
| Track failed frames | Render Queue Management | Dead Letter Queue (DLQ) |
| Optimize tile rendering | Render Farm Patterns | Tile-Based Rendering |

---

## Cross-Topic Dependencies

```
Batch Render Setup
    ↓ (uses output from)
Output Format Guide
    ↓ (feeds into)
Render Queue Management
    ↓ (scales with)
Render Farm Patterns
```

## Knowledge Confidence

- **Batch Render Setup:** High (Blender API stable)
- **Output Format Guide:** High (industry standard)
- **Render Farm Patterns:** Medium-High (architecture varies by deployment)
- **Render Queue Management:** Medium (pattern-dependent on infrastructure)
