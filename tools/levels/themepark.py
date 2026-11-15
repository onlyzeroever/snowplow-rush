"""Theme Park: 15 jobs (12 main, 2 side, 1 boss), Super Plow era.
New mechanics: bumper cars (Bumper Cars), the roller coaster rushing across (Roller Coaster), ghosts (Haunted
House). Boss: Opening Day, with Benny Bear the mascot after a hug.  python3 themepark.py -> themepark.json"""
from common import *

J = []
SH = dict(TICKETS=31, SOUVENIRS=32, ARCADE=33, HAUNTED=34, BURGERS=35, ICECREAM=36, GHOSTTRAIN=37, FLUME=38)
def park_paths(d, h, main=(64, 52)):
    G(d, 'grass', 0, 0, 180, h); G(d, 'conc', main[0], 0, main[1], h)
def lamps(d, xs, y0, y1, step):
    for y in range(y0, y1, step):
        for x in xs: P(d, 'lamp', x, y)

# 1 TICKET GATES
d = job('gates', 'TICKET GATES', 'themepark', ['parade'], 2400, 63, 7.8, 7, start=[90, 2360])
G(d, 'asph', 0, 1700, 180, 700)                                      # coach park
for y in range(1760, 2300, 110):
    for x in range(4, 176, 30): G(d, 'wht', x, y, 2, 40)
    P(d, 'bus', 6 if (y // 110) % 2 else 150, y + 2)
G(d, 'conc', 0, 900, 180, 800)
for k, x in enumerate((6, 81, 156)): P(d, 'booth', x, 1500, k % 3)        # ticket booths with wide lanes between
for x in (8, 22, 36, 136, 150, 164): P(d, 'turnstile', x, 1420)
P(d, 'big', 35, 980, SH['TICKETS'])
for x, y in [(10, 1200), (150, 1260), (60, 1300), (110, 1150)]: P(d, 'balloons', x, y)
H(d, 'pedx', 30, 1350); H(d, 'pedx', 120, 1250, 1); H(d, 'ped', 160, 1100)
park_paths(d, 900)
P(d, 'carousel', 6, 200); P(d, 'carousel', 134, 500); P(d, 'popcorn', 140, 120); P(d, 'popcorn', 20, 600)
lamps(d, (56, 120), 60, 880, 160)
H(d, 'thrower', 150, 300)
J.append(d)

# 2 MAIN STREET
d = job('mainst', 'MAIN STREET', 'themepark', ['gates'], 2800, 58, 8.0, 7, start=[90, 40])
G(d, 'red', 0, 0, 180, 2800); G(d, 'conc', 44, 0, 92, 2800)
y = 60
k = 0
while y < 2700:
    P(d, 'shopv', 0, y, [32, 36, 35, 33][k % 4]); P(d, 'shopv', 136, y + 40, [36, 32, 33, 35][k % 4]); y += 140; k += 1
for y in range(200, 2700, 300): P(d, 'popcorn', 60 if (y // 300) % 2 else 104, y); P(d, 'balloons', 104 if (y // 300) % 2 else 64, y + 140)
for y in range(140, 2800, 240): d['data']['decor'].append(['bunting', 44, y, 92])
H(d, 'pedx', 60, 600); H(d, 'pedx', 110, 1300, 1); H(d, 'pedx', 60, 2000); H(d, 'ped', 80, 900); H(d, 'ped', 100, 2300, 1); H(d, 'cart', 90, 1700)
J.append(d)

# 3 CAROUSEL COURT
d = job('carousel', 'CAROUSEL COURT', 'themepark', ['mainst'], 2600, 68, 8.2, 7, start=[90, 2560])
G(d, 'wood', 0, 0, 180, 2600)
for k, y in enumerate(range(200, 2400, 330)):
    x = 8 if k % 2 == 0 else 132
    C(d, 'red', x + 20, y + 26, 30); P(d, 'carousel', x, y)
    P(d, 'cup', 120 if k % 2 == 0 else 20, y + 100, k % 4); P(d, 'bench', 90, y + 60)
for y in range(150, 2500, 400): P(d, 'popcorn', 70, y); P(d, 'balloons', 100, y + 200)
H(d, 'pedx', 40, 500); H(d, 'pedx', 120, 1200, 1); H(d, 'pedx', 60, 1900); H(d, 'thrower', 150, 2200)
J.append(d)

# 4 GAMES ALLEY
d = job('games', 'GAMES ALLEY', 'themepark', ['carousel'], 2800, 71, 8.4, 8, start=[90, 40])
G(d, 'conc', 0, 0, 180, 2800)
for y in range(120, 2700, 180):
    P(d, 'stall', 2, y, (y // 180) % 4); P(d, 'stall', 148, y + 90, (y // 180 + 1) % 4)
for k, y in enumerate(range(400, 2600, 700)):                         # hook-a-duck ponds
    C(d, 'ice', 90, y, 22); P(d, 'reed', 80, y - 6); P(d, 'reed', 98, y + 4)
for y in range(250, 2700, 350): P(d, 'balloons', 70 if (y // 350) % 2 else 100, y)
H(d, 'thrower', 40, 800); H(d, 'thrower', 140, 1600); H(d, 'pedx', 60, 1200); H(d, 'pedx', 110, 2200, 1)
J.append(d)

# 5 BUMPER CARS  (new)
d = job('bumpers', 'BUMPER CARS', 'themepark', ['games'], 2600, 64, 8.6, 7, start=[90, 2560])
G(d, 'conc', 0, 0, 180, 2600)
for k, y0 in enumerate((1700, 900, 150)):                             # three arenas, each with cars
    G(d, 'wood', 10, y0, 160, 600)
    wallbox(d, 8, y0 - 2, 172, y0 + 602, [('b', 62, 118), ('t', 62, 118)], kind='rail')
    H(d, 'bumper', 30, y0 + 120, 4 + k); H(d, 'bumper', 110, y0 + 400, 3 + k)
for y in (1640, 840): P(d, 'booth', 6, y, 1); P(d, 'popcorn', 150, y)
H(d, 'pedx', 40, 2450); H(d, 'pedx', 120, 1620, 1)
J.append(d)

# 6 FOOD COURT & TEACUPS
d = job('food', 'FOOD COURT', 'themepark', ['bumpers'], 2700, 68, 8.8, 7, start=[90, 40])
G(d, 'conc', 0, 0, 180, 2700)
P(d, 'shop', 4, 0, SH['BURGERS']); P(d, 'shop', 120, 0, SH['ICECREAM'])
for r, y in enumerate(range(160, 1300, 70)):
    P(d, 'table', 8 if r % 2 else 104, y, r % 4)
    if r % 3 == 0: P(d, 'table', 54 if r % 2 else 146, y + 30, (r + 2) % 4)
G(d, 'wood', 0, 1400, 180, 1200)
for k, (x, y) in enumerate([(20, 1500), (130, 1620), (40, 1800), (120, 1980), (20, 2160), (130, 2360)]): P(d, 'cup', x, y, k % 4)
H(d, 'bumper', 70, 1700, 3)
H(d, 'pedx', 30, 600); H(d, 'pedx', 120, 1000, 1); H(d, 'cart', 80, 900); H(d, 'thrower', 150, 2500)
J.append(d)

# 7 FERRIS WHEEL
d = job('ferris', 'FERRIS WHEEL', 'themepark', ['food'], 2800, 71, 9.0, 7, start=[90, 2760])
G(d, 'grass', 0, 0, 180, 2800); G(d, 'conc', 0, 1500, 180, 900)
P(d, 'ferris', 54, 1520)
for k in range(4):                                                    # the queue: rails zigzag, 52 apart
    y = 1720 + k * 60
    if k % 2 == 0: P(d, 'rail', 0, y, 120)
    else: P(d, 'rail', 60, y, 120)
G(d, 'conc', 64, 0, 52, 1500)
for y in range(200, 1400, 300): P(d, 'carousel' if (y // 300) % 2 else 'helter', 8 if (y // 300) % 2 else 140, y)
lamps(d, (56, 120), 100, 1460, 200)
H(d, 'pedx', 40, 2000); H(d, 'pedx', 120, 1880, 1); H(d, 'thrower', 20, 900); H(d, 'ped', 100, 600)
J.append(d)

# 8 HELTER SKELTER
d = job('helter', 'HELTER SKELTER', 'themepark', ['ferris'], 2700, 67, 9.2, 7, start=[90, 40])
G(d, 'grass', 0, 0, 180, 2700)
for k, y in enumerate(range(120, 2600, 260)):
    P(d, 'helter', 6 if k % 2 == 0 else 148, y); C(d, 'red', 19 if k % 2 == 0 else 161, y + 52, 18)
    P(d, 'balloons', 120 if k % 2 == 0 else 40, y + 120)
for y in range(300, 2600, 500): P(d, 'popcorn', 82, y)
H(d, 'pedx', 40, 700); H(d, 'pedx', 120, 1400, 1); H(d, 'pedx', 50, 2100); H(d, 'thrower', 90, 1800)
J.append(d)

# 9 HAUNTED HOUSE  (side)
d = job('haunted', 'HAUNTED HOUSE', 'themepark', ['helter'], 2200, 60, 9.2, 9, start=[90, 2160], bonus=True)
G(d, 'asph', 0, 0, 180, 2200)
P(d, 'big', 35, 60, SH['HAUNTED'])
for y in range(300, 2000, 220): P(d, 'oak', 4 if (y // 220) % 2 else 154, y); P(d, 'statue', 40 if (y // 220) % 2 else 130, y + 100)
for y in range(400, 2100, 300): H(d, 'ghost', 40, y, 0); H(d, 'ghost', 130, y + 150, 1)
P(d, 'booth', 150, 2000, 0)
J.append(d)

# 10 ROLLER COASTER  (new: the coaster rushes across)
d = job('coaster', 'ROLLER COASTER', 'themepark', ['helter'], 3000, 73, 9.4, 7, start=[90, 2960])
G(d, 'grass', 0, 0, 180, 3000)
for k, yc in enumerate((500, 1100, 1700, 2400)):
    G(d, 'conc', 0, yc - 4, 180, 30); P(d, 'coaster', 0, yc - 16, 50); P(d, 'coaster', 130, yc - 16, 50)
    H(d, 'cross', 0, yc, 1 if k % 2 == 0 else -1, 4.5, 'coaster')
for k, y in enumerate(range(200, 2900, 300)):
    P(d, 'coasterv', 6 if k % 2 == 0 else 167, y, 120)
P(d, 'big', 35, 40, SH['TICKETS']); P(d, 'droptower', 140, 120)
for y in range(300, 2900, 450): P(d, 'balloons', 60 if (y // 450) % 2 else 110, y)
H(d, 'pedx', 40, 800); H(d, 'pedx', 120, 1400, 1); H(d, 'thrower', 100, 2000)
J.append(d)

# 11 LOG FLUME
d = job('flume', 'LOG FLUME', 'themepark', ['coaster'], 2800, 69, 9.6, 7, start=[90, 100])
G(d, 'grass', 0, 0, 180, 2800)
P(d, 'big', 35, 0, SH['FLUME'])
for k, y in enumerate(range(200, 2700, 250)):                          # the frozen channel snakes left-right
    if k % 2 == 0: G(d, 'ice', 0, y, 120, 24); G(d, 'conc', 120, y - 4, 60, 32)
    else: G(d, 'ice', 60, y, 120, 24); G(d, 'conc', 0, y - 4, 60, 32)
for y in range(320, 2700, 250): P(d, 'pine', 10 if (y // 250) % 2 else 154, y, 22)
H(d, 'pedx', 40, 900); H(d, 'pedx', 120, 1700, 1); H(d, 'thrower', 150, 2300)
J.append(d)

# 12 DROP TOWER & ARCADE
d = job('drop', 'DROP TOWER', 'themepark', ['flume'], 3000, 71, 9.8, 7, start=[90, 2960])
G(d, 'conc', 0, 0, 180, 3000)
P(d, 'droptower', 80, 1300); C(d, 'yel', 91, 1380, 40); C(d, 'conc', 91, 1380, 36)
P(d, 'big', 35, 60, SH['ARCADE']); P(d, 'big', 35, 2500, SH['SOUVENIRS'])
for y in range(300, 1200, 200): P(d, 'cup', 10 if (y // 200) % 2 else 150, y, (y // 200) % 4)
for y in range(1600, 2400, 200): P(d, 'carousel', 4 if (y // 200) % 2 else 136, y)
H(d, 'bumper', 70, 600, 3); H(d, 'pedx', 40, 1700); H(d, 'pedx', 120, 2200, 1); H(d, 'thrower', 150, 900)
J.append(d)

# 13 MINI GOLF  (side)
d = job('minigolf', 'MINI GOLF', 'themepark', ['drop'], 2400, 64, 9.8, 9, start=[90, 40], bonus=True)
G(d, 'grass', 0, 0, 180, 2400)
for k, y in enumerate(range(100, 2300, 240)):
    x0 = 8 if k % 2 == 0 else 96
    G(d, 'red', x0, y, 76, 180); P(d, 'hole', x0 + 50, y + 30, k % 3)
    if k % 3 == 0: P(d, 'windmill', x0 + 16, y + 60)
    else: P(d, 'cup', x0 + 10, y + 70, k % 4)
for y in range(300, 2300, 400): P(d, 'bench', 84, y)
H(d, 'pedx', 40, 900); H(d, 'pedx', 120, 1700, 1)
J.append(d)

# 14 FIREWORKS LAKE
d = job('lake', 'FIREWORKS LAKE', 'themepark', ['drop'], 3000, 71, 10.0, 7, start=[90, 2960])
G(d, 'grass', 0, 0, 180, 3000)
C(d, 'ice', 90, 1500, 80); C(d, 'ice', 90, 1200, 60); C(d, 'ice', 90, 1800, 60)
G(d, 'wood', 0, 1480, 180, 40)                                          # a boardwalk across the lake
for y in range(300, 2800, 300): P(d, 'lamp', 4, y); P(d, 'lamp', 170, y + 150)
P(d, 'stage', 50, 80); P(d, 'speaker', 36, 90); P(d, 'speaker', 134, 90)
for y in (600, 2400): P(d, 'stall', 10, y, 0); P(d, 'stall', 140, y, 2)
H(d, 'pedx', 40, 1490); H(d, 'pedx', 140, 2600, 1); H(d, 'thrower', 20, 800); H(d, 'cannon', 2, 1000, 0.3, 7.0, 64)
J.append(d)

# 15 OPENING DAY  (boss)
d = job('openingday', 'OPENING DAY', 'themepark', ['lake'], 3400, 77, 10.5, 9, start=[90, 3360], boss=True)
G(d, 'conc', 0, 0, 180, 3400)
for y in range(140, 3400, 220): d['data']['decor'].append(['bunting', 0, y, 180])
P(d, 'ferris', 54, 60); P(d, 'carousel', 6, 600); P(d, 'carousel', 134, 900); P(d, 'helter', 150, 300)
for k, yc in enumerate((1300, 2300)):
    G(d, 'wood', 0, yc - 4, 180, 30); H(d, 'cross', 0, yc, 1 if k == 0 else -1, 5.0, 'coaster')
G(d, 'wood', 10, 1500, 160, 500); wallbox(d, 8, 1498, 172, 2002, [('b', 62, 118), ('t', 62, 118)], kind='rail'); H(d, 'bumper', 30, 1600, 5)
for y in range(2500, 3300, 200): P(d, 'stall', 4 if (y // 200) % 2 else 146, y, (y // 200) % 4)
for y in range(700, 3300, 500): P(d, 'balloons', 80, y)
H(d, 'pedx', 40, 1100); H(d, 'pedx', 120, 2700, 1); H(d, 'thrower', 90, 2200)
H(d, 'chaser', 160, 3000, 'mascot', 5)
J.append(d)

ids = [j['id'] for j in J]
POS = {}
for k, i in enumerate(ids):
    y = 4846 - k * 61
    x = 40 if k % 2 == 0 else 140
    if i in ('haunted', 'minigolf'): x = 20 if k % 2 == 0 else 160
    if i == 'openingday': x = 90
    POS[i] = [x, y]
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/themepark.json', mappos=POS, landmark=LM, bossStars={'openingday': 26},
       story=['THE THEME PARK IS SNOWED IN!', 'OPENING DAY IS COMING', 'AND THE RIDES ARE BURIED.', 'CLEAR THE WAY FOR THE FUN!'])
