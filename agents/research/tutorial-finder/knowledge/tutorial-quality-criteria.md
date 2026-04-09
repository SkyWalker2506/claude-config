---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Tutorial Quality Criteria

## Quick Reference

| Boyut | İyi işaret | Kırmızı bayrak |
|-------|------------|----------------|
| **Güncellik** | Son 12 ay veya sürüm notu | Eski API, kaldırılmış komut |
| **Derinlik** | Çalışan repro, edge case | Sadece “copy hello world” |
| **Netlik** | Önkoşullar listelenmiş | Belirsiz “bazı araçlar” |
| **Bakım** | Issue cevapları, yorum güncellemesi | Ölü repo linki |

```text
Skor: 1–5 veya PASS / REVIEW / REJECT + gerekçe
```

## Patterns & Decision Matrix

| Tür | Ağırlık |
|-----|---------|
| Resmi doc tutorial | Yüksek güven |
| Üçüncü parti blog | Kod örneği doğrulanmalı |
| Video-only | Transkript veya K5 özet şart (referans) |

**Karar:** “PASS” için çoğu kriter yeşil; tek kritik kırmızı (güvenlik) → REJECT.

## Code Examples

**Değerlendirme satırı:**

```text
[TUTORIAL QA] url=… | score=4/5 | freshness=ok | tested_repro=no | verdict=REVIEW
```

## Anti-Patterns

- **Yıldız / view saymak:** Popülerlik kalite değil.
- **Tek platform:** Mobil/desktop farkını görmezden gelme.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- Diátaxis — tutorial vs how-to ayrımı
- Proje resmi “getting started” sayfaları
