---
last_updated: 2026-04-10
refined_by: composer-2
confidence: high
sources: 4
---

# Ethics, platform safety, and contests

## Quick Reference

| Konu | Kural |
|------|--------|
| **Yanıltıcı kanca** | İçerik vaadi ile uyumlu olmalı |
| **Yarışma / çekiliş** | Meta / TikTok / X — bölge ve şeffaflık kuralları |
| **Minors** | Çocuk içeriği — platform özel politikalar |
| **Sağlık / finans** | Aşırı iddia — düzeltme ve kaynak |

H12 manipülatif nefret, zarar veya sahte aciliyet üretmez.

## Patterns & Decision Matrix

| Format | Risk |
|--------|------|
| “Son şans” sayımı | Gerçek bitiş tarihi yoksa yasak his |
| Kullanıcı içeriği yeniden paylaşım | İzin + etiket |
| Ödüllü challenge | Kurallar sabit landing’de |

## Code Examples

**Yarışma disclosure şablonu (caption altı):**

```text
Ödül: [ürün / kupon]. Son katılım [UTC tarih]. Kazanan [X] gün içinde DM ile duyurulur.
Bu kampanya [Marka] tarafından yürütülür; [Platform] sponsor değildir.
```

**A/B test etik notu (iç doküman):**

```yaml
experiment: hook_set_q2
hypothesis: "İlk satırda sayı kullanımı kaydetmeyi artırır"
guardrails:
  - no_health_claims
  - no_targeting_protected_classes
success_metric: saves_per_1k_impressions
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Sahte sosyal kanıt | Hesap kapatma |
| Etiket olmadan ücretli ortaklık | FTC / yerel reklam ihlali |
| Hassas konularda şok görsel | Platform removal |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Meta — Promotions rules](https://www.facebook.com/business/help/)
- [FTC — Endorsement guides](https://www.ftc.gov/legal-library/browse/federal-register-notices/guides-concerning-use-endorsements-testimonials-advertising)
- [TikTok — Branded content](https://www.tiktok.com/creators/creator-portal/)
- [X — Paid partnership](https://help.x.com/en/rules-and-policies)
