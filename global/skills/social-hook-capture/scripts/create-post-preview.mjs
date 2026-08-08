#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

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

function rel(file) {
  return path.relative(postsDir, path.resolve(projectRoot, file)).replaceAll('\\', '/');
}

const postsDir = path.join(projectRoot, 'posts');
fs.mkdirSync(postsDir, { recursive: true });
fs.mkdirSync(path.join(postsDir, 'assets'), { recursive: true });

const number = Number(option('number', nextPostNumber(postsDir)));
const postPath = path.join(postsDir, `post_${number}.md`);
const platform = option('platform', 'reddit');
const target = option('target', '');
const screenshot = option('screenshot', `posts/assets/post_${number}.png`);
const gif = option('gif', '');
const hook = option('hook', '');
const audience = option('audience', '');
const historyPath = path.join(postsDir, 'post-history-analysis.md');
const historyNote = fs.existsSync(historyPath)
  ? 'Review `post-history-analysis.md` before finalizing to avoid repeating prior hooks.'
  : 'Run `analyze-post-history.mjs` before finalizing to avoid repetition.';

if (fs.existsSync(postPath)) {
  throw new Error(`Post already exists: ${postPath}`);
}

const screenshotRel = rel(screenshot);
const gifRel = gif ? rel(gif) : '';
const content = `---
post_number: ${number}
platform: "${platform}"
target: "${target}"
audience: "${audience}"
hook: "${hook}"
screenshot: "${screenshotRel}"
gif: "${gifRel}"
status: "draft"
---

# Post ${number} Preview

![Hook screenshot](${screenshotRel})
${gifRel ? `\n![Hook GIF](${gifRel})\n` : ''}

## Target

- Platform: ${platform}
- Target: ${target || 'TODO'}
- Audience: ${audience || 'TODO'}
- Primary hook: ${hook || 'TODO'}
- Media: ${gifRel ? `GIF \`${gifRel}\` plus screenshot \`${screenshotRel}\`` : `Screenshot \`${screenshotRel}\``}

## History Notes

${historyNote}

## Hook Options

1. TODO
2. TODO
3. TODO

## Recommended Draft

### Reddit Title

TODO

### Reddit Body

TODO

### Short Social Variant

TODO

## QA

- [ ] Screenshot exists and supports the hook.
- [ ] GIF exists and shows the hook quickly, if used.
- [ ] First line is specific and not generic hype.
- [ ] Target community/platform fit is clear.
- [ ] No repeated angle from previous posts.
- [ ] No misleading claim or fake metric.
- [ ] Final copy has no TODO placeholders.
`;

fs.writeFileSync(postPath, content.replace(/\n/g, '\r\n'));
console.log(`Post preview created: ${postPath}`);
