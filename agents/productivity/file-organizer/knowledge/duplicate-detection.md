---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Duplicate Detection

## Quick Reference

**Katmanlar:** (1) Boyut + kısa hash (hızlı aday); (2) tam SHA-256; (3) görüntü için perceptual hash (pHash). **Yanlış pozitif:** aynı boyut farklı içerik — tam hash ile çöz.

| Yöntem | Çakışma riski | Hız |
|--------|---------------|-----|
| MD5/SHA256 dosya | Önemsiz | Orta |
| rsync --checksum | Senkron doğrulama | Yavaş |
| fdupes / jdupes | Kullanıcı dostu | Orta |

```text
near-duplicate (metin): simhash veya minhash — farklı kayıtlı aynı PDF
```

## Patterns & Decision Matrix

| Senaryo | Öneri |
|---------|--------|
| Aynı indirme 2 kez | Boyut+isim veya SHA |
| Fotoğraf kopyaları | `exiftool` + perceptual hash |
| Kod kopyası | Git içinde `git blame` / dedup değil refactor |

**Silme politikası:** En eski veya en kısa yolu tut; önce karantina.

## Code Examples

**SHA-256 listesi (find + shasum):**

```bash
find ~/Documents -type f -print0 | xargs -0 shasum -a 256 \
  | sort | awk '{c[$1]++; l[$1]=l[$1] $2 "\n"} END{for(h in c) if(c[h]>1) print h, l[h]}'
```

**Python — chunk okuma:**

```python
import hashlib
def sha256_file(path, chunk=1024*1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()
```

**fdupes örnek (interaktif olmadan rapor):**

```bash
fdupes -r -S ~/Pictures > /tmp/dup-report.txt
```

## Anti-Patterns

- **Sert link ile duplicate sanmak:** İki dosya aynı inode olabilir (hard link) — kasıtlı.
- **Küçük farklılıkta bin silmek:** Near-dup için insan onayı.
- **Bulut çözümlü dosyada hash:** Önce tam indirilmiş mi kontrol.
- **Sistem kütüphanelerinde tarama:** `/System` hariç tut.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [NIST — SHA-256](https://csrc.nist.gov/publications/detail/fips/180/4/final) — hash standardı
- [jdupes](https://github.com/jbruchon/jdupes) — hızlı duplicate finder
- [ImageHash — perceptual hashing](https://pypi.org/project/ImageHash/) — görüntü yakın eşleri
