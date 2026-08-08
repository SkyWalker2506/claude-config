#!/usr/bin/env node
import path from 'node:path';
import { createRequire } from 'node:module';
import { spawnSync } from 'node:child_process';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : process.cwd());

async function hasPlaywright() {
  try {
    await import('playwright');
    return true;
  } catch {
    try {
      const requireFromProject = createRequire(path.join(projectRoot, 'package.json'));
      requireFromProject('playwright');
      return true;
    } catch {
      return false;
    }
  }
}

function hasCommand(command) {
  const result = spawnSync(command, ['-version'], { stdio: 'ignore' });
  return result.status === 0;
}

const playwright = await hasPlaywright();
const ffmpeg = hasCommand('ffmpeg');
const issues = [];

if (!playwright) {
  issues.push('Playwright is missing. Install it with: npm install -D playwright');
}
if (!ffmpeg) {
  issues.push('ffmpeg is missing from PATH. Install ffmpeg and ensure the ffmpeg command is available before GIF encoding.');
}

console.log(`Project: ${projectRoot}`);
console.log(`Playwright: ${playwright ? 'available' : 'missing'}`);
console.log(`ffmpeg: ${ffmpeg ? 'available' : 'missing'}`);

if (issues.length) {
  console.log('');
  console.log('Required action for the agent/user:');
  for (const issue of issues) console.log(`- ${issue}`);
  process.exitCode = 1;
} else {
  console.log('Media capture dependencies are ready.');
}
