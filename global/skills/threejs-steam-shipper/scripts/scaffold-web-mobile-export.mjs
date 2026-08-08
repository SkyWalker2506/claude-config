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
  return String(value || 'threejs-game')
    .toLowerCase()
    .replace(/^@[^/]+\//, '')
    .replace(/[^a-z0-9-]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'threejs-game';
}

function writeNew(file, content) {
  if (fs.existsSync(file)) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content.replace(/\n/g, '\r\n'));
  return true;
}

const pkg = readJson(path.join(projectRoot, 'package.json')) || {};
const productName = readOption('name', safeName(pkg.productName || pkg.name || path.basename(projectRoot)));
const webBuildDir = readOption('web', 'dist');
const webOutDir = path.resolve(readOption('web-out', path.join(projectRoot, 'buildable', 'web')));
const mobileOutDir = path.resolve(readOption('mobile-out', path.join(projectRoot, 'buildable', 'mobile-cordova')));
const sourceRelToWeb = path.relative(webOutDir, projectRoot).replaceAll('\\', '/') || '.';
const sourceRelToMobile = path.relative(mobileOutDir, projectRoot).replaceAll('\\', '/') || '.';
const webBuildRel = path.posix.join(sourceRelToWeb, webBuildDir.replaceAll('\\', '/'));
const mobileBuildRel = path.posix.join(sourceRelToMobile, webBuildDir.replaceAll('\\', '/'));
const normalizedPackageName = packageName(pkg.name || productName);
const appId = readOption('id', `com.${normalizedPackageName.replace(/-/g, '.')}.game`);

const created = [];
function add(root, file, content) {
  const target = path.join(root, file);
  if (writeNew(target, content)) created.push(path.relative(projectRoot, target).replaceAll('\\', '/'));
}

fs.mkdirSync(webOutDir, { recursive: true });
fs.mkdirSync(mobileOutDir, { recursive: true });

add(webOutDir, 'scripts/copy-web.mjs', `#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const from = path.resolve(args[args.indexOf('--from') + 1] || '${webBuildRel}');
const to = path.resolve(args[args.indexOf('--to') + 1] || 'dist');

if (!fs.existsSync(from)) throw new Error(\`Web build folder not found: \${from}\`);
fs.rmSync(to, { recursive: true, force: true });
fs.mkdirSync(to, { recursive: true });
fs.cpSync(from, to, { recursive: true });
console.log(\`Copied static web export from \${from} to \${to}\`);
`);

add(webOutDir, 'release-checklist.md', `# Web Export Checklist

- Build the source project in production mode.
- Run \`node scripts/copy-web.mjs\` inside this folder.
- Serve \`dist/\` over HTTP/HTTPS for QA; do not rely on opening files directly.
- Verify relative asset paths, workers/WASM decoders, fonts, locale JSON, and audio files.
- Verify fullscreen, pointer lock, keyboard/touch input, save data, and audio unlock.
- If WebGPU is enabled, test both supported WebGPU and forced WebGL fallback paths.
- Exclude source files, sourcemaps, raw art, secrets, logs, and unused dev assets from public hosting.
`);

add(mobileOutDir, 'package.json', JSON.stringify({
  name: `${normalizedPackageName}-cordova`,
  version: pkg.version || '0.1.0',
  private: true,
  scripts: {
    'copy:web': `node scripts/copy-web.mjs --from "${mobileBuildRel}" --to www`,
    'platform:add:android': 'cordova platform add android',
    'platform:add:ios': 'cordova platform add ios',
    'prepare:android': 'npm run copy:web && cordova prepare android',
    'prepare:ios': 'npm run copy:web && cordova prepare ios',
    'build:android-debug': 'npm run copy:web && cordova build android --debug',
    'build:android-release': 'npm run copy:web && cordova build android --release',
    'build:ios-debug': 'npm run copy:web && cordova build ios --debug',
    'build:ios-release': 'npm run copy:web && cordova build ios --release'
  },
  devDependencies: {
    cordova: '^14.0.1'
  },
  cordova: {
    platforms: [],
    plugins: {}
  }
}, null, 2));

add(mobileOutDir, 'config.xml', `<?xml version='1.0' encoding='utf-8'?>
<widget id="${appId}" version="${pkg.version || '0.1.0'}" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
  <name>${productName}</name>
  <description>Three.js mobile export</description>
  <author />
  <content src="index.html" />
  <access origin="*" />
  <allow-navigation href="*" />
  <preference name="Fullscreen" value="true" />
  <preference name="DisallowOverscroll" value="true" />
</widget>
`);

add(mobileOutDir, 'scripts/copy-web.mjs', `#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const from = path.resolve(args[args.indexOf('--from') + 1] || '${mobileBuildRel}');
const to = path.resolve(args[args.indexOf('--to') + 1] || 'www');

if (!fs.existsSync(from)) throw new Error(\`Web build folder not found: \${from}\`);
fs.rmSync(to, { recursive: true, force: true });
fs.mkdirSync(to, { recursive: true });
fs.cpSync(from, to, { recursive: true });
console.log(\`Copied Cordova web assets from \${from} to \${to}\`);
`);

add(mobileOutDir, 'mobile-checklist.md', `# Cordova Mobile Checklist

- Install Cordova CLI and platform SDKs before building.
- Android: install Android Studio, Android SDK, JDK/Gradle requirements, then run \`npx cordova platform add android\`.
- iOS: build on macOS with Xcode, command line tools, CocoaPods, and provisioning, then run \`npx cordova platform add ios\`.
- Run \`npm run copy:web\` after each production web build.
- Add only required plugins such as screen orientation/status bar; keep native surface minimal.
- Verify touch controls, safe areas/notches, orientation, resize, pause/resume, audio unlock, saves, and offline first launch.
- Test memory pressure and WebGL context loss on real devices before release signing.
- Produce Android/iOS signed release artifacts only after debug builds run on target devices.
`);

console.log(`Web export scaffold ready: ${webOutDir}`);
console.log(`Cordova mobile scaffold ready: ${mobileOutDir}`);
if (created.length) {
  console.log('Created files:');
  for (const file of created) console.log(`- ${file}`);
} else {
  console.log('No new files created; existing export scaffolds were preserved.');
}
