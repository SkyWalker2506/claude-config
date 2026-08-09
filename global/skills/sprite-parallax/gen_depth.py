#!/usr/bin/env python3
"""Height maps for the card paintings, one per card.

The card shader displaces UVs by height, so the height map decides whether the
effect reads as depth or as a smear. The old stand-in was a vertical ramp with a
luminance nudge, which knows nothing about what is actually in the picture: a
tank in the middle of frame got the same height as the road behind it, so the
whole painting slid as one sheet.

Three cues, combined, get close enough on painted art without a depth model:

  detail   near things carry high-frequency texture; distance is smoothed by
           haze and by how the painter treated it. This is the strongest cue
           and does follow the subject's silhouette.
  ramp     card art is composed with the near subject low in frame and sky
           high. A weak prior, but it fixes detail's blind spot: a busy sky.
  tone     aerial perspective lightens distance. Weakest of the three, and
           actively wrong on night scenes, so it gets the smallest share.

Output is 8-bit grayscale WebP, white = near.

    python3 gen_depth.py                 # every sprite under DEPTH_SRC
    python3 gen_depth.py --check <id>    # write a side-by-side preview

    DEPTH_SRC=art/units DEPTH_OUT=art/depth DEPTH_SIZE=256x256 python3 gen_depth.py
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

SRC = Path(os.environ.get("DEPTH_SRC", "public/assets/cards"))
OUT = Path(os.environ.get("DEPTH_OUT", "public/assets/depth"))

# Height maps do not need the resolution of the artwork; the shader blurs the
# field anyway and a small map keeps the whole set a few dozen KB.
SIZE = tuple(int(n) for n in os.environ.get("DEPTH_SIZE", "256x340").split("x"))

# The ramp is the ground the scene stands on; detail is what stands up out of
# it. Adding them flattened the near foreground, because smooth mud in the
# bottom of frame carries no detail and the sum dragged it back to "far".
W_LIFT, W_TONE = 0.62, 0.12

# The horizon the ramp bends around, as a fraction of card height.
HORIZON = 0.42

# Any height field guessed from a painting shears whatever spans a depth
# gradient: the top of a shovel gets a different offset from its handle, so the
# shovel bends. Quantising into planes was tried and is worse — it turns the
# smooth bend into a visible kink at every plane boundary.
#
# So the field stays continuous and deliberately soft, and the displacement it
# drives stays small enough that the residual shear is below notice. Depth on
# these cards comes from the card moving, not from bending the picture.
SMOOTH = 4.5

# Pull the extremes in: it is the far tail of the range that produces the
# largest offsets and therefore the most visible warping.
RANGE = 0.82


def normalise(a):
    lo, hi = np.percentile(a, 2), np.percentile(a, 98)
    if hi - lo < 1e-6:
        return np.zeros_like(a)
    return np.clip((a - lo) / (hi - lo), 0.0, 1.0)


def detail_energy(gray):
    """High-frequency energy, smoothed into regions.

    A plain edge filter gives thin outlines, and displacing by an outline tears
    the image. Blurring the energy afterwards turns those lines into the solid
    mass of the object that produced them, which is what should move together.
    """
    img = Image.fromarray((gray * 255).astype(np.uint8))
    fine = np.asarray(img.filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32)
    coarse = np.asarray(img.filter(ImageFilter.GaussianBlur(6.0)), dtype=np.float32)
    energy = np.abs(fine - coarse)
    spread = Image.fromarray(np.clip(energy * 3.0, 0, 255).astype(np.uint8))
    spread = spread.filter(ImageFilter.GaussianBlur(9.0))
    return normalise(np.asarray(spread, dtype=np.float32) / 255.0)


def compositional_ramp(h, w):
    t = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    # Everything above the horizon is far and roughly equally far; below it,
    # depth falls away quickly toward the viewer.
    ramp = np.where(t < HORIZON, (t / HORIZON) * 0.30, 0.30 + ((t - HORIZON) / (1 - HORIZON)) * 0.70)
    return np.repeat(ramp, w, axis=1)


def height_map(path):
    img = Image.open(path).convert("RGB").resize(SIZE, Image.LANCZOS)
    rgb = np.asarray(img, dtype=np.float32) / 255.0
    gray = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    h, w = gray.shape

    ramp = compositional_ramp(h, w)
    detail = detail_energy(gray)

    # Take whichever cue says "nearer". The ground keeps the height the
    # composition gives it, and a detailed subject lifts above that ground
    # instead of being averaged into it.
    height = np.maximum(ramp, W_LIFT * detail + ramp * (1.0 - W_LIFT) * 0.5)
    height = normalise(height + W_TONE * (1.0 - normalise(gray)))

    height = 0.5 + (height - 0.5) * RANGE

    out = Image.fromarray((height * 255).astype(np.uint8), mode="L")
    return out.filter(ImageFilter.GaussianBlur(SMOOTH))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", help="write a source|height preview for one card id")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    sources = sorted(SRC.glob("*.webp"))
    if not sources:
        sys.exit(f"no paintings under {SRC}")

    if args.check:
        src = SRC / f"{args.check}.webp"
        if not src.exists():
            sys.exit(f"no such card: {args.check}")
        left = Image.open(src).convert("RGB").resize(SIZE, Image.LANCZOS)
        right = height_map(src).convert("RGB")
        sheet = Image.new("RGB", (SIZE[0] * 2, SIZE[1]))
        sheet.paste(left, (0, 0))
        sheet.paste(right, (SIZE[0], 0))
        out = Path(os.environ.get("DEPTH_PREVIEW", ".")) / f"depth-{args.check}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(out)
        print(out)
        return

    total = 0
    for src in sources:
        dst = OUT / f"{src.stem}.webp"
        height_map(src).save(dst, "WEBP", quality=88, method=6)
        total += dst.stat().st_size
    print(f"{len(sources)} height maps -> {OUT}  ({total / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
