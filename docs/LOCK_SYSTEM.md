# Forge Lock Sistemi

Bu dosya otonom task pipeline'lari icin ortak lock protokolünü tanımlar.  
Referans veren skill'ler: `/forge`, `/yolo`

---

## Sprint Dosyasi Lock (`.forge-state/sprint-op.lock`)

Birden çok agent aynı anda sprint dosyasina yazmasın diye kullanılır.

| Durum | Aksiyon |
|-------|---------|
| Lock yok | Yaz → işlemi yap → lock sil |
| Lock var, timestamp < 60s | 30s bekle → tekrar kontrol (max 5 deneme) → sonra stale say |
| Lock var, timestamp ≥ 60s (stale) | Lock sil → devam et |
| İşlem sonrası | Her zaman lock sil (hata olsa bile) |

```bash
# Lock yaz
date -u +"%Y-%m-%dT%H:%M:%SZ" > .forge-state/sprint-op.lock

# Lock sil
rm -f .forge-state/sprint-op.lock
```

---

## Working Lock (`.forge-state/working-{T-NNN}.lock`)

Implementation agent'ın aktif olduğunu gösterir.

| Durum | Aksiyon |
|-------|---------|
| Lock var, timestamp < 15dk | Implementation çalışıyor → atla |
| Lock yok veya ≥ 15dk (stale) | Lock sil → yeni implementation agent başlat |

```bash
# Lock oluştur (agent başlarken)
date -u +"%Y-%m-%dT%H:%M:%SZ" > .forge-state/working-{T-NNN}.lock

# Her 10dk yenile
date -u +"%Y-%m-%dT%H:%M:%SZ" > .forge-state/working-{T-NNN}.lock

# Bitince MUTLAKA sil (hata olsa bile)
rm -f .forge-state/working-{T-NNN}.lock
```

---

## Stop Dosyası (`.forge-state/forge-run.stop`)

Kullanici iptal ettiginde olusturulur. Her tur başında kontrol edilir.

```bash
# Kontrol (her tur başı)
[ -f .forge-state/forge-run.stop ] && rm -f .forge-state/forge-run.stop && exit

# Cancel komutu
touch .forge-state/forge-run.stop
```

---

## Dizin yapısı

```
.forge-state/
  sprint-op.lock          # İşlem lock (geçici)
  forge-run.stop         # Cancel sinyali
  working-{T-NNN}.lock # Implementation agent lock
```

`mkdir -p .forge-state` ile dizin oluşturulmuş olmalı.
