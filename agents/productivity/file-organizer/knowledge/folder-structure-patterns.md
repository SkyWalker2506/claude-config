---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Folder Structure Patterns

## Quick Reference

**Kullanıcı dizinleri (XDG benzeri):** `~/Downloads` geçici; `~/Documents` kalıcı; `~/Desktop` minimal tut (≤10 kısayol). **Projeler:** `~/Projects/<org>/<repo>`.

| Klasör | Amaç | Temizlik |
|--------|------|----------|
| Downloads | 30 gün kuralı | Haftalık |
| Desktop | aktif iş | Günlük |
| Archive | salt okunur yıl | Yıllık |

```text
Derinlik: tercihen ≤4 seviye — navigasyon ve yedek maliyeti
```

## Patterns & Decision Matrix

| Şema | Artı | Eksi |
|------|------|------|
| Yaşa göre yıl/ay | Arşiv kolay | Aktif proje dağılır |
| Projeye göre | Odak | Çapraz dosya zor |
| Tür bazlı (pdf/img) | Medya bulma | Proje bağlamı kaybolur |

**L5 ↔ L4:** Notlar `~/Vault`; ham indirilenler `~/Downloads` → PARA ile taşınır.

## Code Examples

**Önerilen iskelet:**

```text
~/Documents/
  Work/
    ACME/
      contracts/
      invoices/
  Personal/
    Finance/
    Health/
~/Downloads/
  _staging/   # taşınmayı bekleyen
```

**rsync yedek (örnek — dikkat trailing slash):**

```bash
rsync -a --delete ~/Documents/ /Volumes/Backup/Documents/
```

**find — 90 günden eski Downloads:**

```bash
find ~/Downloads -type f -mtime +90 -print
```

## Anti-Patterns

- **Tek dev "Stuff" klasörü:** Arama maliyeti patlar.
- **Senkron klasöründe build artifact:** `node_modules` OneDrive’a kopyalama.
- **İzin 0777 paylaşılan klasör:** Ekip için en az grup yazılabilir + sticky bit düşün.
- **Sistem köküne dosya:** `/`, `/etc` dokunma.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) — konfig ve veri yolları
- [Apple — macOS Library folders](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/) — sistem dizinleri
- [rsync manual](https://download.samba.org/pub/rsync/rsync.html) — yedekleme
