---
last_updated: 2026-04-10
refined_by: coverage-bootstrap
confidence: high
sources: 3
---

# README standards (badges, sections, quality)

## Quick Reference

| Bölüm | Amaç |
|-------|------|
| Hero | Proje adı, tek cümle değer |
| Badges | lisans, CI, paket sürümü |
| Install | kopyala-yapıştır çalışır komut |
| Related | ekosistem sırası (catalog → marketplace → config) |

## Patterns & Decision Matrix

| Repo tipi | Minimum |
|-----------|---------|
| Kütüphane | API örneği + semver |
| Uygulama | env + run |
| Meta (marketplace) | plugin tablosu |

## Code Examples

```markdown
[![License](https://img.shields.io/badge/license-MIT-22c55e)](./LICENSE)
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sürüm yok | Kullanıcı ne yüklediğini bilmez |

## Deep Dive Sources

- [GitHub — About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [shields.io](https://shields.io/)
- [Make a README](https://www.makeareadme.com/)
