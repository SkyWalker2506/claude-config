# claude-config

Tasinabilir Claude Code konfigurasyonu. Clone + `install.sh` ile herhangi bir Mac/Linux'ta calisir hale gelir.

## Ne yapar

- `~/.claude/` altina global talimatlar, 18 skill, MCP ayarlari ve hook'lari kurar
- Proje kok dizinine (`~/Projects/` vb.) ortak kurallar, migration sistemi ve script'leri yazar
- Yeni projelerde `claude` acinca otomatik setup wizard tetiklenir
- Hardcoded path yok — her sey `install.sh` ile hedef PC'ye uyarlanir
- OpenCode (Claude’dan bagimsiz terminal asistani): Ollama ile ucretsiz lokal modeller — ilk `install.sh` calistirmasinda `~/.config/opencode/opencode.json` sablonu (dosya yoksa)

## Kurulum

```bash
git clone https://github.com/SkyWalker2506/claude-config.git ~/Projects/claude-config
cd ~/Projects/claude-config
./install.sh
# OpenCode CLI de kurulsun (npm global, paket: opencode-ai):
# ./install.sh --opencode
```

Installer soracak:
1. **Proje kok dizini** (default: `~/Projects`)
2. **Secrets vault** — sahipsen otomatik cekilir, degilsen elle girersin veya kendi private reponun URL'sini verirsin
3. **uvx yolu** otomatik bulunur (jCodeMunch MCP icin)

Mevcut `~/.claude/` varsa `~/.claude.backup.<tarih>` olarak yedeklenir.

## Geri alma

```bash
./uninstall.sh
```

En son yedegi bulur ve geri yukler.

## Dosya yapisi

```
claude-config/
├── install.sh                 # Tek komutla kurulum
├── uninstall.sh               # Yedekten geri yukle
├── CLAUDE.md                  # Bu reponun yonetici talimatlari
├── global/
│   ├── CLAUDE.md              # → ~/.claude/CLAUDE.md
│   ├── settings.json.template # → ~/.claude/settings.json
│   └── skills/                # → ~/.claude/skills/ (18 skill)
│       ├── refine/            #   Konfigürasyon temizleme
│       ├── index/             #   jCodeMunch indexleme
│       ├── audit/             #   Kod taramasi
│       ├── migration/         #   Proje setup wizard
│       ├── web-research/      #   Web arastirmasi
│       ├── jira-run/          #   Jira izleme dongusu
│       ├── jira-run-fast/     #   Hizli Jira dongusu
│       ├── jira-run-detailed/ #   Detayli Jira analiz
│       ├── jira-cancel/       #   Jira dongu iptal
│       ├── jira-start-new-task/ # Yeni Jira gorev
│       ├── rbg/               #   Arka plan delegasyonu
│       ├── decide/            #   WAITING karar verme
│       ├── dashboard/         #   Terminal dashboard
│       ├── dashboard-sync/    #   Dashboard Jira sync
│       ├── project-analysis/  #   12 kategori derin audit
│       ├── sprint-plan/       #   Sprint planlama
│       ├── agent-browser/     #   Tarayici ajanı
│       └── agent-browser/     #   Browser automation
├── projects/
│   ├── CLAUDE.md              # → $PROJECTS_ROOT/CLAUDE.md
│   ├── MIGRATION_GUIDE.md     # → Setup wizard + changelog
│   ├── MIGRATION_VERSION      # → Versiyon numarasi (2.0)
│   ├── PROJECT_ANALYSIS.md    # → Analiz sablonu
│   └── scripts/
│       └── migration_check.sh # → Hook: sinyal uretici
└── templates/
    ├── project-claude.md      # Yeni proje CLAUDE.md sablonu
    └── project-settings.json  # Yeni proje settings sablonu
```

## Nasil calisir

### 3 katmanli CLAUDE.md hiyerarsisi

```
~/.claude/CLAUDE.md          ← Global (tum projeler)
~/Projects/CLAUDE.md         ← Ortak kurallar (framework-agnostik)
~/Projects/MyApp/CLAUDE.md   ← Projeye ozel (framework, komutlar, Jira)
```

Claude Code bunlari otomatik birlestirir. Ustten alta oncelik artar.

### Otomatik proje kurulumu

1. Yeni bir proje dizininde `claude` ac
2. `migration_check.sh` hook'u otomatik calisir
3. **MIGRATION_NEEDED** sinyali uretilir
4. Claude setup wizard'i baslatir, framework/test/lint sorar
5. Proje CLAUDE.md ve settings.json olusturulur

### Migration sistemi

Config repo guncellendikten sonra (`git pull && ./install.sh`):
- Projelerde `claude` acinca **MIGRATION_UPDATE** sinyali gelir
- Delta adimlar otomatik uygulanir
- Proje versiyonu guncellenir

### MCP (tek kaynak)

Tum MCP tanimlari `~/.claude/settings.json` icinde. Projeler `enabledMcpjsonServers` ile sadece hangi MCP'leri kullanacagini secer. Duplikasyon yok.

## Yeni proje ekleme

```bash
cd ~/Projects/YeniProje
claude
# → MIGRATION_NEEDED tetiklenir
# → /migration setup ile interaktif kurulum
```

Veya manuel:
```bash
mkdir -p .claude
cp ~/Projects/.claude-templates/project-claude.md CLAUDE.md
cp ~/Projects/.claude-templates/project-settings.json .claude/settings.json
# Placeholder'lari duzenle
```

## Secrets vault

API key ve token'lar private bir git reposunda saklanir (`~/.claude/secrets/`).

| Durum | Ne olur |
|-------|---------|
| Repo sahibi, yeni PC | `gh api user` ile otomatik tespit → `claude-secrets` clone edilir |
| Baska kullanici | URL sorar veya elle giris + kendi private reposunu olusturur |
| Mevcut secrets var | `git pull` ile gunceller |

Secret'lar asla public repoya girmez. `secrets.env` dosya izni 600.

## Baska PC'ye tasima

```bash
# Yeni PC'de:
git clone https://github.com/SkyWalker2506/claude-config.git ~/Projects/claude-config
cd ~/Projects/claude-config
./install.sh

# Mevcut projeler icin:
cd ~/Projects/MevcutProje
claude
# → MIGRATION_NEEDED tetiklenir, setup wizard baslar
```

## Degisiklik yapma

1. `claude-config/` icindeki dosyayi duzenle
2. `./install.sh` calistir (degisiklikler kopyalanir)
3. `git add . && git commit && git push`
4. Diger PC'lerde: `git pull && ./install.sh`

## Skill listesi

| Skill | Aciklama |
|-------|----------|
| `/refine` | Config dosyalarini tara, temizle (project/global/all) |
| `/index` | jCodeMunch indexleme + marker |
| `/audit` | Kod taramasi (security, cost, performance, cleanup, all) |
| `/migration` | Yeni proje interaktif setup |
| `/web-research` | Web arastirmasi (competitors, reviews, trends, ux...) |
| `/jira-run` | Jira wait-and-check dongusu |
| `/jira-run-fast` | Hizli Jira dongusu (1s aralik) |
| `/jira-run-detailed` | Detayli Jira analiz (security, ux, performance...) |
| `/jira-cancel` | Jira dongusunu iptal et |
| `/jira-start-new-task` | Yeni Jira gorev olustur |
| `/rbg` | Arka plan delegasyonu |
| `/decide` | WAITING kartlarinda hizli karar |
| `/dashboard` | Terminal dashboard (cache) |
| `/dashboard-sync` | Dashboard + Jira sync |
| `/project-analysis` | 12 kategori derin audit |
| `/sprint-plan` | Sprint planlama + Jira task |
| `/agent-browser` | Tarayici ajani |
| `/opencode` | OpenCode + Ollama — Claude kotasi bitince lokal ucretsiz model |

OpenCode kullanimi: [Ollama](https://ollama.com) kur, `ollama pull qwen2.5-coder:7b`, proje dizininde `opencode`. Ayrinti: `/opencode` skill.
