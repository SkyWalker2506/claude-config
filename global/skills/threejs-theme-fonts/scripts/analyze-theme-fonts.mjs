#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const projectRoot = path.resolve(process.argv[2] || process.cwd());
const outDir = path.join(projectRoot, 'buildable', 'typography');
const SKIP_DIRS = new Set(['.git', 'node_modules', 'dist', 'build', 'buildable', '.next', '.svelte-kit']);
const STYLE_EXT = new Set(['.css', '.scss', '.sass', '.less']);
const SOURCE_EXT = new Set(['.js', '.jsx', '.ts', '.tsx', '.html', '.css']);
const IMAGE_EXT = new Set(['.png', '.jpg', '.jpeg', '.webp']);
const STEAM_FULL_LOCALES = ['ar', 'bg', 'zh-CN', 'zh-TW', 'cs', 'da', 'nl', 'en', 'fi', 'fr', 'de', 'el', 'hu', 'id', 'it', 'ja', 'ko', 'ms', 'no', 'pl', 'pt', 'pt-BR', 'ro', 'ru', 'es', 'es-419', 'sv', 'th', 'tr', 'uk', 'vi'];

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) walk(full, out);
    } else {
      out.push(full);
    }
  }
  return out;
}

function read(file) {
  try {
    return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  } catch {
    return '';
  }
}

function readJson(file) {
  try {
    return JSON.parse(read(file));
  } catch {
    return null;
  }
}

function rel(file) {
  return path.relative(projectRoot, file).replaceAll('\\', '/');
}

function detectTheme(text) {
  const lower = text.toLowerCase();
  const scores = {
    'sci-fi': ['space', 'neon', 'cyber', 'laser', 'ship', 'robot', 'terminal', 'hologram', 'future'],
    fantasy: ['magic', 'spell', 'dungeon', 'dragon', 'sword', 'rune', 'kingdom', 'quest'],
    cozy: ['cozy', 'garden', 'farm', 'soft', 'cute', 'calm', 'warm', 'village'],
    horror: ['horror', 'dark', 'ghost', 'blood', 'fear', 'nightmare', 'haunt'],
    retro: ['retro', 'pixel', 'arcade', '8bit', '8-bit', 'crt', 'scanline'],
    minimal: ['minimal', 'clean', 'abstract', 'puzzle', 'grid']
  };
  let best = 'neutral';
  let bestScore = 0;
  for (const [theme, words] of Object.entries(scores)) {
    const score = words.reduce((sum, word) => sum + (lower.includes(word) ? 1 : 0), 0);
    if (score > bestScore) {
      best = theme;
      bestScore = score;
    }
  }
  return { theme: best, score: bestScore };
}

function scriptBucketsForLocales(locales) {
  const buckets = new Set(['latin']);
  for (const locale of locales) {
    if (locale === 'ar') buckets.add('arabic');
    if (locale === 'zh-CN') buckets.add('simplified-chinese');
    if (locale === 'zh-TW') buckets.add('traditional-chinese');
    if (locale === 'ja') buckets.add('japanese');
    if (locale === 'ko') buckets.add('korean');
    if (locale === 'th') buckets.add('thai');
    if (['bg', 'ru', 'uk'].includes(locale)) buckets.add('cyrillic');
    if (locale === 'el') buckets.add('greek');
    if (['tr', 'vi', 'cs', 'pl', 'ro', 'hu'].includes(locale)) buckets.add('latin-diacritics');
  }
  return [...buckets].sort();
}

const files = walk(projectRoot);
const styleFiles = files.filter((file) => STYLE_EXT.has(path.extname(file).toLowerCase()));
const sourceFiles = files.filter((file) => SOURCE_EXT.has(path.extname(file).toLowerCase()));
const images = files.filter((file) => IMAGE_EXT.has(path.extname(file).toLowerCase()) && /screenshot|screen|capture|preview|hero|thumb/i.test(file));
const textSample = sourceFiles.slice(0, 150).map(read).join('\n').slice(0, 250000);
const theme = detectTheme(`${path.basename(projectRoot)}\n${read(path.join(projectRoot, 'README.md'))}\n${textSample}`);
const fontFamilies = [];

for (const file of styleFiles) {
  const content = read(file);
  for (const match of content.matchAll(/font-family\s*:\s*([^;]+)/gi)) {
    fontFamilies.push({ file: rel(file), value: match[1].trim() });
  }
}

const localeDir = path.join(projectRoot, 'src', 'i18n', 'locales');
const locales = fs.existsSync(localeDir)
  ? fs.readdirSync(localeDir).filter((name) => name.endsWith('.json')).map((name) => path.basename(name, '.json'))
  : STEAM_FULL_LOCALES;
const buckets = scriptBucketsForLocales(locales);

const report = {
  projectRoot,
  detectedTheme: theme.theme,
  themeConfidence: theme.score,
  locales,
  scriptBuckets: buckets,
  currentFontFamilies: fontFamilies,
  screenshotCandidates: images.map(rel),
  recommendation: {
    ui: 'Research current free/open-source theme-fit UI fonts first; keep Noto families as fallback coverage only.',
    fallback: ['Noto Sans', 'Noto Sans Arabic', 'Noto Sans SC', 'Noto Sans TC', 'Noto Sans JP', 'Noto Sans KR', 'Noto Sans Thai'],
    display: 'Pick one optional theme display font only after checking license and glyph coverage.',
    hud: 'Use the UI stack with stronger weight, shadow/backplate, and stable responsive sizing.',
    researchGate: 'Before scaffolding final choices, browse current Google Fonts/Fontsource/upstream pages and compare at least 3 theme-fit candidates when available.'
  }
};

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'theme-font-analysis.json'), JSON.stringify(report, null, 2));

const md = [
  '# Theme Font Analysis',
  '',
  `Project: ${projectRoot}`,
  `Detected theme: ${theme.theme} (score ${theme.score})`,
  '',
  '## Locale Script Buckets',
  ...buckets.map((bucket) => `- ${bucket}`),
  '',
  '## Current Font Families',
  ...(fontFamilies.length ? fontFamilies.map((item) => `- ${item.file}: \`${item.value}\``) : ['- No explicit CSS font-family declarations found.']),
  '',
  '## Screenshot Candidates',
  ...(images.length ? images.map((file) => `- ${file}`) : ['- None found. Use Playwright screenshots if theme is unclear.']),
  '',
  '## Font Research Guidance',
  `- UI: ${report.recommendation.ui}`,
  `- Gate: ${report.recommendation.researchGate}`,
  '- Search current Google Fonts/Fontsource/upstream font pages for theme-fit candidates before falling back.',
  '- Record candidate source URLs, licenses, scripts/subsets, weights, and rejection reasons.',
  '',
  '## Candidate Matrix',
  '| Candidate | Source URL | License | Theme fit | Covered scripts | Missing scripts | Decision |',
  '| --- | --- | --- | --- | --- | --- | --- |',
  '| Fill after internet research |  |  |  |  |  |  |',
  '',
  '## Noto Fallback Set',
  ...report.recommendation.fallback.map((font) => `- ${font}`),
  '',
  '## Notes',
  '- Use themed display fonts only for short accent text.',
  '- Keep localized HUD, menus, dialogue, buttons, and center popups on the multilingual UI stack.',
  '- Self-host fonts under `public/fonts/` before Steam/Electron shipping.'
].join('\n');

fs.writeFileSync(path.join(outDir, 'theme-font-analysis.md'), `${md}\n`);
console.log(`Theme font analysis written: ${path.join(outDir, 'theme-font-analysis.md')}`);
