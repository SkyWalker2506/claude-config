---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Segmentation Strategies

## Quick Reference

| Segment boyutu | Örnek |
|----------------|--------|
| **Demografik** | Ülke, dil |
| **Davranışsal** | Son satın alma, site ziyareti, ürün kullanımı |
| **Yaşam döngüsü** | Deneme, aktif, uyku, churn riski |
| **İzin** | Çift opt-in, tercih merkezi |

**KVKK/GDPR:** Segmentasyon için gerekli veri işleme amacı ve saklama süresi dokümante.

## Patterns & Decision Matrix

| Senaryo | Strateji |
|---------|----------|
| B2B | Rol (economic buyer vs. user) |
| E-ticaret | Sepet terk, yeniden stok |
| İçerik | Konu tercihleri — self-segmentation |

### Test

- Aynı kampanyayı segment A/B ile — ölçülebilir öğrenme

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Aşırı ince segment (N küçük) | İstatistik anlamsız |
- Hassas sağlık/politik ayrımı | Etik + hukuk riski |
| Statik segmentler | Davranış değişince güncellenmez |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [HubSpot — segmentation](https://www.hubspot.com/products/marketing/segmentation) — ürün bağlamı
- [Salesforce — Marketing Cloud segmentation](https://help.salesforce.com/) — kurumsal örnek
- [ICO — direct marketing](https://ico.org.uk/for-organisations/guide-to-pecr/electronic-mail-marketing/) — UK PECR
- [FTC — CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — ticari e-posta
