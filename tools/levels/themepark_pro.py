"""Theme Park, pro pass. Shop names: 31 TICKETS 32 SOUVENIRS 33 ARCADE 34 HAUNTED HOUSE 35 BURGERS 36 ICE CREAM
37 GHOST TRAIN 38 LOG FLUME. Grounds: mosaic plazas, purple and orange paths, boardwalk, tile. Lights everywhere."""
from common import *
import math


def lights(d, ys, x=0, w=180):
    for k, y in enumerate(ys): over(d, 'lights', x, y, w, k)


def beds(d, y0, y1, seed, side='both', w=30):
    """landscaped planting beds flush to the edges, staggered, with lamps between: breaks up the open paving"""
    r = rng(seed); y = y0
    while y < y1 - 60:
        h = r.randint(70, 140)
        if side in ('both', 'l') and r.random() < 0.8: wild(d, r.choice(['bush', 'park', 'bush']), 0, y, w, h, y + seed, 0.9, 8)
        if side in ('both', 'r') and r.random() < 0.8: wild(d, r.choice(['bush', 'park', 'bush']), 180 - w, y + r.randint(20, 60), w, h, y + seed + 1, 0.9, 8)
        y += h + r.randint(60, 120)


def snacks(d, x, y, seed):
    """a little cluster of snack stands against an edge"""
    r = rng(seed); k = r.choice(['popcorn', 'balloons', 'kiosk'])
    P(d, k, x, y, r.randint(0, 3)) if k == 'kiosk' else P(d, k, x, y)


def gates():
    """TICKET GATES: the park opens at nine. Off the coach park, through the turnstiles under the great gate, past
    the ticket booths and the welcome plaza with the mascot statue, up the avenue of lights."""
    d = job('gates', 'TICKET GATES', 'themepark', ['parade'], 2400, 63, 7.8, 7, start=[90, 2356])
    # coach park (1960-2400)
    G(d, 'asph', 0, 1960, 180, 440)
    for y in (2000, 2120, 2240):
        dec(d, 'bay', 0, y, 28, 56); P(d, 'bus', 2, y + 2)
    for y in (2060, 2180, 2300): dec(d, 'bay', 152, y, 28, 56)
    P(d, 'bus', 154, 2062); dec(d, 'arrow', 86, 2260, 0); dec(d, 'arrow', 86, 2060, 0); dec(d, 'hatch', 70, 1980, 40, 40)
    # turnstiles under the gate (1860-1960)
    G(d, 'mosaic', 0, 1860, 180, 100)
    for x in (30, 60, 112, 142): P(d, 'turnstile', x, 1920)
    over(d, 'parkgate', 0, 1880, 180); P(d, 'booth', 4, 1870, 0); P(d, 'booth', 158, 1870, 1)
    # ticket booths & queue lanes (1500-1860)
    G(d, 'slab', 0, 1500, 180, 360); G(d, 'tile', 60, 1500, 60, 360)
    for y in (1540, 1660, 1780): P(d, 'booth', 6, y, y % 3); P(d, 'booth', 156, y + 50, (y + 1) % 3)
    for y in (1560, 1700): P(d, 'rail', 24, y, 30); P(d, 'rail', 126, y + 40, 30)
    lights(d, (1600, 1760))
    # welcome plaza (1000-1500): the mascot on his plinth, a ring of flowerbeds, the souvenir shop
    G(d, 'tile', 0, 1000, 180, 500); C(d, 'mosaic', 90, 1250, 70); C(d, 'tile', 90, 1250, 40); dec(d, 'starm', 90 - 28, 1250 - 28, 28)
    P(d, 'mascot', 77, 1222)
    for a in range(6):
        x, y = 90 + 86 * math.cos(a * math.pi / 3 + 0.5), 1250 + 86 * math.sin(a * math.pi / 3 + 0.5)
        if 10 < x < 160: P(d, 'planter', int(x) - 7, int(y) - 14)
    scen(d, 'shop', 0, 1010, 32); scen(d, 'shop', 124, 1420, 31); P(d, 'balloons', 140, 1060); P(d, 'popcorn', 20, 1440)
    H(d, 'ped', 40, 1350); H(d, 'ped', 140, 1150, 1); H(d, 'thrower', 150, 1300)
    # avenue of lights (0-1000)
    G(d, 'pave', 0, 0, 180, 1000); G(d, 'purple', 76, 0, 4, 1000); G(d, 'purple', 100, 0, 4, 1000); beds(d, 60, 980, 101, w=26)
    for y in (100, 300, 500, 700, 900): P(d, 'lamp', 6, y); P(d, 'lamp', 168, y + 100)
    for y in (160, 440, 760): P(d, 'kiosk', 2, y, y % 4); P(d, 'balloons', 158, y + 120)
    lights(d, (80, 260, 440, 620, 800))
    over(d, 'banner', 0, 40, 180, 0); H(d, 'pedx', 40, 600); H(d, 'ped', 120, 300)
    return d


def mainst():
    """MAIN STREET: the park's high street, gingerbread shopfronts both sides, a little railway station at the top
    and the band playing in the square halfway down."""
    d = job('mainst', 'MAIN STREET', 'themepark', ['gates'], 2800, 58, 8.0, 7, start=[90, 52])
    G(d, 'cobble', 0, 0, 180, 2800); G(d, 'red', 82, 0, 16, 2800)
    names = [32, 33, 35, 36, 15, 5, 2, 14]
    from city_pro import shopfronts
    shopfronts(d, 'l', 120, 1200, 71, names, gap=(0, 30)); shopfronts(d, 'r', 140, 1200, 72, names, gap=(0, 30))
    shopfronts(d, 'l', 1560, 2780, 73, names, gap=(0, 40)); shopfronts(d, 'r', 1580, 2780, 74, names, gap=(0, 40))
    # the station at the top
    G(d, 'wood', 0, 0, 180, 100); P(d, 'track', 0, 0, 100) if False else None; dec(d, 'railsh', 0, 30, 180)
    P(d, 'bench', 20, 70); P(d, 'bench', 150, 70); P(d, 'clock', 84, 40)
    # band square (1220-1540)
    G(d, 'mosaic', 0, 1220, 180, 320); C(d, 'tile', 90, 1380, 60)
    P(d, 'stage', 50, 1340, 3); P(d, 'speaker', 52, 1378); P(d, 'speaker', 118, 1378)
    for x, y in ((10, 1250), (156, 1500), (16, 1490)): P(d, 'balloons', x, y)
    over(d, 'banner', 0, 1240, 180, 1)
    lights(d, (200, 420, 640, 860, 1080, 1640, 1860, 2080, 2300, 2520), 44, 92)
    for y in (300, 700, 1100, 1800, 2200, 2600): dec(d, 'manhole', 64, y)
    H(d, 'pedx', 50, 500); H(d, 'pedx', 120, 900, 1); H(d, 'ped', 70, 1800); H(d, 'ped', 110, 2300, 1); H(d, 'cart', 90, 2000)
    return d


def carousel():
    """CAROUSEL COURT: the old gallopers turn under the fairy lights; teacups spin across the court; organ music."""
    d = job('carousel', 'CAROUSEL COURT', 'themepark', ['mainst'], 2600, 68, 8.2, 7, start=[90, 2556])
    G(d, 'tile', 0, 0, 180, 2600)
    # entry walk (2200-2600)
    G(d, 'pave', 0, 2200, 180, 400); G(d, 'purple', 84, 2200, 12, 400)
    for y in (2240, 2380, 2520): P(d, 'kiosk', 2, y, y % 4); P(d, 'popcorn', 160, y + 60)
    # first court: the carousel itself (1600-2200)
    C(d, 'mosaic', 90, 1900, 86); C(d, 'wood', 90, 1900, 40)
    scen(d, 'carousel', 70, 1872)
    for a in range(8):
        x, y = 90 + 66 * math.cos(a * math.pi / 4), 1900 + 66 * math.sin(a * math.pi / 4)
        if a % 2: P(d, 'lamp', int(x) - 3, int(y) - 22)
    lights(d, (1640, 1780, 2020, 2160))
    # teacups (1000-1600)
    C(d, 'blue', 90, 1300, 70); scen(d, 'teacups', 55, 1270)
    P(d, 'arcade', 4, 1060, 0); P(d, 'arcade', 4, 1084, 1); P(d, 'claw', 156, 1520)
    P(d, 'balloons', 160, 1100); P(d, 'bench', 6, 1500)
    # organ court (400-1000): a second, smaller carousel and the big top
    scen(d, 'bigtop', 0, 420, 0); C(d, 'mosaic', 120, 760, 40); scen(d, 'carousel', 100, 732)
    P(d, 'popcorn', 156, 460); P(d, 'balloons', 10, 900)
    lights(d, (640, 900))
    # the exit arch at the top (0-400)
    G(d, 'pave', 0, 0, 180, 400); over(d, 'banner', 0, 120, 180, 2)
    for x, y in ((10, 200), (150, 240), (20, 340)): P(d, 'stree', x, y, 26)
    H(d, 'ped', 40, 1700); H(d, 'pedx', 30, 1100); H(d, 'ped', 140, 600, 1); H(d, 'thrower', 150, 300)
    return d


def games():
    """GAMES ALLEY: hook-a-duck, coconut shy, the arcade hall; three alleys of stalls joined by little squares."""
    d = job('games', 'GAMES ALLEY', 'themepark', ['carousel'], 2800, 71, 8.4, 8, start=[90, 52])
    G(d, 'pave', 0, 0, 180, 2800)
    for y0 in (120, 1000, 1880):
        G(d, 'wood', 40, y0, 100, 700)
        for k, y in enumerate(range(y0 + 20, y0 + 680, 90)):
            P(d, 'stall', 0, y, k % 5); P(d, 'stall', 150, y + 40, (k + 2) % 5)
        lights(d, (y0 + 100, y0 + 300, y0 + 500), 30, 120)
    for yc in (900, 1780):
        C(d, 'mosaic', 90, yc, 56); P(d, 'claw', 80, yc - 20)
        P(d, 'arcade', 2, yc - 40, 2); P(d, 'arcade', 18, yc - 40, 3); P(d, 'arcade', 150, yc + 10, 4); P(d, 'arcade', 166, yc + 10, 0)
    scen(d, 'shop', 0, 2700, 33); scen(d, 'shop', 124, 2700, 32)
    over(d, 'banner', 0, 40, 180, 3)
    for y in (500, 1400, 2300): H(d, 'thrower', 90, y)
    H(d, 'pedx', 60, 700); H(d, 'pedx', 120, 1500, 1); H(d, 'ped', 80, 2200)
    return d


def bumpers():
    """BUMPER CARS: two big floors of bumper cars running while you plow. Watch the bumpers."""
    d = job('bumpers', 'BUMPER CARS', 'themepark', ['games'], 2600, 64, 8.6, 7, start=[90, 2556])
    G(d, 'slab', 0, 0, 180, 2600)
    for k, y0 in enumerate((300, 1400)):
        G(d, 'deck', 8, y0, 164, 700); wallbox(d, 4, y0 - 4, 176, y0 + 708, [('t', 62, 118), ('b', 62, 118)], kind='rail')
        for x in range(20, 170, 30): dec(d, 'starm', x, y0 + 340 + (x % 60), 5)
        H(d, 'bumper', 30, y0 + 120, 4 + k); H(d, 'bumper', 110, y0 + 400, 3 + k)
        lights(d, (y0 + 60, y0 + 300, y0 + 540))
    # between the floors: a little plaza, prize booth, snacks
    G(d, 'tile', 0, 1020, 180, 360); C(d, 'mosaic', 90, 1200, 40); P(d, 'mascot', 77, 1170); P(d, 'booth', 6, 1100, 2); P(d, 'popcorn', 160, 1240); P(d, 'balloons', 10, 1300); P(d, 'arcade', 156, 1060, 1)
    scen(d, 'shop', 0, 2440, 33); P(d, 'kiosk', 150, 2460, 2); P(d, 'kiosk', 150, 2200, 1)
    G(d, 'pave', 0, 0, 180, 280); over(d, 'banner', 0, 120, 180, 2); P(d, 'popcorn', 10, 140); beds(d, 2010, 2420, 51)
    H(d, 'ped', 60, 1200); H(d, 'ped', 120, 2200, 1); H(d, 'thrower', 150, 200)
    return d


def food():
    """FOOD COURT: lunchtime. Burgers, ice cream, the waffle truck; terraces of tables under heaters and lights."""
    d = job('food', 'FOOD COURT', 'themepark', ['bumpers'], 2700, 68, 8.8, 7, start=[90, 52])
    G(d, 'tile', 0, 0, 180, 2700)
    scen(d, 'shop', 0, 100, 35); scen(d, 'shop', 124, 160, 36)
    for y0 in (360, 1260, 2060):
        G(d, 'wood', 0, y0, 180, 520)
        for k in range(3):
            for x, a in ((20, k), (130, k + 1)):
                P(d, 'parasol', x, y0 + 40 + k * 150, a % 4); P(d, 'table', x + 20, y0 + 70 + k * 150)
        lights(d, (y0 + 30, y0 + 260))
    for k, (x, y) in enumerate(((4, 980), (150, 1040), (4, 1880), (150, 1940))): P(d, 'foodtruck', x, y, k % 3)
    scen(d, 'shop', 0, 2620, 35); scen(d, 'shop', 124, 2620, 14)
    H(d, 'bumper', 70, 1700, 3); H(d, 'ped', 90, 900); H(d, 'pedx', 60, 1500); H(d, 'cart', 80, 2300)
    return d


def ferris():
    """FERRIS WHEEL: the giant wheel on its hill, the queue maze, a garden walk, the viewing terrace."""
    d = job('ferris', 'FERRIS WHEEL', 'themepark', ['food'], 2800, 71, 9.0, 7, start=[90, 2756])
    G(d, 'grass', 0, 0, 180, 2800)
    path(d, 'pave', 52, [(90, 2800), (60, 2500), (120, 2200), (60, 1900), (90, 1600)])
    for x, y in ((10, 2600), (150, 2400), (10, 2200), (150, 2000), (12, 1800)): P(d, 'stree', x, y, 28)
    for x, y in ((140, 2650), (20, 2350), (140, 2100)): P(d, 'balloons', x, y)
    # the wheel on its plaza (800-1600)
    C(d, 'mosaic', 90, 1200, 88); C(d, 'tile', 90, 1200, 50)
    scen(d, 'ferris', 54, 1140)
    for y in (1360, 1420, 1480): P(d, 'rail', 30, y, 36); P(d, 'rail', 114, y + 30, 36)
    lights(d, (900, 1100, 1500))
    # viewing terrace (0-800)
    G(d, 'deck', 0, 0, 180, 800); P(d, 'rail', 0, 0, 180)
    for x, y in ((20, 120), (140, 220), (20, 420), (140, 560)): P(d, 'bench', x, y)
    P(d, 'kiosk', 150, 40, 1); P(d, 'popcorn', 10, 40); P(d, 'mascot', 150, 680)
    H(d, 'ped', 60, 300); H(d, 'ped', 120, 2000, 1); H(d, 'thrower', 40, 1700); H(d, 'pedx', 30, 600)
    return d


def helter():
    """HELTER SKELTER: three slides on a fairground green, mats piled up, the big top and the swing boats."""
    d = job('helter', 'HELTER SKELTER', 'themepark', ['ferris'], 2700, 67, 9.2, 7, start=[90, 52])
    G(d, 'grass', 0, 0, 180, 2700)
    path(d, 'pave', 56, [(90, 0), (90, 400), (60, 800), (120, 1300), (60, 1800), (90, 2300), (90, 2700)]); path(d, 'orange', 6, [(90, 0), (90, 400), (60, 800), (120, 1300), (60, 1800), (90, 2300), (90, 2700)])
    for x, y in ((10, 500), (140, 1100), (10, 1700)): scen(d, 'helter', x, y)
    scen(d, 'bigtop', 104, 300, 1); scen(d, 'pirate', 0, 2100)
    for x, y in ((150, 700), (10, 1300), (150, 1900), (150, 2500)): P(d, 'balloons', x, y)
    for x, y in ((40, 900), (130, 1500), (40, 2400)): P(d, 'popcorn', x, y)
    lights(d, (200, 600, 1000, 1400, 1800, 2200, 2600))
    H(d, 'ped', 90, 700); H(d, 'ped', 90, 1600, 1); H(d, 'thrower', 150, 1400); H(d, 'pedx', 30, 2000)
    return d


def haunted():
    """HAUNTED HOUSE (side job): dark grounds, gravestones and dead trees, the ghost train track, the house itself.
    Ghosts drift about."""
    d = job('haunted', 'HAUNTED HOUSE', 'themepark', ['helter'], 2200, 60, 9.2, 9, start=[90, 2156], bonus=True)
    G(d, 'stone', 0, 0, 180, 2200); path(d, 'gravel', 40, [(90, 2200), (60, 1800), (120, 1400), (60, 1000), (90, 600), (90, 0)])
    for x, y in ((0, 1900), (130, 1500), (0, 1100), (130, 700)): wild(d, 'park', x, y, 50, 200, x + y, 0.8, 11)
    for x, y in ((60, 1700), (110, 1200), (60, 800)): P(d, 'cairn', x, y)
    dec(d, 'rails', 150, 0, 600); scen(d, 'shop', 0, 0, 34); scen(d, 'shop', 124, 0, 37)
    for y in range(400, 2100, 300): H(d, 'ghost', 40, y, 0); H(d, 'ghost', 130, y + 150, 1)
    over(d, 'lant', 0, 300, 180)
    return d


def coaster():
    """ROLLER COASTER: the big one. Its track crosses the paths at four places; trains roar through."""
    d = job('coaster', 'ROLLER COASTER', 'themepark', ['helter'], 3000, 73, 9.4, 7, start=[90, 2956])
    G(d, 'grass', 0, 0, 180, 3000); G(d, 'pave', 34, 0, 112, 3000); G(d, 'purple', 88, 0, 4, 3000); beds(d, 100, 2800, 61, w=30)
    for k, yc in enumerate((400, 1100, 1800, 2500)):
        G(d, 'wood', 0, yc - 4, 180, 30); H(d, 'cross', 0, yc, 1 if k % 2 == 0 else -1, 4.5, 'coaster')
        P(d, 'warnsign', 50, yc - 30); P(d, 'warnsign', 120, yc + 30)
    for y in range(80, 2950, 240): P(d, 'coasterv', 0, y, 120) if y % 480 == 80 else P(d, 'coasterv', 172, y, 120)
    for x, y in ((20, 700), (140, 1400), (20, 2100), (140, 2800), (140, 300)): P(d, 'balloons', x, y)
    scen(d, 'shop', 0, 2860, 31); P(d, 'mascot', 150, 2840)
    lights(d, (200, 900, 1600, 2300))
    H(d, 'ped', 90, 1300); H(d, 'thrower', 150, 2000); H(d, 'pedx', 50, 1500)
    return d


def flume():
    """LOG FLUME: the flume channel winds through the woods; logs splash down. Boardwalks, the splash zone."""
    d = job('flume', 'LOG FLUME', 'themepark', ['coaster'], 2800, 69, 9.6, 7, start=[90, 104])
    G(d, 'grass', 0, 0, 180, 2800)
    wood(d, 0, 300, 50, 2200, 3) if False else wild(d, 'forest', 0, 300, 44, 2200, 3, 0.8, 9)
    wild(d, 'forest', 150, 300, 30, 2200, 4, 0.8, 9)
    G(d, 'blue', 120, 300, 24, 2200)
    for y in range(360, 2460, 300): P(d, 'log', 125, y)
    G(d, 'deck', 50, 300, 66, 2200)
    for y in range(400, 2500, 200): P(d, 'lamp', 52, y)
    scen(d, 'shop', 0, 0, 38); G(d, 'tile', 0, 0, 180, 300); P(d, 'kiosk', 150, 220, 2)
    G(d, 'tile', 0, 2500, 180, 300); C(d, 'blue', 90, 2650, 50); P(d, 'swan', 80, 2630); P(d, 'balloons', 10, 2700)
    lights(d, (200, 2560))
    H(d, 'ped', 80, 900); H(d, 'pedx', 60, 1600); H(d, 'thrower', 100, 2200)
    return d


def drop():
    """DROP TOWER: the tallest ride in the park on its plaza; the funfair below it; a sky bridge."""
    d = job('drop', 'DROP TOWER', 'themepark', ['flume'], 3000, 71, 9.8, 7, start=[90, 2956])
    G(d, 'slab', 0, 0, 180, 3000); beds(d, 1000, 1350, 71); beds(d, 1700, 2050, 72)
    C(d, 'mosaic', 90, 1500, 80); C(d, 'tile', 90, 1500, 30); scen(d, 'droptower', 79, 1424)
    over(d, 'fbridge', 0, 900, 180); over(d, 'fbridge', 0, 2100, 180)
    for x, y, a in ((0, 300, 0), (124, 500, 1), (0, 700, 2)): scen(d, 'shop', x, y, [33, 35, 36][a])
    for x, y in ((10, 2300), (150, 2500), (10, 2700)): P(d, 'arcade', x, y, x % 5)
    scen(d, 'pirate', 110, 2700)
    lights(d, (200, 1100, 1900, 2400))
    H(d, 'bumper', 70, 600, 3); H(d, 'pedx', 40, 1700); H(d, 'pedx', 120, 2200, 1); H(d, 'thrower', 150, 900)
    return d


def minigolf():
    """MINI GOLF (side job): nine holes on astroturf, windmills, little bridges, a frozen water hazard."""
    d = job('minigolf', 'MINI GOLF', 'themepark', ['drop'], 2400, 64, 9.8, 9, start=[90, 52], bonus=True)
    G(d, 'pave', 0, 0, 180, 2400)
    for k in range(9):
        y0 = 160 + k * 240; x0 = 10 if k % 2 == 0 else 96
        G(d, 'green', x0, y0, 74, 180); P(d, 'hole', x0 + 34, y0 + 30, k % 3)
        if k % 3 == 0: P(d, 'windmill', x0 + 14, y0 + 80)
        elif k % 3 == 1: C(d, 'ice', x0 + 37, y0 + 110, 22)
        else: P(d, 'rock', x0 + 20, y0 + 100, 18)
    scen(d, 'shop', 0, 0, 32); P(d, 'kiosk', 150, 20, 3)
    lights(d, (120, 1000, 1900))
    H(d, 'thrower', 90, 1200); H(d, 'ped', 90, 600)
    return d


def lake():
    """FIREWORKS LAKE: the boardwalk round the frozen lake, swan boats iced in, the fireworks barge."""
    d = job('lake', 'FIREWORKS LAKE', 'themepark', ['drop'], 3000, 71, 10.0, 7, start=[90, 2956])
    G(d, 'deck', 0, 0, 180, 3000)
    wild(d, 'park', 0, 0, 180, 260, 81, 0.6, 12); carve(d, 60, [(90, 0), (90, 270)]); wild(d, 'park', 0, 2700, 180, 300, 82, 0.6, 12); carve(d, 60, [(90, 2700), (90, 3000)])
    G(d, 'ice', 40, 600, 100, 1800); C(d, 'ice', 90, 600, 50); C(d, 'ice', 90, 2400, 50)
    for x, y in ((60, 900), (100, 1100), (70, 1500), (110, 1900)): P(d, 'swan', x, y)
    scen(d, 'stage', 50, 1300, 4)
    for y in (700, 1700, 2600): over(d, 'fireworks', 60, y, y % 4)
    for y in (300, 1000, 2100, 2800): P(d, 'bench', 4, y); P(d, 'bench', 164, y + 100)
    lights(d, (400, 1200, 2000, 2800))
    H(d, 'pedx', 40, 1490); H(d, 'pedx', 140, 2600, 1); H(d, 'thrower', 20, 800); H(d, 'cannon', 2, 1000, 0.3, 7.0, 64)
    return d


def openingday():
    """OPENING DAY (boss): Benny Bear is NOT ready for the crowds. Run the whole park: the coaster crossings, the
    bumper floor, the castle at the end."""
    d = job('openingday', 'OPENING DAY', 'themepark', ['lake'], 3400, 77, 10.5, 9, start=[90, 3356], boss=True)
    G(d, 'slab', 0, 0, 180, 3400); G(d, 'mosaic', 72, 0, 36, 3400); beds(d, 200, 1400, 91); beds(d, 2100, 3200, 92)
    for k, yc in enumerate((2700, 600)):
        G(d, 'wood', 0, yc - 4, 180, 30); H(d, 'cross', 0, yc, 1 if k == 0 else -1, 5.0, 'coaster')
    G(d, 'deck', 10, 1500, 160, 500); wallbox(d, 8, 1498, 172, 2002, [('b', 62, 118), ('t', 62, 118)], kind='rail'); H(d, 'bumper', 30, 1600, 5)
    scen(d, 'castle', 40, 0)
    for x, y in ((10, 3000), (150, 2900), (10, 2400), (150, 2200), (10, 1200), (150, 1000)): P(d, 'balloons', x, y)
    for x, y in ((4, 2500), (150, 800)): scen(d, 'shop', x if x < 90 else 124, y, 32)
    lights(d, (300, 900, 1400, 2100, 2600, 3100))
    for y in (200, 2200): over(d, 'fireworks', 60, y, y % 4)
    H(d, 'chaser', 160, 3000, 'mascot', 5); H(d, 'thrower', 150, 1300); H(d, 'pedx', 40, 2300)
    return d


ALL = [gates, mainst, carousel, games, bumpers, food, ferris, helter, haunted, coaster, flume, drop, minigolf, lake, openingday]


# ---------------------------------------------------------------- densify: second pass of dressing on every job
def islands(d, y0, y1, seed, cx=90, w=24):
    """a chain of centre islands down a wide promenade: planting beds, little fountains, balloon sellers, lamps"""
    r = rng(seed); y = y0; k = 0
    while y < y1 - 70:
        t = k % 4
        if t == 0: wild(d, 'bush', cx - w // 2, y, w, 56, y + seed, 0.95, 7); P(d, 'lamp', cx - 3, y - 26); P(d, 'lamp', cx - 3, y + 58)
        elif t == 1: C(d, 'mosaic', cx, y + 26, 22); C(d, 'tile', cx, y + 26, 14); P(d, 'fountain', cx - 12, y + 14)
        elif t == 2: P(d, 'balloons', cx - 8, y); P(d, 'popcorn', cx - 8, y + 40)
        else: P(d, 'planter', cx - 7, y + 10); P(d, 'planter', cx - 7, y + 40)
        y += r.randint(150, 220); k += 1


def densify(J):
    by = {d['id']: d for d in J}
    from city_pro import shopfronts
    PN = [31, 32, 33, 35, 36, 37, 38, 5, 15, 14]
    d = by['carousel']; islands(d, 1020, 1240, 2)
    shopfronts(d, 'l', 2200, 2600, 301, PN); shopfronts(d, 'r', 2230, 2600, 302, PN)
    for y in (1380, 1440): P(d, 'arcade', 4, y, y % 5); P(d, 'arcade', 18, y, (y + 1) % 5)
    for x, y in ((150, 1650), (10, 1650), (150, 2150), (10, 2150)): P(d, 'bench', x, y)
    scen(d, 'helter', 150, 380); over(d, 'banner', 0, 1580, 180, 3)
    d = by['games']
    for y0 in (120, 1000, 1880):
        G(d, 'red', 86, y0, 8, 700)
        for k, y in enumerate(range(y0 + 60, y0 + 680, 180)): P(d, 'tub', 34, y); P(d, 'tub', 132, y + 90)
        over(d, 'banner', 0, y0 + 10, 180, (y0 // 100) % 4)
    for yc in (900, 1780): over(d, 'fireworks', 60, yc - 60, yc % 4)
    d = by['bumpers']
    shopfronts(d, 'l', 2120, 2420, 331, PN); shopfronts(d, 'r', 2160, 2420, 332, PN)
    for k, y0 in enumerate((300, 1400)):
        for x, y in ((6, y0 - 40), (150, y0 - 40)): P(d, 'booth', x, y, k)
    islands(d, 1040, 1380, 3, cx=40)
    d = by['food']
    shopfronts(d, 'l', 900, 1250, 311, PN); shopfronts(d, 'r', 1800, 2050, 312, PN)
    islands(d, 900, 1250, 5); islands(d, 1800, 2050, 6)
    for x, y in ((4, 300), (150, 860), (4, 1180), (150, 2560)): P(d, 'kiosk', x, y, y % 4)
    d = by['ferris']
    for x, y in ((0, 2600), (150, 2300), (0, 2000), (150, 1700)): wild(d, 'bush', x, y, 30, 80, x + y, 0.95, 7)
    scen(d, 'pirate', 110, 1620); P(d, 'teacups', 0, 1660) if False else scen(d, 'teacups', 0, 1640)
    for y in range(1650, 2750, 160): P(d, 'lamp', 46 if (y // 160) % 2 else 128, y)
    lights(d, (1700, 2100, 2500))
    d = by['helter']
    for x, y in ((150, 160), (0, 1000), (150, 1600), (0, 2250)): wild(d, 'bush', x, y, 30, 90, x + y, 0.95, 7)
    for x, y in ((140, 900), (10, 1500), (140, 2100)): P(d, 'stall', x, y, y % 5)
    scen(d, 'teacups', 110, 2420)
    d = by['coaster']
    for k, y in enumerate((150, 850, 1550, 2250)): scen(d, 'shop', 0 if k % 2 else 124, y + 100, [31, 32, 33, 35][k])
    for y in range(300, 2900, 300): P(d, 'lamp', 36, y); P(d, 'lamp', 140, y + 150)
    d = by['drop']
    shopfronts(d, 'r', 1000, 1380, 321, PN); shopfronts(d, 'l', 1620, 1900, 322, PN)
    islands(d, 200, 900, 7); islands(d, 2150, 2600, 8)
    scen(d, 'bigtop', 104, 1960, 2); scen(d, 'helter', 0, 1950)
    d = by['minigolf']
    for k in range(9):
        y0 = 160 + k * 240; x0 = 96 if k % 2 == 0 else 10
        wild(d, 'bush', 0 if x0 < 90 else 150, y0 + 40, 30, 100, y0 + 9, 0.9, 7)
        P(d, 'flag', x0 + 40 if x0 > 90 else x0 + 30, y0 + 20, k % 4)
    d = by['lake']
    for y in range(500, 2500, 260): P(d, 'lamp', 26, y); P(d, 'lamp', 148, y + 130)
    for x, y in ((4, 640), (150, 1240), (4, 1840), (150, 2340)): P(d, 'kiosk', x, y, y % 4)
    d = by['openingday']
    for y in (2900, 2300, 1100, 500): scen(d, 'helter' if y % 600 else 'teacups', 0 if y % 1200 else 110, y)
    islands(d, 2050, 2650, 9, cx=40); over(d, 'parkgate', 0, 3220, 180)
