---
name: suggest-plugins
description: "Projeyi tarayip uygun marketplace plugin'lerini oner. Triggers: suggest plugins, hangi plugin, plugin oner, plugin tavsiye."
argument-hint: ""
---

# /suggest-plugins — Plugin Recommender

Mevcut projeyi analiz edip Claude Code marketplace'den uygun plugin'leri oneriri.

## Akis

### 1. Proje tara (max 5 tool call)

Asagidakileri kontrol et:
- `pubspec.yaml` → Flutter projesi
- `package.json` → Node.js / Next.js
- `docs/CLAUDE_JIRA.md` veya Jira referansi → Jira kullanimi
- `.github/workflows/` → CI/CD var
- `firebase.json` veya `google-services.json` → Firebase
- `README.md` → proje tipi ve teknoloji stack

### 2. Oneri tablosu olustur

Tarama sonucuna gore uygun plugin'leri sec:

| Plugin | Ne zaman oner |
|--------|--------------|
| `code-quality` | Her zaman |
| `git-github` | Her zaman |
| `devtools-setup` | Her zaman |
| `flutter-firebase` | pubspec.yaml varsa |
| `jira-suite` | Jira referansi varsa |
| `sprint-planner` | Jira + agile referansi varsa |
| `research-tools` | README'de pazar/arastirma bahsi varsa |
| `autonomous-ops` | Buyuk/karmasik proje ise |
| `ai-review` | .github/workflows/ varsa |
| `telegram-bridge` | Uzaktan kontrol istiyorsa |
| `agent-browser` | Web scraping / e2e test varsa |
| `opencode-bridge` | Local model kullanimi varsa |
| `daily-check` | Uzun vadeli proje ise |

### 3. Cikti

```
## Plugin Onerileri — [proje adi]

### Kesinlikle ekle
- `code-quality` — kod audit, refine, memory-prune
- `git-github` — Git + GitHub MCP

### Proje icin uygun
- `flutter-firebase` — pubspec.yaml bulundu
- `jira-suite` — docs/CLAUDE_JIRA.md bulundu

### Ihtiyac olursa
- `autonomous-ops` — /yolo ve /team-build modlari

Kurmak icin:
claude plugin install <plugin-adi>@musabkara-claude-marketplace
```

## Kurallar

- Sadece oner, kur + onay al
- Zaten yuklu olanlari listeden cikar (mcp.json veya .claude-plugin/ kontrol)
- Max 5 tool call
