#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a one-page newspaper front page.

All artwork is flat PIL geometry + real rendered text. No AI-generated imagery.
Output: entry.png, 1024x1024, <= 1 MiB.

Stories verified against news reporting on 18 November 2026 (APEC Shenzhen,
Quad Manila, North Korea missile, Iran/Bahrain drones, Dow sell-off,
Cyclone Akvan). Wording hedges where the record is uncertain.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
CARD = (255, 254, 249)
NAVY = (20, 33, 61)
RED = (192, 57, 43)
GREY = (90, 92, 96)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_skyline(d, x, y, w, h, c):
    # three towers of different heights, lit windows, ground line
    towers = [(0.04, 0.55, 0.26), (0.30, 0.30, 0.24), (0.58, 0.42, 0.26),
              (0.82, 0.62, 0.14)]
    for fx, fy, fw in towers:
        tx0, tx1 = x + w * fx, x + w * (fx + fw)
        ty0 = y + h * fy
        d.rectangle([tx0, ty0, tx1, y + h - 6], fill=c)
        for wy in (ty0 + 8, ty0 + 20):
            for wx in (tx0 + 5, tx0 + 14):
                if wx + 4 < tx1:
                    d.rectangle([wx, wy, wx + 4, wy + 4], fill=CREAM)
    d.rectangle([x, y + h - 6, x + w, y + h - 2], fill=c)


def draw_plane(d, x, y, w, h, c):
    # side view, nose to the right: fuselage, tail fin, swept wings
    d.ellipse([x + 4, y + h * 0.34, x + w - 2, y + h * 0.60], fill=c)
    d.polygon([(x + 10, y + h * 0.42), (x + 22, y + 2),
               (x + 34, y + 4), (x + 30, y + h * 0.46)], fill=c)
    d.polygon([(x + w * 0.42, y + h * 0.52), (x + w * 0.62, y + h * 0.52),
               (x + w * 0.42, y + h - 4), (x + w * 0.30, y + h - 4)], fill=c)
    d.polygon([(x + w * 0.16, y + h * 0.44), (x + w * 0.28, y + h * 0.44),
               (x + w * 0.14, y + h * 0.20), (x + w * 0.06, y + h * 0.20)],
              fill=c)
    for i in range(3):
        cx = x + w * (0.52 + i * 0.11)
        d.ellipse([cx, y + h * 0.42, cx + 6, y + h * 0.42 + 6], fill=CREAM)


def draw_missile(d, x, y, w, h, c):
    # missile climbing to the upper right, with a short smoke trail.
    # All geometry is scaled (s = 0.6 of the old 92x46 design) so the
    # drawing stays inside its (w, h) box: the old version used absolute
    # offsets plus a ground line, which escaped the box and struck
    # through the headline's first line below the icon. No ground line.
    s = 0.6
    cx, cy = x + w * 0.55, y + h * 0.45
    ang = math.radians(-55)
    dx, dy = math.cos(ang), math.sin(ang)
    px, py = -dy, dx  # perpendicular
    nose = (cx + dx * 24 * s, cy + dy * 24 * s)
    tail = (cx - dx * 16 * s, cy - dy * 16 * s)
    hw = 7 * s
    body = [(nose[0] + px * hw, nose[1] + py * hw),
            (tail[0] + px * hw, tail[1] + py * hw),
            (tail[0] - px * hw, tail[1] - py * hw),
            (nose[0] - px * hw, nose[1] - py * hw)]
    d.polygon(body, fill=c)
    # fins at the tail
    d.polygon([(tail[0], tail[1]),
               (tail[0] - dx * 10 * s + px * 12 * s,
                tail[1] - dy * 10 * s + py * 12 * s),
               (tail[0] - dx * 2 * s + px * 8 * s,
                tail[1] - dy * 2 * s + py * 8 * s)], fill=c)
    d.polygon([(tail[0], tail[1]),
               (tail[0] - dx * 10 * s - px * 12 * s,
                tail[1] - dy * 10 * s - py * 12 * s),
               (tail[0] - dx * 2 * s - px * 8 * s,
                tail[1] - dy * 2 * s - py * 8 * s)], fill=c)
    # short smoke trail: two small puffs down to the lower left, kept
    # inside the clear zone above the headline
    for off, r in ((6, 2.5), (11, 3)):
        sx = tail[0] - dx * off
        sy = tail[1] - dy * off
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=GREY)


def draw_drone(d, x, y, w, h, c):
    # quadcopter: central body, four arms, four rotor discs
    cx, cy = x + w / 2, y + h * 0.52
    d.line([(x + 8, y + 8), (cx, cy)], fill=c, width=4)
    d.line([(x + w - 8, y + 8), (cx, cy)], fill=c, width=4)
    d.line([(x + 8, y + h - 8), (cx, cy)], fill=c, width=4)
    d.line([(x + w - 8, y + h - 8), (cx, cy)], fill=c, width=4)
    for rx, ry in ((x + 8, y + 8), (x + w - 8, y + 8),
                   (x + 8, y + h - 8), (x + w - 8, y + h - 8)):
        d.ellipse([rx - 12, ry - 4, rx + 12, ry + 4], fill=c)
    d.rectangle([cx - 16, cy - 9, cx + 16, cy + 9], fill=c)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def draw_chart(d, x, y, w, h, c):
    # axes + a jagged line plunging down, ending in a red arrowhead
    d.line([(x + 6, y + 4), (x + 6, y + h - 8)], fill=c, width=3)
    d.line([(x + 6, y + h - 8), (x + w - 2, y + h - 8)], fill=c, width=3)
    pts = [(x + 8, y + 8), (x + w * 0.28, y + 12), (x + w * 0.45, y + 26),
           (x + w * 0.62, y + 22), (x + w * 0.80, y + h - 16),
           (x + w - 6, y + h - 12)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED)


def draw_cyclone(d, x, y, w, h, c):
    # spiral: concentric arcs of growing radius, like a storm swirl
    cx, cy = x + w / 2, y + h * 0.56
    for i, r in enumerate((7, 13, 19, 25)):
        start = 20 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start=start,
              end=start + 250, fill=c if i % 2 == 0 else RED, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


ICONS = {
    "skyline": draw_skyline,
    "plane": draw_plane,
    "missile": draw_missile,
    "drone": draw_drone,
    "chart": draw_chart,
    "cyclone": draw_cyclone,
}

STORIES = [
    ("ASIA", "APEC summit opens in Shenzhen",
     "Leaders of 21 economies gather in Shenzhen; China said Xi, Trump "
     "and Putin will hold a first trilateral meeting on Thursday, 19 November.",
     "skyline"),
    ("ASIA", "Quad leaders meet in Manila, unveil new plan",
     "Trump met the leaders of Japan, India and Australia and announced "
     "new critical-minerals deals and a joint maritime patrol plan.",
     "plane"),
    ("ASIA", "North Korea fires missile toward Sea of Japan",
     "South Korea's military said Pyongyang fired a ballistic missile "
     "toward the Sea of Japan, the latest in a series of launches this year.",
     "missile"),
    ("MIDDLE EAST", "Iran claims drone strike on US radar site in Bahrain",
     "Iran's Revolutionary Guard said it launched drones at a US radar "
     "site at Sheikh Isa Air Base; Bahrain and the US said the attack "
     "was intercepted.",
     "drone"),
    ("BUSINESS", "US stocks plunge as Dow drops 1,000 points",
     "The Dow fell 849 points after dropping more than 1,000 intraday, "
     "as investors sold tech shares ahead of Nvidia's earnings.",
     "chart"),
    ("WEATHER", "Cyclone Akvan strengthens over Bay of Bengal",
     "The storm strengthened over the Bay of Bengal and headed for the "
     "Andhra Pradesh coast, with landfall forecast around 20 November.",
     "cyclone"),
]


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 36  # margin

    # --- masthead ---
    d.rectangle([mx, 24, W - mx, 30], fill=RED)
    f_title = font(BOLD, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 40), title, font=f_title, fill=NAVY)
    f_date = font(BOLD, 31)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 112), date, font=f_date, fill=RED)
    f_sub = font(REG, 23)
    sub = "Six stories that defined the day"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 150), sub, font=f_sub, fill=NAVY)
    d.line([(mx, 184), (W - mx, 184)], fill=NAVY, width=3)
    d.line([(mx, 190), (W - mx, 190)], fill=NAVY, width=1)

    # --- story grid: 2 cols x 3 rows ---
    gx, gy = mx, 204
    gap = 20
    cw = (W - 2 * mx - gap) // 2
    ch = 246
    f_tag = font(BOLD, 18)
    f_head = font(BOLD, 27)
    f_body = font(REG, 20)
    for i, (tag, head, body, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (cw + gap)
        y0 = gy + row * (ch + 12)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=NAVY,
                    width=2)
        # red tag bar
        d.rectangle([x0, y0, x0 + cw, y0 + 4], fill=RED)
        px, py = x0 + 18, y0 + 16
        d.text((px, py), tag, font=f_tag, fill=RED)
        # flat icon in the top-right corner, clear of all text
        if icon == "missile":
            # smaller (64x34) and higher (y0+6): the old 92x46 missile
            # box bottom sat at y0+54, inside the headline band (from
            # y0+50), and its ground line struck through "missile".
            # New box ends at y0+40, 10px clear of the headline.
            iw, ih = 64, 34
            ICONS[icon](d, x0 + cw - iw - 14, y0 + 6, iw, ih, NAVY)
        else:
            iw, ih = 92, 46
            ICONS[icon](d, x0 + cw - iw - 14, y0 + 8, iw, ih, NAVY)
        py += 34
        # headline, max 2 lines
        for line in wrap(d, head, f_head, cw - 36)[:2]:
            d.text((px, py), line, font=f_head, fill=NAVY)
            py += 33
        py += 4
        # summary, up to 4 lines at full cell width
        for line in wrap(d, body, f_body, cw - 36)[:4]:
            d.text((px, py), line, font=f_body, fill=NAVY)
            py += 25

    # --- footer ---
    fy = gy + 3 * ch + 2 * 12 + 10
    d.line([(mx, fy), (W - mx, fy)], fill=NAVY, width=2)
    f_foot = font(REG, 17)
    foot = ("As reported on 18 November 2026 \u00b7 Sources: Reuters, AP, "
            "White House, IMD")
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, fy + 10), foot, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
