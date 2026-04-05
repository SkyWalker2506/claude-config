---
name: plugin-update
description: "Kurulu plugin'leri güncelle. Triggers: plugin update, plugin güncelle, pluginleri güncelle, update plugins"
argument-hint: "[plugin-id veya boş = hepsi]"
---

# /plugin-update

Kurulu plugin'leri GitHub'dan günceller.

## Kullanım
- `/plugin-update` — tüm plugin'leri güncelle
- `/plugin-update notifications` — sadece notifications plugin'ini güncelle

## Akış
1. `config/plugin-update.sh` çalıştır
2. Sonucu raporla
