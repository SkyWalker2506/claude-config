#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';

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

function ffmpegExists() {
  const result = spawnSync('ffmpeg', ['-version'], { stdio: 'ignore' });
  return result.status === 0;
}

const postsDir = path.join(projectRoot, 'posts');
const assetsDir = path.join(postsDir, 'assets');
const number = Number(option('number', nextPostNumber(postsDir)));
const out = path.resolve(option('out', path.join(assetsDir, `post_${number}.gif`)));
const frameDir = path.resolve(option('frames', path.join(assetsDir, `post_${number}_frames_${Date.now()}`)));
const selector = option('selector', '');
const durationMs = Number(option('duration', '3500'));
const fps = Number(option('fps', '12'));
const waitMs = Number(option('wait', '1200'));
const width = Number(option('width', '1280'));
const height = Number(option('height', '720'));
const file = option('file', '');
const evaluate = option('evaluate', '');
let url = option('url', '');

if (!url && file) {
  url = pathToFileURL(path.resolve(projectRoot, file)).href;
}
if (!url) {
  throw new Error('Pass --url http://localhost:5173 or --file index.html');
}

fs.mkdirSync(path.dirname(out), { recursive: true });
fs.mkdirSync(frameDir, { recursive: true });

const { chromium } = await loadPlaywright();
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(waitMs);
  if (evaluate) await page.evaluate(evaluate);

  const frameCount = Math.max(1, Math.ceil((durationMs / 1000) * fps));
  const frameDelay = Math.max(1, Math.round(1000 / fps));
  const locator = selector ? page.locator(selector).first() : null;
  if (locator) await locator.waitFor({ state: 'visible', timeout: 10000 });

  for (let i = 0; i < frameCount; i++) {
    const framePath = path.join(frameDir, `frame_${String(i).padStart(4, '0')}.png`);
    if (locator) await locator.screenshot({ path: framePath });
    else await page.screenshot({ path: framePath, fullPage: false });
    await page.waitForTimeout(frameDelay);
  }
} finally {
  await browser.close();
}

if (!ffmpegExists()) {
  console.error(`Frames captured but ffmpeg was not found on PATH. Frames: ${frameDir}`);
  process.exitCode = 2;
} else {
  const palette = path.join(frameDir, 'palette.png');
  const inputPattern = path.join(frameDir, 'frame_%04d.png');
  const paletteResult = spawnSync('ffmpeg', [
    '-y', '-framerate', String(fps), '-i', inputPattern,
    '-vf', 'palettegen=stats_mode=diff', palette
  ], { stdio: 'inherit' });

  if (paletteResult.status !== 0) {
    throw new Error('ffmpeg palette generation failed.');
  }

  const gifResult = spawnSync('ffmpeg', [
    '-y', '-framerate', String(fps), '-i', inputPattern,
    '-i', palette,
    '-lavfi', `fps=${fps},scale=${width}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3`,
    out
  ], { stdio: 'inherit' });

  if (gifResult.status !== 0) {
    throw new Error('ffmpeg GIF encoding failed.');
  }

  console.log(`GIF saved: ${out}`);
}

console.log(`Frames saved: ${frameDir}`);
