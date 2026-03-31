---
name: admin-login
description: "GitHub authentication and account management. Login, switch accounts, check auth status. Triggers: login, gh auth, github login, admin login, hesap degistir."
user-invocable: true
---

# Admin Login — GitHub Authentication

GitHub CLI ile kimlik dogrulama, hesap yonetimi ve repo-bazli hesap ayari.

## Calisma Akisi

### 1. Durum Kontrolu

```bash
gh auth status
```

Sonuca gore:
- **Giris yapilmamis** → Adim 2'ye git
- **Giris yapilmis** → Kullaniciya aktif hesabi goster, ne yapmak istedigini sor

### 2. Giris (interaktif — kullanici calistirir)

Kullaniciya soyle:

> GitHub'a giris yapmak icin asagidaki komutu calistir:
> ```
> ! gh auth login --web -p https
> ```
> Browser acilacak, GitHub'da onaylayinca giris tamamlanir.

**Not:** `!` prefixi komutu bu session'da calistirir, ciktiyi dogrudan konusmaya getirir.

### 3. Coklu Hesap Yonetimi

Farkli repolar farkli GitHub hesaplarina ait olabilir:
- `claude-config` → SkyWalker2506 (veya baska bir admin hesabi)
- Proje repolari → kullanicinin kendi hesabi

#### Aktif hesabi goster
```bash
gh auth status
gh api user -q .login
```

#### Baska hesap ekle
```
! gh auth login --web -p https
```
(Farkli hesapla giris yapar, mevcut hesabi korur)

#### Hesaplar arasi gecis
```bash
gh auth switch --user <KULLANICI_ADI>
```

#### Belirli repo icin hesap ayarla
```bash
# Proje reposu icin kendi hesabini kullan
cd ~/Projects/MyApp
git remote set-url origin https://<KULLANICI>@github.com/<KULLANICI>/MyApp.git

# claude-config icin admin hesabini kullan
cd ~/Projects/claude-config
git remote set-url origin https://SkyWalker2506@github.com/SkyWalker2506/claude-config.git
```

#### Git credential helper ayarla (repo-bazli)
```bash
# GitHub CLI'yi credential helper olarak kullan
gh auth setup-git
```

### 4. Dogrulama

Giris sonrasi kontrol:
```bash
gh auth status
gh api user -q '.login'
gh repo list --limit 3
```

Basarili ise kullaniciya bildir:
> GitHub'a [KULLANICI] olarak giris yapildi. Push/pull hazir.

### 5. Push Testi (opsiyonel)

Kullanici isterse mevcut repo icin push testi:
```bash
git remote -v
git push --dry-run
```

## Onemli

- `gh auth login` interaktif — kullanici `!` ile calistirmali, Claude dogrudan calistiramaz
- Secret/token degerleri terminale yazma
- Birden fazla hesap eklenebilir, `gh auth switch` ile gecis yapilir
- Her repo'nun remote URL'i hangi hesabi kullanacagini belirler
