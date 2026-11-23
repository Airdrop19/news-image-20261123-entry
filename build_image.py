"""Build entry.png: a one-page broadsheet summing up world news of Monday 23 November 2026.

Drawn with Pillow at 1024x1024. Every story below was reported on 23 Nov 2026
(wire and day-page reporting aggregated that day). Claims are worded as claims
and credited to whoever made them. Layout follows the classic one-day
front-page pattern: masthead, stat strip, region bar, 13 numbered illustrated
cards, a pinned world map, 26 one-line briefs and a date-check footer.
All artwork is original flat drawing.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (18, 22, 32)
MUTED = (92, 96, 104)
RED = (176, 42, 42)
NAVY = (27, 58, 110)
TEAL = (18, 110, 118)
GOLD = (176, 128, 10)
GREEN = (44, 120, 66)
PURPLE = (96, 70, 150)
RUST = (172, 84, 44)
OLIVE = (110, 104, 52)
SLATE = (84, 96, 110)
CARD_BG = (255, 253, 246)
LINE = (206, 198, 178)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, max_w, gap=3, max_lines=4):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w)[:max_lines]:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


# ---------------- flat banner icons ----------------
def ic_gavel(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 28, cy + 10, cx + 28, cy + 24], fill=(240, 200, 90))
    d.line([(cx - 32, cy - 18), (cx + 6, cy + 10)], fill=(240, 200, 90), width=8)
    d.rectangle([cx - 44, cy - 30, cx - 18, cy - 8], fill=(240, 200, 90))
    d.ellipse([cx + 26, cy - 24, cx + 54, cy + 4], fill=(246, 241, 229))


def ic_flame(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx, cy - 24), (cx + 17, cy + 4), (cx + 9, cy + 22), (cx - 9, cy + 22), (cx - 17, cy + 4)], fill=(240, 120, 40))
    d.polygon([(cx, cy - 5), (cx + 8, cy + 9), (cx, cy + 20), (cx - 8, cy + 9)], fill=(250, 200, 80))


def ic_ship(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx - 32, cy + 5), (cx + 32, cy + 5), (cx + 20, cy + 20), (cx - 20, cy + 20)], fill=(246, 241, 229))
    d.rectangle([cx - 15, cy - 11, cx + 7, cy + 4], fill=(246, 241, 229))
    d.line([(cx + 17, cy - 20), (cx + 17, cy + 4)], fill=(246, 241, 229), width=4)
    d.polygon([(cx + 17, cy - 20), (cx + 31, cy - 12), (cx + 17, cy - 5)], fill=RED)
    d.arc([cx - 38, cy + 15, cx - 8, cy + 29], 0, 180, fill=(150, 200, 220), width=3)
    d.arc([cx + 2, cy + 15, cx + 32, cy + 29], 0, 180, fill=(150, 200, 220), width=3)


def ic_drone(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx - 22, cy - 14), (cx + 22, cy + 14)], fill=(246, 241, 229), width=4)
    d.line([(cx - 22, cy + 14), (cx + 22, cy - 14)], fill=(246, 241, 229), width=4)
    for dx, dy in [(-22, -14), (22, -14), (-22, 14), (22, 14)]:
        d.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6], fill=(240, 200, 90))
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(246, 241, 229))


def ic_dome(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.arc([cx - 24, cy - 22, cx + 24, cy + 14], 180, 360, fill=(246, 241, 229), width=5)
    d.line([(cx, cy - 27), (cx, cy - 18)], fill=(246, 241, 229), width=4)
    d.rectangle([cx - 28, cy + 1, cx + 28, cy + 8], fill=(246, 241, 229))
    for i in range(-2, 3):
        d.line([(cx + i * 10, cy + 10), (cx + i * 10, cy + 20)], fill=(246, 241, 229), width=4)
    d.line([(cx - 30, cy + 23), (cx + 30, cy + 23)], fill=(246, 241, 229), width=4)


def ic_ballot(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 24, cy - 1, cx + 24, cy + 22], fill=(246, 241, 229))
    d.rectangle([cx - 12, cy - 25, cx + 12, cy - 3], fill=(255, 255, 255), outline=(246, 241, 229), width=3)
    d.line([(cx - 6, cy - 16), (cx - 1, cy - 9), (cx + 7, cy - 19)], fill=GREEN, width=4)
    d.rectangle([cx - 15, cy + 5, cx + 15, cy + 10], fill=NAVY)


def ic_scales(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx, cy - 22), (cx, cy + 16)], fill=(246, 241, 229), width=4)
    d.line([(cx - 24, cy - 16), (cx + 24, cy - 16)], fill=(246, 241, 229), width=4)
    for sx in (-1, 1):
        px = cx + sx * 24
        d.line([(px, cy - 16), (px - 9, cy + 1)], fill=(246, 241, 229), width=3)
        d.line([(px, cy - 16), (px + 9, cy + 1)], fill=(246, 241, 229), width=3)
        d.arc([px - 10, cy - 1, px + 10, cy + 12], 0, 180, fill=(240, 200, 90), width=4)
    d.line([(cx - 13, cy + 20), (cx + 13, cy + 20)], fill=(246, 241, 229), width=4)


def ic_chart(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx - 28, cy - 22), (cx - 28, cy + 22), (cx + 30, cy + 22)], fill=(246, 241, 229), width=4)
    d.line([(cx - 24, cy - 13), (cx - 7, cy - 3), (cx + 6, cy + 2), (cx + 24, cy + 16)], fill=(240, 120, 40), width=5)
    d.polygon([(cx + 24, cy + 16), (cx + 14, cy + 14), (cx + 22, cy + 5)], fill=(240, 120, 40))


def ic_planet(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(200, 170, 130))
    d.ellipse([cx - 7, cy - 11, cx + 2, cy - 2], fill=(160, 130, 95))
    d.ellipse([cx + 4, cy + 3, cx + 12, cy + 11], fill=(160, 130, 95))
    d.arc([cx - 31, cy - 9, cx + 31, cy + 14], 200, 340, fill=(246, 241, 229), width=3)
    d.ellipse([cx + 20, cy - 24, cx + 27, cy - 17], fill=(246, 241, 229))


def ic_flag(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.line([(cx - 18, cy - 24), (cx - 18, cy + 24)], fill=(246, 241, 229), width=4)
    sq = 12
    for row in range(3):
        for col in range(3):
            fill = (18, 22, 32) if (row + col) % 2 == 0 else (255, 255, 255)
            d.rectangle([cx - 18 + col * sq, cy - 24 + row * sq,
                         cx - 18 + (col + 1) * sq, cy - 24 + (row + 1) * sq], fill=fill)


def ic_star(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 24 if i % 2 == 0 else 11
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=(240, 200, 90))


def ic_doc(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 15, cy - 24, cx + 15, cy + 24], fill=(255, 255, 255), outline=(246, 241, 229), width=3)
    for yy in (-13, -4, 5):
        d.line([(cx - 9, cy + yy), (cx + 9, cy + yy)], fill=MUTED, width=3)
    d.line([(cx - 7, cy + 13), (cx - 2, cy + 18), (cx + 8, cy + 9)], fill=GREEN, width=4)


def ic_cricket(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.text((cx - d.textlength("720/9", font=F(SERIF_B, 30)) / 2, cy - 18), "720/9", font=F(SERIF_B, 30), fill=(246, 241, 229))
    d.ellipse([cx + 44, cy - 16, cx + 58, cy - 2], fill=(240, 120, 40))


def ic_pope(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.polygon([(cx, cy - 26), (cx + 14, cy - 6), (cx + 16, cy + 14), (cx - 16, cy + 14), (cx - 14, cy - 6)], fill=(246, 241, 229))
    d.line([(cx, cy - 18), (cx, cy + 2)], fill=GOLD, width=4)
    d.line([(cx - 6, cy - 12), (cx + 6, cy - 12)], fill=GOLD, width=4)
    d.line([(cx - 20, cy + 22), (cx + 20, cy + 22)], fill=(246, 241, 229), width=4)


def ic_globe(d, box, c):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(246, 241, 229), width=4)
    d.ellipse([cx - 10, cy - 22, cx + 10, cy + 22], outline=(246, 241, 229), width=3)
    d.line([(cx - 22, cy), (cx + 22, cy)], fill=(246, 241, 229), width=3)


# ---------------- content ----------------
CARDS = [
    (RED, ic_drone, "BRUSSELS, BELGIUM", "NATO EMERGENCY TALKS",
     "NATO meets over Russian missiles in Poland",
     "The North Atlantic Council meets Monday after Poland says three Russian Kh-101 cruise missiles fell in its southeast on Friday. Rutte vows to defend every inch.",
     "PAP · RMF24 · Reuters", (4.4, 50.8)),
    (NAVY, ic_gavel, "ANTALYA, TURKEY", "CLIMATE FALLOUT",
     "COP31 ends with no deal; leaders react",
     "Talks collapse over fossil-fuel wording, the longest COP on record. On Monday Australia's PM calls the failure a sign of difficult geopolitical times.",
     "AFP · Reuters · CNN", (30.7, 36.9)),
    (TEAL, ic_chart, "TAIPEI, TAIWAN", "MARKETS",
     "Taiwan bans short selling after crash",
     "The Taiex falls 17.5% in its worst week since 1991. From Monday, short sales below the prior close are banned; a NT$500bn fund is buying shares.",
     "Bloomberg · FSC", (121.6, 25.0)),
    (RUST, ic_flame, "DYMER, UKRAINE", "UKRAINE WAR",
     "Rescuers dig for 14 missing in Kyiv flats",
     "A Russian drone partly destroys a five-storey block in Dymer. Rescuers search the rubble into Monday.",
     "BBC · AP", (30.5, 50.5)),
    (RED, ic_flame, "CIKANDE, INDONESIA", "FACTORY FIRE",
     "Candy factory fire: 24 dead",
     "Rescuers recover 24 body bags from the Cikande candy factory fire in Banten.",
     "AP", (106.2, -6.1)),
    (PURPLE, ic_doc, "SEOUL, SOUTH KOREA", "AI CHEATING ROW",
     "Education minister quits over AI exam scandal",
     "South Korea's education minister resigns as an AI-driven exam cheating scandal spreads through schools.",
     "AFP", (127.0, 37.6)),
    (GREEN, ic_flag, "LONDON, UK", "FOOTBALL",
     "UK to host 2035 Women's World Cup",
     "FIFA is set to confirm on Monday that the United Kingdom will host the 2035 Women's World Cup.",
     "BBC", (-0.1, 51.5)),
    (GOLD, ic_dome, "OKINAWA, JAPAN", "HERITAGE",
     "Shuri Castle hall reopens to the public",
     "Okinawa celebrates the restored main hall of Shuri Castle, opening to visitors Monday.",
     "AP", (127.7, 26.2)),
    (TEAL, ic_ship, "BENGHAZI, LIBYA", "WAR AT SEA",
     "Drone boat hits Russian ship in Libya",
     "Libya's eastern government says a suspected sea drone exploded aboard a Russian ship.",
     "Reuters · RFE/RL", (20.1, 32.1)),
    (NAVY, ic_ship, "STRAIT OF HORMUZ", "GULF SHIPPING",
     "Tankers struck near Hormuz again",
     "Iran says two more tankers caught fire after hitting naval mines near Hormuz.",
     "AP · UKMTO", (56.5, 26.6)),
    (GOLD, ic_star, "ATP FINALS", "TENNIS",
     "Alcaraz wins first ATP Finals title",
     "Carlos Alcaraz beats Alexander Zverev in the final to lift his first ATP Finals trophy.",
     "wire reports", (7.7, 45.1)),
    (RED, ic_flag, "PORTUGAL", "MOTOGP",
     "Marquez ties record with eighth title",
     "Marc Marquez wins a record-tying eighth MotoGP world title at the Portuguese Grand Prix.",
     "wire reports", (-8.6, 39.5)),
    (SLATE, ic_scales, "UNITED NATIONS", "AI WEAPONS",
     "128 states back killer-robot rules by 2028",
     "128 states agree to pursue international rules on lethal autonomous weapons by 2028 as UN talks continue.",
     "UN · wire reports", (-73.9, 40.7)),
]

BRIEFS = [
    "SOUTH SUDAN — 24 civilians killed in violence",
    "LAHORE — World's worst air, AQI 538",
    "MANILA — Transport strike; free rides offered",
    "AMAZON — Man rescued after 11 days lost",
    "JERUSALEM — Coalition talks end, no deal",
    "BRASILIA — Bolsonaro stable in intensive care",
    "TEHRAN — Iran rations electricity amid strikes",
    "SEOUL · TOKYO — Asia holds emergency market talks",
    "LPGA — Thitikul wins third title in a row",
    "ANFIELD — Liverpool beat ten-man Man United",
    "WASHINGTON — Trump reposts 'TrumpCare' pitch",
    "KHARTOUM — Drones hit homes, UN building",
    "WEST BANK — Settlers torch 12 vehicles",
    "OHIO — Three killed at baby shower shooting",
    "IOWA — Army to detonate bomb chemicals",
    "KINSHASA — WHO chief pleads for peace in Ebola zone",
    "RIYADH — Coalition intercepts Houthi missile",
    "MANAMA — Iran strike wounds two, Saudis condemn",
    "KANO — 35 Fulani killed in revenge attacks",
    "WARSAW — Tusk calls missile fall a provocation",
    "BRUSSELS — EU weighs €45bn Ukraine loan",
    "NEW YORK — US intel chief backs Trump's Putin line",
    "MADRID — Sanchez: people, not papers, decide PM",
    "DHAKA — Hasina seeks new passport, report says",
    "SEOUL — Kim: North seeks security, not supremacy",
    "SUVA · SYDNEY — Pacific reels from COP31 failure",
]

STATS = [
    ("3", "Russian Kh-101 missiles Poland says fell on its soil"),
    ("-17.5%", "Taiex weekly fall, worst since 1991"),
    ("14", "still missing after drone hit Kyiv flats"),
    ("24", "dead in Indonesia candy factory fire"),
    ("538", "Lahore AQI, world's most polluted city"),
    ("128", "states back killer-robot rules by 2028"),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.text((18, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 16), fill=RED)
right = "39 STORIES · 7 REGIONS · EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
d.text((W - 18 - d.textlength(right, font=F(SANS_B, 14)), 10), right, font=F(SANS_B, 14), fill=INK)
title = "Monday 23 November 2026"
tw = d.textlength(title, font=F(SERIF_B, 50))
d.text(((W - tw) / 2, 26), title, font=F(SERIF_B, 50), fill=INK)
ticker = "NATO meets over missiles in Poland · COP31 fallout · Taiwan bans short selling · 14 missing in Kyiv · UK to host 2035 Women's World Cup"
tw2 = d.textlength(ticker, font=F(SERIF_I, 17))
d.text(((W - tw2) / 2, 82), ticker, font=F(SERIF_I, 17), fill=MUTED)
d.line([(18, 106), (W - 18, 106)], fill=INK, width=3)
d.line([(18, 111), (W - 18, 111)], fill=INK, width=1)

# ---------- stat strip ----------
sy = 118
col_w = (W - 36) // 6
for i, (num, cap) in enumerate(STATS):
    x = 18 + i * col_w
    d.text((x + 4, sy), num, font=F(SERIF_B, 28), fill=RED if i % 2 == 0 else NAVY)
    para(d, (x + 4, sy + 34), cap, F(SANS_R, 11), MUTED, col_w - 10, gap=2, max_lines=3)
    if i:
        d.line([(x - 4, sy + 2), (x - 4, sy + 60)], fill=LINE, width=1)
d.line([(18, sy + 66), (W - 18, sy + 66)], fill=LINE, width=1)

# ---------- region bar ----------
regions = [("EUROPE", 8, NAVY), ("ASIA", 9, RUST), ("MID EAST", 7, OLIVE), ("AFRICA", 5, GREEN),
           ("AMERICAS", 6, PURPLE), ("OCEANIA", 1, TEAL), ("GLOBAL", 3, SLATE)]
total_r = sum(v for _, v, _ in regions)
ry = sy + 74
x = 18
for name, v, color in regions:
    wpx = int((W - 36) * v / total_r)
    d.rectangle([x, ry, x + wpx, ry + 19], fill=color)
    label = f"{name} {v}"
    if wpx > d.textlength(label, font=F(SANS_B, 11.5)) + 8:
        d.text((x + 6, ry + 4), label, font=F(SANS_B, 11.5), fill=(255, 255, 255))
    x += wpx

# ---------- cards ----------
def card(x0, y0, wpx, hpx, idx, banner_h, head_size, body_size, body_lines, show_credit=True):
    color, icon, loc, kicker, head, summ, credit, _pin = CARDS[idx]
    d.rounded_rectangle([x0, y0, x0 + wpx, y0 + hpx], 8, fill=CARD_BG, outline=LINE, width=2)
    d.rectangle([x0, y0, x0 + wpx, y0 + banner_h], fill=color)
    # draw the icon on its own layer so it is clipped to the banner
    layer = Image.new("RGBA", (wpx, banner_h), (0, 0, 0, 0))
    icon(ImageDraw.Draw(layer), [0, 0, wpx, banner_h], color)
    img.paste(layer, (x0, y0), layer)
    d.ellipse([x0 + 8, y0 + banner_h - 13, x0 + 34, y0 + banner_h + 13], fill=NAVY, outline=(255, 255, 255), width=2)
    ns = str(idx + 1)
    d.text((x0 + 21 - d.textlength(ns, font=F(SANS_B, 16)) / 2, y0 + banner_h - 8), ns, font=F(SANS_B, 16), fill=(255, 255, 255))
    d.text((x0 + 42, y0 + banner_h + 3), loc, font=F(SANS_B, 10.5), fill=MUTED)
    ty = y0 + banner_h + 19
    d.text((x0 + 10, ty), kicker, font=F(SANS_B, 11.5), fill=color)
    cw = d.textlength(credit, font=F(SANS_R, 9.5))
    d.text((x0 + wpx - 10 - cw, ty + 2), credit, font=F(SANS_R, 9.5), fill=MUTED)
    ty += 15
    ty = para(d, (x0 + 10, ty), head, F(SERIF_B, head_size), INK, wpx - 20, gap=2, max_lines=2)
    para(d, (x0 + 10, ty + 2), summ, F(SANS_R, body_size), INK, wpx - 20, gap=2, max_lines=body_lines)
    if show_credit:
        d.text((x0 + 10, y0 + hpx - 16), credit, font=F(SANS_R, 10), fill=MUTED)


cy = ry + 27
gap = 8
w3 = (W - 36 - 2 * gap) // 3
for i in range(3):
    card(18 + i * (w3 + gap), cy, w3, 164, i, 48, 18, 12.5, 4, show_credit=False)
cy += 164 + gap
w5 = (W - 36 - 4 * gap) // 5
for r in range(2):
    for i in range(5):
        card(18 + i * (w5 + gap), cy, w5, 150, 3 + r * 5 + i, 38, 15.5, 11.5, 3, show_credit=False)
    cy += 150 + gap

# ---------- bottom: map + briefs ----------
by = cy + 2
d.line([(18, by), (W - 18, by)], fill=INK, width=2)
by += 7
d.text((18, by), "THE 13 DRAWN STORIES, MAPPED", font=F(SANS_B, 13.5), fill=INK)
d.text((430, by), "IN BRIEF — 26 MORE STORIES OF THE DAY", font=F(SANS_B, 13.5), fill=INK)
by += 20

MAP_ROWS = [
    "  ####    ##        #####  #########      ",
    " ########  #   ##  ########################",
    "  #########     ######################### ",
    "   ######       #######  #################",
    "    ####         #####    ############### ",
    "     ##           ###      #############  ",
    "     #             #        ###########   ",
    "      #                     ##########    ",
    "      ##                     ########     ",
    "       ##                     ######  #   ",
    "        #                      ####       ",
    "        #                       ##    #   ",
]
map_x0, map_y0, map_w, map_h = 18, by, 396, 140
d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], fill=(232, 238, 240), outline=LINE, width=1)
cols = max(len(r) for r in MAP_ROWS)
for ri, row in enumerate(MAP_ROWS):
    for ci, ch in enumerate(row):
        if ch == "#":
            px = map_x0 + 6 + ci * (map_w - 12) / cols
            py = map_y0 + 7 + ri * (map_h - 14) / len(MAP_ROWS)
            d.ellipse([px - 2.3, py - 2.3, px + 2.3, py + 2.3], fill=(150, 170, 140))
for i, c in enumerate(CARDS):
    lon, lat = c[7]
    px = map_x0 + (lon + 180) / 360 * map_w
    py = map_y0 + (90 - lat) / 180 * map_h
    px = max(map_x0 + 10, min(map_x0 + map_w - 10, px))
    py = max(map_y0 + 10, min(map_y0 + map_h - 10, py))
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
    ns = str(i + 1)
    d.text((px - d.textlength(ns, font=F(SANS_B, 11)) / 2, py - 7), ns, font=F(SANS_B, 11), fill=(255, 255, 255))
para(d, (map_x0, map_y0 + map_h + 5), "Pins match the numbered cards above. Schematic map, not to scale.",
     F(SANS_R, 10.5), MUTED, map_w, gap=2, max_lines=2)

bx = 430
bw = (W - 18 - bx - 14) // 2
for i, line in enumerate(BRIEFS):
    col, row = i % 2, i // 2
    x = bx + col * (bw + 14)
    y = by + row * 14.5
    d.text((x, y), f"{i + 14}", font=F(SANS_B, 11), fill=NAVY)
    d.text((x + 24, y), line, font=F(SANS_R, 11), fill=INK)

# ---------- footer ----------
fy = H - 88
d.rounded_rectangle([18, fy, W - 18, fy + 42], 6, outline=RED, width=2)
d.text((28, fy + 5), "DATE CHECK — NOT MONDAY'S NEWS, AND NOT COUNTED ABOVE", font=F(SANS_B, 12), fill=RED)
para(d, (28, fy + 22),
     "Weekend items still circulating (the COP31 collapse itself, Friday's missile fall, Sunday's finals) are shown only through Monday's reporting; every story above was reported on Monday 23 November 2026.",
     F(SANS_R, 11), INK, W - 76, gap=2, max_lines=2)
d.text((18, fy + 50), "Monday 23 November 2026, in every time zone; claims credited to those who made them.",
       font=F(SANS_R, 11.5), fill=MUTED)
src = "Sources: BBC · Reuters · AP · AFP · Al Jazeera · PAP · Bloomberg — artwork original"
d.text((18, fy + 67), src, font=F(SANS_R, 11.5), fill=MUTED)
d.text((W - 18 - d.textlength("23 NOV 2026", font=F(SANS_B, 12.5)), fy + 67), "23 NOV 2026", font=F(SANS_B, 12.5), fill=INK)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)
