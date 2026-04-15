---
last_updated: 2026-04-14
refined_by: agent-sharpen round 3
confidence: high
sources: [Blender 4.0/4.1/4.2/5.0 release notes, Blender Python API changelog, community migration guides, live test Blender 5.1.0]
---

# Blender 4.x / 5.x API Değişiklikleri

## Özet: Kritik Breaking Changes

| Versiyon | Değişiklik | Etki |
|----------|-----------|------|
| 4.0 | `use_auto_smooth` kaldırıldı | Smooth shading farklı çalışıyor |
| 4.0 | Principled BSDF input isimleri değişti | Material node kodu bozulur |
| 4.0 | `EEVEE` engine adı değişmedi (4.2'de değişti) | |
| 4.2 | `BLENDER_EEVEE` → `BLENDER_EEVEE_NEXT` | render engine seçimi bozulur |
| 4.2 | Geometry Nodes socket API değişti | GN scriptleri bozulabilir |
| 4.3+ | Action (animasyon) slot sistemi | Animasyon rig kodları etkilendi |
| 5.0 | Devam eden refactor (Grease Pencil v3) | GP scriptleri değişti |

---

## use_auto_smooth Kaldırıldı (Blender 4.0+)

**Eski kod (ÇALIŞMAZ Blender 4.0+):**
```python
obj.data.use_auto_smooth = True
obj.data.auto_smooth_angle = math.radians(30)
```

**Yeni yaklaşım (Blender 4.0+):**
```python
# Yöntem 1: Shade Smooth with angle (operator)
bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))

# Yöntem 2: Smooth Shade + custom normals attribute
bpy.ops.object.shade_smooth()
# Angle-based smooth için mesh attribute kullan:
mesh = obj.data
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.customdata_custom_splitnormals_clear()
bpy.ops.object.mode_set(mode='OBJECT')
mesh.normals_split_custom_set_from_vertices(...)  # advanced

# Yöntem 3: Smooth by Angle Modifier (en güvenli)
mod = obj.modifiers.new("SmoothByAngle", 'SMOOTH_BY_ANGLE')
mod.angle = math.radians(30)
```

**Önerilen approach (script için):**
```python
def apply_smooth_shading(obj, angle_degrees=30):
    """4.0+ uyumlu smooth shading"""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        # 4.0+ yol
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle_degrees))
    except AttributeError:
        # Fallback: eskiye uyumlu
        bpy.ops.object.shade_smooth()
        try:
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = math.radians(angle_degrees)
        except AttributeError:
            pass  # 4.0+ use_auto_smooth yok
```

---

## Principled BSDF Input İsimleri (Blender 4.0+ / 5.1)

> **Blender 5.1 tam input listesi (live test, 2026-04-14):**
> Base Color, Metallic, Roughness, IOR, Alpha, Normal, Weight,
> Diffuse Roughness, Subsurface Weight, Subsurface Radius, Subsurface Scale,
> Subsurface IOR, Subsurface Anisotropy, Specular IOR Level, Specular Tint,
> Anisotropic, Anisotropic Rotation, Tangent, Transmission Weight,
> Coat Weight, Coat Roughness, Coat IOR, Coat Tint, Coat Normal,
> Sheen Weight, Sheen Roughness, Sheen Tint, Emission Color, Emission Strength,
> Thin Film Thickness, Thin Film IOR

**Blender 3.x ve öncesi → Blender 4.0+ değişimleri:**

| Blender 3.x | Blender 4.0+ / 5.1 | Not |
|------------|-------------------|-----|
| `"Subsurface"` | `"Subsurface Weight"` | SSS kuvveti |
| `"Specular"` | `"Specular IOR Level"` | Specular artık IOR bazlı |
| `"Specular Tint"` | `"Specular Tint"` | Aynı kaldı |
| `"Transmission"` | `"Transmission Weight"` | |
| `"Coat"` | `"Coat Weight"` | Clear coat |
| `"Clearcoat"` | `"Coat Weight"` | Eski isim kaldırıldı |
| `"Sheen"` | `"Sheen Weight"` | |
| `"IOR"` | `"IOR"` | Aynı kaldı |
| `"Emission"` | `"Emission Color"` | Ayrı strength input geldi |
| `"Subsurface Color"` | **KALDIRILDI** | 5.x'te yok |

```python
# YANLIŞ — Blender 3.x kodu (4.0'da hata verir):
bsdf.inputs["Subsurface"].default_value = 0.3
bsdf.inputs["Specular"].default_value = 0.5

# DOĞRU — 4.0+ uyumlu:
bsdf.inputs["Subsurface Weight"].default_value = 0.3
bsdf.inputs["Specular IOR Level"].default_value = 0.5
```

**Güvenli bsdf input setter (versiyon bağımsız):**
```python
def set_bsdf_input(bsdf, name_3x, name_4x, value):
    """Blender 3.x ve 4.x uyumlu input setter"""
    if name_4x in bsdf.inputs:
        bsdf.inputs[name_4x].default_value = value
    elif name_3x in bsdf.inputs:
        bsdf.inputs[name_3x].default_value = value
    else:
        print(f"WARN: BSDF input bulunamadı: {name_4x} / {name_3x}")

# Kullanım:
set_bsdf_input(bsdf, "Subsurface", "Subsurface Weight", 0.3)
set_bsdf_input(bsdf, "Specular", "Specular IOR Level", 0.5)
set_bsdf_input(bsdf, "Transmission", "Transmission Weight", 0.0)
set_bsdf_input(bsdf, "Coat", "Coat Weight", 0.0)
```

---

## EEVEE Engine Adı

> **Kritik düzeltme (live test 2026-04-14, Blender 5.1.0):**
> `BLENDER_EEVEE_NEXT` 5.1'de **kaldırıldı**. `BLENDER_EEVEE` geri döndü.

```
Blender 3.x - 4.1 : BLENDER_EEVEE
Blender 4.2 - 4.x : BLENDER_EEVEE_NEXT
Blender 5.0+       : BLENDER_EEVEE  (5.1 live test ile doğrulandı)
```

```python
# Versiyon-bağımsız güvenli setter (5.1 dahil):
def set_eevee_engine(scene):
    version = bpy.app.version
    if (4, 2, 0) <= version < (5, 0, 0):
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        scene.render.engine = 'BLENDER_EEVEE'

# Blender 5.1 direkt kullanım:
scene.render.engine = 'BLENDER_EEVEE'   # ✅ DOĞRU
# scene.render.engine = 'BLENDER_EEVEE_NEXT'  # ❌ YANLIŞ — 5.1'de yok
```

**Not:** `CYCLES` ismi hiç değişmedi. Cycles scriptleri tüm versiyonlarda çalışır.

---

## Geometry Nodes Socket API (Blender 3.2+ ve 4.x)

```python
# ESKİ (Blender 3.1 ve öncesi) — ÇALIŞMAZ:
node_tree.inputs.new('NodeSocketFloat', 'My Input')
node_tree.outputs.new('NodeSocketGeometry', 'Geometry')

# YENİ (Blender 3.2+) — DOĞRU:
node_tree.interface.new_socket(
    name='My Input',
    socket_type='NodeSocketFloat',
    in_out='INPUT'
)
node_tree.interface.new_socket(
    name='Geometry',
    socket_type='NodeSocketGeometry',
    in_out='OUTPUT'
)
```

**Blender 4.0+'da socket tipleri:**
```python
# Geometry Nodes için geçerli socket tipleri (4.0+)
VALID_SOCKET_TYPES = {
    'NodeSocketGeometry',
    'NodeSocketFloat',
    'NodeSocketInt',
    'NodeSocketBool',
    'NodeSocketVector',
    'NodeSocketColor',
    'NodeSocketMaterial',
    'NodeSocketObject',
    'NodeSocketImage',
    'NodeSocketMenu',  # 4.0+ yeni
}
```

---

## Modifier API Değişiklikleri

### Smooth Modifier (4.0+)
```python
# ESKİ:
mod = obj.modifiers.new("Smooth", 'SMOOTH')
mod.factor = 0.5
mod.iterations = 10

# BLENDER 4.0+ Ek modifier:
# "Smooth by Angle" modifier artık mevcut
mod = obj.modifiers.new("SmoothAngle", 'SMOOTH_BY_ANGLE')
mod.angle = math.radians(30)  # bu açıdan az → smooth, fazla → flat
```

### Remesh Modifier
```python
# Quad remesh (4.1+) — voxel yerine quad topoloji
obj.data.remesh_mode = 'QUAD'
obj.data.remesh_voxel_size = 0.05
bpy.ops.object.quadriflow_remesh(
    target_faces=5000,
    use_mesh_curvature=True,
    use_preserve_sharp=True,
    use_preserve_boundary=True
)
```

---

## Armature / Pose API (4.3+)

Blender 4.3 animasyon sistemi "Versioned Actions" ekledi:

```python
# ESKİ (4.2-):
action = bpy.data.actions.new("MyAction")
obj.animation_data.action = action

# YENİ (4.3+) — slot sistemi:
action = bpy.data.actions.new("MyAction")
obj.animation_data_create()
track = obj.animation_data.nla_tracks.new()
slot = action.slots.new('OBJECT', obj.name)
obj.animation_data.action = action
# obj.animation_data.action_slot = slot  # aktif slot seç

# Güvenli backward-compatible:
def assign_action(obj, action):
    if obj.animation_data is None:
        obj.animation_data_create()
    obj.animation_data.action = action
    # 4.3+ slot varsa:
    if hasattr(obj.animation_data, 'action_slot'):
        slots = action.slots
        if slots:
            obj.animation_data.action_slot = slots[0]
```

---

## Versiyon Tespiti (Runtime Check)

```python
import bpy

def get_blender_version():
    return bpy.app.version  # tuple: (major, minor, patch)

def is_blender_4x():
    return bpy.app.version >= (4, 0, 0)

def is_blender_42_plus():
    return bpy.app.version >= (4, 2, 0)

def is_blender_43_plus():
    return bpy.app.version >= (4, 3, 0)

# Kullanım:
if is_blender_4x():
    # 4.0+ kod yolu
    bsdf.inputs["Subsurface Weight"].default_value = 0.3
else:
    # 3.x kod yolu
    bsdf.inputs["Subsurface"].default_value = 0.3
```

---

## bpy.app Özellikleri

```python
import bpy

print(bpy.app.version)          # (4, 2, 0)
print(bpy.app.version_string)   # "4.2.0"
print(bpy.app.build_date)       # build tarihi
print(bpy.app.background)       # True = headless mod (script çalışıyor)
```

---

## Özet: Script Başına Eklenecek Uyumluluk Kodu

```python
import bpy
import bmesh
import math
from mathutils import Vector

# Versiyon sabitleri
BL_VERSION = bpy.app.version
IS_4X = BL_VERSION >= (4, 0, 0)
IS_42 = BL_VERSION >= (4, 2, 0)

# EEVEE engine adı — 5.1'de EEVEE_NEXT kaldırıldı, EEVEE geri döndü
IS_5X = BL_VERSION >= (5, 0, 0)
EEVEE_ENGINE = 'BLENDER_EEVEE_NEXT' if (IS_42 and not IS_5X) else 'BLENDER_EEVEE'

# BSDF input isim haritası
BSDF_NAMES = {
    'subsurface': 'Subsurface Weight' if IS_4X else 'Subsurface',
    'specular':   'Specular IOR Level' if IS_4X else 'Specular',
    'transmission': 'Transmission Weight' if IS_4X else 'Transmission',
    'coat':       'Coat Weight' if IS_4X else 'Coat',
    'sheen':      'Sheen Weight' if IS_4X else 'Sheen',
}

def bsdf_set(bsdf, key, value):
    """Versiyon-bağımsız BSDF input setter"""
    input_name = BSDF_NAMES.get(key, key)
    if input_name in bsdf.inputs:
        bsdf.inputs[input_name].default_value = value
```
---

## Blender 5.1 — Live Test Özeti (2026-04-14)

Blender 5.1.0 (build 2026-03-17) ile doğrulandı:

| Özellik | Durum |
|---------|-------|
| `BLENDER_EEVEE` | ✅ Çalışıyor |
| `BLENDER_EEVEE_NEXT` | ❌ Yok — sadece 4.2-4.x'te vardı |
| `CYCLES` | ✅ Çalışıyor |
| `BLENDER_WORKBENCH` | ✅ Çalışıyor |
| Principled BSDF `Subsurface Weight` | ✅ Var |
| Principled BSDF `Specular IOR Level` | ✅ Var |
| Principled BSDF `Subsurface Color` | ❌ Yok — kaldırıldı |
| Principled BSDF `Emission Color` + `Emission Strength` | ✅ Var (artık ayrı) |

---

## Blender 5.1 — Ek Düzeltme ve Açıklamalar

> Yukarıdaki "5.1 Doğrulanmış Gerçekler" bölümünü bu bölümle birlikte oku.

### EEVEE Engine Adı Özeti (Tüm Versiyonlar)

| Versiyon | Engine Adı |
|---------|-----------|
| 4.1 ve öncesi | `BLENDER_EEVEE` |
| 4.2 – 4.x | `BLENDER_EEVEE_NEXT` |
| **5.0+** | **`BLENDER_EEVEE`** (geri döndü) |

```python
# Güvenli EEVEE engine seçimi:
def get_eevee_engine_name():
    v = bpy.app.version
    if (4, 2, 0) <= v < (5, 0, 0):
        return 'BLENDER_EEVEE_NEXT'
    return 'BLENDER_EEVEE'

scene.render.engine = get_eevee_engine_name()
```

### Modifier Apply Sırası

```
DOĞRU: Mirror → Smooth By Angle → Subdivision
YASAK: Subdivision → Mirror  (simetri kaybolur)
```

```python
def apply_modifiers_in_order(obj):
    APPLY_ORDER = ['MIRROR', 'CORRECTIVE_SMOOTH', 'SMOOTH_BY_ANGLE', 'SUBSURF']
    for mod_type in APPLY_ORDER:
        for mod in list(obj.modifiers):
            if mod.type == mod_type:
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                except RuntimeError as e:
                    print(f"WARN: {mod.name} apply basarisiz: {e}")
```

### bpy.ops.object.convert — Metaball Context

```python
def safe_metaball_convert(meta_obj):
    """4.x/5.x uyumlu metaball -> mesh convert."""
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = meta_obj
    meta_obj.select_set(True)
    bpy.context.view_layer.update()
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    try:
        bpy.ops.object.convert(target='MESH')
        return bpy.context.active_object
    except RuntimeError as e:
        print(f"ERROR convert: {e}")
        return None
# POLL() HATASI: meta_obj aktif degil | Object mode degil | depsgraph eski
```

### Guncel Uyumluluk Kodu (4.x + 5.x)

```python
BL_VERSION = bpy.app.version
IS_4X = BL_VERSION >= (4, 0, 0)
IS_42 = BL_VERSION >= (4, 2, 0)
IS_5X = BL_VERSION >= (5, 0, 0)

# EEVEE — 5.x'te 'BLENDER_EEVEE_NEXT' KALDIRILDI
EEVEE_ENGINE = 'BLENDER_EEVEE_NEXT' if (IS_42 and not IS_5X) else 'BLENDER_EEVEE'

BSDF_NAMES = {
    'subsurface':   'Subsurface Weight',
    'specular':     'Specular IOR Level',
    'transmission': 'Transmission Weight',
    'coat':         'Coat Weight',
    'sheen':        'Sheen Weight',
    'emission':     'Emission Color',  # 5.x: "Emission" artik yok
}

def bsdf_set(bsdf, key, value):
    name = BSDF_NAMES.get(key, key)
    if name in bsdf.inputs:
        bsdf.inputs[name].default_value = value
    else:
        print(f"WARN: BSDF input bulunamadi: {name}")
```
