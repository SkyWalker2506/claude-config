#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : process.cwd());

function option(name, fallback) {
  const index = args.indexOf(`--${name}`);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

function nextPostNumber(postsDir) {
  if (!fs.existsSync(postsDir)) return 0;
  const nums = fs.readdirSync(postsDir)
    .map((name) => name.match(/^post_(\d+)\.md$/))
    .filter(Boolean)
    .map((match) => Number(match[1]));
  return nums.length ? Math.max(...nums) + 1 : 0;
}

async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {
    try {
      const requireFromProject = createRequire(path.join(projectRoot, 'package.json'));
      return requireFromProject('playwright');
    } catch {
      throw new Error('Playwright is not installed. Run `npm install -D playwright` in the target project or tool environment, then rerun this script.');
    }
  }
}

const postsDir = path.join(projectRoot, 'posts');
const assetsDir = path.join(postsDir, 'assets');
const number = Number(option('number', nextPostNumber(postsDir)));
const out = path.resolve(option('out', path.join(assetsDir, `post_${number}.png`)));
const selector = option('selector', '');
const waitMs = Number(option('wait', '1200'));
const width = Number(option('width', '1280'));
const height = Number(option('height', '720'));
const file = option('file', '');
let url = option('url', '');

if (!url && file) {
  url = pathToFileURL(path.resolve(projectRoot, file)).href;
}
if (!url) {
  throw new Error('Pass --url http://localhost:5173 or --file index.html');
}

fs.mkdirSync(path.dirname(out), { recursive: true });
const { chromium } = await loadPlaywright();
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(waitMs);

  if (selector) {
    const target = page.locator(selector).first();
    await target.waitFor({ state: 'visible', timeout: 10000 });
    await target.screenshot({ path: out });
  } else {
    await page.screenshot({ path: out, fullPage: false });
  }
} finally {
  await browser.close();
}

console.log(`Screenshot saved: ${out}`);
