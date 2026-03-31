# Global Claude (tum projeler)

Bu dosya her projede otomatik birlestirilir (`~/.claude/CLAUDE.md`). Evrensel kurallar burada; projeye ozel detaylar projenin kendi `CLAUDE.md` dosyasinda.

---

## 1. Calisma tarzi

- Varsayilan izin modu: **bypassPermissions**
- Proaktif, kararlı, minimum soru
- Mantikli varsayimlarla ilerle; geri alinabilir isleri onaysiz yap
- **Yalniz su durumlarda sor:** yuksek risk (guvenlik, KVKK, odeme, prod), geri alinamaz veri kaybi, veya istek kritik olcude belirsiz

## 2. Tool-first ve maliyet

**Oncelik sirasi:** (1) MCP / tool → (2) yerel script / mevcut cozum → (3) son care reasoning.

- MCP veya tool ile cozulebiliyorsa **her zaman** tool kullan
- Buyuk isi parcala; maliyet icin sorma
- Gereksiz exploration yok — sadece edit edecegi veya bagimliligini anlamasi gereken dosyalari oku

## 3. Model ve dil

- Yanit basinda model etiketi: `(Model Adi)` — orn. `(Opus 4.6)`
- **Dil:** kullaniciya Turkce; kod Ingilizce; commit mesaji Ingilizce
- Basit/orta is + Opus aktifken → daha ucuz modele gecmeyi **oner**; kullanici karar verir

| Model | Maliyet | Ne zaman |
|-------|---------|----------|
| Haiku 4.5 | En dusuk | Label, kucuk duzenleme, basit soru |
| Sonnet 4.6 | Orta | Kod, orta karmasiklik |
| Opus 4.6 | En yuksek | Mimari, buyuk feature, zor debug |

### Token koruma

- **Iki paralel Opus session acma** — her biri ayri limit harcar
- **Sub-agent:** prompt'un ilk satiri `(Model Adi)`. Limiti belirt ("max 10 tool call"). Paralel agent max 2-3
- **Buyuk dosya okuma+yazma** (>20KB): Sonnet'te yap
- Session ortasinda is hafiflediyse model gecisi **oner**

## 4. jCodeMunch MCP ve otomatik indexleme

`jcodemunch` MCP bagliyken:

1. `resolve_repo` ile calisma kokunu coz; indeks yoksa `index_folder`
2. Kod arama/kesif icin jCodeMunch araclarini kullan: `search_symbols`, `get_symbol_source`, `get_file_outline`, `get_repo_outline`, `get_file_tree`, `search_text`, `find_importers`, `find_references`
3. Yerlesik Read/Grep/Glob ile tum dosyayi tarama varsayilan olmasin; once sembol ve yapi odakli sorgu
4. Tam dosya okuma yalnizca dosya duzeyinde baglam gerektiginde

### Otomatik indexleme sinyalleri

Hook ciktisinda su sinyaller gorunebilir:

| Sinyal | Aksiyon |
|--------|---------|
| `INDEX_ASK` | Kullaniciya sor: "Bu klasorde jCodeMunch indexleme yapayim mi?" Onay gelirse: `resolve_repo` → `index_folder` → marker olustur |
| `INDEX_UPDATE` | Sessizce guncelle: `resolve_repo` → `index_folder` → marker guncelle. Kullaniciya bildirim yapma. |

**Marker:** Indexleme sonrasi marker'i guncelle (timestamp + git HEAD):
```bash
mkdir -p .claude && { date -u +%FT%TZ; git rev-parse HEAD 2>/dev/null; } > .claude/jcodemunch_indexed
```

**Manuel indexleme:** `/index` komutu ile. Ayni zamanda auto-update'i aktif eder.

## 5. Migration sistemi

Her konusma basinda `migration_check.sh` hook'u calisir. Ciktisina gore:

| Sinyal | Aksiyon |
|--------|---------|
| `INSTALL_NEEDED` | Kullaniciya `cd ~/Projects/claude-config && ./install.sh` calistirmasini ve sonra oturumu yeniden baslatmasini (`/restart`) soylen. Baska islem yapma. |
| `MCP_SETUP_NEEDED` | MCP sunuculari eksik. Kullaniciya `cd ~/Projects/claude-config && ./install.sh` calistirmasini ve oturumu yeniden baslatmasini soylen. |
| `MIGRATION_NEEDED` | `/migration` calistir veya `MIGRATION_GUIDE.md` Bolum 0'i izle |
| `MIGRATION_UPDATE` | `MIGRATION_GUIDE.md` Changelog'dan delta uygula, versiyon guncelle |
| `SECRETS_MISSING` | Kullaniciya eksik secret'lari bildir. `~/.claude/secrets/secrets.env` dosyasini duzenlemesini soylen. Git reposu varsa commit+push hatırlat. **Secret degerlerini asla konusma ciktisina, public repoya veya log'a yazma.** |
| `SECRETS_NONE` | Secrets dosyasi yok. Kullaniciya `install.sh` calistirmasini veya `~/.claude/secrets/secrets.env` olusturmasini soylen. |
| `CONFIG_UPDATE` | claude-config reposunda guncelleme var. Kullaniciya sor: "claude-config guncellendi, git'ten cekmek ister misin?" Onay verirse: (1) `cd ~/Projects/claude-config && git pull` calistir, (2) `./install.sh` calistir, (3) "Degisiklikler uygulandi. Oturumu yeniden baslatmak ister misin?" sor. Hayir derse: "Sorun degil — claude tekrar acildiginda otomatik kontrol edecek." de. |
| Sinyal yok | Sessiz gec |

### Secrets guvenligi

- **Secret degerleri ASLA** konusma ciktisina, commit mesajina, public dosyaya veya log'a yazilmaz
- Secret'lar yalnizca `~/.claude/secrets/` altinda tutulur
- `~/.claude/secrets/.git` varsa → private repo, degisiklik sonrasi `git push` hatırlat
- `~/.claude/secrets/.git` yoksa → lokal dosya, sadece o PC'de gecerli
- Kullanici secret ekledi/degistirdiyse ve git reposu varsa, **yalnizca private repoya** push edilir

## 6. Global skills

Tum skill'ler `~/.claude/skills/` altinda — proje klasorlerine kopyalamak gerekmez.

| Skill | Komut | Aciklama |
|-------|-------|----------|
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
| ralph | `/ralph` | PRD'yi prd.json'a cevir + Ralph baslat |
| add-mcp | `/add-mcp [flutter\|firebase]` | Sonradan MCP sunucusu ekle/kaldir |
| index | `/index [force]` | jCodeMunch indexle + auto-update aktif et |

## 7. Watchdog (uzun suren gorevler)

>=10 dk beklenen her arka plan gorevinde **self-monitoring protokolu** uygulanir. Ayri watchdog agent yok — gorev agent'i kendi kendini izler.

### Protokol (agent prompt'una eklenir)

**Checkpoint (her 5 tool call):**
```bash
mkdir -p /tmp/watchdog
echo '{"task":"TASK","checkpoint":N,"tool_calls":M,"status":"running","last_action":"...","errors":0,"ts":"'$(date -u +%FT%TZ)'"}' > /tmp/watchdog/TASK_ID.json
```

**Self-evaluate (her 10 tool call):**
1. Son 5 tool call'da anlamli ilerleme oldu mu?
2. Ayni hatayi 2+ kez aldim mi?
3. Dongüye girdim mi?

→ ILERLEME VAR: devam + checkpoint
→ ILERLEME YOK: recovery mode

**Recovery mode (max 2 deneme):**
1. Sorunu teshis et (hata mesaji, kok neden)
2. Farkli yaklasim dene (MCP→curl fallback, lock temizle, dependency kur)
3. Basarili → "recovered" logla, devam et
4. 2x basarisiz → **DURDUR**

**Durdurma:**
1. Kullaniciya terminalde kisa ozet dondur
2. `~/Projects/.watchdog/feedback.jsonl`'e kayit ekle
3. `~/Projects/.watchdog/latest.md`'ye okunabilir rapor yaz

**Basari:**
1. Ayni feedback kaydi (outcome: "success", learnings dahil)
2. `/tmp/watchdog/TASK_ID.json` sil

### Feedback log formati

`~/Projects/.watchdog/feedback.jsonl` — append-only, her satir:
```json
{"id":"abc","task":"...","project":"...","model":"...","started":"...","ended":"...","duration_sec":N,"tool_calls":N,"outcome":"success|recovered|failed","recovery_attempts":N,"stuck_reason":null,"resolution":null,"learnings":"..."}
```

### Stale alert

`migration_check.sh` hook'u /tmp/watchdog/ altinda >15dk guncellenmemis heartbeat bulursa terminalde uyari verir.

### Kisa gorevlerde (<10 dk) watchdog baslatma.
