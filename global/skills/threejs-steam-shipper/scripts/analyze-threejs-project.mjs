#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const SKIP_DIRS = new Set(['.git', 'node_modules', 'buildable', '.next', '.svelte-kit', 'coverage', '.cache']);
const MODEL_EXT = new Set(['.glb', '.gltf', '.fbx', '.obj', '.dae', '.usdz']);
const TEXTURE_EXT = new Set(['.png', '.jpg', '.jpeg', '.webp', '.ktx2', '.basis', '.hdr', '.exr']);
const SOURCE_EXT = new Set(['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.html', '.css']);

const projectRoot = path.resolve(process.argv[2] || process.cwd());
const jsonOnly = process.argv.includes('--json');

function exists(file) {
  return fs.existsSync(file);
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

function walk(dir, out = []) {
  let entries = [];
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) walk(full, out);
      continue;
    }
    const stat = fs.statSync(full);
    out.push({ full, rel: path.relative(projectRoot, full).replaceAll('\\', '/'), size: stat.size, ext: path.extname(entry.name).toLowerCase() });
  }
  return out;
}

function detectPackageManager() {
  if (exists(path.join(projectRoot, 'pnpm-lock.yaml'))) return 'pnpm';
  if (exists(path.join(projectRoot, 'yarn.lock'))) return 'yarn';
  if (exists(path.join(projectRoot, 'bun.lockb')) || exists(path.join(projectRoot, 'bun.lock'))) return 'bun';
  if (exists(path.join(projectRoot, 'package-lock.json'))) return 'npm';
  return 'npm';
}

function detectFramework(pkg, files) {
  const deps = { ...pkg?.dependencies, ...pkg?.devDependencies };
  if (deps['@react-three/fiber'] || deps.react) return 'react-three-or-react';
  if (deps.vue || deps['@vitejs/plugin-vue']) return 'vue';
  if (deps.svelte || deps['@sveltejs/kit']) return 'svelte';
  if (deps.vite || files.some((f) => /(^|\/)vite\.config\./.test(f.rel))) return 'vite';
  if (files.some((f) => f.rel === 'index.html')) return 'static';
  return 'unknown';
}

function detectBuildOutput(pkg) {
  const candidates = ['dist', 'build', 'out', 'public'];
  for (const dir of candidates) {
    if (exists(path.join(projectRoot, dir, 'index.html'))) return dir;
  }
  const scripts = pkg?.scripts || {};
  const build = scripts.build || '';
  if (build.includes('vite')) return 'dist';
  if (build.includes('react-scripts')) return 'build';
  if (build.includes('next export')) return 'out';
  return 'dist';
}

function formatBytes(bytes) {
  const units = ['B', 'KB', 'MB', 'GB'];
  let value = bytes;
  let i = 0;
  while (value >= 1024 && i < units.length - 1) {
    value /= 1024;
    i++;
  }
  return `${value.toFixed(value >= 10 || i === 0 ? 0 : 1)} ${units[i]}`;
}

const pkg = readJson(path.join(projectRoot, 'package.json'));
const files = walk(projectRoot);
const deps = { ...pkg?.dependencies, ...pkg?.devDependencies };
const models = files.filter((f) => MODEL_EXT.has(f.ext)).sort((a, b) => b.size - a.size);
const textures = files.filter((f) => TEXTURE_EXT.has(f.ext)).sort((a, b) => b.size - a.size);
const sources = files.filter((f) => SOURCE_EXT.has(f.ext));
const largeFiles = files.filter((f) => f.size >= 10 * 1024 * 1024).sort((a, b) => b.size - a.size).slice(0, 30);
const sourceTextSample = sources.slice(0, 300).map((f) => {
  try {
    return fs.readFileSync(f.full, 'utf8').slice(0, 20000);
  } catch {
    return '';
  }
}).join('\n');

const usesWebGPU = /three\/webgpu|WebGPURenderer|navigator\.gpu|GPUAdapter|GPUDevice/.test(sourceTextSample);
const usesWebGLRenderer = /WebGLRenderer|webgl2?|getContext\(['"]webgl/.test(sourceTextSample);
const hasCordova = Boolean(deps.cordova || exists(path.join(projectRoot, 'config.xml')) || exists(path.join(projectRoot, 'www')));
const hasTouchHandling = /pointerdown|pointermove|touchstart|touchmove|TouchEvent|navigator\.maxTouchPoints/.test(sourceTextSample);
const hasFullscreenOrPointerLock = /requestFullscreen|pointerLock|requestPointerLock/.test(sourceTextSample);

const risks = [];
if (!pkg) risks.push('No package.json found; packaging may need a static/manual build path.');
if (!deps.three && !deps['@react-three/fiber']) risks.push('No direct three/@react-three/fiber dependency found; confirm this is a Three.js runtime project.');
if (/from\s+['"]\/|url\(['"]?\//.test(sourceTextSample)) risks.push('Absolute / asset paths detected; Electron file:// builds usually need relative paths or bundler base configuration.');
if (models.some((f) => f.ext === '.gltf')) risks.push('Loose .gltf assets detected; verify .bin/textures are copied into the packaged web folder.');
if (largeFiles.length) risks.push('Large runtime files found; inspect whether they are optimized assets or raw source content.');
if (deps.electron) risks.push('Project already includes Electron; prefer adapting existing wrapper rather than creating a second one.');
if (deps['@tauri-apps/api'] || exists(path.join(projectRoot, 'src-tauri'))) risks.push('Project already includes Tauri; consider continuing with Tauri if Steam/WebView2 requirements are acceptable.');
if (usesWebGPU && !usesWebGLRenderer) risks.push('WebGPU usage detected without an obvious WebGL renderer path; verify fallback before shipping to web/mobile/Steam.');
if (!hasTouchHandling) risks.push('No obvious touch/pointer input handling found; Cordova/mobile export may need touch controls.');
if (!hasFullscreenOrPointerLock) risks.push('No obvious fullscreen or pointer-lock handling found; verify browser, Steam wrapper, and mobile UX expectations.');

const report = {
  projectRoot,
  packageManager: detectPackageManager(),
  framework: detectFramework(pkg, files),
  packageName: pkg?.name || path.basename(projectRoot),
  scripts: pkg?.scripts || {},
  dependencies: Object.fromEntries(Object.entries(deps).filter(([name]) => ['three', '@react-three/fiber', '@react-three/drei', 'vite', 'electron', 'electron-builder', '@tauri-apps/api', 'cordova'].includes(name))),
  exportSignals: {
    usesWebGPU,
    usesWebGLRenderer,
    hasCordova,
    hasTouchHandling,
    hasFullscreenOrPointerLock
  },
  suggestedWebBuildDir: detectBuildOutput(pkg),
  counts: {
    files: files.length,
    sourceFiles: sources.length,
    models: models.length,
    textures: textures.length
  },
  largestFiles: largeFiles.map((f) => ({ path: f.rel, size: f.size, humanSize: formatBytes(f.size) })),
  largestModels: models.slice(0, 20).map((f) => ({ path: f.rel, size: f.size, humanSize: formatBytes(f.size) })),
  largestTextures: textures.slice(0, 20).map((f) => ({ path: f.rel, size: f.size, humanSize: formatBytes(f.size) })),
  risks
};

const reportsDir = path.join(projectRoot, 'buildable', 'reports');
fs.mkdirSync(reportsDir, { recursive: true });
fs.writeFileSync(path.join(reportsDir, 'threejs-steam-analysis.json'), JSON.stringify(report, null, 2));

const lines = [
  '# Three.js Ship Analysis',
  '',
  `Project: ${report.projectRoot}`,
  `Package manager: ${report.packageManager}`,
  `Framework: ${report.framework}`,
  `Suggested web build dir: ${report.suggestedWebBuildDir}`,
  '',
  '## Scripts',
  ...Object.entries(report.scripts).map(([name, value]) => `- ${name}: \`${value}\``),
  '',
  '## Key Dependencies',
  ...Object.entries(report.dependencies).map(([name, value]) => `- ${name}: ${value}`),
  '',
  '## Export Signals',
  `- WebGPU usage: ${report.exportSignals.usesWebGPU ? 'yes' : 'no'}`,
  `- WebGL renderer path: ${report.exportSignals.usesWebGLRenderer ? 'yes' : 'unknown'}`,
  `- Cordova project signals: ${report.exportSignals.hasCordova ? 'yes' : 'no'}`,
  `- Touch/pointer handling: ${report.exportSignals.hasTouchHandling ? 'yes' : 'unknown'}`,
  `- Fullscreen/pointer-lock handling: ${report.exportSignals.hasFullscreenOrPointerLock ? 'yes' : 'unknown'}`,
  '',
  '## Largest Runtime-Relevant Files',
  ...(report.largestFiles.length ? report.largestFiles.map((f) => `- ${f.humanSize}: ${f.path}`) : ['- None over 10 MB found.']),
  '',
  '## Largest Models',
  ...(report.largestModels.length ? report.largestModels.map((f) => `- ${f.humanSize}: ${f.path}`) : ['- None found.']),
  '',
  '## Largest Textures',
  ...(report.largestTextures.length ? report.largestTextures.map((f) => `- ${f.humanSize}: ${f.path}`) : ['- None found.']),
  '',
  '## Risks And Follow-Ups',
  ...(report.risks.length ? report.risks.map((risk) => `- ${risk}`) : ['- No obvious packaging risks detected.'])
];

fs.writeFileSync(path.join(reportsDir, 'threejs-steam-analysis.md'), `${lines.join('\n')}\n`);

if (jsonOnly) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`Analysis written to ${path.join(reportsDir, 'threejs-steam-analysis.md')}`);
  console.log(`Suggested build output: ${report.suggestedWebBuildDir}`);
  if (report.risks.length) {
    console.log('Risks:');
    for (const risk of report.risks) console.log(`- ${risk}`);
  }
}
