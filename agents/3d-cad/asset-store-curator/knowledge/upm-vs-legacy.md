# UPM vs Legacy Package Formats

## Quick Comparison

| Feature | `.unitypackage` (Legacy) | UPM `com.*` | Which to Choose |
|---------|-------------------------|------------|-----------------|
| **Import** | Manual (drag-drop) | Auto (manifest.json) | UPM if available |
| **Versioning** | Single version | Pinned to version | UPM (reproducible) |
| **Updates** | Manual re-import | Automatic check + update | UPM (modern) |
| **Location** | Assets/ directory | Packages/ directory | UPM (isolated) |
| **Nested deps** | Manual management | Automatic resolution | UPM (dependency hell) |
| **Old assets** | Common (pre-2018) | Growing (2018+) | Accept both, prefer UPM |

## Legacy `.unitypackage` Format

### What It Is
Zip file containing folder structure mirroring Assets/ layout.
Import action: unpacks into Assets/ directory.
No version tracking; no dependency management.

### How to Identify
- File extension: `.unitypackage`
- Asset Store page: "Download" button (vs "Add to Project")
- Import dialog: "Import Into Project"

### Installation Pattern
```csharp
// Manual import (Editor only)
// 1. Download .unitypackage
// 2. Assets > Import Package > Custom Package
// 3. Select file, click Import
// (No code change needed if asset is self-contained)
```

### Pros
- Works offline
- No external dependencies
- Simple for small assets (single shader, animation pack)

### Cons
- Manual updates (re-download, re-import)
- Conflicts if multiple versions installed
- Asset churn risk (if publisher delists, file lost)
- No dependency tracking

## UPM `com.*` Format

### What It Is
Package stored in Packages/ directory, managed by `manifest.json`.
Package ID: e.g., `com.synty.polygon` or `com.amplify.materialcomposer`.
Automatic dependency resolution and updates.

### How to Identify
- Asset Store page: "Add to Project" button
- manifest.json entry: `"com.publisher.asset": "1.2.3"`
- Packages/ folder entry

### Installation Pattern
```json
// Edit Packages/manifest.json
{
  "dependencies": {
    "com.amplify.materialcomposer": "1.3.2",
    "com.synty.polygon": "2.0.0"
  }
}
```
Then Unity auto-downloads and resolves.

Or use Package Manager UI:
```
Window > TextAsset & Rendering > Package Manager
→ Search "Amplify"
→ Click "Install"
```

### Pros
- Automatic updates available (one-click)
- Version-pinned (reproducible builds)
- Cleaner project structure (Packages/ vs Assets/)
- Dependency resolution (nested dependencies auto-handled)
- Cached locally

### Cons
- Requires internet for initial download
- Slightly more complex (manifest.json management)
- Some old assets don't support UPM yet

## Mixed Projects (UPM + Legacy)

Common in mature projects:

```
Assets/
  ├── Scripts/
  ├── 3D/
  └── Imported/
      ├── LegacyUIKit/          (imported .unitypackage)
      └── OldInputSystem/       (.unitypackage, pre-2019)

Packages/
  ├── manifest.json
  └── (UPM packages auto-managed here)
      ├── com.amplify.color/
      ├── com.synty.polygon/
      └── com.unity.inputsystem/
```

**Good practice:** Prefer UPM for new projects; accept legacy if no UPM version available.

## Migration Path: Legacy → UPM

If upgrading a legacy asset to UPM:

1. **Check if publisher offers UPM version**
   - Asset Store page: search for same name, check for "com.*" variant
   - Example: "Amplify Color" vs "Amplify Color URP" (different packages)

2. **Remove legacy version**
   ```
   Delete Assets/ImportedAsset/ folder
   ```

3. **Add UPM version**
   - Edit `Packages/manifest.json` or use Package Manager UI
   - Version: specify exact version or `latest`

4. **Update code imports** (if needed)
   ```csharp
   // Old (legacy)
   using AmplifyColor;
   
   // New (UPM)
   using AmplifyColor;  // Usually same namespace
   ```

5. **Test thoroughly**
   - Some UPM versions have different default settings
   - Check for namespace conflicts

## Manifest.json Example

```json
{
  "name": "my-game",
  "version": "1.0.0",
  "displayName": "My Game",
  "dependencies": {
    "com.unity.textmeshpro": "3.0.6",
    "com.amplify.materialcomposer": "1.3.2",
    "com.synty.polygon": "2.0.0",
    "com.unity.inputsystem": "1.7.0",
    "com.unity.postprocessing": "3.2.2"
  },
  "description": "Minimal manifest with essential packages"
}
```

## When to Prefer Each

**Use `.unitypackage` (Legacy):**
- Asset not available as UPM
- Old Unity version (pre-2018)
- Asset is self-contained utility (no deps)

**Use UPM `com.*`:**
- Asset publisher offers UPM version
- Modern project (Unity 2018.3+)
- Asset has dependencies
- Team wants reproducible builds

## UPM Registry Discovery

Agent'in bilgisi gereken uc kaynak sistem ve her birinden nasil paket bulunacagi:

### 1. Unity Resmi Registry (Unity Package Manager Registry)

**URL:** `https://packages.unity.com/` — acik web arayuzu yok; tumu Editor icinden veya dokumantasyon uzerinden bulunur.

**Kaynak ve arama stratejileri:**
- **Unity Editor UI:** Window > Package Manager > "Unity Registry" sekmesi (manuel browsing, UI tabanlı)
- **Resmi dokumantasyon:** `https://docs.unity3d.com/Manual/PackagesList.html` — Unity sürümüne gore tüm `com.unity.*` paketlerinin listesi
- **Bireysel paket sayfasi:** `https://docs.unity3d.com/Packages/com.unity.<name>@latest/manual/index.html`
  - Örnek: `https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/manual/index.html`

**Özellikler:**
- Isimlendirme: `com.unity.*` (örn. `com.unity.addressables`, `com.unity.cinemachine`)
- Ücretsiz, tamamı resmi Unity desteği
- Sürüm sabitleme ve otomatik güncellemeler
- Unity sürümüne gore derlenmiş ve test edilmiş

**Avantajları:**
- En guvenli ve stabil
- Dokümantasyon ve destek garantili
- Bağımlılık çözünürlüğü bilinir
- Sürüm uyumluluğu kontrol edilir

### 2. OpenUPM (Topluluk Kurasyonlu Registry)

**URL:** `https://openupm.com/` — tam fonksiyon web UI + API var.

**Arama stratejileri:**
- **Web tarama:** https://openupm.com/?q=<terimler> (manuel arama, filtreleme)
- **API sorgusu:** `https://api.openupm.com/search-v2?q=<terimler>` — JSON döner; ad, aciklama, indir sayisi, yildiz sayisi iceriyor
  - Örnek: `https://api.openupm.com/search-v2?q=async` → `[{name: "com.cysharp.unitask", downloads: 15000, stars: 450, ...}]`
- **Paket detaylari:** `https://api.openupm.com/packages/<paketad>` → versiyonlar, bağımlılıklar, GitHub linki
  - Örnek: `https://api.openupm.com/packages/com.cysharp.unitask`

**Kurulum:**
- **CLI:** `openupm add <name>` — manifest.json otomatik duzenler
- **Manuel:** `Packages/manifest.json` icine `scopedRegistries` ve `dependencies` ekle:
  ```json
  {
    "scopedRegistries": [
      {
        "name": "openupm",
        "url": "https://package.openupm.com",
        "scopes": ["com.cysharp.*"]
      }
    ],
    "dependencies": {
      "com.cysharp.unitask": "2.5.1"
    }
  }
  ```

**Özellikler:**
- Acik kaynak ve topluluk paketleri (MIT, genelde)
- Degisken kalite ama seçilmis; cüruf az
- Indir sayisi ve yildiz orani ile ranking

**Avantajlari:**
- Assert Store alternatifleri sik daha iyi (bağımsız gelistirme, daha çabuk güncelleme)
- Tümü ücretsiz
- Licans sorunları sik (MIT, Apache, GPL net)
- Aktif topluluk bakımı

### 3. Git UPM Paketleri

**Kaynak:** GitHub (veya başka Git sunucu) — sadece `package.json` dosyası root'ta olan repo'yu paket olarak kurabilir.

**Kurulum:**
Manifest icine doğrudan Git URL'i:
```json
{
  "dependencies": {
    "com.cysharp.unitask": "https://github.com/Cysharp/UniTask.git"
  }
}
```

**Arama stratejileri:**
- **GitHub arama:** `path:package.json "com.*"` — Git UPM paketleri bul
- **Ortak ornekler:**
  - Cysharp UniTask: `https://github.com/Cysharp/UniTask.git`
  - Graphy (profiler görselleştirme): `https://github.com/Tayx94/graphy.git`
  - Naughty Attributes (Inspector UI): `https://github.com/dbrizov/NaughtyAttributes.git`

**Özellikler:**
- Depo doğrudan Git #tag veya #branch ile versionlanır
- Herhangi GitHub repo'su paket olabilir (MIT degil ise dikkat et)
- En "keskin" - en yeni features ama test edilmemiş olabilir

**Avantajlari:**
- Acık source garantisi (kod görün)
- Degişiklik takibi (Git history)
- Niche / cutting-edge paketler

---

### Agent Arama Önceligi (Kullanıcı Bir İhtiyaç Sordiginda)

Kaynakları **bu sirayla** kontrol et:

1. **Unity Resmi Registry** — açık, stabil, destekli; sık çözüm var
2. **OpenUPM** — assert Store'dan çogu kez daha iyi, tamamı ücretsiz, kurasyonlu
3. **Asset Store** (sadece OpenUPM/Official kaynaklari yeterli degil) — ücretsiz paketler (parasal, legacy)
4. **Git UPM** — niş ihtiyaçlar, cutting-edge

---

### Ortak İhtiyaçlar ve En İyi Kaynak

| İhtiyaç | En iyi kaynak | Paket ID | Sebep |
|--------|---|---|---|
| Async/await, coroutine yok | OpenUPM + Git | `com.cysharp.unitask` | Endüstri standardı, MIT, 15k+ indir |
| Addressables (asset loading) | Unity Resmi | `com.unity.addressables` | First-party, sürüm-sabitlenymiş |
| Cinemachine (kamera) | Unity Resmi | `com.unity.cinemachine` | First-party, 3.x modern |
| UI layout (UI Toolkit) | Unity Resmi | `com.unity.ui` | First-party |
| Lokalizasyon | Unity Resmi | `com.unity.localization` | First-party, multilingual |
| Durum makinası | OpenUPM | `com.xesmedia.fsm` | Ücretsiz, NodeCanvas alternatifi |
| Profiler görselleştirme | Git UPM | `github.com/Tayx94/graphy` | MIT, hafif |
| Input (yeni sistem) | Unity Resmi | `com.unity.inputsystem` | First-party |
| AI Navigation | Unity Resmi | `com.unity.ai.navigation` | First-party |
| VFX Graph | Unity Resmi | `com.unity.visualeffectgraph` | First-party |

---

### Manifest.json Desenler

**Unity Resmi Registry (sadece dependency):**
```json
{
  "dependencies": {
    "com.unity.addressables": "1.21.0",
    "com.unity.cinemachine": "3.0.0"
  }
}
```

**OpenUPM paketleri (scopedRegistry gerekli):**
```json
{
  "scopedRegistries": [
    {
      "name": "openupm",
      "url": "https://package.openupm.com",
      "scopes": ["com.cysharp.*"]
    }
  ],
  "dependencies": {
    "com.cysharp.unitask": "2.5.1"
  }
}
```

**Git UPM (doğrudan URL):**
```json
{
  "dependencies": {
    "com.cysharp.unitask": "https://github.com/Cysharp/UniTask.git#v2.5.1"
  }
}
```

---

### Sürüm Sabitleme

UPM paketleri **tam sürüm sabitleme** destekler (Asset Store `.unitypackage` olamaz):

- `"com.unity.addressables": "1.21.0"` — tam sürüm (önerilen)
- `"com.unity.addressables": "1.21"` — minor sabitleme
- `"com.unity.addressables": "1"` — major sabitleme
- `"com.unity.addressables": "latest"` — her zaman güncelle (üretim icin önerilmez)

Git UPM'de:
- `"https://github.com/Cysharp/UniTask.git#v2.5.1"` — tag sürümü
- `"https://github.com/Cysharp/UniTask.git#main"` — branch (yaşayan, test edilmemis)
- `"https://github.com/Cysharp/UniTask.git"` — en son commit (en riskli)
