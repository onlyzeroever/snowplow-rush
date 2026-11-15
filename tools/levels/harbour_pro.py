"""Frozen Harbour, pro pass. The sea has frozen solid: basins are ice you can drive (slippery once scraped), boats
are frozen in, quays edged with bollards. Shop names: 39 FISH MARKET 40 WAREHOUSE 41 CUSTOMS 42 HARBOUR MASTER
43 FERRIES 44 BOAT SHED."""
from common import *


def quay_edge(d, x, y0, y1, seed, vertical=True):
    """the stone edge of a quay: kerbstones and a mooring bollard every so often"""
    r = rng(seed)
    if vertical:
        dec(d, 'kerb', x, y0, y1 - y0); y = y0 + r.randint(10, 40)
        while y < y1 - 10: P(d, 'mooring', x - 3, y); y += r.randint(70, 120)
    else:
        dec(d, 'kerbh', x, y0, y1 - x); xx = x + r.randint(10, 30)
        while xx < y1 - 10: P(d, 'mooring', xx, y0 - 3); xx += r.randint(50, 80)


def warehouses(d, y0, y1, seed, x=0, gap=(30, 90)):
    """a row of warehouses and sheds down the land side, with yards between"""
    r = rng(seed); y = y0 + r.randint(0, 40)
    while y + 72 < y1:
        scen(d, 'warehouse', x, y, r.randint(0, 3)); y += 72 + r.randint(*gap)


def frozen_boats(d, x0, x1, y0, y1, seed, n):
    r = rng(seed)
    for k in range(n):
        y = y0 + (y1 - y0) * (k + 0.5) / n + r.randint(-30, 30)
        P(d, 'boat' if r.random() < 0.7 else 'tug', r.choice((x0, x1 - 30)), int(y), r.randint(0, 3))


def harbour_clutter(d, rect, seed, n):
    scatter(d, ['crate', 'pots', 'nets', 'fishbox', 'barrel', 'pallet'], rect, n, seed, minsep=22)


def fishmarket():
    """FISH MARKET: the five o'clock auction. Off the quay road, through the market hall's stalls of fish boxes,
    along the frozen basin where the trawlers are iced in, to the ice factory."""
    d = job('fishmarket', 'FISH MARKET', 'harbour', ['openingday'], 2600, 62, 10.8, 7, start=[70, 2556])
    G(d, 'conc', 0, 0, 120, 2600); G(d, 'ice', 120, 0, 60, 2600); quay_edge(d, 120, 0, 2600, 1)
    frozen_boats(d, 126, 180, 100, 2500, 2, 6)
    # quay road (2300-2600)
    G(d, 'asph', 0, 2300, 120, 300); dec(d, 'dashv', 58, 2304, 292); P(d, 'van', 4, 2380, 1); P(d, 'van', 4, 2470, 3)
    # the market hall (1500-2300): stalls in two aisles under a canopy
    scen(d, 'shop', 0, 2236, 39)
    for y in range(1560, 2200, 110): P(d, 'stall', 0, y, (y // 110) % 5); P(d, 'fishbox', 34, y + 4); P(d, 'fishbox', 34, y + 18)
    over(d, 'canopy', 0, 1540, 70, 640)
    for y in (1600, 1820, 2040): P(d, 'pallet', 96, y)
    H(d, 'gull', 60, 1700, 5); H(d, 'cart', 80, 1900); H(d, 'pedx', 40, 2000)
    # the basin walk (600-1500)
    warehouses(d, 620, 1480, 41)
    for y in (700, 1000, 1300): P(d, 'lifering', 108, y)
    H(d, 'gull', 100, 900, 5); H(d, 'pedx', 120, 1100, 1)
    # ice factory (0-600)
    scen(d, 'shop', 0, 0, 40); P(d, 'iceblock', 66, 80, 16); P(d, 'iceblock', 84, 80, 14); P(d, 'iceblock', 76, 98, 12)
    P(d, 'van', 90, 200, 1); harbour_clutter(d, (4, 300, 110, 240), 4, 6)
    over(d, 'lights', 0, 260, 120, 2)
    return d


def quay():
    """QUAYSIDE: a long walk along the warehouses with the whole harbour frozen beside you."""
    d = job('quay', 'QUAYSIDE', 'harbour', ['fishmarket'], 2800, 66, 11.0, 7, start=[70, 52])
    G(d, 'cobble', 0, 0, 110, 2800); G(d, 'ice', 110, 0, 70, 2800); quay_edge(d, 110, 0, 2800, 5)
    from city_pro import shopfronts
    for y0 in (120, 900, 1700): scen(d, 'big', 0, y0, 40) if False else None
    for k, y0 in enumerate(range(100, 2700, 260)):
        scen(d, 'shopv' if k % 3 else 'shop', 0, y0, [40, 39, 42, 2, 44, 59][k % 6])
    frozen_boats(d, 120, 180, 60, 2740, 6, 8)
    for k, y0 in enumerate(range(100, 2700, 260)): harbour_clutter(d, (4, y0 + 80, 36, 150), 70 + k, 3)
    for y in range(200, 2700, 400): P(d, 'lamp', 98, y)
    over(d, 'lights', 0, 600, 110, 1); over(d, 'lights', 0, 1800, 110, 3)
    H(d, 'gull', 50, 800, 6); H(d, 'gull', 60, 2000, 5); H(d, 'pedx', 30, 1400); H(d, 'thrower', 80, 2300)
    return d


def lighthouse():
    """LIGHTHOUSE POINT: out along the headland path over the rocks to the lighthouse, past the coastguard hut."""
    d = job('lighthouse', 'LIGHTHOUSE POINT', 'harbour', ['quay'], 2600, 63, 11.2, 7, start=[90, 2556])
    G(d, 'grass', 0, 0, 180, 2600)
    wild(d, 'rocks', 0, 0, 180, 2600, 11, 0.8, 10)
    pts = [(90, 2600), (60, 2300), (120, 2000), (70, 1700), (110, 1400), (60, 1100), (110, 800), (80, 500), (90, 200)]
    carve(d, 78, pts); path(d, 'gravel', 34, pts)
    carve(d, 120, [(90, 140), (90, 260)]); C(d, 'stone', 90, 180, 56)
    scen(d, 'lighthouse', 77, 70); P(d, 'hut', 30, 150)
    H(d, 'gull', 70, 700, 6); H(d, 'gull', 110, 1700, 5); H(d, 'thrower', 60, 1200)
    return d


def containers():
    """CONTAINER YARD: stacks in rows, forklifts shuttling, the gantry cranes over the quay."""
    d = job('containers', 'CONTAINER YARD', 'harbour', ['lighthouse'], 3000, 68, 11.4, 7, start=[90, 2956])
    G(d, 'conc', 0, 0, 180, 3000)
    for k, y in enumerate(range(200, 2700, 280)):
        for x in (0, 136):
            for j in range(3): P(d, 'container', x, y + j * 18, (k + j + x) % 6) if x == 0 else P(d, 'container', x, y + 60 + j * 18, (k + j) % 6)
        dec(d, 'hatch', 70, y + 100, 40, 40) if k % 3 == 0 else None
    for y in range(300, 2800, 400): dec(d, 'arrow', 86, y, y % 800 // 400)
    scen(d, 'gantry', 55, 0); scen(d, 'shop', 0, 2860, 40)
    for y in range(400, 2800, 500): H(d, 'forklift', 40 if (y // 500) % 2 else 120, y + 60, (y // 500) % 2)
    P(d, 'pallet', 80, 2700); H(d, 'gull', 90, 1500, 5)
    return d


def boatyard():
    """BOATYARD: boats up on stands for the winter, the boat shed, a slipway onto the ice, the chandlery."""
    d = job('boatyard', 'BOATYARD', 'harbour', ['containers'], 2800, 64, 11.6, 7, start=[90, 52])
    G(d, 'gravel', 0, 0, 180, 2400); G(d, 'ice', 0, 2400, 180, 400); quay_edge(d, 0, 2400, 180, 13, vertical=False)
    scen(d, 'shop', 0, 100, 44); scen(d, 'shop', 124, 100, 42)
    r = rng(14)
    for k, y in enumerate(range(260, 2300, 170)):
        P(d, 'boat', 0 if k % 2 else 150, y, k % 4); P(d, 'crate', 34 if k % 2 else 130, y + 40)
    G(d, 'wood', 70, 2200, 40, 200)
    frozen_boats(d, 10, 170, 2450, 2750, 15, 3)
    warehouses(d, 300, 2100, 42, x=62, gap=(140, 220))
    H(d, 'forklift', 90, 900, 1); H(d, 'forklift', 90, 1700, 0); H(d, 'gull', 100, 2600, 6); H(d, 'pedx', 40, 1300)
    return d


def ferry():
    """FERRY TERMINAL: car lanes through the check-in booths, the ferry docked at the ramp, the terminal hall."""
    d = job('ferry', 'FERRY TERMINAL', 'harbour', ['boatyard'], 3000, 69, 11.8, 7, start=[90, 2956])
    G(d, 'asph', 0, 0, 180, 3000)
    scen(d, 'big', 0, 2600, 43); G(d, 'slab', 0, 2660, 180, 340)
    for x in (44, 90, 136): dec(d, 'dashv', x, 1000, 1500)
    for y in (1200, 1500, 1800): dec(d, 'arrow', 60, y, 0); dec(d, 'arrow', 112, y + 60, 0)
    for x in (4, 154): P(d, 'booth', x, 900, 1)
    H(d, 'barrier', 50, 800, 80, 5.0)
    G(d, 'ice', 0, 0, 180, 500); scen(d, 'hull', 45, 0); G(d, 'wood', 60, 500, 60, 200)
    for x, y in ((10, 560), (150, 560)): P(d, 'lifering', x, y)
    harbour_clutter(d, (4, 1100, 30, 1400), 17, 6); harbour_clutter(d, (150, 1100, 26, 1400), 18, 6)
    H(d, 'ped', 160, 1500); H(d, 'gull', 60, 300, 6); H(d, 'taxi', 70, 1500, 1, 700, 2600)
    return d


def drawbridge():
    """DRAWBRIDGE: the old canal quarter; three lifting bridges over the frozen canal close in turn."""
    d = job('drawbridge', 'DRAWBRIDGE', 'harbour', ['ferry'], 3000, 71, 12.0, 7, start=[90, 52])
    G(d, 'cobble', 0, 0, 180, 3000); G(d, 'ice', 50, 0, 80, 3000); quay_edge(d, 48, 0, 3000, 19); quay_edge(d, 130, 0, 3000, 20)
    for k, yc in enumerate((700, 1500, 2300)):
        G(d, 'deck', 0, yc - 20, 180, 40); P(d, 'lamp', 40, yc - 40); P(d, 'lamp', 136, yc + 20)
        H(d, 'barrier', 50, yc - 14, 80, 4.5 + k * 0.4)
    for y in range(100, 2900, 300): scen(d, 'shopv', 0 if (y // 300) % 2 else 136, y, [40, 42, 2, 59][(y // 300) % 4])
    frozen_boats(d, 54, 130, 200, 2800, 21, 5)
    H(d, 'gull', 100, 800, 5); H(d, 'forklift', 90, 2000, 0); H(d, 'pedx', 40, 1400)
    over(d, 'lights', 0, 1000, 180, 2); over(d, 'lights', 0, 1900, 180, 4)
    return d


def icefish():
    """ICE FISHING: out on the frozen bay among the fishing huts and their holes; sleds pulled about."""
    d = job('icefish', 'ICE FISHING', 'harbour', ['drawbridge'], 2800, 66, 12.2, 7, start=[90, 2756])
    G(d, 'ice', 0, 0, 180, 2600); G(d, 'gravel', 0, 2600, 180, 200); quay_edge(d, 0, 2600, 180, 22, vertical=False)
    r = rng(23)
    for k in range(14):
        x, y = r.choice((10, 40, 120, 150)), 200 + k * 170 + r.randint(-20, 20)
        P(d, 'hut', x, y, k % 3); dec(d, 'puddle', x + 20 if x < 90 else x - 20, y + 20, 5)
    for y in (500, 1300, 2100): P(d, 'sled', 80, y) if False else P(d, 'crate', 84, y)
    scen(d, 'cabin', 136, 2620); P(d, 'van', 4, 2640, 2)
    H(d, 'gull', 60, 1200, 6); H(d, 'thrower', 120, 2000); H(d, 'ped', 60, 800)
    return d


def pier():
    """PIER ARCADE (side job): out along the pier over the ice: arcade cabinets, booths, the helter at the end."""
    d = job('pier', 'PIER ARCADE', 'harbour', ['icefish'], 2400, 61, 12.2, 9, start=[90, 2356], bonus=True)
    G(d, 'ice', 0, 0, 180, 2400); G(d, 'deck', 24, 0, 132, 2400)
    wild(d, 'ice', 0, 0, 22, 2200, 33, 0.4, 14); wild(d, 'ice', 158, 0, 22, 2200, 34, 0.4, 14)
    for x in (22, 153): P(d, 'railv', x, 0, 2200)
    for y in range(200, 2200, 160): P(d, 'arcade', 34, y, y % 5); P(d, 'arcade', 132, y + 80, (y + 1) % 5)
    for y in (500, 1300): P(d, 'booth', 34, y + 40, 1)
    scen(d, 'helter', 77, 20); P(d, 'balloons', 40, 140)
    for y in (400, 1200, 2000): over(d, 'lights', 30, y, 120, y % 4)
    H(d, 'gull', 70, 900, 6); H(d, 'gull', 100, 1800, 6); H(d, 'pedx', 40, 1200)
    return d


def customs():
    """CUSTOMS HOUSE: the inspection lanes, barriers rising and falling, the grand old customs house."""
    d = job('customs', 'CUSTOMS HOUSE', 'harbour', ['icefish'], 3000, 70, 12.4, 7, start=[90, 2956])
    G(d, 'asph', 0, 0, 180, 3000)
    for k, y in enumerate(range(600, 2600, 500)):
        P(d, 'booth', 82, y, k % 3); H(d, 'barrier', 8, y + 30, 70, 5.0); H(d, 'barrier', 102, y + 30, 70, 5.6)
        dec(d, 'stop', 8, y + 46, 164)
    scen(d, 'big', 35, 0, 41); G(d, 'slab', 0, 0, 180, 300); dec(d, 'crest', 72, 180, 18)
    for x in (10, 166): P(d, 'flag', x, 120, 2)
    harbour_clutter(d, (4, 2640, 30, 300), 24, 4); harbour_clutter(d, (150, 2640, 26, 300), 35, 4)
    for y in (420, 1000, 1500, 2100): scen(d, 'warehouse', 0 if y % 1000 < 500 else 124, y + 120, y % 4)
    H(d, 'forklift', 40, 1300, 1); H(d, 'forklift', 140, 2200, 1); H(d, 'ped', 160, 900)
    return d


def locks():
    """CANAL LOCKS: a flight of locks climbing the hill; the gates swing, boats wait in the chambers."""
    d = job('locks', 'CANAL LOCKS', 'harbour', ['customs'], 3000, 69, 12.6, 7, start=[90, 52])
    G(d, 'grass', 0, 0, 180, 3000); G(d, 'cobble', 0, 0, 60, 3000); G(d, 'ice', 60, 0, 60, 3000); G(d, 'cobble', 120, 0, 60, 3000)
    quay_edge(d, 60, 0, 3000, 25); quay_edge(d, 118, 0, 3000, 26)
    for k, y in enumerate(range(400, 2800, 600)):
        H(d, 'barrier', 60, y, 60, 5.0 + (k % 2)); P(d, 'boat', 76, y + 120, k % 4)
        P(d, 'lamp', 30, y - 30); G(d, 'stone', 0, y - 6, 180, 12)
    scen(d, 'cabin', 0, 1400); scen(d, 'cabin', 136, 2400)
    H(d, 'gull', 140, 1300, 5); H(d, 'pedx', 20, 1800); H(d, 'thrower', 150, 600)
    return d


def gullisland():
    """GULL ISLAND (side job): a rocky island, the gull colony, a jetty and the old beacon."""
    d = job('gullisland', 'GULL ISLAND', 'harbour', ['locks'], 2400, 61, 12.6, 9, start=[90, 2356], bonus=True)
    G(d, 'ice', 0, 0, 180, 2400); G(d, 'sand', 20, 300, 140, 1800)
    wild(d, 'rocks', 0, 300, 30, 1800, 27, 0.8, 10); wild(d, 'rocks', 150, 300, 30, 1800, 28, 0.8, 10)
    G(d, 'deck', 70, 2100, 40, 300); scen(d, 'lighthouse', 77, 120)
    for y in range(300, 2300, 400): H(d, 'gull', 70, y, 6)
    for x, y in ((50, 800), (110, 1300), (60, 1800)): P(d, 'rock', x, y, 20)
    return d


def shipyard():
    """SHIPYARD: a new ship on the slipway, gantry cranes, steel plates stacked, forklifts everywhere."""
    d = job('shipyard', 'SHIPYARD', 'harbour', ['locks'], 3200, 71, 12.8, 7, start=[90, 3156])
    G(d, 'conc', 0, 0, 180, 3200); G(d, 'ice', 0, 0, 180, 300)
    scen(d, 'hull', 45, 300); scen(d, 'gantry', 55, 100); scen(d, 'gantry', 0, 600) if False else None
    warehouses(d, 560, 1640, 43, gap=(40, 80)); warehouses(d, 1700, 3000, 44, x=124, gap=(60, 140))
    for y in range(600, 1600, 200): P(d, 'pallet', 154, y + 100)
    for y in range(1800, 3000, 400): H(d, 'forklift', 90, y, (y // 400) % 2)
    harbour_clutter(d, (4, 1700, 172, 1300), 29, 14)
    H(d, 'cannon', 2, 1300, 0.2, 7.0, 60)
    return d


def icebreaker():
    """ICEBREAKER DOCK: the red icebreaker in its broken channel, containers on the quay, barriers on the bridge."""
    d = job('icebreaker', 'ICEBREAKER DOCK', 'harbour', ['shipyard'], 3200, 71, 13.0, 7, start=[90, 52])
    G(d, 'conc', 0, 0, 180, 3200); G(d, 'ice', 0, 1500, 180, 1700)
    for k, y in enumerate(range(300, 1300, 200)): P(d, 'container', 2 if k % 2 else 134, y, k % 6); H(d, 'barrier', 50, y + 100, 80, 5.0 + k % 2)
    scen(d, 'hull', 45, 1700); frozen_boats(d, 4, 176, 2400, 3100, 30, 4)
    for x, y in ((6, 1520), (160, 1520)): P(d, 'lifering', x, y)
    H(d, 'cannon', 2, 2200, 0.2, 7.0, 64); H(d, 'cannon', 160, 2600, 3.0, 7.0, 64); H(d, 'gull', 100, 1500, 6); H(d, 'forklift', 90, 700, 0)
    return d


def festival():
    """HARBOUR FESTIVAL (boss): the whole harbour turns out, and a runaway forklift hunts you all job."""
    d = job('festival', 'HARBOUR FESTIVAL', 'harbour', ['icebreaker'], 3400, 75, 13.4, 9, start=[90, 3356], boss=True)
    G(d, 'cobble', 0, 0, 120, 3400); G(d, 'ice', 120, 0, 60, 3400); quay_edge(d, 120, 0, 3400, 31)
    frozen_boats(d, 126, 180, 100, 3300, 32, 8)
    for y in range(300, 3200, 280): P(d, 'stall', 0, y, (y // 280) % 5)
    for y in (420, 1260, 2100, 2940): scen(d, 'warehouse', 64, y, y % 4)
    P(d, 'stage', 30, 200, 5); P(d, 'speaker', 30, 238); P(d, 'speaker', 100, 238)
    for k, y in enumerate((900, 1800, 2700)): H(d, 'barrier', 40, y, 70, 5.0 + k * 0.5)
    for y in range(500, 3300, 500): over(d, 'lights', 0, y, 180, y % 5)
    for y in (700, 2200): over(d, 'fireworks', 60, y - 200, y % 4)
    H(d, 'gull', 80, 600, 6); H(d, 'gull', 80, 2200, 6); H(d, 'pedx', 40, 1300); H(d, 'pedx', 60, 2500, 1)
    H(d, 'chaser', 100, 3000, 'forklift', 5)
    return d


ALL = [fishmarket, quay, lighthouse, containers, boatyard, ferry, drawbridge, icefish, pier, customs, locks, gullisland, shipyard, icebreaker, festival]


HPAL = ['crate', 'pots', 'nets', 'fishbox', 'barrel', 'pallet', 'lifering', 'bins', 'bench', 'lamp', 'crate', 'pots']
def dress(J):
    for k, d in enumerate(J):
        autodress(d, HPAL, 500 + k, chance=0.6)
        r = rng(900 + k)
        for g in [g for g in d['data']['ground'] if g[0] == 'ice']:
            for _ in range(max(2, g[4] // 160)):
                x, y = g[1] + r.randint(4, max(5, g[3] - 30)), g[2] + r.randint(4, max(5, g[4] - 30))
                dec(d, r.choice(['crack', 'puddle', 'crack']), x, y, r.randint(8, 24), r.randint(1, 99))
