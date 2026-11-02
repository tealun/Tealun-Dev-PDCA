"""Draw the dev-pdca marketplace avatar (512x512 PNG).

A PDCA ring around a code mark. The ring has four quadrants, Plan, Do, Check
and Act; Check is split in two (auditor and bugfixer), so the five arcs are
the five sub-skills.
Usage: python3 scripts/make_avatar.py assets/dev-pdca-avatar.png   (needs Pillow, Inter Display)
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

S = 2048
FONT_DIR = "/usr/share/fonts/opentype/inter/"
BG_A, BG_B = (30, 27, 75), (15, 23, 42)  # deep indigo -> slate
# (start angle, sweep, colour, label); angles clockwise from 3 o'clock
ARCS = [
    (180, 90, (96, 165, 250), "P"),   # Plan    planner
    (270, 90, (52, 211, 153), "D"),   # Do      tasker
    (0, 45, (251, 191, 36), "C"),     # Check   auditor
    (45, 45, (251, 146, 60), None),   # Check   bugfixer
    (90, 90, (167, 139, 250), "A"),   # Act     evolver
]


def background() -> Image.Image:
    img = Image.new("RGB", (S, S))
    px = img.load()
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S - 2)
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(BG_A, BG_B))
    return img


def arc(d, c, r, w, a0, a1, fill):
    d.arc([c - r, c - r, c + r, c + r], a0, a1, fill=fill, width=w)
    rm = r - w / 2
    for a in (a0, a1):
        x, y = c + rm * math.cos(math.radians(a)), c + rm * math.sin(math.radians(a))
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)


def main(out: str) -> None:
    img = background()
    d = ImageDraw.Draw(img)
    c, r, w = S / 2, 700, 80
    label = ImageFont.truetype(FONT_DIR + "InterDisplay-SemiBold.otf", 160)
    mark = ImageFont.truetype(FONT_DIR + "InterDisplay-Bold.otf", 300)
    gap = 9  # degrees between arcs, room for the round caps
    for start, sweep, colour, text in ARCS:
        arc(d, c, r, w, start + gap / 2, start + sweep - gap / 2, colour)
        if text:
            mid = math.radians(start + 45)
            rl = r - w - 160
            d.text((c + rl * math.cos(mid), c + rl * math.sin(mid)), text, font=label, fill=colour, anchor="mm")
    d.text((c, c - 20), "</>", font=mark, fill=(255, 255, 255), anchor="mm")
    img.resize((512, 512), Image.LANCZOS).save(out, "PNG", optimize=True)


if __name__ == "__main__":
    main(sys.argv[1])
