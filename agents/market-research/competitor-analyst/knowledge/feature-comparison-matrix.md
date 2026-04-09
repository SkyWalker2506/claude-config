---
last_updated: 2026-04-09
refined_by: mega-rollout
confidence: high
sources: 4
---

# Feature Comparison Matrix

## Quick Reference

| Sütun türü | Anlam |
|------------|--------|
| **Must-have** | Satın alma için kritik (deal-breaker) |
| **Differentiator** | Satışta öne çıkan 2–3 özellik |
| **Table stakes** | Herkesde var; eksikse güven kaybı |
| **Roadmap signal** | Beta, “coming soon”, iş ilanından çıkan |

**Ölçek:** `Yes` / `Partial` / `No` / `Unknown` — Unknown’u gizleme; araştırma görevi olarak işaretle.

## Patterns & Decision Matrix

### Matris şablonu

| Özellik | Ağırlık (1–5) | Biz | R1 | R2 | R3 | Not |
|---------|---------------|-----|----|----|-----|-----|
| SSO / SCIM | 5 | | | | | |
| API rate limit | 3 | | | | | |

**Ağırlık kaynağı:** Müşteri görüşmesi > satış kaybı nedeni > ürün varsayımı.

| Durum | Yorum |
|-------|--------|
| Partial yaygın | Entegrasyon derinliği veya sürüm farkı netleştir |
| Hepsi Yes | Fiyat veya güven / marka ile rekabet |

## Anti-Patterns

| Hata | Sonuç |
|------|--------|
| 50+ satır özellik listesi | Okunamaz; karar yok |
| Pazarlama isimleriyle karşılaştırma | Aynı özelliği iki kez saymak |
| Güncel olmayan doküman | Yanlış kazan/kaybet analizi |

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [G2 — Grid & comparison](https://www.g2.com/compare) — kategori karşılaştırma UI mantığı
- [Capterra — feature filters](https://www.capterra.com/) — özellik etiketleme örnekleri
- [Product Marketing Alliance — competitive intel](https://productmarketingalliance.com/) — battlecard kültürü
- [Pragmatic Institute — competitive analysis](https://www.pragmaticinstitute.com/resources/) — PMM çerçeveleri
