#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const projectRoot = path.resolve(process.argv[2] || process.cwd());
const outDir = path.join(projectRoot, 'buildable', 'typography');
const cssPath = path.join(projectRoot, 'src', 'theme', 'typography.css');
const samples = {
  en: 'Wave clear! Collect the reward.',
  tr: 'Dalga temizlendi! \u00d6d\u00fcl\u00fc topla.',
  de: 'Welle abgeschlossen! Sammle die Belohnung ein.',
  fr: 'Vague termin\u00e9e ! R\u00e9cup\u00e9rez la r\u00e9compense.',
  es: 'Oleada superada. Recoge la recompensa.',
  ru: '\u0412\u043e\u043b\u043d\u0430 \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430! \u0417\u0430\u0431\u0435\u0440\u0438\u0442\u0435 \u043d\u0430\u0433\u0440\u0430\u0434\u0443.',
  uk: '\u0425\u0432\u0438\u043b\u044e \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e! \u0417\u0430\u0431\u0435\u0440\u0456\u0442\u044c \u043d\u0430\u0433\u043e\u0440\u043e\u0434\u0443.',
  el: '\u03a4\u03bf \u03ba\u03cd\u03bc\u03b1 \u03bf\u03bb\u03bf\u03ba\u03bb\u03b7\u03c1\u03ce\u03b8\u03b7\u03ba\u03b5! \u03a0\u03ac\u03c1\u03b5 \u03c4\u03b7\u03bd \u03b1\u03bd\u03c4\u03b1\u03bc\u03bf\u03b9\u03b2\u03ae.',
  ar: '\u0627\u0643\u062a\u0645\u0644\u062a \u0627\u0644\u0645\u0648\u062c\u0629! \u0627\u062c\u0645\u0639 \u0627\u0644\u0645\u0643\u0627\u0641\u0623\u0629.',
  th: '\u0e40\u0e04\u0e25\u0e35\u0e22\u0e23\u0e4c\u0e23\u0e30\u0e25\u0e2d\u0e01\u0e41\u0e25\u0e49\u0e27! \u0e23\u0e31\u0e1a\u0e23\u0e32\u0e07\u0e27\u0e31\u0e25\u0e02\u0e2d\u0e07\u0e04\u0e38\u0e13',
  vi: '\u0110\u1ee3t t\u1ea5n c\u00f4ng \u0111\u00e3 xong! Nh\u1eadn ph\u1ea7n th\u01b0\u1edfng.',
  ja: '\u30a6\u30a7\u30fc\u30d6\u5b8c\u4e86\uff01\u5831\u916c\u3092\u53d7\u3051\u53d6\u308d\u3046\u3002',
  ko: '\uc6e8\uc774\ube0c \uc644\ub8cc! \ubcf4\uc0c1\uc744 \ubc1b\uc73c\uc138\uc694.',
  'zh-CN': '\u6ce2\u6b21\u5b8c\u6210\uff01\u9886\u53d6\u5956\u52b1\u3002',
  'zh-TW': '\u6ce2\u6b21\u5b8c\u6210\uff01\u9818\u53d6\u734e\u52f5\u3002'
};
const stressSamples = {
  de: 'Belohnung sofort einsammeln und Verbesserungsfenster \u00f6ffnen',
  tr: 'Geli\u015ftirme se\u00e7eneklerini hemen kar\u015f\u0131la\u015ft\u0131r',
  ar: '\u0627\u0641\u062a\u062d \u062e\u064a\u0627\u0631\u0627\u062a \u0627\u0644\u062a\u0631\u0642\u064a\u0629 \u0648\u0627\u062c\u0645\u0639 \u0627\u0644\u0645\u0643\u0627\u0641\u0623\u0629',
  th: '\u0e40\u0e1b\u0e34\u0e14\u0e15\u0e31\u0e27\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e2d\u0e31\u0e1b\u0e40\u0e01\u0e23\u0e14\u0e41\u0e25\u0e30\u0e23\u0e31\u0e1a\u0e23\u0e32\u0e07\u0e27\u0e31\u0e25',
  vi: 'M\u1edf b\u1ea3ng n\u00e2ng c\u1ea5p v\u00e0 nh\u1eadn ph\u1ea7n th\u01b0\u1edfng ngay',
  ja: '\u30a2\u30c3\u30d7\u30b0\u30ec\u30fc\u30c9\u3092\u9078\u3093\u3067\u5831\u916c\u3092\u53d7\u3051\u53d6\u308b',
  ko: '\uc5c5\uadf8\ub808\uc774\ub4dc\ub97c \uc120\ud0dd\ud558\uace0 \ubcf4\uc0c1\uc744 \ubc1b\uc73c\uc138\uc694',
  'zh-CN': '\u9009\u62e9\u5347\u7ea7\u5e76\u7acb\u5373\u9886\u53d6\u5956\u52b1'
};

fs.mkdirSync(outDir, { recursive: true });
const cssLink = fs.existsSync(cssPath)
  ? '<link rel="stylesheet" href="../../src/theme/typography.css">'
  : '<style>body{font-family:system-ui,sans-serif}.hud-popup__text{padding:10px 18px;background:#17202a;color:white;border-radius:8px}</style>';

const html = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Preview</title>
    ${cssLink}
    <style>
      body { margin: 24px; background: #101419; color: #f6f7f9; }
      main { max-width: 980px; margin: 0 auto; }
      .sample { margin: 14px 0; padding: 14px; border: 1px solid rgb(255 255 255 / 0.14); border-radius: 8px; }
      .locale { opacity: 0.68; font-size: 12px; margin-bottom: 6px; }
      .stress-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; margin: 18px 0; }
      .stress-card { min-width: 0; padding: 12px; border: 1px solid rgb(255 255 255 / 0.14); border-radius: 8px; background: rgb(255 255 255 / 0.04); }
      .narrow-button { inline-size: 170px; min-block-size: 42px; display: inline-grid; place-items: center; padding: 8px 12px; border-radius: 6px; background: #d6f35f; color: #101419; font-weight: 700; text-align: center; overflow-wrap: anywhere; }
      .dialogue-box { inline-size: min(100%, 270px); min-block-size: 74px; padding: 10px 12px; border-radius: 8px; background: rgb(255 255 255 / 0.1); overflow-wrap: anywhere; }
      .popup-box { inline-size: min(100%, 300px); min-block-size: 96px; display: grid; place-items: center; overflow: hidden; }
      .hud-demo { position: relative; min-height: 220px; border: 1px solid rgb(255 255 255 / 0.14); border-radius: 8px; overflow: hidden; }
      .hud-demo .hud-popup { position: absolute; }
    </style>
  </head>
  <body>
    <main>
      <h1 class="font-display">Theme Font Preview</h1>
      <section class="hud-demo" data-locale="en">
        <div class="hud-popup"><div class="hud-popup__text">Wave clear! +250 XP</div></div>
      </section>
      <h2>Overflow Stress Preview</h2>
      <section class="stress-grid">
        ${Object.entries(stressSamples).map(([locale, text]) => `<article class="stress-card" data-locale="${locale}" lang="${locale}" dir="${locale === 'ar' ? 'rtl' : 'auto'}"><div class="locale">${locale}</div><div class="narrow-button">${text}</div><div class="dialogue-box">${text}</div><div class="popup-box"><div class="hud-popup__text">${text}</div></div></article>`).join('\n        ')}
      </section>
      ${Object.entries(samples).map(([locale, text]) => `<section class="sample" data-locale="${locale}" lang="${locale}" dir="${locale === 'ar' ? 'rtl' : 'auto'}"><div class="locale">${locale}</div><div>${text}</div><div class="hud-popup__text">${text}</div></section>`).join('\n      ')}
    </main>
  </body>
</html>
`;

fs.writeFileSync(path.join(outDir, 'font-preview.html'), html.replace(/\n/g, '\r\n'));
console.log(`Font preview written: ${path.join(outDir, 'font-preview.html')}`);
