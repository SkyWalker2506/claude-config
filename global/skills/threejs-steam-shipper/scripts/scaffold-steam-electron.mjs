#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] || process.cwd());

function readOption(name, fallback) {
  const index = args.indexOf(`--${name}`);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function safeName(value) {
  return String(value || 'ThreeJS Game')
    .replace(/^@[^/]+\//, '')
    .replace(/[-_]+/g, ' ')
    .replace(/\b\w/g, (ch) => ch.toUpperCase())
    .trim() || 'ThreeJS Game';
}

function packageName(value) {
  return String(value || 'threejs-steam-game')
    .toLowerCase()
    .replace(/^@[^/]+\//, '')
    .replace(/[^a-z0-9-]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'threejs-steam-game';
}

function writeNew(file, content) {
  if (fs.existsSync(file)) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content.replace(/\n/g, '\r\n'));
  return true;
}

const pkg = readJson(path.join(projectRoot, 'package.json')) || {};
const appId = readOption('appid', '480');
const winDepotId = readOption('win-depotid', readOption('depotid', `${appId}1`));
const macDepotId = readOption('mac-depotid', `${appId}2`);
const linuxDepotId = readOption('linux-depotid', `${appId}3`);
const productName = readOption('name', safeName(pkg.productName || pkg.name || path.basename(projectRoot)));
const outDir = path.resolve(readOption('out', path.join(projectRoot, 'buildable', 'steam-electron')));
const webBuildDir = readOption('web', 'dist');
const sourceRel = path.relative(outDir, projectRoot).replaceAll('\\', '/') || '.';
const webBuildRel = path.posix.join(sourceRel, webBuildDir.replaceAll('\\', '/'));
const normalizedPackageName = packageName(pkg.name || productName);
const bundleId = `com.${normalizedPackageName.replace(/-/g, '.')}.game`;

fs.mkdirSync(outDir, { recursive: true });

const created = [];
function add(file, content) {
  if (writeNew(path.join(outDir, file), content)) created.push(file);
}

add('package.json', JSON.stringify({
  name: `${normalizedPackageName}-steam`,
  version: pkg.version || '0.1.0',
  private: true,
  main: 'electron/main.cjs',
  scripts: {
    'copy:web': `node scripts/copy-web.mjs --from "${webBuildRel}" --to web`,
    'build:desktop-dir': 'npm run copy:web && node scripts/build-desktop.mjs --dir',
    'build:desktop': 'npm run copy:web && node scripts/build-desktop.mjs',
    'build:win-dir': 'npm run copy:web && electron-builder --win --x64 --dir',
    'build:win-installer': 'npm run copy:web && electron-builder --win --x64',
    'build:mac-dir': 'npm run copy:web && electron-builder --mac --dir',
    'build:mac': 'npm run copy:web && electron-builder --mac',
    'build:linux-dir': 'npm run copy:web && electron-builder --linux --dir',
    'build:linux': 'npm run copy:web && electron-builder --linux'
  },
  devDependencies: {
    electron: '^43.3.0',
    'electron-builder': '^26.15.3'
  }
}, null, 2));

add('electron-builder.yml', `appId: ${bundleId}
productName: ${productName}
asar: true
directories:
  output: release
files:
  - package.json
  - electron/**
  - web/**
win:
  target:
    - target: dir
      arch:
        - x64
    - target: nsis
      arch:
        - x64
nsis:
  oneClick: false
  perMachine: false
  allowToChangeInstallationDirectory: true
mac:
  category: public.app-category.games
  target:
    - target: dir
    - target: dmg
linux:
  category: Game
  target:
    - target: dir
    - target: AppImage
`);

add('electron/main.cjs', `const { app, BrowserWindow, Menu } = require('electron');
const path = require('node:path');

const isDev = !app.isPackaged;

app.setAppUserModelId('${bundleId}');
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');

function createWindow() {
  Menu.setApplicationMenu(null);

  const win = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 960,
    minHeight: 540,
    backgroundColor: '#050505',
    show: false,
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      backgroundThrottling: false
    }
  });

  win.once('ready-to-show', () => {
    win.show();
    if (isDev) win.webContents.openDevTools({ mode: 'detach' });
  });

  win.loadFile(path.join(__dirname, '..', 'web', 'index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
`);

add('electron/preload.cjs', `const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('steamShell', {
  platform: process.platform
});
`);

add('scripts/copy-web.mjs', `#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const from = path.resolve(args[args.indexOf('--from') + 1] || 'dist');
const to = path.resolve(args[args.indexOf('--to') + 1] || 'web');

function copyDir(src, dest) {
  if (!fs.existsSync(src)) {
    throw new Error(\`Web build folder not found: \${src}\`);
  }
  fs.rmSync(dest, { recursive: true, force: true });
  fs.mkdirSync(dest, { recursive: true });
  fs.cpSync(src, dest, { recursive: true });
}

copyDir(from, to);
console.log(\`Copied web build from \${from} to \${to}\`);
`);

add('scripts/build-desktop.mjs', `#!/usr/bin/env node
import { spawnSync } from 'node:child_process';

const args = process.argv.slice(2);
const platformMap = {
  win32: 'win',
  darwin: 'mac',
  linux: 'linux'
};
const defaultArch = process.arch === 'arm64' ? 'arm64' : 'x64';

function option(name, fallback) {
  const index = args.indexOf(\`--\${name}\`);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

const platform = option('platform', platformMap[process.platform] || 'linux');
const arch = option('arch', defaultArch);
const builderArgs = [\`--\${platform}\`, \`--\${arch}\`];
if (args.includes('--dir')) builderArgs.push('--dir');

if (!['win', 'mac', 'linux'].includes(platform)) {
  throw new Error(\`Unsupported desktop platform: \${platform}. Use win, mac, or linux.\`);
}

if (platform !== platformMap[process.platform]) {
  console.warn(\`[build-desktop] Cross-building \${platform} from \${process.platform}. Verify electron-builder host limitations, signing, and native dependencies.\`);
}

const command = process.platform === 'win32' ? 'npx.cmd' : 'npx';
const result = spawnSync(command, ['electron-builder', ...builderArgs], { stdio: 'inherit', shell: false });
process.exit(result.status ?? 1);
`);

add('steampipe/app_build_' + appId + '.vdf', `"appbuild"
{
  "appid" "${appId}"
  "desc" "${productName} desktop build"
  "buildoutput" "..\\\\build-output"
  "contentroot" "..\\\\steam-content"
  "setlive" ""
  "preview" "0"
  "local" ""
  "depots"
  {
    "${winDepotId}" "depot_build_${winDepotId}.vdf"
    "${macDepotId}" "depot_build_${macDepotId}.vdf"
    "${linuxDepotId}" "depot_build_${linuxDepotId}.vdf"
  }
}
`);

add('steampipe/depot_build_' + winDepotId + '.vdf', `"DepotBuildConfig"
{
  "DepotID" "${winDepotId}"
  "contentroot" "..\\\\steam-content\\\\windows"
  "FileMapping"
  {
    "LocalPath" "*"
    "DepotPath" "."
    "recursive" "1"
  }
}
`);

add('steampipe/depot_build_' + macDepotId + '.vdf', `"DepotBuildConfig"
{
  "DepotID" "${macDepotId}"
  "contentroot" "..\\\\steam-content\\\\macos"
  "FileMapping"
  {
    "LocalPath" "*"
    "DepotPath" "."
    "recursive" "1"
  }
}
`);

add('steampipe/depot_build_' + linuxDepotId + '.vdf', `"DepotBuildConfig"
{
  "DepotID" "${linuxDepotId}"
  "contentroot" "..\\\\steam-content\\\\linux"
  "FileMapping"
  {
    "LocalPath" "*"
    "DepotPath" "."
    "recursive" "1"
  }
}
`);

add('steampipe/steam-content/windows/.gitkeep', '');
add('steampipe/steam-content/macos/.gitkeep', '');
add('steampipe/steam-content/linux/.gitkeep', '');

add('ship-checklist.md', `# Steam Ship Checklist

- Build the source project in production mode.
- Run \`npm install\` inside this folder.
- Run \`npm run build:desktop-dir\` on the target OS. It builds Windows on Windows, macOS on macOS, and Linux on Linux.
- Or run an explicit target: \`npm run build:win-dir\`, \`npm run build:mac-dir\`, or \`npm run build:linux-dir\`.
- Copy the unpacked output into the matching depot folder:
  - Windows: \`release/win-unpacked/**\` -> \`steampipe/steam-content/windows/\`
  - macOS: \`release/mac*/${productName}.app\` or matching app bundle -> \`steampipe/steam-content/macos/\`
  - Linux: \`release/linux-unpacked/**\` -> \`steampipe/steam-content/linux/\`
- Launch the unpacked app on the same OS and verify rendering, input, audio, save data, and shutdown.
- Replace placeholder app/depot IDs before uploading with SteamPipe. Add each platform depot to the right Steam package and launch option.
- For macOS release, plan signing/notarization before public Steam release.
- Remove \`steam_appid.txt\` from public depot unless intentionally required.
- Exclude source files, sourcemaps, raw art, secrets, logs, and unused assets.
`);

console.log(`Steam Electron scaffold ready: ${outDir}`);
if (created.length) {
  console.log('Created files:');
  for (const file of created) console.log(`- ${file}`);
} else {
  console.log('No new files created; existing scaffold was preserved.');
}
