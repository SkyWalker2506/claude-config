#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = { target: null, options: {} };
  const rest = [...argv];
  args.target = rest.shift();
  for (let i = 0; i < rest.length; i += 1) {
    const token = rest[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = rest[i + 1];
    if (!next || next.startsWith("--")) args.options[key] = true;
    else {
      args.options[key] = next;
      i += 1;
    }
  }
  return args;
}

function slugify(value) {
  return String(value || "character").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "character";
}

const { target, options } = parseArgs(process.argv.slice(2));
if (!target) {
  console.error("Usage: node plan-3d-character.mjs <target-project> --name hero --character \"stylized space mechanic\" --style \"low-poly cozy sci-fi\" --poly-budget 20000 --animations \"idle,walk,run\"");
  process.exit(1);
}

const projectRoot = path.resolve(target);
const name = options.name || "character";
const slug = slugify(name);
const character = options.character || name;
const style = options.style || "game-ready stylized 3D";
const pose = options.pose || "clean A-pose, full body, separated limbs";
const texture = options.texture || "PBR base color, roughness, normal where useful";
const polyBudget = options["poly-budget"] || "10000-35000 triangles";
const animations = String(options.animations || "idle,walk,run").split(",").map((item) => item.trim()).filter(Boolean);
const outDir = path.resolve(options.out || path.join(projectRoot, "buildable", "characters", slug));
const assetDir = path.join(projectRoot, "public", "assets", "characters", slug);

for (const dir of [
  outDir,
  path.join(outDir, "references"),
  path.join(outDir, "trellis"),
  path.join(outDir, "blender"),
  path.join(outDir, "mixamo"),
  path.join(outDir, "previewer"),
  path.join(assetDir, "animations"),
  path.join(assetDir, "textures")
]) {
  fs.mkdirSync(dir, { recursive: true });
}

const masterCharacterPrompt = [
  `Full-body master character concept for a Three.js game asset: ${character}.`,
  `Style: ${style}.`,
  "Readable silhouette, strong front/side design cues, clear material zones, no text, no watermark, plain removable background."
].join(" ");

const masterPosePrompt = [
  `Rigging-ready master pose reference for ${character}.`,
  `Pose: ${pose}.`,
  `Texture/material direction: ${texture}.`,
  "Full body visible, hands and feet unobscured, symmetric enough for rigging, neutral expression, clean background."
].join(" ");

const trellisPrompt = [
  `Use the master pose image as single-image input for TRELLIS.2 image-to-3D.`,
  `Target style: ${style}.`,
  `Target mesh budget after cleanup: ${polyBudget}.`,
  `Texture target: ${texture}.`,
  "Preserve character identity, avoid floaters, keep limbs separate, export textured mesh for Blender cleanup."
].join(" ");

const promptPack = {
  name,
  slug,
  targetProject: projectRoot,
  requested: { character, style, pose, texture, polyBudget, animations },
  prompts: { masterCharacterPrompt, masterPosePrompt, trellisPrompt },
  output: {
    workDir: outDir,
    finalAssetDir: assetDir,
    previewerDir: path.join(projectRoot, "buildable", "character-previewer")
  }
};

const plan = `# ${name} 3D Character Pipeline

## Character

${character}

## Style

${style}

## Targets

- Pose: ${pose}
- Poly budget: ${polyBudget}
- Textures: ${texture}
- Animations: ${animations.join(", ")}

## Steps

1. Generate and save imagegen master character/reference images under \`references/\`.
2. Generate a rigging-friendly master pose image.
3. Use TRELLIS.2 if available to create a textured mesh, or document missing setup.
4. Clean and optimize in Blender through MCP or Blender CLI/manual workflow.
5. Rig with Make-It-Animatable or Mixamo where available.
6. Import/bake requested animations and export \`${slug}.glb\`.
7. Test in the local Three.js previewer with skeleton and animation controls.

## Prompts

### Master Character

${masterCharacterPrompt}

### Master Pose

${masterPosePrompt}

### TRELLIS.2 Direction

${trellisPrompt}
`;

const log = `# Generation Log

- Created: ${new Date().toISOString()}
- Character: ${name}
- Source imagegen references: add saved paths here.
- TRELLIS.2 source/runtime: add repo/service/version here.
- Blender cleanup notes: add scale, orientation, decimation, material, and export notes here.
- Rigging route: Make-It-Animatable / Mixamo / Blender manual.
- Animation clips: ${animations.join(", ")}
- Shipping status: prototype until mesh, rig, texture, license, and preview QA pass.
`;

fs.writeFileSync(path.join(outDir, "character-plan.md"), plan, "utf8");
fs.writeFileSync(path.join(outDir, "prompt-pack.json"), `${JSON.stringify(promptPack, null, 2)}\n`, "utf8");
fs.writeFileSync(path.join(outDir, "generation-log.md"), log, "utf8");

console.log(`Created 3D character plan at ${outDir}`);
console.log(`Final assets should be staged at ${assetDir}`);
