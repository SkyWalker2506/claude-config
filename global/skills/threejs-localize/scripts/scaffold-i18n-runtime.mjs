#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] || process.cwd());

function option(name, fallback) {
  const index = args.indexOf(`--${name}`);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

function writeNew(file, content) {
  if (fs.existsSync(file)) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content.replace(/\n/g, '\r\n'));
  return true;
}

const sourceLocale = option('source', 'en');
const i18nDir = path.join(projectRoot, 'src', 'i18n');
const localesDir = path.join(i18nDir, 'locales');
const draftCatalog = path.join(projectRoot, 'buildable', 'localization', `source-catalog.${sourceLocale}.json`);
let catalog = {};

if (fs.existsSync(draftCatalog)) {
  try {
    catalog = JSON.parse(fs.readFileSync(draftCatalog, 'utf8').replace(/^\uFEFF/, ''));
  } catch {
    catalog = {};
  }
}

const created = [];
if (writeNew(path.join(localesDir, `${sourceLocale}.json`), JSON.stringify(catalog, null, 2))) created.push(`src/i18n/locales/${sourceLocale}.json`);
if (writeNew(path.join(i18nDir, 'locale-meta.json'), JSON.stringify({
  [sourceLocale]: {
    nativeName: sourceLocale,
    flag: null
  }
}, null, 2))) created.push('src/i18n/locale-meta.json');

if (writeNew(path.join(i18nDir, 'index.js'), `import sourceCatalog from './locales/${sourceLocale}.json';
import localeMeta from './locale-meta.json';

const localeModules = typeof import.meta.glob === 'function'
  ? import.meta.glob('./locales/*.json', { eager: true, import: 'default' })
  : {};

const catalogs = Object.fromEntries(
  Object.entries(localeModules).map(([file, catalog]) => {
    const locale = file.match(/\\/([^/]+)\\.json$/)?.[1];
    return [locale, catalog];
  }).filter(([locale]) => Boolean(locale))
);

if (!catalogs['${sourceLocale}']) {
  catalogs['${sourceLocale}'] = sourceCatalog;
};

let currentLocale = '${sourceLocale}';

const steamToBcp47 = {
  arabic: 'ar',
  bulgarian: 'bg',
  schinese: 'zh-CN',
  tchinese: 'zh-TW',
  czech: 'cs',
  danish: 'da',
  dutch: 'nl',
  english: 'en',
  finnish: 'fi',
  french: 'fr',
  german: 'de',
  greek: 'el',
  hungarian: 'hu',
  indonesian: 'id',
  italian: 'it',
  japanese: 'ja',
  koreana: 'ko',
  malay: 'ms',
  norwegian: 'no',
  polish: 'pl',
  portuguese: 'pt',
  brazilian: 'pt-BR',
  romanian: 'ro',
  russian: 'ru',
  spanish: 'es',
  latam: 'es-419',
  swedish: 'sv',
  thai: 'th',
  turkish: 'tr',
  ukrainian: 'uk',
  vietnamese: 'vi'
};

function normalizeLocale(locale) {
  if (!locale) return '';
  const mapped = steamToBcp47[String(locale).toLowerCase()] || String(locale).replace('_', '-');
  const parts = mapped.split('-');
  if (parts.length === 1) return parts[0].toLowerCase();
  return \`\${parts[0].toLowerCase()}-\${parts.slice(1).join('-').toUpperCase()}\`
    .replace('ZH-CN', 'zh-CN')
    .replace('ZH-TW', 'zh-TW')
    .replace('PT-BR', 'pt-BR')
    .replace('ES-419', 'es-419');
}

function bestSupportedLocale(locale) {
  const normalized = normalizeLocale(locale);
  if (!normalized) return '';
  if (catalogs[normalized]) return normalized;
  const base = normalized.split('-')[0];
  return catalogs[base] ? base : '';
}

export function detectDefaultLocale({ steamLanguage } = {}) {
  const saved = typeof localStorage !== 'undefined' ? localStorage.getItem('game.locale') : '';
  const browserLanguages = typeof navigator !== 'undefined' ? [...(navigator.languages || []), navigator.language] : [];
  const candidates = [saved, steamLanguage, ...browserLanguages];
  return candidates.map(bestSupportedLocale).find(Boolean) || '${sourceLocale}';
}

export function initLocale(options = {}) {
  setLocale(detectDefaultLocale(options));
  return currentLocale;
}

export function getLocale() {
  return currentLocale;
}

export function getAvailableLocales() {
  return Object.keys(catalogs);
}

export function getLocaleMeta(locale = currentLocale) {
  return localeMeta[locale] || { nativeName: locale, flag: null };
}

export function registerLocale(locale, catalog) {
  catalogs[locale] = catalog;
}

export function setLocale(locale) {
  currentLocale = bestSupportedLocale(locale) || '${sourceLocale}';
  if (typeof localStorage !== 'undefined') localStorage.setItem('game.locale', currentLocale);
  window.dispatchEvent(new CustomEvent('localechange', { detail: { locale: currentLocale } }));
}

export function t(key, vars = {}) {
  const value = catalogs[currentLocale]?.[key] ?? catalogs['${sourceLocale}']?.[key] ?? key;
  return String(value).replace(/\\{(\\w+)\\}/g, (_, name) => String(vars[name] ?? \`{\${name}}\`));
}
`)) created.push('src/i18n/index.js');

console.log(`I18n runtime scaffold checked: ${i18nDir}`);
if (created.length) {
  console.log('Created files:');
  for (const file of created) console.log(`- ${file}`);
} else {
  console.log('No new files created; existing i18n files were preserved.');
}
