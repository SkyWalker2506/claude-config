#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const options = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      options[key] = true;
    } else {
      options[key] = next;
      i += 1;
    }
  }
  return options;
}

const options = parseArgs(process.argv.slice(2));
if (!options.image) {
  console.error("Usage: node create-spritesheet-preview.mjs --image path/to/sheet.png --cols 4 --rows 4 --frame-width 32 --frame-height 32 --out buildable/spritesheets/hero/preview");
  process.exit(1);
}

const imagePath = path.resolve(options.image);
const cols = Number(options.cols || 4);
const rows = Number(options.rows || 4);
const frameWidth = Number(options["frame-width"] || options.frame || 32);
const frameHeight = Number(options["frame-height"] || options.frame || 32);
const outDir = path.resolve(options.out || path.join(process.cwd(), "buildable", "spritesheets", "preview"));
const outFile = path.join(outDir, "spritesheet-preview.html");
const imageExists = fs.existsSync(imagePath);

fs.mkdirSync(outDir, { recursive: true });

const cells = [];
for (let row = 0; row < rows; row += 1) {
  for (let col = 0; col < cols; col += 1) {
    const index = row * cols + col;
    cells.push(`<figure><div class="frame" style="background-position:${-col * frameWidth}px ${-row * frameHeight}px"></div><figcaption>${index}</figcaption></figure>`);
  }
}

const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Spritesheet Preview</title>
  <style>
    :root { color-scheme: dark; font-family: system-ui, sans-serif; background: #15171d; color: #f5f7fb; }
    body { margin: 24px; }
    main { max-width: 1100px; margin: 0 auto; }
    .meta { color: #b7bdca; line-height: 1.5; }
    .sheet { max-width: 100%; image-rendering: pixelated; background: #2a2e39; }
    .grid { display: grid; grid-template-columns: repeat(${cols}, ${Math.max(frameWidth * 3, 64)}px); gap: 12px; margin-top: 24px; }
    figure { margin: 0; }
    .frame { width: ${frameWidth}px; height: ${frameHeight}px; transform-origin: top left; transform: scale(3); image-rendering: pixelated; background-image: url("${imagePath.replace(/\\/g, "/")}"); background-repeat: no-repeat; background-size: ${cols * frameWidth}px ${rows * frameHeight}px; background-color: #2a2e39; }
    figcaption { margin-top: ${frameHeight * 3 + 6}px; color: #9ba3b4; font-size: 12px; }
    .warning { padding: 10px 12px; border: 1px solid #d7a33a; color: #ffd27a; background: #302614; }
  </style>
</head>
<body>
  <main>
    <h1>Spritesheet Preview</h1>
    ${imageExists ? "" : `<p class="warning">Image file was not found when this preview was created. Place the sheet at the path below or regenerate this preview.</p>`}
    <p class="meta">Image: ${imagePath}<br>Grid: ${cols} x ${rows}<br>Frame: ${frameWidth} x ${frameHeight}</p>
    <img class="sheet" src="${imagePath.replace(/\\/g, "/")}" alt="Full spritesheet">
    <section class="grid">${cells.join("")}</section>
  </main>
</body>
</html>
`;

fs.writeFileSync(outFile, html, "utf8");
console.log(`Created preview at ${outFile}`);
