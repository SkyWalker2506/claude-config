---
last_updated: 2026-04-09
confidence: high
sources: 3
---

# Skill Level Matching

## Quick Reference

| Seviye | Tanım sinyali | Uygun içerik |
|--------|---------------|--------------|
| **Beginner** | Terim sözlüğü gerekir | Kurulum, ilk proje |
| **Intermediate** | Bir dil/çatı biliyor | Desenler, hata ayıklama |
| **Advanced** | Üretim deneyimi | Performans, güvenlik, mimari |
| **Expert** | Sınırları zorlama | RFC, katkı, özel derleyici |

```text
Eşleştirme: hedef_skill_vector - user_vector = gap → içerik seç
```

## Patterns & Decision Matrix

| Yanlış eşleme | Belirti |
|---------------|---------|
| Çok kolay | “Biliyorum” tekrarı |
| Çok zor | Takılma, jargon duvarı |

**Karar:** Şüphede bir seviye aşağı + “stretch” kaynak ekle.

## Code Examples

**Profil satırı:**

```text
[LEVEL] declared=intermediate | evidence: 2y prod Go | match_tutorials: [A, B] | stretch: [C]
```

## Anti-Patterns

- **Unvan ile seviye:** “Senior” her yerde aynı değil — kanıt iste.
- **Tek değerlendirme:** Öğrenme stili (video vs metin) farkını gör.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- SFIA / e-CF yetkinlik çerçeveleri — kurumsal seviye dil
- Bloom — bilişsel seviye ile içerik zorluğu
