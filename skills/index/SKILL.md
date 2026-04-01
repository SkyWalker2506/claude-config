---
name: index
description: jCodeMunch ile mevcut projeyi indexle. Otomatik index guncellemeyi de aktif eder.
argument-hint: "[force] — force ile mevcut indexi sifirdan olusturur"
---

# /index — jCodeMunch Proje Indexleme

Mevcut calisma dizinini jCodeMunch ile indexler. Ayni zamanda otomatik index guncellemeyi aktif eder — bundan sonra bu klasorde her Claude oturumu basinda index sessizce guncellenir.

## Kullanim

```
/index          → indexle (varsa guncelle, yoksa olustur) + auto-update aktif et
/index force    → mevcut indexi sil, sifirdan olustur
```

## Arguman

```
$ARGUMENTS
```

`force` kelimesi varsa sifirdan indexle. Yoksa incremental guncelleme.

## Akis

### 1. jCodeMunch MCP kontrol

jCodeMunch MCP bagli mi kontrol et (ToolSearch "jcodemunch"). Bagli degilse:
```
jCodeMunch MCP bagli degil. Indexleme yapilamaz.
Global settings.json'da jcodemunch tanimli mi kontrol et, yoksa ekle.
```

### 2. Index islemi

```python
# a. Repo coz
resolve_repo(path=os.getcwd())

# b. Indexle
index_folder(path=os.getcwd())
```

`force` argumani varsa once mevcut indexi temizle:
```python
# force modda once temizle
# (jcodemunch otomatik yeniden olusturur)
index_folder(path=os.getcwd(), force=True)  # veya reindex parametresi varsa
```

### 3. Marker olustur/guncelle

```bash
mkdir -p .claude && date -u +%FT%TZ > .claude/jcodemunch_indexed
```

Bu marker'in varligi, `migration_check.sh` hook'una "bu proje indexli, her oturum basinda guncelle" sinyali verir.

### 4. Sonuc

```
jCodeMunch index tamamlandi.
- Proje: [dizin adi]
- Otomatik guncelleme: aktif (her oturum basinda sessizce guncellenir)
- Manuel guncelleme: /index
```

## Notlar

- Index ilk kez olusturulurken buyuk projelerde 10-30sn surebilir
- Sonraki guncellemeler incremental — sadece degisen dosyalar, cok hizli
- `.claude/jcodemunch_indexed` dosyasi `.gitignore`'da olmali (yerel state)
