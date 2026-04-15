---
last_updated: 2026-04-14
refined_by: live testing goblin face v1-v4
confidence: high
---

# Feature Recipes — Blender'da Yüz Parçaları Nasıl Yapılır

Her feature için: doğru yöntem, boyut, renk, yaygın hatalar.

---

## DİŞ / FANG

### Doğru yöntem
- **Cone primitive** — `primitive_cone_add(vertices=8, radius1=base, radius2=tip, depth=length)`
- Üst dişler aşağı sarkar, alt fanglar yukarı çıkar
- Her diş AYRI obje — metaball ile YAPMA (lump olur)

### Boyutlar (1.0m boy goblin kafası için)
| Diş tipi | Base radius | Tip radius | Uzunluk | Not |
|----------|------------|------------|---------|-----|
| Alt fang (büyük) | 0.012 | 0.003 | 0.05 | En dikkat çekici |
| Üst fang | 0.010 | 0.002 | 0.04 | |
| Küçük diş | 0.006 | 0.002 | 0.025 | |

### Renk
- BEYAZ DEĞİL — kemik/fildişi: (0.65, 0.58, 0.40, 1.0)
- Roughness: 0.3-0.4 (hafif parlak)
- Diş dibinde daha koyu (gum line)

### Yerleşim
- Üst dişler: üst dudak hizasında, Y = dudak Y - 0.01
- Alt fanglar: alt çene hizasında, Y = çene Y - 0.02
- X aralığı: her diş arası ~0.02-0.03

### Yaygın hatalar
- ❌ Metaball ile diş → lump olur
- ❌ Çok büyük cone → bıçak gibi görünür
- ❌ Beyaz renk → plastik görünür
- ❌ Tüm dişleri aynı boyut → doğal değil

---

## GÖZ

### Doğru yöntem
- **UV Sphere** — `primitive_uv_sphere_add(radius=0.04, segments=16, ring_count=12)`
- Göz çukuru içine yerleştir (brow ridge altında)
- Emission material ile glow efekti

### Boyut
- Radius: kafanın %8-12'si (0.035-0.05 for 0.35 radius head)
- Gözler arası mesafe: kafa genişliğinin %35'i

### Renk (goblin)
- Base: sarı-turuncu (1.0, 0.6, 0.0)
- Emission: aynı renk, strength 8-15
- Roughness: 0.05 (çok parlak)

### Yerleşim
- X: ±0.10 (kafa merkezinden)
- Y: -0.17 (öne doğru, brow ridge altında)
- Z: 0.0 (kafa merkezi hizası)

### Yaygın hatalar
- ❌ Göz çok büyük → karikatür
- ❌ Emission çok düşük → glow yok
- ❌ Gözler çok yakın → tuhaf bakış

---

## KULAK

### Doğru yöntem
- **Metaball chain** — 4 segment (base → mid1 → mid2 → tip)
- Base kafaya gömülü (cranium ile overlap)
- Her segment küçülür: base 0.12 → tip 0.04

### Boyut
- Toplam uzunluk: kafa yüksekliğinin %50-70'i
- Base radius: 0.10-0.12
- Tip radius: 0.03-0.04
- Yayılma: X yönünde 0.30+ kafa merkezinden

### Yön
- Yukarı ve geriye doğru (~30-45° swept back)
- İç kısmı hafif öne (inner element ekle)

### Yaygın hatalar
- ❌ Kulak çok küçük → goblin gibi okunmuyor
- ❌ Threshold yüksek → kulak ayrık blob
- ❌ Sadece 2 segment → yuvarlak, sivri değil

---

## BURUN

### Doğru yöntem
- **Metaball** — 4-5 element (bridge → mid → tip → nostrils)
- Tip en büyük element (bulbous)
- Nostriller tip'in yanlarında

### Boyut
- Bridge radius: 0.05-0.06
- Tip radius: 0.07-0.08 (burnun en geniş yeri)
- Nostril radius: 0.04-0.05

### Yaygın hatalar
- ❌ Burun çok küçük → yüzde kaybolur
- ❌ Tek element → top gibi, burun değil

---

## BROW RIDGE (Alın Çıkıntısı)

### Doğru yöntem
- **3 metaball** — sol, sağ, merkez
- Gözlerin hemen üstünde, öne çıkık
- Y değeri cranium'dan -0.20 öne

### Boyut
- Sol/sağ: radius 0.09-0.10
- Merkez: radius 0.07-0.08
- Dış köşe: radius 0.05-0.06

---

## ÇENE

### Doğru yöntem
- Üst çene ve alt çene AYRI element grupları
- Aralarında Z boşluğu = ağız açıklığı
- Alt çene daha aşağıda (Z fark: 0.10-0.14)

### Ağız açıklığı
- Upper lip Z: -0.14
- Lower jaw Z: -0.26
- Boşluk: 0.12 (dişler burada görünür)

### Yaygın hatalar
- ❌ Çeneler çok yakın → ağız kapalı
- ❌ Çok fazla küçük element → kaotik lump
- ❌ Alt çene çok büyük → balon gibi
