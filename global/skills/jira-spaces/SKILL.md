---
name: jira-spaces
description: "Jira'daki tüm projeleri açık task sayısıyla listele. Triggers: jira-spaces, jira projeleri, proje listesi, hangi projeler var, spaces."
argument-hint: "[]"
---

# /jira-spaces — Jira Proje Listesi

`mcp__atlassian__getVisibleJiraProjects` ile tüm projeleri çek, her biri için açık task sayısını al, tablo göster.

## Akış

1. Tüm projeleri çek
2. Her proje için: `project = {KEY} AND status != Done` JQL ile açık task sayısı al
3. Açık task sayısına göre sırala (çok → az), 0 olanlar en alta

## Çıktı

```
| Proje           | Key  | Açık |
|-----------------|------|------|
| Vocab           | VOC  | 294  |
| ApApp           | AC   | 123  |
| ...             | ...  | ...  |
```

## Kurallar
- Max 10 tool call
- 0 açık task'lı projeler en alta
