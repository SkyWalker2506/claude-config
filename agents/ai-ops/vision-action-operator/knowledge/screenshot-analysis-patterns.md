---
last_updated: 2026-04-18
confidence: high
sources: 5
---

# Screenshot Analysis Patterns

## Quick Reference

UI element detection, anchor point matching, ve pixel coordinates'dan GameObject resolution işlemi.

| Kavram | Açıklama |
|--------|----------|
| Anchor Detection | UI element köşelerini bulma (TL, TR, BL, BR) |
| Pixel Mapping | Screenshot koordinat → Scene space dönüşümü |
| State Detection | UI state (active, disabled, hidden) bulma |
| Confidence Score | Detection kesinliğini 0.0-1.0 ile skalama |

## Detection Heuristics

### 1. UI Element Localization

Ekran görüntüsünde UI elementlerini bulma adımları:

```
1. Edge detection (Canny/Sobel) → kontürleri bul
2. Rectangle fitting → element bounds'u tahmin et
3. Color analysis → foreground/background ayrıştır
4. Text OCR (optional) → label match for verification
5. Return: { name, bounds: {x, y, w, h}, confidence: 0.85 }
```

**Örnek deteksiyon:**
- Button "Save": bounds=[120, 450, 80, 40], confidence=0.92
- Input Field "Name": bounds=[50, 200, 300, 25], confidence=0.88
- Panel "Settings": bounds=[10, 10, 980, 590], confidence=0.95

### 2. Anchor Point Matching

Her UI element'in reference anchor'u karşılaştırma:

```
Detected anchor = {left: 120, top: 450, width: 80, height: 40}

Known patterns (cache'den):
  - Button.Save: {left: 120, top: 450, w: 80, h: 40} → EXACT MATCH (confidence=1.0)
  - Dialog.Confirm: {left: 300, top: 200, w: 150, h: 100} → no match

Match algorithm: Jaccard similarity = intersection / union
  If similarity >= 0.85 → MATCH (cache hit)
  If similarity < 0.85 → NEW ELEMENT (live analysis)
```

### 3. Coordinate to GameObject Resolution

Screenshot pixel → Scene GameObject mapping:

```
Screenshot resolution: 1920x1080
Detected element (button): screen_coords = (120, 450)

Mapping logic:
1. Get Canvas bounds in world space
2. Calculate screen-to-canvas scale
3. Convert pixel coords to Canvas local space
4. Find GameObject at that Canvas position
5. Return: GameObject name, Component type, State

Example:
  screen: (120, 450) 
  → canvas_local: (60, 215)
  → gameobject: "UI/Buttons/SaveButton"
  → component: Button (enabled=true, interactable=true)
```

### 4. State Detection Rules

UI elementinin durumunu tespit etme:

| State | Detection Signal | Confidence Threshold |
|-------|------------------|----------------------|
| **active** | Color brightness high, interaction enabled | >= 0.80 |
| **disabled** | Color desaturated, opacity < 0.7 | >= 0.85 |
| **hidden** | Element not visible in screenshot | 1.0 (binary) |
| **focused** | Border highlight or glow effect | >= 0.75 |
| **pressed** | Inset shadow or color shift | >= 0.78 |

**Örnek state detection:**
```json
{
  "element": "Button_Save",
  "states": {
    "visible": true,
    "enabled": true,
    "focused": false,
    "interactable": true,
    "text_color": "rgb(255, 255, 255)",
    "bg_color": "rgb(0, 122, 204)"
  },
  "confidence": 0.88
}
```

## Patterns & Decision Matrix

### High Confidence Scenarios

| Senaryo | Heuristic | Action |
|---------|-----------|--------|
| Static UI layout | Element bounds stable, cache hit | Use cached CRAFT ops |
| Button click target | Center of button detected clearly | Derive Modify op (state) |
| Dialog appearance | Modal bounds detected, state=active | Derive Create ops (child elements) |
| Text input clear | Input field bounds, state=empty | Derive Modify op (text content) |

### Low Confidence Scenarios

| Senaryo | Risk | Mitigation |
|---------|------|-----------|
| Overlapping elements | Ambiguous anchor | Request user clarification or live analysis retry |
| Dynamic layout | Element position varies | Skip cache, force live analysis |
| Partial occlusion | Element partially hidden | Use visible bounds, flag as "incomplete" |
| Low resolution image | Pixel artifacts, noise | Reject screenshot, request higher res |

## Code Examples

### Pattern Detection Pseudocode

```python
def detect_ui_elements(screenshot: Image) -> List[UIElement]:
    """
    Analyze screenshot ve UI elementleri bul.
    
    Returns: [{name, bounds, confidence, state}, ...]
    """
    edges = canny_edge_detection(screenshot)
    contours = find_contours(edges)
    
    elements = []
    for contour in contours:
        bounds = fit_rectangle(contour)
        if bounds.area > MIN_ELEMENT_SIZE:
            colors = extract_dominant_colors(screenshot[bounds])
            state = infer_state(colors, bounds)
            
            element = {
                'bounds': bounds,
                'colors': colors,
                'state': state,
                'confidence': compute_confidence(contour, bounds)
            }
            elements.append(element)
    
    return elements
```

### Coordinate Mapping Pseudocode

```python
def map_pixel_to_gameobject(
    pixel_x: int, pixel_y: int,
    screenshot_size: (int, int),
    canvas_world_bounds: Bounds
) -> GameObject:
    """
    Screenshot pixel coordinate → Scene GameObject.
    """
    screen_w, screen_h = screenshot_size
    
    # Normalize to 0.0-1.0
    norm_x = pixel_x / screen_w
    norm_y = pixel_y / screen_h
    
    # Map to canvas local space
    canvas_x = canvas_world_bounds.min_x + norm_x * canvas_world_bounds.width
    canvas_y = canvas_world_bounds.min_y + norm_y * canvas_world_bounds.height
    
    # Find GO at position
    gameobject = raycast_scene(canvas_x, canvas_y)
    return gameobject
```

### State Detection Pseudocode

```python
def detect_state(element: UIElement) -> Dict[str, Any]:
    """
    UI element state'i belirle (active, disabled, focused vb.).
    """
    colors = element['colors']
    bounds = element['bounds']
    
    # Brightness check
    brightness = mean([r, g, b] for r, g, b in colors)
    
    # Saturation check (desaturated = disabled)
    saturation = max_color_saturation(colors)
    
    # Border check (focused)
    border_pixels = detect_edge_pixels(bounds, screenshot)
    
    state = {
        'active': brightness > 128 and saturation > 0.3,
        'disabled': saturation < 0.2,
        'focused': len(border_pixels) > MIN_BORDER_PIXELS,
        'interactable': brightness > 100 and saturation > 0.2
    }
    
    return state
```

## Anti-Patterns

- **Cascade bias**: İlk detected element'i tüm koordinat mapping'e güvenmek — her element için ayrı validate et
- **State assumption**: Previous state'i assume etmek — her screenshot'ta fresh detection yap
- **Resolution mismatch**: Canvas size ≠ screenshot size → mapping hataları — mutlaka normalization yap
- **Confidence threshold blind**: Detection confidence'ı ignore etmek → her zaman >= 0.75 threshold kontrol et
- **Cache without verification**: Pattern cache'den ops alıp state hash verify etmemek — always hash check

## Deep Dive Sources

- [Unity Canvas Rendering](https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/UICanvas.html) — coordinate systems
- [Image Processing Handbook](https://www.cambridge.org/core/books/image-processing) — edge detection, contour analysis
- [OpenCV Documentation](https://docs.opencv.org/4.x/) — practical vision algorithms
- [CRAFT Tool Integration](../../../../../../ccplugin-unity-craft/SKILL.md) — ops and state tracking

---

**Revision**: Screenshot analizi 2026-04-18 güncellenmiş; edge detection heuristics v3 + state inference confidence model.
