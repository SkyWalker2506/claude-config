---
name: download-repos
description: "Git'ten repoları indir — DownloadEssentials, DownloadClaude, DownloadSDK, DownloadAll. Triggers: download repos, repo indir, repoları çek, clone repos, git clone all."
argument-hint: "[DownloadEssentials|DownloadClaude|DownloadSDK|DownloadAll]"
user-invocable: true
---

# /download-repos — Repo İndirici

`projects.json` + GitHub MCP ile repoları `~/Projects/` altına clone'la veya pull yap.

## Argüman yoksa

Seçenekleri göster:

```
Hangi set indirilsin?

  DownloadEssentials  — Temel config + hub repoları
  DownloadClaude      — Claude ekosistemi repoları
  DownloadSDK         — SDK ve API repoları
  DownloadAll         — projects.json'daki tüm repolar
```

## Repo Setleri

### DownloadEssentials
Çalışmak için gereken minimum set:
- `SkyWalker2506/claude-config`
- `SkyWalker2506/ClaudeHQ`
- `SkyWalker2506/claude-secrets` → `~/.claude/secrets/` altına indir (private repo)

### DownloadClaude
Claude ekosistemi:
- `SkyWalker2506/claude-config`
- `SkyWalker2506/ClaudeHQ`
- `SkyWalker2506/claude-marketplace`

### DownloadSDK
SDK, API ve entegrasyon repoları:
- `SkyWalker2506/claude-marketplace`
- `SkyWalker2506/ar-research`

### DownloadAll
`~/Projects/ClaudeHQ/projects.json` içindeki tüm `git` alanına sahip repolar.

## Akış

### 1. GitHub login kontrol

```bash
gh auth status
```

- **Login yok** → Kullaniciya soyle:
  > `! gh auth login --web -p https` komutunu çalıştır, sonra tekrar dene.
  Dur, devam etme.

### 2. Kullanıcı adını al

```bash
GH_USER=$(gh api user -q .login)
```

### 3. Her repo için — clone veya pull

```bash
PROJECTS="$HOME/Projects"
REPO="<org>/<repo-name>"
DEST="$PROJECTS/<repo-name>"

if [ -d "$DEST/.git" ]; then
  echo "↻ Pull: $REPO"
  git -C "$DEST" pull --ff-only
else
  echo "⬇ Clone: $REPO"
  gh repo clone "$REPO" "$DEST"
fi
```

Bash tool ile her repo için sırayla çalıştır. Paralel değil — çıktı takibi için sıralı.

### 4. Özet tablo göster

```
| Repo               | İşlem  | Durum |
|--------------------|--------|-------|
| claude-config      | clone  | ✅    |
| ClaudeHQ           | pull   | ✅    |
| claude-marketplace | clone  | ✅    |
```

### 5. DownloadAll sonrası install.sh öner

> `claude-config` reposu indirildi. `./install.sh` çalıştırıp config'i kurmak ister misin?

Evet → `cd ~/Projects/claude-config && ./install.sh`

## Kurallar

- `gh repo clone` kullan — SSH key gerekmez, token yeterli
- Hata olursa atla, listeye `❌ (hata mesajı)` yaz, devam et
- `claude-secrets` reposu **istisnası**: `~/Projects/` değil `~/.claude/secrets/` altına indir
- Secret değerlerini terminale yazma
