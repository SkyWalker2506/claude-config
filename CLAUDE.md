# claude-config — Merkezi Konfigürasyon

Bu klasor Claude Code konfigürasyonunun **kaynak reposudur**. Global CLAUDE.md, settings.json, skill'ler ve migration — her sey buradan yonetilir.

**Global `~/.claude/CLAUDE.md` sadece yonlendiricidir. Tum kurallar bu dosyadadir.**

---

## Repo yapisi

`install.sh` calistirinca:
- `global/` → `~/.claude/` (CLAUDE.md, settings.json, skills/)
- `projects/` → `$PROJECTS_ROOT/` (CLAUDE.md, MIGRATION_GUIDE.md, scripts/)
- Placeholder'lar (`__PROJECTS_ROOT__`, `__UVX_PATH__`) otomatik degistirilir

```
global/
  CLAUDE.md                → Yonlendirici (minimal)
  settings.json.template   → MCP, izinler, hook'lar
  skills/                  → Tum skill SKILL.md dosyalari

projects/
  CLAUDE.md                → Ortak proje kurallari
  MIGRATION_GUIDE.md       → Setup wizard
  scripts/                 → Hook script'leri

templates/                 → Yeni proje sablonlari
```

## Degisiklik yapma

1. **Bu repodaki** dosyayi duzenle
2. `./install.sh` calistir → yerlerine kopyalanir
3. Commit + push → diger PC'lerde `git pull && ./install.sh`

**`~/.claude/` altindaki dosyalari dogrudan duzenleme** — `install.sh` ile ezilir.

---

## Calisma kurallari (tum projeler)

### 1. Calisma tarzi

- Proaktif, kararlı, minimum soru
- Mantikli varsayimlarla ilerle; geri alinabilir isleri onaysiz yap
- **Yalniz su durumlarda sor:** yuksek risk (guvenlik, KVKK, odeme, prod), geri alinamaz veri kaybi, veya istek kritik olcude belirsiz

### 2. Tool-first ve maliyet

**Oncelik sirasi:** (1) MCP / tool → (2) yerel script / mevcut cozum → (3) son care reasoning

- MCP veya tool ile cozulebiliyorsa **her zaman** tool kullan
- Buyuk isi parcala; maliyet icin sorma
- Gereksiz exploration yok — sadece edit edecegi veya bagimliligini anlamasi gereken dosyalari oku

### 3. Model ve dil

- Yanit basinda model etiketi: `(Model Adi)` — orn. `(Opus 4.6)`
- **Dil:** kullaniciya Turkce; kod/commit Ingilizce
- Basit/orta is + Opus aktifken → daha ucuz modele gecmeyi **oner**

| Model | Maliyet | Ne zaman |
|-------|---------|----------|
| Haiku 4.5 | En dusuk | Label, kucuk duzenleme, basit soru |
| Sonnet 4.6 | Orta | Kod, orta karmasiklik |
| Opus 4.6 | En yuksek | Mimari, buyuk feature, zor debug |

**Token koruma:**
- Iki paralel Opus session acma
- Sub-agent: prompt basinda `(Model Adi)`, limit belirt, max 2-3 paralel
- Buyuk dosya okuma+yazma (>20KB): Sonnet'te yap
- Is hafiflediyse model gecisi oner

### 4. jCodeMunch MCP

`jcodemunch` MCP bagliyken:
1. `resolve_repo` ile koku coz; indeks yoksa `index_folder`
2. Kod arama icin jCodeMunch araclari: `search_symbols`, `get_symbol_source`, `get_file_outline`, `get_repo_outline`, `get_file_tree`, `search_text`, `find_importers`, `find_references`
3. Read/Grep/Glob ile tum dosya tarama varsayilan olmasin; once sembol odakli sorgu
4. Tam dosya okuma yalnizca dosya duzeyinde baglam gerektiginde

**Indexleme sinyalleri:**

| Sinyal | Aksiyon |
|--------|---------|
| `INDEX_ASK` | Kullaniciya sor, onaylarsa `resolve_repo` → `index_folder` → marker |
| `INDEX_UPDATE` | Sessizce guncelle: `resolve_repo` → `index_folder` → marker |

**Marker:** `mkdir -p .claude && { date -u +%FT%TZ; git rev-parse HEAD 2>/dev/null; } > .claude/jcodemunch_indexed`

### 5. Migration sistemi

Hook ciktisindaki sinyaller:

| Sinyal | Aksiyon |
|--------|---------|
| `INSTALL_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` + `/restart` |
| `MCP_SETUP_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` + `/restart` |
| `MIGRATION_NEEDED` | `/migration` calistir veya `MIGRATION_GUIDE.md` Bolum 0 |
| `MIGRATION_UPDATE` | Changelog'dan delta uygula, versiyon guncelle |
| `SECRETS_MISSING` | `~/.claude/secrets/secrets.env` duzenle, git varsa push hatırlat |
| `SECRETS_NONE` | `install.sh` calistir veya secrets.env olustur |
| `CONFIG_UPDATE` | Kullaniciya sor: git pull + install.sh + restart |
| `BIND_NEEDED` | `/bind` calistir — global CLAUDE.md'yi claude-config'e bagla |

### 6. Secrets guvenligi

- Secret degerleri **ASLA** konusma ciktisina, commit'e, public dosyaya veya log'a yazilmaz
- Secret'lar yalnizca `~/.claude/secrets/` altinda
- `.git` varsa → private repo, push hatırlat
- `.git` yoksa → lokal, sadece o PC

### 7. settings.json konfigürasyonu

`global/settings.json.template` icerigi — `install.sh` placeholder'lari cozer:

| Ayar | Deger |
|------|-------|
| `defaultMode` | `bypassPermissions` |
| `effortLevel` | `high` |
| `model` | `opus` |
| `voiceEnabled` | `true` |
| `includeGitInstructions` | `true` |
| `skipDangerousModePermissionPrompt` | `true` |
| Hook | `migration_check.sh` (UserPromptSubmit) |

**MCP sunuculari:** github, git, atlassian, flutter-dev, firebase, context7, jcodemunch, fetch

**Izin ask:** `git push --force`, `rm -rf`, `gh repo delete`, `shred`

### 8. Skill'ler

Tum skill'ler `global/skills/` altinda:

| Skill | Komut | Aciklama |
|-------|-------|----------|
| install | `/install` | claude-config kurulumu |
| admin-login | `/admin-login` | GitHub auth ve hesap yonetimi |
| download-secrets | `/download-secrets` | Private repo'dan secrets indir |
| refine | `/refine [global\|all] [model]` | Config dosyalarini rafine et |
| migration | `/migration [health\|setup\|fix]` | Proje kurulum + saglik kontrolu |
| audit | `/audit [security\|cost\|performance\|cleanup\|all]` | Kod taramasi |
| rbg | `/rbg <gorev>` | Arka plan delegasyonu |
| dashboard | `/dashboard` | Terminal dashboard (cache, 0 token) |
| dashboard-sync | `/dashboard-sync` | Jira'dan taze veri + dashboard |
| jira-run | `/jira-run [N] [aralik]` | Jira wait-and-check dongusu |
| jira-run-fast | `/jira-run-fast [N]` | 1s aralikli hizli dongu |
| jira-run-detailed | `/jira-run-detailed [odak]` | Board derinlemesine audit + bakim |
| jira-cancel | `/jira-cancel` | jira-run durdur |
| jira-start-new-task | `/jira-start-new-task` | Coklu agent pipeline |
| decide | `/decide` | WAITING kartlari hizli karar |
| project-analysis | `/project-analysis` | 12 kategori paralel audit |
| sprint-plan | `/sprint-plan` | Analiz raporlarindan sprint plani |
| web-research | `/web-research [odak]` | Web arastirmasi (parametrik) |
| agent-browser | `/agent-browser` | Browser otomasyon CLI |
| prd | `/prd` | Feature icin PRD olustur |
| ralph | `/ralph` | PRD → prd.json + Ralph baslat |
| add-mcp | `/add-mcp [flutter\|firebase]` | MCP sunucusu ekle/kaldir |
| index | `/index [force]` | jCodeMunch indexle + auto-update |
| team-build | `/team-build [setup\|run\|status]` | Multi-agent takim |
| bind | `/bind` | Global CLAUDE.md'yi claude-config'e bagla |

### 9. Task Discipline & Watchdog

#### 9a. Gorev basinda — Plan (zorunlu)

Her oturum basinda **plan moduna gir** (`EnterPlanMode`). Ilk gorev geldiginde once planla → kullanici onayi → sonra uygula. Plan onaylanana kadar kod yazma.

Her yeni gorev/istek geldiginde:

```
PLAN:
1. [adim 1]
2. [adim 2]
3. [adim 3]
Tahmin: quick | medium | long
```

| Seviye | Tool call | Sure |
|--------|-----------|------|
| `quick` | ≤5 | <2 dk |
| `medium` | 5-20 | 2-10 dk |
| `long` | >20 | >10 dk |

- Plan cikarmak hizli — 10 saniyede bitir
- "Hemen yap" denirse → 1 satirda ozetle, basla
- Sub-agent'lara da plan zorunlu

#### 9b. Self-monitoring

**Her 5 tool call → sessiz self-check:**
1. Dogru adimda miyim?
2. Somut ilerleme oldu mu?
3. Tekrar mi yapiyorum?

**Her 10 tool call → 1 satir durum:**
```
[3/5] Component olusturuldu, test geciyor.
```

**Alarm kosullari:**

| Kosul | Aksiyon |
|-------|---------|
| Ayni hata 2x | DUR → farkli yaklasim (max 1 alternatif) |
| 8+ call dosya degismedi | DUR → rapor, yeniden degerlendir |
| 5+ call ayni dosya dongusu | DUR → donguden cik |
| Onceki adima geri donme | 1 satirda bildir |

#### 9c. Overrun detection

| Tahmin | Limit | Asilirsa |
|--------|-------|----------|
| `quick` | 10 | Uyar, sor |
| `medium` | 30 | Uyar + rapor + alternatif |
| `long` | 50 | Danis |

Onay sonrasi yeni limit: mevcut + 50%. Tekrar asarsa durdur.

#### 9d. Recovery

1. Sorunu 1 cumlede belirt
2. TEK alternatif dene
3. Basarisizsa → rapor et, DUR

#### 9e. Otonom gorevler (heartbeat)

```bash
mkdir -p /tmp/watchdog
echo '{"task":"TASK","step":"...","progress":"3/7","status":"running","ts":"..."}' > /tmp/watchdog/TASK_ID.json
```

**Feedback log:** `~/Projects/.watchdog/feedback.jsonl`
```json
{"id":"ID","task":"...","project":"...","model":"...","started":"T","ended":"T","tool_calls":N,"outcome":"success|recovered|failed","stuck_reason":null,"learnings":"..."}
```

Stale alert: >10dk guncellenmemis → uyari. Kisa gorevlerde (<10 dk) watchdog baslatma.

#### 9f. Sub-agent watchdog

Sub-agent prompt'una ekle:
```
WATCHDOG: Bu gorev [quick|medium|long]. Max N tool call.
Plan: [1-3 adim]. Her 5 call self-check yap.
```

---

## Yeni skill ekleme

```bash
mkdir -p global/skills/yeni-skill
# global/skills/yeni-skill/SKILL.md olustur
./install.sh
```

## Migration guncelleme

1. `projects/MIGRATION_GUIDE.md` → Changelog'a versiyon ekle
2. `projects/MIGRATION_VERSION` → numara artir
3. `./install.sh` → tasinir
