---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# YouTube Transcript Extraction

## Quick Reference

| Yol | Koşul | Not |
|-----|-------|-----|
| **Resmi caption track** | Video’da CC var | Dil seçimi |
| **Auto-caption** | Kalite değişken | Teknik terim hataları |
| **3rd-party API** | Politika uyumu | Hizmet şartlarını kontrol et |
| **fetch MCP / sayfa** | Transcript endpoint erişilebilir | Rate limit |

```text
Çıktı: segments[{start_sec, text}] veya düz metin + zaman damgası her N satır
```

## Patterns & Decision Matrix

| Sorun | Çözüm |
|-------|-------|
| Çoklu dil | Varsayılan dil + manuel seçim |
| Müzik ağırlıklı | Transcript boşsa “no reliable transcript” |
| Canlı yayın arşivi | Gecikmeli işleme; bölümler ayrı |

**Karar:** Otomatik altyazıda teknik isimleri video başlığı / açıklama ile çapraz doğrula.

## Code Examples

**Segment şablonu:**

```text
[TRANSCRIPT] video_id=… | lang=en | source=auto|manual | segments=142
0:00 Intro …
3:12 …
```

## Anti-Patterns

- **Transcript’i kaynak sanmak:** Konuşmacı slayt / demoda düzeltme yapmış olabilir.
- **Telif ihlali:** Ham videoyu dağıtmadan özet üret; politika ihlali yok.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [YouTube Data API — captions](https://developers.google.com/youtube/v3/docs/captions) — yetkili erişim gereksinimleri
- [WebVTT spec](https://www.w3.org/TR/webvtt1/) — zaman formatı
