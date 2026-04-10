---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Multi-Channel Adaptation

## Quick Reference

| Kanal | Uyarlama |
|-------|----------|
| **LinkedIn** | Paragraf aralığı, ilk cümle hook, profesyonel ton |
| **X / Threads** | Kısa zincir; tek fikir per post |
| **YouTube** | Başlık + thumb + ilk 30 sn teklif |
| **E-posta** | Tek konu, tek CTA |
| **Slack / Discord** | Mention ve kanal kültürü — kısa özet + link |

**Başlık uzunluğu ve görsel oranları** kanala göre değişir — “resize” yetmez, **yeniden kurgu** gerekir.

## Patterns & Decision Matrix

| Kontrol listesi | Soru |
|-----------------|------|
| Ton | Resmî / samimi — marka sesi |
| CTA | Kanalda izin verilen link türü |
| Yasal | Finans veya sağlık iddiası — uyarı gerekiyor mu |

### Yerelleştirme

- Dil, para birimi, örnek müşteri — bölgeye özgü

## Code Examples

### Örnek: tek mesaj, üç kanal

```text
Core claim: "Cut ad-hoc SQL requests by 60% in 90 days."

- Email: subject + 4 bullets + PS with case study
- X/Twitter: 240 chars + link to thread
- Slack customer: 2 sentences + link to Loom walkthrough
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Blog’u e-postaya yapıştır | Okunmaz |
| Video’yu transkriptsiz kısaltmak | Erişilebilirlik eksik |
| Her kanalda aynı saatte | Hedef kitle farklı |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Nielsen Norman Group — omnichannel](https://www.nngroup.com/) — UX tutarlılığı
- [Google — E-E-A-T](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) — güvenilir içerik
- [W3C — WCAG](https://www.w3.org/WAI/WCAG21/quickref/) — erişilebilir içerik
- [CAN-SPAM / GDPR context](https://ico.org.uk/for-organisations/guide-to-data-protection/) — e-posta (bölgeye göre)
