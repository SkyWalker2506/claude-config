---
last_updated: 2026-04-14
confidence: high
sources: [blender-manual, api-docs, production-patterns]
---

# Batch Render Setup

## Quick Reference

Blender CLI'da headless (background) render işleri çalıştırma ve frame range yapılandırması.

| Konsept | Açıklama |
|---------|----------|
| **Headless Rendering** | `-b` / `--background` flag'i ile UI olmadan render |
| **Python Scripts** | `-p` / `--python` ile özel script çalıştırma |
| **Frame Range** | `-f N` (single frame) veya `-s N -e M` (start-end) |
| **Output Path** | `-o /path/` ile çıktı dizini, `####` frame pad için |
| **Engine Selection** | Cycles vs Eevee, GPU vs CPU |

## Blender CLI Core Commands

### macOS / Linux
```bash
# Generic path (macOS)
/Applications/Blender.app/Contents/MacOS/Blender

# Linux
blender
```

### Basic Headless Render
```bash
# Single frame
blender -b file.blend -o /output/render_####.png -f 1

# Frame range (1-100)
blender -b file.blend -o /output/frame_####.png -s 1 -e 100

# With render engine (Cycles)
blender -b file.blend -o /output/frame_####.png -s 1 -e 100 --engine CYCLES

# EEVEE engine
blender -b file.blend -o /output/frame_####.png -s 1 -e 100 --engine EEVEE
```

### With Python Script
```bash
# Run custom Python script in Blender context
blender -b file.blend -p setup_render.py -o /output/frame_####.png -s 1 -e 100

# Pass args to script (after --)
blender -b file.blend -p render_batch.py -- --samples 128 --denoise
```

### Common Options
```bash
# Suppress splash screen
blender -b file.blend -noaudio -o /output/ -s 1 -e 100

# Verbose logging
blender -b file.blend -d -o /output/ -s 1 -e 100

# Set threads (CPU)
blender -b file.blend -t 8 -o /output/ -s 1 -e 100

# Custom Python path
blender -b file.blend --python-expr "import sys; print(sys.path)" 
```

## Frame Padding Convention

Blender uses `#` symbols for frame numbering:
- `frame_####.png` → `frame_0001.png`, `frame_0002.png`, etc.
- `render_##.exr` → `render_01.exr` (2 digits)
- Single `#` → single digit (0-9 only)

## Render Engine Selection

| Engine | GPU Support | Speed | Quality | Use Case |
|--------|------------|-------|---------|----------|
| **Cycles** | CUDA, HIP, OptiX | Slow-Medium | Photorealistic | Product viz, film |
| **EEVEE** | NVIDIA, AMD | Fast | Real-time quality | Games, fast preview |

```bash
# Check available engines
blender -b file.blend --engine CYCLES -o /tmp/ -f 1
blender -b file.blend --engine EEVEE -o /tmp/ -f 1
```

## Python Script Pattern (setup_render.py)

```python
import bpy

# Access active scene
scene = bpy.context.scene

# Set render engine
scene.render.engine = 'CYCLES'  # or 'BLENDER_EEVEE'

# Samples / denoise
if scene.render.engine == 'CYCLES':
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True

# Frame range
scene.frame_start = 1
scene.frame_end = 100

# Output path already set via CLI -o flag
# But can override:
scene.render.filepath = "/path/to/output_####.png"
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_depth = '16'

# Render
bpy.ops.render.render(write_still=True)
```

## Batch Submission Pattern

### Bash Loop (Sequential)
```bash
#!/bin/bash
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
INPUT="scene.blend"
OUTPUT_DIR="/renders"
FRAMES=1-100

$BLENDER -b $INPUT -o $OUTPUT_DIR/frame_#### -s 1 -e 100 --engine CYCLES
```

### Queue File (JSON)
```json
{
  "jobs": [
    {
      "id": "job_001",
      "blend_file": "asset_01.blend",
      "frames": [1, 50],
      "engine": "CYCLES",
      "samples": 256,
      "output_prefix": "asset_01_"
    },
    {
      "id": "job_002",
      "blend_file": "asset_02.blend",
      "frames": [1, 100],
      "engine": "EEVEE",
      "samples": 32,
      "output_prefix": "asset_02_"
    }
  ]
}
```

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| "Invalid output path" | Ensure directory exists before render; use absolute paths |
| Frame sequence gaps | Check `-s` / `-e` bounds; verify no errors in log |
| GPU out of memory | Lower `--cycles-device-type CPU` or reduce resolution |
| Scene not loading | Verify `.blend` file path and Blender version compat |
| Python script not found | Use absolute path or ensure cwd is correct |

## Performance Tips

- Use GPU rendering when available (CUDA/HIP faster than CPU)
- Lower sample count for previews (16-32), higher for final (256+)
- Denoise to reduce sample requirements
- Tile-based rendering for large images (64x64 or 128x128 tiles)
- Multi-threaded CPU: `-t 0` = auto (all cores)

## Verification Checklist

- [ ] Output directory exists and is writable
- [ ] Frame range matches scene duration
- [ ] Render engine supports desired features
- [ ] Sample count / denoise settings configured
- [ ] Python script (if used) has correct paths and syntax
- [ ] Log files capture errors for debugging
