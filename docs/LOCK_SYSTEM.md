# Jira Lock Sistemi

Bu dosya tüm Jira skill'leri için ortak lock protokolünü tanımlar.  
Referans veren skill'ler: `/jira-run`, `/jira-start-new-task`

---

## Jira İşlem Lock (`.jira-state/jira-op.lock`)

Birden çok agent aynı anda Jira'ya yazmasın diye kullanılır.

| Durum | Aksiyon |
|-------|---------|
| Lock yok | Yaz → işlemi yap → lock sil |
| Lock var, timestamp < 60s | 30s bekle → tekrar kontrol (max 5 deneme) → sonra stale say |
| Lock var, timestamp ≥ 60s (stale) | Lock sil → devam et |
| İşlem sonrası | Her zaman lock sil (hata olsa bile) |

```bash
# Lock yaz
date -u +"%Y-%m-%dT%H:%M:%SZ" > .jira-state/jira-op.lock

# Lock sil
rm -f .jira-state/jira-op.lock
```

---

## Working Lock (`.jira-state/working-{KEY-XX}.lock`)

Implementation agent'ın aktif olduğunu gösterir.

| Durum | Aksiyon |
|-------|---------|
| Lock var, timestamp < 15dk | Implementation çalışıyor → atla |
| Lock yok veya ≥ 15dk (stale) | Lock sil → yeni implementation agent başlat |

```bash
# Lock oluştur (agent başlarken)
date -u +"%Y-%m-%dT%H:%M:%SZ" > .jira-state/working-{KEY-XX}.lock

# Her 10dk yenile
date -u +"%Y-%m-%dT%H:%M:%SZ" > .jira-state/working-{KEY-XX}.lock

# Bitince MUTLAKA sil (hata olsa bile)
rm -f .jira-state/working-{KEY-XX}.lock
```

---

## Stop Dosyası (`.jira-state/jira-run.stop`)

`/jira-cancel` tarafından oluşturulur. Her tur başında kontrol edilir.

```bash
# Kontrol (her tur başı)
[ -f .jira-state/jira-run.stop ] && rm -f .jira-state/jira-run.stop && exit

# Cancel komutu
bash scripts/jira_run_cancel.sh
```

---

## Dizin yapısı

```
.jira-state/
  jira-op.lock          # İşlem lock (geçici)
  jira-run.stop         # Cancel sinyali
  working-{KEY-XX}.lock # Implementation agent lock
```

`mkdir -p .jira-state` ile dizin oluşturulmuş olmalı.
