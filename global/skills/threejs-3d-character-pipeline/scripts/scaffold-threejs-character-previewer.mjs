#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const target = process.argv[2];
if (!target) {
  console.error("Usage: node scaffold-threejs-character-previewer.mjs <target-project> [out-dir]");
  process.exit(1);
}

const projectRoot = path.resolve(target);
const outDir = path.resolve(process.argv[3] || path.join(projectRoot, "buildable", "character-previewer"));
const srcDir = path.join(outDir, "src");
fs.mkdirSync(srcDir, { recursive: true });

const packageJson = {
  scripts: { dev: "vite --host 127.0.0.1", build: "vite build", preview: "vite preview --host 127.0.0.1" },
  dependencies: { "vite": "latest", "three": "latest" },
  devDependencies: {}
};

fs.writeFileSync(path.join(outDir, "package.json"), `${JSON.stringify(packageJson, null, 2)}\n`, "utf8");
fs.writeFileSync(path.join(outDir, "index.html"), `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Three.js Character Previewer</title>
</head>
<body>
  <div id="app">
    <canvas id="viewport"></canvas>
    <aside id="panel">
      <h1>Character Previewer</h1>
      <label class="drop" id="dropzone">
        <input id="file" type="file" accept=".glb,.gltf">
        <span>Drop GLB/GLTF or click</span>
      </label>
      <select id="clips"></select>
      <div class="row">
        <button id="prev">Prev</button>
        <button id="play">Play</button>
        <button id="pause">Pause</button>
        <button id="stop">Stop</button>
        <button id="next">Next</button>
      </div>
      <label>Time <input id="time" type="range" min="0" max="1" value="0" step="0.001"></label>
      <label>Speed <input id="speed" type="range" min="0" max="2" value="1" step="0.05"></label>
      <label><input id="skeleton" type="checkbox"> Skeleton</label>
      <label><input id="wireframe" type="checkbox"> Wireframe</label>
      <pre id="info">Load a rigged GLB/GLTF.</pre>
    </aside>
  </div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
`, "utf8");

fs.writeFileSync(path.join(srcDir, "styles.css"), `html, body, #app { width: 100%; height: 100%; margin: 0; overflow: hidden; }
body { font-family: system-ui, sans-serif; background: #111318; color: #f4f6fb; }
#viewport { display: block; width: 100%; height: 100%; }
#panel { position: fixed; top: 12px; right: 12px; width: min(340px, calc(100vw - 24px)); padding: 12px; background: rgba(18, 21, 29, 0.9); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; backdrop-filter: blur(10px); }
h1 { font-size: 16px; margin: 0 0 10px; }
button, select, input { font: inherit; }
button, select { background: #242a36; color: #f4f6fb; border: 1px solid #3b4353; border-radius: 6px; padding: 7px 9px; }
select { width: 100%; margin: 8px 0; }
.row { display: flex; gap: 6px; flex-wrap: wrap; }
label { display: block; margin-top: 10px; color: #c7cfdd; font-size: 13px; }
input[type="range"] { width: 100%; }
.drop { border: 1px dashed #647089; border-radius: 8px; padding: 14px; text-align: center; cursor: pointer; }
.drop input { display: none; }
.drop.drag { border-color: #86efac; background: rgba(134, 239, 172, 0.08); }
pre { white-space: pre-wrap; color: #aeb7c8; font-size: 12px; }
`, "utf8");

fs.writeFileSync(path.join(srcDir, "main.js"), `import './styles.css';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const canvas = document.querySelector('#viewport');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111318);

const camera = new THREE.PerspectiveCamera(45, 1, 0.01, 500);
camera.position.set(3, 2.2, 4);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.HemisphereLight(0xffffff, 0x334455, 2.2));
const key = new THREE.DirectionalLight(0xffffff, 2.4);
key.position.set(4, 6, 5);
scene.add(key);
scene.add(new THREE.GridHelper(10, 20, 0x3f4656, 0x252a35));
scene.add(new THREE.AxesHelper(1.5));

const loader = new GLTFLoader();
const clock = new THREE.Clock();
let currentUrl = null;
let root = null;
let mixer = null;
let clips = [];
let action = null;
let skeletonHelper = null;
let duration = 1;
let scrubbing = false;

const ui = {
  file: document.querySelector('#file'),
  dropzone: document.querySelector('#dropzone'),
  clips: document.querySelector('#clips'),
  prev: document.querySelector('#prev'),
  play: document.querySelector('#play'),
  pause: document.querySelector('#pause'),
  stop: document.querySelector('#stop'),
  next: document.querySelector('#next'),
  time: document.querySelector('#time'),
  speed: document.querySelector('#speed'),
  skeleton: document.querySelector('#skeleton'),
  wireframe: document.querySelector('#wireframe'),
  info: document.querySelector('#info')
};

function setInfo(text) {
  ui.info.textContent = text;
}

function clearModel() {
  if (root) scene.remove(root);
  if (skeletonHelper) scene.remove(skeletonHelper);
  if (currentUrl) URL.revokeObjectURL(currentUrl);
  root = null;
  mixer = null;
  clips = [];
  action = null;
  skeletonHelper = null;
  ui.clips.innerHTML = '';
}

function frameObject(object) {
  const box = new THREE.Box3().setFromObject(object);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  const maxSize = Math.max(size.x, size.y, size.z) || 1;
  const distance = maxSize / Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2);
  controls.target.copy(center);
  camera.position.copy(center).add(new THREE.Vector3(distance * 0.45, distance * 0.35, distance * 0.65));
  camera.near = Math.max(distance / 1000, 0.01);
  camera.far = distance * 10;
  camera.updateProjectionMatrix();
  controls.update();
}

function selectClip(index) {
  if (!mixer || !clips.length) return;
  if (action) action.stop();
  const clip = clips[index];
  action = mixer.clipAction(clip);
  action.reset().play();
  duration = Math.max(clip.duration, 0.001);
  ui.time.value = 0;
  ui.clips.value = String(index);
  setInfo(\`Loaded \${root.name || 'model'}\\nClip: \${clip.name}\\nDuration: \${duration.toFixed(2)}s\\nAnimations: \${clips.length}\`);
}

function loadFile(file) {
  clearModel();
  currentUrl = URL.createObjectURL(file);
  setInfo(\`Loading \${file.name}...\`);
  loader.load(currentUrl, (gltf) => {
    root = gltf.scene;
    root.name = file.name;
    scene.add(root);
    clips = gltf.animations || [];
    mixer = clips.length ? new THREE.AnimationMixer(root) : null;
    skeletonHelper = new THREE.SkeletonHelper(root);
    skeletonHelper.visible = ui.skeleton.checked;
    scene.add(skeletonHelper);
    ui.clips.innerHTML = clips.map((clip, index) => \`<option value="\${index}">\${clip.name || \`Clip \${index + 1}\`}</option>\`).join('');
    root.traverse((child) => {
      if (child.isMesh) child.frustumCulled = false;
    });
    frameObject(root);
    if (clips.length) selectClip(0);
    else setInfo(\`Loaded \${file.name}\\nNo animations found.\`);
  }, undefined, (error) => {
    setInfo(\`Failed to load \${file.name}: \${error.message}\`);
  });
}

ui.file.addEventListener('change', () => {
  const file = ui.file.files?.[0];
  if (file) loadFile(file);
});

for (const event of ['dragenter', 'dragover']) {
  ui.dropzone.addEventListener(event, (e) => {
    e.preventDefault();
    ui.dropzone.classList.add('drag');
  });
}
for (const event of ['dragleave', 'drop']) {
  ui.dropzone.addEventListener(event, (e) => {
    e.preventDefault();
    ui.dropzone.classList.remove('drag');
  });
}
ui.dropzone.addEventListener('drop', (e) => {
  const file = e.dataTransfer?.files?.[0];
  if (file) loadFile(file);
});

ui.clips.addEventListener('change', () => selectClip(Number(ui.clips.value)));
ui.play.addEventListener('click', () => { if (action) action.paused = false; });
ui.pause.addEventListener('click', () => { if (action) action.paused = true; });
ui.stop.addEventListener('click', () => { if (action) action.stop().reset().play(); });
ui.prev.addEventListener('click', () => selectClip((Number(ui.clips.value || 0) - 1 + clips.length) % clips.length));
ui.next.addEventListener('click', () => selectClip((Number(ui.clips.value || 0) + 1) % clips.length));
ui.speed.addEventListener('input', () => { if (mixer) mixer.timeScale = Number(ui.speed.value); });
ui.skeleton.addEventListener('change', () => { if (skeletonHelper) skeletonHelper.visible = ui.skeleton.checked; });
ui.wireframe.addEventListener('change', () => {
  if (!root) return;
  root.traverse((child) => {
    if (child.isMesh && child.material) {
      const materials = Array.isArray(child.material) ? child.material : [child.material];
      for (const material of materials) material.wireframe = ui.wireframe.checked;
    }
  });
});
ui.time.addEventListener('pointerdown', () => { scrubbing = true; });
ui.time.addEventListener('pointerup', () => { scrubbing = false; });
ui.time.addEventListener('input', () => {
  if (!mixer || !action) return;
  mixer.setTime(Number(ui.time.value) * duration);
});

function resize() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  if (mixer && !scrubbing) {
    mixer.update(delta);
    ui.time.value = String((mixer.time % duration) / duration);
  }
  controls.update();
  renderer.render(scene, camera);
}
resize();
animate();
`, "utf8");

console.log(`Created Three.js character previewer at ${outDir}`);
console.log("Run: npm install");
console.log("Then: npm run dev");
