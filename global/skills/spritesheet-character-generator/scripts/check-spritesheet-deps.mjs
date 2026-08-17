#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

function run(cmd, args) {
  const result = spawnSync(cmd, args, { encoding: "utf8" });
  return {
    ok: result.status === 0,
    stdout: (result.stdout || "").trim(),
    stderr: (result.stderr || "").trim()
  };
}

function printStatus(label, ok, detail = "") {
  const mark = ok ? "OK" : "MISSING";
  console.log(`${mark} ${label}${detail ? ` - ${detail}` : ""}`);
}

const python = run("python", ["--version"]);
printStatus("python", python.ok, python.stdout || python.stderr);

const packages = ["diffusers", "transformers", "accelerate", "safetensors", "PIL", "torch"];
const pyCheck = run("python", [
  "-c",
  `import importlib.util; mods=${JSON.stringify(packages)}; print("\\n".join(f"{m}:{bool(importlib.util.find_spec(m))}" for m in mods))`
]);

let missingPy = packages;
if (pyCheck.ok) {
  const rows = pyCheck.stdout.split(/\r?\n/).filter(Boolean);
  missingPy = rows.filter((row) => row.endsWith(":False")).map((row) => row.split(":")[0]);
  for (const row of rows) {
    const [name, ok] = row.split(":");
    printStatus(`python package ${name}`, ok === "True");
  }
} else {
  console.log("MISSING python package check - Python could not import-check packages.");
}

const falClient = run("python", ["-c", "import importlib.util; print(bool(importlib.util.find_spec('fal_client')))"]);
printStatus("python package fal_client", falClient.ok && falClient.stdout === "True");
printStatus("FAL_KEY", Boolean(process.env.FAL_KEY), process.env.FAL_KEY ? "set" : "not set");

const comfyPath = process.env.COMFYUI_PATH || "";
const comfyExists = Boolean(comfyPath && fs.existsSync(comfyPath));
printStatus("COMFYUI_PATH", comfyExists, comfyPath || "not set");
if (comfyExists) {
  const loraDir = path.join(comfyPath, "models", "loras");
  printStatus("ComfyUI models/loras", fs.existsSync(loraDir), loraDir);
}

console.log("\nInstall guidance:");
if (!python.ok || missingPy.length) {
  console.log("- Local Diffusers: install Python, then `pip install -U diffusers transformers accelerate safetensors pillow huggingface_hub`.");
  console.log("- Install PyTorch from the official PyTorch selector for your CUDA/MPS/CPU environment.");
  console.log("- Accept/verify Hugging Face model licenses and authentication before downloading gated base models.");
}
if (!(falClient.ok && falClient.stdout === "True") || !process.env.FAL_KEY) {
  console.log("- fal.ai route: `pip install fal-client` and set `FAL_KEY` before using the fal 2x2 image-to-image endpoint.");
}
if (!comfyExists) {
  console.log("- ComfyUI route: install ComfyUI, set COMFYUI_PATH, and place LoRA `.safetensors` files in `ComfyUI/models/loras/`.");
}

console.log("\nThis script only reports readiness. It does not install multi-GB models automatically.");
