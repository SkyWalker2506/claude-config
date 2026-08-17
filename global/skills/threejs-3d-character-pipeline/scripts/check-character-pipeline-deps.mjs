#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

function run(cmd, args = []) {
  const executable = process.platform === "win32" && ["npm", "npx"].includes(cmd) ? `${cmd}.cmd` : cmd;
  const result = spawnSync(executable, args, { encoding: "utf8" });
  return {
    ok: result.status === 0,
    text: `${result.stdout || ""}${result.stderr || ""}`.trim()
  };
}

function exists(label, value) {
  const ok = Boolean(value && fs.existsSync(value));
  console.log(`${ok ? "OK" : "MISSING"} ${label}${value ? ` - ${value}` : ""}`);
  return ok;
}

function command(label, cmd, args = ["--version"]) {
  const result = run(cmd, args);
  const firstLine = result.text.split(/\r?\n/).find(Boolean) || "";
  console.log(`${result.ok ? "OK" : "MISSING"} ${label}${firstLine ? ` - ${firstLine}` : ""}`);
  return result.ok;
}

const nodeOk = command("node", "node");
const npmOk = command("npm", "npm", ["--version"]);
const blenderOk = command("blender", "blender", ["--version"]);
const pythonOk = command("python", "python", ["--version"]);

const trellisPath = process.env.TRELLIS2_PATH || "";
exists("TRELLIS2_PATH", trellisPath);
if (trellisPath) {
  exists("TRELLIS.2 repo", path.join(trellisPath, "README.md"));
}

const miaPath = process.env.MAKE_IT_ANIMATABLE_PATH || "";
exists("MAKE_IT_ANIMATABLE_PATH", miaPath);
if (miaPath) {
  exists("Make-It-Animatable app.py", path.join(miaPath, "app.py"));
}

const gltfTransform = run("npx", ["--no-install", "@gltf-transform/cli", "--version"]);
console.log(`${gltfTransform.ok ? "OK" : "MISSING"} glTF-Transform CLI${gltfTransform.text ? ` - ${gltfTransform.text.split(/\r?\n/)[0]}` : ""}`);

console.log("\nInstall/action guidance:");
if (!nodeOk || !npmOk) {
  console.log("- Install Node.js LTS to scaffold and run the Three.js previewer.");
}
if (!blenderOk) {
  console.log("- Install Blender and ensure `blender` is on PATH, or use Blender MCP with Blender open and its addon enabled.");
}
if (!pythonOk) {
  console.log("- Install Python/Conda for TRELLIS.2 and Make-It-Animatable workflows.");
}
if (!trellisPath) {
  console.log("- TRELLIS.2 route: clone/setup microsoft/TRELLIS.2, set TRELLIS2_PATH, and verify Linux + CUDA + 24GB+ NVIDIA VRAM or use a trusted hosted run.");
}
if (!miaPath) {
  console.log("- Make-It-Animatable route: clone/setup jasongzy/Make-It-Animatable, download required model/data weights, and set MAKE_IT_ANIMATABLE_PATH.");
}
console.log("- Mixamo route needs Adobe login and manual upload/download unless the user provides already-downloaded FBX animation files.");
console.log("- If glTF-Transform is unavailable, the previewer still works; optimization/compression commands should be skipped or installed explicitly.");
