#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const targetRoot = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : process.cwd());

function option(name, fallback) {
  const index = args.indexOf(`--${name}`);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
}

function slug(value) {
  return String(value || 'threejs-prototype')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'threejs-prototype';
}

function title(value) {
  return String(value || 'Three.js Prototype').trim() || 'Three.js Prototype';
}

function writeNew(relativePath, content) {
  const file = path.join(targetRoot, relativePath);
  if (fs.existsSync(file)) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, content.replace(/\n/g, '\r\n'));
  return true;
}

const projectTitle = title(option('name', path.basename(targetRoot)));
const packageName = slug(projectTitle);
const created = [];

fs.mkdirSync(targetRoot, { recursive: true });
fs.mkdirSync(path.join(targetRoot, 'public', 'assets'), { recursive: true });
fs.mkdirSync(path.join(targetRoot, 'src'), { recursive: true });

function add(relativePath, content) {
  if (writeNew(relativePath, content)) created.push(relativePath);
}

add('package.json', JSON.stringify({
  name: packageName,
  version: '0.1.0',
  private: true,
  type: 'module',
  scripts: {
    dev: 'vite',
    build: 'vite build',
    preview: 'vite preview'
  },
  dependencies: {
    three: '^0.180.0'
  },
  devDependencies: {
    vite: '^7.0.0'
  }
}, null, 2));

add('vite.config.js', `import { defineConfig } from 'vite';

export default defineConfig({
  base: './'
});
`);

add('index.html', `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <title>${projectTitle}</title>
  </head>
  <body>
    <main id="app">
      <canvas id="game"></canvas>
      <section id="hud" aria-live="polite">
        <h1 id="title"></h1>
        <p id="hint"></p>
      </section>
      <section id="touch-controls" aria-label="Touch controls">
        <div id="stick-zone" aria-label="Move">
          <div id="stick-knob"></div>
        </div>
        <button id="action-button" type="button" aria-label="Action">A</button>
      </section>
    </main>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
`);

add('src/main.js', `import * as THREE from 'three';
import './styles.css';
import { createInput, whenRuntimeReady } from './input.js';
import { createPrototypeScene } from './scene.js';
import { createUi } from './ui.js';

await whenRuntimeReady();

const canvas = document.querySelector('#game');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
camera.position.set(0, 3, 7);

const input = createInput({
  canvas,
  touchControls: document.querySelector('#touch-controls')
});
const ui = createUi();
const prototype = createPrototypeScene({ THREE, camera });

function resize() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

window.addEventListener('resize', resize);
resize();
ui.setStatus(input.describeControls());

let lastTime = performance.now();
function animate(time) {
  const delta = Math.min((time - lastTime) / 1000, 0.05);
  lastTime = time;
  input.update();
  if (!input.state.paused) {
    prototype.update(delta, input.state);
  }
  renderer.render(prototype.scene, camera);
  requestAnimationFrame(animate);
}

requestAnimationFrame(animate);
`);

add('src/scene.js', `export function createPrototypeScene({ THREE, camera }) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x101419);

  const player = new THREE.Mesh(
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.MeshStandardMaterial({ color: 0x62d2ff, roughness: 0.45 })
  );
  player.position.y = 0.6;
  scene.add(player);

  const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(12, 12),
    new THREE.MeshStandardMaterial({ color: 0x202832, roughness: 0.9 })
  );
  floor.rotation.x = -Math.PI / 2;
  scene.add(floor);

  const marker = new THREE.Mesh(
    new THREE.TorusGeometry(1.8, 0.035, 12, 96),
    new THREE.MeshBasicMaterial({ color: 0xffd166 })
  );
  marker.rotation.x = -Math.PI / 2;
  marker.position.y = 0.03;
  scene.add(marker);

  const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
  keyLight.position.set(4, 6, 3);
  scene.add(keyLight);
  scene.add(new THREE.AmbientLight(0x9bb4c7, 0.65));

  const velocity = new THREE.Vector3();
  const direction = new THREE.Vector3();

  function update(delta, input) {
    direction.set(input.moveX, 0, input.moveY);
    if (direction.lengthSq() > 1) direction.normalize();

    velocity.lerp(direction.multiplyScalar(4), 1 - Math.pow(0.001, delta));
    player.position.addScaledVector(velocity, delta);
    player.position.x = THREE.MathUtils.clamp(player.position.x, -5, 5);
    player.position.z = THREE.MathUtils.clamp(player.position.z, -5, 5);

    const pulse = input.action ? 1.25 : 1;
    player.scale.setScalar(THREE.MathUtils.lerp(player.scale.x, pulse, 1 - Math.pow(0.001, delta)));
    player.rotation.y += delta * (input.action ? 4 : 1);
    marker.rotation.z -= delta * 0.8;

    camera.position.x = THREE.MathUtils.lerp(camera.position.x, player.position.x * 0.35, 0.06);
    camera.lookAt(player.position.x, 0.8, player.position.z);
  }

  return { scene, update };
}
`);

add('src/input.js', `const DEADZONE = 0.18;

export function whenRuntimeReady() {
  if (!globalThis.cordova) return Promise.resolve();
  return new Promise((resolve) => {
    document.addEventListener('deviceready', resolve, { once: true });
  });
}

export function createInput({ canvas = window, touchControls = null } = {}) {
  const params = new URLSearchParams(globalThis.location?.search || '');
  const requestedControls = params.get('controls');
  const hasTouch = Boolean(globalThis.cordova || navigator.maxTouchPoints > 0 || matchMedia('(pointer: coarse)').matches);
  const touchMode = requestedControls === 'touch' || (!requestedControls && hasTouch);
  const state = {
    moveX: 0,
    moveY: 0,
    action: false,
    paused: document.visibilityState === 'hidden',
    activeControls: touchMode ? 'touch' : 'desktop'
  };

  const keysDown = new Set();
  const keyMap = new Map([
    ['KeyW', ['y', -1]],
    ['ArrowUp', ['y', -1]],
    ['KeyS', ['y', 1]],
    ['ArrowDown', ['y', 1]],
    ['KeyA', ['x', -1]],
    ['ArrowLeft', ['x', -1]],
    ['KeyD', ['x', 1]],
    ['ArrowRight', ['x', 1]]
  ]);
  const touchAxis = { x: 0, y: 0, active: false };
  let keyboardAction = false;
  let pointerAction = false;
  let stickPointerId = null;
  let stickOrigin = null;

  document.documentElement.dataset.controls = touchMode ? 'touch' : 'desktop';
  if (canvas?.style) canvas.style.touchAction = 'none';

  function markControls(mode) {
    state.activeControls = mode;
    document.documentElement.dataset.lastInput = mode;
  }

  function setKey(event, down) {
    if (keyMap.has(event.code)) {
      if (down) keysDown.add(event.code);
      else keysDown.delete(event.code);
      markControls('keyboard');
      event.preventDefault();
    }
    if (event.code === 'Space') {
      keyboardAction = down;
      markControls('keyboard');
      event.preventDefault();
    }
  }

  window.addEventListener('keydown', (event) => setKey(event, true));
  window.addEventListener('keyup', (event) => setKey(event, false));

  canvas.addEventListener('pointerdown', (event) => {
    if (event.pointerType !== 'touch') {
      pointerAction = true;
      markControls('pointer');
    }
  });
  window.addEventListener('pointerup', () => {
    pointerAction = false;
  });

  const stickZone = touchControls?.querySelector('#stick-zone');
  const stickKnob = touchControls?.querySelector('#stick-knob');
  const actionButton = touchControls?.querySelector('#action-button');

  function resetStick() {
    stickPointerId = null;
    stickOrigin = null;
    touchAxis.x = 0;
    touchAxis.y = 0;
    touchAxis.active = false;
    if (stickKnob) stickKnob.style.transform = 'translate3d(0, 0, 0)';
  }

  function moveStick(event) {
    if (event.pointerId !== stickPointerId || !stickOrigin) return;
    const maxDistance = 44;
    const dx = event.clientX - stickOrigin.x;
    const dy = event.clientY - stickOrigin.y;
    const distance = Math.min(Math.hypot(dx, dy), maxDistance);
    const angle = Math.atan2(dy, dx);
    const x = Math.cos(angle) * distance;
    const y = Math.sin(angle) * distance;
    touchAxis.x = x / maxDistance;
    touchAxis.y = y / maxDistance;
    touchAxis.active = true;
    if (stickKnob) stickKnob.style.transform = \`translate3d(\${x}px, \${y}px, 0)\`;
    markControls('touch');
    event.preventDefault();
  }

  stickZone?.addEventListener('pointerdown', (event) => {
    stickPointerId = event.pointerId;
    stickOrigin = { x: event.clientX, y: event.clientY };
    stickZone.setPointerCapture?.(event.pointerId);
    moveStick(event);
  }, { passive: false });
  stickZone?.addEventListener('pointermove', moveStick, { passive: false });
  stickZone?.addEventListener('pointerup', resetStick);
  stickZone?.addEventListener('pointercancel', resetStick);
  stickZone?.addEventListener('lostpointercapture', resetStick);

  actionButton?.addEventListener('pointerdown', (event) => {
    pointerAction = true;
    markControls('touch');
    actionButton.setPointerCapture?.(event.pointerId);
    event.preventDefault();
  }, { passive: false });
  actionButton?.addEventListener('pointerup', () => {
    pointerAction = false;
  });
  actionButton?.addEventListener('pointercancel', () => {
    pointerAction = false;
  });

  function setPaused(paused) {
    state.paused = paused;
  }
  document.addEventListener('visibilitychange', () => setPaused(document.visibilityState === 'hidden'));
  document.addEventListener('pause', () => setPaused(true));
  document.addEventListener('resume', () => setPaused(false));
  document.addEventListener('backbutton', (event) => {
    event.preventDefault();
    setPaused(!state.paused);
  });

  function readKeyboardAxis() {
    let x = 0;
    let y = 0;
    for (const code of keysDown) {
      const [axis, value] = keyMap.get(code);
      if (axis === 'x') x += value;
      if (axis === 'y') y += value;
    }
    return { x: Math.max(-1, Math.min(1, x)), y: Math.max(-1, Math.min(1, y)) };
  }

  function readGamepad() {
    const pads = navigator.getGamepads?.() || [];
    const pad = Array.from(pads).find(Boolean);
    if (!pad) return null;
    const x = Math.abs(pad.axes[0] || 0) > DEADZONE ? pad.axes[0] : 0;
    const y = Math.abs(pad.axes[1] || 0) > DEADZONE ? pad.axes[1] : 0;
    const action = Boolean(pad.buttons[0]?.pressed || pad.buttons[1]?.pressed);
    if (x || y || action) markControls('gamepad');
    return { x, y, action };
  }

  function update() {
    const keyboard = readKeyboardAxis();
    const gamepad = requestedControls === 'touch' ? null : readGamepad();
    const useTouch = touchAxis.active || requestedControls === 'touch';
    const x = useTouch ? touchAxis.x : (gamepad?.x || keyboard.x);
    const y = useTouch ? touchAxis.y : (gamepad?.y || keyboard.y);
    state.moveX = Math.abs(x) > DEADZONE ? x : 0;
    state.moveY = Math.abs(y) > DEADZONE ? y : 0;
    state.action = keyboardAction || pointerAction || Boolean(gamepad?.action);
  }

  function describeControls() {
    if (touchMode) return 'Use the left stick to move. Tap A to pulse.';
    return 'Move with WASD, arrows, or a gamepad. Click or press Space/A to pulse.';
  }

  return { state, update, describeControls };
}
`);

add('src/ui.js', `const text = {
  title: '${projectTitle}',
  hint: 'Move, pulse, and find the fun.'
};

export function createUi() {
  const title = document.querySelector('#title');
  const hint = document.querySelector('#hint');

  title.textContent = text.title;
  hint.textContent = text.hint;

  return {
    setStatus(message) {
      hint.textContent = message;
    }
  };
}
`);

add('src/styles.css', `html,
body,
#app {
  width: 100%;
  height: 100%;
  margin: 0;
  overflow: hidden;
  background: #101419;
  color: #f6f7f9;
  font-family: Arial, sans-serif;
  overscroll-behavior: none;
}

body {
  touch-action: none;
}

#game {
  display: block;
  width: 100%;
  height: 100%;
  touch-action: none;
}

#hud {
  position: fixed;
  left: calc(20px + env(safe-area-inset-left, 0px));
  top: calc(18px + env(safe-area-inset-top, 0px));
  max-width: min(360px, calc(100vw - 48px));
  pointer-events: none;
}

#title {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 700;
}

#hint {
  margin: 0;
  color: #cbd5df;
  font-size: 14px;
  line-height: 1.4;
}

#touch-controls {
  display: none;
  position: fixed;
  inset: auto 0 0;
  min-height: 154px;
  padding:
    18px calc(22px + env(safe-area-inset-right, 0px))
    calc(18px + env(safe-area-inset-bottom, 0px))
    calc(22px + env(safe-area-inset-left, 0px));
  pointer-events: none;
}

[data-controls='touch'] #touch-controls {
  display: block;
}

#stick-zone,
#action-button {
  pointer-events: auto;
  user-select: none;
  -webkit-user-select: none;
  touch-action: none;
}

#stick-zone {
  position: absolute;
  left: calc(22px + env(safe-area-inset-left, 0px));
  bottom: calc(22px + env(safe-area-inset-bottom, 0px));
  width: 116px;
  height: 116px;
  border-radius: 999px;
  background: rgb(255 255 255 / 0.12);
  border: 1px solid rgb(255 255 255 / 0.22);
}

#stick-knob {
  position: absolute;
  left: 34px;
  top: 34px;
  width: 48px;
  height: 48px;
  border-radius: 999px;
  background: #62d2ff;
  box-shadow: 0 8px 24px rgb(0 0 0 / 0.35);
}

#action-button {
  position: absolute;
  right: calc(26px + env(safe-area-inset-right, 0px));
  bottom: calc(32px + env(safe-area-inset-bottom, 0px));
  width: 78px;
  height: 78px;
  border: 0;
  border-radius: 999px;
  background: #ffd166;
  color: #101419;
  font-size: 28px;
  font-weight: 800;
}
`);

console.log(`Three.js prototype scaffold checked: ${targetRoot}`);
if (created.length) {
  console.log('Created files:');
  for (const file of created) console.log(`- ${file}`);
} else {
  console.log('No new files created; existing prototype files were preserved.');
}
