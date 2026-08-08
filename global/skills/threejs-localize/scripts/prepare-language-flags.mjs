#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] || process.cwd());

function option(name, fallback) {
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

const metaPath = path.resolve(option('meta', path.join(projectRoot, 'src', 'i18n', 'locale-meta.json')));
const flagsDir = path.resolve(option('out', path.join(projectRoot, 'public', 'localization', 'flags')));
const style = option('style', '4x3');
const source = option('source', 'flag-icons');
const meta = readJson(metaPath);

if (!meta) {
  throw new Error(`Locale metadata not found or invalid JSON: ${metaPath}`);
}

if (source !== 'flag-icons') {
  throw new Error('Only --source flag-icons is built in. Verify other sources manually before adding assets.');
}

fs.mkdirSync(flagsDir, { recursive: true });

const flags = [...new Set(Object.values(meta).map((entry) => entry?.flag).filter(Boolean))].sort();
const downloaded = [];
const skipped = [];

for (const flag of flags) {
  const file = path.join(flagsDir, `${flag}.svg`);
  if (fs.existsSync(file)) {
    skipped.push(flag);
    continue;
  }
  const url = `https://cdn.jsdelivr.net/npm/flag-icons/flags/${style}/${flag}.svg`;
  const response = await fetch(url);
  if (!response.ok) {
    skipped.push(flag);
    continue;
  }
  fs.writeFileSync(file, await response.text());
  downloaded.push(flag);
}

const noticeDir = path.join(projectRoot, 'buildable', 'localization');
fs.mkdirSync(noticeDir, { recursive: true });
fs.writeFileSync(path.join(noticeDir, 'THIRD_PARTY_NOTICES.localization.md'), `# Localization Third-Party Notices

Flag SVGs copied from flag-icons by Panayiotis Lipiridis and contributors.
Source: https://github.com/lipis/flag-icons
License: MIT

Flags are used only as optional visual hints in the language selector. Language names remain visible in the UI.
`);

console.log(`Flag output: ${flagsDir}`);
console.log(`Downloaded: ${downloaded.length ? downloaded.join(', ') : 'none'}`);
if (skipped.length) console.log(`Skipped/existing/unavailable: ${skipped.join(', ')}`);
