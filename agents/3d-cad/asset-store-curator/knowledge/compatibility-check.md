# Compatibility Check Patterns

## Unity Version Compatibility

### Check Before Download

1. **Asset Store Page**
   - "Supported Unity Versions" field (official source)
   - Example: "Unity 2019.4 LTS, 2020.3 LTS, 2021 LTS, 2022 LTS, 6"

2. **Version Compatibility Matrix**
   | Asset | 2020.3 | 2021 LTS | 2022 LTS | 6 | 7+ |
   |-------|--------|----------|----------|---|-----|
   | Synty POLYGON | ✓ | ✓ | ✓ | ✓ | ? |
   | Amplify Color | ✓ | ✓ | ✓ | ✓ | ⚠ |
   | NGUI | ✓ | ✓ | ⚠ | ✗ | ✗ |

   Legend: ✓ = confirmed working, ⚠ = reported issues, ✗ = incompatible, ? = untested

3. **Red Flags**
   - No mention of Unity 6 support (asset may be abandoned)
   - Only supports versions >2 years old (risky for current projects)
   - "Last update: 2021" + "Supports up to 2022" = outdated

### Minimum Version Strategy

Development: Use minimum officially supported version.
Shipping: Target LTS version + one version newer.

Example for 2026 project:
- Dev environment: Unity 2022 LTS (stable for daily work)
- Shipping target: 2022 LTS (maximize compatibility)
- Asset requirement: "2020.3 LTS or newer" (covers both)

## Render Pipeline Compatibility

Unity supports three render pipelines. Asset must match target.

| Pipeline | Abbr | Typical Use | Asset Support |
|----------|------|------------|---------------|
| Built-in Render Pipeline | Default | Legacy, learning, simple games | Common (older assets) |
| Universal Render Pipeline | URP | Mobile, VR, performance | Growing (most new assets) |
| High Definition Render Pipeline | HDRP | Console/PC AAA | Specialized (fewer assets) |

### Check Compatibility
1. **Project Setting** → Graphics → Render Pipeline Asset
   - None = Built-in (default)
   - UniversalRenderPipeline = URP
   - HDRenderPipeline = HDRP

2. **Asset Support**
   - Asset Store page: filter by "Render Pipelines" or search description
   - Check for tags: "URP", "HDRP", "Built-in", "All"
   - Asset with "URP + Built-in" = works in both

3. **Common Incompatibility Causes**
   - Shader written for Built-in only → won't render in URP
   - Postprocessing V2 (old) → replace with PostProcess V3 or Volume Framework
   - Material using Standard Shader (Built-in) → rewrite for URP

### Safe Assumption
If asset doesn't mention render pipeline: Built-in only.
Test on target pipeline before shipping.

## Dependency Checking

### What Are Dependencies?

Assets can depend on:
- **Unity packages:** Input System, PostProcessing, Cinemachine, etc.
- **Third-party assets:** Another paid asset or framework
- **External libraries:** Wwise, FMOD, Havok Physics

### How to Find Dependencies

1. **Asset Store page** → scroll down "Requirements" or "Dependencies"
2. **Documentation** → check README or "Getting Started" guide
3. **manifest.json** (if UPM) → lists all package dependencies

### Example: Opsive Character Controller
```
Dependencies:
  - Unity.InputSystem (com.unity.inputsystem) v1.4+
  - Unity.Cinemachine v2.8+
  - Optional: Invector (third-party asset, $25)
```

Action:
1. Install new Input System (Package Manager)
2. Install Cinemachine (Package Manager)
3. If using Invector: buy + install separately

### Dependency Chain Risk

High-risk dependency chains:
- Asset A → depends on Asset B → depends on Asset C
- If Asset C abandoned, whole chain breaks
- Mitigation: Check all transitive deps' health

## Platform Support

Assets often declare platform support:

| Platform | Check For | Common Issues |
|----------|-----------|---------------|
| Windows Editor | Usually works | Rare issues |
| macOS Editor | Ask in reviews | M1/M2 compatibility? |
| Linux Editor | Check explicitly | Uncommon, usually works |
| Standalone PC | Usually works | Rare |
| iOS | Search for "iOS support" | Metal shader support? |
| Android | Search for "Android" | Performance on mid-range phones? |
| WebGL | Rare | Shader limitations |

Red flag: "Editor only" asset for game runtime (e.g., debug tool).

## Warning Signs That Asset Is Abandoned

1. **Last update >18 months ago**
2. **No mention of recent Unity versions** (2024, 2025, 6+)
3. **Negative reviews with "broken in 2022/2023"** and no developer response
4. **GitHub repo deleted or archived** (if public)
5. **Publisher website offline or portfolio removed**
6. **One-star reviews citing missing support, no replies**

### Abandoned Asset Survival Kit

If you must use abandoned asset:
- Version lock (don't update Unity)
- Vendor fork (download + maintain yourself)
- Migrate to replacement (planned roadmap)
- Wrap in compatibility layer (C# adapter)

## Pre-Download Gatekeeping Checklist

Before clicking "Download" or "Add to Project":

- [ ] **Version**: Asset supports my target Unity version
- [ ] **Render Pipeline**: Asset compatible with URP/HDRP/Built-in
- [ ] **Dependencies**: I can install all required packages/assets
- [ ] **Platform**: Asset supports my shipping platform (PC/mobile/web)
- [ ] **Publisher**: Reputation signal = 4.0+ rating or active maintenance
- [ ] **Maintenance**: Last update <12 months ago
- [ ] **Reviews**: No recent "broken in Unity 2025" complaints

If any box unchecked: ask publisher in review, wait for response, or pick alternative.
