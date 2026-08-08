#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : process.cwd());
const STEAM_FULL_LOCALES = [
  'ar', 'bg', 'zh-CN', 'zh-TW', 'cs', 'da', 'nl', 'en', 'fi', 'fr',
  'de', 'el', 'hu', 'id', 'it', 'ja', 'ko', 'ms', 'no', 'pl',
  'pt', 'pt-BR', 'ro', 'ru', 'es', 'es-419', 'sv', 'th', 'tr', 'uk', 'vi'
];
const LOCALE_META = {
  ar: { nativeName: '\u0627\u0644\u0639\u0631\u0628\u064a\u0629', flag: null },
  bg: { nativeName: '\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438 \u0435\u0437\u0438\u043a', flag: 'bg' },
  'zh-CN': { nativeName: '\u7b80\u4f53\u4e2d\u6587', flag: 'cn' },
  'zh-TW': { nativeName: '\u7e41\u9ad4\u4e2d\u6587', flag: 'tw' },
  cs: { nativeName: '\u010de\u0161tina', flag: 'cz' },
  da: { nativeName: 'Dansk', flag: 'dk' },
  nl: { nativeName: 'Nederlands', flag: 'nl' },
  en: { nativeName: 'English', flag: 'gb' },
  fi: { nativeName: 'Suomi', flag: 'fi' },
  fr: { nativeName: 'Fran\u00e7ais', flag: 'fr' },
  de: { nativeName: 'Deutsch', flag: 'de' },
  el: { nativeName: '\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac', flag: 'gr' },
  hu: { nativeName: 'Magyar', flag: 'hu' },
  id: { nativeName: 'Bahasa Indonesia', flag: 'id' },
  it: { nativeName: 'Italiano', flag: 'it' },
  ja: { nativeName: '\u65e5\u672c\u8a9e', flag: 'jp' },
  ko: { nativeName: '\ud55c\uad6d\uc5b4', flag: 'kr' },
  ms: { nativeName: 'Bahasa Melayu', flag: 'my' },
  no: { nativeName: 'Norsk', flag: 'no' },
  pl: { nativeName: 'Polski', flag: 'pl' },
  pt: { nativeName: 'Portugu\u00eas', flag: 'pt' },
  'pt-BR': { nativeName: 'Portugu\u00eas-Brasil', flag: 'br' },
  ro: { nativeName: 'Rom\u00e2n\u0103', flag: 'ro' },
  ru: { nativeName: '\u0420\u0443\u0441\u0441\u043a\u0438\u0439', flag: 'ru' },
  es: { nativeName: 'Espa\u00f1ol-Espa\u00f1a', flag: 'es' },
  'es-419': { nativeName: 'Espa\u00f1ol-Latinoam\u00e9rica', flag: 'mx' },
  sv: { nativeName: 'Svenska', flag: 'se' },
  th: { nativeName: '\u0e44\u0e17\u0e22', flag: 'th' },
  tr: { nativeName: 'T\u00fcrk\u00e7e', flag: 'tr' },
  uk: { nativeName: '\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430', flag: 'ua' },
  vi: { nativeName: 'Ti\u1ebfng Vi\u1ec7t', flag: 'vn' }
};

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

function sortObject(obj) {
  return Object.fromEntries(Object.entries(obj).sort(([a], [b]) => a.localeCompare(b)));
}

const sourceLocale = option('source', 'en');
const localeList = args.includes('--steam-full')
  ? STEAM_FULL_LOCALES
  : option('locales', '').split(',').map((x) => x.trim()).filter(Boolean);
const localeDir = path.resolve(option('dir', path.join(projectRoot, 'src', 'i18n', 'locales')));
const outDir = path.join(projectRoot, 'buildable', 'localization');
const sourcePath = path.join(localeDir, `${sourceLocale}.json`);
const source = readJson(sourcePath);

if (!source) {
  throw new Error(`Source locale file not found or invalid JSON: ${sourcePath}`);
}
if (!localeList.length) {
  throw new Error('Pass target locales with --locales tr,es,fr or use --steam-full');
}

fs.mkdirSync(localeDir, { recursive: true });
fs.mkdirSync(outDir, { recursive: true });

const sourceKeys = Object.keys(source).sort();
const report = [];
const metaPath = path.join(path.dirname(localeDir), 'locale-meta.json');
const existingMeta = readJson(metaPath) || {};
const nextMeta = { ...existingMeta };

if (!nextMeta[sourceLocale]) {
  nextMeta[sourceLocale] = LOCALE_META[sourceLocale] || { nativeName: sourceLocale, flag: null };
}

for (const locale of localeList) {
  if (!nextMeta[locale]) nextMeta[locale] = LOCALE_META[locale] || { nativeName: locale, flag: null };
  if (locale === sourceLocale) continue;

  const file = path.join(localeDir, `${locale}.json`);
  const existing = readJson(file) || {};
  const next = { ...existing };
  const missing = [];
  const extra = Object.keys(existing).filter((key) => !Object.prototype.hasOwnProperty.call(source, key)).sort();

  for (const key of sourceKeys) {
    if (!Object.prototype.hasOwnProperty.call(next, key)) {
      next[key] = `TODO:${source[key]}`;
      missing.push(key);
    }
  }

  fs.writeFileSync(file, JSON.stringify(sortObject(next), null, 2));

  const batch = {};
  for (const key of sourceKeys) {
    if (String(next[key]).startsWith('TODO:')) batch[key] = source[key];
  }
  fs.writeFileSync(path.join(outDir, `translation-batch.${locale}.json`), JSON.stringify(batch, null, 2));

  report.push({ locale, missing, extra, todo: Object.keys(batch).length });
}

fs.writeFileSync(metaPath, JSON.stringify(sortObject(nextMeta), null, 2));

const md = [
  '# Locale Key Report',
  '',
  `Source locale: ${sourceLocale}`,
  `Locale directory: ${localeDir}`,
  args.includes('--steam-full') ? 'Target set: Steam full platform/API languages' : `Target set: ${localeList.join(', ')}`,
  '',
  '| Locale | Missing Added | TODO Values | Extra Keys |',
  '| --- | ---: | ---: | ---: |',
  ...report.map((item) => `| ${item.locale} | ${item.missing.length} | ${item.todo} | ${item.extra.length} |`),
  '',
  '## Details',
  ...report.flatMap((item) => [
    '',
    `### ${item.locale}`,
    item.missing.length ? `Missing added: ${item.missing.map((key) => `\`${key}\``).join(', ')}` : 'Missing added: none',
    item.extra.length ? `Extra keys: ${item.extra.map((key) => `\`${key}\``).join(', ')}` : 'Extra keys: none'
  ])
].join('\n');

fs.writeFileSync(path.join(outDir, 'locale-key-report.md'), `${md}\n`);
console.log(`Locale keys synced for: ${localeList.join(', ')}`);
console.log(`Report: ${path.join(outDir, 'locale-key-report.md')}`);
console.log(`Locale metadata: ${metaPath}`);
