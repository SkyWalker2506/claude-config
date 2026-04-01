---
name: bind
description: claude-config baglantisi kur — global CLAUDE.md'yi yonlendiriciye cevir, mevcut icerigi tasit
user_invocable: true
trigger_phrases:
  - /bind
  - bind
  - bagla
  - baglanti kur
  - connect config
---

# /bind — claude-config Baglanti Kurulumu

Bu skill, global `~/.claude/CLAUDE.md` dosyasini `~/Projects/claude-config` reposuna baglar. Tum kurallar ve konfigürasyon claude-config'den yonetilir hale gelir.

## Adim adim akis

Asagidaki adimlari **sirayla ve kullaniciya sorarak** uygula. Her adimda kullanicinin onayini al.

### Adim 1: Durum kontrolu

1. `~/.claude/CLAUDE.md` dosyasinin varligini kontrol et
2. `~/Projects/claude-config/CLAUDE.md` dosyasinin varligini kontrol et
3. Mevcut global CLAUDE.md'de "claude-config/CLAUDE.md dosyasini oku" ifadesi var mi kontrol et

Eger baglanti zaten kuruluysa → "Baglanti zaten aktif. Islem gerekmiyor." de ve dur.

### Adim 2: Baglanti onayi

Kullaniciya sor:

> claude-config baglantisi kurulsun mu? Bu islem:
> - Global CLAUDE.md'yi sadece yonlendirici yapacak
> - Tum kurallar ~/Projects/claude-config/CLAUDE.md'den okunacak
> - Config degisiklikleri sadece claude-config reposu uzerinden yapilacak
>
> Devam edeyim mi?

Hayir derse → dur.

### Adim 3: Mevcut icerik analizi

1. `~/.claude/CLAUDE.md` dosyasini oku
2. Icerigini `~/Projects/claude-config/CLAUDE.md` ile karsilastir
3. Kullaniciya rapor ver:

> Mevcut global CLAUDE.md'de su icerikler var:
> - [bolum listesi]
>
> claude-config/CLAUDE.md'de zaten mevcut olanlar: [liste]
> Eksik olup tasinmasi gerekenler: [liste]
> Tasiyayim mi?

Tasinacak icerik yoksa → "Tum icerik zaten claude-config'de. Dogrudan yonlendirici yaziyorum." de, Adim 5'e atla.

### Adim 4: Icerik tasima

1. Eksik icerikleri `~/Projects/claude-config/CLAUDE.md` dosyasina ekle (uygun bolume)
2. Kullaniciya ne eklendigini 1-2 satirda ozetle

### Adim 5: Yonlendirici yazma

1. `~/Projects/claude-config/global/CLAUDE.md` dosyasini yonlendirici icerigi ile guncelle:

```markdown
# Global Claude — Yonlendirici

> **Bu dosya sadece yonlendiricidir.** Tum kurallar, skill tanimlari ve konfigürasyon detaylari `~/Projects/claude-config/CLAUDE.md` dosyasindadir.

---

## Her oturum basinda

1. **`~/Projects/claude-config/CLAUDE.md` dosyasini oku** ve talimatlarini uygula — bu okuma yapilmadan hicbir kural uygulanmaz ve hicbir kod yazilmaz
2. Yanit basinda model etiketi: `(Model Adi)`
3. Dil: kullaniciya Turkce; kod/commit Ingilizce

## Config degisikligi

Degisiklik yapmak icin `~/Projects/claude-config/` reposunda duzenle → `./install.sh` calistir.
**`~/.claude/` altindaki dosyalari dogrudan duzenleme** — `install.sh` ile ezilir.

## Migration sinyalleri

| Sinyal | Aksiyon |
|--------|---------|
| `INSTALL_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` + `/restart` |
| `MCP_SETUP_NEEDED` | `cd ~/Projects/claude-config && ./install.sh` + `/restart` |
| `MIGRATION_NEEDED` | `/migration` calistir |
| `MIGRATION_UPDATE` | Delta uygula, versiyon guncelle |
| `SECRETS_MISSING` | `~/.claude/secrets/secrets.env` duzenle |
| `SECRETS_NONE` | `install.sh` calistir veya secrets.env olustur |
| `CONFIG_UPDATE` | Kullaniciya sor: git pull + install.sh |
| `BIND_NEEDED` | `/bind` calistir — claude-config baglantisi kur |

## Secrets

- Secret degerleri **ASLA** konusma ciktisina, commit'e, public dosyaya veya log'a yazilmaz
- Secret'lar yalnizca `~/.claude/secrets/` altinda
```

2. `install.sh` calistir → yonlendirici `~/.claude/CLAUDE.md`'ye kopyalanir

### Adim 6: Dogrulama

1. `~/.claude/CLAUDE.md` dosyasini oku, yonlendirici icerigini dogrula
2. Kullaniciya bildir: "Baglanti kuruldu. Artik tum kurallar ~/Projects/claude-config/CLAUDE.md'den okunuyor."

## Onemli

- **Her adimda kullanici onayi al** — otomatik ilerleme
- Mevcut icerikte kullanicinin elle ekledigi ozel kurallar olabilir — bunlari kaybetme
- `install.sh` calistirmadan once degisiklikleri claude-config reposunda commit et
