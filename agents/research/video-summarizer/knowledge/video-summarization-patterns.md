---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Video Summarization Patterns

## Quick Reference

| Pattern | Ne zaman | Çıktı |
|---------|----------|-------|
| **Section chunking** | Uzun konuşma | Bölüm başlıkları |
| **Key claim extraction** | Argüman videosu | Numaralı iddialar |
| **Demo timeline** | Eğitim | Adım listesi |
| **Q&A pullout** | Panel | Soru → cevap çiftleri |

```text
Özet katmanları: ultra_short (3 cümle) | structured (bullets) | deep (bölüm + alıntı)
```

## Patterns & Decision Matrix

| İçerik türü | Odak |
|-------------|------|
| Haber | 5W1H |
| Tutorial | Komut / dosya adları |
| Röportaj | İsim ve rol doğruluğu |

**Karar:** “Deep” özet isteniyorsa önce bölüm sınırlarını çıkar (sessizlik veya konu değişimi).

## Code Examples

**Özet başlığı:**

```text
[VIDEO SUMMARY] title=… | duration=… | pattern=section_chunking
## Chapters
1. … (0:00–4:00)
2. …
## Key claims
- …
```

## Anti-Patterns

- **İlk 2 dakikaya takılmak:** Intro sponsor olabilir.
- **Spekülasyonu fact sanmak:** “I think” cümlelerini işaretle.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- Konuşma özetleme araştırma özetleri — ACL / arXiv (speech summarization)
- Video platform içerik politikaları — özet dağıtım kuralları
