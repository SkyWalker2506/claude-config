---
name: gorsel-uret
description: "Ortak GPU makinesine sprite/gorsel uretim istegi birak, sirasini takip et, sonucu indir (SDXL + Qwen, API uzerinden kuyruk). Triggers: gorsel uret, resim uret, sprite uret, ikon uret, karakter gorseli, sahne gorseli, image generate, gorsel api, kuyruga ekle, sprite forge, anim_image_jobs."
user-invocable: true
---

# Görsel üret — ortak GPU kuyruğuna istek bırak

Sprite, karakter, sahne ya da ikon görseli üretmek için. Üretimi RTX 5080'li
ortak makine yapıyor; bu belge **istek bırakan tarafın** ne yapması gerektiğini
anlatır.

- API: `https://arngdwwjjopmggixakez.supabase.co/rest/v1`
- Web: https://animation-review-phi.vercel.app → **Görsel üret** sekmesi
- Repo: `~/Projects/animation-creator` (kuyruk + ajan), `~/Projects/bm-sprite-forge` (model seçimi)
- Tam API belgesi: `animation-creator/docs/GORSEL-API.md`

**Makine kapalıyken de istek bırakılabilir.** İstek Supabase'e yazılır, GPU
makinesi açılınca sırayla üretir. "Makine açık mı" diye beklemeye gerek yok.

Referans verildiğinde stil tarif edilmez, **gösterilir**. Genel kural:
**[/reference-style](../reference-style/SKILL.md)**.

---

## 0. Anahtar

```
ANON=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFybmdkd3dqam9wbWdnaXhha2V6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM3MzM4MjUsImV4cCI6MjA5OTMwOTgyNX0.lLOjQed_JkZwWCSd7w-h6Ph5xbc9gBtnZsz_3XEN0mw
```

Herkese açık olacak şekilde tasarlandı (yayınlanan sayfanın içinde de duruyor).
Güvenlik satır bazlı izinlerde: dışarıdan yalnızca bekleyen iş açılabilir ve
iptal edilebilir. `status: "done"` göndermek **401** ile reddedilir — üretimi
yalnızca GPU makinesi bitirebilir.

## 1. İş aç

```bash
curl -X POST "https://arngdwwjjopmggixakez.supabase.co/rest/v1/anim_image_jobs" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON" \
  -H "Content-Type: application/json" \
  -d '{"id":"ij_'$(date +%s)'","ad":"kilic-ikonu","sinif":"karakter",
       "prompt":"a knight sprite, side view, black background",
       "negative":"blurry, watermark, text",
       "params":{"adet":2,"genislik":1024,"yukseklik":1024,"tohum":0},
       "status":"pending","requested_by":"'$USER'"}'
```

**Prompt İngilizce yazılır.** Türkçe prompt çıktı kalitesini düşürüyor —
ölçüldü, bu ekosistemde tekrar eden bir hata.

`params.tohum` 0 ise rastgele seçilir ve **kullanılan tohum sonuca yazılır**.
Tohum kaydedilmezse görsel yeniden üretilemez; "bunu tekrar yap" bu hattın en
sık isteği.

## 2. Takip et

```bash
curl "https://arngdwwjjopmggixakez.supabase.co/rest/v1/anim_image_jobs?id=eq.ij_xxx&select=status,error" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
```

`pending` → `claimed` → `done` / `failed`.

**`failed` görünce `error` alanını oku.** Sebep oraya yazılıyor; tahmin etme,
log dosyası arama. Kapalı bir sınıfa istek açtıysan sebep orada yazar.

## 3. Sonucu al

```bash
curl "https://arngdwwjjopmggixakez.supabase.co/rest/v1/anim_image_results?job_id=eq.ij_xxx&select=url,tohum,model" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON"
```

`url` doğrudan indirilebilir.

## 4. Referanslı üretim

Önce `sources/` altına yükle, sonra yolu `referanslar` dizisine koy:

```bash
curl -X POST "https://arngdwwjjopmggixakez.supabase.co/storage/v1/object/animations/sources/$(date +%s)_ref.png" \
  -H "apikey: $ANON" -H "Authorization: Bearer $ANON" \
  -H "Content-Type: image/png" --data-binary @ref.png
```

En fazla 3 referans, yol **`sources/` ile başlamak zorunda** — başka önek
reddediliyor (keyfi yol okutmak dosya sızdırır).

Referanslı kipte sınıfın varsayılan modeli yerine Qwen-Image-Edit kullanılır.

> **Boş bıraktığın her şey referanstan kopyalanır.** Neyin değişmesini
> istiyorsan açıkça yaz; genel bir prompt referansı yeniden üretir.

---

## Sınıflar — ikisi kapalı, kasıtlı

| sınıf | boyut | durum |
|---|---|---|
| `karakter` | 1024×1024 | ✅ SDXL / Juggernaut-XL |
| `sahne` | 720×960 | ✅ Qwen-Image |
| `ikon` | 1024×1024 | ⛔ ölçülmedi |
| `yazili` | 1024×1024 | ⛔ ölçülmedi |

Kapalı sınıf bir eksiklik değil, bir **kapı**: hangi modelin o işi iyi yaptığı
ölçülmeden üretime açılmıyor. Açmak için `bm-sprite-forge`'da
`python tools/bakeoff.py --sinif ikon` çalıştırılır ve sonuç `SECIMLER`'e
işlenir.

Sınıf seçimi burada YAPILMAZ, `bm-sprite-forge/pipeline/models.py`'ye
sorulur. İki yerde iki karar tablosu tutmak zamanla iki farklı karara döner.

## Süre — ne beklemeli

RTX 5080'de ölçüldü (2026-08-17), 1024×1024 `karakter`:

```
ilk görsel (model yükleme dahil)   23.7 sn
sonraki her görsel                  8.4 sn   (9 üretimde sapma yok)
10 görsellik parti                 99.4 sn
```

Ama **sıra paylaşımlı**. Aynı kart video da üretiyor ve ikisi aynı anda
sığmıyor (Wan ~14.5 GB, SDXL ~8 GB, kart 16.3 GB). Tür değişimi ~45 saniye saf
model taşıma demek, o yüzden işler öbek hâlinde çalışıyor:

- resim üretiliyorsa → resim kuyruğu **boşalana kadar** devam eder
- video üretiliyorsa → **10 resim birikmeden** kesilmez
- video kuyruğu boşsa → tek resim için bile resme geçilir

Yani tek bir acil resim isteği, çalışan video kuyruğunu kesmez. Acilse GPU
makinesindeki panelden elle "resme geç" denir.

## Tuzaklar

**Silme 200 dönebilir ama silmemiş olabilir.** PostgREST kapalı bir DELETE'i
hata yerine "0 satır etkilendi" ile döndürüyor. Ölçüldü: 82 silme denemesi
başarılı göründü, hiçbiri silmedi. Silmeden sonra satırı **tekrar sorgula**.

**Yalnızca `pending` iş silinebilir.** Üretime alınmış işe dokunulamıyor.

**`adet` en fazla 10.** Fazlası için birden çok iş aç; her görsele ayrı tohum
verilir, yoksa aynı görsel defalarca üretilir.

**Üretilen dosyalar herkese açık bağlantıda.** Gizli içerik gönderme.

## İlgili

- **[/animate](../animate/SKILL.md)** — üretilen görseli sprite animasyonuna çevir
- **[/reference-style](../reference-style/SKILL.md)** — referanstan stil aktarımı kuralı
- **[/image-prompt](../image-prompt/SKILL.md)** — prompt yazım biçimi
