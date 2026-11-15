"""The Frozen North, pro pass (the finale). Taiga and tundra, a frozen bay, the research base, the aurora, then
Santa's country: the North Pole Post, the palace gardens, the gates, the Great Hall and the Ice Palace itself.
Shop names: 52 RESEARCH BASE 53 ICE PALACE 54 POST OFFICE."""
import math
from common import *
from ski_pro import cx_at, edge, woods, run

SH = dict(BASE=52, PALACE=53, POST=54)


def lane(d, yc, dirn, per=5.0, t='piste'):
    """a dog-sled lane straight across, cleared through whatever is there, flags at both ends"""
    clear(d, 0, yc - 24, 180, 56, t)
    P(d, 'flag', 2, yc - 30, 0); P(d, 'flag', 166, yc - 30, 1)
    H(d, 'cross', 0, yc, dirn, per, 'sled')


def igloo_ring(d, cx, cy, r, n, start=0):
    for k in range(n):
        a = start + k * 2 * math.pi / n
        P(d, 'igloo', int(cx + r * math.cos(a) - 15), int(cy + r * math.sin(a) - 14))


def icy_band(d, y, h, gap_x, gap_w, seed):
    """a pressure ridge of ice boulders across the field with one gap"""
    if gap_x > 0: wild(d, 'ice', 0, y, gap_x, h, seed, 0.9, 8)
    if gap_x + gap_w < 180: wild(d, 'ice', gap_x + gap_w, y, 180 - gap_x - gap_w, h, seed + 1, 0.9, 8)


# ------------------------------------------------------------------ the fifteen jobs
def huskies():
    """HUSKY CAMP: the expedition camp in the taiga: tents, kennels and sleds; the trail north crosses the sled
    race lanes."""
    h = 4000; d = job('huskies', 'HUSKY CAMP', 'north', ['blizzard'], h, 74, 21.6, 7, start=[90, h - 44])
    G(d, 'grass', 0, 0, 180, h); woods(d, 3101, dens=0.86)
    clear(d, 0, 3300, 180, 700, 'piste')
    for k, (x, y) in enumerate(((6, 3330), (44, 3340), (130, 3330), (6, 3420), (146, 3430))): P(d, 'tent', x, y, k % 3)
    for y in range(3520, 3940, 34): P(d, 'kennel', 2, y); P(d, 'kennel', 160, y + 14)
    P(d, 'firepit', 82, 3400); P(d, 'dogsled', 30, 3560); P(d, 'dogsled', 136, 3600); P(d, 'crate', 70, 3560); P(d, 'crate', 70, 3574)
    P(d, 'signpost', 100, 3330); over(d, 'lights', 0, 3480, 180, 1)
    pts = [(90, 3300), (60, 2950), (120, 2550), (60, 2150), (120, 1750), (70, 1350), (110, 950), (90, 300)]
    i = run(d, pts, 110)
    for k, yc in enumerate((2950, 2150, 1350)): lane(d, yc, 1 if k % 2 == 0 else -1, 5.0 - k * 0.3)
    clear(d, 0, 0, 180, 320, 'piste')
    for x in (20, 70, 120): P(d, 'dogsled', x, 40)
    d['data'].setdefault('decor', []).append(['bunting', 0, 110, 180])
    P(d, 'kennel', 160, 200); P(d, 'kennel', 160, 230); P(d, 'tent', 2, 220, 1)
    H(d, 'dog', 90, 3700); H(d, 'dog', 60, 1900); H(d, 'dog', 120, 600); H(d, 'thrower', 90, 2500)
    return d


def penguins():
    """PENGUIN BAY: across the frozen bay from the shore station: icebergs locked in the ice, fishing holes, the jetty,
    and the penguin huddles everywhere."""
    h = 4000; d = job('penguins', 'PENGUIN BAY', 'north', ['huskies'], h, 74, 22.0, 7, start=[90, 40])
    G(d, 'ice', 0, 0, 180, h); G(d, 'stone', 0, 0, 180, 300)
    for k, y in enumerate(range(300, h, 200)):       # the rocky shore down the left, pack ice down the right
        wl = (30, 18, 40, 24, 12)[k % 5]; wr = (16, 26, 10, 22, 30)[k % 5]
        wild(d, 'rocks', 0, y, wl, 200, 3200 + k, 0.8, 10); wild(d, 'ice', 180 - wr, y, wr, 200, 3250 + k, 0.7, 10)
    P(d, 'hut', 10, 40); P(d, 'hut', 150, 60, 2); P(d, 'flag', 80, 30, 1); P(d, 'crate', 40, 150); P(d, 'crate', 40, 164); P(d, 'trailmap', 120, 180)
    G(d, 'wood', 40, 300, 30, 260); P(d, 'mooring', 36, 400); P(d, 'mooring', 70, 500)      # the jetty
    for k, (x, y) in enumerate(((100, 700), (40, 1200), (110, 1700), (52, 2300), (104, 2800), (40, 3300), (110, 3650))):
        P(d, 'iceberg', x, y)
    for k, y in enumerate(range(900, 3800, 520)): P(d, 'hole', 70 if k % 2 else 120, y)
    for k, y in enumerate(range(450, 3900, 400)): H(d, 'peng', (60, 120, 90)[k % 3], y, 6 + k % 3)
    return d


def igloos():
    """IGLOO VILLAGE: rings of igloos round little squares, ice sculptures, drying racks and lanterns, and the village
    tree with its presents."""
    h = 4000; d = job('igloos', 'IGLOO VILLAGE', 'north', ['penguins'], h, 73, 22.4, 7, start=[90, h - 44])
    G(d, 'piste', 0, 0, 180, h); woods(d, 3301, dens=0.84)
    pts = [(90, h), (90, 3700), (56, 3500), (56, 2900), (124, 2700), (124, 2100), (56, 1900), (56, 1300), (124, 1100), (124, 500), (90, 300), (90, 0)]
    carve(d, 100, pts); path(d, 'stone', 40, pts)
    for k, (y0, y1, side) in enumerate(((2940, 3460, 1), (2140, 2660, -1), (1340, 1860, 1), (540, 1060, -1))):
        x0 = 106 if side > 0 else 0
        clear(d, x0, y0, 74, y1 - y0, 'piste')
        for j, y in enumerate(range(y0 + 10, y1 - 30, 64)):
            P(d, 'igloo', 150 if side > 0 else 0, y)
            if j % 2 == 1: P(d, ('icesculpt', 'firepit', 'xmastree', 'gifts')[(k + j) % 4], 112 if side > 0 else 40, y - 10)
            elif j % 4 == 0: P(d, 'dogsled', 120 if side > 0 else 44, y)
    clear(d, 0, 0, 180, 300, 'stone'); C(d, 'mosaic', 90, 140, 50); C(d, 'ice', 90, 140, 26)
    P(d, 'xmastree', 74, 90); P(d, 'gifts', 40, 180); P(d, 'gifts', 116, 190); P(d, 'lantpost', 10, 60); P(d, 'lantpost', 160, 60)
    over(d, 'lights', 0, 40, 180, 3); over(d, 'lights', 0, 250, 180, 1)
    for y in (3500, 2550, 1550, 600): over(d, 'lant', int(cx_at(pts, y)) - 50, y, 100)
    for y in (3200, 2400, 1600, 800): P(d, 'rail', int(cx_at(pts, y)) - 50, y, 24)        # fish drying racks
    H(d, 'peng', 90, 2000, 5); H(d, 'pedx', 40, 150); H(d, 'thrower', 120, 2400); H(d, 'dog', 90, 3300); H(d, 'thrower', 60, 1000)
    return d


def research():
    """RESEARCH BASE: modules on raised decks, masts and radar domes, the helipad, fuel drums, solar arrays, and the
    snowcats; a sled lane cuts through."""
    h = 4000; d = job('research', 'RESEARCH BASE', 'north', ['igloos'], h, 73, 22.8, 7, start=[90, 40])
    G(d, 'piste', 0, 0, 180, h)
    for k, y in enumerate(range(0, h, 400)):
        wild(d, 'ice', 0, y, (8, 16, 4, 12)[k % 4], 400, 3400 + k, 0.8, 9); wild(d, 'ice', 180 - (12, 4, 16, 8)[k % 4], y, (12, 4, 16, 8)[k % 4], 400, 3450 + k, 0.8, 9)
    G(d, 'conc', 0, 0, 180, 560)
    P(d, 'big', 0, 110, SH['BASE']); P(d, 'radar', 140, 4); P(d, 'mast', 152, 230); P(d, 'solar', 4, 200); P(d, 'solar', 4, 228)
    P(d, 'flag', 160, 330, 0); P(d, 'radar', 0, 380)
    G(d, 'deck', 78, 560, 24, 3240)                            # the boardwalk up the middle
    for k, y in enumerate(range(700, 3700, 300)):       # modules on decks both sides, with kit between them
        if 1380 < y < 1640 or 2580 < y < 2840 or 1930 < y < 2180: continue
        for x in (14, 122):
            G(d, 'deck', x - 6, y - 8, 56, 52); P(d, 'container', x, y, (k + x) % 6); P(d, 'container', x, y + 18, (k + x + 3) % 6)
        kit = k % 4
        if kit == 0: P(d, 'radar', 2, y + 52); P(d, 'solar', 142, y + 60)
        elif kit == 1: P(d, 'barrel', 4, y + 56); P(d, 'barrel', 16, y + 56); P(d, 'barrel', 160, y + 58); P(d, 'mast', 150, y + 52)
        elif kit == 2: P(d, 'solar', 6, y + 60); P(d, 'radar', 146, y + 52)
        else: P(d, 'mast', 10, y + 52); P(d, 'barrel', 150, y + 58); P(d, 'barrel', 162, y + 58)
    C(d, 'conc', 90, 2050, 40); dec(d, 'heli', 90 - 34, 2050 - 34, 34); P(d, 'heli', 68, 2024)
    lane(d, 1500, 1, 5.5); lane(d, 2700, -1, 5.0)
    clear(d, 0, 3780, 180, 220, 'conc'); P(d, 'shed', 6, 3820, 1); P(d, 'skip', 140, 3830)
    H(d, 'cannon', 18, 2350, 0.35, 7.0, 64); H(d, 'pedx', 40, 600); H(d, 'dog', 90, 3300)
    return d


def icefield():
    """ICE FIELD: across the open ice, ridge after pressure ridge with one way through each, seracs, the route
    flags, penguins."""
    h = 4200; d = job('icefield', 'ICE FIELD', 'north', ['research'], h, 74, 23.2, 7, start=[90, h - 44])
    G(d, 'piste', 0, 0, 180, h)
    for k, y in enumerate(range(3700, 400, -300)):
        gx = (6, 94, 50, 100, 16, 76, 100, 30, 86, 10, 64)[k % 11]; icy_band(d, y, 36, gx, 80, 3500 + k * 2)
        G(d, 'ice', 0, y + 120, 180, 40)
        P(d, 'iceblock', (gx + 100) % 150 + 10, y + 90, 16 + (k % 3) * 3)
        P(d, 'snowpole', gx - 2, y + 20); P(d, 'snowpole', gx + 80, y + 20)
    clear(d, 0, 3900, 180, 300); P(d, 'tent', 10, 3940, 0); P(d, 'tent', 140, 3950, 2); P(d, 'dogsled', 50, 4040)
    G(d, 'stone', 0, 0, 180, 300); P(d, 'flag', 20, 40, 0); P(d, 'flag', 150, 40, 1); P(d, 'cairn', 82, 120)
    for k, y in enumerate(range(800, 3800, 600)): H(d, 'peng', 90 + (-30, 30)[k % 2], y, 6)
    return d


def frozenlake():
    """FROZEN LAKE: a great lake frozen solid in the forest: ice-fishing huts and holes, the skating rink with its
    resurfacer, skaters crossing."""
    h = 4200; d = job('frozenlake', 'FROZEN LAKE', 'north', ['icefield'], h, 74, 23.6, 7, start=[90, 40])
    G(d, 'grass', 0, 0, 180, h); woods(d, 3601, dens=0.86)
    clear(d, 0, 0, 180, 400, 'deck'); P(d, 'cabin', 4, 20); P(d, 'bench', 20, 200); P(d, 'bench', 148, 200); P(d, 'trailmap', 20, 320)
    lake = [(90, 400), (70, 900), (100, 1600), (80, 2400), (100, 3200), (90, 3900), (90, h)]
    carve(d, 170, lake); path(d, 'ice', 150, lake)
    for c in ((90, 1100, 76), (90, 2000, 80), (90, 2900, 76)): C(d, 'ice', *c)
    for k, y in enumerate(range(700, 1800, 220)): P(d, 'hut', 30 if k % 2 == 0 else 134, y, k % 4); P(d, 'hole', 60 if k % 2 == 0 else 110, y + 40)
    clear(d, 30, 2240, 120, 340, 'ice'); P(d, 'rail', 30, 2236, 40); P(d, 'rail', 110, 2236, 40); P(d, 'rail', 30, 2580, 40); P(d, 'rail', 110, 2580, 40)
    H(d, 'orbit', 90, 2410, 44, 0, 'zam')
    for k, y in enumerate(range(2800, 3900, 260)): P(d, 'hut', 30 if k % 2 else 134, y, (k + 1) % 4); P(d, 'hole', 104 if k % 2 else 60, y + 50)
    for y in (1000, 1900, 3100, 3600): H(d, 'pedx', 40, y, (y // 100) % 2)
    H(d, 'peng', 90, 1500, 5); H(d, 'peng', 90, 3400, 5)
    return d


def aurora():
    """AURORA RIDGE: up the ridge path in the dark under the northern lights, cairns and the observatory hut at the
    top. Whiteouts."""
    h = 4200; d = job('aurora', 'AURORA RIDGE', 'north', ['frozenlake'], h, 78, 24.0, 7, start=[90, h - 44], squall=1)
    G(d, 'stone', 0, 0, 180, h); woods(d, 3701, 0, h, dens=0.8, kind='rocks', step=10)
    pts = [(90, h), (90, 3800), (50, 3400), (120, 2900), (50, 2400), (130, 1900), (60, 1400), (120, 900), (90, 500)]
    i = run(d, pts, 96, t='piste')
    for k, y in enumerate(range(3700, 600, -330)): P(d, 'cairn', int(edge(pts, 96, y, -1 if k % 2 else 1, 0)) - (0 if k % 2 else 14), y)
    for y in range(400, h - 200, 520): over(d, 'aurora', 0, y, 180)
    clear(d, 0, 0, 180, 520, 'stone'); P(d, 'cabin', 68, 30); P(d, 'radar', 10, 60); P(d, 'flag', 150, 60, 1); P(d, 'bench', 40, 200); P(d, 'bench', 130, 200)
    for x in (70, 110): H(d, 'rockfall', x, 0, 6.0 + x / 60, i)
    H(d, 'thrower', 90, 2200)
    return d


def snowmen():
    """SNOWMAN PARK (side): a whole park of snowmen, snowball forts with kids behind the walls, the park trees."""
    h = 3400; d = job('snowmen', 'SNOWMAN PARK', 'north', ['aurora'], h, 68, 24.0, 12, start=[90, h - 44], bonus=True)
    G(d, 'grass', 0, 0, 180, h); woods(d, 3801, 0, h, 0, 12, dens=0.9); woods(d, 3802, 0, h, 168, 180, dens=0.9)
    for k, y in enumerate(range(200, 3100, 96)):
        for x in ((22, 84, 146) if k % 2 == 0 else (54, 116)):
            if k % 6 == 3 and x in (54,): continue
            P(d, 'snowman', x, y)
    for k, y in enumerate((600, 1500, 2400)):           # snowball forts
        x = 20 if k % 2 == 0 else 104
        P(d, 'icewall', x, y + 60, 56); P(d, 'icewallv', x, y, 60) if k % 2 == 0 else P(d, 'icewallv', x + 46, y, 60)
        H(d, 'thrower', x + 24, y + 30)
    for y in (1050, 1950, 2850): P(d, 'xmastree', 74, y)
    clear(d, 0, 3200, 180, 200); P(d, 'gifts', 20, 3260); P(d, 'gifts', 134, 3270)
    H(d, 'thrower', 140, 3000); H(d, 'dog', 90, 300)
    return d


def polartrail():
    """POLAR TRAIL: the long trail over the tundra, flagged all the way, across the sled lanes and the frozen river to
    the rest camp."""
    h = 4400; d = job('polartrail', 'POLAR TRAIL', 'north', ['aurora'], h, 79, 24.4, 7, start=[90, 40])
    G(d, 'piste', 0, 0, 180, h)
    for k, y in enumerate(range(0, h, 300)):            # scattered thickets of stunted pines, tundra between
        x = (0, 120, 20, 110, 0, 130, 30, 100)[k % 8]; w = (60, 60, 40, 70, 50, 50, 40, 80)[k % 8]
        wild(d, 'forest', x, y + 30, w, 200, 3900 + k, 0.85, 9)
    pts = [(90, 0), (90, 400), (60, 900), (120, 1500), (60, 2100), (120, 2700), (60, 3300), (110, 3900), (90, h)]
    i = run(d, pts, 100)
    for y in range(200, h - 100, 150): c = cx_at(pts, y); P(d, 'snowpole', int(c - 50), y); P(d, 'snowpole', int(c + 46), y + 75)
    for k, yc in enumerate((800, 1800, 3000, 3800)): lane(d, yc, 1 if k % 2 == 0 else -1, 4.6)
    G(d, 'ice', 0, 2350, 180, 40); G(d, 'wood', int(cx_at(pts, 2370)) - 34, 2340, 68, 60)
    clear(d, 0, 2440, 180, 260, 'piste'); P(d, 'tent', 6, 2470, 0); P(d, 'tent', 146, 2480, 2); P(d, 'firepit', 40, 2600); P(d, 'dogsled', 150, 2600)
    clear(d, 0, 0, 180, 200, 'stone'); P(d, 'signpost', 20, 40); P(d, 'hut', 150, 40)
    H(d, 'dog', 90, 2560); H(d, 'thrower', 90, 1300)
    return d


def spires():
    """ICE SPIRES: a forest of ice: winding ways between the spires, opening into blue chambers."""
    h = 4400; d = job('spires', 'ICE SPIRES', 'north', ['polartrail'], h, 78, 24.8, 7, start=[90, h - 44])
    G(d, 'ice', 0, 0, 180, h); wild(d, 'ice', 0, 0, 180, h, 4001, 0.9, 8)
    pts = [(90, h), (90, 4000), (50, 3600), (130, 3200), (60, 2800), (120, 2300), (50, 1900), (130, 1400), (60, 1000), (110, 600), (90, 200), (90, 0)]
    run(d, pts, 92, t='piste')
    for (cx, cy) in ((90, 3400), (90, 2100), (90, 800)):
        carve(d, 160, [(cx - 10, cy), (cx + 10, cy)]); C(d, 'blue', cx, cy, 56)
        for a in (0, 0.5, -0.5, math.pi, math.pi - 0.5, math.pi + 0.5): P(d, 'spire', int(cx + 56 * math.cos(a) - 8), int(cy + 48 * math.sin(a) - 28))
        P(d, 'icesculpt', cx - 15, cy - 30)
    for y in range(3800, 300, -700): P(d, 'spire', int(edge(pts, 92, y, -1, -6)), y)
    clear(d, 0, 0, 180, 140, 'stone')
    H(d, 'peng', 90, 2100, 6); H(d, 'peng', 90, 800, 5); H(d, 'thrower', 90, 3000)
    return d


def gardens2():
    """PALACE GARDENS: the formal ice gardens below the palace: parterres walled in ice, frozen fountains, sculptures,
    the reindeer paddock, the decorated trees, ice arches over the walks."""
    h = 4400; d = job('gardens2', 'PALACE GARDENS', 'north', ['spires'], h, 74, 25.2, 7, start=[90, 40])
    G(d, 'piste', 0, 0, 180, h); G(d, 'stone', 64, 0, 52, h)
    for r in range(8):
        y = 240 + r * 500
        for x in (4, 122):                                # parterres: low ice walls round a bed
            P(d, 'icewall', x, y, 54); P(d, 'icewall', x, y + 170, 54)
            G(d, 'green', x + 4, y + 14, 46, 150)
            P(d, ('icesculpt', 'xmastree', 'statue', 'icecol')[(r + (x > 90)) % 4], x + 14, y + 60)
        C(d, 'mosaic', 90, y + 360, 30); C(d, 'ice', 90, y + 360, 18); P(d, 'fountain', 80, y + 350)
        over(d, 'icearch', 50, y + 220, 80)
    G(d, 'dirt', 0, 2160, 180, 150); P(d, 'rail', 0, 2150, 50); P(d, 'rail', 130, 2150, 50); P(d, 'rail', 0, 2312, 50); P(d, 'rail', 130, 2312, 50)
    P(d, 'reindeer', 8, 2190, 0); P(d, 'reindeer', 150, 2200, 1); P(d, 'reindeer', 10, 2260, 0); P(d, 'hay', 158, 2270)
    for y in range(120, h - 60, 260): P(d, 'lantpost', 54, y); P(d, 'lantpost', 116, y + 130)
    H(d, 'peng', 90, 1600, 5); H(d, 'thrower', 150, 3000); H(d, 'pedx', 40, 1200); H(d, 'dog', 90, 3800)
    return d


def northpole():
    """NORTH POLE POST (side): the post office and the Pole itself, Santa's sleigh and the reindeer, sacks of letters
    and piles of presents, elves everywhere."""
    h = 3400; d = job('northpole', 'NORTH POLE POST', 'north', ['gardens2'], h, 68, 25.2, 14, start=[90, h - 44], bonus=True)
    G(d, 'piste', 0, 0, 180, h); woods(d, 4201, 0, h, 0, 14, dens=0.9); woods(d, 4202, 0, h, 166, 180, dens=0.9)
    G(d, 'stone', 0, 0, 180, 300); P(d, 'big', 35, 40, SH['POST']); P(d, 'xmastree', 4, 60); P(d, 'xmastree', 144, 60)
    over(d, 'banner', 20, 230, 140, 17); over(d, 'lights', 0, 120, 180, 3)
    C(d, 'mosaic', 90, 1100, 70); C(d, 'ice', 90, 1100, 40); P(d, 'polepost', 83, 1050)
    for (x, y) in ((16, 1030), (16, 1130), (140, 1030), (140, 1130)): P(d, 'gifts', x, y)
    P(d, 'sleigh', 16, 1720); P(d, 'reindeer', 18, 1690, 1); P(d, 'reindeer', 38, 1690, 0); P(d, 'reindeer', 18, 1664, 0); P(d, 'reindeer', 38, 1664, 0)
    for k, y in enumerate(range(1960, 3140, 120)):
        P(d, 'stall', 14, y, k % 5) if k % 3 != 1 else P(d, 'xmastree', 14, y - 20)
        P(d, 'stall', 136, y + 40, (k + 2) % 5) if k % 3 != 2 else P(d, 'xmastree', 134, y + 20)
    for k, y in enumerate(range(360, 900, 130)): P(d, 'polepost', 20, y); P(d, 'polepost', 146, y + 60); P(d, 'gifts', 44 if k % 2 else 110, y + 40)
    for k, y in enumerate(range(1300, 1640, 110)): P(d, 'gifts', 14, y); P(d, 'gifts', 140, y + 50)
    for y in (500, 1500, 2300): over(d, 'lights', 14, y, 152, (y // 100) % 4)
    for y in (700, 1900, 2700): H(d, 'pedx', 30, y, (y // 100) % 2)
    H(d, 'dog', 90, 2500); H(d, 'thrower', 140, 600)
    return d


def palacegates():
    """PALACE GATES: up the grand avenue between ice columns, under ice arches, through gate after gate in the ice
    walls as the gates swing shut."""
    h = 4400; d = job('palacegates', 'PALACE GATES', 'north', ['gardens2'], h, 77, 25.6, 7, start=[90, h - 44])
    G(d, 'piste', 0, 0, 180, h); G(d, 'stone', 40, 0, 100, h)
    for k, y in enumerate(range(500, 4000, 560)):
        P(d, 'icewall', 0, y, 62); P(d, 'icewall', 118, y, 62); H(d, 'barrier', 62, y, 56, 5.0 + (k % 2))
        P(d, 'icecol', 44, y - 30); P(d, 'icecol', 122, y - 30)
        over(d, 'icearch', 40, y - 44, 100)
    for y in range(200, 4100, 140): P(d, 'icecol', 4, y); P(d, 'icecol', 162, y + 70)
    for y in (300, 1400, 2500, 3600): over(d, 'banner', 20, y + 120, 140, 18)
    for k, y in enumerate(range(760, 4000, 560)):
        P(d, 'icesculpt', 20 if k % 2 == 0 else 130, y + 40); P(d, 'lantpost', 44, y + 200); P(d, 'lantpost', 130, y + 200)
        P(d, 'statue', 30 if k % 2 else 142, y + 260)
    clear(d, 0, 0, 180, 200); P(d, 'flag', 30, 30, 0); P(d, 'flag', 140, 30, 1)
    H(d, 'cannon', 18, 1800, 0.35, 7.0, 64); H(d, 'peng', 90, 2600, 5); H(d, 'peng', 90, 900, 5)
    return d


def greathall():
    """THE GREAT HALL: inside the palace: ice walls, the red carpet, columns, chandeliers overhead, the feast tables
    and the presents under the great tree."""
    h = 4200; d = job('greathall', 'THE GREAT HALL', 'north', ['palacegates'], h, 69, 26.0, 7, start=[90, 40])
    G(d, 'ice', 0, 0, 180, h); G(d, 'blue', 10, 0, 160, h); G(d, 'red', 70, 0, 40, h)
    P(d, 'icewallv', 0, 0, h); P(d, 'icewallv', 170, 0, h)
    for k, y in enumerate(range(260, h - 200, 240)): P(d, 'icecol', 34, y); P(d, 'icecol', 132, y)
    for y in range(400, h - 300, 480): over(d, 'chandelier', 68, y)
    for k, y in enumerate(range(600, h - 600, 700)):
        P(d, 'table', 12, y, k % 4); P(d, 'table', 12, y + 30, (k + 1) % 4); P(d, 'table', 142, y + 200, (k + 2) % 4); P(d, 'table', 142, y + 230, (k + 3) % 4)
    for y in range(900, h - 400, 900): P(d, 'statue', 50, y); P(d, 'statue', 122, y)
    P(d, 'xmastree', 74, h - 240); P(d, 'gifts', 40, h - 180); P(d, 'gifts', 114, h - 180); P(d, 'gifts', 74, h - 150)
    H(d, 'peng', 90, 1500, 6); H(d, 'thrower', 90, 2700); H(d, 'peng', 90, 3400, 5)
    return d


def icepalace():
    """THE ICE PALACE (boss): the finale. Through the outer gate, across the courtyard with sleds racing through,
    past the gardens and the inner gate to the palace itself, with fireworks, and the polar bear on your tail."""
    h = 4800; d = job('icepalace', 'THE ICE PALACE', 'north', ['greathall'], h, 81, 27.0, 10, start=[90, h - 44], boss=True)
    G(d, 'piste', 0, 0, 180, h); G(d, 'stone', 50, 0, 80, h)
    P(d, 'big', 35, 40, SH['PALACE']); over(d, 'fireworks', 10, 20, 0); over(d, 'fireworks', 120, 30, 2); over(d, 'banner', 20, 150, 140, 19)
    for y in range(240, h - 100, 300): d['data'].setdefault('decor', []).append(['bunting', 0, y, 180])
    for k, y in enumerate((900, 2100, 3300, 4300)):    # gates in ice walls
        P(d, 'icewall', 0, y, 62); P(d, 'icewall', 118, y, 62); H(d, 'barrier', 62, y, 56, 5.0 + (k % 2) * 0.6)
        over(d, 'icearch', 40, y - 44, 100); P(d, 'icecol', 44, y - 30); P(d, 'icecol', 122, y - 30)
    for k, yc in enumerate((1500, 2700, 3800)):
        clear(d, 0, yc - 24, 180, 56, 'piste'); H(d, 'cross', 0, yc, 1 if k % 2 == 0 else -1, 5.0, 'sled')
    C(d, 'mosaic', 90, 1800, 50); C(d, 'ice', 90, 1800, 30); P(d, 'fountain', 80, 1790)
    for y in (2400, 3000): P(d, 'xmastree', 8, y); P(d, 'xmastree', 140, y + 100)
    for y in range(400, h - 200, 200): P(d, 'icecol', 4, y); P(d, 'icecol', 162, y + 100)
    P(d, 'sleigh', 10, 600); P(d, 'reindeer', 60, 620, 1); P(d, 'gifts', 140, 640); P(d, 'gifts', 130, 700)
    for k, y in enumerate((1100, 2300, 3500)): P(d, 'icesculpt', 18, y); P(d, 'icesculpt', 132, y + 60); P(d, 'lantpost', 50, y + 160); P(d, 'lantpost', 124, y + 160)
    for y in (2900, 4000): P(d, 'reindeer', 20, y, 1); P(d, 'reindeer', 140, y + 30, 0); P(d, 'gifts', 60, y + 60)
    H(d, 'peng', 70, 1300, 6); H(d, 'peng', 110, 2500, 6); H(d, 'cannon', 18, 2000, 0.35, 7.0, 64); H(d, 'cannon', 144, 3600, 2.79, 7.0, 64)
    H(d, 'chaser', 120, 4500, 'bear', 5)
    return d


ALL = [huskies, penguins, igloos, research, icefield, frozenlake, aurora, snowmen, polartrail, spires, gardens2, northpole, palacegates, greathall, icepalace]
