---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Semantic versioning and changelog for MCP packages

## Quick Reference

| Kural | Uygulama |
|-------|----------|
| **SemVer** | MAJOR = kırıcı şema; MINOR = uyumlu özellik; PATCH = düzeltme |
| **CHANGELOG.md** | Keep a Changelog formatı |
| **Pre-release** | `1.2.0-beta.1` — dizinlerde “stable” etiketi |
| **engines** | `node >=18` — Claude Code ortamıyla uyum |

MCP sunucusu: `tools` / `resources` şeması değişince **MAJOR** yükselt.

## Patterns & Decision Matrix

| Değişiklik | Sürüm |
|------------|-------|
| Yeni tool, eski çağrılar çalışıyor | MINOR |
| Tool input şeması alan sildi / tip değiştirdi | MAJOR |
| Dokümantasyon / README | PATCH veya MINOR (görünürlük) |

## Code Examples

**package.json alanları (yayın öncesi kontrol):**

```json
{
  "name": "@acme/mcp-weather",
  "version": "1.3.0",
  "license": "MIT",
  "repository": { "type": "git", "url": "https://github.com/acme/mcp-weather.git" },
  "files": ["dist", "README.md", "LICENSE"],
  "engines": { "node": ">=18" }
}
```

**CHANGELOG parçası:**

```markdown
## [1.3.0] - 2026-04-10
### Added
- tool `forecast` — şehir bazlı 7 günlük özet

### Changed
- `alerts` artık ISO-8601 zaman damgası döndürür (kırıcı — MAJOR gerekirdi; burada örnek MINOR tutuldu → gerçekte MAJOR yapın)
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sürümü manuel unutup npm publish | Aynı semver tekrar |
| Kırıcı değişiklik PATCH’te | İstemci kırılır |
| Git tag yok | Kullanıcı hangi kaynak kodu eşleşiyor bilmez |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [SemVer 2.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [npm — package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
- [Model Context Protocol — versioning notes](https://modelcontextprotocol.io/) — resmi şema değişiklikleri
