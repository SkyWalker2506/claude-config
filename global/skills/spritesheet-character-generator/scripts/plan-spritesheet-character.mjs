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
    if (!next || next.startsWith("--")) {
      args.options[key] = true;
    } else {
      args.options[key] = next;
      i += 1;
    }
  }
  return args;
}

function slugify(value) {
  return String(value || "character")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "") || "character";
}

function chooseRoute({ style, motion, view, character }) {
  const haystack = `${style} ${motion} ${view} ${character}`.toLowerCase();
  if (/(pixel|32x32|4walk|four.?direction|rpg|tiny|chibi|walk)/.test(haystack)) {
    return {
      id: "svntax-dev/pixel_spritesheet_4walk_small_lora_v1",
      mode: "text-to-image or edit",
      license: "apache-2.0",
      grid: "4x4",
      size: "512x512 raw, downscale to 128x128 for 32x32 frames",
      notes: ["use FLUX.2 Klein base 4B, not distilled", "3000-step LoRA for humanoids", "2750-step LoRA can be more creative for non-humanoids with reference"]
    };
  }
  if (/(2x2|multi.?view|turnaround|isometric|object|vehicle|reference)/.test(haystack)) {
    return {
      id: "fal/flux-2-klein-4b-spritesheet-lora",
      mode: "image-to-image",
      license: "apache-2.0",
      grid: "2x2",
      size: "model default",
      notes: ["prompt usually `2x2 sprite sheet`", "recommended LoRA scale 1.1", "red background cleanup required"]
    };
  }
  if (/(lpc|top.?down|humanoid|sprite sheet|action|rogue|knight|mage|archer)/.test(haystack)) {
    return {
      id: "Mystic07/flux-lora-spritesheet",
      mode: "text-to-image or ComfyUI",
      license: "flux-1-dev-non-commercial-license inherited from base",
      grid: "route-dependent",
      size: "768x768 or 1024x1024",
      notes: ["prototype-only until commercial rights are verified", "use trigger `gmsspritesheet`", "30 steps and guidance 4.0 are good starting points"]
    };
  }
  return {
    id: "imagegen",
    mode: "concept/reference/fallback",
    license: "record generated asset terms for project",
    grid: "custom",
    size: "match project",
    notes: ["use to create master character and master pose first", "external LoRA route can be selected after style is clarified"]
  };
}

const { target, options } = parseArgs(process.argv.slice(2));
if (!target) {
  console.error("Usage: node plan-spritesheet-character.mjs <target-project> --name hero --character \"clockwork knight\" --style \"pixel art\" --motion 4walk");
  process.exit(1);
}

const projectRoot = path.resolve(target);
const name = options.name || "character";
const slug = slugify(name);
const character = options.character || name;
const style = options.style || "game-ready 2D sprite";
const motion = options.motion || "idle";
const view = options.view || "project camera";
const artDirection = options["art-direction"] || "match the target game's existing visual language";
const cols = Number(options.cols || (String(motion).toLowerCase().includes("4walk") ? 4 : 0)) || null;
const rows = Number(options.rows || (String(motion).toLowerCase().includes("4walk") ? 4 : 0)) || null;
const frame = options.frame || "match project";
const outDir = path.resolve(options.out || path.join(projectRoot, "buildable", "spritesheets", slug));
const publicDir = path.join(projectRoot, "public", "assets", "sprites", slug);
const route = chooseRoute({ style, motion, view, character });

fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(path.join(outDir, "preview"), { recursive: true });
fs.mkdirSync(path.join(publicDir, "references"), { recursive: true });

const masterCharacterPrompt = [
  `Full-body master character reference for a 2D game sprite: ${character}.`,
  `Art style: ${style}.`,
  `Art direction: ${artDirection}.`,
  `Camera/view target: ${view}.`,
  "Clear readable silhouette, consistent costume, limited key palette, centered body, no cropping, plain removable background."
].join(" ");

const masterPosePrompt = [
  `Master pose/turnaround reference for ${character}.`,
  "Show neutral stance and readable front, side, and back cues where appropriate.",
  `Keep ${style}, same colors, same outfit, same proportions, plain removable background.`
].join(" ");

const gridDescription = route.grid === "4x4"
  ? "The spritesheet is a 4 by 4 grid: row 1 has 3 walking frames facing down plus 1 arms-raised frame; row 2 has 3 walking frames facing left plus 1 jumping-left frame; row 3 has 3 walking frames facing right plus 1 jumping-right frame; row 4 has 3 walking frames facing up/back plus 1 lying-on-floor frame."
  : route.grid === "2x2"
    ? "The spritesheet is a 2 by 2 grid: top-left isometric front-right, top-right isometric front-left, bottom-left side profile facing left, bottom-right top-down facing up."
    : `The spritesheet layout should match ${cols && rows ? `${cols} by ${rows}` : "the requested"} grid and motion state ${motion}.`;

const trigger = route.id === "Mystic07/flux-lora-spritesheet" ? "gmsspritesheet, " : "";
const spritesheetPrompt = [
  `${trigger}${gridDescription}`,
  `Character: ${character}.`,
  `Motion/state: ${motion}.`,
  `View: ${view}.`,
  `Style: ${style}.`,
  "Consistent proportions, same outfit in every frame, centered in each cell, clean frame boundaries, game-ready sprite sheet, plain removable background."
].join(" ");

const negativePrompt = "extra limbs, duplicate character in one frame, cropped head, cropped weapon, inconsistent costume, perspective mismatch, blurry pixels, uneven frame size, text labels, watermark, noisy background, overlapping frames";

const promptPack = {
  name,
  slug,
  targetProject: projectRoot,
  recommendedRoute: route,
  requested: { character, style, motion, view, artDirection, cols, rows, frame },
  prompts: {
    masterCharacterPrompt,
    masterPosePrompt,
    spritesheetPrompt,
    negativePrompt,
    imagegenFallbackPrompt: `${masterCharacterPrompt} Also include a clean sprite-ready pose study for ${motion}.`
  },
  output: {
    workDir: outDir,
    finalAssetDir: publicDir,
    previewDir: path.join(outDir, "preview")
  }
};

const brief = `# ${name} Spritesheet Brief

## Character

${character}

## Art Direction

${artDirection}

## Style And Motion

- Style: ${style}
- View: ${view}
- Motion/state: ${motion}
- Frame size: ${frame}
- Grid: ${cols && rows ? `${cols}x${rows}` : route.grid}

## Recommended Route

- Model: ${route.id}
- Mode: ${route.mode}
- License: ${route.license}
- Size: ${route.size}
- Notes: ${route.notes.join("; ")}

## Master Character Prompt

${masterCharacterPrompt}

## Master Pose Prompt

${masterPosePrompt}

## Spritesheet Prompt

${spritesheetPrompt}

## Negative Prompt

${negativePrompt}
`;

const log = `# Generation Log

- Character: ${name}
- Created: ${new Date().toISOString()}
- Route: ${route.id}
- License: ${route.license}
- Source references: add imagegen/HF/ComfyUI/fal output paths here.
- Cleanup notes: add background removal, crop, alpha, palette, and downscale steps here.
- Shipping status: prototype until license and QA checklist pass.
`;

fs.writeFileSync(path.join(outDir, "character-brief.md"), brief, "utf8");
fs.writeFileSync(path.join(outDir, "prompt-pack.json"), `${JSON.stringify(promptPack, null, 2)}\n`, "utf8");
fs.writeFileSync(path.join(outDir, "generation-log.md"), log, "utf8");

console.log(`Created spritesheet plan at ${outDir}`);
console.log(`Recommended route: ${route.id}`);
console.log(`Final assets should be staged at ${publicDir}`);
