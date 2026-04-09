---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Meeting Note Templates

## Quick Reference

**Çekirdek bölümler:** Bağlam → Gündem → Tartışma özeti → Kararlar → Aksiyonlar → Sonraki toplantı. **DACI:** Driver, Approver, Contributor, Informed — karar kutusunda yaz.

| Süre | Şablon derinliği |
|------|------------------|
| ≤15 dk | Sadece karar + aksiyon |
| 30–60 dk | Tartışma maddeleri + risk |

```text
Dosya adı: YYYY-MM-DD-<slug>-notes.md veya Confluence sayfa başlığı ile eşleşen
```

## Patterns & Decision Matrix

| Stil | Artı | Eksi |
|------|------|------|
| Cornell tarzı (not / ipuçları / özet) | Öğrenme | Toplantıda yavaş |
| Sadece karar kaydı | Hızlı | Bağlam kaybolur |
| Tam transkript + özet | Denetlenebilir | Uzun |

**L6 ↔ L2:** Gündem L2’den kopyalanır; notlar `## Agenda alignment` ile başlar.

## Code Examples

**Markdown şablon:**

```markdown
# Decision workshop — 2026-04-10

**Attendees:** @alice @bob @carol  
**DACI:** Driver @alice · Approver @bob

## Context
Problem: API v1 sunset timeline unclear.

## Decisions
1. Sunset **2026-09-01** — approved by @bob
2. Comms owner: @carol — draft by 2026-04-20

## Action Items
| ID | Owner | Due | Task |
|----|-------|-----|------|
| A1 | @carol | 2026-04-20 | Customer email draft |
| A2 | @alice | 2026-04-15 | Error metrics export |

## Next meeting
2026-04-24 10:00 ET — review comms
```

**Confluence wiki markup (kısa):**

```text
h1. Team Sync 2026-04-10
{panel:title=Decision|borderStyle=solid}
We will deprecate v1 on 2026-09-01.
{panel}
```

## Anti-Patterns

- **Verbata tartışma yazmak:** Özet + doğrudan alıntı (riskli) ayrımı yap.
- **Karar yok "sync":** Karar kutusu boşsa "No decisions — parking lot" yaz.
- **Katılımcı listesi eksik:** RACI takip edilemez.
- **Aksiyon sahibi @everyone:** Her aksiyon tek isim.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Atlassian — meeting notes](https://www.atlassian.com/team-playbook/plays/meeting-notes) — oyun kitabı
- [Amazon — narrative memos](https://www.aboutamazon.com/news/company-news/amazon-shareholder-letters) — yazılı bağlam kültürü (referans)
- [Minto — SCQA](https://www.amazon.com/Minto-Pyramid-Principle-Logic-Writing/dp/0273710516) — yapı
