---
name: install
description: "Run claude-config installer. Asks questions via Claude, then runs install.sh with correct flags. Triggers: install, kurulum, setup config."
user-invocable: true
---

# Install — claude-config Kurulum

Claude Code icinden install.sh'i calistir. Interaktif sorulari Claude sorar, sonra script'e arguman olarak gecirir.

## Akis

### 1. Platform ve durum kontrolu

```bash
uname -s
gh auth status 2>&1
ls ~/.claude/secrets/secrets.env 2>/dev/null
```

### 2. Kullaniciya sor

Sirasıyla sor (zaten ayarliysa atlama):

**A. Proje kok dizini:**
> Proje kok dizinin nedir? (macOS varsayilan: ~/Projects, Windows: ~/Documents/GitHub)

**B. GitHub login** (gh auth status basarisizsa):
> GitHub'a login olmak ister misin? Login icin calistir:
> ```
> ! gh auth login --web -p https
> ```
> Login tamamlaninca "tamam" yaz.

Login istemezse → `--skip-login` flag kullan.

**C. Secrets** (secrets.env yoksa):
> Private secrets repon var mi? Varsa URL'yi yaz, yoksa "yok" de.

- URL verdiyse → `--secrets-repo URL`
- "yok" dediyse → `--skip-secrets`

### 3. install.sh calistir

Topladığın cevaplardan komutu olustur:

```bash
cd ~/Projects/claude-config && bash ./install.sh --auto --root <CEVAP_A> [--skip-login] [--skip-secrets] [--secrets-repo <URL>]
```

`--auto` her zaman ekle — script'in kendi read -p'leri calismaz, tum parametreler arguman olarak gecer.

### 4. Sonuc

Script ciktisini goster. Hata varsa yardimci ol.
Basarili ise: "Kurulum tamamlandi." de.

## Kurallar

- Script her zaman `--auto` ile calistirilir
- Kullanici bilgisi eksikse **Claude sorar**, script'e sormadan gecirir
- Zaten ayarli olan seyler (login var, secrets var) icin soru sorma
- Secret degerleri terminale yazma
