---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Asset Store Evaluation

## Quick Reference

| Kriter | Soru |
|--------|------|
| Destek | Son güncelleme, yorum |
| Uyumluluk | Unity sürüm aralığı |
| Boyut | İndirme + build etkisi |
| Dokümantasyon | Örnek sahne var mı |

## Patterns & Decision Matrix

| Tür | Ek |
|------|-----|
| Kod tabanlı | API yüzeyi incele |
| Saf içerik | Lisans + kalite |

## Code Examples

```text
[EVAL] asset_id=… | unity=[2022.3,6000] | last_update=… | rating>=4.0 | risk=low|med|high
```

## Anti-Patterns

- Yıllardır güncellenmemiş bağımlılığı temel almak.

## Deep Dive Sources

- [Unity Asset Store](https://assetstore.unity.com/)
