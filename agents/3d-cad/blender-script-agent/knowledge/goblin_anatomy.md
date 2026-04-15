---
last_updated: 2026-04-14
refined_by: agent-sharpen round 2
confidence: high
sources: [fantasy character design books, game art reference, CG character guides, World of Warcraft goblin proportions analysis]
---

# Goblin Anatomy — Fantasy Character Oranları

## Goblin Genel Tanımı

Goblin = küçük, kurnaz, fiziksel olarak zayıf ama hareketli humanoid fantasy yaratık.
Standart referans: D&D goblin, WoW goblin, Elder Scrolls goblin, Warhammer goblin.

---

## Head Count Sistemi

**Normal insan:** 7-8 head tall (standart anatomik oran)
**Goblin:** 4-5 head tall (çizgi film karakteri oranı)

```
Total height = 4.5 × head_height

Head height   = 1.0 unit  (büyük, yaklaşık %22 toplam boy)
Neck + torso  = 1.2 unit
Hip to knee   = 1.0 unit
Knee to foot  = 1.0 unit
Foot          = 0.3 unit (büyük, geniş)
```

---

## Goblin Oranları Tablosu

| Bölge | Normal İnsan (%) | Goblin (%) | Fark |
|-------|-----------------|-----------|------|
| Kafa | 13% boy | 22% boy | +9% |
| Kulak uzunluğu | kafa yüksekliği %30 | kafa yüksekliği %45 | sivri, uzun |
| Omuz genişliği | boy × 0.27 | boy × 0.20 | dar |
| Kalça genişliği | omuz × 0.85 | omuz × 0.65 | daha dar |
| Kol uzunluğu | boy × 0.40 | boy × 0.38 | biraz kısa |
| El boyutu | kafa × 0.75 | kafa × 0.95 | büyük el |
| Bacak uzunluğu | boy × 0.55 | boy × 0.44 | kısa bacak |
| Ayak uzunluğu | boy × 0.15 | boy × 0.14 | normal |

---

## Goblin Karakter Özellikleri (Blender Koordinatları)

Boy = 1.0m (1 Blender unit) varsayımı ile:

```python
# Goblin boyut sabitleri (1m goblin için)
GOBLIN = {
    # Kafa
    'head_height':   0.22,   # büyük kafa
    'head_width':    0.18,   # geniş alın
    'head_depth':    0.16,   # ön-arka derinlik
    'jaw_width':     0.14,   # çıkık alt çene
    'ear_length':    0.10,   # sivri kulak
    'ear_width':     0.04,
    'nose_length':   0.04,   # sivri burun
    'eye_size':      0.025,  # büyük göz
    'eye_spacing':   0.08,   # geniş göz aralığı

    # Boyun + Torso
    'neck_height':   0.06,
    'neck_radius':   0.04,   # ince boyun
    'torso_height':  0.25,   # kısa gövde
    'shoulder_w':    0.20,   # dar omuz
    'chest_depth':   0.12,
    'waist_w':       0.14,   # ince bel
    'hip_w':         0.16,

    # Kollar
    'upper_arm_len': 0.15,
    'lower_arm_len': 0.13,
    'hand_size':     0.08,   # büyük el (kafa × 0.95 / 2)
    'arm_radius':    0.025,  # ince kol

    # Bacaklar
    'thigh_len':     0.18,   # kısa uyluk
    'shin_len':      0.16,
    'foot_len':      0.12,
    'leg_radius':    0.035,  # orta bacak kalınlığı

    # Genel
    'total_height':  1.00,
    'head_ratio':    0.22,   # kafa/boy oranı
}
```

---

## Goblin Kafa Modelleme

### Karakteristik Özellikler

1. **Büyük alın** — kafa önden bakıldığında oval, tepe yuvarlak
2. **Çıkık alt çene** — prognathism, alt çene öne çıkıyor
3. **Büyük kulaklar** — sivri uç, elips şekli, yanlara açık
4. **Küçük ve sivri burun** — ya çok küçük ya da kanca biçimli
5. **Büyük gözler** — sarı veya kırmızı, geniş açık
6. **Büyük ağız** — boyun genişliğinde veya daha geniş, dişler çıkık

```python
def create_goblin_head(obj):
    """Mevcut objeye goblin kafası ekle (torso üstüne extrude)"""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    # Boyun üstündeki yüzleri bul
    neck_top_z = 0.78  # torso + boyun yüksekliği
    neck_faces = [f for f in bm.faces
                  if f.calc_center_median().z > neck_top_z - 0.02]

    # Kafa gövdesi: büyük yuvarlak kütle
    # 3 segment extrude, genişleyerek
    head_segs = [
        (Vector((0, 0, 0.04)), 1.4),   # boyun-kafa geçiş, genişle
        (Vector((0, 0, 0.10)), 1.1),   # kafa ortası
        (Vector((0, 0, 0.08)), 0.85),  # kafa tepesi, küçül
    ]

    current = neck_faces
    for direction, scale in head_segs:
        r = bmesh.ops.extrude_face_region(bm, geom=current)
        verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=direction, verts=verts)
        c = sum((v.co for v in verts), Vector()) / len(verts)
        for v in verts:
            v.co.x = c.x + (v.co.x - c.x) * scale
            v.co.y = c.y + (v.co.y - c.y) * scale
        bm.faces.ensure_lookup_table()
        current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    # Çene: alt kafa segmentleri öne çıkart
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        if v.co.z > neck_top_z and v.co.z < neck_top_z + 0.08:
            # Alt kafa — çene öne çıkart
            v.co.y += 0.02

    bm.normal_update()
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

## Goblin Kulak Modelleme

Kulak: kafa kenarından dışa extrude, sivri üç boyutlu kulak.

```python
def add_goblin_ears(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    for side in ['LEFT', 'RIGHT']:
        x_sign = -1 if side == 'LEFT' else 1
        # Kafa yan yüzlerini bul (orta yükseklik)
        ear_z = 0.85  # kafa ortası
        ear_faces = [f for f in bm.faces
                     if abs(f.calc_center_median().z - ear_z) < 0.04
                     and f.calc_center_median().x * x_sign > 0.07]

        if not ear_faces:
            continue

        # Kulak: 3 segment dışa, sivrilecek
        ear_dir = Vector((x_sign * 0.04, 0, 0.01))
        current = ear_faces[:2]  # küçük yüz seç
        for i, scale in enumerate([1.0, 0.7, 0.3]):
            r = bmesh.ops.extrude_face_region(bm, geom=current)
            verts = [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=ear_dir + Vector((0, 0, i * 0.02)), verts=verts)
            c = sum((v.co for v in verts), Vector()) / len(verts)
            for v in verts:
                v.co.y = c.y + (v.co.y - c.y) * scale
                v.co.z = c.z + (v.co.z - c.z) * (0.6 + i * 0.2)
            bm.faces.ensure_lookup_table()
            current = [f for f in bm.faces if all(v in verts for v in f.verts)]

    bm.normal_update()
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

## Goblin Renk Paleti (PBR)

```python
GOBLIN_COLORS = {
    'skin_green':   (0.15, 0.35, 0.12),  # klasik goblin yeşili
    'skin_grey':    (0.25, 0.28, 0.22),  # gri-yeşil varyant
    'skin_brown':   (0.30, 0.22, 0.10),  # kahverengi varyant
    'eye_yellow':   (0.85, 0.75, 0.05),
    'eye_red':      (0.80, 0.10, 0.05),
    'tooth_cream':  (0.90, 0.85, 0.70),
    'sclera':       (0.95, 0.92, 0.80),
}

def apply_goblin_skin(obj):
    mat = bpy.data.materials.new("GoblinSkin")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*GOBLIN_COLORS['skin_green'], 1.0)
    bsdf.inputs["Roughness"].default_value = 0.75
    bsdf.inputs["Subsurface Weight"].default_value = 0.15  # hafif SSS
    bsdf.inputs["Subsurface Radius"].default_value = (0.05, 0.10, 0.05)
    obj.data.materials.append(mat)
```

---

## Poly Count Hedefleri (Goblin Game-Ready)

| Seviye | Tris | Kullanım |
|--------|------|----------|
| LOD0 (yakın) | 3000-8000 | Ana karakter |
| LOD1 (orta) | 1500-3000 | NPC |
| LOD2 (uzak) | 500-1500 | Kalabalık |
| Mobile | 800-2000 | Mobil oyun |

---

## Goblin Silüet Kontrol Listesi

- [ ] Kafa vücudun %20-25'i kadar büyük (yandan ve önden)
- [ ] Kulaklar kafa yüksekliğinin %40'ı kadar uzun, sivri
- [ ] Omuzlar kalçadan dar
- [ ] Kollar bedene oranla doğru (kısa ama büyük el)
- [ ] Bacaklar kısa, diz hafif bükülü duruş
- [ ] Çene öne çıkık görünüyor
- [ ] Genel siluet "inverted pear" değil "big head, small body"

---

## Referans: Goblin Varyantları

| Tür | Kafa Oranı | Özellik |
|-----|-----------|---------|
| Klasik D&D Goblin | 4 head | Küçük, hızlı, korkak |
| WoW Goblin | 5 head | Büyük burun, teknoloji odaklı |
| Warhammer Night Goblin | 4.5 head | Çadır gibi giysi, çılgın göz |
| Tolkien Goblin/Orc | 6 head | Daha insan benzeri, kas |
| Chibi Goblin | 3 head | Sevimli oyun karakteri |

---

## Metaball Element Listesi — 1m Boy Standardı

Aşağıdaki tablo, 1m boyunda klasik goblin için tüm metaball elementlerinin
(x, y, z, radius) değerlerini verir. Koordinat sistemi: z=0 zemin, z=1.0 tepe.

```python
# Goblin Metaball Element Tablosu (1m boy, Blender units)
# (co_x, co_y, co_z, radius, stiffness)

GOBLIN_METABALL_ELEMENTS = [
    # --- Gövde (Torso) ---
    # x=0 orta, y=0 ön-arka merkez, z = yükseklik
    {'name': 'torso_lower',   'co': (0.00,  0.00,  0.30), 'radius': 0.16, 'stiffness': 1.0},
    {'name': 'torso_mid',     'co': (0.00,  0.00,  0.42), 'radius': 0.14, 'stiffness': 1.0},
    {'name': 'torso_upper',   'co': (0.00,  0.00,  0.52), 'radius': 0.13, 'stiffness': 1.0},
    {'name': 'chest',         'co': (0.00, -0.02,  0.58), 'radius': 0.12, 'stiffness': 0.9},

    # --- Boyun ---
    {'name': 'neck',          'co': (0.00,  0.00,  0.66), 'radius': 0.05, 'stiffness': 1.0},

    # --- Kafa ---
    {'name': 'head_main',     'co': (0.00,  0.00,  0.80), 'radius': 0.18, 'stiffness': 1.0},
    {'name': 'forehead',      'co': (0.00, -0.03,  0.88), 'radius': 0.12, 'stiffness': 0.8},
    {'name': 'jaw',           'co': (0.00,  0.02,  0.70), 'radius': 0.10, 'stiffness': 0.9},
    {'name': 'snout',         'co': (0.00, -0.10,  0.74), 'radius': 0.06, 'stiffness': 0.8},

    # --- Kulaklar (simetrik) ---
    {'name': 'ear_R',         'co': ( 0.16, 0.00,  0.80), 'radius': 0.05, 'stiffness': 0.7},
    {'name': 'ear_R_tip',     'co': ( 0.22, 0.00,  0.87), 'radius': 0.02, 'stiffness': 0.6},
    {'name': 'ear_L',         'co': (-0.16, 0.00,  0.80), 'radius': 0.05, 'stiffness': 0.7},
    {'name': 'ear_L_tip',     'co': (-0.22, 0.00,  0.87), 'radius': 0.02, 'stiffness': 0.6},

    # --- Omuzlar ---
    {'name': 'shoulder_R',    'co': ( 0.14, 0.00,  0.58), 'radius': 0.07, 'stiffness': 1.0},
    {'name': 'shoulder_L',    'co': (-0.14, 0.00,  0.58), 'radius': 0.07, 'stiffness': 1.0},

    # --- Kollar (Sağ) ---
    {'name': 'upper_arm_R',   'co': ( 0.22, 0.00,  0.52), 'radius': 0.05, 'stiffness': 1.0},
    {'name': 'lower_arm_R',   'co': ( 0.30, 0.00,  0.44), 'radius': 0.04, 'stiffness': 1.0},
    {'name': 'wrist_R',       'co': ( 0.36, 0.00,  0.38), 'radius': 0.03, 'stiffness': 0.9},
    {'name': 'hand_R',        'co': ( 0.40, 0.00,  0.34), 'radius': 0.06, 'stiffness': 0.8},

    # --- Kollar (Sol) ---
    {'name': 'upper_arm_L',   'co': (-0.22, 0.00,  0.52), 'radius': 0.05, 'stiffness': 1.0},
    {'name': 'lower_arm_L',   'co': (-0.30, 0.00,  0.44), 'radius': 0.04, 'stiffness': 1.0},
    {'name': 'wrist_L',       'co': (-0.36, 0.00,  0.38), 'radius': 0.03, 'stiffness': 0.9},
    {'name': 'hand_L',        'co': (-0.40, 0.00,  0.34), 'radius': 0.06, 'stiffness': 0.8},

    # --- Kalça / Pelvis ---
    {'name': 'pelvis',        'co': (0.00,  0.00,  0.22), 'radius': 0.14, 'stiffness': 1.0},
    {'name': 'hip_R',         'co': ( 0.10, 0.00,  0.20), 'radius': 0.08, 'stiffness': 0.9},
    {'name': 'hip_L',         'co': (-0.10, 0.00,  0.20), 'radius': 0.08, 'stiffness': 0.9},

    # --- Bacaklar (Sağ) ---
    {'name': 'thigh_R',       'co': ( 0.09, 0.00,  0.14), 'radius': 0.07, 'stiffness': 1.0},
    {'name': 'knee_R',        'co': ( 0.09, 0.01,  0.07), 'radius': 0.05, 'stiffness': 0.9},
    {'name': 'shin_R',        'co': ( 0.09, 0.00,  0.03), 'radius': 0.04, 'stiffness': 1.0},
    {'name': 'foot_R',        'co': ( 0.09, 0.04,  0.01), 'radius': 0.05, 'stiffness': 0.8},

    # --- Bacaklar (Sol) ---
    {'name': 'thigh_L',       'co': (-0.09, 0.00,  0.14), 'radius': 0.07, 'stiffness': 1.0},
    {'name': 'knee_L',        'co': (-0.09, 0.01,  0.07), 'radius': 0.05, 'stiffness': 0.9},
    {'name': 'shin_L',        'co': (-0.09, 0.00,  0.03), 'radius': 0.04, 'stiffness': 1.0},
    {'name': 'foot_L',        'co': (-0.09, 0.04,  0.01), 'radius': 0.05, 'stiffness': 0.8},
]

def build_goblin_metaball():
    """Goblin metaball oluşturma — tüm elementler"""
    # Metaball data oluştur
    meta_data = bpy.data.metaballs.new("GoblinMeta")
    meta_obj = bpy.data.objects.new("Goblin_Meta", meta_data)
    bpy.context.collection.objects.link(meta_obj)

    meta_data.resolution = 0.04       # render çözünürlük (küçük = daha iyi)
    meta_data.render_resolution = 0.02
    meta_data.threshold = 0.6         # blend eşiği

    # İlk element zaten var (index 0), değerini güncelle
    first = GOBLIN_METABALL_ELEMENTS[0]
    meta_data.elements[0].co = first['co']
    meta_data.elements[0].radius = first['radius']
    meta_data.elements[0].stiffness = first['stiffness']

    # Kalanları ekle
    for elem_def in GOBLIN_METABALL_ELEMENTS[1:]:
        elem = meta_data.elements.new('BALL')
        elem.co = elem_def['co']
        elem.radius = elem_def['radius']
        elem.stiffness = elem_def['stiffness']

    bpy.context.view_layer.objects.active = meta_obj
    return meta_obj
```

---

## Goblin Parmak Anatomisi

**Goblin parmak sayısı:** Klasik fantasy = 4 parmak (D&D, WoW), bazı versiyonlar 3 veya 5.
**Önerilen:** 4 parmak (index, middle, ring, pinky — başparmak dahil).

### Goblin El Boyutları (1m boy)

```
El uzunluğu:   ~0.10 (büyük el, kafa boyutunun ~0.45'i)
El genişliği:  ~0.07
Avuç:          ~0.05 uzunluk

Parmak segment uzunlukları (proximal → middle → distal):
  Başparmak:   0.025 + 0.020         (2 falange, kısa, geniş)
  İşaret:      0.025 + 0.018 + 0.014
  Orta:        0.028 + 0.020 + 0.015  (en uzun)
  Yüzük:       0.024 + 0.018 + 0.013
  
Parmak kalınlığı (radius):
  Proximal:    0.008-0.010
  Middle:      0.007-0.008
  Distal:      0.005-0.006
  
Parmak aralığı: 0.016 (parmaklar arası merkez-merkez)
```

```python
# Goblin parmak metaball elementleri (sağ el için, avuç merkezi = (0.40, 0, 0.34))
GOBLIN_FINGERS_R = [
    # Başparmak (thumb) — alta açılmış
    ('thumb_prox_R',  (0.42, -0.02, 0.30), 0.010),
    ('thumb_dist_R',  (0.44, -0.04, 0.28), 0.007),
    # İşaret (index)
    ('index_prox_R',  (0.45,  0.00, 0.30), 0.009),
    ('index_mid_R',   (0.47,  0.00, 0.27), 0.007),
    ('index_dist_R',  (0.49,  0.00, 0.25), 0.006),
    # Orta (middle)
    ('mid_prox_R',    (0.45,  0.016, 0.30), 0.009),
    ('mid_mid_R',     (0.47,  0.016, 0.27), 0.008),
    ('mid_dist_R',    (0.49,  0.016, 0.24), 0.006),
    # Yüzük (ring)
    ('ring_prox_R',   (0.45,  0.032, 0.30), 0.009),
    ('ring_mid_R',    (0.47,  0.032, 0.27), 0.007),
    ('ring_dist_R',   (0.49,  0.032, 0.25), 0.005),
]
```

---

## Goblin Diş / Fang Anatomisi

**Goblin dişleri:** Alt çeneden çıkan 2 adet sivri azı (fang), küçük ön dişler.

```
Fang sayısı:     2 (alt çene, simetrik)
Fang konumu:     Alt çene yan tarafları, z ≈ 0.69 (ağız alt hizası)
Fang X offset:   ±0.025 (orta hattan yana)
Fang boyutu:
  Uzunluk:       0.025-0.030
  Taban radius:  0.008
  Uç radius:     0.002

Ön dişler:       6 adet küçük (radius 0.004), alt çene ön kısmı
```

```python
GOBLIN_TEETH = [
    # Fanglar (alt çeneden yukarı çıkıyor)
    {'name': 'fang_R', 'base': ( 0.025, -0.06, 0.695), 'tip': ( 0.022, -0.06, 0.720), 'r_base': 0.008, 'r_tip': 0.002},
    {'name': 'fang_L', 'base': (-0.025, -0.06, 0.695), 'tip': (-0.022, -0.06, 0.720), 'r_base': 0.008, 'r_tip': 0.002},
    # Küçük ön dişler (alt)
    {'name': 'tooth_0', 'base': (0.000, -0.07, 0.693), 'tip': (0.000, -0.07, 0.705), 'r_base': 0.005, 'r_tip': 0.003},
    {'name': 'tooth_1', 'base': (0.012, -0.07, 0.693), 'tip': (0.012, -0.07, 0.704), 'r_base': 0.004, 'r_tip': 0.003},
    {'name': 'tooth_2', 'base': (-0.012, -0.07, 0.693), 'tip': (-0.012, -0.07, 0.704), 'r_base': 0.004, 'r_tip': 0.003},
]

def add_goblin_teeth_metaball(meta_data):
    """Dişleri metaball elipsoidi olarak ekle (basit versiyon)"""
    for t in GOBLIN_TEETH:
        elem = meta_data.elements.new('ELLIPSOID')
        # Elipsoid base konumu
        bx, by, bz = t['base']
        tx, ty, tz = t['tip']
        elem.co = ((bx+tx)/2, (by+ty)/2, (bz+tz)/2)
        elem.radius = t['r_base']
        elem.size_x = t['r_base']
        elem.size_y = t['r_base']
        elem.size_z = abs(tz - bz) / 2
        elem.stiffness = 0.6
```

---

## Goblin Silhouette Kuralları

Her açıdan görünmesi gereken ana şekiller:

```
ÖNDEN BAKIŞ (Y- ekseni):
  ┌──────────────────────┐
  │ Kural: büyük oval kafa, dar omuz, geniş el
  │
  │        ╭─────╮           ← kafa: toplam boyun %22'si
  │       ╔═══════╗          ← kulaklar: kenara çıkmış, sivri
  │       ║ Goblin║
  │       ╚══╤╤══╝          ← omuzlar: kafanın %55'i kadar geniş
  │          ││
  │        ╔═╪╪═╗           ← torso: kısa, hafif armut (üst→alt genişler)
  │       ╔╝ ╪╪ ╚╗
  │       ║  ╪╪  ║          ← kollar: omuzdan aşağı, büyük el
  │       ╚╗ ╪╪ ╔╝
  │        ╚═╪╪═╝
  │          ╪╪             ← bacaklar: kısa, diz hafif bükük
  │         ╔╪╪╗
  │         ╚══╝            ← ayaklar: hafif geniş
  └──────────────────────┘

YANDAN BAKIŞ (X+ ekseni):
  ┌──────────────────────┐
  │ Kural: çıkık çene, öne eğik duruş, büyük but
  │
  │      ╭──╮              ← kafa hafif öne eğik
  │    ──╯  │              ← çene: öne çıkık
  │      ╲──╯
  │       │ ╲              ← boyun: kısa, öne eğik
  │      ╔╝  ╲             ← sırt: hafif kambur (goblin duruşu)
  │      ║    │
  │      ╚╗   │
  │       ╚══╗│
  │          ╚╝            ← bacak: diz önde, hafif bükük
  └──────────────────────┘

ARKADAN BAKIŞ (Y+ ekseni):
  ┌──────────────────────┐
  │ Kulaklar görünür (kenara çıkmış)
  │ Sırt: kambur profile
  │ Kalça: dar, bacaklar simetrik
  └──────────────────────┘

YUKARI BAKIŞ (Z- ekseni):
  ┌──────────────────────┐
  │ Kafa en büyük element
  │ Omuzlar kafanın dışına çıkmaz
  │ El ve ayaklar görünür
  └──────────────────────┘
```

### Silhouette Kontrol Algoritması (Script)

```python
def check_goblin_silhouette(obj):
    """Goblin oranları kontrol et, hata varsa uyar"""
    mesh = obj.data
    verts = [v.co for v in mesh.vertices]

    total_height = max(v.z for v in verts) - min(v.z for v in verts)
    total_width  = max(v.x for v in verts) - min(v.x for v in verts)

    # Kafa bölgesi (üst %30)
    head_z_min = max(v.z for v in verts) - total_height * 0.30
    head_verts = [v for v in verts if v.z >= head_z_min]
    head_width = (max(v.x for v in head_verts) - min(v.x for v in head_verts)) if head_verts else 0

    head_ratio = head_width / total_width if total_width > 0 else 0

    issues = []
    if head_ratio < 0.55:
        issues.append(f"WARN: Kafa çok dar (oran={head_ratio:.2f}, beklenen > 0.55)")
    if total_height > 1.15 or total_height < 0.85:
        issues.append(f"WARN: Boy beklenenden farklı ({total_height:.2f}m, beklenen ~1.0m)")

    for issue in issues:
        print(issue)
    return len(issues) == 0
```
