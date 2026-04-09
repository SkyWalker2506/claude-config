---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Automated Cleanup

## Quick Reference

**Politika:** Silmeden önce karantina (`~/.cleanup-quarantine/2026-04-09/`) veya çöp kutusu süresi 7 gün. **Hedefler:** `Downloads/*.tmp`, `.DS_Store`, boş klasörler, `Thumbs.db`.

| Tetik | Araç |
|-------|------|
| Zaman | `cron`, `launchd`, `systemd timer` |
| Eşik | disk %85 dolunca agresif mod |

```text
dry_run: her zaman önce --dry-run veya log-only modu
```

## Patterns & Decision Matrix

| Strateji | Risk | Kullan |
|----------|------|--------|
| Yaş bazlı silme | Orta | Cache, temp |
| Tür bazlı arşiv | Düşük | Eski PDF → Archive |
| İçerik hash sonrası | Düşük | Duplicate sonrası |

**G6 (Backup Agent) ile:** Temizlik öncesi yedek doğrulanmış mı kontrol et.

## Code Examples

**macOS launchd — haftalık temizlik (özet):**

```xml
<key>StartCalendarInterval</key>
<dict>
  <key>Weekday</key><integer>0</integer>
  <key>Hour</key><integer>3</integer>
  <key>Minute</key><integer>0</integer>
</dict>
```

**Güvenli yaş silme (bash — örnek):**

```bash
QUAR=~/.cleanup-quarantine/$(date +%F)
mkdir -p "$QUAR"
find ~/Downloads -type f -mtime +60 -exec mv {} "$QUAR/" \;
echo "Moved to $QUAR — review before rm -rf"
```

**Disk eşik uyarısı:**

```bash
pct=$(df -h ~ | awk 'NR==2 {gsub(/%/,""); print $5}')
if [ "$pct" -ge 85 ]; then echo "WARN disk ${pct}% full"; fi
```

## Anti-Patterns

- **`rm -rf ~/Downloads/*` otomasyon:** Kullanıcı onayı olmadan yok.
- **Proje klasöründe agresif `*.log` silme:** Geliştirici logları gerekli olabilir.
- **iCloud çakışma anında silme:** Önce senkron durumu kontrol.
- **Sessiz başarısızlık:** Cron çıktısını `/var/log` veya `~/Library/Logs` yaz.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [GNU findutils](https://www.gnu.org/software/findutils/manual/html_node/find_html/index.html) — `find` güvenli kullanım
- [Apple — launchd](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html) — zamanlayıcı
- [systemd.timer](https://www.freedesktop.org/software/systemd/man/systemd.timer.html) — Linux zamanlayıcı
