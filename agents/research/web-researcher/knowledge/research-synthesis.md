---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Research Synthesis

## Quick Reference

| Aşama | Soru | Çıktı |
|-------|------|-------|
| **Scope** | Kullanıcı ne karar verecek? | Soru cümlesi |
| **Harvest** | Hangi kaynak türleri gerekli? | Kaynak listesi |
| **Extract** | Tekrarlayan tema? | Bullet bulgular |
| **Synthesize** | Çelişki var mı? | Birleşik görüş + güven bandı |
| **Deliver** | Eylem önerisi? | Özet + next steps |

```text
Güven bandı: HIGH (≥2 bağımsız T0/T1) | MEDIUM | LOW (tek T2 veya çelişkili)
```

## Patterns & Decision Matrix

| Rapor türü | Yapı | Uzunluk rehberi |
|------------|------|-----------------|
| Executive brief | Bulgu → risk → öneri | 1 sayfa |
| Teknik derinlik | Bağlam → detay → alternatifler | Çok bölüm |
| Karşılaştırma | Matris + kazanan kriterleri | Tablo ağırlıklı |

**Karar:** Her ana bulgu için en az bir “so what?” cümlesi; yoksa kes.

## Code Examples

**Sentez blok şablonu:**

```markdown
## Synthesis
**Question:** …
**Consensus:** … (confidence: MEDIUM)
**Dissent:** … — sources: …
**Recommendation:** …
**Open gaps:** …
```

## Anti-Patterns

- **Kopyala-yapıştır derleme:** Aynı cümleyi üç kaynaktan üst üste koyma; tek paragrafta birleştir.
- **Kaynak sayısını kalite sanmak:** 10 zayıf blog yerine 2 güçlü kaynak.
- **Sonuçsuz özet:** Okuyucu “ne yapmalıyım?” bilmiyorsa başarısız.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [PRISMA (systematic reviews)](http://www.prisma-statement.org/) — yapılandırılmış literatür sentezi
- [Evidence synthesis basics — Cochrane intro](https://www.cochrane.org/) — sağlık odaklı ama metod genel
