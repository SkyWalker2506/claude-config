---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Library Version Tracking

## Quick Reference

| Ecosystem | Kilit dosya | Sürüm alanı |
|-----------|-------------|-------------|
| npm / JS | `package.json` | `dependencies` semver |
| Python | `pyproject.toml` / `requirements` | PEP 440 |
| Rust | `Cargo.toml` | `version` + edition |
| Unity | `Packages/manifest.json` | `com.unity.*` |
| .NET | `*.csproj` | `PackageReference` |

```text
Matris: library@requested → resolved@lock → doc_url(version)
```

## Patterns & Decision Matrix

| Durum | Aksiyon |
|-------|---------|
| Caret `^` geniş | Minimum ve maximum uyumlu aralığı not et |
| Pin exact | Tek sürüm — doc tek URL |
| Transitive conflict | Hangi üst paket zorluyor — `npm ls` / `cargo tree` |

**Karar:** Kullanıcıya “hangi kilit dosyayı doğruladın?” satırını ekle.

## Code Examples

**Sürüm satırı:**

```text
[VERSION]
declared: foo@^2.1.0
lockfile: foo@2.1.3 (from package-lock / Cargo.lock)
doc: https://…/v2.1/
```

## Anti-Patterns

- **Major atlamayı patch sanmak:** Breaking başlıkları migration guide’da ara.
- **Pre-release karışımı:** `2.0.0-rc` ile `2.0.0` doc farklı olabilir.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Semver spec](https://semver.org/) — sürüm anlamı
- [PEP 440](https://peps.python.org/pep-0440/) — Python sürümleme
