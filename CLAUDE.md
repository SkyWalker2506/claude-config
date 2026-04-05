# claude-config — Calisma Kurallari

> Degisiklik: bu repoda duzenle → `./install.sh` → commit + push. `~/.claude/` altini dogrudan duzenleme.

## Calisma kurallari (tum projeler)

### 1. Calisma tarzi

- Proaktif, kararlı, minimum soru
- Mantikli varsayimlarla ilerle; geri alinabilir isleri onaysiz yap
- **Yalniz su durumlarda sor:** yuksek risk (guvenlik, KVKK, odeme, prod), geri alinamaz veri kaybi, veya istek kritik olcude belirsiz
- **Komutlari dogrudan calistir** — "su komutu calistir: `...`" yazma, Bash tool ile kendin calistir. Kullaniciya copy-paste yaptirma
- **Tehlikeli komutlar** (`rm -rf`, force push, DB drop, prod silme vb.): calistirma — kullaniciya ac,ikca soyle ("BU TEHLİKELİ: [ne olur]"), birden fazla kez sor, emin degilsen yapma
- **Kullaniciya soru sormak gerekirse:** once terminal'de sor; kullanici yoksa (otonom/background gorev) `bash ~/Projects/claude-config/config/telegram-ask.sh "soru" "emoji"` ile Telegram'a gonder, cevap bekle

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

**Haftalik kota yonetimi** (reset gunu: /usage'dan oku):

| Kalan / gun | Mod | Kural |
|-------------|-----|-------|
| ≥10% | Normal | Opus mimari/karar, Sonnet kod, Haiku trivial |
| 5-10% | Tasarruf | Opus yalniz kritik karar; geri kalan Sonnet |
| <5% | Kritik | Opus yok — Sonnet + Haiku; Opus sadece geri alinamaz karar |
| <1% (Haiku) | Sonnet-only | Haiku bitti sayilir — Sonnet'e gec; %0 bekleme |

Hesaplama: `(kalan all-models %) / (reset'e kalan gun)` — ortukte uyar, mod degistir.

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
| `INSTALL_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` |
| `MCP_SETUP_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` |
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

### 7. Skill'ler

Tum skill'ler `global/skills/` altinda — her klasorde `SKILL.md` trigger ve aciklama icerir. Ayrintili konfigürasyon: `global/settings.json.template`.

**Dinamik skill prompt'lari:** Skill .md icinde `$(komut)` ile shell ciktisi gomulur. Skill calistiginda komut calistirilir, sonuc prompt'a inline eklenir — model komutu degil sonucu gorur. Ornek: `$(git branch --show-current)`, `$(date +%F)`, `$(cat .env.example | head -5)`.

### 8. Proje gelistirme kurallari

Asagidaki kurallar `~/Projects/` altindaki **tum projeler** icin gecerlidir. Projeye ozel detaylar her projenin kendi `CLAUDE.md` dosyasinda tanimlanir.

#### 8a. Gorev parcalama

- Gorev ≤ ~10 dakika; asarsa Jira'da alt goreve bol, sonra tek tek uygula
- **Paten → Kaykay → Bisiklet → Araba:** Her sprint sonunda deploy edilebilir, test edilebilir, kullanici tarafindan deneyimlenebilir bir butun teslim et
- **Kapsam:** "Sunu da yapayim" yok; refactor gorursen ayri task ac
- **Sirala:** IP'deki isi tamamla → commit → push → CI yesil → Done
- **Tek gorev adami:** Her session/agent tek bir is bilir. Sohbete bildirim ekliyorsan sadece bildirim ekle — ustune dashboard, settings, review ekleme. Bitti → yeni session ac, yeni is ver

#### 8b. Git ve CI

- **Conventional commit:** `feat:`, `fix:`, `refactor:`, `chore:` (Ingilizce)
- **Dal kurali:**
  - 1-3 dosya, tek commit → main'e direkt push
  - 4+ dosya veya birden fazla commit → feature branch → PR → CI yesil → merge
  - CI workflow degisikligi → her zaman PR
  - Mimari / buyuk refactor → feature branch + PR + review
- **Force push → sor**
- **Worktree / branch:** Riskli refactor veya deney oncesi `/branch` ile session fork'la veya `worktree` kullan. Sub-agent'lar izole worktree'de calisabilir — ana branch'i bozmaz

#### 8c. Dosya sistemi ve guvenlik

- **Proje ici:** olusturma, duzenleme, refactor, gereksiz dosya silme — sormadan yap
- **Proje disi / kisisel / sistem dosyalari:** ASLA sormadan dokunma
- **Guvenli sil:** `build/`, cache, gecici, generated, kullanilmayan proje dosyasi
- **Mutlaka sor:** `rm -rf` (tehlikeli kapsam), `git reset --hard`, `git push --force`, repo silme, guvenlik/KVKK, odeme, secrets (`.env`), ucretli servis

#### 8d. Hata yonetimi

- **Self-healing:** analiz → kok neden → duzelt → tekrar dene; **max 3 deneme**; sonra kullaniciya rapor
- **Akilli tekrar:** ayni hatayi tekrarlama; farkli cozum dene
- **Riskli is oncesi yedek:** `.backup/<timestamp>/` — buyuk refactor, toplu silme, config degisimi
- **Dogrulama donguleri:** Yap → dogrula zinciri kur. Ornek: build et → loglari izle → hata olmadigini dogrula. Sadece "calisiyor" yetmez — log/test/lint ile dogrula

#### 8e. Jira (kullanan projeler icin)

> Jira detaylari projenin `docs/CLAUDE_JIRA.md` dosyasinda. Lock sistemi: `~/Projects/claude-config/docs/LOCK_SYSTEM.md`. Implementation agent şablonu: skill'in `docs/agent-template.md` dosyasinda.

- Koda baslamadan **In Progress** (transition 21)
- Tum alt gorevler bitmeden ana gorevi Done yapma
- **WAITING (7):** onay, credential, ucretli servis, urun karari gereken isler
- IP'de "bekletme" yok — ya tamamla ya WAITING'e tasi

#### 8f. Bootstrap (setup eksikse)

```
repo yapisi → paket yoneticisi → bagimliliklar → .env.example → calistir/build
```

- Self-healing: §9d kurali gecerli
- Mantikli varsayimlarla ilerle; her adimda sorma
- `.claudeignore` yoksa → `~/Projects/claude-config/templates/claudeignore.template` kopyala

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
Model: Haiku/Sonnet/Opus | Effort: low/medium/high
Agent: [registry'den uygun agent ID + isim] | Fallback: [fallback agent]
```

**Otomatik model/effort onerisi:** Her planda gorev tipine gore model ve effort oner. Kullanici gecmezse hatırlat.

| Gorev tipi | Model | Effort |
|-----------|-------|--------|
| Sohbet, karar, README, config | Haiku/Sonnet | low |
| Kod yazma, bug fix, refactor | Sonnet | medium |
| Mimari, buyuk feature, karmasik debug | Opus | high |
| GitHub API, topic/description, polish | Sonnet | low |
| Plan tartismasi, strateji | Sonnet | medium |

| Seviye | Tool call | Sure | Effort |
|--------|-----------|------|--------|
| `quick` | ≤5 | <2 dk | low |
| `medium` | 5-20 | 2-10 dk | medium |
| `long` | >20 | >10 dk | high |

**Effort level:** Skill/agent bazinda reasoning derinligini belirler. `quick` → hizli cevap, `long` → derin dusunme. Skill .md'lerde `effort` alani tanimlanabilir; tanimlanmamissa gorev tahmininden turetilir.

**Agent routing (otomatik):** Her planda gorev tipine gore `config/agent-registry.json`'dan uygun agent sec. Agent'in `primary_model` ve `effort` degerleri plan'daki Model/Effort'u override eder. Agent bulunamazsa varsayilan model/effort tablosu kullanilir.

| Gorev ornegi | Agent | Model (override) |
|-------------|-------|-------------------|
| REST API yaz | B2 Backend Coder | Sonnet, high |
| Flutter widget | B15 Mobile Dev | Sonnet, high |
| Bug fix, debug | B7 Bug Hunter | Sonnet, medium |
| Security audit | B13 Security Auditor | Opus, high |
| Jira sprint plan | I2 Sprint Planner | Sonnet, medium |
| Web arastirmasi | K1 Web Researcher | Free, medium |
| GitHub polish | H5 SEO + H6 GEO | Free/Haiku, medium |
| Phaser/JS game | B16 Web Game Dev | Sonnet, high |
| Unity gelistirme | B19 Unity Developer | Sonnet, high |

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

`learnings` alani: otonom gorevlerde VE her interaktif session sonunda yazilir (bkz §10).

Stale alert: >10dk guncellenmemis → uyari. Kisa gorevlerde (<10 dk) watchdog baslatma.

#### 9f. Sub-agent watchdog

Sub-agent prompt'una ekle:
```
WATCHDOG: Bu gorev [quick|medium|long]. Max N tool call.
Plan: [1-3 adim]. Her 5 call self-check yap.
```

---

### 10. Session sonu — ders çıkarma (otomatik)

Her session'da proaktif olarak ders çıkar ve kaydet. **Kullaniciya sorma** — dogrudan yap.

#### Ne zaman tetiklenir

| Durum | Örnek |
|-------|-------|
| Hata yapıp düzelttinde | Yanlış API çağrısı → doğruya bulundu |
| Kullanıcı düzeltme/yönlendirme yaptığında | "Hayır öyle değil, şöyle yap" |
| Beklenmedik çözüm bulunduğunda | Paket versiyon çakışması, garip davranış |
| Görev tamamlandığında — öğrenilecek bir şey varsa | Mimari karar, teknik insight |

Sıradan soru-cevap, trivial değişiklikler → ders çıkarmaya gerek yok.

#### Ne yapar

1. Oturumda öğrenilen 1-3 şeyi belirle
2. Her ders için memory sistemine `feedback` tipi dosya yaz
3. `~/Projects/.watchdog/feedback.jsonl`'e JSON satırı ekle
4. Kullanıcıya kısa blok göster:

```
📋 Bu oturumdan dersler:
- [ders 1]
- [ders 2]
Kaydedildi → memory/feedback_xxx.md
```

#### Memory dosyasi formati

`feedback_<konu>.md` — CLAUDE.md §feedback tipi kurallari gecerli:

```markdown
---
name: <konu>
description: <tek satir — gelecekte alaka degerlendirmesi icin spesifik ol>
type: feedback
---

<kural>

**Why:** <sebep — kullanicinin verdigi neden veya yasanan olay>
**How to apply:** <ne zaman / nerede bu kural devreye girer>
```

#### feedback.jsonl satiri

Format: `§9e` ile ayni — `learnings` alani serbest metin.

### 11. Multi-Agent Sistemi

- Agent tanimlari: `agents/` dizini (134 agent, 15 kategori — 30 active, 104 pool)
- Registry: `config/agent-registry.json` — agent → model mapping, capability tags, retry strategy
- Fallback: `config/fallback-chains.json` — conditional (hata turune gore farkli yol), local-first
- Tier kurallari: `config/model-tiers.json` — kota bazli mod (Normal/Saving/Critical/Local-only), cost control
- Layer contracts: `config/layer-contracts.json` — Ultra Plan Mode structured output zorunluluklari
- Health check: `config/daily-check.sh` — gunluk Ollama/MCP/API/registry kontrolu
- Routing: A2 (Task Router, Sonnet) capability match + confidence skoru ile agent secer
- Fallback oncelik: LOCAL (Ollama) → CLAUDE (paid) → FREE (OpenRouter)
- Mevcut skill'ler aynen calisir — agent sistemi ust katman, degisiklik yok
- Pool → Active gecis: `agent-registry.json`'da `status` degistir
- Auto-dispatch: Her plan ciktiginda `agent-registry.json`'dan capability match ile uygun agent secer; model/effort/MCP o agent'in kurallarina gore atanir
