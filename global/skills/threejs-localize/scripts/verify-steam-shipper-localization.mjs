#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : process.cwd());

function option(name, fallback) {
  const index = args.indexOf(`--${name}`);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
  } catch {
    return null;
  }
}

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

const localeDir = path.resolve(option('dir', path.join(projectRoot, 'src', 'i18n', 'locales')));
const sourceLocale = option('source', 'en');
const steamWebDir = path.resolve(option('steam-web', path.join(projectRoot, 'buildable', 'steam-electron', 'web')));
const publicFlagsDir = path.join(projectRoot, 'public', 'localization', 'flags');
const reportDir = path.join(projectRoot, 'buildable', 'localization');
const source = readJson(path.join(localeDir, `${sourceLocale}.json`));
const strictSteam = args.includes('--strict-steam');
const issues = [];
const notes = [];

if (!source) {
  issues.push(`Missing or invalid source locale: ${path.join(localeDir, `${sourceLocale}.json`)}`);
} else {
  const sourceKeys = Object.keys(source).sort();
  for (const file of fs.existsSync(localeDir) ? fs.readdirSync(localeDir).filter((name) => name.endsWith('.json')) : []) {
    const locale = path.basename(file, '.json');
    const catalog = readJson(path.join(localeDir, file));
    if (!catalog) {
      issues.push(`Invalid locale JSON: ${file}`);
      continue;
    }
    const missing = sourceKeys.filter((key) => !Object.prototype.hasOwnProperty.call(catalog, key));
    const todos = Object.entries(catalog).filter(([, value]) => String(value).startsWith('TODO:')).map(([key]) => key);
    if (missing.length) issues.push(`${locale} missing keys: ${missing.join(', ')}`);
    if (todos.length) issues.push(`${locale} has TODO translations: ${todos.join(', ')}`);
  }
}

if (fs.existsSync(publicFlagsDir)) {
  const flags = fs.readdirSync(publicFlagsDir).filter((name) => name.endsWith('.svg'));
  notes.push(`Project flag assets: ${flags.length}`);
  if (fs.existsSync(steamWebDir)) {
    const packagedFlagsDir = path.join(steamWebDir, 'localization', 'flags');
    if (!fs.existsSync(packagedFlagsDir)) {
      issues.push(`Steam web folder exists but localization flags were not copied: ${packagedFlagsDir}`);
    }
  }
}

if (fs.existsSync(steamWebDir)) {
  if (!fs.existsSync(path.join(steamWebDir, 'index.html'))) {
    issues.push(`Steam web folder exists but has no index.html: ${steamWebDir}`);
  }
  const leakedBuildableFiles = walk(steamWebDir).filter((file) => /translation-batch|i18n-candidates|locale-key-report|THIRD_PARTY_NOTICES\.localization/i.test(path.basename(file)));
  if (leakedBuildableFiles.length) {
    issues.push(`Build-only localization files leaked into Steam web output: ${leakedBuildableFiles.map((file) => path.relative(steamWebDir, file)).join(', ')}`);
  }
} else {
  const message = 'Steam shipper web folder not found; standalone localization validation can continue.';
  if (strictSteam) issues.push(`${message} Expected after copy:web: ${steamWebDir}`);
  else notes.push(message);
}

fs.mkdirSync(reportDir, { recursive: true });
const md = [
  '# Steam Shipper Localization Compatibility',
  '',
  `Project: ${projectRoot}`,
  `Locale directory: ${localeDir}`,
  `Steam web directory: ${steamWebDir}`,
  `Strict Steam mode: ${strictSteam ? 'yes' : 'no'}`,
  '',
  '## Issues',
  ...(issues.length ? issues.map((issue) => `- ${issue}`) : ['- None found.']),
  '',
  '## Notes',
  ...(notes.length ? notes.map((note) => `- ${note}`) : ['- None.'])
].join('\n');

fs.writeFileSync(path.join(reportDir, 'steam-shipper-localization-report.md'), `${md}\n`);

if (issues.length) {
  console.error(`Localization compatibility issues found: ${issues.length}`);
  console.error(`Report: ${path.join(reportDir, 'steam-shipper-localization-report.md')}`);
  process.exitCode = 1;
} else {
  console.log(strictSteam
    ? 'Localization is compatible with the current Steam shipper staging state.'
    : 'Localization validation passed; Steam staging checks were optional.');
  console.log(`Report: ${path.join(reportDir, 'steam-shipper-localization-report.md')}`);
}
