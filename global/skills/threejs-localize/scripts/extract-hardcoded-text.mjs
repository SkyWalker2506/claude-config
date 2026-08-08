#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const projectRoot = path.resolve(process.argv[2] || process.cwd());
const outDir = path.join(projectRoot, 'buildable', 'localization');
const SKIP_DIRS = new Set(['.git', 'node_modules', 'buildable', 'dist', 'build', 'out', 'coverage', '.next', '.svelte-kit']);
const SOURCE_EXT = new Set(['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.html', '.vue', '.svelte']);
const TECH_PATTERNS = [
  /^https?:\/\//i,
  /^data:/i,
  /^#[a-f0-9]{3,8}$/i,
  /^[.#]?[a-z0-9_-]+$/i,
  /^[@./\\\w-]+\.(png|jpe?g|webp|svg|glb|gltf|mp3|wav|ogg|json|js|ts|css|html|wasm)$/i,
  /^[A-Z0-9_]+$/,
  /^[a-z]+:[\w.-]+$/i
];

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
    if (SOURCE_EXT.has(path.extname(entry.name).toLowerCase())) out.push(full);
  }
  return out;
}

function hasHumanText(value) {
  const text = value.trim();
  if (text.length < 2 || text.length > 280) return false;
  if (!/[A-Za-z\u00C0-\u024F\u0400-\u04FF\u0370-\u03FF\u0600-\u06FF\u3040-\u30FF\u3400-\u9FFF]/.test(text)) return false;
  if (TECH_PATTERNS.some((pattern) => pattern.test(text))) return false;
  if (/^(true|false|null|undefined|GET|POST|PUT|PATCH|DELETE)$/i.test(text)) return false;
  if (/^[\w.-]+\/[\w./-]+$/.test(text)) return false;
  return /[\s.,!?;:'"()[\]{}-]/.test(text) || text.length >= 8;
}

function makeKey(text, used) {
  const words = text
    .toLowerCase()
    .replace(/\{[^}]+\}/g, ' value ')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 6);
  let base = words.length ? words.join('.') : 'text';
  base = `ui.${base}`;
  let key = base;
  let i = 2;
  while (used.has(key)) key = `${base}.${i++}`;
  used.add(key);
  return key;
}

function lineNumber(source, index) {
  return source.slice(0, index).split(/\r?\n/).length;
}

function pushCandidate(candidates, seen, file, source, index, text, kind) {
  const normalized = text.replace(/\s+/g, ' ').trim();
  if (!hasHumanText(normalized)) return;
  const id = `${file}:${lineNumber(source, index)}:${normalized}`;
  if (seen.has(id)) return;
  seen.add(id);
  candidates.push({
    file: path.relative(projectRoot, file).replaceAll('\\', '/'),
    line: lineNumber(source, index),
    kind,
    text: normalized
  });
}

const candidates = [];
const seen = new Set();

for (const file of walk(projectRoot)) {
  let source = '';
  try {
    source = fs.readFileSync(file, 'utf8');
  } catch {
    continue;
  }

  const stringRegex = /(['"`])((?:\\.|(?!\1)[\s\S])*?)\1/g;
  let match;
  while ((match = stringRegex.exec(source))) {
    const quote = match[1];
    const text = match[2]
      .replace(/\\n/g, '\n')
      .replace(/\\"/g, '"')
      .replace(/\\'/g, "'");
    const before = source.slice(Math.max(0, match.index - 30), match.index);
    if (/\b(import|from|require)\s*\(?\s*$/.test(before)) continue;
    if (quote === '`' && /\$\{/.test(match[2])) {
      pushCandidate(candidates, seen, file, source, match.index, text.replace(/\$\{[^}]+\}/g, '{value}'), 'template-literal');
    } else {
      pushCandidate(candidates, seen, file, source, match.index, text, 'string-literal');
    }
  }

  const tagTextRegex = />\s*([^<>{}][^<>{}]{1,180}?)\s*</g;
  while ((match = tagTextRegex.exec(source))) {
    pushCandidate(candidates, seen, file, source, match.index, match[1], 'markup-text');
  }
}

const usedKeys = new Set();
const enriched = candidates.map((candidate) => ({
  ...candidate,
  suggestedKey: makeKey(candidate.text, usedKeys)
}));

const sourceCatalog = {};
for (const candidate of enriched) {
  sourceCatalog[candidate.suggestedKey] = candidate.text;
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'i18n-candidates.json'), JSON.stringify({ projectRoot, candidates: enriched }, null, 2));
fs.writeFileSync(path.join(outDir, 'source-catalog.en.json'), JSON.stringify(sourceCatalog, null, 2));

const md = [
  '# I18n Hardcoded Text Candidates',
  '',
  `Project: ${projectRoot}`,
  `Candidates: ${enriched.length}`,
  '',
  'Review these before patching. Some technical strings may still need to be ignored.',
  '',
  '| Key | File | Line | Kind | Text |',
  '| --- | --- | ---: | --- | --- |',
  ...enriched.map((c) => `| \`${c.suggestedKey}\` | \`${c.file}\` | ${c.line} | ${c.kind} | ${c.text.replace(/\|/g, '\\|')} |`)
].join('\n');

fs.writeFileSync(path.join(outDir, 'i18n-candidates.md'), `${md}\n`);
console.log(`Found ${enriched.length} candidate strings.`);
console.log(`Report: ${path.join(outDir, 'i18n-candidates.md')}`);
console.log(`Source catalog draft: ${path.join(outDir, 'source-catalog.en.json')}`);
