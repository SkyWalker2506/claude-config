#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const projectRoot = path.resolve(process.argv[2] || process.cwd());
const postsDir = path.join(projectRoot, 'posts');

function read(file) {
  try {
    return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  } catch {
    return '';
  }
}

function postNumber(file) {
  const match = path.basename(file).match(/^post_(\d+)\.md$/);
  return match ? Number(match[1]) : -1;
}

function summarizePost(file) {
  const text = read(file);
  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const heading = lines.find((line) => /^#\s+/.test(line)) || '';
  const image = lines.find((line) => /!\[.*\]\(.+\)/.test(line)) || '';
  const gif = (text.match(/gif:\s*"?([^"\n]+)"?/i) || text.match(/\*\*GIF:\*\*\s*(.+)/i) || [])[1] || '';
  const platform = (text.match(/platform:\s*"?([^"\n]+)"?/i) || text.match(/\*\*Platform:\*\*\s*(.+)/i) || [])[1] || '';
  const target = (text.match(/target:\s*"?([^"\n]+)"?/i) || text.match(/\*\*Target:\*\*\s*(.+)/i) || [])[1] || '';
  const hook = (text.match(/hook:\s*"?([^"\n]+)"?/i) || text.match(/\*\*Primary Hook:\*\*\s*(.+)/i) || [])[1] || '';
  return {
    file: path.relative(projectRoot, file).replaceAll('\\', '/'),
    number: postNumber(file),
    heading: heading.replace(/^#\s+/, ''),
    platform: platform.trim(),
    target: target.trim(),
    hook: hook.trim(),
    gif: gif.trim(),
    image: image.trim()
  };
}

fs.mkdirSync(postsDir, { recursive: true });
const posts = fs.readdirSync(postsDir)
  .filter((name) => /^post_\d+\.md$/.test(name))
  .map((name) => path.join(postsDir, name))
  .sort((a, b) => postNumber(a) - postNumber(b))
  .map(summarizePost);

const nextNumber = posts.length ? Math.max(...posts.map((post) => post.number)) + 1 : 0;
const usedTargets = [...new Set(posts.map((post) => post.target).filter(Boolean))];
const usedHooks = [...new Set(posts.map((post) => post.hook).filter(Boolean))];
const usedPlatforms = [...new Set(posts.map((post) => post.platform).filter(Boolean))];

const report = {
  projectRoot,
  postsDir,
  postCount: posts.length,
  nextNumber,
  usedPlatforms,
  usedTargets,
  usedHooks,
  posts
};

fs.writeFileSync(path.join(postsDir, 'post-history-analysis.json'), JSON.stringify(report, null, 2));

const md = [
  '# Post History Analysis',
  '',
  `Project: ${projectRoot}`,
  `Post count: ${posts.length}`,
  `Next post: post_${nextNumber}.md`,
  '',
  '## Used Platforms',
  ...(usedPlatforms.length ? usedPlatforms.map((item) => `- ${item}`) : ['- None yet.']),
  '',
  '## Used Targets',
  ...(usedTargets.length ? usedTargets.map((item) => `- ${item}`) : ['- None yet.']),
  '',
  '## Used Hooks',
  ...(usedHooks.length ? usedHooks.map((item) => `- ${item}`) : ['- None yet.']),
  '',
  '## Posts',
  ...(posts.length ? posts.map((post) => `- ${post.file}: ${post.hook || post.heading || 'No hook recorded'}`) : ['- No previous posts found.'])
].join('\n');

fs.writeFileSync(path.join(postsDir, 'post-history-analysis.md'), `${md}\n`);
console.log(`Post history analyzed. Next post number: ${nextNumber}`);
console.log(`Report: ${path.join(postsDir, 'post-history-analysis.md')}`);
