---
last_updated: 2026-04-10
refined_by: composer-2
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

## Code Examples

**ESP segment tanımı (pseudo — Iterable / Customer.io benzeri):**

```yaml
segment:
  name: trial_users_day7_no_convert
  rules:
    - event: trial_started
      within_days: 7
    - event: purchase_completed
      count: 0
  channels:
    email: true
    sms: false
```

**Warehouse SQL (BigQuery) — davranışsal segment:**

```sql
SELECT user_id
FROM analytics.events
WHERE event = 'pricing_page_view'
  AND ts > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 14 DAY)
  AND user_id NOT IN (SELECT user_id FROM billing.subscribers WHERE status = 'active');
```

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| Aşırı ince segment (N küçük) | İstatistik anlamsız |
| Hassas sağlık/politik ayrımı | Etik + hukuk riski |
| Statik segmentler | Davranış değişince güncellenmez |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [HubSpot — segmentation](https://www.hubspot.com/products/marketing/segmentation) — ürün bağlamı
- [Salesforce — Marketing Cloud segmentation](https://help.salesforce.com/) — kurumsal örnek
- [ICO — direct marketing](https://ico.org.uk/for-organisations/guide-to-pecr/electronic-mail-marketing/) — UK PECR
- [FTC — CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) — ticari e-posta
