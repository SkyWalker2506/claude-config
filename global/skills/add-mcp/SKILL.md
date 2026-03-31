---
name: add-mcp
description: "Add optional MCP servers after initial install. Triggers: add mcp, mcp ekle, firebase ekle, flutter ekle, unity ekle."
user-invocable: true
---

# Add MCP — Sonradan MCP Sunucusu Ekle

Kurulum sonrasi ek MCP sunuculari ekler. Mevcut olanlar atlanir.

## Kullanim

```
/add-mcp              → mevcut secenekleri listele, kullanici secsin
/add-mcp flutter      → flutter-dev MCP ekle
/add-mcp firebase     → firebase MCP ekle
/add-mcp unity        → Unity MCP ekle (proje bazli)
/add-mcp flutter,firebase → birden fazla ekle
```

## Mevcut Opsiyonel MCP'ler

| Anahtar | MCP | Komut | Not |
|---------|-----|-------|-----|
| `flutter` | flutter-dev | `claude mcp add -s user flutter-dev -- npx -y flutter-dev-mcp` | — |
| `firebase` | firebase | `claude mcp add -s user firebase -e "SERVICE_ACCOUNT_KEY_PATH=$PATH" -- npx -y @gannonh/firebase-mcp` | `FIREBASE_SERVICE_ACCOUNT_PATH` gerekir (secrets.env) |
| `unity` | unity-mcp | Proje bazli kurulum (asagiya bak) | Unity Editor acik olmali |

## Akis

### 1. Arguman kontrolu

Arguman verilmisse → direkt ekle.
Verilmemisse → listeyi goster, kullanici secsin.

### 2. Zaten kurulu mu?

```bash
claude mcp list 2>/dev/null
```

Secilen MCP zaten listedeyse: "flutter-dev zaten kurulu, atlaniyor" de.

### 3. Gereksinim kontrolu

**firebase** icin:
```bash
grep "^FIREBASE_SERVICE_ACCOUNT_PATH=" ~/.claude/secrets/secrets.env 2>/dev/null
```
Yoksa kullaniciya sor:
> Firebase service account JSON dosyasinin yolu nedir?

Cevabi `secrets.env`'e ekle, sonra MCP'yi kur.

**unity** icin:
1. `unity-mcp-cli` kurulu mu?
```bash
command -v unity-mcp-cli
```
Yoksa: `npm install -g unity-mcp-cli`

2. Bulundugun dizin Unity projesi mi?
```bash
ls -d "$(pwd)/Assets" "$(pwd)/ProjectSettings" 2>/dev/null
```
Unity projesi degilse → **KURMA**. Kullaniciya de:
> Bu klasor Unity projesi degil. Unity proje dizininde `/add-mcp unity` calistir.

3. Unity projesi ise:
```bash
unity-mcp-cli install-plugin .
unity-mcp-cli setup-skills claude-code .
```

### 4. Kur

**flutter/firebase:** Tablodan ilgili `claude mcp add` komutunu calistir.
**unity:** Adim 3'teki proje bazli komutu calistir.

### 5. Sonuc

Basarili: "[mcp-adi] MCP eklendi. Yeni oturumda aktif olacak."
Unity icin: "Unity MCP kuruldu. Unity Editor'u ac, Tools > MCP Unity > Server Window'dan serveri baslat."
Basarisiz: hatayi goster, yardimci ol.

## Kaldirma

Kullanici "kaldir" / "remove" derse:
```bash
claude mcp remove -s user <mcp-name>
```
