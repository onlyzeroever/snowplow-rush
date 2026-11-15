"""Ski Resort, pro pass. Every job is a real mountain: forest everywhere, and the pistes are carved corridors that
wind down through it (all checked for every machine). Skiers ride the pistes (they follow the carved line), snow guns
stand at the piste edges, chairlifts and the gondola run overhead along cleared lift lines.
Shop names: 45 SKI SCHOOL 46 LIFT 47 SKI HIRE 48 APRES 49 GONDOLA."""
import math
from common import *

SH = dict(SCHOOL=45, LIFT=46, HIRE=47, APRES=48, GONDOLA=49)
GREEN, BLUE, RED, BLACK = 0, 1, 2, 3


# ------------------------------------------------------------------ geometry helpers
def cx_at(pts, y):
    """x of a polyline's centre at height y"""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        lo, hi = min(ay, by), max(ay, by)
        if lo <= y <= hi and hi > lo: return ax + (bx - ax) * (y - ay) / (by - ay)
    return min(pts, key=lambda p: abs(p[1] - y))[0]


def hw_at(pts, w, y):
    """horizontal half-width of a carved corridor at height y (wider on the diagonals)"""
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        lo, hi = min(ay, by), max(ay, by)
        if lo <= y <= hi and hi > lo:
            L = math.hypot(bx - ax, by - ay); return w / 2 * L / abs(by - ay)
    return w / 2


def edge(pts, w, y, side, inset=0):
    """the x of the left (side=-1) or right (side=1) edge of a corridor at height y"""
    return cx_at(pts, y) + side * (hw_at(pts, w, y) - inset)


def woods(d, seed, y0=0, y1=None, x0=0, x1=180, dens=0.85, kind='forest', step=9):
    wild(d, kind, x0, y0, x1 - x0, (d['h'] if y1 is None else y1) - y0, seed, dens, step)


def run(d, pts, w, t='piste'):
    """carve a piste through the woods; returns its carve index (for skiers to follow)"""
    carve(d, w, pts); path(d, t, w - 4, pts)
    return len(d['data']['carves']) - 1


def clearing(d, x, y, w, h, t=None): clear(d, x, y, w, h, t)


def poles(d, pts, w, seed, every=120, inset=2, y0=None, y1=None):
    """piste marker poles down both edges of a run, alternating sides"""
    r = rng(seed); k = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 90: continue
        t = 40
        while t < L - 40:
            cx, cy = ax + (bx - ax) * t / L, ay + (by - ay) * t / L
            if (y0 is None or cy >= y0) and (y1 is None or cy <= y1):
                s = -1 if k % 2 == 0 else 1
                x = edge(pts, w, cy, s, inset) - (0 if s < 0 else 4)
                if 2 <= x <= 174: P(d, 'snowpole', int(x), int(cy) - 15)
                k += 1
            t += every + r.randint(-14, 14)


def grade(d, pts, w, y, g, side=-1):
    """the round/square/diamond piste sign painted at the side of a run"""
    x = edge(pts, w, y, side, 20 if side < 0 else 36)
    dec(d, 'piste', int(max(2, min(162, x))), int(y), g)


def skiers(d, idx, n, per0, offs=(-22, 18, 0, -8)):
    for k in range(n): H(d, 'skier', 90 + offs[k % len(offs)], 0, round(per0 + k * 1.3, 1), idx)


def gun(d, pts, w, y, side, per=7.0, rng_=64):
    """a snow gun standing at the piste edge, spraying across it"""
    x = edge(pts, w, y, side, 4); x = int(max(2, min(160, x if side < 0 else x - 18)))
    H(d, 'cannon', x, int(y), 0.35 if side < 0 else 2.79, per, rng_)


def fence(d, x, y, n, v=True):
    P(d, 'snowfencev' if v else 'snowfence', int(x), int(y), int(n))


def base_plaza(d, y0, y1, seed, racks=True, dress=True):
    """the busy resort base: paving, ski racks, deckchairs, a trail map and lamps"""
    G(d, 'pave', 0, y0, 180, y1 - y0); r = rng(seed)
    if racks:
        for y in range(y0 + 16, y1 - 30, 26): P(d, 'skirack', 2, y); P(d, 'skirack', 154, y + 8)
    if dress: P(d, 'trailmap', 30, y0 + 4); P(d, 'lamp', 60, y0 + 8); P(d, 'lamp', 116, y0 + 8)
    dec(d, 'kerbh', 0, y0, 180)


# ------------------------------------------------------------------ the fifteen jobs
def skischool():
    """SKI SCHOOL: the resort base, the nursery slope with its magic carpet and kids' slalom, then the gentle green
    run up through the pines to the mountain hut."""
    h = 3600; d = job('skischool', 'SKI SCHOOL', 'ski', ['festival'], h, 65, 13.8, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h)
    woods(d, 101, 0, 3240, dens=0.86)
    base_plaza(d, 3380, h, 1)
    P(d, 'big', 0, 3300, SH['SCHOOL']); P(d, 'kiosk', 150, 3330, 1); P(d, 'parasol', 120, 3420, 0); P(d, 'parasol', 118, 3470, 2)
    P(d, 'deckchair', 30, 3440, 0); P(d, 'deckchair', 44, 3440, 1); P(d, 'deckchair', 30, 3490, 2); P(d, 'deckchair', 44, 3490, 0)
    # the nursery slope: wide open, a magic carpet up the right side, cones and baby gates, two snowmen
    G(d, 'piste', 0, 2260, 180, 1060)
    for r_ in ((0, 2260, 180, 440), (0, 2770, 180, 550), (0, 2700, 64, 70), (108, 2700, 72, 70)): clearing(d, *r_)
    P(d, 'carpet', 166, 2420, 520); P(d, 'hut', 164, 2944); P(d, 'flag', 150, 2396, 0)
    for k, y in enumerate(range(2480, 3000, 104)): P(d, 'cone', 40 if k % 2 == 0 else 96, y)
    for k, y in enumerate(range(2560, 3000, 150)):
        x = 30 if k % 2 == 0 else 80; P(d, 'gatepole', x, y, 0); P(d, 'gatepole', x + 46, y, 1)
    P(d, 'snowman', 6, 2300); P(d, 'snowman', 136, 3140); P(d, 'signpost', 70, 3200)
    for x in (4, 18, 32): P(d, 'bench', x, 3236)
    # the green run up the mountain
    pts = [(90, 2300), (60, 2050), (112, 1800), (70, 1520), (110, 1250), (74, 960), (108, 700), (84, 440), (90, 220)]
    i = run(d, pts, 112); poles(d, pts, 112, 11)
    grade(d, pts, 112, 2160, GREEN, -1); grade(d, pts, 112, 1180, GREEN, 1)
    clearing(d, 0, 0, 180, 260, 'stone')
    P(d, 'cabin', 68, 4); P(d, 'firepit', 40, 96); P(d, 'bench', 10, 60); P(d, 'bench', 156, 60); P(d, 'trailmap', 136, 120)
    for y in (700, 1450, 2000): H(d, 'thrower', int(cx_at(pts, y)) + 20, y)
    for y in (2440, 2860, 3120): H(d, 'pedx', 30, y, (y // 100) % 2)
    H(d, 'dog', 90, 3460)
    return d


def chalets():
    """CHALET VILLAGE: a lane winding down through the woods between chalets, hot tubs and woodpiles, lanterns strung
    across it, and the Christmas market on the village square at the bottom."""
    h = 3800; d = job('chalets', 'CHALET VILLAGE', 'ski', ['skischool'], h, 70, 14.0, 7, start=[90, 40])
    G(d, 'grass', 0, 0, 180, h); woods(d, 202, dens=0.88)
    pts = [(90, 0), (90, 180), (60, 380), (60, 980), (120, 1180), (120, 1760), (90, 1900), (90, 2120), (60, 2320), (60, 2900), (120, 3100), (120, h)]
    carve(d, 120, pts); path(d, 'cobble', 44, pts)
    # chalets flush to the edges of each straight, each with a hot tub, a fire pit or a woodpile
    for k, y in enumerate(range(420, 940, 110)):
        P(d, 'chalet', -2, y, k % 3)
        P(d, ('tub', 'firepit', 'crate')[k % 3], 106, y + 18)
    for k, y in enumerate(range(1220, 1740, 110)):
        P(d, 'chalet', 138, y, (k + 1) % 3)
        P(d, ('firepit', 'tub', 'crate')[k % 3], 58, y + 18)
    for k, y in enumerate(range(2360, 2880, 110)):
        P(d, 'chalet', -2, y, (k + 2) % 3)
        P(d, ('crate', 'tub', 'firepit')[k % 3], 106, y + 20)
    for k, y in enumerate(range(3140, 3700, 120)):
        P(d, 'chalet', 138, y, k % 3)
        P(d, ('tub', 'crate', 'firepit')[k % 3], 58, y + 18)
    # the village square, half way down: market stalls, an ice sculpture, the clock tower
    clearing(d, 0, 1880, 180, 260, 'stone'); C(d, 'mosaic', 90, 2010, 30); C(d, 'ice', 90, 2010, 18)
    P(d, 'icesculpt', 75, 1960); P(d, 'stall', 4, 1890, 0); P(d, 'stall', 146, 1890, 2); P(d, 'stall', 4, 2100, 3); P(d, 'stall', 146, 2100, 1)
    P(d, 'bench', 40, 1930); P(d, 'bench', 128, 1930); P(d, 'bench', 40, 2090); P(d, 'bench', 128, 2090)
    over(d, 'lights', 0, 1900, 180, 3); over(d, 'lights', 0, 2120, 180, 1)
    for y in (300, 700, 1400, 2600, 3300): over(d, 'lant', int(cx_at(pts, y)) - 50, y, 100)
    for y in (560, 1500, 2500, 3400): P(d, 'lantpost', int(cx_at(pts, y)) - 30, y)
    P(d, 'signpost', 120, 60); P(d, 'trailmap', 30, 90)
    H(d, 'pedx', 30, 1960); H(d, 'pedx', 120, 2060, 1); H(d, 'dog', 60, 800); H(d, 'dog', 120, 3300)
    H(d, 'thrower', 70, 1500); H(d, 'thrower', 60, 2700); H(d, 'thrower', 110, 3600)
    return d


def lift():
    """LIFT STATION: the queue maze and ticket booths at the base, the chairlift running overhead up a cleared lift line,
    the piste weaving under it, and the top station."""
    h = 3800; d = job('lift', 'LIFT STATION', 'ski', ['chalets'], h, 70, 14.2, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h); woods(d, 303, 0, 3360, dens=0.86)
    base_plaza(d, 3400, h, 3, racks=False, dress=False); P(d, 'trailmap', 146, 3590); P(d, 'lamp', 150, 3420)
    for y in range(3660, h - 30, 26): P(d, 'skirack', 2, y)
    P(d, 'big', 70, 3330, SH['LIFT'])
    P(d, 'rail', 100, 3470, 80); P(d, 'rail', 60, 3530, 80)        # the lift queue
    P(d, 'booth', 40, 3610, 0); P(d, 'groomer', 136, 3640)
    # the lift line: a wide clearing up the right with the chairs overhead and the pylons in it
    carve(d, 60, [(150, 3360), (150, 160)]); G(d, 'grass', 120, 160, 60, 3200)
    over(d, 'liftline', 135, 140, 3220)
    for y in range(400, 3300, 360): P(d, 'pylon', 143, y)
    # the piste weaves left and right, crossing under the lift twice
    pts = [(50, 3420), (60, 3000), (60, 2700), (130, 2400), (60, 2050), (60, 1700), (130, 1380), (60, 1050), (60, 700), (100, 420), (90, 200)]
    i = run(d, pts, 100); poles(d, pts, 100, 13, y1=3300)
    grade(d, pts, 100, 3200, GREEN, -1); grade(d, pts, 100, 1900, BLUE, -1)
    clearing(d, 0, 0, 180, 240, 'stone'); P(d, 'liftstation', 118, 30); P(d, 'trailmap', 20, 40); P(d, 'bench', 30, 150); P(d, 'bench', 70, 150)
    skiers(d, i, 1, 8.0)
    H(d, 'pedx', 20, 3440); H(d, 'pedx', 120, 3560, 1); H(d, 'thrower', 40, 1200); H(d, 'thrower', 60, 2800)
    return d


def snowguns():
    """SNOW GUNS: a wide groomed piste with snow guns standing at its edges, re-covering what you clear."""
    h = 4000; d = job('snowguns', 'SNOW GUNS', 'ski', ['lift'], h, 76, 14.4, 7, start=[90, 40])
    G(d, 'grass', 0, 0, 180, h); woods(d, 404, dens=0.86)
    pts = [(90, 0), (90, 200), (70, 600), (110, 1000), (70, 1450), (110, 1900), (70, 2350), (110, 2800), (70, 3250), (90, 3650), (90, h)]
    i = run(d, pts, 128); poles(d, pts, 128, 14, every=160)
    grade(d, pts, 128, 260, BLUE, -1)
    for k, y in enumerate(range(420, 3600, 420)): gun(d, pts, 128, y, -1 if k % 2 == 0 else 1, 7.0 + (k % 3) * 0.5)
    clearing(d, 0, 0, 180, 200, 'stone'); P(d, 'hut', 10, 20); P(d, 'signpost', 150, 40); P(d, 'trailmap', 28, 120)
    clearing(d, 0, 3700, 180, 300, 'conc'); P(d, 'groomer', 4, 3760); P(d, 'groomer', 136, 3800); P(d, 'shed', 60, 3900, 1)
    P(d, 'warnsign', 120, 3720)
    H(d, 'thrower', 90, 1500); H(d, 'thrower', 90, 2900)
    return d


def bluerun():
    """BLUE RUN: the first real run. It forks round an island of pines, and skiers come down it."""
    h = 4000; d = job('bluerun', 'BLUE RUN', 'ski', ['snowguns'], h, 76, 14.6, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h); woods(d, 505, dens=0.86)
    pts = [(90, h), (90, 3700), (60, 3350), (118, 2950), (90, 2640), (38, 2460), (38, 2220), (90, 2040), (60, 1700), (118, 1300), (62, 900), (110, 520), (90, 200), (90, 0)]
    i = run(d, pts, 104); poles(d, pts, 104, 15)
    rb = [(90, 2640), (142, 2460), (142, 2220), (90, 2040)]          # the right-hand branch
    carve(d, 76, rb); path(d, 'piste', 72, rb)
    P(d, 'signpost', 82, 2600); P(d, 'trailmap', 76, 2060)
    grade(d, pts, 104, 3800, BLUE, -1); grade(d, pts, 104, 1600, BLUE, 1)
    clearing(d, 0, 3760, 180, 240, 'pave'); P(d, 'trailmap', 20, 3800); P(d, 'skirack', 156, 3790); P(d, 'skirack', 156, 3820)
    clearing(d, 0, 0, 180, 220, 'stone'); P(d, 'hut', 20, 30); P(d, 'deckchair', 120, 40, 0); P(d, 'deckchair', 134, 40, 1); P(d, 'firepit', 60, 120)
    skiers(d, i, 2, 6.0)
    H(d, 'thrower', 90, 1100); H(d, 'thrower', 90, 3000)
    return d


def redrun():
    """RED RUN: steeper and narrower, big switchbacks with rocks on the outside of the turns and three skiers."""
    h = 4200; d = job('redrun', 'RED RUN', 'ski', ['bluerun'], h, 75, 14.8, 7, start=[90, 40])
    G(d, 'grass', 0, 0, 180, h); woods(d, 606, dens=0.88)
    pts = [(90, 0), (90, 160), (48, 500), (132, 900), (48, 1300), (132, 1700), (48, 2100), (132, 2500), (48, 2900), (132, 3300), (70, 3700), (90, 3950), (90, h)]
    i = run(d, pts, 94); poles(d, pts, 94, 16, every=110)
    grade(d, pts, 94, 220, RED, 1); grade(d, pts, 94, 2000, RED, 1)
    for k, (x, y) in enumerate(pts[2:-3]):          # boulders and a warning sign on the outside of each hairpin
        side = -1 if x < 90 else 1
        P(d, 'rock', 2 if side < 0 else 152, y - 8, 22 + (k % 2) * 4)
        if k % 2 == 0: P(d, 'warnsign', 30 if side < 0 else 138, y - 60)
    clearing(d, 0, 0, 180, 170, 'stone'); P(d, 'hut', 140, 20); P(d, 'trailmap', 10, 40)
    clearing(d, 0, 3940, 180, 260, 'pave'); P(d, 'skirack', 4, 4040); P(d, 'skirack', 152, 4040); P(d, 'deckchair', 60, 4120, 0); P(d, 'deckchair', 110, 4120, 2)
    skiers(d, i, 3, 5.0)
    H(d, 'thrower', 90, 1500); H(d, 'thrower', 90, 3100)
    return d


def moguls():
    """MOGUL FIELD: a wide bowl of bumps, cut by the zipper line, with the judges' hut at the top."""
    h = 4000; d = job('moguls', 'MOGUL FIELD', 'ski', ['redrun'], h, 75, 15.0, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h); woods(d, 707, dens=0.86)
    pts = [(90, h), (90, 3700), (70, 3500)]
    run(d, pts, 120)
    clearing(d, 8, 400, 164, 3150, 'piste')
    zz = [(90, 3500), (60, 3200), (120, 2900), (60, 2600), (120, 2300), (60, 2000), (120, 1700), (60, 1400), (120, 1100), (60, 800), (90, 500)]
    for k, y in enumerate(range(560, 3460, 72)):
        cx = cx_at(zz, y)
        for x in ((7, 63, 119) if k % 2 == 0 else (35, 91, 156)):
            if abs(x + 8 - cx) < 34: continue          # keep the zipper line clear
            P(d, 'mogul', x, y)
    i = [v for p in zz for v in p]                          # skiers follow the zipper line
    clearing(d, 0, 0, 180, 420, 'stone'); P(d, 'hut', 82, 30); P(d, 'stand', 0, 120, 60); P(d, 'stand', 120, 120, 60)
    P(d, 'scoreboard', 64, 200); P(d, 'bench', 20, 330); P(d, 'bench', 150, 330); P(d, 'trailmap', 10, 40)
    clearing(d, 0, 3720, 180, 280, 'pave'); P(d, 'skirack', 4, 3800); P(d, 'skirack', 152, 3830); P(d, 'signpost', 40, 3900)
    skiers(d, i, 2, 6.5)
    H(d, 'thrower', 6, 1400); H(d, 'thrower', 160, 2600)
    return d


def slalom():
    """SLALOM COURSE: from the start hut down a fenced race course of gates to the finish arch and the grandstands."""
    h = 4200; d = job('slalom', 'SLALOM COURSE', 'ski', ['moguls'], h, 76, 15.2, 7, start=[90, 40])
    G(d, 'grass', 0, 0, 180, h); woods(d, 808, dens=0.86)
    pts = [(90, 0), (90, 300), (80, 1200), (100, 2200), (82, 3000), (90, 3500)]
    i = run(d, pts, 150)
    clearing(d, 0, 3420, 180, 780, 'piste')
    clearing(d, 0, 0, 180, 300, 'stone'); P(d, 'starthut', 0, 70); P(d, 'flag', 140, 80, 0); P(d, 'flag', 160, 80, 1)
    over(d, 'banner', 40, 240, 100, 9)
    for k, y in enumerate(range(420, 3300, 150)):     # alternating gates
        c = cx_at(pts, y); x = int(c - 52) if k % 2 == 0 else int(c + 4)
        P(d, 'gatepole', x, y, k % 2); P(d, 'gatepole', x + 48, y, k % 2)
    for y in range(500, 3300, 340):
        fence(d, edge(pts, 150, y, -1, -1), y, 120); fence(d, edge(pts, 150, y, 1, 5), y + 170, 120)
    over(d, 'finish', 0, 3460, 180)
    G(d, 'red', 0, 3500, 180, 4)
    P(d, 'stand', 0, 3640, 70); P(d, 'stand', 110, 3640, 70); P(d, 'crowd', 0, 3700, 60); P(d, 'crowd', 120, 3700, 60)
    P(d, 'scoreboard', 64, 3880); P(d, 'stand', 0, 4000, 60); P(d, 'stand', 120, 4000, 60)
    P(d, 'booth', 80, 4120, 2); P(d, 'skirack', 4, 4140); P(d, 'skirack', 152, 4140)
    for y in range(140, 3400, 320): d['data'].setdefault('decor', []).append(['bunting', 0, y, 180])
    skiers(d, i, 2, 6.0, offs=(-30, 30))
    H(d, 'pedx', 40, 3580); H(d, 'pedx', 120, 3800, 1)
    return d


def terrain():
    """TERRAIN PARK (side): kickers, rails and boxes, a halfpipe, the DJ stage and its speakers."""
    h = 3400; d = job('terrain', 'TERRAIN PARK', 'ski', ['slalom'], h, 67, 15.2, 9, start=[90, h - 44], bonus=True)
    G(d, 'piste', 0, 0, 180, h)
    woods(d, 910, 0, h, 0, 14, dens=0.9); woods(d, 911, 0, h, 166, 180, dens=0.9)
    over(d, 'parkgate', 20, 3250, 140)
    for k, y in enumerate(range(2900, 2200, -230)):        # kicker line
        P(d, 'ramp', 24 if k % 2 == 0 else 116, y)
    G(d, 'blue', 52, 1500, 76, 560); dec(d, 'kerb', 52, 1500, 560); dec(d, 'kerb', 126, 1500, 560)   # the halfpipe
    P(d, 'icewallv', 52, 1500, 200); P(d, 'icewallv', 118, 1500, 200); P(d, 'icewallv', 52, 1860, 200); P(d, 'icewallv', 118, 1860, 200)
    for k, y in enumerate(range(1300, 600, -170)):           # the rail garden
        P(d, 'rail', 20 if k % 2 == 0 else 100, y, 60)
    P(d, 'stage', 14, 240, 4); P(d, 'speaker', 100, 250)
    over(d, 'banner', 20, 420, 140, 12)
    P(d, 'booth', 20, 60, 1); P(d, 'booth', 142, 60, 2); P(d, 'flag', 70, 40, 0); P(d, 'flag', 104, 40, 1)
    for y in range(520, 2900, 200): fence(d, 14, y, 150); fence(d, 160, y + 100, 150)
    for k, y in enumerate((3000, 2050, 1450, 520)): over(d, 'banner', 20, y, 140, (12, 13, 12, 13)[k])
    for k, y in enumerate(range(2780, 2280, -250)): P(d, 'rail', 70, y, 40)            # boxes between the kickers
    clear(d, 0, 3200, 180, 200)
    P(d, 'crowd', 16, 3150, 50); P(d, 'crowd', 114, 3150, 50)
    P(d, 'deckchair', 22, 2100, 0); P(d, 'deckchair', 34, 2100, 1); P(d, 'firepit', 140, 2120); P(d, 'deckchair', 148, 2160, 2)
    P(d, 'flag', 20, 1420, 0); P(d, 'flag', 150, 1420, 1); P(d, 'flag', 20, 2090, 1); P(d, 'flag', 150, 2070, 0)
    for k, y in enumerate(range(560, 1100, 180)): P(d, 'mogul', 30 if k % 2 else 130, y)
    for y in (3100, 2100, 1100): H(d, 'pedx', 30, y, (y // 1000) % 2)
    H(d, 'skier', 90, 0, 6.0); H(d, 'thrower', 150, 2600)
    return d


def gondola():
    """GONDOLA TOP: up past the tree line to the rocky ridge, the gondola cabins overhead, the top station and its
    viewing deck."""
    h = 4200; d = job('gondola', 'GONDOLA TOP', 'ski', ['slalom'], h, 75, 15.4, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h)
    woods(d, 1001, 1800, h, dens=0.86)                         # forest below,
    woods(d, 1002, 0, 1800, dens=0.7, kind='rocks', step=11)  # rock above the tree line
    carve(d, 56, [(152, h - 120), (152, 300)]); G(d, 'grass', 124, 300, 56, h - 420)
    over(d, 'gondola', 137, 280, h - 380)
    for y in range(600, h - 200, 500): P(d, 'pylon', 145, y)
    pts = [(90, h), (70, 3800), (70, 3400), (120, 3050), (60, 2700), (110, 2300), (60, 1900), (100, 1500), (60, 1150), (100, 800), (80, 520)]
    i = run(d, pts, 104); poles(d, pts, 104, 17, y0=1800)
    for k, y in enumerate(range(600, 1800, 180)): P(d, 'cairn', int(edge(pts, 104, y, -1 if k % 2 == 0 else 1, 18)), y)
    grade(d, pts, 104, 3900, BLUE, -1); grade(d, pts, 104, 1300, RED, 1)
    clearing(d, 0, 0, 180, 540, 'deck')
    P(d, 'big', 35, 20, SH['GONDOLA']); P(d, 'flag', 4, 30, 0); P(d, 'flag', 164, 30, 1)
    for x in (6, 40, 128, 160): P(d, 'bench', x, 200)
    P(d, 'rail', 0, 470, 60); P(d, 'rail', 120, 470, 60); P(d, 'deckchair', 20, 300, 0); P(d, 'deckchair', 150, 300, 1); P(d, 'trailmap', 74, 300)
    gun(d, pts, 104, 2500, -1); gun(d, pts, 104, 3200, 1)
    skiers(d, i, 2, 6.5)
    H(d, 'pedx', 30, 380); H(d, 'thrower', 90, 1700)
    return d


def apres():
    """APRES-SKI: the party on the terrace: the stage, deckchairs and hot tubs, fire pits, the bar, lights and
    fireworks, with a snowy lane winding through."""
    h = 3600; d = job('apres', 'APRES-SKI', 'ski', ['gondola'], h, 69, 15.6, 7, start=[90, 40])
    G(d, 'grass', 0, 0, 180, h); woods(d, 1101, dens=0.86)
    pts = [(90, 0), (90, 600), (60, 1000), (120, 1500), (90, 1800), (90, 2300), (60, 2700), (120, 3100), (90, h)]
    run(d, pts, 120)
    clearing(d, 0, 0, 180, 640, 'deck')
    P(d, 'big', 0, 70, SH['APRES']); P(d, 'kiosk', 150, 150, 2)
    for k, y in enumerate(range(220, 600, 70)):
        P(d, 'table', 4, y, k % 4); P(d, 'table', 150, y + 30, (k + 2) % 4)
    over(d, 'lights', 0, 160, 180, 3); over(d, 'lights', 0, 420, 180, 1)
    clearing(d, 0, 1700, 180, 700, 'deck')
    P(d, 'stage', 50, 1740, 6); P(d, 'speaker', 134, 1750)
    P(d, 'crowd', 0, 1860, 50); P(d, 'crowd', 130, 1860, 50)
    for k, y in enumerate(range(1960, 2360, 60)):
        P(d, 'deckchair', 4, y, k % 3); P(d, 'deckchair', 18, y, (k + 1) % 3); P(d, 'deckchair', 152, y + 20, (k + 2) % 3); P(d, 'deckchair', 166, y + 20, k % 3)
    P(d, 'firepit', 70, 2120); P(d, 'firepit', 96, 2280); P(d, 'tub', 60, 2350); P(d, 'tub', 110, 2000)
    over(d, 'fireworks', 20, 1680, 0); over(d, 'fireworks', 110, 1690, 2)
    for y in (760, 1000, 1300, 2560, 2800, 3100): P(d, 'lantpost', int(edge(pts, 120, y, -1, 2)), y); P(d, 'lantpost', int(edge(pts, 120, y + 120, 1, 12)), y + 120)
    for y in (880, 1400, 2650, 3200): over(d, 'lant', int(cx_at(pts, y)) - 60, y, 120)
    for y in (1150, 2950): P(d, 'tub', int(edge(pts, 120, y, -1, 0)), y); P(d, 'firepit', int(edge(pts, 120, y + 60, 1, 16)), y + 60)
    clearing(d, 0, 3300, 180, 300, 'pave'); P(d, 'foodtruck', 4, 3360); P(d, 'foodtruck', 150, 3380, 2); P(d, 'skirack', 70, 3540); P(d, 'skirack', 96, 3540)
    for y in (300, 2000, 2240): H(d, 'pedx', 40, y, (y // 100) % 2)
    H(d, 'thrower', 90, 1200); H(d, 'thrower', 90, 2900); H(d, 'dog', 100, 3400)
    return d


def snowshoe():
    """SNOWSHOE TRAIL (side): a narrow trail through deep forest, over a wooden bridge and round a frozen pond."""
    h = 3600; d = job('snowshoe', 'SNOWSHOE TRAIL', 'ski', ['apres'], h, 68, 15.6, 9, start=[90, h - 44], bonus=True)
    G(d, 'grass', 0, 0, 180, h); woods(d, 1201, dens=0.92, step=8)
    pts = [(90, h), (90, 3400), (40, 3100), (40, 2800), (140, 2500), (140, 2200), (60, 1900), (50, 1500), (130, 1200), (130, 900), (50, 600), (90, 300), (90, 0)]
    carve(d, 72, pts); path(d, 'gravel', 30, pts)
    # the frozen pond, half way, and the stream with its bridge
    carve(d, 150, [(90, 1700), (90, 1720)]); C(d, 'ice', 90, 1710, 52); P(d, 'reed', 40, 1650); P(d, 'reed', 130, 1760)
    G(d, 'ice', 0, 2645, 180, 30); G(d, 'wood', 62, 2636, 56, 48); P(d, 'snowpole', 60, 2622); P(d, 'snowpole', 116, 2672)
    for k, y in enumerate(range(400, 3400, 500)): P(d, 'signpost' if k % 2 == 0 else 'cairn', int(edge(pts, 72, y, -1, -10)) if k % 2 else int(edge(pts, 72, y, 1, 0)) - 6, y)
    carve(d, 120, [(90, 140), (90, 200)]); P(d, 'cabin', 68, 80); P(d, 'firepit', 40, 200); P(d, 'bench', 130, 200)
    H(d, 'dog', 60, 1700); H(d, 'dog', 120, 2400); H(d, 'thrower', 60, 1000); H(d, 'thrower', 120, 3100)
    return d


def blackrun():
    """BLACK RUN: steep, narrow and icy, between rocks; skiers and loose boulders come down the line."""
    h = 4400; d = job('blackrun', 'BLACK RUN', 'ski', ['apres'], h, 80, 15.8, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h)
    woods(d, 1301, 2400, h, dens=0.9); woods(d, 1302, 0, 2400, dens=0.75, kind='rocks', step=10)
    pts = [(90, h), (90, 4150), (50, 3850), (130, 3500), (50, 3150), (130, 2800), (50, 2450), (130, 2100), (50, 1750), (130, 1400), (50, 1050), (130, 700), (90, 420), (90, 0)]
    i = run(d, pts, 92)
    for k, (x, y) in enumerate(pts[3:-3]):
        G(d, 'ice', int(x) - 20, int(y) - 140, 40, 90)            # sheet ice on the steep bits
        if k % 2: P(d, 'warnsign', int(edge(pts, 92, y - 40, -1 if x > 90 else 1, 16)), int(y) - 40)
    poles(d, pts, 92, 18, every=100)
    grade(d, pts, 92, 4200, BLACK, -1); grade(d, pts, 92, 2000, BLACK, 1)
    clearing(d, 0, 4160, 180, 240, 'pave'); P(d, 'hut', 10, 4200); P(d, 'trailmap', 140, 4220)
    clearing(d, 0, 0, 180, 440, 'stone'); P(d, 'hut', 82, 30); P(d, 'flag', 30, 40, 0); P(d, 'flag', 140, 40, 1); P(d, 'warnsign', 40, 300)
    skiers(d, i, 3, 5.0)
    H(d, 'rockfall', 90, 0, 9.0, i); H(d, 'thrower', 90, 3000)
    return d


def glacier():
    """GLACIER: high above the trees, the ice field split by crevasses and seracs, the rescue helicopter on its pad."""
    h = 4400; d = job('glacier', 'GLACIER', 'ski', ['blackrun'], h, 79, 16.0, 7, start=[90, 40])
    G(d, 'ice', 0, 0, 180, h); G(d, 'stone', 0, 0, 180, 600); G(d, 'piste', 0, 600, 180, 3460); G(d, 'stone', 0, 4060, 180, 340)
    # rock walls down both sides, wider in places, so the field narrows and opens
    for k, y in enumerate(range(600, 4060, 220)):
        wl = (14, 30, 20, 40, 12, 26)[k % 6]; wr = (26, 12, 38, 18, 30, 14)[k % 6]
        wild(d, 'rocks', 0, y, wl, 220, 1400 + k, 0.8, 10); wild(d, 'rocks', 180 - wr, y, wr, 220, 1450 + k, 0.8, 10)
    C(d, 'conc', 44, 150, 36); dec(d, 'heli', 44 - 32, 150 - 32, 32); P(d, 'heli', 22, 122); P(d, 'hut', 120, 40); P(d, 'flag', 160, 120, 0); P(d, 'signpost', 120, 200)
    P(d, 'rock', 0, 300, 26); P(d, 'rock', 154, 420, 26); P(d, 'cairn', 70, 480)
    for k, y in enumerate(range(800, 3900, 340)):                  # seracs and crevasse bands
        x = (40, 100, 70)[k % 3]
        wild(d, 'ice', x, y, 40, 56, 1410 + k, 0.85, 10)
        G(d, 'ice', 0, y + 150, 180, 26)
        P(d, 'iceblock', (x + 84) % 150 + 4, y + 26, 14 + (k % 3) * 4)
    zz = [(130, 560), (130, 900), (50, 1100), (50, 1250), (140, 1450), (140, 1560), (130, 1900), (50, 2120), (50, 2260), (140, 2480),
          (140, 2580), (130, 2950), (50, 3150), (50, 3280), (140, 3500), (140, 3600), (130, 3950), (90, 4100)]
    i = [v for p in zz for v in p]
    P(d, 'cabin', 68, 4300); P(d, 'cairn', 30, 4150); P(d, 'cairn', 140, 4170); P(d, 'trailmap', 120, 4100)
    H(d, 'cannon', 42, 1500, 0.35, 7.0, 64); H(d, 'cannon', 120, 2700, 2.79, 7.0, 64)
    skiers(d, i, 1, 7.0); H(d, 'rockfall', 90, 0, 10.0, i)
    H(d, 'thrower', 90, 2000)
    return d


def grandslalom():
    """THE GRAND SLALOM (boss): the big race. From the finish arena with its grandstands up the whole course of gates to
    the start, with snow guns, racers, and the runaway snowball."""
    h = 4600; d = job('grandslalom', 'THE GRAND SLALOM', 'ski', ['glacier'], h, 80, 16.6, 9, start=[90, h - 44], boss=True)
    G(d, 'grass', 0, 0, 180, h); woods(d, 1501, dens=0.86)
    pts = [(90, h), (90, 3800), (70, 3300), (110, 2800), (70, 2300), (110, 1800), (70, 1300), (110, 800), (90, 400), (90, 0)]
    i = run(d, pts, 140)
    clearing(d, 0, 3780, 180, 820, 'piste')
    over(d, 'finish', 0, 3800, 180); G(d, 'red', 0, 3840, 180, 4)
    P(d, 'stand', 0, 3980, 70); P(d, 'stand', 110, 3980, 70); P(d, 'crowd', 0, 4040, 60); P(d, 'crowd', 120, 4040, 60)
    P(d, 'scoreboard', 64, 4200); P(d, 'stand', 0, 4300, 60); P(d, 'stand', 120, 4300, 60); P(d, 'booth', 80, 4460, 2)
    over(d, 'banner', 20, 3920, 140, 14)
    for k, y in enumerate(range(500, 3700, 160)):
        c = cx_at(pts, y); x = int(c - 50) if k % 2 == 0 else int(c + 2)
        P(d, 'gatepole', x, y, k % 2); P(d, 'gatepole', x + 48, y, k % 2)
    for y in range(140, 3700, 300): d['data'].setdefault('decor', []).append(['bunting', 0, y, 180])
    clearing(d, 0, 0, 180, 400, 'stone'); P(d, 'starthut', 60, 30)
    P(d, 'flag', 10, 60, 0); P(d, 'flag', 160, 60, 1); P(d, 'trailmap', 10, 300)
    for k, y in enumerate(range(900, 3500, 800)): gun(d, pts, 140, y, -1 if k % 2 == 0 else 1, 7.5, 60)
    skiers(d, i, 2, 5.5, offs=(-30, 30))
    H(d, 'chaser', 90, 3560, 'snowball', 5)
    return d


ALL = [skischool, chalets, lift, snowguns, bluerun, redrun, moguls, slalom, terrain, gondola, apres, snowshoe, blackrun, glacier, grandslalom]
