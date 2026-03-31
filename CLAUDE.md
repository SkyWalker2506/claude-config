# claude-config — Yonetici

Bu klasor Claude Code konfigurasyonunun **kaynak reposudur**. Buraya girince yonetici moduyla calisirsin: skill duzenleme, global config guncelleme, yeni skill ekleme, migration guide guncelleme.

---

## Bu repo ne yapar

`install.sh` calistirinca:
- `global/` → `~/.claude/` (CLAUDE.md, settings.json, skills/)
- `projects/` → `$PROJECTS_ROOT/` (CLAUDE.md, MIGRATION_GUIDE.md, scripts/)
- Hardcoded path'ler otomatik degistirilir

## Dosya yapisi

```
global/           → ~/.claude/ altina yuklenir
  CLAUDE.md       → Global talimatlar (tum projeler icin)
  settings.json.template → MCP, izinler, hook (path placeholder'li)
  skills/         → /refine, /audit, /index, /web-research vb.

projects/         → Proje kok dizinine yuklenir
  CLAUDE.md       → Ortak gelistirme kurallari (framework-agnostik)
  MIGRATION_GUIDE.md → Yeni proje setup wizard
  scripts/        → Hook script'leri

templates/        → Yeni proje sablonlari (/migration setup kullanir)
```

## Degisiklik yapinca

1. Bu repodaki dosyayi duzenle (orn. `global/skills/audit/SKILL.md`)
2. `./install.sh` calistir → degisiklikler yerlerine kopyalanir
3. Commit + push → diger PC'lerde `git pull && ./install.sh`

## Yeni skill ekleme

```bash
mkdir -p global/skills/yeni-skill
# global/skills/yeni-skill/SKILL.md olustur
./install.sh  # → ~/.claude/skills/yeni-skill/ olusur
```

## Migration guncelleme

1. `projects/MIGRATION_GUIDE.md` → Changelog'a yeni versiyon ekle
2. `projects/MIGRATION_VERSION` → versiyon numarasini artir
3. `./install.sh` → degisiklikler tasinir
4. Diger projelerde `claude` acinca `MIGRATION_UPDATE` sinyali gelir → delta otomatik uygulanir
