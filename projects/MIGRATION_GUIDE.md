# Claude Code Project Migration Guide

<!-- MASTER_VERSION: 2.0 -->

Bu rehber, `__PROJECTS_ROOT__/` altindaki **tum projeler** icin ortak MCP, skill, hook, config ve kurulum yapisini tanimlar. Yeni bir proje acildiginda veya migration guncelleme sinyali geldiginde bu dosya izlenir.

> **Claude icin talimat:** `MIGRATION_NEEDED` sinyali aldiysan **Bolum 0**'i calistir. `MIGRATION_UPDATE` sinyali aldiysan **Changelog** bolumunu oku, yalnizca delta adimlarini uygula.

---

## Changelog

### v2.0 (2026-03-31) — Bulletproof refactor
- **MCP tek kaynak:** Tum MCP tanimlari yalnizca `~/.claude/settings.json`'da. Proje `.mcp.json` ve `~/.claude/mcp.json` **silindi**. Projeler `enabledMcpjsonServers` ile secim yapar.
- **Skills konsolidasyonu (35 → 18):** 10 `web-research-*` ve 10 `jira-run-detailed-*` varyanti silindi. Base skill'ler parametrik (`/web-research competitors`, `/jira-run-detailed security`).
- **3 katmanli CLAUDE.md:** `~/.claude/CLAUDE.md` (global) → `~/Projects/CLAUDE.md` (ortak) → `proje/CLAUDE.md` (ozel). Her katman sadece kendi sorumlulugunu tasir; tekrar yok.
- **Projects/CLAUDE.md framework-agnostik:** Flutter, Jira VOC, APK gibi proje detaylari cikarildi.
- **Watchdog §10 kaldirildi:** Karmasik Haiku→Opus zinciri pratikte calismiyor.
- **Hardcoded referanslar temizlendi:** audit, web-research, jira-run-detailed skill'lerindeki VocabLearningApp yollari ve VOC referanslari parametrik yapildi.
- **Yeni skill:** `/refine [global|all] [model]` — config dosyalarini rafine et.

**v1.0 → v2.0 delta adimlari:**
1. `~/.claude/mcp.json` sil (varsa)
2. Proje `.mcp.json` sil (varsa) — `enabledMcpjsonServers` yeterli
3. `~/.claude/skills/web-research-*/` dizinlerini sil (10 adet)
4. `~/.claude/skills/jira-run-detailed-*/` dizinlerini sil (10 adet)
5. `~/.claude/CLAUDE.md`'yi guncelle (yeni format: global kurallar + skill tablosu)
6. `~/Projects/CLAUDE.md`'yi guncelle (framework-agnostik ortak kurallar)
7. Proje `CLAUDE.md`'sindeki tekrar eden bolumleri cikar (global/ortak'tan devraliniyor)
8. `.claude/migration_version` → `2.0` yaz

### v1.0 (2026-03-30) — Ilk surum
- Interaktif setup wizard (Bolum 0)
- Global MCP, skill, hook altyapisi
- Versiyon karsilastirma sistemi kuruldu

> **Delta uygulama kurali:** Proje versiyonu ile master versiyon arasindaki TUM versiyonlarin degisikliklerini sirali uygula. Ornegin proje v1.0, master v1.2 ise: v1.1 deltalerini, sonra v1.2 deltelerini uygula.

---

## Icindekiler

0. [Interaktif Setup Wizard](#0-interaktif-setup-wizard)
1. [Onkoşullar](#1-onkosullar)
2. [MCP Sunuculari](#2-mcp-sunuculari)
3. [Claude Code Settings](#3-claude-code-settings)
4. [Skills (Slash Commands)](#4-skills-slash-commands)
5. [Hooks](#5-hooks)
6. [CLAUDE.md Dosyalari](#6-claudemd-dosyalari)
7. [Firebase Kurulumu](#7-firebase-kurulumu)
8. [CI/CD (GitHub Actions)](#8-cicd-github-actions)
9. [Scripts](#9-scripts)
10. [Environment Variables](#10-environment-variables)
11. [Jira Entegrasyonu](#11-jira-entegrasyonu)
12. [Projeye Ozel Degistirilecekler](#12-projeye-ozel-degistirilecekler)

---

## 0. Interaktif Setup Wizard

> **Claude icin ZORUNLU talimat:** Bu dosya yeni bir projede kurulum icin kullanildiginda, herhangi bir dosya olusturmadan ONCE asagidaki bilgileri kullanicidan topla. Kullanici "-" veya "yok" derse o servisi atla. Tum cevaplari aldiktan sonra dosyalari bu degerlere gore olustur.

### Adim 1 — Temel Proje Bilgileri (ZORUNLU)

Kullaniciya asagidaki soruları tek mesajda sor:

```
Yeni projeyi kurmak icin birkac bilgi lazim:

1. **Proje adi:** (orn. "MyApp", "TaskManager")
2. **Framework/dil:** (orn. Flutter, React, Python, Go)
3. **Paket yonetici:** (orn. flutter pub, npm, pip, go mod)
4. **Test komutu:** (orn. "flutter test", "npm test", "pytest")
5. **Lint komutu:** (orn. "flutter analyze", "eslint .", "ruff check .")
6. **Kullanici dili:** (orn. Turkce, Ingilizce)
7. **GitHub repo URL:** (orn. github.com/user/repo veya "henuz yok")
```

### Adim 2 — Servis Entegrasyonlari (OPSIYONEL)

Kullaniciya hangi servisleri kullanacagini sor:

```
Hangi servisleri kullanacaksiniz? (kullanmayacaklara "-" yazin)

8.  **Jira:** Proje anahtari? (orn. "VOC", "TASK")
9.  **Jira site:** (orn. "myteam.atlassian.net")
10. **Firebase:** Project ID? (orn. "myapp-12345")
11. **Firebase Android App ID:** (orn. "1:123:android:abc")
12. **Firebase iOS App ID:** (orn. "1:123:ios:abc")
13. **Telegram bot:** Token + Chat ID? (orn. "123:ABC, -100123")
14. **Google Drive:** Folder ID? (orn. "1AbC...")
15. **AdMob:** Kullanilacak mi? (E/H)
16. **RevenueCat:** Kullanilacak mi? (E/H)
```

### Adim 3 — Dosyalari Olustur

Kullanicinin cevaplarina gore asagidaki placeholder'lari degistir ve dosyalari olustur:

| Placeholder | Kaynak | Kullanildigi dosyalar |
|-------------|--------|----------------------|
| `PROJECT_NAME` | Soru 1 | CLAUDE.md, CI yml |
| `FRAMEWORK` | Soru 2 | CLAUDE.md, hooks |
| `PKG_MANAGER` | Soru 3 | CLAUDE.md, hooks, CI |
| `TEST_CMD` | Soru 4 | hooks, CI, CLAUDE.md |
| `LINT_CMD` | Soru 5 | hooks, CI, CLAUDE.md |
| `USER_LANG` | Soru 6 | CLAUDE.md |
| `GITHUB_REPO` | Soru 7 | .mcp.json, CI |
| `JIRA_PROJECT_KEY` | Soru 8 | skills, CLAUDE_JIRA.md, scripts |
| `JIRA_SITE` | Soru 9 | .env, scripts |
| `FIREBASE_PROJECT_ID` | Soru 10 | firebase.json, .env, CI |
| `FIREBASE_ANDROID_APP_ID` | Soru 11 | firebase.json, .env |
| `FIREBASE_IOS_APP_ID` | Soru 12 | firebase.json, .env |
| `TELEGRAM_BOT_TOKEN` | Soru 13a | .env |
| `TELEGRAM_CHAT_ID` | Soru 13b | .env |
| `GOOGLE_DRIVE_FOLDER_ID` | Soru 14 | .env |

### Olusturma Sirasi

```
1. .gitignore          — framework'e gore
2. CLAUDE.md           — proje adi, framework, test/lint, dil
3. .mcp.json           — yalnizca kullanilacak MCP'ler (proje duzeyinde override gerekiyorsa)
4. .claude/settings.json — yalnizca: enabledMcpjsonServers + framework hook
5. .env.example        — yalnizca kullanilacak servisler
6. firebase.json       — Firebase varsa
7. firestore.rules     — Firebase varsa
8. storage.rules       — Firebase varsa
9. .github/workflows/  — CI (framework'e gore test/lint komutu)
10. docs/CLAUDE_JIRA.md — Jira varsa (proje anahtari degistirilmis)
11. scripts/           — kullanilacak scriptler
```

> **Not:** `.claude/skills/` ARTIK GEREKMEZ — tum skill'ler `~/.claude/skills/` altinda global olarak yuklenir.

### Framework'e Gore Hook Sablonlari

| Framework | Stop Hook komutu |
|-----------|-----------------|
| Flutter | `flutter gen-l10n && flutter test` |
| React/Next.js | `npm run lint && npm test -- --watchAll=false` |
| Python | `ruff check . && pytest` |
| Go | `go vet ./... && go test ./...` |
| Rust | `cargo clippy && cargo test` |
| Node.js | `npm test` |

### Framework'e Gore .gitignore Temeli

| Framework | Eklenecekler |
|-----------|-------------|
| Flutter | `.dart_tool/`, `build/`, `/dist/`, `.flutter-plugins-dependencies`, `*.g.dart` |
| React | `node_modules/`, `.next/`, `dist/`, `.env.local` |
| Python | `__pycache__/`, `*.pyc`, `.venv/`, `dist/`, `*.egg-info/` |
| Go | `/bin/`, `/vendor/` (opsiyonel) |

### Ortak .gitignore (tum projeler)

```gitignore
# Claude Code
.mcp.json
.claude/settings.local.json
.jira-state/
.agent_locks/
.agent_progress.json
.worktrees/
.claude/worktrees/

# Environment
.env

# OS
.DS_Store
*.swp

# IDE
.idea/
.vscode/
.cursor/

# Runtime
*.log
*.pid

# Build output
/dist/
```

### Ornek Cikti

Kullanici asagidaki cevaplari verdiyse:

```
1. TaskManager
2. Flutter
3. flutter pub
4. flutter test
5. flutter analyze
6. Turkce
7. github.com/user/task-manager
8. TM
9. myteam.atlassian.net
10. taskmanager-abc12
11. 1:123:android:abc
12. -
13. -
14. -
15. H
16. H
```

Claude su dosyalari olusturur:
- `CLAUDE.md` → proje adi "TaskManager", test komutu "flutter test", Jira "TM"
- `.claude/settings.json` → yalnizca Flutter hooks + enabledMcpjsonServers (permissions global'den gelir)
- `.env.example` → yalnizca Firebase + Jira alanlari (Telegram/Drive/AdMob/RC yok)
- `firebase.json` → project ID "taskmanager-abc12", yalnizca Android (iOS yok)
- `.github/workflows/flutter_ci.yml` → Flutter CI
- **Skill'ler:** `~/.claude/skills/` altinda global — proje klasorune kopyalanmaz
- iOS bilgisi "-" oldugu icin firebase.json'da iOS bolumu ATLANIR
- Telegram/Drive "-" oldugu icin .env.example'da o satirlar OLMAZ

---

## 1. Onkosullar

### Global Araclar (bir kez kurulur)

```bash
# Node.js + npm (MCP sunuculari icin)
brew install node

# Python3 + uvx (jcodemunch, mcp-server-git icin)
brew install python3
pip3 install pipx
pipx ensurepath
pipx install uvx

# Flutter SDK
# https://docs.flutter.dev/get-started/install

# Firebase CLI
npm install -g firebase-tools
firebase login

# GitHub CLI
brew install gh
gh auth login
```

### Global Claude Config

**Dosya:** `~/.claude/settings.json`

> Ortak izinler, MCP tanimlari ve skill yolu burada — her proje otomatik devralir.

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "ask": [
      "Bash(git push --force*)", "Bash(git push -f *)",
      "Bash(rm -rf *)", "Bash(rm -fr *)",
      "Bash(gh repo delete*)", "Bash(shred *)"
    ],
    "allow": [
      "Bash(git *)", "Bash(flutter *)", "Bash(dart *)",
      "Bash(gh *)", "Bash(brew *)", "Bash(mkdir *)",
      "Bash(npm *)", "Bash(npx *)", "Bash(node *)", "Bash(tsx *)",
      "Bash(python3 *)", "Bash(python *)", "Bash(curl *)",
      "Bash(cp *)", "Bash(mv *)", "Bash(env *)", "Bash(open *)",
      "Read(~/.zshrc)"
    ]
  },
  "includeGitInstructions": true,
  "model": "sonnet",
  "effortLevel": "high",
  "voiceEnabled": true,
  "skipDangerousModePermissionPrompt": true,
  "mcpServers": {
    "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" } },
    "git": { "command": "/Users/KULLANICI/.local/bin/uvx", "args": ["mcp-server-git"] },
    "atlassian": { "command": "npx", "args": ["-y", "mcp-remote@latest", "https://mcp.atlassian.com/v1/mcp"] },
    "flutter-dev": { "command": "npx", "args": ["-y", "flutter-dev-mcp"] },
    "firebase": { "command": "npx", "args": ["-y", "@gannonh/firebase-mcp"],
      "env": { "SERVICE_ACCOUNT_KEY_PATH": "${FIREBASE_SERVICE_ACCOUNT_PATH}" } },
    "context7": { "command": "npx", "args": ["-y", "@upstash/context7-mcp"] },
    "jcodemunch": { "command": "/Users/KULLANICI/.local/bin/uvx", "args": ["jcodemunch-mcp"] }
  }
}
```

**Dosya:** `~/.claude/skills/`

> **Tum ortak skill'ler (jira-run, audit, dashboard, web-research vb.) burada — proje klasorlerine kopyalamak gerekmez.** Yeni proje acildiginda global skill'ler otomatik yuklenir. Skill ekleme/guncelleme sadece bu dizinde yapilir.

**Dosya:** `~/.claude/CLAUDE.md`

Global talimatlar dosyasi. Icerik projeye gore uyarlanir. Ornek:

```markdown
# Global Claude (tum projeler)

## Code exploration - jCodeMunch MCP
- `resolve_repo` ile calisma kokunu coz
- Kod arama/kesif icin jCodeMunch araclarini kullan
- Tam dosya okuma yalnizca gerektiginde

**Kurulum:** MCP command: `uvx`, args: `["jcodemunch-mcp"]`
```

---

## 2. MCP Sunuculari

### Proje seviyesi: `.mcp.json` (proje kokune kopyala)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "git": {
      "command": "/Users/KULLANICI/.local/bin/uvx",
      "args": ["mcp-server-git"]
    },
    "atlassian": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://mcp.atlassian.com/v1/mcp"]
    },
    "flutter-dev": {
      "command": "npx",
      "args": ["-y", "flutter-dev-mcp"]
    },
    "firebase": {
      "command": "npx",
      "args": ["-y", "@gannonh/firebase-mcp"],
      "env": {
        "SERVICE_ACCOUNT_KEY_PATH": "${FIREBASE_SERVICE_ACCOUNT_PATH}"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### MCP Aciklamalari

| MCP | Paket | Ne yapar | Gerekli env |
|-----|-------|----------|-------------|
| **github** | `@modelcontextprotocol/server-github` | PR, issue, repo islemleri | `GITHUB_TOKEN` |
| **git** | `mcp-server-git` | Git komutlari (status, diff, log, commit) | - |
| **atlassian** | `mcp-remote` + Atlassian URL | Jira/Confluence islemleri | Atlassian OAuth (ilk calistirmada) |
| **flutter-dev** | `flutter-dev-mcp` | Flutter build, analyze, test, hot reload | - |
| **firebase** | `@gannonh/firebase-mcp` | Firestore, Storage, Auth islemleri | `FIREBASE_SERVICE_ACCOUNT_PATH` |
| **context7** | `@upstash/context7-mcp` | Guncel kutuphane dokumantasyonu | - |

### Etkinlestirme

`.claude/settings.json` icinde hangi MCP'lerin aktif oldugunu belirt:

```json
{
  "enabledMcpjsonServers": ["github", "git", "atlassian", "context7", "firebase"]
}
```

### MODIFIYE: Projeye ozel

- `git` → `command` yolunu kendi `uvx` konumunuza guncelleyin (`which uvx`)
- `firebase` → `SERVICE_ACCOUNT_KEY_PATH` env degiskenini ayarlayin
- `github` → `GITHUB_TOKEN` env degiskenini ayarlayin
- Kullanmayacaginiz MCP'yi `enabledMcpjsonServers`'dan cikarin

---

## 3. Claude Code Settings

> **Mimari:** Ortak izinler (`permissions`), `includeGitInstructions` ve MCP tanimlari `~/.claude/settings.json`'da global olarak tanimlidir. Proje `settings.json`'u yalnizca proje ozgune ihtiyac duyulan alanlari icerir.

### Proje seviyesi: `.claude/settings.json` (minimal sablon)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "enabledMcpjsonServers": ["github", "git", "atlassian", "context7"],
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "flutter gen-l10n && flutter test",
            "async": true,
            "timeout": 300,
            "statusMessage": "Running flutter test..."
          }
        ]
      }
    ]
  }
}
```

### Mevcut proje ornekleri

| Proje | enabledMcpjsonServers | Hook |
|-------|----------------------|------|
| VocabLearningApp | github, git, atlassian, context7, firebase | `flutter gen-l10n && flutter test` |
| ApApp-CrossPlatform | github, git, atlassian, jcodemunch | `flutter pub get && flutter analyze && flutter test` |
| football-ai-platform | github, git, atlassian, context7 | `npx next lint` |
| ByteCraftHQ | github, git, context7, atlassian | (yok) |
| KnightOnlineAI | github, git, atlassian, context7 | (yok) |

### MODIFIYE: Projeye ozel

- **`hooks.Stop.command`**: Proje diline gore degistir:
  - Flutter: `flutter gen-l10n && flutter test`
  - Node.js/Next: `npx next lint`
  - Python: `pytest`
  - Go: `go test ./...`
- **`enabledMcpjsonServers`**: Kullanilacak MCP'leri belirt (tanimlari global'de mevcut)
- `permissions` ve `includeGitInstructions` YAZMA — global'den devralinir

---

## 4. Skills (Slash Commands)

Tum skill'ler `.claude/skills/<skill-adi>/SKILL.md` konumunda. Asagidaki tablodan ihtiyac duyulanlari kopyala.

### Temel Skills (her projede faydali)

| Skill | Komut | Aciklama |
|-------|-------|----------|
| **refine** | `/refine [global\|all] [model]` | Config dosyalarini rafine et |
| **migration** | `/migration [health\|setup\|fix]` | Proje kurulum + saglik kontrolu |
| **audit** | `/audit [security\|cost\|performance\|cleanup\|all]` | Kod taramasi |
| **rbg** | `/rbg <gorev>` | Arka plan delegasyonu |
| **dashboard** | `/dashboard` | Terminal dashboard (cache, 0 token) |
| **dashboard-sync** | `/dashboard-sync` | Jira'dan taze veri + dashboard |
| **agent-browser** | `/agent-browser` | Browser otomasyon CLI |
| **restart** | `/restart` | Oturumu yeniden baslat |
| **claude-api** | `/claude-api` | Claude API/SDK yardim |

### Jira Skills (Jira kullanan projeler icin)

| Skill | Komut | Aciklama |
|-------|-------|----------|
| **jira-run** | `/jira-run [N] [aralik]` | Wait-and-check dongusu |
| **jira-run-fast** | `/jira-run-fast [N]` | 1s aralikli hizli dongu |
| **jira-run-detailed** | `/jira-run-detailed [odak]` | Board derinlemesine audit + bakim (parametrik) |
| **jira-cancel** | `/jira-cancel` | jira-run durdur |
| **jira-start-new-task** | `/jira-start-new-task` | Coklu agent pipeline |
| **decide** | `/decide` | WAITING kartlari hizli karar |

### Arastirma ve Analiz Skills

| Skill | Komut | Aciklama |
|-------|-------|----------|
| **web-research** | `/web-research [odak]` | Web arastirmasi (parametrik) |
| **project-analysis** | `/project-analysis` | 12 kategori paralel audit |
| **sprint-plan** | `/sprint-plan` | Analiz raporlarindan sprint plani |

> **Not:** `web-research` ve `jira-run-detailed` **parametrik** — ayri varyant skill'ler kaldirildi. Odak arguman olarak verilir: `/web-research competitors`, `/jira-run-detailed security` vb.

### Skill Konumu

> **Tum skill'ler `~/.claude/skills/` altinda — yeni proje icin kopyalamak gerekmez.**
> Skill eklemek veya guncellemek icin yalnizca `~/.claude/skills/` dizinini kullan.

```bash
# Mevcut global skill'leri gor
ls ~/.claude/skills/

# Yeni skill ekle
mkdir -p ~/.claude/skills/SKILL_ADI
# SKILL.md dosyasini olustur

# Skill'i tum projelerde aninda kullanilabilir olur (kopyalama gerekmez)
```

### MODIFIYE: Projeye ozel

- Jira skill'leri Jira proje anahtarini `docs/CLAUDE_JIRA.md`'den okur — skill dosyasinda degistirme gerekmez
- Dashboard skill'i proje JQL'ini CLAUDE_JIRA.md'ye bagli okur
- web-research skill'lerindeki rakip/urun isimleri gerekiyorsa skill prompt'unda belirt

---

## 5. Hooks

### Claude Code Hooks (`.claude/settings.json` icinde)

**Stop Hook** — session sonunda otomatik calisir:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "flutter gen-l10n && flutter test",
            "async": true,
            "timeout": 300,
            "statusMessage": "Running flutter test..."
          }
        ]
      }
    ]
  }
}
```

### Diger Hook Turleri (ihtiyaca gore ekle)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File being edited'",
            "async": true
          }
        ]
      }
    ],
    "PostToolUse": [],
    "Notification": []
  }
}
```

### MODIFIYE: Projeye ozel

- `command` alanini proje diline/aracina gore degistir
- Flutter olmayan projede `flutter gen-l10n && flutter test` yerine uygun komutu yaz

---

## 6. CLAUDE.md Dosyalari

### Dosya Hiyerarsisi

```
~/.claude/CLAUDE.md                      # Global (tum projeler)
~/Projects/CLAUDE.md                     # Ust dizin (ortak kurallar)
~/Projects/YeniProje/CLAUDE.md           # Proje ozel (ana talimat)
~/Projects/YeniProje/docs/CLAUDE_JIRA.md # Jira protokolu (Jira kullananlar)
```

### Yeni Proje CLAUDE.md Sablonu

```markdown
# [Proje Adi] — Claude Code

## AI icin hizli tarama

| Once | Kaynak | Not |
|------|--------|-----|
| 1 | Bu dosya (`CLAUDE.md`) | Davranis, Git, CI |
| 2 | `docs/CLAUDE_JIRA.md` | Jira protokolu (varsa) |

**Kesin kurallar:**
1. Oncelik: MCP/tool → script / mevcut kod → reasoning
2. Commit oncesi: [TEST_KOMUTU]
3. Dil: Kullaniciya [DIL]; kod Ingilizce; commit mesaji Ingilizce

---

## 1. Calisma tarzi
- Varsayilan izin modu: **bypassPermissions**
- Minimum soru; mantikli varsayimlarla ilerle
- Yalniz yuksek risk, geri alinamaz veri kaybi veya kritik belirsizlikte sor

## 2. Tool-first ve maliyet
- Oncelik sirasi: (1) MCP/tool → (2) yerel script → (3) reasoning
- Buyuk isi parcala; maliyet icin sorma

## 3. Gorev parcalama
- Gorev ≤ ~10 dakika; asarsa alt goreve bol
- [FRAMEWORK] ozellik sablonu: [ADIMLAR]

## 4. Git, CI
- Commit oncesi: [PAKET_YONETICI] → [LINT] → [TEST]
- Conventional commit: feat:, fix:, refactor:, chore:
- 1-3 dosya → main'e direkt; 4+ → feature branch + PR

## 5. Model ve dil
- Yanitbasi model etiketi: `(Model Adi)`
- Dil: kullaniciya [DIL]; kod Ingilizce; commit Ingilizce

| Model | Maliyet | Ne zaman |
|-------|---------|----------|
| Haiku 4.5 | En dusuk | Label, kucuk duzenleme |
| Sonnet 4.6 | Orta | Kod, orta karmasiklik |
| Opus 4.6 | En yuksek | Mimari, buyuk feature |
```

### MODIFIYE: Projeye ozel

- `[Proje Adi]`, `[TEST_KOMUTU]`, `[FRAMEWORK]`, `[DIL]`, `[PAKET_YONETICI]`, `[LINT]`, `[ADIMLAR]` placeholder'larini doldurun
- Jira kullanmiyorsaniz Jira referanslarini cikarin
- Projeye ozel kurallar ekleyin

---

## 7. Firebase Kurulumu

### firebase.json

```json
{
  "firestore": { "rules": "firestore.rules" },
  "storage": { "rules": "storage.rules" },
  "database": { "rules": "database.rules.json" },
  "functions": [
    {
      "source": "functions",
      "codebase": "default",
      "ignore": ["node_modules", ".git", "firebase-debug.log", "*.local"]
    }
  ],
  "flutter": {
    "platforms": {
      "android": {
        "default": {
          "projectId": "FIREBASE_PROJECT_ID",
          "appId": "ANDROID_APP_ID",
          "fileOutput": "android/app/google-services.json"
        }
      },
      "ios": {
        "default": {
          "projectId": "FIREBASE_PROJECT_ID",
          "appId": "IOS_APP_ID",
          "uploadDebugSymbols": false,
          "fileOutput": "ios/Runner/GoogleService-Info.plist"
        }
      }
    }
  }
}
```

### firestore.rules (ornek)

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Kullanici verileri — yalnizca sahip
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null
                         && request.auth.uid == userId;
    }
    // Feedback — yalnizca olusturma
    match /feedback/{docId} {
      allow create: if request.auth != null
                    && request.resource.data.userId == request.auth.uid;
    }
  }
}
```

### storage.rules (ornek)

```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /feedback/{userId}/{timestamp}/{fileName} {
      allow write: if request.auth != null
                   && request.auth.uid == userId
                   && request.resource.size < 5 * 1024 * 1024
                   && request.resource.contentType.matches('image/.*');
    }
  }
}
```

### Kurulum adimlari

```bash
# 1. Firebase projesi olustur (console.firebase.google.com)
# 2. CLI ile baglan
firebase login
firebase init firestore storage functions

# 3. Kurallari deploy et
firebase deploy --only firestore:rules,storage
```

### MODIFIYE: Projeye ozel

- `FIREBASE_PROJECT_ID`, `ANDROID_APP_ID`, `IOS_APP_ID` degistir
- Firestore/Storage rules'lari projenin veri yapisina gore yaz
- Firebase kullanmiyorsan bu bolumu atla

---

## 8. CI/CD (GitHub Actions)

### Flutter CI: `.github/workflows/flutter_ci.yml`

```yaml
name: Flutter CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: stable
          cache: true

      - name: Create .env
        run: |
          cat > .env << 'ENVEOF'
          FIREBASE_PROJECT_ID=${{ secrets.FIREBASE_PROJECT_ID }}
          FIREBASE_MESSAGING_SENDER_ID=${{ secrets.FIREBASE_MESSAGING_SENDER_ID }}
          FIREBASE_STORAGE_BUCKET=${{ secrets.FIREBASE_STORAGE_BUCKET }}
          FIREBASE_ANDROID_API_KEY=${{ secrets.FIREBASE_ANDROID_API_KEY }}
          FIREBASE_ANDROID_APP_ID=${{ secrets.FIREBASE_ANDROID_APP_ID }}
          FIREBASE_IOS_API_KEY=${{ secrets.FIREBASE_IOS_API_KEY }}
          FIREBASE_IOS_APP_ID=${{ secrets.FIREBASE_IOS_APP_ID }}
          FIREBASE_IOS_BUNDLE_ID=${{ secrets.FIREBASE_IOS_BUNDLE_ID }}
          ENVEOF

      - run: flutter pub get
      - run: flutter gen-l10n
      - run: flutter analyze
      - run: flutter test --exclude-tags golden
```

### MODIFIYE: Projeye ozel

- Secrets'lari GitHub repo Settings → Secrets'a ekle
- Flutter degilse `flutter` komutlarini proje aracina degistir
- Ekstra adimlar (deploy, Docker build, vs.) ekle

---

## 9. Scripts

### Tasinabilir scriptler (`scripts/` dizini)

| Script | Aciklama | Bagimlilik | Degistirilecek |
|--------|----------|------------|----------------|
| `dashboard.py` | Terminal dashboard | Python3, `.jira_cache.json` | Jira proje anahtari |
| `jira_run_cancel.sh` | jira-run durdur | Bash | - |
| `jira_clear_working_lock.sh` | Working lock temizle | Bash | - |
| `jira_draft_to_todo.py` | Bulk Draft→To Do | Python3, Jira API | Jira URL, proje |
| `jira_setup_board.py` | Board baslat | Python3, Jira API | Jira URL, proje |
| `jira_sync.sh` | Jira sync | Bash, Jira API | Jira URL |
| `build_and_distribute.sh` | APK build + dagitim | Bash, Flutter | Build path |
| `notify_telegram.sh` | Telegram bildirim | Bash, curl | Bot token, chat ID |
| `upload_drive.sh` | Google Drive upload | Bash, gcloud | Drive folder ID |

### Kopyalama

```bash
cp -r KAYNAK_PROJE/scripts/ HEDEF_PROJE/scripts/
chmod +x HEDEF_PROJE/scripts/*.sh
```

### MODIFIYE: Projeye ozel

- Jira URL'leri ve proje anahtarlarini degistir
- Telegram bot token/chat ID'yi degistir
- Build path'leri projeye uyarla

---

## 10. Environment Variables

### `.env.example` (proje kokune kopyala, `.env` olarak doldur)

```bash
# === Telegram ===
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_ALLOWED_CHAT_ID=

# === Jira API ===
JIRA_URL=https://SITE.atlassian.net
JIRA_USERNAME=
JIRA_API_TOKEN=

# === Google Drive ===
GOOGLE_DRIVE_FOLDER_ID=
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=

# === Firebase (--dart-define ile gecilir, .env'ye de yedek) ===
FIREBASE_PROJECT_ID=
FIREBASE_MESSAGING_SENDER_ID=
FIREBASE_STORAGE_BUCKET=
FIREBASE_ANDROID_API_KEY=
FIREBASE_ANDROID_APP_ID=
FIREBASE_IOS_API_KEY=
FIREBASE_IOS_APP_ID=
FIREBASE_IOS_BUNDLE_ID=

# === RevenueCat ===
REVENUE_CAT_ANDROID_API_KEY=
REVENUE_CAT_IOS_API_KEY=

# === AdMob ===
ADMOB_ANDROID_APP_ID=
ADMOB_IOS_APP_ID=
ADMOB_ANDROID_BANNER_ID=
ADMOB_IOS_BANNER_ID=
```

### MODIFIYE: Projeye ozel

- Kullanmayacaginiz servisleri cikarin
- Kendi API anahtarlarinizi doldurun
- `.env` dosyasini `.gitignore`'a ekleyin

---

## 11. Jira Entegrasyonu

### Gerekli dosyalar

```
docs/CLAUDE_JIRA.md          # Jira protokolu (tam metin)
docs/CLAUDE_JIRA_NOTES.md    # Degisiklik logu
docs/jira_loop_log.md        # Tur izleme logu (append-only)
.jira_cache.json             # Dashboard cache (otomatik olusur)
```

### Jira Transition ID'leri

| Durum | ID | Aciklama |
|-------|----|----------|
| Draft | 2 | Taslak |
| Feedback | 3 | Geri bildirim bekliyor |
| Backlog | 4 | Backlog |
| Refine | 5 | Detaylandirma |
| Blocked | 6 | Engellenmis |
| Waiting | 7 | Onay bekliyor |
| To Do | 11 | Yapilacak |
| In Progress | 21 | Devam ediyor |
| Done | 31 | Tamamlandi |

### MODIFIYE: Projeye ozel

- `VOC` → kendi Jira proje anahtariniz
- Transition ID'leri projenizin workflow'una gore degisebilir — `getTransitionsForJiraIssue` ile kontrol edin
- Cloud ID'yi `getAccessibleAtlassianResources` ile alin
- `CLAUDE_JIRA.md` icerigini proje akisina uyarlayin

---

## 12. Projeye Ozel Degistirilecekler — Kontrol Listesi

Yeni projeye tasirken asagidaki maddeleri tek tek kontrol edin:

### Zorunlu Degisiklikler

- [ ] `~/.claude/settings.json` → `mcpServers.git.command` ve `jcodemunch.command` yolunu guncelleyin (`which uvx`)
- [ ] `.claude/settings.json` → `enabledMcpjsonServers` listesini guncelleyin
- [ ] `.claude/settings.json` → Hook komutlarini proje diline uyarlayin
- [ ] `CLAUDE.md` → Proje adini, framework'u, test komutunu degistirin
- [ ] `.env` → Tum API anahtarlarini doldurun
- [ ] `.gitignore` → `/dist/` ve diger build ciktilarina ekleyin
- **Skill kopyalamaya GEREK YOK** — `~/.claude/skills/` global olarak tum projelerde aktif

### Firebase Kullananlar

- [ ] `firebase.json` → Project ID, App ID guncelleyin
- [ ] `firestore.rules` → Veri yapisina gore kurallari yazin
- [ ] `storage.rules` → Upload kurallarina uyarlayin
- [ ] `firebase deploy --only firestore:rules,storage`

### Jira Kullananlar

- [ ] `docs/CLAUDE_JIRA.md` → Proje anahtarini degistirin
- [ ] Transition ID'leri kontrol edin
- [ ] Cloud ID'yi guncelleyin
- (Skill'lerde degistirme gerekmez — Jira anahtari CLAUDE_JIRA.md'den okunur)

### CI/CD

- [ ] `.github/workflows/` → Secrets ekleyin
- [ ] Build/test komutlarini proje diline uyarlayin

### Opsiyonel

- [ ] Telegram entegrasyonu → Bot token + chat ID
- [ ] Google Drive upload → Service account + folder ID
- [ ] web-research skill'leri → Rakip/urun isimlerini degistirin

---

## Hizli Baslangic (TL;DR)

### Yol A — Interaktif (Onerilen)

```bash
# 1. Yeni proje dizininde Claude Code'u ac
mkdir YeniProje && cd YeniProje && git init && claude

# 2. Claude'a soyle:
#    "MIGRATION_GUIDE.md'yi oku ve bu projeyi kur"
#    veya "@__PROJECTS_ROOT__/MIGRATION_GUIDE.md bu rehberi kullanarak projeyi kur"
#
# Claude Bolum 0'daki sorulari soracak, cevaplarina gore
# tum dosyalari otomatik olusturacak.
```

### Yol B — Manuel

```bash
# 1. Proje olustur
mkdir YeniProje && cd YeniProje && git init

# 2. Proje settings.json olustur (sadece hooks + MCP secimi)
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "enabledMcpjsonServers": ["github", "git", "atlassian", "context7"],
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "YOUR_TEST_CMD", "async": true, "timeout": 300 }] }]
  }
}
EOF

# 3. CLAUDE.md olustur (sablondan)
# Bu dosyanin "Yeni Proje CLAUDE.md Sablonu" bolumunu kullan

# 4. Env dosyasini hazirla
cp KAYNAK/.env.example .env.example
cp .env.example .env
# .env icini doldur

# 5. Claude Code'u baslat — permissions + skill'ler ~/.claude/ globalden otomatik gelir
claude
```

> **Not:** Skill kopyalamaya gerek yok. `~/.claude/skills/` altindaki tum skill'ler yeni projede otomatik aktif olur.

---

*Bu rehber VocabLearningApp projesinden olusturulmustur. Son guncelleme: 2026-03-30*
