---
last_updated: 2026-04-14
refined_by: agent-sharpen round 2
confidence: high
sources: [Blender Python API docs 4.x/5.x, bmesh module docs, community patterns]
---

# Blender Python API — Karakter Modelleme Kritik Operatörler

## bmesh.ops — Temel Karakter Operatörleri

### extrude_face_region

```python
import bmesh
from mathutils import Vector

bm = bmesh.new()
bm.from_mesh(obj.data)
bm.faces.ensure_lookup_table()

# Yüzleri seç
target_faces = [f for f in bm.faces if f.calc_center_median().z > 0.5]

# Extrude
result = bmesh.ops.extrude_face_region(bm, geom=target_faces)

# YENİ oluşan verts/edges/faces'i ayır
new_verts  = [e for e in result['geom'] if isinstance(e, bmesh.types.BMVert)]
new_edges  = [e for e in result['geom'] if isinstance(e, bmesh.types.BMEdge)]
new_faces  = [e for e in result['geom'] if isinstance(e, bmesh.types.BMFace)]

# Translate (mutlaka extrude'dan sonra)
bmesh.ops.translate(bm, vec=Vector((0, 0, 0.2)), verts=new_verts)

bm.to_mesh(obj.data)
bm.free()
obj.data.update()
```

**Kritik:** `extrude_face_region` sonucu `result['geom']` karışık tip içerir — isinstance ile filtrele.

---

### subdivide_edges

```python
# Edge subdivision — genel kullanım
bmesh.ops.subdivide_edges(
    bm,
    edges=bm.edges[:],   # tüm edge'ler
    cuts=2,              # her edge'e 2 kesim
    use_grid_fill=True,  # iç yüzleri doldur
    smooth=0.0           # düzleştirme yok (0.0) veya var (1.0)
)

# Seçici subdivision (sadece belirli bölge)
joint_edges = [e for e in bm.edges
               if abs(e.verts[0].co.z - joint_z) < 0.03
               and abs(e.verts[1].co.z - joint_z) < 0.03]
bmesh.ops.subdivide_edges(bm, edges=joint_edges, cuts=1)
```

---

### smooth_vert

```python
# Vertex smoothing — organik yüzey için
bmesh.ops.smooth_vert(
    bm,
    verts=bm.verts[:],
    factor=0.5,      # 0.0-1.0, ne kadar yumuşatılacak
    mirror_clip_x=False,
    mirror_clip_y=False,
    mirror_clip_z=False,
    clip_dist=0.001,
    use_axis_x=True,
    use_axis_y=True,
    use_axis_z=True
)
```

**Kullanım:** Base form oluşturduktan sonra bir kez çalıştır, organik görünüm için.

---

### create_* primitives

```python
# İnsan başı için ico sphere (quad olmasa da iyi base)
bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.12)

# Kutu (torso, gövde için)
bmesh.ops.create_cube(bm, size=1.0)

# Silindir (boyun, kol, bacak için)
bmesh.ops.create_cone(
    bm,
    cap_ends=True,
    cap_tris=False,
    segments=8,
    radius1=0.04,   # alt radius
    radius2=0.03,   # üst radius (koni efekti)
    depth=0.2
)
```

---

### recalc_face_normals

```python
# Normal yönleri düzelt — her major edit sonrası çalıştır
bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
```

---

### dissolve_faces / dissolve_edges

```python
# NGon'ları temizle: gereksiz loop'u kaldır
bm.edges.ensure_lookup_table()
edges_to_dissolve = [e for e in bm.edges if len(e.link_faces) == 2
                     and e.calc_face_angle() < 0.05]  # düz açı
bmesh.ops.dissolve_edges(bm, edges=edges_to_dissolve, use_verts=True)
```

---

## Metaball → Mesh Convert Workflow

Metaball: hızlı base form, sonra mesh'e convert edilir.

```python
# 1. Metaball oluştur
bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 0.9))
meta = bpy.context.active_object
meta.data.resolution = 0.05  # detay (küçük = detaylı ama yavaş)
meta.data.threshold = 0.6

# Elemanlar ekle (gövde şekli)
elem = meta.data.elements[0]
elem.size_x = 0.25  # torso genişliği
elem.size_y = 0.15
elem.size_z = 0.40

# Kafa elementi
new_elem = meta.data.elements.new('BALL')
new_elem.co = (0, 0, 0.60)
new_elem.radius = 0.22

# 2. Mesh'e convert
bpy.ops.object.convert(target='MESH')
mesh_obj = bpy.context.active_object

# 3. Voxel remesh ile temizle
mesh_obj.data.remesh_voxel_size = 0.03  # çözünürlük
mesh_obj.data.remesh_voxel_adaptivity = 0.0
bpy.ops.object.voxel_remesh()
```

---

## Voxel Remesh — Karakter Ayarları

```python
def voxel_remesh_character(obj, quality='medium'):
    """Karakter için voxel remesh uygula"""
    settings = {
        'low':    {'voxel_size': 0.05, 'adaptivity': 0.1},
        'medium': {'voxel_size': 0.025, 'adaptivity': 0.05},
        'high':   {'voxel_size': 0.01, 'adaptivity': 0.0},
    }
    s = settings[quality]

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    obj.data.remesh_voxel_size = s['voxel_size']
    obj.data.remesh_voxel_adaptivity = s['adaptivity']
    bpy.ops.object.voxel_remesh()
    # Remesh sonrası normals
    bpy.ops.object.shade_smooth()
```

**Dikkat:** Voxel remesh tüm topolojiyi siler → rigging sonrası kullanma.

---

## Modifier Stack Sırası (Karakter)

**YANLIŞ sıra → bozuk deformasyon.**

```
DOĞRU SIRALAMA:
1. Armature modifier     ← rigging (varsa)
2. Corrective Smooth     ← deformasyon düzeltme
3. Mirror modifier       ← simetri (edit fazında aktif)
4. Subdivision Surface   ← son olarak, render kalitesi
5. (Decimate)            ← export için poly azaltma

YASAK:
- Subdivision → Armature (armature sonra gelmeli)
- Remesh → Subdivision (gereksiz)
```

```python
def setup_character_modifiers(obj, has_rig=False):
    # Mirror (edit fazı simetri için)
    if not has_rig:
        mirror = obj.modifiers.new("Mirror", 'MIRROR')
        mirror.use_axis = (True, False, False)
        mirror.use_clip = True

    # SubSurf (son)
    subsurf = obj.modifiers.new("SubSurf", 'SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3

    bpy.ops.object.shade_smooth()
```

---

## Armature Oluşturma (Temel Karakter Rig)

```python
def create_basic_humanoid_rig(char_obj):
    """Basit humanoid rig — T-pose için"""
    bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Humanoid_Rig"
    arm = arm_obj.data

    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()  # default kemik sil

    # Kemik oluşturma yardımcısı
    def add_bone(name, head, tail, parent_name=None):
        bone = arm.edit_bones.new(name)
        bone.head = head
        bone.tail = tail
        if parent_name and parent_name in arm.edit_bones:
            bone.parent = arm.edit_bones[parent_name]
            bone.use_connect = True
        return bone

    # Omurga
    add_bone("spine_root",   (0, 0, 0.40), (0, 0, 0.60))
    add_bone("spine_mid",    (0, 0, 0.60), (0, 0, 0.75), "spine_root")
    add_bone("spine_chest",  (0, 0, 0.75), (0, 0, 0.88), "spine_mid")
    add_bone("neck",         (0, 0, 0.88), (0, 0, 0.96), "spine_chest")
    add_bone("head",         (0, 0, 0.96), (0, 0, 1.10), "neck")

    # Sağ kol (T-pose)
    add_bone("shoulder_R",   (0, 0, 0.88), (0.12, 0, 0.87), "spine_chest")
    add_bone("upper_arm_R",  (0.12, 0, 0.87), (0.30, 0, 0.86), "shoulder_R")
    add_bone("lower_arm_R",  (0.30, 0, 0.86), (0.46, 0, 0.85), "upper_arm_R")
    add_bone("hand_R",       (0.46, 0, 0.85), (0.54, 0, 0.84), "lower_arm_R")

    # Sol kol (mirror)
    add_bone("shoulder_L",   (0, 0, 0.88),   (-0.12, 0, 0.87), "spine_chest")
    add_bone("upper_arm_L",  (-0.12, 0, 0.87), (-0.30, 0, 0.86), "shoulder_L")
    add_bone("lower_arm_L",  (-0.30, 0, 0.86), (-0.46, 0, 0.85), "upper_arm_L")
    add_bone("hand_L",       (-0.46, 0, 0.85), (-0.54, 0, 0.84), "lower_arm_L")

    # Sağ bacak
    add_bone("thigh_R",    (0.08, 0, 0.40), (0.10, 0, 0.20), "spine_root")
    add_bone("shin_R",     (0.10, 0, 0.20), (0.10, 0, 0.04), "thigh_R")
    add_bone("foot_R",     (0.10, 0, 0.04), (0.10, 0.10, 0.00), "shin_R")

    # Sol bacak
    add_bone("thigh_L",    (-0.08, 0, 0.40), (-0.10, 0, 0.20), "spine_root")
    add_bone("shin_L",     (-0.10, 0, 0.20), (-0.10, 0, 0.04), "thigh_L")
    add_bone("foot_L",     (-0.10, 0, 0.04), (-0.10, 0.10, 0.00), "shin_L")

    bpy.ops.object.mode_set(mode='OBJECT')

    # Mesh'i armature'a bağla
    char_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')  # auto weight paint

    return arm_obj
```

---

## Non-Manifold Tespiti

```python
def find_non_manifold(obj):
    """Non-manifold edge/vertex bul — export öncesi çalıştır"""
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
    non_manifold_verts = [v for v in bm.verts if not v.is_manifold]

    print(f"Non-manifold edges: {len(non_manifold_edges)}")
    print(f"Non-manifold verts: {len(non_manifold_verts)}")

    bm.free()
    return len(non_manifold_edges) == 0  # True = clean mesh

def fix_non_manifold(obj):
    """Otomatik non-manifold fix denemesi"""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.mesh.fill_holes(sides=4)
    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Context Override (Blender 3.2+)

```python
# Blender 3.2+'da operator context override şart
with bpy.context.temp_override(active_object=obj, selected_objects=[obj]):
    bpy.ops.object.shade_smooth()

# Edit mode operatör
bpy.ops.object.mode_set(mode='EDIT')
with bpy.context.temp_override(active_object=obj):
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()
bpy.ops.object.mode_set(mode='OBJECT')
```

---

## Hızlı Referans Tablosu

| İşlem | Fonksiyon |
|-------|-----------|
| Face extrude | `bmesh.ops.extrude_face_region(bm, geom=faces)` |
| Edge subdivide | `bmesh.ops.subdivide_edges(bm, edges=edges, cuts=N)` |
| Vert smooth | `bmesh.ops.smooth_vert(bm, verts=verts, factor=0.5)` |
| Normal recalc | `bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])` |
| Translate | `bmesh.ops.translate(bm, vec=Vector(...), verts=verts)` |
| Voxel remesh | `bpy.ops.object.voxel_remesh()` |
| Shade smooth | `bpy.ops.object.shade_smooth()` |
| Non-manifold | `e.is_manifold` (BMEdge property) |
