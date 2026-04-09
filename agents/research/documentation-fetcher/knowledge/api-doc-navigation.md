---
last_updated: 2026-04-09
confidence: high
sources: 4
---

# API Doc Navigation

## Quick Reference

| Hedef | Tipik yol | İpucu |
|-------|-----------|-------|
| REST endpoint | `/reference` veya OpenAPI | `GET /v1/...` tam path |
| SDK method | Dil paketi → class | semver ile eşle |
| CLI | Commands / flags | exit code bölümü |
| Auth | Security / OAuth | scope tablosu |

```text
URL şablonu: base_docs + /api|reference|sdk + version_segment
```

## Patterns & Decision Matrix

| Doc stili | Okuma sırası |
|-----------|--------------|
| OpenAPI öncelikli | Paths → schemas → examples |
| Narrative öncelikli | Quickstart → API reference |
| Monorepo çok paket | Paket adını kilitle, yanlış re-export’a düşme |

**Karar:** Örnek kod dilini tüketici projeyle eşle; yoksa “pseudo + link” ile işaretle.

## Code Examples

**Fetch görev özeti:**

```text
[DOC FETCH]
product: …
version: x.y.z
artifact: REST / SDK_python / CLI
pages_resolved: [url1, url2]
breaking_notes: … | none
```

## Anti-Patterns

- **“Latest”e körü körüne:** Proje `package.json` / `Cargo.toml` sürümüyle doc URL’ini eşle.
- **Eski CDN cache:** Doc sayfası “edited date” ve changelog ile çapraz kontrol.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [OpenAPI Specification](https://swagger.io/specification/) — makine okunur API haritası
- [Diátaxis framework](https://diataxis.fr/) — dokümantasyon türleri (tutorial/how-to/reference)
