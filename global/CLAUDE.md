# Global Claude — Yonlendirici + Bootstrap

> **Bu dosya sadece yonlendiricidir.** Tum kurallar, skill tanimlari ve konfigürasyon detaylari `~/Projects/claude-config/CLAUDE.md` dosyasindadir.

---

## Bootstrap (ILKLEME — claude-config yoksa)

Asagidaki kontrolleri **her oturum basinda sirayla** yap. Herhangi biri basarisizsa o adimi calistir, sonraki adimlara gec.

### Adim 1: claude-config repo

```bash
# Kontrol
ls ~/Projects/claude-config/install.sh 2>/dev/null
```

**Yoksa:**
```bash
mkdir -p ~/Projects
cd ~/Projects
gh auth status 2>/dev/null || git clone https://github.com/SkyWalker2506/claude-config.git
gh auth status 2>/dev/null && gh repo clone SkyWalker2506/claude-config 2>/dev/null || git clone https://github.com/SkyWalker2506/claude-config.git
```

### Adim 2: Secrets

```bash
# Kontrol
ls ~/Projects/claude-config/claude-secrets/secrets.env 2>/dev/null
```

**Yoksa:**
```bash
cd ~/Projects/claude-config
gh auth status 2>/dev/null && gh repo clone SkyWalker2506/claude-secrets claude-secrets 2>/dev/null
```

gh auth yoksa kullaniciya bildir: "Secrets icin GitHub login gerekli. `! gh auth login --web -p https` calistir."

### Adim 3: install.sh

```bash
# Kontrol — settings.json ve skill'ler mevcut mu
ls ~/.claude/settings.json 2>/dev/null && ls ~/.claude/skills/ 2>/dev/null
```

**Yoksa veya eksikse:**
```bash
cd ~/Projects/claude-config && bash ./install.sh --auto --skip-login --stacks general
```

Kullaniciya stack sorusu sormadan `general` ile basla. Kurulum sonrasi `/restart` hatırlat.

### Adim 4: Normal akis

Bootstrap tamamsa asagidaki "Her oturum basinda" bolumune gec.

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
- Kanonik kaynak: `~/Projects/claude-config/claude-secrets/secrets.env`
- `~/.claude/secrets/secrets.env` bu dosyaya symlink (install.sh kurar)
