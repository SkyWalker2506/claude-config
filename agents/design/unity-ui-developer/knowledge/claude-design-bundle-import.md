---
last_updated: 2026-04-18
confidence: high
sources: 4
---

# Claude Design Bundle Import

## Quick Reference

| Kavram | Not |
|--------|-----|
| Bundle yapısı | components[], design tokens, HTML, interactions, README |
| Mapping hedefi | HTML → UXML, tokens → USS variables |
| Caching strateji | Proje hash-tabanlı cache ile depolanır |
| Risk | Flex/Grid mismatch, z-index eksikliği, hover state yönetimi |

## Bundle Yapısı

Claude Design handoff bundle aşağıdaki içeriği içerir:

```json
{
  "components": [
    {
      "name": "MainMenu",
      "html": "<div class=\"menu\">...</div>",
      "css": ".menu { ... }",
      "interactions": [{ "event": "click", "action": "navigate" }]
    }
  ],
  "designTokens": {
    "colors": { "primary": "#007AFF", "text": "#333333" },
    "spacing": { "sm": "8px", "md": "16px", "lg": "24px" },
    "radii": { "default": "4px", "large": "12px" },
    "typography": { "body": "14px/1.5", "heading": "24px/1.2 bold" }
  },
  "readme": "...",
  "version": "1.0.0"
}
```

## Bundle Indirme

Bundle API'den curl ile indir:

```bash
BUNDLE_URL="https://design.example.com/api/bundles/your-project-id"
curl -H "Authorization: Bearer $TOKEN" "$BUNDLE_URL" > bundle.json
```

## HTML → UXML Mapping Tablosu

| HTML | UXML | Not |
|------|------|-----|
| `<div>` | `<VisualElement>` | Genel konteyner |
| `<button>` | `<Button>` | İnteraktif buton |
| `<input>` | `<TextField>` | Metin girdisi |
| `<label>` | `<Label>` | Statik metin |
| `<img>` | `<VisualElement>` + `background-image` | Arka plan görseli |
| `<ul><li>` | `<ListView>` | Dinamik liste |
| `<select>` | `<DropdownField>` | Açılır menü |
| `<section>` | `<VisualElement>` + class | Semantik bölüm |

## Design Tokens → USS Variables

Design token'ları `:root` USS scope'unda tanımla:

```uss
:root {
  --color-primary: #007AFF;
  --color-text: #333333;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --radius-default: 4px;
  --radius-large: 12px;
  --font-body: 14px;
  --font-heading: 24px;
  --font-weight-bold: bold;
}
```

## Component → UXML Hiyerarşisi Dönüşümü

Örnek HTML bileşen:

```html
<div class="card">
  <h2>Title</h2>
  <p>Description</p>
  <button class="btn-primary">Click me</button>
</div>
```

Karşılık gelen UXML:

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
  <VisualElement class="card">
    <Label text="Title" class="heading" />
    <Label text="Description" class="body" />
    <Button text="Click me" class="btn-primary" />
  </VisualElement>
</ui:UXML>
```

USS sınıfları:

```uss
.card {
  flex-direction: column;
  padding: var(--spacing-md);
  background-color: #ffffff;
  border-radius: var(--radius-default);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card > .heading {
  font-size: var(--font-heading);
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.card > .body {
  font-size: var(--font-body);
  color: var(--color-text);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-default);
  font-size: var(--font-body);
  font-weight: var(--font-weight-bold);
}

.btn-primary:hover {
  opacity: 0.85;
}
```

## Proje Cache Stratejisi

Bundle'ı hash-tabanlı cache'de depolamak:

```
<project>/.unity-craft/design-cache/
  ├── <bundle-hash>/
  │   ├── bundle.json
  │   ├── components/
  │   │   ├── MainMenu.uxml
  │   │   ├── MainMenu.uss
  │   │   └── Dialog.uxml
  │   └── tokens.uss
  └── metadata.json
```

Metadata cache dosyası:

```json
{
  "bundles": {
    "https://design.example.com/api/bundles/abc123": {
      "hash": "sha256-hash-value",
      "cached_at": "2026-04-18T10:30:00Z",
      "version": "1.0.0"
    }
  }
}
```

## Kod Örneği: Bundle → UXML/USS Dönüşümü

```csharp
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text.Json;
using UnityEngine;

public class DesignBundleImporter
{
    public static void ImportBundle(string bundleUrl, string projectCachePath)
    {
        var bundleJson = FetchBundle(bundleUrl);
        var hash = ComputeHash(bundleJson);
        var cachePath = Path.Combine(projectCachePath, hash);
        Directory.CreateDirectory(cachePath);
        
        File.WriteAllText(Path.Combine(cachePath, "bundle.json"), bundleJson);
        
        using var doc = JsonDocument.Parse(bundleJson);
        var root = doc.RootElement;
        
        // Tokens → USS
        var tokensUss = GenerateTokensUss(root.GetProperty("designTokens"));
        File.WriteAllText(Path.Combine(cachePath, "tokens.uss"), tokensUss);
        
        // Components → UXML/USS
        var componentsDir = Path.Combine(cachePath, "components");
        Directory.CreateDirectory(componentsDir);
        
        foreach (var component in root.GetProperty("components").EnumerateArray())
        {
            var name = component.GetProperty("name").GetString();
            var uxml = HtmlToUxml(component.GetProperty("html").GetString());
            var uss = component.GetProperty("css").GetString();
            
            File.WriteAllText(Path.Combine(componentsDir, $"{name}.uxml"), uxml);
            File.WriteAllText(Path.Combine(componentsDir, $"{name}.uss"), uss);
        }
        
        Debug.Log($"Bundle imported to {cachePath}");
    }
    
    private static string ComputeHash(string content)
    {
        using var sha = SHA256.Create();
        var hash = sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(content));
        return "sha256-" + System.Convert.ToHexString(hash).ToLower();
    }
    
    private static string GenerateTokensUss(JsonElement tokens)
    {
        var uss = ":root {\n";
        foreach (var category in tokens.EnumerateObject())
        {
            foreach (var token in category.Value.EnumerateObject())
            {
                var varName = $"--{category.Name}-{token.Name}";
                uss += $"  {varName}: {token.Value.GetString()};\n";
            }
        }
        uss += "}";
        return uss;
    }
    
    private static string HtmlToUxml(string html)
    {
        // Basit HTML → UXML dönüştürücü (production'da HtmlAgilityPack kullan)
        var uxml = html
            .Replace("<div", "<VisualElement")
            .Replace("</div>", "</VisualElement>")
            .Replace("<button", "<Button")
            .Replace("</button>", "</Button>")
            .Replace("<input", "<TextField");
        
        return $"<ui:UXML xmlns:ui=\"UnityEngine.UIElements\">\n{uxml}\n</ui:UXML>";
    }
    
    private static string FetchBundle(string url)
    {
        using var client = new System.Net.Http.HttpClient();
        var response = client.GetAsync(url).Result;
        return response.Content.ReadAsStringAsync().Result;
    }
}
```

## Sık Karşılaşılan Hatalar

| Hata | Çözüm |
|------|-------|
| Flex vs Grid Mismatch | HTML'deki `display: grid` → UXML'de `flex-direction` yerine `display: grid` stil kullan (UIE compat mode) |
| Z-Index Eksikliği | UI Toolkit hiyerarşiye dayalı; `order: N` veya parent reorder kullan |
| Hover State Yönetimi | `:hover` pseudo-class yerine C# event listener veya Unity stylesheets'te `#element:hover` |
| Media Query Yok | Runtime viewport değişiklikleri için `Panel.onSizeChange` event'i oku; statik breakpoint CSS yaz |
| Rem/Em Birim Sorunu | UI Toolkit px cinsinden çalışır; `font-size: 14px` olarak dönüştür |

## Kaynaklar

- [Bundle API Docs](https://design.example.com/docs) — authentication token alma
- [UI Toolkit USS Reference](https://docs.unity3d.com/Manual/UIE-USS-Selectors.html) — selector ve pseudo-class syntax
- [UXML Manual](https://docs.unity3d.com/Manual/UIE-UXML.html) — element mapping
