---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Resource Curation

## Quick Reference

| İlke | Uygulama |
|------|----------|
| **Kapsam** | Tek konu — “her şey” listesi yok |
| **Çeşitlilik** | Resmi + topluluk + bir karşı görüş |
| **Metadata** | Erişim (ücretsiz/ücretli), dil, sürüm |
| **Yenileme** | Liste tarihi ve sahibi |

```text
Paket: tema | hedef kitle | 5–12 kaynak | çıkartma politikası
```

## Patterns & Decision Matrix

| Liste boyutu | Kullanım |
|--------------|----------|
| 3–5 | Hızlı başlangıç |
| 8–12 | Derin öğrenme |
| 20+ | Arşiv — filtre şart |

**Karar:** Aynı içeriğin aynalarını (aynı yazının kopyası) tek girişte birleştir.

## Code Examples

**Kürasyon bloğu:**

```text
[CURATE] topic=… | audience=junior | count=8 | last_review=…
primary: [url, url]
community: [url]
contrarian: [url] — note: …
```

## Anti-Patterns

- **Affiliate gizleme:** Ticari ilişki varsa etiketle.
- **Ölü link:** Liste yayınlanmadan önce HEAD/GET kontrolü.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- Zotero / reference manager en iyi uygulamaları
- Creative Commons lisans özetleri — yeniden kullanım
