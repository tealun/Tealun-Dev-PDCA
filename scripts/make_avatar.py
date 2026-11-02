"""Draw the dev-pdca marketplace avatar (512x512 PNG).

A closed loop that resolves into a check mark: iterate, then prove it.
Usage: python3 scripts/make_avatar.py assets/dev-pdca-avatar.png   (needs Pillow)
"""
import math
import sys

from PIL import Image, ImageDraw

S = 2048  # draw large, downsample for smooth edges
TOP, BOTTOM = (79, 70, 229), (14, 165, 233)  # indigo -> sky


def gradient() -> Image.Image:
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S - 2)
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM))
    return img


def round_arc(d, c, r, w, a0, a1, fill):
    d.arc([c - r, c - r, c + r, c + r], a0, a1, fill=fill, width=w)
    rm = r - w / 2
    for a in (a0, a1):
        x, y = c + rm * math.cos(math.radians(a)), c + rm * math.sin(math.radians(a))
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)


def main(out: str) -> None:
    base = gradient().convert("RGBA")
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c, r, w = S / 2, 640, 112
    # loop: open at the upper right, where the check mark leaves it
    round_arc(d, c, r, w, -18, 278, (255, 255, 255, 115))
    # check mark, rising out through the gap in the loop
    pts = [(c - 330, c + 60), (c - 100, c + 290), (c + 470, c - 540)]
    d.line(pts, fill=(255, 255, 255, 255), width=w + 16, joint="curve")
    for x, y in (pts[0], pts[-1]):
        h = (w + 16) / 2
        d.ellipse([x - h, y - h, x + h, y + h], fill=(255, 255, 255, 255))
    img = Image.alpha_composite(base, layer).convert("RGB").resize((512, 512), Image.LANCZOS)
    img.save(out, "PNG", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1])
