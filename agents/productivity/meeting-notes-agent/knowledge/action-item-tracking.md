---
last_updated: 2026-04-09
refined_by: composer-2
confidence: high
sources: 3
---

# Action Item Tracking

## Quick Reference

**Alanlar:** `id`, `title`, `owner`, `due`, `status` (`open|blocked|done`), `source_meeting`, `blocked_by`. **SLA:** due geçince `overdue=true`; günlük özet L3’e beslenebilir.

| Durum | Anlam |
|-------|-------|
| open | Aktif |
| blocked | Bağımlılık veya kaynak yok |
| done | Tamamlandı — tarih ve kanıt linki |

```text
ID format: A-{meetingDate}-{seq} örn. A-20260410-01
```

## Patterns & Decision Matrix

| Araç | Artı | Eksi |
|------|------|------|
| Markdown tablo + Git | Sürüm kontrolü | Otomasyon az |
| Jira / Linear | İş akışı | Bağlam iki yerde |
| Notion DB | Esnek | Export karmaşık |

**I9 retrospective ile fark:** I9 takım süreci; L6 toplantı çıktısı odaklı.

## Code Examples

**CSV dışa aktarım (Jira içe aktarım için):**

```csv
Summary,Assignee,Due date,Description
Customer comms draft,carol@co.com,2026-04-20,From meeting 2026-04-10
```

**YAML aksiyon listesi:**

```yaml
actions:
  - id: A-20260410-01
    title: Export error metrics
    owner: alice@co.com
    due: 2026-04-15
    status: open
    evidence_url: null
```

**Blokaj notu:**

```text
[A-20260410-02] BLOCKED — waiting on Legal review (ticket LEG-88)
```

## Anti-Patterns

- **Sahipsiz aksiyon:** Default owner yoksa "TBD" + L3'te üst sıra uyarı.
- **Done without evidence:** Link veya kısa tamamlanma notu.
- **Aynı aksiyon iki toplantıda farklı due:** Tek kanonik kayıt; eski due `superseded`.
- **100+ açık aksiyon:** Haftalık kapatma seansı öner.

## Deep Dive Sources

> Agent derine inmesi gerekirse bu kaynaklardan fetch eder:

- [Jira — importing CSV](https://support.atlassian.com/jira-cloud-administration/docs/import-issues-from-a-csv-file/) — toplu oluşturma
- [Linear — issue API](https://developers.linear.app/docs/graphql/working-with-the-graphql-api) — programatik
- [GTD — next actions](https://gettingthingsdone.com/) — tek sonraki eylem disiplini
