#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : process.cwd());

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

const theme = option('theme', 'neutral');
const researchedUiFont = option('ui-font', '');
const researchedDisplayFont = option('display-font', '');
const quoteFont = (font) => `"${String(font).replaceAll('"', '\\"')}"`;
const themeUiCandidates = {
  'sci-fi': ['Rajdhani', 'Exo 2'],
  fantasy: ['Alegreya', 'Cinzel'],
  cozy: ['Nunito', 'Baloo 2'],
  horror: ['Alegreya Sans', 'Noto Sans'],
  retro: ['Oxanium', 'Noto Sans'],
  minimal: ['Inter', 'Noto Sans'],
  neutral: ['Inter', 'Noto Sans']
}[theme] || ['Inter', 'Noto Sans'];
const themeDisplay = {
  'sci-fi': 'Rajdhani',
  fantasy: 'Cinzel',
  cozy: 'Nunito',
  horror: 'Alegreya Sans',
  retro: 'Oxanium',
  minimal: 'Inter',
  neutral: 'Inter'
}[theme] || 'Inter';
const uiPrimary = researchedUiFont || themeUiCandidates[0];
const displayPrimary = researchedDisplayFont || themeDisplay;
const notoFallbacks = ['Noto Sans', 'Noto Sans Arabic', 'Noto Sans SC', 'Noto Sans TC', 'Noto Sans JP', 'Noto Sans KR', 'Noto Sans Thai'];
const uiStack = [uiPrimary, ...themeUiCandidates.filter((font) => font !== uiPrimary), ...notoFallbacks].filter((font, index, arr) => arr.indexOf(font) === index).map(quoteFont).join(', ');
const displayStack = [displayPrimary, uiPrimary, ...notoFallbacks].filter((font, index, arr) => arr.indexOf(font) === index).map(quoteFont).join(', ');
function localeStack(scriptFallback) {
  const fonts = researchedUiFont
    ? [uiPrimary, scriptFallback, ...notoFallbacks]
    : [scriptFallback, uiPrimary, ...notoFallbacks];
  return fonts.filter((font, index, arr) => arr.indexOf(font) === index).map(quoteFont).join(', ');
}

const themeDir = path.join(projectRoot, 'src', 'theme');
const outDir = path.join(projectRoot, 'buildable', 'typography');
const created = [];

const css = `:root {
  --font-ui: ${uiStack}, system-ui, sans-serif;
  --font-display: ${displayStack}, system-ui, sans-serif;
  --font-hud: var(--font-ui);
  --font-mono: "Consolas", "Menlo", monospace;
  --hud-popup-color: #ffffff;
  --hud-popup-shadow: 0 3px 18px rgb(0 0 0 / 0.55);
  --hud-popup-backplate: rgb(10 14 18 / 0.42);
}

[data-locale="ar"],
[lang="ar"] {
  --font-ui: ${localeStack('Noto Sans Arabic')}, system-ui, sans-serif;
  direction: rtl;
}

[data-locale="zh-CN"],
[lang="zh-CN"] {
  --font-ui: ${localeStack('Noto Sans SC')}, system-ui, sans-serif;
}

[data-locale="zh-TW"],
[lang="zh-TW"] {
  --font-ui: ${localeStack('Noto Sans TC')}, system-ui, sans-serif;
}

[data-locale="ja"],
[lang="ja"] {
  --font-ui: ${localeStack('Noto Sans JP')}, system-ui, sans-serif;
}

[data-locale="ko"],
[lang="ko"] {
  --font-ui: ${localeStack('Noto Sans KR')}, system-ui, sans-serif;
}

[data-locale="th"],
[lang="th"] {
  --font-ui: ${localeStack('Noto Sans Thai')}, system-ui, sans-serif;
}

body,
button,
input,
select,
textarea {
  font-family: var(--font-ui);
}

.font-display {
  font-family: var(--font-display);
}

.hud-popup {
  position: fixed;
  inset: 42% 16px auto;
  z-index: 50;
  display: grid;
  place-items: center;
  pointer-events: none;
  text-align: center;
  color: var(--hud-popup-color);
  font-family: var(--font-hud);
  font-size: clamp(24px, 4vw, 56px);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: 0;
  text-wrap: balance;
  overflow-wrap: anywhere;
  text-shadow: var(--hud-popup-shadow);
}

.hud-popup__text {
  max-width: min(760px, calc(100vw - 32px));
  padding: 10px 18px;
  border-radius: 8px;
  background: var(--hud-popup-backplate);
  transform-origin: center;
  animation: hud-popup-pop 900ms ease both;
}

@keyframes hud-popup-pop {
  0% {
    opacity: 0;
    transform: translateY(10px) scale(0.94);
  }
  18% {
    opacity: 1;
    transform: translateY(0) scale(1.02);
  }
  72% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-8px) scale(0.98);
  }
}
`;

const plan = {
  theme,
  researchRequired: !researchedUiFont,
  selectionRule: 'Use a researched theme-appropriate free/open-source UI font first; keep Noto as fallback coverage, not the default first choice.',
  researchGate: researchedUiFont
    ? 'Research font was provided through --ui-font. Verify source URL, license, weights, and script coverage before shipping.'
    : 'Research is still required. Browse current free/open-source font sources and compare theme-fit candidates before treating this scaffold as final.',
  roles: {
    ui: [uiPrimary, ...themeUiCandidates.filter((font) => font !== uiPrimary)],
    fallback: notoFallbacks,
    display: displayPrimary,
    hud: 'Use --font-hud for center popups and localized moment text.'
  },
  candidateNotes: 'Verify current license, source URL, available weights, and script coverage before shipping. Pass --ui-font and --display-font after research to lock choices.',
  localizeCompatible: true,
  steamCompatible: 'Self-host fonts under public/fonts before shipping.'
};

if (writeNew(path.join(themeDir, 'typography.css'), css)) created.push('src/theme/typography.css');
if (writeNew(path.join(themeDir, 'font-plan.json'), JSON.stringify(plan, null, 2))) created.push('src/theme/font-plan.json');
if (writeNew(path.join(outDir, 'FONT_NOTICES.md'), `# Font Notices

Chosen UI candidate: ${uiPrimary}
Chosen display candidate: ${displayPrimary}

Verify current source URLs and licenses before shipping. Prefer theme-appropriate free/open-source fonts found through current research. Keep Noto families only as fallback coverage when candidates miss scripts.

Research status: ${researchedUiFont ? 'UI font was provided manually; verify and record its source/license.' : 'Provisional scaffold only; perform internet font research before shipping.'}

Fallback source: https://notofonts.github.io/
Fallback license: Verify current font files before shipping; Noto families are commonly distributed under the SIL Open Font License.

Record every bundled font source, license, copyright notice, and any reserved font name notes here.
`)) created.push('buildable/typography/FONT_NOTICES.md');

console.log(`Typography scaffold checked: ${projectRoot}`);
if (created.length) {
  console.log('Created files:');
  for (const file of created) console.log(`- ${file}`);
} else {
  console.log('No new files created; existing typography files were preserved.');
}
