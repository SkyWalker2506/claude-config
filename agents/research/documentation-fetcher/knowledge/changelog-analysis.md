---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Changelog Analysis

## Quick Reference

| Okuma modu | Ne aranır | Çıktı |
|------------|-----------|-------|
| **Upgrade** | BREAKING, Deprecated, Removed | Göç adımları |
| **Security** | CVE, GHSA | Etkilenen sürümler |
| **Bugfix** | Regression fix | Senin hatana benzeyen issue # |

```text
Etiketler: ADDED | CHANGED | DEPRECATED | REMOVED | FIXED | SECURITY
```

## Patterns & Decision Matrix

| Kaynak formatı | Güvenilirlik |
|----------------|--------------|
| Keep a Changelog uyumlu | Yüksek |
| GitHub Releases notları | Orta–yüksek |
| Sadece git log | Düşük — özütle |

**Karar:** Breaking madde varsa migration linkini aynı blokta ver.

## Code Examples

**Changelog özeti:**

```text
[CHANGELOG digest] lib@2.1 → 2.4
breaking:
  - … (link)
deprecations:
  - … removal: v3
action_items_for_consumer:
  - …
```

## Anti-Patterns

- **Sadece son sürüm notuna bakmak:** Ara major’ları atla.
- **“Misc fixes”e güvenmek:** Issue tracker’da anahtar kelime tara.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Keep a Changelog](https://keepachangelog.com/) — bölüm standardı
- [GitHub Advisory Database](https://github.com/advisories) — güvenlik düzeltmeleri
