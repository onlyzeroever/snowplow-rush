"""Farmland part 2, pro pass. Real farm country: hedgerows and dry-stone walls dividing the land, muddy tracks, frozen
ponds and streams, yards full of kit, animals in their fields. Shop names: 16 FARM SHOP 17 DAIRY 18 STABLES
19 THE MILL 20 SHOW RING 21 TEA ROOM"""
from common import *
import math


def hedgerow(d, x, y, w, h, seed):
    """a thick hedgerow with the odd tree in it (blocks, fills itself with scenery)"""
    wild(d, 'bush', x, y, w, h, seed, 0.95, 8)


def wood(d, x, y, w, h, seed, dens=0.8):
    wild(d, 'forest', x, y, w, h, seed, dens, 9)


def milkshed():
    """MILKING SHED: early milking. From the lane, through the cow field to the muddy yard where the milk tanker waits,
    past the dairy and its churns, out to the frozen duck pond and the farmhouse."""
    d = job('milkshed', 'MILKING SHED', 'farm', ['village'], 1300, 86, 2.65, 6, start=[90, 1262])
    G(d, 'grass', 0, 0, 180, 1300)
    # the lane in (1180-1300), hedges either side
    G(d, 'dirt', 62, 1120, 56, 180); path(d, 'gravel', 12, [(76, 1300), (76, 1120)]); path(d, 'gravel', 12, [(104, 1300), (104, 1120)])
    hedgerow(d, 0, 1150, 56, 150, 1); hedgerow(d, 124, 1160, 56, 140, 2)
    P(d, 'signpost', 60, 1150); P(d, 'churn', 112, 1200); P(d, 'churn', 112, 1210)
    # cow field (760-1120): stone walls with a gate, cows grazing, a trough and a feeder
    P(d, 'stonewall', 0, 1110, 70); P(d, 'stonewall', 110, 1110, 70)
    G(d, 'dirt', 70, 1080, 40, 40)
    for x, y in [(30, 860), (130, 920), (60, 1000), (140, 1040), (100, 820)]: H(d, 'cow', x, y)
    P(d, 'trough', 10, 960); P(d, 'hay', 150, 800); P(d, 'hay', 150, 812); P(d, 'oak', 6, 780)
    dec(d, 'puddle', 120, 980, 9); dec(d, 'puddle', 40, 1060, 7)
    P(d, 'stonewall', 0, 752, 70); P(d, 'stonewall', 110, 752, 70)
    # the yard (420-752): muddy concrete, the milking shed, the tanker, churns and the silo pair
    G(d, 'conc', 0, 420, 180, 332); G(d, 'dirt', 50, 600, 80, 140)
    for x, y in ((20, 640), (150, 700), (90, 560)): dec(d, 'puddle', x, y, 8)
    scen(d, 'barn', 0, 430); scen(d, 'shop', 124, 430, 17); P(d, 'silo', 20, 370); P(d, 'silo', 42, 370)
    P(d, 'trailer', 150, 560); P(d, 'tractor', 20, 600, 1)
    for x in (66, 74, 82): P(d, 'churn', x, 520)
    P(d, 'trough', 110, 720); P(d, 'sacks', 30, 712); dec(d, 'oil', 120, 640, 6, 2)
    H(d, 'cart', 100, 640); H(d, 'cow', 140, 680)
    # pond & orchard (160-420)
    G(d, 'grass', 0, 160, 180, 260); C(d, 'stone', 110, 300, 40); C(d, 'ice', 110, 300, 35)
    P(d, 'reed', 76, 280); P(d, 'reed', 140, 320); P(d, 'reed', 120, 268); P(d, 'bench', 140, 360)
    for x, y in ((10, 200), (30, 300), (10, 380)): P(d, 'oak', x, y)
    # farmhouse at the top (0-160)
    G(d, 'gravel', 0, 0, 180, 160)
    scen(d, 'house', 50, 0); P(d, 'well', 14, 90); P(d, 'tub', 150, 90); P(d, 'scarecrow', 150, 30)
    wood(d, 0, 0, 40, 70, 5, 0.8); wood(d, 140, 0, 40, 70, 6, 0.8)
    return d


def treefarm():
    """PINE TREE FARM: the cutting season. Plantation blocks of pines with lanes between them; the netting shed,
    tractor and trailer of cut trees, the sales hut at the gate."""
    d = job('treefarm', 'PINE TREE FARM', 'farm', ['milkshed'], 1400, 92, 2.7, 6, start=[90, 48])
    G(d, 'grass', 0, 0, 180, 1400)
    # gate & sales hut (0-180)
    G(d, 'gravel', 0, 0, 180, 180)
    scen(d, 'shop', 0, 0, 16); scen(d, 'cabin', 136, 4)
    P(d, 'parasol', 64, 100, 1); P(d, 'table', 84, 120); P(d, 'signpost', 150, 120); P(d, 'trailer', 150, 140)
    over(d, 'lights', 0, 70, 180, 3)
    # plantation: blocks of pines, a cross lane, the main track down the middle
    G(d, 'dirt', 62, 180, 56, 1220); path(d, 'gravel', 10, [(72, 180), (72, 1400)]); path(d, 'gravel', 10, [(108, 180), (108, 1400)])
    for k, y in enumerate(range(200, 1340, 230)):
        for x, w in ((0, 58), (122, 58)):
            wild(d, 'forest', x, y, w, 170, 30 + k * 3 + x, 0.9, 8)
        G(d, 'dirt', 0, y + 170, 180, 60)
    # cutting gang and kit in the cross lanes
    P(d, 'tractor', 20, 386, 0); P(d, 'trailer', 140, 618); P(d, 'sacks', 10, 840); P(d, 'hay', 150, 1076)
    for x, y in ((40, 400), (150, 860)): P(d, 'pine', x, y, 16)
    H(d, 'ped', 30, 620); H(d, 'ped', 150, 1080, 1); H(d, 'thrower', 140, 400); H(d, 'cow', 30, 1300)
    # the netting shed at the bottom
    scen(d, 'barn', 58, 1330); P(d, 'well', 10, 1350)
    return d


def sheepfields():
    """SHEEP FIELDS: four walled fields down the hill, each with its own flock. Gates in the walls, a stream with a
    stone bridge, the shepherd's hut, hay racks."""
    d = job('sheepfields', 'SHEEP FIELDS', 'farm', ['treefarm'], 1400, 88, 2.75, 6, start=[90, 1356])
    G(d, 'grass', 0, 0, 180, 1400)
    path(d, 'dirt', 26, [(90, 1400), (70, 1200), (110, 1000), (80, 800), (100, 600), (80, 400), (100, 200), (90, 0)])
    for y in (1100, 760, 420):
        P(d, 'stonewall', 0, y, 60); P(d, 'stonewall', 120, y, 60)
        P(d, 'gatepole', 58, y - 4); P(d, 'gatepole', 118, y - 4)
    # the stream and its bridge (580-620)
    G(d, 'ice', 0, 590, 180, 22); G(d, 'stone', 64, 586, 52, 30)
    P(d, 'stonewall', 60, 584, 6); P(d, 'stonewall', 114, 584, 6); P(d, 'stonewall', 60, 614, 6); P(d, 'stonewall', 114, 614, 6)
    for x, y in ((20, 600), (150, 596)): P(d, 'reed', x, y - 8)
    # flocks
    H(d, 'sheep', 110, 1200, 6); H(d, 'sheep', 40, 880, 6); H(d, 'sheep', 120, 480, 5); H(d, 'sheep', 50, 180, 6)
    # hay racks, troughs, the hut
    for x, y in ((150, 1220), (14, 940), (150, 520), (14, 260)): P(d, 'hay', x, y); P(d, 'trough', x - 6 if x > 90 else x, y + 30)
    scen(d, 'cabin', 136, 4); P(d, 'well', 14, 40)
    hedgerow(d, 0, 0, 30, 140, 7); hedgerow(d, 160, 1250, 20, 150, 8)
    for x, y in ((150, 820), (20, 1300), (156, 300)): P(d, 'oak', x, y)
    H(d, 'thrower', 150, 960)
    return d


def stables():
    """STABLES: the riding school. Up from the horsebox park, past the stable block and its muck heap, round the
    paddocks with the horses, through the jumping arena."""
    d = job('stables', 'STABLES', 'farm', ['sheepfields'], 1500, 92, 2.8, 6, start=[90, 1456])
    G(d, 'grass', 0, 0, 180, 1500)
    # horsebox park (1300-1500)
    G(d, 'gravel', 0, 1300, 180, 200)
    for x in (4, 154): P(d, 'trailer', x, 1340); P(d, 'trailer', x, 1420)
    P(d, 'signpost', 40, 1460)
    # stable block & yard (980-1300)
    G(d, 'cobble', 0, 980, 180, 320); scen(d, 'shop', 0, 1000, 18); scen(d, 'barn', 116, 990)
    G(d, 'dirt', 120, 1200, 60, 60); P(d, 'sacks', 140, 1210); P(d, 'hay', 120, 1180); P(d, 'hay', 132, 1180)
    for x, y in ((60, 1100), (100, 1130)): P(d, 'trough', x, y)
    P(d, 'well', 10, 1240); H(d, 'cart', 90, 1220)
    # paddocks (520-980): two railed paddocks either side of the track, horses inside
    G(d, 'dirt', 64, 520, 52, 460)
    wallbox(d, 0, 540, 60, 960, [('r', 720, 780)], kind='rail'); wallbox(d, 120, 540, 180, 960, [('l', 640, 700)], kind='rail')
    H(d, 'sheep', 20, 600, 3, 'horse'); H(d, 'sheep', 136, 820, 3, 'horse')
    P(d, 'oak', 6, 880); P(d, 'trough', 136, 560)
    # jumping arena (100-520): sand, a course of jumps
    G(d, 'sand', 10, 120, 160, 380); wallbox(d, 4, 110, 176, 510, [('b', 64, 116), ('t', 64, 116)], kind='rail')
    for x, y in ((40, 200), (110, 260), (40, 340), (110, 420), (76, 160)): P(d, 'hurdle', x, y)
    H(d, 'sheep', 120, 180, 2, 'horse')
    # the yard house at the top
    G(d, 'gravel', 0, 0, 180, 100); scen(d, 'house', 0, 0); P(d, 'tub', 150, 40); wood(d, 100, 0, 80, 60, 9)
    return d


def farmcafe():
    """FARM SHOP: Saturday morning. From the tea room terrace, past the farm shop and the pumpkin patch, round the
    car park, by the duck pond and play barn, down to the pick-your-own field."""
    d = job('farmcafe', 'FARM SHOP', 'farm', ['stables'], 1500, 94, 2.85, 6, start=[90, 48])
    G(d, 'grass', 0, 0, 180, 1500)
    # tea room & terrace (0-260)
    G(d, 'pave', 0, 0, 180, 260); scen(d, 'shop', 0, 0, 21); scen(d, 'shop', 124, 0, 16)
    for x, y, a in ((70, 80, 0), (140, 120, 2), (20, 140, 1)): P(d, 'parasol', x, y, a)
    P(d, 'table', 100, 150); P(d, 'planterl', 60, 220, 60); over(d, 'lights', 0, 66, 180, 1)
    # car park (260-620)
    G(d, 'gravel', 0, 260, 180, 360)
    r = rng(17)
    for y in (290, 420, 550):
        for x in (0, 152):
            dec(d, 'bay', x, y, 28, 36)
            if r.random() < 0.7: P(d, 'car', x + 2, y + 2, r.randint(0, 4))
    d['data']['pull'] += [[154, 552, 2]]; P(d, 'signpost', 90, 600); H(d, 'cart', 80, 480)
    # pumpkin patch & pond (620-1000)
    field(d, 0, 640, 60, 220); P(d, 'scarecrow', 20, 700); P(d, 'sacks', 30, 820)
    C(d, 'stone', 120, 760, 42); C(d, 'ice', 120, 760, 37); P(d, 'reed', 90, 740); P(d, 'reed', 150, 790); P(d, 'bench', 140, 820)
    H(d, 'ped', 30, 900); H(d, 'thrower', 150, 680)
    # play barn & tractor ride (1000-1240)
    G(d, 'dirt', 0, 1000, 180, 240); scen(d, 'barn', 116, 1010); P(d, 'tractor', 20, 1060, 2); P(d, 'trailer', 20, 1110)
    P(d, 'hay', 70, 1140); P(d, 'hay', 84, 1140); P(d, 'hay', 77, 1130)
    # pick-your-own (1240-1500): rows of fruit bushes in a field
    for y in range(1260, 1480, 44): wild(d, 'bush', 0, y, 60, 14, y, 0.95, 7); wild(d, 'bush', 120, y + 20, 60, 14, y + 1, 0.95, 7)
    P(d, 'well', 82, 1440); H(d, 'ped', 90, 1340)
    return d


def windmill():
    """WINDMILL HILL: up the farm road to the windmill on the hill. Tractors and trailers cross the lanes."""
    d = job('windmill', 'WINDMILL HILL', 'farm', ['farmcafe'], 1600, 100, 2.9, 6, start=[90, 1556])
    G(d, 'grass', 0, 0, 180, 1600)
    path(d, 'dirt', 40, [(90, 1600), (110, 1400), (70, 1200), (110, 1000), (70, 800), (100, 600), (90, 400), (90, 0)])
    for y in (1180, 660, 220):
        G(d, 'dirt', 0, y - 6, 180, 30); H(d, 'cross', 0, y, 1 if y % 2 else -1, 6.0)
    # fields either side, walls and hedgerows
    field(d, 0, 1260, 56, 300); field(d, 128, 900, 52, 240); field(d, 0, 300, 50, 300)
    hedgerow(d, 140, 1260, 40, 200, 11); hedgerow(d, 0, 760, 40, 160, 12)
    P(d, 'stonewall', 60, 1240, 60) if False else None
    for x, y in ((150, 1500), (10, 1000), (150, 700), (14, 160)): P(d, 'oak', x, y)
    H(d, 'sheep', 40, 470, 4); H(d, 'cow', 140, 1400); H(d, 'cow', 30, 820)
    # the windmill on the hill, flour sacks, the miller's cart
    C(d, 'grass', 90, 90, 70); scen(d, 'windmill', 66, 20); P(d, 'sacks', 30, 120); P(d, 'sacks', 140, 110); P(d, 'trailer', 150, 30)
    return d


def maze():
    """MAIZE MAZE (side job): plow out a maize maze. Wide passages, dead ends with prizes, the lookout in the middle."""
    d = job('maze', 'MAIZE MAZE', 'farm', ['windmill'], 1300, 84, 2.9, 9, start=[90, 1262], bonus=True)
    G(d, 'dirt', 0, 0, 180, 1300)
    wild(d, 'bush', 0, 80, 180, 1120, 61, 0.9, 7)
    pts = [[(90, 1300), (90, 1110), (30, 1110), (30, 900), (150, 900), (150, 720), (60, 720), (60, 560), (130, 560), (130, 380), (40, 380), (40, 200), (90, 200), (90, 0)]]
    pts += [[(90, 1110), (150, 1110), (150, 1000)], [(30, 900), (30, 780)], [(60, 640), (150, 640)], [(130, 470), (40, 470)], [(40, 300), (150, 300), (150, 160)]]
    for p in pts: carve(d, 56, p); path(d, 'gravel', 22, p)
    P(d, 'scarecrow', 86, 640); P(d, 'hay', 140, 1000); P(d, 'hay', 24, 780); P(d, 'tub', 144, 160)
    G(d, 'gravel', 0, 1200, 180, 100); G(d, 'gravel', 0, 0, 180, 80); P(d, 'signpost', 120, 1240); P(d, 'shed', 0, 10, 1)
    H(d, 'thrower', 150, 560); H(d, 'ped', 40, 300)
    return d


def mill():
    """THE MILL: the watermill on the frozen river. Down the cart track, over the two road crossings, along the mill
    race to the mill and its pond."""
    d = job('mill', 'THE MILL', 'farm', ['windmill'], 1700, 100, 2.95, 6, start=[90, 1656])
    G(d, 'grass', 0, 0, 180, 1700)
    path(d, 'dirt', 46, [(90, 1700), (90, 1300), (70, 1100), (90, 900), (90, 0)])
    G(d, 'asph', 0, 1240, 180, 40); H(d, 'cross', 0, 1250, 1, 5.5); dec(d, 'dashh', 4, 1259, 172)
    G(d, 'asph', 0, 900, 180, 40); H(d, 'cross', 0, 910, -1, 5.0); dec(d, 'dashh', 4, 919, 172)
    # the river on the right, frozen, with its banks
    G(d, 'ice', 140, 0, 40, 1700); dec(d, 'puddle', 150, 400, 8)
    for y in (300, 700, 1100, 1500): P(d, 'reed', 132, y)
    hedgerow(d, 0, 1300, 40, 340, 21); wood(d, 0, 940, 40, 290, 22)
    field(d, 0, 300, 56, 300); H(d, 'sheep', 30, 420, 4)
    # the mill and its yard
    G(d, 'cobble', 0, 0, 140, 280); scen(d, 'shop', 0, 0, 19); scen(d, 'barn', 60, 0)
    C(d, 'stone', 150, 160, 30); C(d, 'ice', 150, 160, 26)
    for x in (20, 36, 52): P(d, 'sacks', x, 230)
    P(d, 'trailer', 110, 200); P(d, 'well', 80, 120); H(d, 'cart', 60, 180)
    return d


def harvestfair():
    """HARVEST FAIR (boss): the county show, and the Goose has escaped. From the car field, past the animal pens and
    the marquees, round the show ring and the vintage tractors, to the bandstand."""
    d = job('harvestfair', 'HARVEST FAIR', 'farm', ['mill'], 1900, 104, 3.0, 8, start=[90, 1856], boss=True)
    G(d, 'grass', 0, 0, 180, 1900)
    # car field (1640-1900)
    G(d, 'dirt', 70, 1640, 40, 260)
    r = rng(5)
    for y in range(1660, 1880, 44):
        if r.random() < 0.8: P(d, 'car', 4, y, r.randint(0, 4))
        if r.random() < 0.8: P(d, 'car', 156, y + 10, r.randint(0, 4))
    P(d, 'booth', 112, 1640, 1); P(d, 'turnstile', 64, 1630); P(d, 'turnstile', 110, 1630)
    # animal pens (1300-1620)
    wallbox(d, 0, 1320, 62, 1440, [('r', 1360, 1410)], kind='rail'); H(d, 'sheep', 16, 1360, 4)
    wallbox(d, 118, 1320, 180, 1440, [('l', 1360, 1410)], kind='rail'); H(d, 'sheep', 128, 1370, 3, 'horse')
    wallbox(d, 0, 1480, 62, 1600, [('r', 1520, 1570)], kind='rail'); H(d, 'cow', 30, 1540)
    for x, y in ((150, 1460), (162, 1460)): P(d, 'hay', x, y)
    # marquee lane (900-1300)
    G(d, 'dirt', 60, 900, 60, 400)
    for x, y, a in ((0, 920, 0), (120, 980, 1), (0, 1080, 2), (120, 1160, 0), (0, 1220, 1)): scen(d, 'marquee', x, y, a)
    for y in (960, 1120, 1260): over(d, 'banner' if y == 960 else 'lights', 0, y, 180, 3 if y == 960 else 2)
    H(d, 'pedx', 60, 1040); H(d, 'ped', 90, 1200)
    # the show ring (460-900): sand ring, rails, the grandstand
    G(d, 'sand', 20, 480, 140, 400); C(d, 'sand', 90, 680, 70)
    wallbox(d, 14, 470, 166, 890, [('t', 64, 116), ('b', 64, 116)], kind='rail')
    scen(d, 'stand', 0, 420, 80); scen(d, 'shop', 120, 410, 20)
    for x, y in ((50, 560), (110, 640), (60, 760)): P(d, 'hurdle', x, y)
    # vintage tractors & bandstand (0-420)
    G(d, 'gravel', 0, 0, 180, 400)
    for x, y, a in ((10, 200, 0), (150, 260, 2), (12, 320, 1)): P(d, 'tractor', x, y, a)
    P(d, 'stage', 50, 40, 2); P(d, 'speaker', 52, 78); P(d, 'speaker', 118, 78)
    for x, y in ((40, 150), (140, 140)): P(d, 'stall', x - 20 if x > 90 else x, y, 1)
    over(d, 'banner', 0, 120, 180, 3)
    H(d, 'thrower', 150, 340); H(d, 'pedx', 30, 280)
    H(d, 'chaser', 150, 1500, 'goose', 5)
    return d


ALL = [milkshed, treefarm, sheepfields, stables, farmcafe, windmill, maze, mill, harvestfair]
