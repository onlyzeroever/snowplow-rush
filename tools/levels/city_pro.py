"""City, pro pass. Every job is a walk through a real piece of town, told in beats from the start to a set piece.
Shop name indices: 2 CAFE 3 BOOKS 4 FLOWERS 7 CHEMIST 10 BANK 11 BARBER 12 DELI 13 SHOES 14 PIZZA 15 GIFTS
22 CITY HALL 23 STATION 24 HOSPITAL 25 NOODLES 26 TEA HOUSE 27 DUMPLINGS 28 HOTEL 29 THEATRE 30 ICE RINK
55 COFFEE 56 CINEMA 57 POST OFFICE 58 LIBRARY 59 DINER 60 RECORDS 61 GALLERY 62 TAILOR 63 LAUNDRY 64 JEWELLER
65 MARKET HALL 66 TRAM DEPOT 67 CAR PARK 68 OPERA 69 COURT 70 FLORIST"""
from common import *
import math


def crossing_corners(d, y, h, seed):
    """traffic lights, tactile paving and a drain or two at the four corners of a cross street"""
    r = rng(seed)
    for x in (6, 168):
        P(d, 'tlight', x, y - 30); P(d, 'tlight', x, y + h + 2)
    for x in (22, 146):
        dec(d, 'tactile', x, y - 10); dec(d, 'tactile', x, y + h + 2)
    dec(d, 'drain', r.choice((28, 140)), y - 6); dec(d, 'drain', r.choice((28, 140)), y + h + 3)


def cityhall():
    """CITY HALL: the mayor gives her winter address at noon. Start in Bank Lane, cross the market square and two busy
    streets, run the tree-lined boulevard, open up the Plaza of the Seasons and finish on the steps of City Hall."""
    d = job('cityhall', 'CITY HALL', 'city', ['airport'], 2400, 58, 6.2, 7, start=[92, 2354])
    # ---- BANK LANE (2080-2400): a cobbled lane between shopfronts; vans and bins, a dug-up corner
    G(d, 'cobble', 0, 2080, 180, 320)
    G(d, 'slab', 50, 2096, 10, 304); G(d, 'slab', 122, 2096, 10, 304)
    dec(d, 'kerb', 60, 2096, 304); dec(d, 'kerb', 120, 2096, 304)
    for y, k, a in ((2096, 'shop', 10), (2156, 'shopv', 55), (2228, 'shopv', 62), (2300, 'shopv', 11), (2372, 'shopv', 70)):
        scen(d, k, 0 if k == 'shop' else 6, y, a)
    for y, k, a in ((2104, 'shopv', 64), (2176, 'shop', 3), (2236, 'shopv', 60), (2308, 'shopv', 12)):
        scen(d, k, 124 if k == 'shop' else 136, y, a)
    G(d, 'slab', 44, 2156, 6, 244); G(d, 'slab', 132, 2104, 4, 296)
    P(d, 'van', 110, 2108, 0); P(d, 'bins', 112, 2268); P(d, 'meter', 112, 2320); P(d, 'meter', 112, 2350)
    P(d, 'bikerack', 30, 1846); P(d, 'trash', 52, 2262); P(d, 'hydrant', 52, 2336)
    for x, y in ((80, 2230), (100, 2330), (74, 2384)): dec(d, 'manhole', x, y)
    dec(d, 'crack', 70, 2280, 26, 5); dec(d, 'drain', 62, 2200); dec(d, 'drain', 110, 2380)
    # ---- MARKET SQUARE (1816-2080): the old cobbled square round a street clock; stalls, a cafe terrace
    G(d, 'cobble', 0, 1816, 180, 264)
    C(d, 'pave', 90, 1950, 34); C(d, 'cobble', 90, 1950, 26); C(d, 'pave', 90, 1950, 8)
    P(d, 'clock', 84, 1920)
    for x, y, a in ((6, 1830, 0), (6, 1880, 2), (144, 2016, 1)): P(d, 'stall', x, y, a)
    for x, y, a in ((140, 1836, 0), (156, 1866, 1), (134, 1880, 2)): P(d, 'parasol', x, y, a)
    P(d, 'news', 8, 2030); P(d, 'phonebox', 160, 1940); P(d, 'bench', 60, 1990); P(d, 'bench', 108, 1990)
    P(d, 'planter', 40, 1910); P(d, 'planter', 126, 1960); P(d, 'trash', 70, 1866); P(d, 'postbox', 44, 2040)
    dec(d, 'manhole', 30, 1960); dec(d, 'crack', 150, 1910, 22, 9)
    H(d, 'ped', 30, 1990); H(d, 'ped', 150, 1900, 1); H(d, 'thrower', 104, 1846)
    # ---- KINGS ROAD (1760-1816): two-way cross traffic over a yellow box junction
    street_h(d, 1760, 56, centre='dash')
    dec(d, 'boxj', 30, 1762, 120, 52)
    dec(d, 'zebrah', 2, 1762, 22, 52); dec(d, 'zebrah', 156, 1762, 22, 52)
    crossing_corners(d, 1760, 56, 3)
    H(d, 'cross', 0, 1766, 1, 6, 'car'); H(d, 'cross', 0, 1792, -1, 8, 'car')
    # ---- CIVIC BOULEVARD (1056-1760): two carriageways either side of a tree-lined median, buses both ways
    G(d, 'slab', 0, 1056, 18, 704); G(d, 'slab', 162, 1056, 18, 704)
    street_v(d, 18, 58, 1056, 1760, centre='dash'); street_v(d, 104, 58, 1056, 1760, centre='dash')
    G(d, 'slab', 76, 1056, 28, 704); dec(d, 'kerb', 76, 1056, 704); dec(d, 'kerb', 102, 1056, 704)
    trees_line(d, 90, 1080, 1700, 11, gap=(58, 90), size=(24, 32))
    furniture_line(d, 4, 1080, 1720, 21, ['lamp', 'lamp', 'bins', 'hydrant', 'postbox', 'meter'], gap=(52, 90))
    furniture_line(d, 168, 1100, 1720, 22, ['lamp', 'lamp', 'trash', 'meter', 'phonebox'], gap=(52, 90))
    for y in (1180, 1560): dec(d, 'arrow', 40, y, 1); dec(d, 'arrow', 136, y + 60, 0)
    dec(d, 'bike', 26, 1300); dec(d, 'bike', 146, 1460)
    # mid-block zebra with a refuge, and the roadworks that squeeze the left carriageway
    dec(d, 'zebra', 18, 1392, 58, 14); dec(d, 'zebra', 104, 1392, 58, 14); dec(d, 'tactile', 84, 1382); dec(d, 'tactile', 84, 1410)
    H(d, 'pedx', 20, 1396); H(d, 'pedx', 150, 1400, 1)
    P(d, 'works', 18, 1250, 36); P(d, 'works', 18, 1320, 36); P(d, 'cone', 42, 1270); P(d, 'cone', 44, 1300); P(d, 'skip', 2, 1276)
    dec(d, 'crack', 24, 1270, 30, 4); dec(d, 'oil', 120, 1620, 6, 3)
    for k in range(4): dec(d, 'manhole', (36, 130, 60, 112)[k], (1140, 1240, 1500, 1680)[k])
    H(d, 'taxi', 106, 1100, 2, 1056, 1760); H(d, 'taxi', 34, 1600, 1, 1056, 1760); H(d, 'taxi', 134, 1300, 0, 1056, 1760)
    d['data']['pull'] += [[0, 1460, 2], [158, 1180, 4]]
    # ---- PARLIAMENT STREET (1000-1056)
    street_h(d, 1000, 56, centre='dyl')
    dec(d, 'zebrah', 70, 1002, 40, 52); crossing_corners(d, 1000, 56, 5)
    H(d, 'cross', 0, 1006, -1, 7, 'car'); H(d, 'cross', 0, 1030, 1, 9, 'car')
    # ---- PLAZA OF THE SEASONS (620-1000): sandstone, a compass rose underfoot, fountains, fairy lights overhead
    G(d, 'slab', 0, 620, 180, 380)
    dec(d, 'compass', 90 - 34, 806 - 34, 34)
    for a in range(8):
        tx, ty = 90 + 64 * math.cos(a * math.pi / 4 + 0.39), 806 + 64 * math.sin(a * math.pi / 4 + 0.39)
        dec(d, 'grate', tx - 8, ty - 6); P(d, 'stree', int(tx) - 11, int(ty) - 22, 24)
    for x, y in ((14, 650), (142, 928)): C(d, 'wht', x + 12, y + 12, 17); C(d, 'tile', x + 12, y + 12, 15); P(d, 'fountain', x, y)
    for x, y in ((150, 660), (22, 930)): P(d, 'statue', x, y)
    P(d, 'sculpt', 152, 760); P(d, 'planterl', 0, 760, 32); P(d, 'planterl', 0, 840, 32)
    for x, y in ((60, 700), (110, 700), (60, 912), (110, 912)): P(d, 'bench', x, y)
    over(d, 'lights', 0, 686, 180, 0); over(d, 'lights', 0, 952, 180, 2)
    H(d, 'ped', 40, 760); H(d, 'ped', 140, 860, 1); H(d, 'thrower', 34, 880)
    # ---- CITY HALL (0-620): the hall, its steps and crest, a red carpet to the podium between the flags
    G(d, 'slab', 0, 0, 180, 620)
    scen(d, 'big', 35, 22, 22)
    for k in range(9): G(d, 'wht', 30, 96 + k * 6, 120, 3)
    for x in (8, 168): P(d, 'planter', x - 4, 40)
    for x in (16, 160): P(d, 'statue', x, 120)
    dec(d, 'crest', 90 - 22, 220 - 22, 22)
    G(d, 'red', 80, 260, 20, 330)
    for y in (360, 420, 480, 540): P(d, 'flag', 70, y, (y // 60) % 4); P(d, 'flag', 106, y + 30, (y // 60 + 1) % 4)
    P(d, 'stage', 50, 300, 1); P(d, 'speaker', 52, 338); P(d, 'speaker', 118, 338)
    over(d, 'banner', 0, 432, 180, 0)
    for x, y in ((6, 250), (162, 250), (6, 520), (162, 520)): P(d, 'lamp', x, y)
    P(d, 'planterl', 0, 380, 40); P(d, 'planterl', 140, 460, 40)
    H(d, 'ped', 30, 300); H(d, 'ped', 150, 520, 1); H(d, 'cart', 140, 200)
    d['data']['decor'] += [['bunting', 0, 160, 180]]
    return d


def shopfronts(d, side, y0, y1, seed, names, gap=(0, 0)):
    """staggered shopfronts down one side (44 or 56 wide) using the given shop names"""
    r = rng(seed); y = y0
    while y < y1:
        k = r.choice(('shopv', 'shopv', 'shop'))
        w, h = (44, 72) if k == 'shopv' else (56, 60)
        if y + h > y1 + 8: break
        scen(d, k, 0 if side == 'l' else 180 - w, y, r.choice(names)); y += h + r.randint(*gap)


def chinatown():
    """CHINATOWN: the Lantern Festival is tonight. In through the Dragon Gate, weave the market stalls of Lantern Street,
    skate the frozen jade pond under the red bridge, dodge the dragon dance on Lucky Lane, finish at the temple."""
    d = job('chinatown', 'CHINATOWN', 'city', ['museum'], 2800, 66, 7.0, 7, start=[90, 52])
    names = [25, 26, 27, 71, 72, 73, 74, 75, 76, 15]
    # ---- GATE PLAZA (0-196)
    G(d, 'slab', 0, 0, 180, 196)
    for x in (16, 42, 132, 158): P(d, 'bollard', x, 110)
    dec(d, 'tactile', 60, 112); dec(d, 'tactile', 108, 112)
    P(d, 'lion', 26, 150, 0); P(d, 'lion', 140, 150, 1)
    P(d, 'gpill', 4, 150); P(d, 'gpill', 164, 150)
    over(d, 'garch', 0, 140, 180)
    P(d, 'news', 150, 20); P(d, 'bins', 8, 22); scen(d, 'shelter', 60, 0); P(d, 'stree', 20, 60, 26); P(d, 'stree', 140, 64, 24)
    dec(d, 'grate', 24, 74); dec(d, 'grate', 142, 76); P(d, 'bench', 110, 30); dec(d, 'manhole', 100, 80)
    # ---- LANTERN STREET (196-900): red brick between shopfronts, stalls set out as a slalom, lanterns overhead
    G(d, 'pave', 0, 196, 180, 704)
    shopfronts(d, 'l', 210, 890, 31, names); shopfronts(d, 'r', 236, 890, 32, names)
    for x, y, a in ((58, 310, 0), (94, 430, 1), (58, 560, 2), (94, 690, 3), (60, 810, 1)): P(d, 'stall', x, y, a)
    for y in (260, 380, 500, 620, 740, 860): over(d, 'lant', 40, y, 100)
    for y in (300, 470, 650, 830): P(d, 'lantpost', 46, y)
    for y in (360, 540, 720): P(d, 'lantpost', 126, y)
    for x, y in ((90, 270), (70, 520), (110, 780)): dec(d, 'manhole', x, y)
    dec(d, 'crack', 100, 600, 24, 3); dec(d, 'drain', 50, 400); dec(d, 'drain', 124, 640)
    H(d, 'pedx', 50, 372); H(d, 'pedx', 120, 620, 1); H(d, 'ped', 90, 480); H(d, 'cart', 80, 760)
    # ---- JADE POND GARDEN (900-1260): a pagoda, a frozen pond with a red bridge, stone lanterns, a bamboo grove
    G(d, 'slab', 0, 900, 180, 360)
    path(d, 'gravel', 20, [(24, 910), (24, 1250)]); path(d, 'gravel', 20, [(156, 1000), (156, 1250)])
    C(d, 'stone', 90, 1092, 52); C(d, 'ice', 90, 1092, 47)
    over(d, 'rbridge', 32, 1074, 116)
    scen(d, 'pagoda', 2, 900)
    wild(d, 'bush', 128, 904, 52, 58, 7, 0.95, 8)
    for x, y in ((40, 1032), (130, 1032), (40, 1140), (130, 1140)): P(d, 'stonelamp', x, y)
    for x, y in ((4, 1180), (162, 1180)): P(d, 'planter', x, y)
    P(d, 'bench', 60, 1210); P(d, 'bench', 108, 1210)
    H(d, 'thrower', 156, 1100); H(d, 'ped', 20, 1000)
    # ---- CANAL STREET (1260-1316)
    street_h(d, 1260, 56, centre='dash', zebras=[(70, 40)])
    crossing_corners(d, 1260, 56, 9)
    H(d, 'cross', 0, 1266, 1, 7, 'car'); H(d, 'cross', 0, 1290, -1, 9, 'car')
    # ---- LUCKY LANE (1316-2000): the dragon dance route; hot pot terraces, lanterns
    G(d, 'cobble', 0, 1316, 180, 684); G(d, 'red', 80, 1316, 20, 684)
    shopfronts(d, 'l', 1330, 1600, 41, names); shopfronts(d, 'r', 1340, 1600, 42, names)
    shopfronts(d, 'l', 1720, 1990, 43, names); shopfronts(d, 'r', 1700, 1990, 44, names)
    # a small square opens in the middle of the lane
    G(d, 'slab', 0, 1610, 180, 100); C(d, 'pave', 90, 1660, 30); C(d, 'cobble', 90, 1660, 26)
    P(d, 'urn', 82, 1648)
    for x, y, a in ((10, 1622, 0), (150, 1676, 1)): P(d, 'parasol', x, y, a)
    P(d, 'table', 30, 1690); P(d, 'kiosk', 150, 1620, 1)
    for y in (1380, 1480, 1580, 1760, 1860, 1960): over(d, 'lant', 40, y, 100)
    for y in (1420, 1800, 1930): P(d, 'lantpost', 52, y)
    for y in (1460, 1880): P(d, 'lantpost', 122, y)
    H(d, 'cross', 0, 1470, 1, 10, 'dragon'); H(d, 'cross', 0, 1840, -1, 11, 'dragon')
    H(d, 'pedx', 60, 1540); H(d, 'ped', 110, 1780, 1)
    dec(d, 'manhole', 64, 1400); dec(d, 'manhole', 112, 1900); dec(d, 'crack', 70, 1720, 20, 8)
    # ---- TEMPLE ROAD (2000-2056)
    street_h(d, 2000, 56, centre=None, ground='cobble', kerbs=True, zebras=[(30, 40), (110, 40)])
    H(d, 'pedx', 20, 2026); H(d, 'pedx', 150, 2010, 1)
    # ---- TEMPLE SQUARE (2056-2800): an old coin set in the paving, the incense urn, lions, lanterns, the temple
    G(d, 'slab', 0, 2056, 180, 744)
    C(d, 'pave', 90, 2330, 46); C(d, 'yel', 90, 2330, 36); C(d, 'pave', 90, 2330, 33); G(d, 'red', 78, 2318, 24, 24)
    for y in (2120, 2440, 2560): over(d, 'lant', 0, y, 180)
    for x in (20, 150):
        for y in (2250, 2440, 2540): P(d, 'stonelamp', x, y)
    for x, y in ((30, 2200), (140, 2290), (36, 2420)): P(d, 'stree', x, y, 26)
    G(d, 'red', 80, 2380, 20, 346); P(d, 'urn', 82, 2600); P(d, 'lion', 30, 2680, 0); P(d, 'lion', 136, 2680, 1)
    for x, y, a in ((14, 2330, 0), (150, 2470, 1)): P(d, 'parasol', x, y, a)
    P(d, 'kiosk', 140, 2330, 0); P(d, 'table', 34, 2360); P(d, 'stree', 112, 2600, 30); P(d, 'stree', 46, 2560, 28)
    for x in (4, 162): P(d, 'planter', x, 2620)
    scen(d, 'temple', 28, 2726)
    P(d, 'stage', 50, 2080, 2); P(d, 'speaker', 52, 2118); P(d, 'speaker', 118, 2118)
    H(d, 'ped', 60, 2480); H(d, 'ped', 120, 2380, 1); H(d, 'cart', 40, 2560)
    return d


def junction():
    """DOWNTOWN JUNCTION: rush hour. Out of the car park under the ticket barrier, across the big four-way junction,
    up the bus avenue, round the roundabout with the traffic, through the towers to the motorway interchange."""
    d = job('junction', 'DOWNTOWN JUNCTION', 'city', ['chinatown'], 3000, 81, 7.2, 7, start=[56, 2950])
    # ---- CAR PARK (2700-3000): bays both sides, a row of pillars, the exit barrier
    G(d, 'conc', 0, 2700, 180, 300)
    for y in range(2730, 2980, 40):
        dec(d, 'bay', 0, y, 28, 38); dec(d, 'bay', 152, y, 28, 38)
    r = rng(77)
    for k, y in enumerate(range(2734, 2960, 40)):
        if r.random() < 0.8: P(d, 'car', 2, y, r.randint(0, 4))
        if r.random() < 0.7 and y < 2920: P(d, 'car', 154, y, r.randint(0, 4))
    d['data']['pull'] += [[155, 2934, 1]]
    for y in (2760, 2840, 2920): scen(d, 'pillar', 85, y)
    dec(d, 'arrow', 50, 2860, 0); dec(d, 'arrow', 124, 2780, 1); dec(d, 'oil', 40, 2800, 7, 2); dec(d, 'oil', 110, 2900, 6, 5)
    d['data']['paint'] += [['EXIT', 66, 2724, 2]]
    P(d, 'rail', 0, 2700, 58); P(d, 'rail', 122, 2700, 58); P(d, 'kiosk', 36, 2708, 3)
    H(d, 'barrier', 60, 2699, 62, 5)
    # ---- STATION PLAZA (2440-2700)
    G(d, 'pave', 0, 2440, 180, 260)
    P(d, 'billboard', 4, 2470, 1); P(d, 'billboard', 130, 2560, 4)
    P(d, 'news', 150, 2460); P(d, 'bikerack', 70, 2650); P(d, 'planter', 40, 2600); P(d, 'planter', 120, 2490)
    P(d, 'bins', 6, 2640); P(d, 'signpost', 100, 2540); P(d, 'parasol', 148, 2652, 2)
    for x, y in ((60, 2500), (110, 2610)): dec(d, 'manhole', x, y)
    H(d, 'ped', 40, 2560); H(d, 'ped', 140, 2500, 1)
    # ---- THE BIG JUNCTION (2296-2440): two lanes each way across, a box junction, crossings on every arm
    G(d, 'slab', 0, 2296, 180, 144)
    street_h(d, 2324, 88, centre='dyl')
    dec(d, 'dashh', 4, 2345, 172); dec(d, 'dashh', 4, 2389, 172)
    G(d, 'asph', 52, 2296, 76, 28); G(d, 'asph', 52, 2412, 76, 28)
    dec(d, 'boxj', 52, 2326, 76, 84)
    dec(d, 'zebra', 52, 2300, 76, 18); dec(d, 'zebra', 52, 2418, 76, 18)
    dec(d, 'zebrah', 18, 2326, 26, 84); dec(d, 'zebrah', 136, 2326, 26, 84)
    for x, y in ((40, 2290), (132, 2290), (40, 2414), (132, 2414)): P(d, 'tlight', x, y)
    for x in (6, 162): dec(d, 'tactile', x, 2310); dec(d, 'tactile', x, 2418)
    H(d, 'cross', 0, 2328, 1, 6, 'car'); H(d, 'cross', 0, 2350, 1, 8, 'car'); H(d, 'cross', 0, 2372, -1, 7, 'car'); H(d, 'cross', 0, 2394, -1, 9, 'car')
    # ---- BUS AVENUE (1664-2296): bus lane, two traffic lanes, cycle lane; traffic comes and goes under the bridges
    G(d, 'slab', 0, 1664, 18, 632); G(d, 'red', 18, 1664, 28, 632); street_v(d, 46, 82, 1664, 2296, centre='dash')
    G(d, 'green', 128, 1664, 22, 632); G(d, 'slab', 150, 1664, 30, 632); dec(d, 'kerb', 150, 1664, 632); dec(d, 'kerb', 16, 1664, 632)
    for y in (1760, 2000, 2200): d['data']['paint'] += [['BUS', 22, y, 2]]
    for y in (1720, 1900, 2080, 2250): dec(d, 'bike', 132, y)
    for y in (1800, 2120): dec(d, 'arrow', 64, y, 1); dec(d, 'arrow', 108, y + 40, 0)
    scen(d, 'shelter', 146, 1900); P(d, 'busstop', 150, 2060)
    furniture_line(d, 2, 1690, 2280, 51, ['lamp', 'lamp', 'bins', 'hydrant', 'postbox'], gap=(60, 96))
    furniture_line(d, 166, 1690, 1880, 52, ['lamp', 'trash'], gap=(60, 90)); furniture_line(d, 166, 1940, 2280, 53, ['lamp', 'trash', 'meter'], gap=(60, 90))
    dec(d, 'hatch', 82, 1980, 18, 64); P(d, 'bollard', 88, 1984); P(d, 'bollard', 88, 2036)
    dec(d, 'zebra', 18, 1820, 132, 14); H(d, 'pedx', 20, 1824); H(d, 'pedx', 150, 1826, 1)
    over(d, 'fbridge', 0, 1640, 180); over(d, 'gantry', 0, 2276, 180, 5)
    H(d, 'taxi', 20, 1700, 2, 1652, 2296); H(d, 'taxi', 58, 2100, 1, 1652, 2296); H(d, 'taxi', 102, 1800, 0, 1652, 2296)
    # ---- THE ROUNDABOUT (1160-1640): traffic circles clockwise; pick your moment
    G(d, 'slab', 0, 1160, 180, 480)
    G(d, 'asph', 52, 1160, 76, 480)
    C(d, 'asph', 90, 1400, 82); C(d, 'wht', 90, 1400, 57); C(d, 'asph', 90, 1400, 55)
    C(d, 'conc', 90, 1400, 33); C(d, 'grass', 90, 1400, 30); P(d, 'sculpt', 79, 1380)
    for a in (0.6, 2.5, 4.2): H(d, 'orbit', 90, 1400, 68, a)
    H(d, 'orbit', 90, 1400, 44, 1.6)
    for x, y in ((4, 1180), (150, 1190), (6, 1596), (152, 1590)): P(d, 'stree', x, y, 28)
    for x, y in ((24, 1230), (140, 1560)): P(d, 'planter', x, y)
    dec(d, 'stop', 52, 1316, 76); dec(d, 'stop', 52, 1484, 76)
    dec(d, 'arrowt', 70, 1290, 1); dec(d, 'arrowt', 98, 1500, 0)
    # ---- EXCHANGE STREET (1100-1160)
    street_h(d, 1100, 60, centre='dyl', zebras=[(20, 30), (130, 30)])
    H(d, 'cross', 0, 1106, -1, 7, 'car'); H(d, 'cross', 0, 1132, 1, 8, 'car')
    # ---- FINANCIAL DISTRICT (480-1100): glass towers staggered round little plazas, a taxi rank
    G(d, 'tile', 0, 480, 180, 620); street_v(d, 64, 52, 480, 1100, centre='dash')
    scen(d, 'tower', 0, 500, 0); scen(d, 'towerw', 110, 540, 2); scen(d, 'towerw', 0, 760, 3); scen(d, 'tower', 130, 800, 1)
    scen(d, 'tower', 0, 990, 4)
    P(d, 'fountain', 18, 640); P(d, 'sculpt', 140, 690); P(d, 'planterl', 120, 950, 50); P(d, 'planterl', 0, 900, 40)
    for x, y in ((30, 700), (150, 1000), (40, 1060)): P(d, 'stree', x, y, 24)
    P(d, 'van', 120, 900, 3); P(d, 'clock', 36, 600)
    over(d, 'gantry', 0, 1080, 180, 4); over(d, 'fbridge', 0, 476, 180)
    H(d, 'taxi', 68, 700, 0, 490, 1092); H(d, 'taxi', 92, 900, 1, 490, 1092)
    H(d, 'ped', 30, 860); H(d, 'ped', 150, 620, 1)
    # ---- RING ROAD (380-476)
    street_h(d, 380, 96, centre='dyl'); dec(d, 'dashh', 4, 404, 172); dec(d, 'dashh', 4, 450, 172)
    H(d, 'cross', 0, 386, 1, 5, 'car'); H(d, 'cross', 0, 410, 1, 7, 'car'); H(d, 'cross', 0, 432, -1, 6, 'car'); H(d, 'cross', 0, 454, -1, 8, 'car')
    # ---- INTERCHANGE (0-380): the slip roads split round a hatched island under the big gantry
    G(d, 'asph', 0, 0, 180, 380)
    dec(d, 'edge', 6, 0, 380); dec(d, 'edge', 172, 0, 380); dec(d, 'dashv', 60, 0, 120); dec(d, 'dashv', 118, 0, 120)
    dec(d, 'hatch', 70, 130, 40, 200); P(d, 'rail', 74, 200, 32); P(d, 'rail', 74, 270, 32)
    P(d, 'signpost', 82, 150); P(d, 'billboard', 66, 300, 2)
    P(d, 'van', 4, 220, 2); P(d, 'cone', 32, 210); P(d, 'cone', 32, 236); P(d, 'cone', 34, 262)
    for y in (40, 160, 320): dec(d, 'arrowt', 30, y, 0); dec(d, 'arrowt', 140, y + 20, 1)
    over(d, 'gantry', 0, 70, 180, 0)
    H(d, 'taxi', 140, 100, 0, 0, 380); H(d, 'taxi', 20, 300, 1, 0, 380)
    return d


def tramway(d, h, x=138):
    """a street tramway down the right-hand side, the whole length of the job (the tram runs it end to end)"""
    G(d, 'asph', x, 0, 180 - x, h); dec(d, 'kerb', x - 2, 0, h); dec(d, 'rails', x + 8, 0, h)
    for y in range(140, h, 420): dec(d, 'manhole', x + 30, y)


def station():
    """TRAIN STATION: the evening rush. Off the taxi rank, round the station hall, down two platforms under glass
    canopies past parked trains, over the boards of the level crossing, through the goods yard to the old engine
    on its turntable. A tram runs the street alongside all job long."""
    d = job('station', 'TRAIN STATION', 'city', ['cityhall'], 2800, 68, 6.4, 7, start=[100, 2754])
    tramway(d, 2800); H(d, 'taxi', 144, 300, 4); H(d, 'taxi', 144, 1700, 5)
    # ---- FORECOURT & TAXI RANK (2560-2800)
    G(d, 'slab', 0, 2560, 138, 240)
    for y in (2600, 2640, 2680, 2720): dec(d, 'bay', 0, y, 30, 38)
    P(d, 'car', 3, 2602, 3); P(d, 'car', 3, 2682, 3); d['data']['pull'] += [[3, 2722, 3]]
    P(d, 'bikerack', 100, 2580); P(d, 'bins', 112, 2700); P(d, 'signpost', 60, 2600); P(d, 'clock', 70, 2700)
    d['data']['paint'] += [['TAXI', 34, 2630, 1]]
    # ---- STATION HALL & CONCOURSE (2200-2560)
    G(d, 'tile', 0, 2200, 138, 360)
    scen(d, 'big', 0, 2286, 23)
    for x in (112, 126): P(d, 'turnstile', x, 2250)
    P(d, 'news', 116, 2380); P(d, 'kiosk', 114, 2440, 2); P(d, 'billboard', 4, 2210, 1)
    dec(d, 'crest', 50, 2470, 14); H(d, 'ped', 120, 2300); H(d, 'pedx', 20, 2520)
    # ---- PLATFORMS (1080-2200): two tracks, trains standing, glass canopies, timetable boards
    G(d, 'gravel', 0, 1080, 22, 1120); G(d, 'gravel', 86, 1080, 22, 1120)
    P(d, 'track', 0, 1080, 1120); P(d, 'track', 86, 1080, 1120)
    G(d, 'tile', 22, 1080, 64, 1120); G(d, 'tile', 108, 1080, 30, 1120)
    for x in (24, 82, 110): G(d, 'yel', x, 1080, 2, 1120)
    P(d, 'train', 0, 1130, 300); P(d, 'train', 86, 1640, 236); P(d, 'train', 86, 1150, 150)
    P(d, 'buffer', 86, 2186); P(d, 'buffer', 0, 2186)
    over(d, 'canopy', 22, 1180, 64, 380); over(d, 'canopy', 22, 1700, 64, 420); over(d, 'canopy', 108, 1400, 30, 520)
    for y in (1240, 1500, 1820, 2060): P(d, 'bench', 28, y)
    P(d, 'trash', 28, 1960); P(d, 'trash', 28, 1420); P(d, 'signal', 26, 1100)
    H(d, 'ped', 46, 1400); H(d, 'ped', 116, 1880, 1); H(d, 'cart', 110, 1700)
    # ---- LEVEL CROSSING & FOOTBRIDGE (1000-1080)
    G(d, 'wood', 0, 1000, 138, 80); over(d, 'fbridge', 0, 1018, 180)
    for x in (0, 86): P(d, 'track', x, 980, 20)
    # ---- GOODS YARD (380-1000): sidings with wagons, stacked freight, the signal box
    G(d, 'gravel', 0, 380, 138, 620)
    P(d, 'track', 0, 380, 620); P(d, 'track', 116, 380, 620)
    P(d, 'wagon', 0, 420, 0); P(d, 'wagon', 0, 484, 2); P(d, 'wagon', 0, 720, 1); P(d, 'wagon', 116, 600, 3); P(d, 'wagon', 116, 664, 4)
    for x, y in ((24, 560), (38, 560), (24, 574)): P(d, 'crate', x, y)
    for x, y in ((96, 820), (104, 820)): P(d, 'barrel', x, y)
    P(d, 'tires', 24, 860); P(d, 'signal', 26, 400)
    dec(d, 'oil', 50, 700, 7, 3); H(d, 'cart', 60, 560)
    # ---- ENGINE SHED & TURNTABLE (0-380)
    G(d, 'conc', 0, 0, 138, 380)
    scen(d, 'big', 14, 0, 66)
    dec(d, 'turntable', 70 - 44, 240 - 44, 44); P(d, 'loco', 58, 200)
    P(d, 'track', 58, 284, 96); P(d, 'buffer', 58, 366)
    for x, y in ((6, 120), (120, 120), (6, 340)): P(d, 'lamp', x, y)
    P(d, 'barrel', 4, 70); P(d, 'barrel', 12, 70); H(d, 'ped', 120, 260)
    return d


def hospital():
    """HOSPITAL: keep the ambulance route open. From the healing garden, past the busy car park and the helipad, up the
    ambulance drive between the wards to A&E; once the drive is clear the paramedic heads out."""
    d = job('hospital', 'HOSPITAL', 'city', ['station'], 2600, 75, 6.6, 7, start=[90, 2556])
    # ---- A&E (0-340)
    G(d, 'conc', 0, 0, 180, 340)
    scen(d, 'big', 35, 0, 24)
    G(d, 'red', 46, 96, 88, 120); dec(d, 'hatch', 50, 100, 80, 26)
    P(d, 'van', 48, 140, 5); P(d, 'van', 112, 150, 5)
    over(d, 'canopy', 34, 60, 112, 40)
    d['data']['paint'] += [['AMBULANCE', 54, 226, 1]]
    P(d, 'planter', 4, 80); P(d, 'planter', 162, 80); P(d, 'bench', 8, 280); P(d, 'bench', 160, 280)
    # ---- AMBULANCE DRIVE between the wards (340-1040)
    G(d, 'slab', 0, 340, 180, 700); street_v(d, 48, 84, 340, 1040, centre='dash')
    G(d, 'red', 90, 340, 42, 700)
    for y in (420, 640, 860): d['data']['paint'] += [['AMBULANCE', 94, y, 1]]
    scen(d, 'towerw', 0, 380, 1); scen(d, 'towerw', 0, 760, 2); scen(d, 'tower', 0, 470, 1)
    scen(d, 'tower', 134, 360, 2); scen(d, 'tower', 134, 640, 4); scen(d, 'tower', 134, 920, 1)
    d['data']['neighbours'] = [dict(rects=[[90, 360, 42, 670]], path=[[110, 1060], [110, 360], [110, 200]])]
    H(d, 'ped', 60, 560); H(d, 'pedx', 50, 980)
    # ---- HOSPITAL ROAD (1040-1100)
    street_h(d, 1040, 60, centre='dyl', zebras=[(66, 48)]); crossing_corners(d, 1040, 60, 13)
    H(d, 'cross', 0, 1046, 1, 7, 'car'); H(d, 'cross', 0, 1072, -1, 8, 'car')
    # ---- HELIPAD (1100-1400)
    G(d, 'conc', 0, 1100, 180, 300); C(d, 'asph', 90, 1250, 62); dec(d, 'heli', 90 - 46, 1250 - 46, 46)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4; P(d, 'bollard', int(90 + 70 * math.cos(a)) - 2, int(1250 + 70 * math.sin(a)) - 6)
    scen(d, 'heli', 140, 1110); P(d, 'flag', 20, 1120, 1); P(d, 'flag', 160, 1370, 1)
    # ---- CAR PARK (1400-2100): rows of bays, pay machines, trolleys, a barrier at the gate
    G(d, 'asph', 0, 1400, 180, 700)
    r = rng(91)
    for row, y in enumerate(range(1440, 2060, 120)):
        for x in range(4, 176, 30):
            dec(d, 'bay', x, y, 28, 36)
            if r.random() < 0.55 and not (60 < x < 120): P(d, 'car', x + 2, y + 2, r.randint(0, 4))
        if row % 2: d['data']['pull'].append([64, y + 2, row % 5])
    for x, y in ((150, 1416), (6, 2076)): P(d, 'meter', x, y)
    dec(d, 'arrow', 86, 1500, 0); dec(d, 'arrow', 86, 1860, 0); H(d, 'cart', 90, 1700); H(d, 'cart', 100, 1980)
    H(d, 'barrier', 60, 2096, 60, 6); P(d, 'rail', 0, 2096, 58); P(d, 'rail', 122, 2096, 58); P(d, 'kiosk', 130, 2104, 3)
    # ---- HEALING GARDEN (2110-2600): winding paths, a frozen pond, bare trees and benches
    G(d, 'grass', 0, 2110, 180, 490)
    path(d, 'gravel', 30, [(90, 2600), (60, 2500), (110, 2400), (60, 2300), (90, 2200), (90, 2110)])
    C(d, 'stone', 140, 2330, 26); C(d, 'ice', 140, 2330, 22)
    for x, y, s in ((10, 2160, 30), (150, 2150, 26), (20, 2400, 28), (140, 2480, 24), (8, 2540, 26)): P(d, 'stree', x, y, s)
    P(d, 'bench', 30, 2260); P(d, 'bench', 120, 2420); P(d, 'sculpt', 14, 2310); P(d, 'planter', 160, 2220)
    H(d, 'ped', 40, 2350); H(d, 'ped', 120, 2200, 1)
    return d


def museum():
    """MUSEUM: the dinosaur gallery opens tomorrow. Start among the food trucks of the museum quarter, wander the
    sculpture park, sweep the formal garden's gravel walks, and finish on the forecourt under the T-rex."""
    d = job('museum', 'MUSEUM', 'city', ['hospital'], 2600, 71, 6.8, 7, start=[90, 2556])
    # ---- MUSEUM QUARTER (2000-2600): cobbles, galleries and food trucks
    G(d, 'cobble', 0, 2000, 180, 600)
    for y, k, a in ((2010, 'shopv', 61), (2082, 'shopv', 58), (2154, 'shop', 2), (2214, 'shopv', 3), (2380, 'shopv', 15), (2452, 'shop', 55)):
        scen(d, k, 0, y, a)
    for y, k, a in ((2030, 'shop', 59), (2090, 'shopv', 60), (2300, 'shopv', 61), (2372, 'shop', 14), (2432, 'shopv', 70)):
        scen(d, k, 124 if k == 'shop' else 136, y, a)
    for x, y, a in ((60, 2120, 0), (100, 2240, 1), (62, 2470, 2)): P(d, 'foodtruck', x, y, a)
    for x, y, a in ((104, 2296, 0), (106, 2340, 3)): P(d, 'parasol', x, y, a)
    P(d, 'table', 120, 2322); P(d, 'bikerack', 100, 2016)
    for x, y in ((170, 2200), (6, 2300), (170, 2540)): P(d, 'lamp', x, y)
    H(d, 'pedx', 60, 2160); H(d, 'ped', 110, 2420, 1); H(d, 'thrower', 120, 2560)
    # ---- GALLERY STREET (1940-2000)
    street_h(d, 1940, 60, centre='dash', zebras=[(20, 36), (124, 36)])
    H(d, 'cross', 0, 1946, -1, 7, 'car'); H(d, 'cross', 0, 1972, 1, 9, 'car')
    # ---- SCULPTURE PARK (1340-1940): lawns, a winding gravel walk, art and an ice sculpture
    G(d, 'grass', 0, 1340, 180, 600)
    path(d, 'gravel', 34, [(90, 1940), (50, 1820), (130, 1680), (60, 1520), (90, 1340)])
    P(d, 'icesculpt', 120, 1820); P(d, 'sculpt', 20, 1640); P(d, 'statue', 150, 1560); P(d, 'statue', 30, 1420)
    for x, y, s in ((140, 1380, 30), (8, 1500, 28), (150, 1460, 24), (10, 1860, 26)): P(d, 'stree', x, y, s)
    P(d, 'bench', 100, 1600); P(d, 'bench', 34, 1760); C(d, 'stone', 140, 1640, 20); C(d, 'ice', 140, 1640, 16)
    H(d, 'ped', 70, 1700); H(d, 'thrower', 150, 1700)
    # ---- FORMAL GARDEN (620-1340): hedge parterres either side of a gravel avenue, a round fountain court between
    G(d, 'gravel', 0, 620, 180, 720)
    for y in (660, 1140):
        for x in (0, 132):
            wallbox(d, x, y, x + 48, y + 160, [], kind='hedge'); wild(d, 'bush', x + 10, y + 10, 28, 140, x + y, 0.9, 9)
    for x, y in ((60, 636), (106, 636), (60, 1310), (106, 1310)): P(d, 'planter', x, y)
    C(d, 'slab', 90, 980, 60); C(d, 'pave', 90, 980, 56); C(d, 'slab', 90, 980, 28); C(d, 'wht', 90, 980, 18); C(d, 'tile', 90, 980, 16); P(d, 'fountain', 77, 966)
    for x, y in ((8, 900), (164, 900), (8, 1050), (164, 1050)): P(d, 'statue', x, y)
    H(d, 'ped', 90, 820); H(d, 'pedx', 70, 1300)
    # ---- FORECOURT & MUSEUM (0-620): the dinosaur, banners, flags, the grand steps
    G(d, 'slab', 0, 0, 180, 620)
    scen(d, 'museum', 30, 20)
    for k in range(9): G(d, 'wht', 28, 82 + k * 6, 124, 3)
    for x in (10, 166): P(d, 'flag', x, 120, 2); P(d, 'flag', x, 200, 0)
    dec(d, 'compass', 90 - 30, 420 - 30, 30); P(d, 'dino', 54, 270)
    over(d, 'banner', 0, 196, 180, 5)
    for x, y in ((6, 470), (150, 470)): P(d, 'fountain', x, y)
    for x, y in ((20, 560), (150, 520)): P(d, 'stree', x, y, 28)
    P(d, 'bench', 60, 540); P(d, 'bench', 108, 540); H(d, 'ped', 60, 520); H(d, 'cart', 140, 420)
    return d


def icerink():
    """ICE RINK (side job): an open-air rink under fairy lights. Two resurfacers lap the ice, skaters weave about,
    and the whole rink is slippery once you've scraped it."""
    d = job('icerink', 'ICE RINK', 'city', ['junction'], 2200, 64, 7.2, 9, start=[146, 2150], bonus=True)
    # ---- ENTRANCE (1880-2200)
    G(d, 'slab', 0, 1880, 180, 320)
    scen(d, 'big', 0, 2096, 30)
    P(d, 'kiosk', 4, 1900, 3); P(d, 'kiosk', 24, 1900, 1); P(d, 'parasol', 46, 1960, 0); P(d, 'table', 64, 1990); P(d, 'parasol', 8, 2010, 2)
    P(d, 'bins', 158, 1890); P(d, 'bench', 162, 1990); P(d, 'stree', 150, 2100, 26)
    # ---- THE RINK (300-1880): hockey markings, boards with four gates, an ice sculpture in the middle
    G(d, 'conc', 0, 300, 180, 1580)
    G(d, 'ice', 6, 330, 168, 1520)
    G(d, 'red', 14, 1088, 152, 3); G(d, 'blue', 14, 820, 152, 3); G(d, 'blue', 14, 1360, 152, 3)
    for cx, cy in ((50, 600), (130, 600), (50, 1580), (130, 1580)): C(d, 'red', cx, cy, 18); C(d, 'ice', cx, cy, 16); C(d, 'red', cx, cy, 2)
    wallbox(d, 0, 322, 180, 1858, [('t', 60, 120), ('b', 60, 120)], kind='rail')
    P(d, 'icesculpt', 75, 1060)
    for x, y in ((50, 720), (126, 760), (50, 1420), (126, 1460)): P(d, 'cone', x, y)
    H(d, 'orbit', 90, 520, 52, 0, 'zam'); H(d, 'orbit', 90, 1640, 52, 3, 'zam')
    H(d, 'pedx', 30, 900); H(d, 'pedx', 140, 1280, 1); H(d, 'ped', 60, 1200); H(d, 'ped', 120, 980, 1)
    for y in (500, 1100, 1700): over(d, 'lights', 0, y, 180, y % 3)
    # ---- STANDS (0-300)
    G(d, 'conc', 0, 0, 180, 300)
    scen(d, 'stand', 0, 0, 180); scen(d, 'scoreboard', 65, 44)
    P(d, 'kiosk', 10, 220, 0); P(d, 'kiosk', 150, 220, 2); H(d, 'thrower', 90, 200)
    return d


def skyline():
    """SKYLINE PLAZA: the wind whips between the towers. A run of plazas zig-zags down between the glass: frozen water
    steps, a sculpture court under a sky bridge, the lunchtime food court, a glass atrium, the wind gap."""
    d = job('skyline', 'SKYLINE PLAZA', 'city', ['junction'], 3200, 73, 7.4, 7, start=[90, 52], squall=1)
    G(d, 'tile', 0, 0, 180, 3200)
    # lobby
    P(d, 'planterl', 10, 120, 40); P(d, 'planterl', 130, 120, 40); P(d, 'sculpt', 140, 20); P(d, 'bins', 10, 20)
    dec(d, 'crest', 72, 160, 18)
    # towers stagger down the job, leaving a plaza on alternate sides
    for k, y in enumerate((260, 780, 1300, 1820, 2340)):
        if k % 2 == 0: scen(d, 'towerw', 0, y, k % 5); scen(d, 'tower', 130, y + 120, (k + 2) % 5)
        else: scen(d, 'tower', 0, y + 110, (k + 1) % 5); scen(d, 'towerw', 110, y, (k + 3) % 5)
    # frozen water steps (300-700)
    for k in range(8): G(d, 'ice' if k % 2 == 0 else 'slab', 74, 360 + k * 40, 80, 40)
    P(d, 'planter', 76, 330); P(d, 'planter', 140, 680)
    # sculpture court under the sky bridge (800-1220)
    over(d, 'fbridge', 0, 900, 180); C(d, 'slab', 110, 1060, 40); dec(d, 'starm', 110 - 22, 1060 - 22, 22); P(d, 'statue', 106, 1050)
    P(d, 'bench', 60, 1000); P(d, 'bench', 150, 1120)
    # food court (1320-1740)
    for x, y, a in ((4, 1420, 0), (4, 1580, 2)): P(d, 'foodtruck', x, y, a)
    for x, y, a in ((34, 1440, 1), (34, 1610, 3)): P(d, 'parasol', x, y, a)
    P(d, 'table', 36, 1520); P(d, 'van', 150, 1640, 2); H(d, 'ped', 100, 1500); H(d, 'cart', 120, 1700)
    # glass atrium (1840-2260)
    over(d, 'canopy', 60, 1880, 120, 340)
    for x, y in ((80, 1920), (140, 2000), (80, 2100), (150, 2180)): P(d, 'planter', x, y)
    P(d, 'sculpt', 110, 2040); H(d, 'pedx', 70, 2200)
    # the wind gap (2360-2860): narrows between the towers, warning signs
    P(d, 'warnsign', 64, 2380); P(d, 'warnsign', 104, 2850); dec(d, 'hatch', 62, 2480, 40, 60); H(d, 'thrower', 90, 2620)
    # observation plaza (2860-3200)
    dec(d, 'compass', 90 - 36, 3040 - 36, 36)
    for x in (10, 150): P(d, 'flag', x, 2900, 3); P(d, 'flag', x, 3120, 1)
    P(d, 'bench', 30, 3160); P(d, 'bench', 140, 3160); H(d, 'ped', 40, 3000); H(d, 'ped', 140, 3080, 1)
    for y in (240, 1280, 2320): over(d, 'lights', 0, y, 180, y % 4)
    return d


def parade():
    """NEW YEAR PARADE (boss): clear the parade route before midnight with the Warden on your tail. From the float
    assembly yard, up the avenue between the crowds and the grandstand, through the square under the giant snowman
    balloon, over the river bridge to the clock tower for the countdown."""
    d = job('parade', 'NEW YEAR PARADE', 'city', ['skyline'], 3400, 91, 7.6, 9, start=[90, 3354], boss=True)
    # ---- ASSEMBLY YARD (3120-3400)
    G(d, 'asph', 0, 3120, 180, 280)
    for x, y, a in ((4, 3140, 0), (150, 3160, 1), (4, 3260, 2)): P(d, 'foodtruck', x, y, a)
    P(d, 'stage', 100, 3250, 2); P(d, 'speaker', 100, 3288); P(d, 'speaker', 166, 3288)
    H(d, 'ped', 60, 3200); H(d, 'ped', 120, 3180, 1)
    # ---- THE AVENUE (2440-3120): red carpet, crowds behind barriers, a grandstand
    G(d, 'asph', 0, 2440, 180, 680); G(d, 'red', 50, 2440, 80, 680)
    for y in range(2460, 3100, 70):
        P(d, 'rail', 22, y, 30) if y % 140 else None
    scen(d, 'crowd', 0, 2470, 20); scen(d, 'crowd', 0, 2700, 20); scen(d, 'crowd', 0, 2900, 20)
    scen(d, 'stand', 140, 2480, 40); scen(d, 'stand', 140, 2780, 40)
    for y in (2520, 2700, 2880, 3060): over(d, 'lant' if y % 2 else 'lights', 0, y, 180, 1)
    H(d, 'thrower', 40, 2820)
    # ---- MARKET CROSS (2380-2440)
    G(d, 'asph', 0, 2380, 180, 60); H(d, 'cross', 0, 2388, 1, 6.5, 'float')
    # ---- THE SQUARE (1720-2380): confetti stars underfoot, the giant balloon overhead
    G(d, 'slab', 0, 1720, 180, 660)
    for x, y in ((30, 1800), (130, 1900), (50, 2100), (140, 2260), (70, 2300)): dec(d, 'starm', x, y, 8)
    over(d, 'balloon', 68, 1980, 0); P(d, 'fountain', 78, 2090)
    scen(d, 'crowd', 0, 1760, 40); scen(d, 'crowd', 140, 2200, 40)
    for x, y in ((8, 1960), (156, 1860), (10, 2300)): P(d, 'stree', x, y, 26)
    P(d, 'kiosk', 150, 2000, 2); P(d, 'kiosk', 6, 2140, 1); H(d, 'ped', 120, 1800); H(d, 'pedx', 30, 2240)
    # ---- RIVER CROSS (1660-1720)
    G(d, 'asph', 0, 1660, 180, 60); H(d, 'cross', 0, 1668, -1, 7.5, 'float')
    # ---- THE BRIDGE (900-1660): a frozen river either side of the deck
    G(d, 'deck', 36, 900, 108, 760)
    wild(d, 'ice', 0, 900, 34, 760, 41, 0.5, 11); wild(d, 'ice', 146, 900, 34, 760, 42, 0.5, 11)
    P(d, 'railv', 34, 900, 760); P(d, 'railv', 141, 900, 760)
    for y in (960, 1160, 1360, 1560): P(d, 'lamp', 38, y); P(d, 'lamp', 134, y + 100)
    over(d, 'lant', 36, 1120, 108); over(d, 'lant', 36, 1440, 108); H(d, 'pedx', 50, 1260)
    # ---- CLOCK TOWER SQUARE (0-900): the countdown
    G(d, 'cobble', 0, 0, 180, 900)
    scen(d, 'clocktower', 64, 10)
    P(d, 'stage', 50, 220, 4); P(d, 'speaker', 52, 258); P(d, 'speaker', 118, 258)
    over(d, 'banner', 0, 330, 180, 7)
    scen(d, 'crowd', 0, 120, 40); scen(d, 'crowd', 140, 120, 40); scen(d, 'crowd', 0, 520, 30); scen(d, 'crowd', 150, 600, 30)
    for x, y in ((40, 700), (130, 760)): dec(d, 'starm', x, y, 10)
    for y in (420, 640, 820): over(d, 'lights', 0, y, 180, y % 5)
    H(d, 'thrower', 120, 460)
    H(d, 'chaser', 160, 3000, 'warden', 5)
    return d
