# Steam And Desktop Packaging Notes

Research baseline: verified against current Steamworks, electron-builder, and Tauri documentation on 2026-08-08.

## Packaging Choice

Default to Electron for unknown Three.js projects:

- Electron bundles Chromium, reducing GPU/WebGL variability.
- It can load a static `dist/` without a local server when asset paths are relative.
- It is larger than Tauri, but size is usually acceptable for Steam compared with runtime reliability.

Use Tauri only when:

- the project already uses Tauri,
- the user prioritizes binary size over bundled runtime consistency,
- Rust/WebView2 prerequisites are acceptable,
- the game has been tested on the intended Windows versions.

On Windows, Tauri depends on Microsoft Edge WebView2. Windows 11 normally includes it; older systems may need installers or a fixed runtime. This can be fine, but is a distribution variable that Electron avoids.

## Steam Desktop Output

SteamPipe uploads depots, not just installer EXEs. Prefer shipping the unpacked app directory:

```text
steam-content/
  windows/
    GameName.exe
    resources/
    locales/
    *.dll
  macos/
    GameName.app/
  linux/
    GameName
    resources/
  steam_appid.txt       # dev/testing only; do not ship in public depots unless intentionally required
```

Use installer targets for direct distribution outside Steam. For Steam, first make the unpacked folder launch cleanly.

Keep Steam, static web, and mobile staging folders separate even when they share the same `dist/` input. Steam may need Electron runtime files and SteamPipe VDFs; web export needs a clean static upload folder; Cordova needs `www/`, `config.xml`, and generated native platform folders.

## Electron Build Defaults

Recommended baseline:

- `npm run build:desktop-dir` for host-OS Steam depot smoke testing: Windows on Windows, macOS on macOS, Linux on Linux.
- Use explicit scripts when needed: `build:win-dir`, `build:mac-dir`, or `build:linux-dir`.
- Keep `win`, `mac`, and `linux` sections in `electron-builder.yml` even if the current machine only builds one OS, so the staged project is ready for another machine or CI runner.
- `nsis`, `dmg`, or `AppImage` only when the user asks for non-Steam distribution or a store/direct artifact.
- Avoid casual cross-building. Build and verify macOS outputs on macOS, Linux outputs on Linux, and Windows outputs on Windows or a deliberate CI/container setup.
- Disable auto-update in Steam builds; let Steam handle updates.
- Keep `nodeIntegration: false`, `contextIsolation: true`, and `sandbox: true` unless a real native integration requires otherwise.
- Set `backgroundThrottling: false` for games.
- Load `web/index.html` from the packaged app with `file://`.
- Use `base: './'` in Vite builds to avoid absolute `/assets/...` paths failing under `file://`.
- If the project uses localization, run it before the production web build. Locale JSON bundled from `src/i18n` and flags copied from `public/localization/flags` must be present in the built web output before `copy:web`. If `$threejs-localize` is unavailable, perform the same checks manually.

## Steamworks SDK And Overlay

Steam Overlay works for games launched through Steam, but browser-wrapper/Electron overlay behavior can vary by OS, Electron version, GPU backend, and Steamworks integration method. Treat overlay as a test item, not a guaranteed property of "has exe".

If Steam API features are required:

- prefer a maintained Node/Electron-compatible Steamworks binding only after checking current compatibility,
- initialize Steamworks before creating the BrowserWindow when the library requires it,
- keep the native module and Steam SDK DLLs outside `asar` if required,
- test from the Steam client or a SteamPipe beta branch, not only by double-clicking the exe.

## SteamPipe Templates

Create VDF templates, but leave real app/depot IDs as user-provided values. Use separate depots/content roots for desktop platforms:

```text
steampipe/
  app_build_<appid>.vdf
  depot_build_<windows_depotid>.vdf
  depot_build_<macos_depotid>.vdf
  depot_build_<linux_depotid>.vdf
  steam-content/
    windows/
    macos/
    linux/
```

The app build script points to one or more depot build scripts. Each depot script maps local content to the depot root for that OS. Do not include source, `node_modules`, logs, `.env`, editor files, raw art sources, or unused dev assets.

## Signing And Release Hygiene

- Code signing is recommended for Windows trust prompts but not required to test a Steam build.
- Apple notarization/signing is required for public modern macOS releases; plan it before marking macOS support publicly.
- For Linux, test on the intended Steam Runtime/SteamOS path and a current Ubuntu LTS-style environment before release.
- Keep save data outside the install folder using Electron's `app.getPath('userData')` or the game's existing storage abstraction.
- Make fullscreen/windowed behavior explicit.
- Remove devtools, debug overlays, sourcemaps, test routes, and verbose console logs from release builds.
- Verify clean install behavior on a machine/account without the source checkout.

## Final Verification

Minimum checklist:

- Production web build succeeds.
- If localization exists, catalogs parse, shipping locales contain no `TODO:` values, and language selector assets are present in the packaged web output.
- Electron unpacked build launches from its release folder on each supported desktop OS.
- WebGL canvas is nonblank and interactive.
- If WebGPU is enabled, both the WebGPU path and the forced WebGL fallback render correctly.
- Relative asset paths work under `file://`.
- Audio starts after user gesture where required.
- Save/load and settings work.
- App exits cleanly from window close and Steam stop button.
- SteamPipe VDF paths point to the exact per-OS release folders, and the platform depots are added to the relevant Steam packages.
- No secrets, source maps, raw source, or huge unused assets are in the depot.
