# Global Claude — Yonlendirici

> **Bu dosya sadece yonlendiricidir.** Tum kurallar, skill tanimlari ve konfigürasyon detaylari `~/Projects/claude-config/CLAUDE.md` dosyasindadir.

---

## Her oturum basinda

1. **`~/Projects/claude-config/CLAUDE.md` dosyasini oku** ve talimatlarini uygula — bu okuma yapilmadan hicbir kural uygulanmaz ve hicbir kod yazilmaz
2. Yanit basinda etiket: `(Jarvis)` — Sonnet disindaysa model adini ekle: `(Jarvis | Opus 4.6)`
3. Dil: kullaniciya Turkce; kod/commit Ingilizce

## Config degisikligi

Degisiklik yapmak icin `~/Projects/claude-config/` reposunda duzenle → `./install.sh` calistir.
**`~/.claude/` altindaki dosyalari dogrudan duzenleme** — `install.sh` ile ezilir.

## Migration sinyalleri

| Sinyal | Aksiyon |
|--------|---------|
| `INSTALL_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` |
| `MCP_SETUP_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` |
| `MIGRATION_NEEDED` | `/migration` calistir |
| `MIGRATION_UPDATE` | Delta uygula, versiyon guncelle |
| `SECRETS_MISSING` | `~/.claude/secrets/secrets.env` duzenle |
| `SECRETS_NONE` | `install.sh` calistir veya secrets.env olustur |
| `CONFIG_UPDATE` | Kullaniciya sor: git pull + install.sh |
| `BIND_NEEDED` | `/bind` calistir — claude-config baglantisi kur |

## Secrets

- Secret degerleri **ASLA** konusma ciktisina, commit'e, public dosyaya veya log'a yazilmaz
- Secret'lar yalnizca `~/.claude/secrets/` altinda
