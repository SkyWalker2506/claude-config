---
name: dashboard-sync
description: Jira MCP'den taze veri cek, cache'e yaz, sonra dashboard goster.
---

## /dashboard-sync

Jira'dan taze veri cek + dashboard goster.

## Uygulama

### 1. Jira'dan veri cek (paralel 2 cagri)

Proje anahtarini projenin `docs/CLAUDE_JIRA.md` veya `CLAUDE.md` dosyasindan oku (orn: VOC, AC, TASK).

- **Not-done:** `project = {KEY} AND status NOT IN ("Done") ORDER BY status ASC, priority DESC` — fields: summary, status, priority, labels — max 50
- **Done:** `project = {KEY} AND status = "Done" ORDER BY updated DESC` — fields: summary, status, priority — max 10

Sonuclar buyukse dosyaya duser; python3 ile parse et.

### 2. Cache yaz

Sonuclari parse et ve `.jira_cache.json`'a yaz:

```json
{
  "updated": "<ISO timestamp>",
  "summary": {"total": N, "todo": N, "in_progress": N, "waiting": N, "blocked": N, "backlog": N, "done": N},
  "todo": [{"key": "PROJECT-XX", "summary": "...", "priority": "High", "labels": [...]}],
  "in_progress": [...],
  "waiting": [...],
  "blocked": [...],
  "backlog": [...],
  "done_recent": [{"key": "PROJECT-XX", "summary": "..."}]
}
```

Status mapping:
- `"To Do"` → todo
- `"In Progress"` → in_progress
- `"WAITING FOR APPROVAL"` → waiting
- `"BLOCKED"` → blocked
- `"BACKLOG"` → backlog
- `"Done"` → done_recent (son 10)

done count icin: toplam not-done'u cik, veya done query totalCount kullan.

### 3. Dashboard goster

```bash
python3 scripts/dashboard.py
```

Ciktidan sonra ek aciklama YAZMA.
