---
last_updated: 2026-04-14
refined_by: agent-sharpen round 2
confidence: high
purpose: copy-paste ready goblin script template
sources: [goblin_anatomy.md, humanoid_modelling.md, blender_4x_api_changes.md, render_setup.md]
---

# Goblin Script Şablonu — Tam Kopyala-Yapıştır

Bu şablon Blender 4.x / 5.x uyumludur.
1m boyunda klasik goblin, metaball tabanlı, tam pipeline.
Her bölüm bağımsız çalıştırılabilir veya hepsi tek script olarak kullanılabilir.

---

## Tam Pipeline Script

```python
"""
Goblin Metaball Script — Blender 4.x / 5.x Uyumlu
Sonuc: 1m boyunda klasik goblin, material, kamera, render
Kullanim: Blender Script Editor yapistir, Run Script
"""

import bpy
import bmesh
import math
from mathutils import Vector

# ====================================================
# VERSIYON UYUMLULUK
# ====================================================
BL_VERSION = bpy.app.version
IS_42  = BL_VERSION >= (4, 2, 0)
IS_5X  = BL_VERSION >= (5, 0, 0)

# EEVEE: 5.x'te BLENDER_EEVEE_NEXT kaldirildi
EEVEE_ENGINE = 'BLENDER_EEVEE_NEXT' if (IS_42 and not IS_5X) else 'BLENDER_EEVEE'

BSDF_NAMES = {
    'subsurface':   'Subsurface Weight',
    'specular':     'Specular IOR Level',
    'transmission': 'Transmission Weight',
    'coat':         'Coat Weight',
    'emission':     'Emission Color',
}

def bsdf_set(bsdf, key, value):
    name = BSDF_NAMES.get(key, key)
    if name in bsdf.inputs:
        bsdf.inputs[name].default_value = value


# ====================================================
# 1. SCENE TEMIZLEME
# ====================================================

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in [bpy.data.meshes, bpy.data.materials,
                  bpy.data.cameras, bpy.data.lights, bpy.data.metaballs]:
        for item in list(block):
            block.remove(item)
    print("Scene temizlendi.")


# ====================================================
# 2. GOBLIN METABALL (1m boy standardi)
# ====================================================

GOBLIN_ELEMENTS = [
    # (isim, (x, y, z), radius, stiffness)
    # --- Govde ---
    ('torso_lower',  (0.00,  0.00, 0.30), 0.16, 1.0),
    ('torso_mid',    (0.00,  0.00, 0.42), 0.14, 1.0),
    ('torso_upper',  (0.00,  0.00, 0.52), 0.13, 1.0),
    ('chest',        (0.00, -0.02, 0.58), 0.12, 0.9),
    # --- Boyun ---
    ('neck',         (0.00,  0.00, 0.66), 0.05, 1.0),
    # --- Kafa ---
    ('head_main',    (0.00,  0.00, 0.80), 0.18, 1.0),
    ('forehead',     (0.00, -0.03, 0.88), 0.12, 0.8),
    ('jaw',          (0.00,  0.02, 0.70), 0.10, 0.9),
    ('snout',        (0.00, -0.10, 0.74), 0.06, 0.8),
    # --- Kulaklar ---
    ('ear_R',        ( 0.16,  0.00, 0.80), 0.05, 0.7),
    ('ear_R_tip',    ( 0.22,  0.00, 0.87), 0.02, 0.6),
    ('ear_L',        (-0.16,  0.00, 0.80), 0.05, 0.7),
    ('ear_L_tip',    (-0.22,  0.00, 0.87), 0.02, 0.6),
    # --- Omuzlar ---
    ('shoulder_R',   ( 0.14,  0.00, 0.58), 0.07, 1.0),
    ('shoulder_L',   (-0.14,  0.00, 0.58), 0.07, 1.0),
    # --- Kol Sag ---
    ('upper_arm_R',  ( 0.22,  0.00, 0.52), 0.05, 1.0),
    ('lower_arm_R',  ( 0.30,  0.00, 0.44), 0.04, 1.0),
    ('wrist_R',      ( 0.36,  0.00, 0.38), 0.03, 0.9),
    ('hand_R',       ( 0.40,  0.00, 0.34), 0.06, 0.8),
    # --- Kol Sol ---
    ('upper_arm_L',  (-0.22,  0.00, 0.52), 0.05, 1.0),
    ('lower_arm_L',  (-0.30,  0.00, 0.44), 0.04, 1.0),
    ('wrist_L',      (-0.36,  0.00, 0.38), 0.03, 0.9),
    ('hand_L',       (-0.40,  0.00, 0.34), 0.06, 0.8),
    # --- Kalca ---
    ('pelvis',       ( 0.00,  0.00, 0.22), 0.14, 1.0),
    ('hip_R',        ( 0.10,  0.00, 0.20), 0.08, 0.9),
    ('hip_L',        (-0.10,  0.00, 0.20), 0.08, 0.9),
    # --- Bacak Sag ---
    ('thigh_R',      ( 0.09,  0.00, 0.14), 0.07, 1.0),
    ('knee_R',       ( 0.09,  0.01, 0.07), 0.05, 0.9),
    ('shin_R',       ( 0.09,  0.00, 0.03), 0.04, 1.0),
    ('foot_R',       ( 0.09,  0.04, 0.01), 0.05, 0.8),
    # --- Bacak Sol ---
    ('thigh_L',      (-0.09,  0.00, 0.14), 0.07, 1.0),
    ('knee_L',       (-0.09,  0.01, 0.07), 0.05, 0.9),
    ('shin_L',       (-0.09,  0.00, 0.03), 0.04, 1.0),
    ('foot_L',       (-0.09,  0.04, 0.01), 0.05, 0.8),
]


def create_goblin_metaball():
    meta_data = bpy.data.metaballs.new("GoblinMeta")
    meta_obj  = bpy.data.objects.new("Goblin", meta_data)
    bpy.context.collection.objects.link(meta_obj)

    meta_data.resolution        = 0.04
    meta_data.render_resolution = 0.02
    meta_data.threshold         = 0.60

    name0, co0, r0, s0 = GOBLIN_ELEMENTS[0]
    meta_data.elements[0].co        = co0
    meta_data.elements[0].radius    = r0
    meta_data.elements[0].stiffness = s0

    for _, co, radius, stiffness in GOBLIN_ELEMENTS[1:]:
        elem           = meta_data.elements.new('BALL')
        elem.co        = co
        elem.radius    = radius
        elem.stiffness = stiffness

    bpy.context.view_layer.objects.active = meta_obj
    bpy.context.view_layer.update()
    print(f"Metaball olusturuldu: {len(meta_data.elements)} element")
    return meta_obj


# ====================================================
# 3. MESH'E CEVIRME
# ====================================================

def convert_to_mesh(meta_obj):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = meta_obj
    meta_obj.select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.update()
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)

    bpy.ops.object.convert(target='MESH')
    mesh_obj = bpy.context.active_object
    if mesh_obj.type != 'MESH':
        raise RuntimeError("Convert basarisiz")
    mesh_obj.name = "Goblin_Mesh"
    print(f"Mesh cevrildi: {len(mesh_obj.data.vertices)} vertex")
    return mesh_obj


# ====================================================
# 4. ZEMINE OTURTMA
# ====================================================

def place_on_ground(obj):
    verts = [obj.matrix_world @ Vector(v.co) for v in obj.data.vertices]
    if not verts:
        return
    min_z = min(v.z for v in verts)
    obj.location.z -= min_z
    bpy.context.view_layer.update()
    print(f"Zemine oturtuldu: offset={-min_z:.4f}")


# ====================================================
# 5. SUBDIVISION + SMOOTH
# ====================================================

def apply_subdivision(obj, viewport_level=1, render_level=2):
    # Voxel remesh (topoloji temizle)
    obj.data.remesh_voxel_size = 0.025
    bpy.ops.object.voxel_remesh()

    # SubSurf
    subsurf = obj.modifiers.new("SubSurf", 'SUBSURF')
    subsurf.subdivision_type = 'CATMULL_CLARK'
    subsurf.levels        = viewport_level
    subsurf.render_levels = render_level

    # Smooth shading
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30))
    except AttributeError:
        bpy.ops.object.shade_smooth()

    print(f"SubSurf: viewport={viewport_level}, render={render_level}")


# ====================================================
# 6. MATERIAL (4.x/5.x uyumlu)
# ====================================================

def apply_goblin_material(obj, color_variant='green'):
    colors = {
        'green': (0.15, 0.35, 0.12, 1.0),
        'grey':  (0.25, 0.28, 0.22, 1.0),
        'brown': (0.30, 0.22, 0.10, 1.0),
    }
    base_color = colors.get(color_variant, colors['green'])

    mat = bpy.data.materials.new("GoblinSkin")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value  = 0.75
    bsdf.inputs['Metallic'].default_value   = 0.0
    bsdf_set(bsdf, 'subsurface', 0.12)
    if 'Subsurface Radius' in bsdf.inputs:
        bsdf.inputs['Subsurface Radius'].default_value = (0.05, 0.10, 0.05)

    obj.data.materials.clear()
    obj.data.materials.append(mat)
    print(f"Material: GoblinSkin ({color_variant})")
    return mat


# ====================================================
# 7. KAMERA + ISIK (Portrait, Tum Vucut)
# ====================================================

def setup_camera_and_lights(char_obj):
    verts  = [char_obj.matrix_world @ Vector(v.co) for v in char_obj.data.vertices]
    min_z  = min(v.z for v in verts)
    max_z  = max(v.z for v in verts)
    height = max_z - min_z
    center = Vector((0, 0, (min_z + max_z) / 2))

    # Kamera
    cam_data = bpy.data.cameras.new("GoblinCam")
    cam_data.lens = 50

    fov_v    = 2 * math.atan(18 / cam_data.lens)  # 36mm sensor / 2
    cam_dist = (height * 1.25) / (2 * math.tan(fov_v / 2))
    cam_dist = max(cam_dist, 2.0)

    cam_obj = bpy.data.objects.new("GoblinCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = Vector((0, -cam_dist, center.z))

    track = cam_obj.constraints.new('TRACK_TO')
    track.target     = char_obj
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis    = 'UP_Y'

    bpy.context.scene.camera = cam_obj
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1920

    # 3-nokta isik
    e = height * 200
    for name, ltype, loc, energy, color, size in [
        ('Key',  'AREA', center + Vector((-height*1.5, -height*2.0, height*1.5)),  e*1.0, (1.0,0.97,0.90), height*1.5),
        ('Fill', 'AREA', center + Vector(( height*2.0, -height*1.0, height*0.3)),  e*0.35,(0.75,0.82,1.00), height*2.0),
        ('Rim',  'SPOT', center + Vector(( height*0.3,  height*2.5, height*1.2)),  e*0.65,(1.0, 1.0, 1.00), None),
    ]:
        ld = bpy.data.lights.new(name, ltype)
        ld.energy = energy
        ld.color  = color
        if ltype == 'AREA' and size:
            ld.size = size
        elif ltype == 'SPOT':
            ld.spot_size  = 0.6
            ld.spot_blend = 0.15
        lo = bpy.data.objects.new(name, ld)
        bpy.context.collection.objects.link(lo)
        lo.location = loc
        d = center - lo.location
        lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

    # Koyu world
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes.clear()
    bg  = world.node_tree.nodes.new('ShaderNodeBackground')
    out = world.node_tree.nodes.new('ShaderNodeOutputWorld')
    bg.inputs['Color'].default_value    = (0.04, 0.04, 0.04, 1.0)
    bg.inputs['Strength'].default_value = 0.2
    world.node_tree.links.new(bg.outputs['Background'], out.inputs['Surface'])

    print(f"Kamera + isik: dist={cam_dist:.2f}m, height={height:.2f}m")
    return cam_obj


# ====================================================
# 8. RENDER + KAYDET
# ====================================================

def render_and_save(output_path="/tmp/goblin_render.png"):
    scene = bpy.context.scene
    scene.render.engine = EEVEE_ENGINE

    eevee = scene.eevee
    eevee.taa_render_samples = 32
    try:
        eevee.use_gtao      = True
        eevee.gtao_distance = 0.2
    except AttributeError:
        pass

    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    print(f"Render kaydedildi: {output_path}")


# ====================================================
# MAIN
# ====================================================

def main(output_path="/tmp/goblin_render.png",
         skin_color='green',
         subsurf_viewport=1,
         subsurf_render=2):
    print("=== GOBLIN PIPELINE BASLADI ===")
    clear_scene()
    meta_obj = create_goblin_metaball()
    mesh_obj = convert_to_mesh(meta_obj)
    place_on_ground(mesh_obj)
    apply_subdivision(mesh_obj, subsurf_viewport, subsurf_render)
    apply_goblin_material(mesh_obj, skin_color)
    setup_camera_and_lights(mesh_obj)
    render_and_save(output_path)
    print(f"=== TAMAMLANDI: {output_path} ===")
    return mesh_obj


main(
    output_path="/tmp/goblin_render.png",
    skin_color='green',
    subsurf_viewport=1,
    subsurf_render=2,
)
```

---

## Parametre Tablosu

| Parametre | Default | Secenekler | Etki |
|-----------|---------|------------|------|
| `skin_color` | `'green'` | `'grey'`, `'brown'` | Skin rengi |
| `subsurf_viewport` | `1` | `0`, `2` | Viewport kalitesi |
| `subsurf_render` | `2` | `1`, `3` | Render kalitesi |
| `meta_data.resolution` | `0.04` | `0.02–0.06` | Metaball detayi (kucuk=detayli) |
| `meta_data.threshold` | `0.60` | `0.4–0.8` | Blend esligi |

---

## Goblin Boyut Ozellestirme

```python
# Daha buyuk kafa:
# ('head_main', (0.00, 0.00, 0.80), 0.18, 1.0)  =>  radius=0.22

# Daha uzun kulaklar:
# ('ear_R_tip', (0.22, 0.00, 0.87), 0.02, 0.6)  =>  co=(0.28, 0.00, 0.95)

# Daha kaslı gövde:
# ('torso_upper', ..., 0.13)  =>  radius=0.17

# Daha kısa bacaklar: thigh/knee/shin Z degerlerini kucult
# ('thigh_R', (0.09, 0.00, 0.14), ...)  =>  co=(0.09, 0.00, 0.10)
```

---

## Hizli Test (Minimal, Sadece Viewport)

```python
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

meta = bpy.data.metaballs.new("G")
obj  = bpy.data.objects.new("G", meta)
bpy.context.collection.objects.link(obj)
meta.resolution = 0.05
meta.threshold  = 0.6

elems = [
    ((0,0,0.50), 0.16),   # torso
    ((0,0,0.66), 0.05),   # boyun
    ((0,0,0.80), 0.18),   # kafa
    ((0.16,0,0.80), 0.05),# kulak R
    ((-0.16,0,0.80),0.05),# kulak L
    ((0.22,0,0.52), 0.05),# kol R
    ((-0.22,0,0.52),0.05),# kol L
    ((0.09,0,0.14), 0.07),# bacak R
    ((-0.09,0,0.14),0.07),# bacak L
]

meta.elements[0].co = elems[0][0]
meta.elements[0].radius = elems[0][1]
for co, r in elems[1:]:
    e = meta.elements.new('BALL')
    e.co = co
    e.radius = r

bpy.context.view_layer.objects.active = obj
print("Minimal goblin: viewport'ta gor")
```
