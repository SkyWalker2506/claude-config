---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Timestamp Navigation

## Quick Reference

| Format | Örnek | Kullanım |
|--------|-------|----------|
| `mm:ss` | `03:42` | <1 saat |
| `hh:mm:ss` | `01:03:42` | Uzun yayın |
| YouTube deep link | `?t=222` | Paylaşım |
| WebVTT | `00:03:42.000` | Altyazı |

```text
Kural: Aynı özette tek format; deep link üretilebiliyorsa ekle
```

## Patterns & Decision Matrix

| Görev | Uygulama |
|-------|----------|
| “Şu konu nerede?” | Anahtar kelime → en yakın segment |
| Bölüm listesi | Sessizlik / müzik geçişi ipucu |
| Alıntı doğrulama | ±2 sn komşu segmentleri oku |

**Karar:** Zaman damgası verirken transkript ile video süresi tutarlı mı kontrol et.

## Code Examples

**Navigasyon satırı:**

```text
[NAV] topic=authentication | start=03:42 | url=…&t=222s | confidence=high
```

## Anti-Patterns

- **Yaklaşık dakika:** “~5:00” yerine transkriptten kesin süre.
- **Bölge farkı:** Canlı kayıtta reklam ekleri süreyi kaydırabilir.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Media Fragments URI](https://www.w3.org/TR/media-frags/) — standart zaman URI
- Platform oynatıcı dokümantasyonu — `t` parametresi davranışı
