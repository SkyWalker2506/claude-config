---
last_updated: 2026-04-14
refined_by: agent-sharpen round 2
confidence: high
sources: [Blender Manual 5.1 EEVEE/Cycles docs, 3-point lighting theory, game art presentation guides]
---

# Render Setup — Karakter Showcase

## EEVEE vs Cycles — Karakter İçin Seçim

| Kriter | EEVEE (Next) | Cycles |
|--------|-------------|--------|
| Hız | Çok hızlı (realtime) | Yavaş (sample-based) |
| Subsurface Scattering | Basit, yaklaşık | Fiziksel, doğru |
| Saçlar | Orta | İyi |
| Refleksiyonlar | Screen-space | Gerçek |
| Script automation | Kolay | Kolay |
| Game preview | İdeal | Gereğinden iyi |

**Karakter showcase için:** EEVEE yeterli + hızlı. Cinematic için Cycles.

---

## 3-Point Lighting Setup (Script)

Endüstri standardı 3-nokta ışık düzeni:

```python
import bpy
from mathutils import Vector
import math

def setup_3point_lighting(target_location=(0, 0, 0.9), scene_scale=1.0):
    """
    3-point lighting setup — karakter için.
    target_location: karakterin merkezi (genellikle göbek veya göğüs yüksekliği)
    scene_scale: ışık gücünü ölçekle (büyük sahneler için artır)
    """

    # Mevcut ışıkları temizle
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    target = Vector(target_location)

    lights = [
        {
            'name': 'Key_Light',
            'type': 'AREA',
            'location': target + Vector((-1.5, -2.0, 1.5)),
            'energy': 200 * scene_scale,
            'color': (1.0, 0.95, 0.85),  # hafif sıcak
            'size': 1.5,
        },
        {
            'name': 'Fill_Light',
            'type': 'AREA',
            'location': target + Vector((2.0, -1.5, 0.8)),
            'energy': 80 * scene_scale,
            'color': (0.7, 0.8, 1.0),   # hafif soğuk (gökyüzü rengi)
            'size': 2.0,
        },
        {
            'name': 'Rim_Light',
            'type': 'AREA',
            'location': target + Vector((0.5, 2.5, 1.0)),
            'energy': 120 * scene_scale,
            'color': (1.0, 1.0, 1.0),   # beyaz
            'size': 0.8,
        },
    ]

    light_objects = []
    for ld in lights:
        light_data = bpy.data.lights.new(ld['name'], ld['type'])
        light_data.energy = ld['energy']
        light_data.color = ld['color']
        if ld['type'] == 'AREA':
            light_data.size = ld['size']

        light_obj = bpy.data.objects.new(ld['name'], light_data)
        bpy.context.collection.objects.link(light_obj)
        light_obj.location = ld['location']

        # Karaktere bak
        direction = target - light_obj.location
        rot = direction.to_track_quat('-Z', 'Y')
        light_obj.rotation_euler = rot.to_euler()

        light_objects.append(light_obj)

    return light_objects
```

### 3-Point Işık Kuralları

| Işık | Güç Oranı | Açı | Amaç |
|------|-----------|-----|------|
| Key (ana) | 100% | 45° yandan, 30° yukarı | Ana ışık, form gösterir |
| Fill (dolgu) | 30-50% | Karşı yandan, düşük | Gölge yumuşatma |
| Rim (kenar) | 60-80% | Arkadan | Siluet ayrıştırma |

---

## Turntable (360°) Render Setup

```python
def setup_turntable_render(char_obj, output_dir="/tmp/turntable", frames=36):
    """
    Karakteri 360° döndürerek render al.
    frames: kaç kare (36 = 10° adım)
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.film_transparent = True  # arka plan şeffaf

    # Kamera setup
    cam_data = bpy.data.cameras.new("TurntableCam")
    cam_data.lens = 85  # portrait lens
    cam_obj = bpy.data.objects.new("TurntableCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    scene.camera = cam_obj

    # Karakterin merkezini bul
    char_center = char_obj.location + Vector((0, 0, 0.9))
    cam_distance = 2.5

    # Empty (pivot) oluştur
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=char_center)
    pivot = bpy.context.active_object
    pivot.name = "TurntablePivot"

    # Kamerayı pivot'a bağla
    cam_obj.parent = pivot
    cam_obj.location = (0, -cam_distance, 0)

    # Karaktere bak
    constraint = cam_obj.constraints.new('TRACK_TO')
    constraint.target = char_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Her frame'de döndür ve render al
    for i in range(frames):
        angle = (360.0 / frames) * i
        pivot.rotation_euler.z = math.radians(angle)
        bpy.context.view_layer.update()

        filepath = os.path.join(output_dir, f"frame_{i:03d}.png")
        scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)

    print(f"Turntable render tamamlandı: {output_dir}")
```

---

## Karakter Portrait Camera

```python
def setup_portrait_camera(char_obj, shot='full'):
    """
    Karakter için portrait kamera.
    shot: 'full' (full body), 'bust' (göğüs üstü), 'face' (yüz yakın)
    """
    cam_data = bpy.data.cameras.new("CharPortrait")
    cam_obj = bpy.data.objects.new("CharPortrait", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Kamera ayarları (shot türüne göre)
    if shot == 'full':
        cam_data.lens = 50    # normal lens
        cam_obj.location = (0, -3.5, 0.9)
    elif shot == 'bust':
        cam_data.lens = 85    # portrait lens
        cam_obj.location = (0, -2.0, 1.1)
    elif shot == 'face':
        cam_data.lens = 135   # tele lens (yüzü düzleştirir)
        cam_obj.location = (0, -1.5, 1.0)

    # Karaktere bak
    constraint = cam_obj.constraints.new('TRACK_TO')
    constraint.target = char_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    bpy.context.view_layer.objects.active = cam_obj
    return cam_obj
```

**Lens Kuralı:**
- 24-35mm: geniş açı (mimari, ortam)
- 50mm: "göz" lens, normal perspektif
- 85mm: portrait standardı, yüz için ideal
- 135mm: tele, yüzü flatten eder (yuvarlak gösterir)

---

## EEVEE Render Ayarları (Script)

```python
def setup_eevee_character(high_quality=False):
    scene = bpy.context.scene
    # Blender 4.2-4.x: BLENDER_EEVEE_NEXT | Blender 3.x + 5.x: BLENDER_EEVEE
    v = bpy.app.version
    scene.render.engine = 'BLENDER_EEVEE_NEXT' if (4, 2) <= v[:2] < (5, 0) else 'BLENDER_EEVEE'

    eevee = scene.eevee

    if high_quality:
        eevee.taa_render_samples = 64
        eevee.use_gtao = True           # ambient occlusion
        eevee.gtao_distance = 0.2
        eevee.use_bloom = True
        eevee.bloom_intensity = 0.05
        eevee.use_ssr = True            # screen space reflections
        eevee.use_shadow_high_bitdepth = True
    else:
        eevee.taa_render_samples = 16
        eevee.use_gtao = True
        eevee.use_bloom = False

    # Render çözünürlük
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
```

---

## Cycles Render Ayarları (Script)

```python
def setup_cycles_character(quality='preview'):
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'

    cycles = scene.cycles
    settings = {
        'preview': {'samples': 64,  'use_denoising': True},
        'final':   {'samples': 256, 'use_denoising': True},
        'hero':    {'samples': 1024,'use_denoising': True},
    }
    s = settings[quality]
    cycles.samples = s['samples']
    cycles.use_denoising = s['use_denoising']

    # GPU varsa
    cycles.device = 'GPU'
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
```

---

## World (Environment) Setup

```python
def setup_studio_world(strength=0.3):
    """Studio tarzı nötr arka plan"""
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    world.use_nodes = True
    tree = world.node_tree
    tree.nodes.clear()

    # Background node
    bg = tree.nodes.new('ShaderNodeBackground')
    bg.inputs['Color'].default_value = (0.05, 0.05, 0.05, 1.0)  # koyu gri
    bg.inputs['Strength'].default_value = strength

    output = tree.nodes.new('ShaderNodeOutputWorld')
    tree.links.new(bg.outputs['Background'], output.inputs['Surface'])
```

---

## Hızlı Render Script (Full Pipeline)

```python
def render_character_showcase(char_obj, output_path="/tmp/character_render.png"):
    """Tek satır çağrı — karakter showcase render"""
    setup_3point_lighting(target_location=(0, 0, 0.9))
    setup_studio_world(strength=0.3)
    setup_portrait_camera(char_obj, shot='full')
    setup_eevee_character(high_quality=True)

    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.film_transparent = False
    bpy.ops.render.render(write_still=True)
    print(f"Render kaydedildi: {output_path}")
```

---

## Tam Kamera Ayarları — Portrait, Tüm Vücut (Kopyala-Yapıştır)

```python
def setup_full_body_portrait_camera(char_obj=None, output_res=(1080, 1920)):
    """
    Portrait format, karakter tüm frame'de, kopyala-yapistir hazir.
    char_obj: None ise scene'deki ilk MESH objeyi kullanir.
    output_res: (genislik, yukseklik) — default portrait 1080x1920
    """
    import bpy
    from mathutils import Vector

    # Karakter objesini bul
    if char_obj is None:
        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        if not meshes:
            raise RuntimeError("Scene'de mesh yok")
        char_obj = meshes[0]

    # Karakterin bounding box'ini hesapla
    verts_world = [char_obj.matrix_world @ Vector(v.co) for v in char_obj.data.vertices]
    min_z = min(v.z for v in verts_world)
    max_z = max(v.z for v in verts_world)
    center_x = sum(v.x for v in verts_world) / len(verts_world)
    center_z = (min_z + max_z) / 2
    char_height = max_z - min_z

    # Kamera mesafesini hesapla (tüm karakter frame'de görünsün)
    # portrait için: dikey alan = char_height * 1.1 (% 10 boşluk)
    fov_vertical = 0.6911  # 50mm lens ekvivalenti (~39.6 derece dikey)
    cam_distance = (char_height * 1.15) / (2 * math.tan(fov_vertical / 2))
    cam_distance = max(cam_distance, 1.5)  # minimum mesafe

    # Mevcut kamerayı temizle
    for obj in list(bpy.data.objects):
        if obj.type == 'CAMERA':
            bpy.data.objects.remove(obj, do_unlink=True)

    # Kamera oluştur
    cam_data = bpy.data.cameras.new("PortraitCam")
    cam_data.lens = 50          # 50mm — natural portrait
    cam_data.sensor_width = 36  # full frame
    cam_data.clip_start = 0.1
    cam_data.clip_end = 100.0

    cam_obj = bpy.data.objects.new("PortraitCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)

    # Kamera konumu: karakterin önünde, merkez hizasında
    cam_obj.location = (center_x, -cam_distance, center_z)

    # Karaktere bak (Track To constraint)
    track = cam_obj.constraints.new('TRACK_TO')
    track.target = char_obj
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    # Scene kamerası yap
    bpy.context.scene.camera = cam_obj

    # Çözünürlük — portrait format
    scene = bpy.context.scene
    scene.render.resolution_x = output_res[0]
    scene.render.resolution_y = output_res[1]
    scene.render.resolution_percentage = 100

    bpy.context.view_layer.update()
    print(f"Kamera: mesafe={cam_distance:.2f}m, karakter={char_height:.2f}m yüksek")
    return cam_obj
```

---

## HDRI Olmadan 3-Nokta Işık (Sadece Area/Spot)

```python
def setup_3point_no_hdri(char_height=1.0):
    """
    Sadece Area/Spot light ile kaliteli 3-nokta ısık.
    HDRI veya environment texture gerektirmez.
    char_height: karakterin toplam yuksekligi (ısık gucunu olcekler)
    """
    import bpy
    from mathutils import Vector

    # Mevcut ısıkları temizle
    for obj in list(bpy.data.objects):
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    # Karakter merkezi (genellikle z=0.5 civarı)
    char_center = Vector((0, 0, char_height * 0.55))
    base_energy = char_height * 200  # ölçekli güç

    light_configs = [
        # Key Light: sol ön-üst, sıcak beyaz
        {
            'name': 'Key',
            'type': 'AREA',
            'location': char_center + Vector((-char_height * 1.5, -char_height * 2.0, char_height * 1.5)),
            'energy': base_energy * 1.0,
            'color': (1.0, 0.97, 0.90),
            'size': char_height * 1.5,
        },
        # Fill Light: sag, dusuk, soguk
        {
            'name': 'Fill',
            'type': 'AREA',
            'location': char_center + Vector((char_height * 2.0, -char_height * 1.0, char_height * 0.3)),
            'energy': base_energy * 0.35,
            'color': (0.75, 0.82, 1.0),
            'size': char_height * 2.0,
        },
        # Rim Light: arkadan, spotlight
        {
            'name': 'Rim',
            'type': 'SPOT',
            'location': char_center + Vector((char_height * 0.3, char_height * 2.5, char_height * 1.2)),
            'energy': base_energy * 0.65,
            'color': (1.0, 1.0, 1.0),
            'spot_size': 0.6,   # radyan, ~35 derece
            'spot_blend': 0.15,
        },
    ]

    for cfg in light_configs:
        ld = bpy.data.lights.new(cfg['name'], cfg['type'])
        ld.energy = cfg['energy']
        ld.color  = cfg['color']
        if cfg['type'] == 'AREA':
            ld.size = cfg['size']
        elif cfg['type'] == 'SPOT':
            ld.spot_size  = cfg.get('spot_size', 0.785)
            ld.spot_blend = cfg.get('spot_blend', 0.15)

        lo = bpy.data.objects.new(cfg['name'], ld)
        bpy.context.collection.objects.link(lo)
        lo.location = cfg['location']

        # Sahne merkezine bak
        d = char_center - lo.location
        lo.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

    print("3-nokta ısık kuruldu (HDRI yok)")
```

---

## Zemin Shadow Catcher (Shadow-Only Plane)

```python
def add_shadow_catcher_floor(z_offset=0.0, size=4.0):
    """
    Sadece golge gösteren zemin plane — EEVEE ve Cycles uyumlu.
    z_offset: karakterin zemin hizasına göre (genellikle 0)
    """
    import bpy

    # Plane oluştur
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z_offset))
    floor = bpy.context.active_object
    floor.name = "ShadowCatcher"

    # Material: shadow catcher
    mat = bpy.data.materials.new("ShadowOnly")
    mat.use_nodes = True
    mat.shadow_method = 'CLIP'  # EEVEE shadow

    # Node tree temizle ve shadow catcher kur
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Cycles: is_shadow_catcher flag
    floor.is_shadow_catcher = True  # Blender 3.x+

    # EEVEE için: Holdout shader
    output = nodes.new('ShaderNodeOutputMaterial')
    holdout = nodes.new('ShaderNodeHoldout')
    links.new(holdout.outputs['Holdout'], output.inputs['Surface'])

    floor.data.materials.append(mat)

    # render.film_transparent = True gerekli (shadow görünsün, bg değil)
    bpy.context.scene.render.film_transparent = True

    print(f"Shadow catcher eklendi: z={z_offset}, size={size}m")
    return floor
```

**Not:** Shadow catcher gerçek gölgeyi görünür kılar, arka planı şeffaf tutar.
PNG olarak kaydettiğinde gölge + karakter, arka plan alpha'lı gelir.
