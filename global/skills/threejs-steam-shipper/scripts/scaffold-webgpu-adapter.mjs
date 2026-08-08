#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const projectRoot = path.resolve(args[0] || process.cwd());
const adapterPath = path.join(projectRoot, 'src', 'rendering', 'createThreeRenderer.mjs');
const reportDir = path.join(projectRoot, 'buildable', 'reports');
const reportPath = path.join(reportDir, 'webgpu-adapter-notes.md');

function writeNew(file, content) {
  if (fs.existsSync(file)) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content.replace(/\n/g, '\r\n'));
  return true;
}

const adapter = `import { WebGLRenderer } from 'three';

export async function createThreeRenderer(options = {}) {
  const { forceWebGL: forceWebGLOption, ...rendererOptions } = options;
  const params = {
    antialias: true,
    powerPreference: 'high-performance',
    ...rendererOptions
  };
  const query = new URLSearchParams(globalThis.location?.search || '');
  const forceWebGL = query.get('renderer') === 'webgl' || forceWebGLOption === true;

  if (!forceWebGL && globalThis.navigator?.gpu) {
    try {
      const { WebGPURenderer } = await import('three/webgpu');
      const renderer = new WebGPURenderer(params);
      await renderer.init();
      renderer.userData = { ...(renderer.userData || {}), backend: 'webgpu' };
      return renderer;
    } catch (error) {
      console.warn('[renderer] WebGPU unavailable, falling back to WebGL.', error);
    }
  }

  const renderer = new WebGLRenderer(params);
  renderer.userData = { ...(renderer.userData || {}), backend: 'webgl' };
  return renderer;
}
`;

const report = `# WebGPU Adapter Notes

Created a progressive renderer factory at \`src/rendering/createThreeRenderer.mjs\`.

Integration:

- Replace direct \`new THREE.WebGLRenderer(...)\` construction with \`await createThreeRenderer(...)\`.
- Keep scene, camera, resize, animation loop, and post-processing behavior unchanged during the first pass.
- Use \`?renderer=webgl\` to force the fallback path during QA.
- Avoid WebGPU-only compute, custom WGSL, or node-material features until WebGL fallback is no longer required.
- Test WebGPU in a secure browser context and test WebGL fallback in Electron, mobile WebViews, and unsupported browsers.
`;

const created = [];
if (writeNew(adapterPath, adapter)) created.push(path.relative(projectRoot, adapterPath).replaceAll('\\', '/'));
fs.mkdirSync(reportDir, { recursive: true });
fs.writeFileSync(reportPath, report.replace(/\n/g, '\r\n'));

console.log(`WebGPU adapter notes written: ${reportPath}`);
if (created.length) {
  console.log('Created files:');
  for (const file of created) console.log(`- ${file}`);
} else {
  console.log('Adapter already exists; left it unchanged.');
}
