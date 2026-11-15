"""Farmland part 2: 9 new jobs (7 main, 1 side, 1 boss), played mostly with the tractor.
New mechanics: sheep flocks that scatter from the plow (Sheep Fields), farm traffic that crosses a lane after a
warning (Windmill Hill). Boss: the Harvest Fair, with the Goose hunting you.  Run: python3 farm.py -> farm.json"""
import random
from common import *

J = []

# ---------------------------------------------------------------- MILKING SHED
# Start at the farm gate, plow the cow yard (cows wander in it), round the dairy, through the silo yard to a field.
d = job('milkshed', 'MILKING SHED', 'farm', ['village'], 1300, 86, 2.65, 6, start=[90, 1262])
G(d, 'grass', 0, 0, 180, 1300)
G(d, 'dirt', 66, 0, 48, 1300)                                   # the farm track, full length
for k in range(6): G(d, 'wht', 68 + k * 8, 1188, 4, 14)          # cattle grid
P(d, 'stonewall', 0, 1170, 60); P(d, 'stonewall', 120, 1170, 60); P(d, 'mailbox', 52, 1230); pines(d, [(4, 1236, 24), (154, 1240, 22)])
# cow yard (y 900-1160): walled, gaps top and bottom
wallbox(d, 8, 920, 172, 1160, [('b', 62, 118), ('t', 62, 118)])
G(d, 'dirt', 16, 928, 148, 224)
P(d, 'trough', 20, 960); P(d, 'trough', 136, 1100); P(d, 'hay', 24, 1120); P(d, 'hay', 150, 950); P(d, 'hay', 148, 1010)
for x, y in [(40, 1000), (120, 980), (60, 1090), (130, 1060)]: H(d, 'cow', x, y)
# the dairy (y 600-900)
P(d, 'big', 4, 620, 17); G(d, 'conc', 4, 678, 110, 40)
for k in range(6): P(d, 'churn', 18 + k * 12, 690)
P(d, 'tractor', 160, 690, 0); P(d, 'trailer', 158, 770); P(d, 'barrel', 10, 760); P(d, 'barrel', 20, 760)
H(d, 'dog', 90, 800)
# silo yard (y 300-600)
G(d, 'conc', 0, 330, 66, 120)
for x in (6, 34): P(d, 'silo', x, 360)
P(d, 'sacks', 10, 420); P(d, 'sacks', 30, 430); P(d, 'barn', 116, 330); P(d, 'tires', 40, 530); P(d, 'tires', 130, 520); P(d, 'well', 150, 470)
H(d, 'thrower', 24, 560)
# the top field (y 0-300)
field(d, 0, 20, 64, 260); field(d, 116, 20, 64, 260)
P(d, 'scarecrow', 24, 120); P(d, 'scarecrow', 146, 180); P(d, 'hay', 30, 250); P(d, 'hay', 140, 60)
for x, y in [(20, 200), (150, 110)]: H(d, 'cow', x, y)
pines(d, [(0, 0, 22), (158, 0, 22)])
J.append(d)

# ---------------------------------------------------------------- CHRISTMAS TREE FARM
# Rows of young trees with an opening at alternate ends: a long serpentine to plow. Families with trees, a shop.
d = job('treefarm', 'CHRISTMAS TREE FARM', 'farm', ['milkshed'], 1400, 92, 2.7, 6, start=[90, 40])
G(d, 'grass', 0, 0, 180, 1400)
G(d, 'dirt', 0, 0, 180, 110)                                     # car park
P(d, 'shop', 4, 0, 16); P(d, 'kiosk', 150, 8, 2)
d['data']['pull'] += [[124, 40, 1]]
# plantation (y 130-1180): 9 tree rows, a 56-wide gap at alternate ends, lanes 52 tall between rows
y = 140
for r in range(9):
    gap_left = r % 2 == 0
    xs = range(64, 176, 13) if gap_left else range(2, 116, 13)
    for x in xs: P(d, 'pine', x, y, 16 + ((x + r) % 3) * 2)
    if r % 3 == 1: H(d, 'pedx', 40 if gap_left else 120, y + 40, 0 if gap_left else 1)
    y += 112
# netting shed and the trailer at the bottom
G(d, 'dirt', 0, 1200, 180, 200)
P(d, 'shed', 10, 1240, 0); P(d, 'trailer', 150, 1230); P(d, 'tractor', 120, 1300, 1); P(d, 'stall', 50, 1330, 2)
H(d, 'thrower', 100, 1260); H(d, 'dog', 60, 1380)
J.append(d)

# ---------------------------------------------------------------- SHEEP FIELDS  (new: sheep flocks)
# Dry-stone paddocks joined by wide gateways. Each paddock has a flock that bolts away from the plow.
d = job('sheepfields', 'SHEEP FIELDS', 'farm', ['treefarm'], 1400, 88, 2.75, 6, start=[90, 1360])
G(d, 'grass', 0, 0, 180, 1400)
# a frozen stream winds across the middle with a bridge
for k in range(0, 180, 4): G(d, 'ice', k, 676 + int(10 * math.sin(k / 18)), 4, 18)
G(d, 'conc', 66, 668, 48, 34)
# paddocks: four of them, gateways 56 wide
wallbox(d, 6, 1060, 174, 1320, [('t', 30, 86), ('b', 62, 118), ('r', 1160, 1216)])
wallbox(d, 6, 760, 174, 1040, [('t', 96, 152), ('b', 30, 86), ('l', 860, 916)])
wallbox(d, 6, 360, 174, 640, [('t', 30, 86), ('b', 96, 152)])
wallbox(d, 6, 60, 174, 340, [('b', 30, 86), ('t', 62, 118)])
H(d, 'sheep', 110, 1180, 6); H(d, 'sheep', 60, 880, 6); H(d, 'sheep', 120, 480, 5); H(d, 'sheep', 70, 180, 6)
P(d, 'cabin', 120, 380); P(d, 'trough', 30, 600); P(d, 'hay', 140, 1280); P(d, 'hay', 20, 820); P(d, 'hay', 150, 980); P(d, 'trough', 140, 120)
P(d, 'oak', 150, 300); P(d, 'oak', 14, 100); P(d, 'oak', 150, 900)
H(d, 'dog', 90, 730)
J.append(d)

# ---------------------------------------------------------------- STABLES
# Horses in railed paddocks, an arena with a jump course, the stable block and horseboxes.
d = job('stables', 'STABLES', 'farm', ['sheepfields'], 1500, 92, 2.8, 6, start=[90, 1460])
G(d, 'grass', 0, 0, 180, 1500)
G(d, 'dirt', 66, 1300, 48, 200)
# paddocks at the bottom with horses
wallbox(d, 4, 1060, 66, 1290, [('r', 1140, 1200), ('t', 14, 56)], kind='rail')
wallbox(d, 114, 1060, 176, 1290, [('l', 1140, 1200), ('t', 124, 166)], kind='rail')
H(d, 'sheep', 20, 1140, 3, 'horse'); H(d, 'sheep', 130, 1180, 3, 'horse')
# arena (dirt) with jumps in a figure of eight
G(d, 'dirt', 10, 620, 160, 380)
wallbox(d, 8, 618, 172, 1002, [('b', 66, 114), ('t', 66, 114), ('l', 760, 820), ('r', 760, 820)], kind='rail')
for x, y in [(40, 680), (124, 680), (82, 760), (40, 860), (124, 860), (82, 940)]: P(d, 'hurdle', x, y)
for x, y in [(30, 780), (140, 780)]: P(d, 'pole', x, y)
# stable yard
G(d, 'conc', 0, 380, 180, 200)
P(d, 'big', 68, 300, 18); P(d, 'trailer', 128, 420); P(d, 'trailer', 154, 420); P(d, 'hay', 30, 520); P(d, 'hay', 44, 520); P(d, 'barrel', 140, 540)
P(d, 'tractor', 120, 480, 2); H(d, 'ped', 70, 450); H(d, 'dog', 100, 560)
# a paddock at the top with more horses
wallbox(d, 4, 40, 176, 280, [('b', 8, 62)], kind='rail')
H(d, 'sheep', 60, 120, 4, 'horse'); P(d, 'trough', 120, 80); P(d, 'oak', 20, 60)
J.append(d)

# ---------------------------------------------------------------- FARM SHOP & TEA ROOM
d = job('farmcafe', 'FARM SHOP', 'farm', ['stables'], 1500, 94, 2.85, 6, start=[90, 40])
G(d, 'grass', 0, 0, 180, 1500)
G(d, 'asph', 0, 80, 180, 360)                                     # car park
for x in range(6, 176, 28): G(d, 'wht', x, 90, 2, 32); G(d, 'wht', x, 400, 2, 32)
P(d, 'car', 9, 92, 1); P(d, 'car', 65, 92, 3); P(d, 'car', 121, 92, 0); P(d, 'car', 37, 402, 2); P(d, 'car', 149, 402, 4)
d['data']['pull'] += [[93, 92, 2], [9, 402, 1]]
H(d, 'cart', 80, 250)
G(d, 'conc', 0, 440, 180, 140)
P(d, 'shop', 4, 470, 16); P(d, 'shop', 120, 470, 21)
for x in (6, 144): P(d, 'stall', x, 600, (x // 32) % 3)
d['data']['neighbours'] = [dict(rects=[[60, 580, 60, 12], [60, 580, 12, 200]], path=[[66, 780], [66, 586], [92, 586]])]
# tea garden, duck pond, play area (y 600-1450)
C(d, 'ice', 120, 760, 34); P(d, 'reed', 84, 740); P(d, 'reed', 150, 790); P(d, 'reed', 110, 720)
for x, y in [(10, 640), (40, 690), (10, 740)]: P(d, 'table', x, y, (x + y) % 4)
P(d, 'swing', 20, 900); P(d, 'slide', 140, 900); P(d, 'sandpit', 70, 960)
field(d, 0, 1040, 180, 220)
P(d, 'scarecrow', 30, 1100); P(d, 'scarecrow', 140, 1180); P(d, 'hay', 90, 1160)
H(d, 'thrower', 150, 1000); H(d, 'pedx', 30, 860); H(d, 'pedx', 120, 1300, 1)
P(d, 'barn', 58, 1330); pines(d, [(4, 1400, 24), (156, 1410, 22)])
J.append(d)

# ---------------------------------------------------------------- WINDMILL HILL  (new: farm traffic)
# Two farm roads cross the hill: tractors with trailers come across after a warning. The windmill at the top.
d = job('windmill', 'WINDMILL HILL', 'farm', ['farmcafe'], 1600, 100, 2.9, 6, start=[90, 1560])
G(d, 'grass', 0, 0, 180, 1600)
field(d, 0, 1240, 180, 260); field(d, 0, 760, 180, 300); field(d, 0, 300, 180, 260)
G(d, 'dirt', 0, 1160, 180, 40); G(d, 'dirt', 0, 640, 180, 40); G(d, 'dirt', 0, 200, 180, 40)     # farm roads
H(d, 'cross', 0, 1172, 1, 6.5); H(d, 'cross', 0, 652, -1, 6.0); H(d, 'cross', 0, 212, 1, 5.5)
P(d, 'hedge', 0, 1120, 60); P(d, 'hedge', 120, 1120, 60); P(d, 'hedge', 0, 600, 50); P(d, 'hedge', 130, 600, 50); P(d, 'hedge', 0, 1220, 40); P(d, 'hedge', 140, 1220, 40)
P(d, 'trailer', 150, 900); P(d, 'tractor', 10, 880, 0); P(d, 'hay', 80, 960); P(d, 'hay', 94, 960); P(d, 'scarecrow', 120, 1340); P(d, 'scarecrow', 30, 420)
P(d, 'windmill', 68, 20); P(d, 'sacks', 30, 110); P(d, 'sacks', 140, 120); P(d, 'barrel', 120, 80)
H(d, 'sheep', 40, 470, 4); H(d, 'cow', 140, 1400); H(d, 'cow', 30, 820)
pines(d, [(0, 0, 24), (156, 4, 22), (4, 1560, 22), (154, 1556, 24)])
J.append(d)

# ---------------------------------------------------------------- MAIZE MAZE  (side job)
# A hedge maze with corridors 50 wide (fits everything). Presents hide in the dead ends.
d = job('maze', 'MAIZE MAZE', 'farm', ['windmill'], 1300, 84, 2.9, 9, start=[90, 1262], bonus=True)
G(d, 'grass', 0, 0, 180, 1300)
COLS, ROWS, CW = 3, 20, 60
rnd = random.Random(7)
walls = {(c, r, s) for c in range(COLS) for r in range(ROWS) for s in 'ES'}
seen = set(); stack = [(1, ROWS - 1)]; seen.add((1, ROWS - 1))
while stack:
    c, r = stack[-1]; nb = [(c + dc, r + dr) for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= c + dc < COLS and 0 <= r + dr < ROWS and (c + dc, r + dr) not in seen]
    if not nb: stack.pop(); continue
    n = rnd.choice(nb); seen.add(n); stack.append(n)
    if n[0] != c: walls.discard((min(c, n[0]), r, 'E'))
    else: walls.discard((c, min(r, n[1]), 'S'))
Y0 = 50
P(d, 'hedge', 0, Y0 - 10, 60); P(d, 'hedge', 120, Y0 - 10, 60)                 # top edge with the exit in the middle
for c in range(COLS):
    for r in range(ROWS):
        x, y = c * CW, Y0 + r * CW
        if (c, r, 'E') in walls and c < COLS - 1: P(d, 'hedgev', x + CW - 5, y, CW)
        if (c, r, 'S') in walls and r < ROWS - 1: P(d, 'hedge', x, y + CW - 5, CW)
deadends = []
for c in range(COLS):
    for r in range(ROWS):
        open_sides = (c > 0 and (c - 1, r, 'E') not in walls) + (c < COLS - 1 and (c, r, 'E') not in walls) + (r > 0 and (c, r - 1, 'S') not in walls) + (r < ROWS - 1 and (c, r, 'S') not in walls)
        if open_sides == 1 and (c, r) != (1, ROWS - 1): deadends.append((c, r))
for c, r in deadends[:5]: P(d, 'scarecrow', c * CW + 24, Y0 + r * CW + 18)
H(d, 'thrower', 150, 600); H(d, 'thrower', 20, 300)
J.append(d)

# ---------------------------------------------------------------- THE MILL
# Silos, sacks and grain trucks crossing the yard; a forklift trolley rolls round.
d = job('mill', 'THE MILL', 'farm', ['windmill'], 1700, 100, 2.95, 6, start=[90, 1660])
G(d, 'grass', 0, 0, 180, 1700)
G(d, 'conc', 0, 1000, 180, 520); G(d, 'dirt', 66, 1520, 48, 180); G(d, 'dirt', 66, 0, 48, 1000)
P(d, 'big', 35, 1020, 19)
for x in (4, 28, 128, 154): P(d, 'silo', x, 1132)
G(d, 'asph', 0, 1240, 180, 40); H(d, 'cross', 0, 1250, 1, 5.5)
for x, y in [(10, 1320), (30, 1330), (140, 1300), (150, 1420)]: P(d, 'sacks', x, y)
P(d, 'trailer', 6, 1400); P(d, 'tractor', 150, 1350, 1); H(d, 'cart', 90, 1380)
G(d, 'asph', 0, 900, 180, 40); H(d, 'cross', 0, 910, -1, 5.0)
field(d, 0, 300, 64, 560); field(d, 116, 300, 64, 560)
P(d, 'hay', 20, 400); P(d, 'hay', 150, 500); P(d, 'scarecrow', 30, 640); P(d, 'scarecrow', 140, 760)
H(d, 'sheep', 130, 380, 5)
P(d, 'barn', 10, 160); P(d, 'well', 140, 200)
pines(d, [(150, 20, 24), (4, 40, 22), (60, 20, 20)])
J.append(d)

# ---------------------------------------------------------------- HARVEST FAIR  (boss)
# The county show: marquees, sheep pens and a show ring, a tractor parade crossing the showground, food stalls
# and hay-bale seating. And the Goose, who has decided you are the enemy.
d = job('harvestfair', 'HARVEST FAIR', 'farm', ['mill'], 1900, 104, 3.0, 8, start=[90, 1860], boss=True)
G(d, 'grass', 0, 0, 180, 1900)
G(d, 'dirt', 0, 1700, 180, 120)                                    # entrance track
P(d, 'stonewall', 0, 1690, 60); P(d, 'stonewall', 120, 1690, 60); P(d, 'stall', 4, 1730, 1); P(d, 'stall', 146, 1730, 0)
# marquees (y 1380-1680)
P(d, 'marquee', 4, 1560, 0); P(d, 'marquee', 116, 1480, 1); P(d, 'marquee', 4, 1400, 2)
H(d, 'pedx', 70, 1640); H(d, 'pedx', 110, 1430, 1)
# sheep pens (y 1100-1360): rail pens with flocks
wallbox(d, 4, 1120, 66, 1340, [('r', 1200, 1260)], kind='rail'); H(d, 'sheep', 16, 1180, 5)
wallbox(d, 114, 1120, 176, 1340, [('l', 1200, 1260)], kind='rail'); H(d, 'sheep', 128, 1260, 5)
# tractor parade across the showground
G(d, 'dirt', 0, 1030, 180, 40); H(d, 'cross', 0, 1040, 1, 5.0)
# show ring (y 620-1000)
G(d, 'dirt', 20, 640, 140, 340)
wallbox(d, 18, 638, 162, 982, [('t', 66, 114), ('b', 66, 114), ('l', 780, 840), ('r', 780, 840)], kind='rail')
for x, y in [(50, 700), (110, 760), (50, 860), (110, 920)]: P(d, 'hurdle', x, y)
H(d, 'cow', 90, 820)
# food and seating (y 260-600)
for x, y in [(4, 300), (75, 300), (146, 300)]: P(d, 'stall', x, y, (x // 30) % 4)
for x, y in [(10, 420), (24, 420), (140, 440), (154, 440), (10, 520), (150, 540)]: P(d, 'hay', x, y)
P(d, 'bbq', 80, 480); P(d, 'table', 50, 560, 1); P(d, 'table', 104, 520, 3)
G(d, 'dirt', 0, 560, 180, 40); H(d, 'cross', 0, 570, -1, 5.5)
# the prize barn at the top
P(d, 'barn', 58, 40); P(d, 'tractor', 20, 120, 0); P(d, 'tractor', 142, 120, 2); P(d, 'hay', 30, 200); P(d, 'hay', 140, 210)
pines(d, [(0, 0, 24), (158, 2, 22)])
H(d, 'chaser', 150, 1500, 'goose', 5)
J.append(d)

# ---------------------------------------------------------------- map: the Farmland part 2 band (6062-6622)
POS = {'milkshed': [40, 6584], 'treefarm': [140, 6532], 'sheepfields': [44, 6470], 'stables': [140, 6414], 'farmcafe': [52, 6352],
       'windmill': [138, 6296], 'maze': [26, 6224], 'mill': [130, 6222], 'harvestfair': [86, 6130]}
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/farm.json', mappos=POS, landmark=LM, relink={'shops': ['harvestfair']},
       edgevia={'harvestfair>shops': [[90, 6090], [92, 6040]]}, bossStars={'harvestfair': 25})
