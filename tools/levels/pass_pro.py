"""Mountain Pass, pro pass. A real mountain road: rock faces everywhere, the road carved through them with gravel
shoulders, a dashed centre line, marker poles, hairpin stacks with chevrons and guard rails, snow-shed galleries and
tunnels overhead, rockfall nets, avalanche fences and blasters. Shop names: 50 MOUNTAIN HUT 51 WEATHER STATION."""
import math
from common import *

SH = dict(HUT=50, WEATHER=51)


# ------------------------------------------------------------------ helpers
def cx_at(pts, y):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        lo, hi = min(ay, by), max(ay, by)
        if lo <= y <= hi and hi > lo: return ax + (bx - ax) * (y - ay) / (by - ay)
    return min(pts, key=lambda p: abs(p[1] - y))[0]


def rocky(d, seed, y0=0, y1=None, x0=0, x1=180, dens=0.8, kind='rocks', step=10):
    wild(d, kind, x0, y0, x1 - x0, (d['h'] if y1 is None else y1) - y0, seed, dens, step)


def dash(d, pts, t='wht'):
    """a dashed centre line along a polyline (painted by the game: 10 on, 12 off)"""
    path(d, '~' + t, 2, pts)


def road(d, pts, w=84, sh=11, dashes=True):
    """the road: a carve through the rock, gravel shoulders, tarmac and a dashed centre line; returns the carve index"""
    carve(d, w + 2 * sh, pts); path(d, 'gravel', w + 2 * sh - 2, pts); path(d, 'asph', w, pts)
    if dashes: dash(d, pts)
    return len(d['data']['carves']) - 1


def hairpins(x0, x1, y0, n, gap):
    """a stack of n horizontal legs joined by tight turns, climbing from y0 (first leg runs x0 -> x1)"""
    pts = []; y = y0
    for k in range(n):
        a, b = (x0, x1) if k % 2 == 0 else (x1, x0)
        pts += [(a, y), (b, y)]; y -= gap
    return pts


def dress_hairpins(d, pts, gap, w=106, rails=True):
    """chevrons on the outside of every turn and a guard rail on the downhill edge of every leg"""
    legs = [(pts[i], pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
    for k, ((ax, ay), (bx, by)) in enumerate(legs):
        if k < len(legs) - 1:
            P(d, 'chevron', 2 if bx < 90 else 160, int(by - gap / 2) - 18, 0 if bx < 90 else 1)
        if rails and k > 0:
            if ax > 90: P(d, 'rail', 6, int(ay + w / 2), int(ax - w / 2 - 12))
            else: P(d, 'rail', int(ax + w / 2 + 6), int(ay + w / 2), int(174 - ax - w / 2 - 6))
        if k % 2 == 1: P(d, 'warnsign', int((ax + bx) / 2) - 7, int(ay - w / 2) - 19)


def poles(d, pts, w, seed, every=130):
    """orange-topped snow poles down both road edges"""
    r = rng(seed); k = 0
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 120: continue
        nx, ny = -(by - ay) / L, (bx - ax) / L; t = 50
        while t < L - 50:
            cx, cy = ax + (bx - ax) * t / L, ay + (by - ay) * t / L; s = -1 if k % 2 == 0 else 1
            x = cx + s * nx * (w / 2 - 1) - 2; y = cy + s * ny * (w / 2 - 1) - 15
            if 2 <= x <= 174: P(d, 'snowpole', int(x), int(y))
            k += 1; t += every + r.randint(-12, 12)


def layby(d, x, y, w, h, t='asph', bays=True):
    """a widened parking area off the road"""
    clear(d, x, y, w, h, t)
    if bays:
        for yy in range(y + 6, y + h - 30, 34): dec(d, 'bay', x + 2, yy, 28, 32)


# ------------------------------------------------------------------ the fifteen jobs
def hairpin():
    """HAIRPIN BEND: out of the pines, up the first stack of hairpins, chevrons on every turn, rocks rolling down."""
    h = 4000; d = job('hairpin', 'HAIRPIN BEND', 'pass', ['grandslalom'], h, 75, 17.0, 7, start=[90, h - 44])
    G(d, 'stone', 0, 0, 180, h)
    wild(d, 'forest', 0, 2700, 180, 1300, 1601, 0.86, 9); rocky(d, 1602, 0, 2700)
    low = [(90, h), (90, 3720), (60, 3400), (110, 3060), (40, 2760)]
    hp = hairpins(40, 140, 2760, 9, 176)
    top = [hp[-1], (90, 1150), (90, 200)]
    pts = low + hp[1:] + top[1:]
    road(d, pts); dress_hairpins(d, hp, 176)
    poles(d, low, 106, 1); poles(d, top, 106, 2)
    layby(d, 0, 0, 180, 220, 'asph', bays=False); P(d, 'shelter', 6, 40); P(d, 'signpost', 150, 60); P(d, 'warnsign', 120, 180)
    for x in (60, 120): H(d, 'rockfall', x, 0, 6.0 + x / 60)
    H(d, 'thrower', 120, 1600)
    return d


def snowshed():
    """SNOW SHED: down a sheer face where the road dives under three concrete avalanche galleries."""
    h = 4000; d = job('snowshed', 'SNOW SHED', 'pass', ['hairpin'], h, 72, 17.3, 7, start=[90, 40])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 1701)
    pts = [(90, 0), (90, 160), (56, 420), (56, 1100), (124, 1400), (124, 2100), (56, 2400), (56, 3100), (124, 3400), (124, 3700), (90, 3880), (90, h)]
    i = road(d, pts)
    for x, y0, y1 in ((56, 520, 1040), (124, 1500, 2040), (56, 2500, 3040)):
        over(d, 'shed', x - 53, y0, 106, y1 - y0)
        G(d, 'conc', x - 42, y0, 84, y1 - y0)
        wild(d, 'ice', 0 if x > 90 else x + 53, y0 + 40, (x - 53) if x > 90 else 180 - x - 53, 140, y0, 0.55, 12)   # the avalanche gully above
    for x, y in ((90, 260), (90, 1250), (90, 2250), (90, 3250)): P(d, 'warnsign', x - 7, y)
    layby(d, 0, 3880, 180, 120, 'asph', bays=False); P(d, 'van', 4, 3900, 2); P(d, 'skip', 150, 3920)
    H(d, 'cannon', 2, 1300, 0.35, 7.0, 64); H(d, 'cannon', 160, 2300, 2.79, 7.0, 64)
    H(d, 'rockfall', 90, 0, 7.0, i); H(d, 'pedx', 40, 3940)
    return d


def tunnel():
    """TUNNEL MOUTH: road works, the traffic lights, and two long tunnels through the mountain."""
    h = 4000; d = job('tunnel', 'TUNNEL MOUTH', 'pass', ['snowshed'], h, 71, 17.6, 7, start=[90, h - 44])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 1801)
    pts = [(90, h), (90, 3500), (70, 3200), (70, 2300), (110, 2000), (110, 1100), (90, 800), (90, 0)]
    i = road(d, pts)
    for x, y0, y1 in ((70, 2340, 3160), (110, 1140, 1960)):
        over(d, 'tunnel', x - 56, y0, 112, y1 - y0)
        P(d, 'tlight', x + 50, y1 + 14); P(d, 'tlight', x - 57, y0 - 40)
    # road works below the first tunnel: cones and a works lorry on the shoulder
    P(d, 'works', 46, 3520, 30); P(d, 'cone', 48, 3480); P(d, 'cone', 66, 3486); P(d, 'warnsign', 120, 3620)
    clear(d, 0, 3780, 180, 220, 'asph'); P(d, 'busstop', 4, 3800); P(d, 'skip', 150, 3820)
    clear(d, 0, 0, 180, 300, 'asph'); P(d, 'shelter', 6, 60); P(d, 'van', 150, 40, 0); P(d, 'signpost', 70, 220)
    for x, y in ((150, 600), (8, 1500), (150, 2700)): P(d, 'snowpole', x, y)
    H(d, 'rockfall', 90, 0, 7.5, i); H(d, 'thrower', 90, 600)
    return d


def rockfall():
    """ROCKFALL ROAD: along the foot of the cliffs, nets on the rock, boulders already on the road, more coming."""
    h = 4200; d = job('rockfall', 'ROCKFALL ROAD', 'pass', ['tunnel'], h, 72, 17.9, 7, start=[90, 40])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 1901, dens=0.85)
    pts = [(96, 0), (96, 300), (110, 800), (90, 1400), (114, 2000), (92, 2600), (110, 3200), (96, 3800), (96, h)]
    i = road(d, pts, w=74, sh=14)
    for y in range(200, h - 200, 300):              # rockfall nets down the cliff on the left
        x = int(cx_at(pts, y) - 52); P(d, 'rocknet', max(0, x - 8), y, 240)
    for k, y in enumerate(range(500, h - 300, 420)):  # boulders that already came down
        sz = 18 + (k % 3) * 3; P(d, 'rock', int(cx_at(pts, y)) - 51 if k % 2 == 0 else int(cx_at(pts, y)) + 51 - sz, y, sz)
    for y in range(350, h, 700): P(d, 'warnsign', int(cx_at(pts, y) + 42), y)
    P(d, 'works', 70, 2300, 40); P(d, 'cone', 72, 2270); P(d, 'cone', 104, 2272)
    for k in range(3): H(d, 'rockfall', 90 + (-20, 0, 20)[k], 0, 5.0 + k * 0.8, i)
    H(d, 'thrower', 110, 1700)
    return d


def mhut():
    """MOUNTAIN HUT: up through the last trees to the hut on its stone terrace, by the frozen tarn."""
    h = 3800; d = job('mhut', 'MOUNTAIN HUT', 'pass', ['rockfall'], h, 67, 18.2, 7, start=[90, h - 44])
    G(d, 'stone', 0, 0, 180, h)
    wild(d, 'forest', 0, 1800, 180, 2000, 2001, 0.86, 9); rocky(d, 2002, 0, 1800)
    pts = [(90, h), (90, 3500), (50, 3100), (130, 2700), (60, 2300), (110, 1900), (110, 1500), (60, 1150), (90, 800), (90, 500)]
    road(d, pts, w=76, sh=10); poles(d, pts, 96, 3)
    clear(d, 0, 0, 180, 560, 'stone'); C(d, 'ice', 140, 380, 34)
    P(d, 'big', 0, 30, SH['HUT']); P(d, 'flag', 124, 30, 0); P(d, 'flag', 150, 30, 1)
    for x in (10, 36, 62): P(d, 'bench', x, 140)
    P(d, 'firepit', 90, 180); P(d, 'crate', 120, 120); P(d, 'crate', 120, 134); P(d, 'signpost', 20, 480); P(d, 'trailmap', 60, 470)
    P(d, 'reed', 110, 360); P(d, 'reed', 168, 410); P(d, 'snowman', 40, 300)
    for k, y in enumerate(range(700, 1800, 220)): P(d, 'cairn', int(cx_at(pts, y)) + (28 if k % 2 else -42), y)
    H(d, 'dog', 90, 300); H(d, 'pedx', 30, 260); H(d, 'pedx', 120, 3400, 1); H(d, 'thrower', 90, 2100)
    return d


def avalanche():
    """AVALANCHE FENCES: a huge open slope barred with rows of steel fences, blasters on the ridges. Whiteouts."""
    h = 4000; d = job('avalanche', 'AVALANCHE FENCES', 'pass', ['mhut'], h, 73, 18.5, 7, start=[90, 40], squall=1)
    G(d, 'stone', 0, 0, 180, h)
    for k, y in enumerate(range(0, h, 250)):        # rock ribs down both sides, uneven
        wl = (16, 24, 10, 20)[k % 4]; wr = (22, 12, 24, 14)[k % 4]
        rocky(d, 2100 + k, y, y + 250, 0, wl); rocky(d, 2150 + k, y, y + 250, 180 - wr, 180)
    for k, y in enumerate(range(260, h - 260, 150)):  # fence rows, staggered, gaps on alternate sides
        if k % 2 == 0: P(d, 'avfence', 0, y, 96)
        else: P(d, 'avfence', 84, y, 96)
    clear(d, 0, 0, 180, 200, 'stone'); P(d, 'shed', 120, 20, 1); P(d, 'warnsign', 30, 120)
    clear(d, 0, 3820, 180, 180, 'stone'); P(d, 'hut', 82, 3900); P(d, 'signpost', 20, 3880)
    for y in (900, 2000, 3100): H(d, 'cannon', 18, y, 0.35, 7.5, 70)
    for y in (1450, 2550): H(d, 'cannon', 144, y, 2.79, 7.5, 70)
    H(d, 'rockfall', 150, 0, 6.0); H(d, 'rockfall', 40, 0, 7.5)
    return d


def weather():
    """WEATHER STATION: the road to the summit observatory: radar dome, masts, solar panels and a windsock."""
    h = 3800; d = job('weather', 'WEATHER STATION', 'pass', ['avalanche'], h, 71, 18.8, 7, start=[90, h - 44])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 2201)
    pts = [(90, h), (90, 3400), (130, 3000), (50, 2500), (130, 2000), (50, 1500), (110, 1000), (90, 700)]
    i = road(d, pts); poles(d, pts, 106, 4)
    clear(d, 0, 0, 180, 740, 'conc')
    P(d, 'big', 35, 0, SH['WEATHER']); P(d, 'radar', -4, 4); P(d, 'radar', 148, 10)
    P(d, 'mast', 4, 140); P(d, 'mast', 158, 150); P(d, 'flag', 84, 120, 1)
    for k, y in enumerate(range(260, 600, 50)): P(d, 'solar', 4, y); P(d, 'solar', 146, y + 20)
    P(d, 'container', 60, 300, 2); P(d, 'container', 60, 470, 4); P(d, 'van', 112, 560, 3)
    for k, y in enumerate(range(1100, 3300, 300)):     # snow-depth survey stakes off the road
        P(d, 'snowpole', int(cx_at(pts, y)) + (34 if k % 2 else -38), y)
    H(d, 'cannon', 2, 1800, 0.35, 7.0, 64); H(d, 'rockfall', 90, 0, 8.0, i); H(d, 'pedx', 40, 650)
    return d


def waterfall():
    """FROZEN WATERFALL (side): up the gorge beside the frozen river, past the icefalls, over the footbridges."""
    h = 3400; d = job('waterfall', 'FROZEN WATERFALL', 'pass', ['weather'], h, 67, 18.8, 9, start=[90, h - 44], bonus=True)
    G(d, 'stone', 0, 0, 180, h); rocky(d, 2301, x0=0, x1=24); rocky(d, 2302, x0=156, x1=180)
    G(d, 'ice', 70, 0, 40, h)                                 # the frozen river down the middle
    for k, y in enumerate(range(300, h - 300, 500)):          # icefalls: a step of ice with spires
        P(d, 'icewall', 24, y, 34); P(d, 'icewall', 122, y, 34)
        P(d, 'spire', 30 if k % 2 else 134, y - 40); P(d, 'iceblock', 40 if k % 2 == 0 else 124, y + 60, 16)
        G(d, 'wood', 70, y + 180, 40, 20)                       # a footbridge deck
    for y in range(500, h - 200, 600): P(d, 'cairn', 30, y); P(d, 'signpost', 134, y + 300)
    clear(d, 0, 3200, 180, 200, 'stone'); P(d, 'hut', 8, 3240); P(d, 'bench', 150, 3260)
    H(d, 'thrower', 40, 1500); H(d, 'dog', 120, 2400); H(d, 'rockfall', 40, 0, 7.0)
    return d


def viewpoint():
    """VIEWPOINT: the big lay-by at the top with its telescopes, kiosk and parked cars pulling out, then down the road."""
    h = 3800; d = job('viewpoint', 'VIEWPOINT', 'pass', ['weather'], h, 68, 19.1, 7, start=[90, 40])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 2401)
    clear(d, 0, 0, 180, 980, 'asph')
    for y in range(80, 900, 120):
        for x in range(4, 176, 30): G(d, 'wht', x, y, 2, 40)
    d['data']['pull'] += [[8, 200, 1], [128, 440, 3], [68, 680, 0]]
    P(d, 'car', 38, 92, 2); P(d, 'car', 98, 212, 4); P(d, 'car', 8, 572, 0); P(d, 'car', 158, 812, 1)
    P(d, 'stonewall', 0, 962, 36); P(d, 'stonewall', 144, 962, 36); P(d, 'kiosk', 154, 20, 2); P(d, 'trailmap', 120, 10)
    for x in (10, 36): P(d, 'statue', x, 940)
    pts = [(90, 960), (90, 1200), (130, 1700), (50, 2300), (130, 2900), (90, 3400), (90, h)]
    i = road(d, pts); poles(d, pts, 106, 5)
    clear(d, 0, 2050, 52, 300, 'asph'); P(d, 'bench', 4, 2120); P(d, 'bench', 4, 2200); P(d, 'statue', 30, 2160)   # a second lookout
    clear(d, 0, 3500, 180, 300, 'asph'); P(d, 'busstop', 4, 3560); P(d, 'van', 150, 3600, 0)
    H(d, 'pedx', 60, 300); H(d, 'pedx', 120, 620, 1); H(d, 'rockfall', 90, 0, 8.0, i)
    return d


def gorge():
    """BRIDGE GORGE: the road crosses the gorge three times on narrow bridges, the frozen river far below."""
    h = 4000; d = job('gorge', 'BRIDGE GORGE', 'pass', ['viewpoint'], h, 71, 19.4, 7, start=[90, h - 44])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 2501)
    pts = [(90, h), (90, 3600), (60, 3300), (120, 2900), (120, 2500), (60, 2100), (60, 1700), (120, 1300), (120, 900), (90, 500), (90, 0)]
    i = road(d, pts)
    for yc in (2630, 1830, 1030):                  # the gorges: frozen river below, deck and parapets across
        c = int(cx_at(pts, yc + 70))
        G(d, 'ice', 0, yc, 180, 140)
        wild(d, 'ice', 0, yc, max(0, c - 53), 140, yc, 0.6, 12); wild(d, 'ice', c + 53, yc, max(0, 127 - c), 140, yc + 1, 0.6, 12)
        G(d, 'wood', c - 44, yc, 88, 140); P(d, 'railv', c - 50, yc, 140); P(d, 'railv', c + 45, yc, 140)
        P(d, 'warnsign', min(160, c + 50), yc + 150)
    clear(d, 0, 0, 180, 200, 'asph'); P(d, 'shelter', 6, 40); P(d, 'signpost', 150, 60)
    H(d, 'rockfall', 90, 0, 6.5, i); H(d, 'thrower', 90, 2500)
    return d


def switchbacks():
    """SWITCHBACKS: the great staircase of hairpins up the mountainside."""
    h = 4400; d = job('switchbacks', 'SWITCHBACKS', 'pass', ['gorge'], h, 77, 19.7, 7, start=[90, 40])
    G(d, 'stone', 0, 0, 180, h); rocky(d, 2601)
    hp = hairpins(40, 140, 4220, 23, 172)
    pts = [(90, h)] + [(40, 4220)] + hp[1:] + [(90, 0)]
    road(d, pts); dress_hairpins(d, hp, 172)
    clear(d, 0, 0, 180, 160, 'asph')
    P(d, 'signpost', 150, 40); P(d, 'shelter', 6, 40)
    for x in (40, 140, 90): H(d, 'rockfall', x, 0, 6.0 + x / 70)
    return d


def icecaves():
    """ICE CAVES (side): blue passages and chambers in the glacier, icicles and seracs, slippery underfoot."""
    h = 3400; d = job('icecaves', 'ICE CAVES', 'pass', ['switchbacks'], h, 68, 19.7, 9, start=[90, h - 44], bonus=True)
    G(d, 'ice', 0, 0, 180, h); wild(d, 'ice', 0, 0, 180, h, 2701, 0.85, 9)
    main = [(90, h), (90, 3100), (50, 2800), (50, 2400), (130, 2000), (130, 1600), (60, 1200), (60, 800), (110, 500), (90, 200), (90, 0)]
    carve(d, 84, main)
    for c in ((90, 2600, 70), (90, 1400, 60), (90, 400, 60)): carve(d, c[2] * 2, [(c[0] - 30, c[1]), (c[0] + 30, c[1])])   # chambers
    carve(d, 64, [(50, 2600), (140, 2700), (140, 3000)]); carve(d, 64, [(130, 1800), (30, 1800), (30, 1500)])            # side passages
    for k, (x, y) in enumerate(((60, 2560), (110, 2640), (70, 1380), (120, 1420), (60, 380), (118, 420))):
        P(d, 'spire', x, y) if k % 2 == 0 else P(d, 'iceblock', x, y, 18)
    G(d, 'blue', 0, 0, 180, 140); clear(d, 0, 0, 180, 140)
    H(d, 'thrower', 90, 2600); H(d, 'dog', 90, 1400)
    return d


def cliffroad():
    """CLIFF ROAD: a ledge cut into the cliff: rock wall and nets on one side, a guard rail and the drop on the other."""
    h = 4400; d = job('cliffroad', 'CLIFF ROAD', 'pass', ['switchbacks'], h, 74, 20.0, 7, start=[90, h - 44])
    G(d, 'stone', 0, 0, 180, h)
    pts = [(80, h), (80, 3800), (60, 3300), (96, 2700), (60, 2100), (96, 1500), (64, 900), (80, 400), (80, 0)]
    i = road(d, pts, w=78, sh=8)
    rocky(d, 2801, x0=0, x1=90, dens=0.85); G(d, 'ice', 90, 0, 90, h); wild(d, 'ice', 90, 0, 90, h, 2802, 0.45, 12)
    for y in range(80, h - 100, 80):               # the drop: an icy void down the right, the guard rail just outside the road
        e = max(cx_at(pts, yy) for yy in range(y, y + 81, 4)) + 47
        P(d, 'railv', int(math.ceil(e)), y, 80)
    for y in range(160, h - 200, 280):            # rockfall nets on the wall, just outside the road
        e = min(cx_at(pts, yy) for yy in range(y, y + 241, 4)) - 47
        P(d, 'rocknet', max(0, int(e) - 8), y, 240)
    for k, y in enumerate(range(600, h - 400, 600)): P(d, 'rock', int(cx_at(pts, y)) - 24, y, 16)
    clear(d, 0, 4200, 180, 200, 'asph'); P(d, 'shelter', 140, 4240); P(d, 'warnsign', 20, 4220)
    clear(d, 0, 0, 180, 160, 'asph'); P(d, 'signpost', 140, 40)
    for k in range(2): H(d, 'rockfall', 90 + (-16, 16)[k], 0, 4.8 + k, i)
    H(d, 'rockfall', 40, 0, 6.5)
    return d


def summit():
    """SUMMIT PASS: the saddle at the top of the pass: the summit sign and cairn, prayer flags, the old hospice; the
    road across the snowfield marked only by poles. Whiteouts."""
    h = 4400; d = job('summit', 'SUMMIT PASS', 'pass', ['cliffroad'], h, 78, 20.4, 7, start=[90, 40], squall=1)
    G(d, 'stone', 0, 0, 180, h)
    for k, y in enumerate(range(0, h, 300)):
        wl = (16, 28, 10, 22, 34)[k % 5]; wr = (24, 12, 30, 18, 8)[k % 5]
        rocky(d, 2900 + k, y, y + 300, 0, wl); rocky(d, 2950 + k, y, y + 300, 180 - wr, 180)
    pts = [(90, 0), (90, 600), (70, 1400), (110, 2200), (70, 3000), (100, 3800), (90, h)]
    path(d, 'asph', 64, pts); dash(d, pts)
    for y in range(150, h - 50, 110):                 # the poles that mark the buried road
        c = cx_at(pts, y); P(d, 'snowpole', int(c - 40), y); P(d, 'snowpole', int(c + 36), y + 55)
    clear(d, 0, 1900, 180, 500)
    P(d, 'passsign', -6, 1950); P(d, 'cairn', 150, 1980); P(d, 'cairn', 146, 2140)
    for y in (2020, 2300): d['data'].setdefault('decor', []).append(['bunting', 0, y, 180])
    P(d, 'cabin', 4, 3400); P(d, 'flag', 150, 3420, 0); P(d, 'bench', 60, 3440)
    for y in (700, 2800): P(d, 'signpost', 150, y)
    H(d, 'rockfall', 90, 0, 6.0); H(d, 'cannon', 18, 1200, 0.35, 7.0, 64); H(d, 'cannon', 144, 3000, 2.79, 7.0, 64); H(d, 'dog', 90, 2200)
    return d


def blizzard():
    """THE BLIZZARD PASS (boss): the whole pass in a storm: galleries, a tunnel, a stack of hairpins, the summit, and
    the Yeti on your tail."""
    h = 4800; d = job('blizzard', 'THE BLIZZARD PASS', 'pass', ['summit'], h, 78, 21.0, 9, start=[90, h - 44], boss=True, squall=1)
    G(d, 'stone', 0, 0, 180, h); rocky(d, 3001)
    low = [(90, h), (90, 4300), (56, 4000), (56, 3500), (124, 3200), (124, 2700), (40, 2440)]
    hp = hairpins(40, 140, 2440, 8, 176)
    top = [hp[-1], (90, 800), (90, 0)]
    pts = low + hp[1:] + top[1:]
    road(d, pts); dress_hairpins(d, hp, 176)
    over(d, 'shed', 56 - 53, 3560, 106, 400); G(d, 'conc', 56 - 42, 3560, 84, 400)
    over(d, 'tunnel', 124 - 56, 2760, 112, 400); P(d, 'tlight', 124 + 46, 3180)
    clear(d, 0, 0, 180, 420, 'stone'); P(d, 'passsign', 52, 60); P(d, 'cairn', 10, 200); P(d, 'cairn', 156, 220)
    d['data'].setdefault('decor', []).append(['bunting', 0, 160, 180])
    for x in (60, 120): H(d, 'rockfall', x, 0, 5.5 + x / 60)
    H(d, 'cannon', 2, 3800, 0.35, 7.0, 64); H(d, 'chaser', 100, 4500, 'yeti', 5)
    return d


ALL = [hairpin, snowshed, tunnel, rockfall, mhut, avalanche, weather, waterfall, viewpoint, gorge, switchbacks, icecaves, cliffroad, summit, blizzard]
