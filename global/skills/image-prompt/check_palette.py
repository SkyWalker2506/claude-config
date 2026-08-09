#!/usr/bin/env python3
"""Palette check for generated illustration batches.

Catches the failure the eye forgives: a batch that looks fine one image at a
time but is actually one hue with a filter over it. Reports, per image, the
hue spread, whether shadows and lights differ in temperature, and whether the
sky is genuinely blue. Anything flagged here reads as "AI output".

    python3 check_palette.py ~/Downloads/*.png
    python3 check_palette.py ~/Downloads/*.png --grade --out graded/
"""

import argparse
import colorsys
import math
from pathlib import Path

import numpy as np
from PIL import Image

LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)
COOL = np.array([-0.055, 0.005, 0.075], np.float32)
WARM = np.array([0.045, 0.012, -0.030], np.float32)

GOOD_SPREAD = 25.0     # degrees of hue variation inside one image
GOOD_TEMP_GAP = 25.0   # degrees between shadow hue and light hue
GOOD_RANGE = 55.0      # 2nd..98th percentile value range, percent


def _circular_hue(hues, weights):
    """Mean hue and spread, weighted by saturation — grey pixels carry no hue."""
    total = weights.sum()
    if total == 0:
        return 0.0, 0.0
    x = float((np.cos(hues * 2 * np.pi) * weights).sum())
    y = float((np.sin(hues * 2 * np.pi) * weights).sum())
    mean = math.degrees(math.atan2(y, x)) % 360
    r = math.hypot(x, y) / total
    spread = math.degrees(math.sqrt(max(0.0, -2 * math.log(max(r, 1e-9)))))
    return mean, spread


def measure(image):
    small = image.convert("RGB").resize((150, 200))
    rgb = np.asarray(small, np.float32) / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in rgb.reshape(-1, 3)], np.float32)
    h, s, v = hsv[:, 0], hsv[:, 1], hsv[:, 2]

    mean, spread = _circular_hue(h, s)
    order = np.argsort(v)
    cut = max(1, len(order) // 7)
    shadow, _ = _circular_hue(h[order[:cut]], s[order[:cut]])
    light, _ = _circular_hue(h[order[-cut:]], s[order[-cut:]])

    gap = abs(shadow - light)
    gap = min(gap, 360 - gap)

    top = rgb[: rgb.shape[0] // 3]
    sky = float((top[..., 2] - top[..., 0]).mean())

    return dict(
        hue=mean, spread=spread, shadow=shadow, light=light, temp_gap=gap,
        sat=float(s.mean() * 100), sky=sky,
        rng=float((np.percentile(v, 98) - np.percentile(v, 2)) * 100),
    )


def grade(image, cast_strength=0.55, split=0.75, sat=1.22, vibrance=0.55):
    """Split-tone rescue: strip the global cast, put cool light in the shadows."""
    a = np.asarray(image.convert("RGB"), np.float32) / 255.0
    lum = (a @ LUMA)[..., None]

    mid = 1.0 - np.abs(lum - 0.5) * 2.0
    a = a - (a.mean(axis=(0, 1)) - a.mean()) * mid * cast_strength

    a = a + np.clip(1 - lum, 0, 1) ** 3.4 * COOL * split
    a = a + np.clip(lum, 0, 1) ** 1.8 * WARM * split

    a = np.clip(a, 0, 1)
    a = a * a * (3 - 2 * a) * 0.35 + a * 0.65

    grey = (a @ LUMA)[..., None]
    chroma = np.abs(a - grey).max(axis=2, keepdims=True)
    boost = 1.0 + vibrance * (1.0 - np.clip(chroma * 3.2, 0, 1))
    a = grey + (a - grey) * boost * sat

    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--grade", action="store_true", help="also write a split-toned rescue")
    ap.add_argument("--out", default="graded")
    args = ap.parse_args()

    print(f"{'file':<26}{'hue°':>6}{'spread':>8}{'shadow/light':>15}{'gap':>6}{'sat%':>7}{'range':>7}{'sky':>8}  flags")
    print("-" * 104)

    rows = []
    for path in args.files:
        image = Image.open(path)
        m = measure(image)
        rows.append(m)

        flags = []
        if m["spread"] < GOOD_SPREAD:
            flags.append("FLAT-HUE")
        if m["temp_gap"] < GOOD_TEMP_GAP:
            flags.append("NO-TEMP-SPLIT")
        if m["rng"] < GOOD_RANGE:
            flags.append("LOW-RANGE")
        if m["sky"] < 0:
            flags.append("WARM-SKY")

        print(f"{Path(path).name[:24]:<26}{m['hue']:6.0f}{m['spread']:8.0f}"
              f"{m['shadow']:8.0f}/{m['light']:<6.0f}{m['temp_gap']:6.0f}"
              f"{m['sat']:7.1f}{m['rng']:7.1f}{m['sky']:+8.3f}  {' '.join(flags) or 'ok'}")

        if args.grade:
            out = Path(args.out)
            out.mkdir(parents=True, exist_ok=True)
            grade(image).save(out / Path(path).with_suffix(".png").name)

    hues = [r["hue"] for r in rows]
    if len(rows) > 1:
        span = max(hues) - min(hues)
        span = min(span, 360 - span)
        print("-" * 104)
        print(f"hue span across the batch: {span:.0f}°  "
              f"({'DESIGNED — subjects have their own palettes' if span > 60 else 'TOO NARROW — one filter over everything'})")
        print(f"mean hue spread inside an image: {sum(r['spread'] for r in rows)/len(rows):.0f}°")


if __name__ == "__main__":
    main()
