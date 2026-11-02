"""Draw the dev-pdca marketplace avatar (512x512 PNG).

Background: five colours, one per sub-skill, swirled into each other like a
rotating iridescent gradient. Foreground: a </> code mark with PDCA centred
beneath it.
Usage: python3 scripts/make_avatar.py assets/dev-pdca-avatar.png   (needs numpy, Pillow, Inter Display)
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 1536  # draw large, downsample for smooth edges
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
# planner, tasker, auditor, bugfixer, evolver
COLOURS = np.array([
    (59, 130, 246),   # blue
    (16, 185, 129),   # green
    (250, 204, 21),   # yellow
    (249, 115, 22),   # orange
    (168, 85, 247),   # violet
], dtype=float)


def swirl_background() -> Image.Image:
    y, x = np.mgrid[0:S, 0:S].astype(float)
    cx = cy = (S - 1) / 2
    dx, dy = (x - cx) / S, (y - cy) / S
    r = np.hypot(dx, dy)
    theta = np.arctan2(dy, dx)
    # twist: the angle shifts with distance from the centre, so the colours spiral
    t = (theta / (2 * np.pi) + 0.55 * r + 0.08) % 1.0
    pos = t * len(COLOURS)
    i0 = np.floor(pos).astype(int) % len(COLOURS)
    i1 = (i0 + 1) % len(COLOURS)
    f = pos - np.floor(pos)
    f = f * f * (3 - 2 * f)  # smoothstep, softer blends between colours
    rgb = COLOURS[i0] * (1 - f)[..., None] + COLOURS[i1] * f[..., None]
    # soft light centre for the mark to sit on, slight darkening at the edge
    glow = np.clip(1 - r / 0.42, 0, 1) ** 2
    rgb = rgb * (1 - 0.18 * glow[..., None]) + 255 * 0.18 * glow[..., None]
    rgb = rgb * 0.9 + 255 * 0.06  # a touch softer, less neon
    rgb *= (1 - 0.22 * np.clip((r - 0.35) / 0.4, 0, 1))[..., None]
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    return img.filter(ImageFilter.GaussianBlur(S / 22))


def mark_layer() -> Image.Image:
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = S / 2
    w = 58
    white = (255, 255, 255, 255)
    my = c - 125  # vertical centre of the code mark
    h, span = 150, 118  # half height of the chevrons, their depth
    left = [(c - 165, my - h), (c - 165 - span, my), (c - 165, my + h)]
    right = [(c + 165, my - h), (c + 165 + span, my), (c + 165, my + h)]
    slash = [(c + 62, my - h - 24), (c - 62, my + h + 24)]
    for pts in (left, right, slash):
        d.line(pts, fill=white, width=w, joint="curve")
        for px, py in (pts[0], pts[-1]):
            d.ellipse([px - w / 2, py - w / 2, px + w / 2, py + w / 2], fill=white)
    font = ImageFont.truetype(FONT, 225)
    text, track = "PDCA", 52
    widths = [d.textlength(ch, font=font) for ch in text]
    x = c - (sum(widths) + track * (len(text) - 1)) / 2
    for ch, cw in zip(text, widths):
        d.text((x, c + 255), ch, font=font, fill=white, anchor="lm")
        x += cw + track
    return layer


def main(out: str) -> None:
    base = swirl_background().convert("RGBA")
    mark = mark_layer()
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    shadow.putalpha(mark.getchannel("A").point(lambda a: a * 0.35))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    shadow = shadow.transform((S, S), Image.AFFINE, (1, 0, 0, 0, 1, -10))
    img = Image.alpha_composite(Image.alpha_composite(base, shadow), mark)
    img.convert("RGB").resize((512, 512), Image.LANCZOS).save(out, "PNG", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1])
