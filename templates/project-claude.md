# __PROJECT_NAME__ — Claude Code

Genel kurallar (calisma tarzi, tool-first, maliyet, dil, model, hata yonetimi) `~/.claude/CLAUDE.md` ve ust dizin `CLAUDE.md`'den devralinir. Bu dosya **yalnizca projeye ozel** kurallari icerir.

---

## 1. Framework ve komutlar

- **Framework:** __FRAMEWORK__
- **Paket yoneticisi:** __PKG_MANAGER__
- **Test:** __TEST_CMD__
- **Lint:** __LINT_CMD__

### Commit oncesi

```bash
__PKG_MANAGER__ → __LINT_CMD__ → __TEST_CMD__
```

---

## 2. Jira (varsa)

- **Proje anahtari:** __JIRA_KEY__
- Detay: `docs/CLAUDE_JIRA.md`

---

## 3. Notlar

Projeye ozel kurallar, ozel dosya yapisi, dikkat edilecekler buraya yazilir.
