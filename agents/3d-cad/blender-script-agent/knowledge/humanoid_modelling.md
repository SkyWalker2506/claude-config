---
last_updated: 2026-04-14
refined_by: agent-sharpen round 2
confidence: high
sources: [Blender Manual 5.1, CG community best practices, game dev topology guides]
---

# Humanoid Character Modelling — Blender Workflow

## Yöntem Karşılaştırması

| Yöntem | Avantaj | Dezavantaj | Ne zaman kullan |
|--------|---------|------------|-----------------|
| Box modelling (bmesh) | Script dostu, kontrollü topoloji | Detay zaman alır | Game-ready, LLM script |
| Sculpting | Organik detay kolay | Retopo gerekir, script zor | Yüksek detay hero asset |
| Metaball → mesh | Hızlı base form | Topoloji düzensiz | Prototip, blob base |
| Voxel remesh | Uniform mesh | Detay kaybı | Cleanup sonrası sculpt |

**LLM script için: Box modelling (bmesh extrude chain)**

---

## T-Pose Base Mesh — Standart Workflow

T-Pose zorunludur: rigging için doğal bind pose, symmetric weight paint, clean edge flow.

### Aşama 1: Torso (ana kütle)

```python
import bpy, bmesh
from mathutils import Vector

def create_humanoid_base():
    mesh = bpy.data.meshes.new("Humanoid")
    obj = bpy.data.objects.new("Humanoid", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    bm = bmesh.new()

    # Torso — temel küp, orantılandır
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 0.25   # torso genişliği (0.5m)
        v.co.y *= 0.15   # torso derinliği (0.3m)
        v.co.z *= 0.40   # torso yüksekliği (0.8m)
        v.co.z += 0.40   # yerden kaldır (bel = z=0.8)

    # Subdivide — omuz/bel loop ekle
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2)

    # Omuz bölgesi genişlet (üst 1/3)
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        if v.co.z > 0.95:  # üst segment
            v.co.x *= 1.25  # omuz genişletme

    # Bel incelt (orta segment)
    for v in bm.verts:
        if 0.65 < v.co.z < 0.80:
            v.co.x *= 0.85

    bm.to_mesh(mesh)
    bm.free()
    return obj
```

### Aşama 2: Kol Extrude (T-Pose = yatay)

```python
def extrude_arms(obj, side='RIGHT'):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    x_sign = 1 if side == 'RIGHT' else -1

    # Omuz yüzlerini seç: X+ (sağ) veya X- (sol), üst bölge
    shoulder_faces = [f for f in bm.faces
                      if f.calc_center_median().x * x_sign > 0.18
                      and f.calc_center_median().z > 0.85]

    # Üst kol: 3 segment, T-pose yatay (X ekseni)
    # Omuz → dirsek
    upper_arm_dir = Vector((x_sign * 0.18, 0, -0.02))
    current = shoulder_faces
    for i in range(3):
        r = bmesh.ops.extrude_face_region(bm, geom=current)
        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=upper_arm_dir, verts=verts)
        taper = 0.90 - i * 0.03
        c = sum((v.co for v in verts), Vector()) / len(verts)
        for v in verts:
            v.co.y = c.y + (v.co.y - c.y) * taper
            v.co.z = c.z + (v.co.z - c.z) * taper
        bm.faces.ensure_lookup_table()
        current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    # Alt kol: dirsek → bilek, aşağı hafif
    lower_arm_dir = Vector((x_sign * 0.16, 0, -0.01))
    for i in range(3):
        r = bmesh.ops.extrude_face_region(bm, geom=current)
        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=lower_arm_dir, verts=verts)
        taper = 0.85 - i * 0.03
        c = sum((v.co for v in verts), Vector()) / len(verts)
        for v in verts:
            v.co.y = c.y + (v.co.y - c.y) * taper
            v.co.z = c.z + (v.co.z - c.z) * taper
        bm.faces.ensure_lookup_table()
        current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    bm.normal_update()
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

### Aşama 3: Bacak Extrude

```python
def extrude_legs(obj, side='RIGHT'):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    x_sign = 1 if side == 'RIGHT' else -1

    # Kalça yüzleri: alt torso, X tarafı
    hip_faces = [f for f in bm.faces
                 if f.calc_center_median().z < 0.45
                 and f.calc_center_median().x * x_sign > 0.05]

    # Uyluk: 4 segment aşağı
    thigh_dir = Vector((x_sign * 0.02, 0, -0.22))
    current = hip_faces
    for i in range(4):
        r = bmesh.ops.extrude_face_region(bm, geom=current)
        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=thigh_dir, verts=verts)
        taper = 0.92 - i * 0.02
        c = sum((v.co for v in verts), Vector()) / len(verts)
        for v in verts:
            v.co.x = c.x + (v.co.x - c.x) * taper
            v.co.y = c.y + (v.co.y - c.y) * taper
        bm.faces.ensure_lookup_table()
        current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    # Baldır: 3 segment, incelerek
    shin_dir = Vector((0, 0, -0.20))
    for i in range(3):
        r = bmesh.ops.extrude_face_region(bm, geom=current)
        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=shin_dir, verts=verts)
        taper = 0.80 - i * 0.05
        c = sum((v.co for v in verts), Vector()) / len(verts)
        for v in verts:
            v.co.x = c.x + (v.co.x - c.x) * taper
            v.co.y = c.y + (v.co.y - c.y) * taper
        bm.faces.ensure_lookup_table()
        current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    bm.normal_update()
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

## Edge Flow Kuralları — Eklem Bölgeleri

**KURAL: Her eklem etrafında minimum 2 edge loop.**

| Eklem | Loop Sayısı | Neden |
|-------|-------------|-------|
| Omuz | 3 loop | 360° rotasyon, yüksek deformasyon |
| Dirsek | 2 loop | Flex/extend |
| Bilek | 2 loop | Twist + flex |
| Kalça | 3 loop | Yüksek deformasyon, ileriye doğru |
| Diz | 2 loop | Sadece flex |
| Ayak bileği | 2 loop | Flex + side bend |

```python
# Eklem bölgesini subdivide et
def add_joint_loops(obj, joint_z, count=2):
    """joint_z: eklemin Z koordinatı (yaklaşık)"""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    # Eklem etrafındaki horizontal edge'leri bul
    joint_edges = [e for e in bm.edges
                   if abs(e.verts[0].co.z - joint_z) < 0.05
                   and abs(e.verts[1].co.z - joint_z) < 0.05]

    if joint_edges:
        bmesh.ops.subdivide_edges(bm, edges=joint_edges, cuts=count)

    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

## Quad Topology Zorunluluğu

- **Quad (4 kenar yüz) = standart**. Triangles OK sadece kapama yüzeylerinde (koltuk altı, ağız köşesi).
- N-gon (5+) = YASAK rigged mesh'te. Subsurf deformasyonu bozar.
- Pole (5+ edge buluşması) = kabul edilebilir ama eklem bölgelerinden uzak tut.

```python
# Quad ratio kontrolü
def check_quad_ratio(obj):
    mesh = obj.data
    total = len(mesh.polygons)
    quads = sum(1 for p in mesh.polygons if len(p.vertices) == 4)
    tris = sum(1 for p in mesh.polygons if len(p.vertices) == 3)
    ngons = total - quads - tris
    print(f"Quad: {quads/total*100:.1f}% | Tri: {tris/total*100:.1f}% | NGon: {ngons}")
    return quads / total  # hedef: > 0.85
```

---

## Normal İnsan Oranları (7.5 head tall)

| Bölge | Head Units | Metre (1.8m boy) |
|-------|-----------|-----------------|
| Toplam boy | 7.5 | 1.80 |
| Kafa yüksekliği | 1.0 | 0.24 |
| Boyun | 0.5 | 0.12 |
| Omuzdan bele | 2.0 | 0.48 |
| Belden kalçaya | 1.0 | 0.24 |
| Uyluk | 2.0 | 0.48 |
| Baldır + ayak | 2.0 | 0.48 |
| Omuz genişliği | 2.0 | 0.48 |
| Kol uzunluğu | 3.0 | 0.72 |

---

## Modifier Stack (Karakter İçin)

```python
def apply_character_modifiers(obj):
    # Mirror (simetri) — önce
    mirror = obj.modifiers.new("Mirror", 'MIRROR')
    mirror.use_axis = (True, False, False)  # X ekseni
    mirror.use_clip = True  # orta çizgi birleştir

    # Subdivision Surface — son
    subsurf = obj.modifiers.new("SubSurf", 'SUBSURF')
    subsurf.levels = 2          # viewport
    subsurf.render_levels = 3   # render

    # Shade smooth
    bpy.ops.object.shade_smooth()
```

**Önemli:** Mirror modifier'ı mesh editing boyunca aktif tut. Subsurf sadece finalize aşamasında uygula.

---

## Vertex Count Hedefleri (Game-Ready)

| Kalite Seviyesi | Vertices | Triangles | Kullanım |
|-----------------|----------|-----------|----------|
| Low (mobile) | 500-1500 | 1000-3000 | Mobil, kalabalık NPC |
| Medium (game) | 1500-5000 | 3000-10000 | Standard game character |
| High (cinematic) | 5000-20000 | 10000-40000 | Hero, cutscene |

---

## Common Pitfalls

| Hata | Belirtisi | Fix |
|------|-----------|-----|
| Simetrik değil | Bir kol diğerinden farklı | Mirror modifier kullan veya X=0'da başla |
| Eklemlerde ngon | Deform bozuk | Eklem bölgelerinde loop cut ekle |
| Ayrı parçalar | Mesh bağlantısız | Extrude chain kullan, ayrı primitif ekleme |
| T-pose değil | Kol aşağı | Extrude yönünü yatay (X eksenine) ayarla |
| Ölçek yanlış | Modifier'lar bozuk | Object mode'da Ctrl+A > Apply Scale |

---

## Metaball → Mesh Workflow (Blender 4.x, Doğrulanmış)

Adım adım metaball'dan temiz mesh üretme:

```python
import bpy
from mathutils import Vector

def metaball_to_mesh_workflow(meta_obj):
    """
    Metaball objesini mesh'e çevir — Blender 4.x doğrulanmış.
    Dikkat: meta_obj aktif ve seçili olmalı, başka obje seçili olmamalı.
    """
    scene = bpy.context.scene

    # 1. Sadece meta_obj'yi seç
    bpy.ops.object.select_all(action='DESELECT')
    meta_obj.select_set(True)
    bpy.context.view_layer.objects.active = meta_obj

    # 2. Object mode garantile (metaball edit mode yoktur ama garanti için)
    bpy.ops.object.mode_set(mode='OBJECT')

    # 3. CRITICAL: Viewport update — metaball mesh'i hesaplanmalı
    bpy.context.view_layer.update()
    scene.frame_set(scene.frame_current)  # force depsgraph update

    # 4. Mesh'e convert
    bpy.ops.object.convert(target='MESH')
    mesh_obj = bpy.context.active_object

    if mesh_obj.type != 'MESH':
        raise RuntimeError("Convert başarısız — obje hâlâ MESH değil")

    print(f"Convert başarılı: {len(mesh_obj.data.vertices)} vertex")
    return mesh_obj


def metaball_to_clean_mesh(meta_obj, voxel_size=0.025):
    """
    Metaball → convert → voxel remesh → smooth shading
    Tam pipeline — kopyala-yapıştır hazır.
    """
    # Convert
    mesh_obj = metaball_to_mesh_workflow(meta_obj)

    # Voxel remesh (topolojiyi temizle)
    mesh_obj.data.remesh_voxel_size = voxel_size
    mesh_obj.data.remesh_voxel_adaptivity = 0.0
    bpy.ops.object.voxel_remesh()

    # Smooth shading (Blender 4.x uyumlu)
    bpy.context.view_layer.objects.active = mesh_obj
    mesh_obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=0.523599)  # 30 derece
    except AttributeError:
        bpy.ops.object.shade_smooth()

    print(f"Clean mesh hazır: {len(mesh_obj.data.vertices)} vertex, voxel={voxel_size}")
    return mesh_obj
```

**Context Gereksinimleri (bpy.ops.object.convert):**
- Active object = metaball objesi olmalı
- Object mode olmalı
- Başka obje seçili olmamalı
- Depsgraph güncel olmalı (view_layer.update() çağrıldı)

**Yaygın Hata:** `RuntimeError: Operator bpy.ops.object.convert.poll() failed`
- Neden: meta_obj aktif değil veya wrong mode
- Fix: `bpy.context.view_layer.objects.active = meta_obj` + `select_set(True)`

---

## Voxel Remesh Sonrası İnce Geometri Kurtarma

Voxel remesh, ince çıkıntıları (parmaklar, kulaklar, fanglar) siler.
Çözüm stratejileri:

### Strateji 1: Remesh'ten Önce Büyüt

```python
def protect_thin_features(meta_obj, thin_element_names, scale_factor=1.5):
    """
    Remesh öncesi ince elementlerin radius'unu büyüt,
    remesh sonrası ayrı obje olarak ekle.
    """
    meta_data = meta_obj.data
    for elem in meta_data.elements:
        # İnce feature ise geçici büyüt
        if elem.radius < 0.015:  # threshold: çok ince
            elem.radius *= scale_factor
    bpy.context.view_layer.update()
```

### Strateji 2: Küçük Voxel Size

```python
# Parmaklar için: voxel_size = 0.010 (yavaş ama detay korur)
# Kulaklar için:  voxel_size = 0.012
# Genel gövde:    voxel_size = 0.025

def adaptive_remesh(mesh_obj, detail_level='fingers'):
    sizes = {
        'fingers':  0.010,  # yavaş, parmakları korur
        'ears':     0.012,
        'standard': 0.025,  # hızlı, genel karakter
        'fast':     0.040,  # hız öncelikli, detay kaybolur
    }
    mesh_obj.data.remesh_voxel_size = sizes[detail_level]
    bpy.ops.object.voxel_remesh()
```

### Strateji 3: Parmakları Sonradan Ekle (Önerilen)

```python
def add_fingers_post_remesh(hand_obj, side='R'):
    """
    Remesh sonrası el bölgesine parmak extrude et.
    El yüzlerini bul → her parmak için extrude chain.
    """
    bm = bmesh.new()
    bm.from_mesh(hand_obj.data)
    bm.faces.ensure_lookup_table()

    x_sign = 1 if side == 'R' else -1
    # El yüzlerini bul (X uç, alçak Z)
    hand_x = max(v.co.x * x_sign for v in bm.verts)
    hand_faces = [f for f in bm.faces
                  if f.calc_center_median().x * x_sign > hand_x - 0.04
                  and f.calc_center_median().z < 0.40]

    if len(hand_faces) < 4:
        print(f"WARN: El yüzü bulunamadı ({len(hand_faces)}), threshold genişlet")
        bm.free()
        return

    # 4 parmak için yüzleri böl
    sorted_faces = sorted(hand_faces, key=lambda f: f.calc_center_median().y)
    chunk = max(1, len(sorted_faces) // 4)

    for finger_idx in range(4):
        start = finger_idx * chunk
        end = start + chunk
        finger_faces = sorted_faces[start:end]
        if not finger_faces:
            continue

        # 3 segment parmak extrude
        current = finger_faces
        finger_dir = Vector((x_sign * 0.025, 0, 0))
        for seg in range(3):
            r = bmesh.ops.extrude_face_region(bm, geom=current)
            verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=finger_dir, verts=verts)
            scale = 0.85 - seg * 0.05
            c = sum((v.co for v in verts), Vector()) / len(verts)
            for v in verts:
                v.co.y = c.y + (v.co.y - c.y) * scale
                v.co.z = c.z + (v.co.z - c.z) * scale
            bm.faces.ensure_lookup_table()
            current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    bm.normal_update()
    bm.to_mesh(hand_obj.data)
    bm.free()
    hand_obj.data.update()
```

---

## Subdivision Level Önerileri

| Kullanım | Viewport Level | Render Level | Açıklama |
|---------|----------------|-------------|---------|
| Mobile game | 1 | 1 | Poly budget kısıtlı |
| Standard game | 1 | 2 | PC/console NPC |
| Hero character (game) | 2 | 2 | Ana karakter, yakın |
| Pre-rendered cinematic | 2 | 3 | Film kalitesi |
| VFX / film hero | 3 | 4 | Maksimum detay |

```python
def set_subdivision_for_use(obj, use_case='game_standard'):
    configs = {
        'mobile':          {'levels': 1, 'render_levels': 1},
        'game_npc':        {'levels': 1, 'render_levels': 2},
        'game_hero':       {'levels': 2, 'render_levels': 2},
        'cinematic':       {'levels': 2, 'render_levels': 3},
        'vfx':             {'levels': 3, 'render_levels': 4},
    }
    cfg = configs.get(use_case, configs['game_npc'])

    # Mevcut subsurf var mı?
    subsurf = next((m for m in obj.modifiers if m.type == 'SUBSURF'), None)
    if not subsurf:
        subsurf = obj.modifiers.new("SubSurf", 'SUBSURF')

    subsurf.levels = cfg['levels']
    subsurf.render_levels = cfg['render_levels']
    subsurf.subdivision_type = 'CATMULL_CLARK'

    print(f"SubSurf: viewport={cfg['levels']}, render={cfg['render_levels']}")
    return subsurf
```

**Kural:** Base mesh subdivision olmadan iyi görünmeli.
Subdivision "polishing" içindir, form düzeltme için değil.
