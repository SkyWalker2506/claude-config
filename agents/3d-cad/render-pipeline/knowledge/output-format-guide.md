---
last_updated: 2026-04-14
confidence: high
sources: [blender-manual, openexr-spec, production-guidelines]
---

# Output Format Guide

## Quick Reference

Blender render output formats: PNG, EXE, JPEG, TIFF, OpenEXR.
Trade-offs between file size, quality, transparency, and production flexibility.

| Format | Color Depth | Transparency | Compression | Use Case |
|--------|------------|-------------|-------------|----------|
| **PNG** | 8/16-bit | Yes (alpha) | Lossless | Web, previews, final stills |
| **EXR** | 16/32-bit float | Yes (multiple) | ZIP/RLE | VFX, color grading, compositing |
| **JPEG** | 8-bit | No | Lossy | Quick preview, web delivery |
| **TIFF** | 8/16-bit | Yes (alpha) | Lossless | Professional print, archival |
| **BMP** | 8-bit | No | Uncompressed | Legacy, quick checks |

## Format Selection Decision Tree

```
Is this for compositing/grading?
├─ YES → EXR (full precision, HDR)
└─ NO  → Is transparency needed?
        ├─ YES → PNG 16-bit or EXR
        └─ NO  → Is file size critical?
                ├─ YES → JPEG or PNG 8-bit
                └─ NO  → PNG 16-bit (safe default)
```

## PNG (Portable Network Graphics)

### Blender Setting
```
Format: PNG
Color: RGB or RGBA
Color Depth: 8-bit or 16-bit
Compression: 9 (max)
```

### Use Cases
- Web display (8-bit sufficient)
- Transparency-enabled previews
- Final stills with alpha channel
- Game engine pipelines (Unity, Unreal)

### Pros/Cons
- **Pros:** Lossless, wide support, HDR via 16-bit, small files
- **Cons:** No native HDR, 16-bit PNG slower than EXR

### Example CLI
```bash
blender -b scene.blend -o /output/frame_####.png -s 1 -e 100
# Blender defaults to PNG with RGBA if transparent
```

## EXR (OpenEXR)

### Blender Setting
```
Format: OpenEXR
Color: RGBA
Color Depth: 32-bit (full float) or 16-bit (half float)
Compression: ZIP (recommended) or RLE
Channels: RGB + Alpha + AOVs (crypto, Z-depth, normal, etc.)
```

### Use Cases
- Professional VFX pipeline
- Color grading in post-production (Nuke, DaVinci)
- Compositing (Blender Compositor, After Effects)
- HDR storage (full 32-bit float per channel)

### Pros/Cons
- **Pros:** Full HDR, lossless, multiple data layers, fast (ZIP compression)
- **Cons:** Larger files than PNG, less web support

### Example CLI
```bash
blender -b scene.blend -o /output/frame_####.exr -s 1 -e 100

# With Python to set 32-bit float
blender -b scene.blend -p set_exr.py -o /output/frame_####.exr -s 1 -e 100
```

### Python Script (set_exr.py)
```python
import bpy

scene = bpy.context.scene
scene.render.image_settings.file_format = 'OPEN_EXR'
scene.render.image_settings.color_depth = '32'  # 32-bit float
scene.render.image_settings.exr_codec = 'ZIP'   # Compression
```

## JPEG

### Blender Setting
```
Format: JPEG
Quality: 80-95 (higher = larger, less compression)
Color: RGB (no transparency)
Chroma Subsampling: 4:2:0 (default, acceptable)
```

### Use Cases
- Quick preview distribution
- Web thumbnails
- Social media uploads
- When alpha channel not needed

### Pros/Cons
- **Pros:** Smallest file size, universal web support
- **Cons:** Lossy (quality loss), no transparency, artifacts with edges

### Example CLI
```bash
blender -b scene.blend -o /output/preview_####.jpg -s 1 -e 10
# Quality set in Blender project or via Python
```

## TIFF

### Blender Setting
```
Format: TIFF
Color: RGBA
Color Depth: 16-bit
Compression: LZW or ZIP (lossless)
```

### Use Cases
- Professional print media
- Archival storage (long-term)
- Prepress workflows
- DTP (Desktop Publishing) pipelines

### Pros/Cons
- **Pros:** Industry standard for print, lossless, layer metadata support
- **Cons:** Large files, slower than PNG/EXR

## Color Depth Explained

| Depth | Bits/Channel | Range | Use Case |
|-------|-------------|-------|----------|
| **8-bit** | 0-255 | Integer | Web, video, previews |
| **16-bit (half)** | 0-65535 | Integer or Float | Professional stills, grading-friendly |
| **32-bit float** | IEEE 754 | Full precision | VFX, HDR compositing, precise math |

### When to Use
- **8-bit:** Final web/social content, no precision loss visible
- **16-bit:** Professional stills, grading room, good balance
- **32-bit:** VFX pipeline, color grading, mathematically precise compositing

## Transparency (Alpha Channel)

### PNG RGBA
```
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'  # Enable alpha
scene.render.use_transparency = True             # Transparent background
```

### EXR RGBA
```
scene.render.image_settings.file_format = 'OPEN_EXR'
scene.render.image_settings.color_mode = 'RGBA'
```

### Background in Blender
```python
# Transparent background (alpha)
bpy.context.scene.render.film_transparent = True

# White background (default)
bpy.context.scene.render.film_transparent = False
```

## Output Path and File Naming

### Frame Padding
```
frame_####.png    → frame_0001.png, frame_0002.png ...
render_##.exr     → render_01.exr, render_02.exr ...
shot_001_###.tif  → shot_001_001.tif, shot_001_002.tif ...
```

### Directory Structure Recommendation
```
/renders/
├── project_name/
│   ├── shot_001/
│   │   ├── lighting/
│   │   │   └── frame_####.exr
│   │   └── final/
│   │       └── frame_####.png
│   └── shot_002/
│       └── final/
│           └── frame_####.png
```

## Performance vs Quality Trade-offs

| Target | Format | Depth | Notes |
|--------|--------|-------|-------|
| Web preview | JPEG | 8-bit | Quality 85, smallest |
| Grading proof | EXR | 32-bit | Full HDR, precise math |
| Game engine | PNG | 8-bit | RGBA with alpha |
| Print | TIFF | 16-bit | LZW compression |
| VFX | EXR | 16-bit | ZIP compression, fast |

## Verification Checklist

- [ ] Format matches pipeline requirements (EXR for VFX, PNG for web)
- [ ] Color depth sufficient (8-bit web, 16-bit+ for grading)
- [ ] Transparency enabled if alpha needed
- [ ] Output path uses correct frame padding (`####`)
- [ ] Compression setting appropriate (ZIP for EXR, lossless for PNG)
- [ ] Directory structure matches naming convention
- [ ] First frame rendered successfully before batch submission
