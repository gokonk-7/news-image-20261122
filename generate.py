"""Render the 22 Nov 2026 world-news magazine cover (1024x1024 PNG).

Run once, by hand, during the build:  python3 generate.py
Writes assets/entry.png next to this file. Deterministic: no clock,
no randomness, no network. Only the system DejaVu fonts are read.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (16, 16, 16)
RED = (178, 34, 34)
NAVY = (18, 35, 63)
NAVY_LIGHT = (36, 58, 92)
GREY = (90, 86, 78)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
PALE = (214, 222, 235)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    """A simple drawn globe: gold disc, white meridian rings, red marker."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=4)
    for k in (0.45, 0.8):
        w = int(r * k)
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=WHITE, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=WHITE, width=3)
    draw.line([cx - r + 18, cy - int(r * 0.62), cx + r - 18, cy - int(r * 0.62)],
              fill=WHITE, width=3)
    draw.line([cx - r + 18, cy + int(r * 0.62), cx + r - 18, cy + int(r * 0.62)],
              fill=WHITE, width=3)
    # red marker: the summit that cannot agree
    mx, my = cx + int(r * 0.42), cy - int(r * 0.5)
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=RED,
                 outline=WHITE, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mx = 36  # side margin

    # --- masthead ---
    title_f = font(FONT_BOLD, 56)
    draw.text((W // 2, 26), "THE WORLD TODAY", font=title_f, fill=INK,
              anchor="ma")
    date_f = font(FONT_BOLD, 30)
    draw.text((W // 2, 92), "SUNDAY 22 NOVEMBER 2026", font=date_f,
              fill=RED, anchor="ma")
    draw.line([mx, 136, W - mx, 136], fill=INK, width=3)

    # --- hero panel ---
    hx0, hy0, hx1, hy1 = mx, 150, W - mx, 540
    draw.rectangle([hx0, hy0, hx1, hy1], fill=NAVY)
    draw_globe(draw, 205, 345, 108)

    kicker_f = font(FONT_BOLD, 22)
    draw.text((352, 178), "CLIMATE SUMMIT  ·  ANTALYA", font=kicker_f,
              fill=GOLD)
    head_f = font(FONT_BOLD, 46)
    headline = "COP31 RUNS INTO SUNDAY \u2014 STILL NO DEAL"
    lines = wrap(draw, headline, head_f, 600)
    y = 214
    for line in lines:
        draw.text((352, y), line, font=head_f, fill=WHITE)
        y += 54
    deck_f = font(FONT_REG, 24)
    deck = ("The fossil-fuel fight stalls the climate summit as delegates "
            "run out of time \u2014 and rebook their flights home.")
    for line in wrap(draw, deck, deck_f, 600):
        draw.text((352, y), line, font=deck_f, fill=PALE)
        y += 32
    # temperature line under the deck
    draw.text((352, 486), "1.5\u00b0C LIMIT  ·  OFFICIALLY MISSED",
              font=font(FONT_BOLD, 22), fill=(224, 90, 70))

    # --- story strips ---
    strips = [
        ("1", "Bahrain probes Patriot crash",
         "Smoke reported after a possible aerial interception; "
         "safety alert issued."),
        ("2", "US airlines warned of terror threat",
         "Possible al-Qaeda-linked attacks feared ahead of "
         "Thanksgiving, US carriers told."),
        ("3", "Suicide bombing kills five in Pakistan",
         "A car bomb hits a security convoy in Naushki, Balochistan; "
         "the BLA claims the attack."),
        ("4", "Australia ends England\u2019s T20 streak",
         "The hosts break a seven-match winning run in the shortest "
         "format."),
    ]
    head_s = font(FONT_BOLD, 26)
    sum_s = font(FONT_REG, 20)
    y = 556
    for num, head, summ in strips:
        draw.ellipse([mx + 4, y + 6, mx + 48, y + 50], fill=RED)
        num_f = font(FONT_BOLD, 26)
        draw.text((mx + 26, y + 8), num, font=num_f, fill=WHITE,
                  anchor="ma")
        draw.text((mx + 62, y + 2), head, font=head_s, fill=INK)
        for i, line in enumerate(wrap(draw, summ, sum_s, W - mx - 62 - mx)):
            draw.text((mx + 62, y + 36 + i * 26), line, font=sum_s,
                      fill=GREY)
        y += 86
        if num != "4":
            draw.line([mx, y - 8, W - mx, y - 8], fill=(210, 204, 190),
                      width=2)

    # --- footer ticker (shrink to fit the band, never overflow it) ---
    draw.rectangle([mx, 916, W - mx, 972], fill=RED)
    ticker = ("GULF  ·  Iran says Qeshm blasts were US munitions disposal "
              "\u2014 not a fresh attack")
    tick_size = 20
    tick_f = font(FONT_BOLD, tick_size)
    while draw.textlength(ticker, font=tick_f) > (W - 2 * mx - 24):
        tick_size -= 1
        tick_f = font(FONT_BOLD, tick_size)
    draw.text((W // 2, 930), ticker, font=tick_f, fill=WHITE, anchor="ma")

    credit_f = font(FONT_REG, 16)
    draw.text((W // 2, 986),
              "All stories reported on Sunday 22 November 2026",
              font=credit_f, fill=GREY, anchor="ma")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
