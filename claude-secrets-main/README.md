# claude-secrets (private)

Bu repo Claude Code'un ihtiyac duydugu API key, token ve credential'lari saklar.
`claude-config/install.sh` bu repoyu otomatik clone/pull eder.

## Dosyalar

- `secrets.env` — Tum secret'lar (key=value formati)
- `*.json` — Service account dosyalari (Firebase vb.)

## Kullanim

Bu repoyu elle duzenlemenize gerek yok.
`install.sh` calistirinca otomatik yuklenir.

Degisiklik yapmak icin:
```bash
nano ~/.claude/secrets/secrets.env
cd ~/.claude/secrets && git add -A && git commit -m "update" && git push
```
