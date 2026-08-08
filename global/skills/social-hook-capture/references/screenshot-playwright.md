# Playwright Media Notes

## Capture Principles

- Capture the real app, game, or page state.
- Prefer desktop size `1280x720` for general social and Steam-adjacent posts.
- Use `1080x1080` or `1200x675` only when the platform benefits from that crop.
- For Three.js, wait for a nonblank canvas before taking the screenshot.
- Hide debug panels, cursor clutter, devtools, and temporary overlays unless the post is about them.

## GIF Capture

Use GIF for motion hooks: a satisfying interaction, reveal, physics moment, animation loop, combat beat, UI transition, before/after change, or funny emergent result. Keep it short, usually 2-5 seconds.

```bash
node <skill>/scripts/capture-hook-gif.mjs <project> --url http://localhost:5173 --selector canvas --duration 3500 --fps 12
```

The GIF script captures frames with Playwright and uses `ffmpeg` to encode `posts/assets/post_N.gif`. If `ffmpeg` is unavailable, it still leaves the captured frames under `posts/assets/post_N_frames_<timestamp>/`.

## Dependency

Before capture, run:

```bash
node <skill>/scripts/check-media-deps.mjs <project>
```

The screenshot and GIF scripts expect Playwright to be available either in the tool environment or in the target project. If it is missing, the agent must tell the user to install it:

```bash
npm install -D playwright
```

GIF encoding expects `ffmpeg` on `PATH`. If it is missing and GIF output is requested, the agent must tell the user to install ffmpeg and ensure it is available on `PATH`. The GIF script can still save PNG frames, but it cannot create the final `.gif` without ffmpeg.

## Local App

If the app needs a dev server, start it separately and pass the URL:

```bash
node <skill>/scripts/capture-hook-screenshot.mjs <project> --url http://localhost:5173 --selector canvas
```

If the page is static HTML, pass a file path:

```bash
node <skill>/scripts/capture-hook-screenshot.mjs <project> --file index.html
```

## Selector

Use `--selector canvas` for Three.js screenshots when the canvas is the product. Use a wider page screenshot when UI chrome, menus, or copy matter.

## QA

After capture:

- Verify the image/GIF exists.
- Open or inspect the media if visual quality matters.
- Retake if the canvas is blank, loading, cropped poorly, slow to reveal the hook, or visually confusing.
