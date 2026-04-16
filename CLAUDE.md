# claude-config — Calisma Kurallari

> Degisiklik: bu repoda duzenle → `./install.sh` → commit + push. `~/.claude/` altini dogrudan duzenleme.

## Calisma kurallari (tum projeler)

## Dispatch-First Rule

Non-trivial görevlerde: classify → lane seç → dispatch → bekle.

- Coding/terminal/git → Codex CLI'a pasla
- Research/architecture → claude sub-agent'a pasla  
- Multimodal (DALL-E vb.) → human_in_loop handoff üret
- API billing gerektiren → varsayılan policy ile reddet
- Kendim yapmak yerine dispatch et; dispatch sonrası aggregator ol

### Davranis Kurallari
> Calisma tarzi, tool kullanimi, model secimi, dil kurallari → `global/charter.md`

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
| `SECRETS_MISSING` | `~/Projects/claude-config/claude-secrets/secrets.env` duzenle, commit + push |
| `SECRETS_NONE` | `install.sh` calistir veya `claude-secrets/secrets.env` olustur |
| `CONFIG_UPDATE` | Kullaniciya sor: git pull + install.sh + restart |
| `BIND_NEEDED` | `/bind` calistir — global CLAUDE.md'yi claude-config'e bagla |

### 6. Secrets guvenligi
> Detaylar → `global/charter.md` Secrets bolumu

### 7. Skill'ler
> Detaylar → `global/charter.md` Skill'ler bolumu

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

#### 8f. Plugin ekleme (zorunlu checklist)

Yeni bir ccplugin eklendiginde **hepsi** guncellenmeli — tek dosya yetmez:

1. `config/plugin-registry.json` — plugin kaydi
2. `README.md` (claude-config) — plugin tablosu + sayi
3. `github.com/SkyWalker2506/claude-marketplace` README — plugin tablosu + sayi (GitHub MCP ile)

#### 8g. Bootstrap (setup eksikse)

```
repo yapisi → paket yoneticisi → bagimliliklar → .env.example → calistir/build
```

- Self-healing: §9d kurali gecerli
- Mantikli varsayimlarla ilerle; her adimda sorma
- `.claudeignore` yoksa → `~/Projects/claude-config/templates/claudeignore.template` kopyala

#### 8g-1. Versiyon yönetimi (tüm uygulamalar)

- Her projede `version` sabiti veya `pubspec.yaml` / `package.json` versiyonu bulunmalı
- **Her deploy/build öncesi versiyonu artır** — kullanıcı değişikliğin yansıyıp yansımadığını görebilsin
- Versiyon formatı: `vMAJOR.MINOR.PATCH` (örn. `v2.5.0`)
- Küçük fix/tweak → PATCH artır (`v2.5.0` → `v2.5.1`)
- Yeni özellik → MINOR artır (`v2.5.0` → `v2.6.0`)
- Büyük değişiklik → MAJOR artır

#### 8h. Rapor işleme protokolü

> Raporlar `~/Projects/claude-config/Reports/` altinda `.md` dosyalari olarak bulunur.
> Hook: `config/reports_check.sh` → SessionStart'ta `REPORTS_PENDING` sinyali uretir.

**Rapor yasam dongusu:** `UNPROCESSED → IN_PROGRESS → DONE → Processed/`

**REPORTS_PENDING sinyali geldiginde — ZORUNLU ilk yanit akisi:**

**Adim 0 — Proaktif bildirim (kullanicinin ilk mesajina verilen yanit basinda):**
Kullanici ne yazarsa yazsin, yanit basina ekle:

```
📋 N rapor bekliyor:
  • [HIGH] 001_dosya_adi.md — [raporu okuyup 1 cumle ozet yaz]
  Aksiyonlar: [Required Actions tablosundaki madde sayisi] degisiklik

Uygulayayim mi? (Evet / Hayir / Sonraki oturuma birak)
```

Kullanici "evet" / "uygula" / "hayata gecir" → Adim 1'e gec.
Kullanici "hayir" / "atlat" / "sonra" → UNPROCESSED birak, konuya devam et.
Kullanici baska bir konudan devam ederse → sormadan sor, asla otomatik isleme.

**Adim 1 — Raporu oku ve onizleme goster:**
```
Rapor: 001_dosya_adi.md ([HIGH], [tarih])
Yapilacaklar:
  1. projects/XXX.md §2 — [ne degisecek]
  2. agents/YYY.md — [ne degisecek]
  3. config/ZZZ.sh — [ne degisecek]
Hayata gecireyim mi?
```

**Adim 2 — Onay geldikten sonra isle:**
1. `Status: IN_PROGRESS` olarak guncelle
2. Her aksiyonu sirayla uygula:
   - Hedef dosya var mi kontrol et
   - Degisikligi yap
   - Basarisizsa notu rapor altina ekle, sonraki aksiyona gec
3. Tum aksiyonlar bittikten sonra:
   - `Status: DONE` olarak guncelle
   - `REPORTS_SUMMARY.md` tablosuna yeni satir ekle: `| N | dosya.md | tarih | oncelik | 1 cumle ozet |`
   - Dosyayi `Reports/Processed/` klasorune tasi
4. Kullaniciya bildir: "X rapor islendi, Y dosya degisti. [Degistirilen dosyalar listesi]"

**Ozel durumlar:**

| Durum | Aksiyon |
|-------|---------|
| `REPORTS_STALE` sinyali | Crash recovery — raporu oku, hangi aksiyonlar uygulanmis kontrol et, kalindan devam et |
| Hedef dosya bulunamadi | Aksiyonu atla, nota yaz, sonrakine gec |
| Kullanici "isleme" / "atla" derse | UNPROCESSED birak |
| 5+ rapor bekliyor | Once Critical/High — token butcesi asarsa geri kalanini sonraki oturuma birak |

**Rapor olusturma:** `Reports/TEMPLATE.md` sablonunu kullan. Dosya adi: `NNN_kisa_baslik.md` (NNN = siradaki numara).

### 9. Task Discipline & Watchdog
> Gorev parcalama, self-monitoring, overrun detection, recovery → `global/harness.md`

---

### 10. Session sonu — ders cikarma
> Detaylar → `global/harness.md`

### 11. Multi-Agent Sistemi
> Agent dispatch, routing, sub-agent watchdog, review pipeline → `global/harness.md`
