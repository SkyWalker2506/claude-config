---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# File Naming Conventions

## Quick Reference

**ISO tarih öneki:** `YYYY-MM-DD-slug.ext` — sıralama ve arama için ideal. **Güvenli karakter:** `[a-z0-9._-]`; boşluk yerine `-`; Türkçe karakterlerden kaçın veya NFC normalize.

| Alan | Kural |
|------|-------|
| Versiyon | `v1.2` veya `_v2` sonek, `final-final` yasak |
| Durum | `DRAFT`, `SIGNED` büyük harf prefix veya alt klasör |

```text
Uzunluk: ≤120 karakter tam yol parçası (Windows uyumu için dikkat)
```

## Patterns & Decision Matrix

| Şema | Artı | Eksi |
|------|------|------|
| Tarih-önce | Kronolojik sıra | Slug uzun |
| Proje-kod-önce | Ekip paylaşımı | Tarih ikinci planda |
| Hash sonek | Çakışma yok | İnsan okunmaz |

**Çift uzantı:** `report.pdf.gz` — sırayı koru; arşiv tipi son uzantı.

## Code Examples

**Slug üretimi (bash):**

```bash
title="Q2 Budget FINAL!!"
slug=$(echo "$title" | iconv -f UTF-8 -t ASCII//TRANSLIT \
  | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-\|-$//g')
echo "2026-04-09-$slug.pdf"
```

**Python — güvenli isim:**

```python
import re
def safe_name(s: str) -> str:
    s = re.sub(r"[^\w.\-]+", "_", s, flags=re.ASCII)
    return s[:120]
```

**Örnek hiyerarşi:**

```text
~/Documents/
  2026/
    2026-04-09-invoice-acme-v2.pdf
    2026-04-08-spec-api-signed.pdf
```

## Anti-Patterns

- **`:` ve `?` (macOS/Win uyumsuzluğu):** NTFS yasaklı karakterler.
- **CASE çakışması:** `Report.pdf` ve `report.pdf` aynı klasörde (Linux’ta mümkün) — tek politika seç.
- **Sürüm karmaşası:** `v2 (1)` yerine anlamlı `v2.1-client-feedback`.
- **Kişisel sırlı dosya adı:** `passwords.txt` — isimlendirme ile içerik ifşa etme.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Unicode — normalization forms](https://unicode.org/reports/tr15/) — NFC/NFD dosya adları
- [Microsoft — Naming conventions](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file) — yasaklı karakterler
- [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) — tarih formatı
