"""Ski Resort: 15 jobs (12 main, 2 side, 1 boss). New mechanics: skiers racing down after a warning arrow (Blue
Run onwards); snow guns re-cover the pistes (Snow Guns). Boss: The Grand Slalom, with a runaway snowball.  -> ski.json"""
from common import *

J = []
SH = dict(SCHOOL=45, LIFT=46, HIRE=47, APRES=48, GONDOLA=49)
def slalom(d, y0, y1, step=150, x0=50, gapw=56):
    for k, y in enumerate(range(y0, y1, step)):
        x = x0 if k % 2 == 0 else 180 - x0 - gapw
        P(d, 'gatepole', x, y, 0); P(d, 'gatepole', x + gapw, y, 1)
def forest_edges(d, h, step=90):
    for y in range(40, h - 40, step): P(d, 'pine', 0, y, 26); P(d, 'pine', 162, y + 45, 24)

# 1 SKI SCHOOL
d = job('skischool', 'SKI SCHOOL', 'ski', ['festival'], 2600, 65, 13.8, 7, start=[90, 2560])
P(d, 'big', 35, 2300, SH['SCHOOL']); forest_edges(d, 2200)
for y in range(300, 2200, 220): P(d, 'cone', 60, y); P(d, 'cone', 114, y + 110)
slalom(d, 400, 2100, 280, 40, 60)
for y in range(500, 2200, 450): H(d, 'pedx', 40, y, (y // 450) % 2)
H(d, 'thrower', 140, 1300)
J.append(d)

# 2 CHALET VILLAGE
d = job('chalets', 'CHALET VILLAGE', 'ski', ['skischool'], 2800, 70, 14.0, 7, start=[90, 40])
G(d, 'conc', 64, 0, 52, 2800)
for k, y in enumerate(range(100, 2700, 200)):
    P(d, 'chalet', 4 if k % 2 == 0 else 132, y, k % 3); P(d, 'tub', 20 if k % 2 else 148, y + 120)
    if k % 3 == 0: P(d, 'crate', 140 if k % 2 == 0 else 26, y + 60)
for y in range(200, 2700, 300): P(d, 'lamp', 56 if (y // 300) % 2 else 118, y)
H(d, 'pedx', 30, 900); H(d, 'pedx', 130, 1700, 1); H(d, 'thrower', 150, 2300); H(d, 'dog', 90, 1200)
J.append(d)

# 3 LIFT STATION
d = job('lift', 'LIFT STATION', 'ski', ['chalets'], 2800, 70, 14.2, 7, start=[90, 2760])
P(d, 'big', 35, 2400, SH['LIFT'])
for k in range(4): P(d, 'rail', 0 if k % 2 == 0 else 60, 2200 - k * 56, 120)        # the lift queue
for y in range(200, 1900, 260): P(d, 'pylon', 150, y)
forest_edges(d, 1900, 120)
for y in range(300, 1900, 400): P(d, 'mogul', 60, y); P(d, 'mogul', 100, y + 200)
H(d, 'pedx', 40, 2280); H(d, 'pedx', 120, 2170, 1); H(d, 'thrower', 40, 800)
J.append(d)

# 4 SNOW GUNS  (snow cannons re-cover the piste)
d = job('snowguns', 'SNOW GUNS', 'ski', ['lift'], 3000, 76, 14.4, 7, start=[90, 40])
forest_edges(d, 3000, 140)
for k, y in enumerate(range(300, 2800, 420)): H(d, 'cannon', 22 if k % 2 == 0 else 140, y, 0.4 if k % 2 == 0 else 2.7, 7.0, 64)
for y in range(500, 2800, 500): P(d, 'mogul', 80, y)
H(d, 'thrower', 90, 1500)
J.append(d)

# 5 BLUE RUN  (new: skiers)
d = job('bluerun', 'BLUE RUN', 'ski', ['snowguns'], 3000, 76, 14.6, 7, start=[90, 2960])
forest_edges(d, 3000, 120)
for x in (50, 110): H(d, 'skier', x, 0, 6.0 if x == 50 else 7.5)
slalom(d, 300, 2800, 300, 30, 62)
for y in range(400, 2800, 600): P(d, 'mogul', 120, y); P(d, 'mogul', 50, y + 300)
J.append(d)

# 6 RED RUN
d = job('redrun', 'RED RUN', 'ski', ['bluerun'], 3000, 75, 14.8, 7, start=[90, 40])
for y in range(200, 2900, 260): P(d, 'pine', 40 if (y // 260) % 2 else 120, y, 24)
forest_edges(d, 3000, 110)
for x in (40, 90, 140): H(d, 'skier', x, 0, 5.0 + x / 60)
H(d, 'thrower', 150, 1600)
J.append(d)

# 7 MOGUL FIELD
d = job('moguls', 'MOGUL FIELD', 'ski', ['redrun'], 3000, 75, 15.0, 7, start=[90, 2960])
for k, y in enumerate(range(200, 2800, 70)):
    for x in ((20, 82, 144) if k % 2 == 0 else (50, 112)): P(d, 'mogul', x, y)
H(d, 'skier', 70, 0, 6.5); H(d, 'skier', 120, 0, 8.0); H(d, 'thrower', 10, 1400)
J.append(d)

# 8 SLALOM
d = job('slalom', 'SLALOM COURSE', 'ski', ['moguls'], 3000, 76, 15.2, 7, start=[90, 40])
slalom(d, 200, 2900, 180, 24, 58)
G(d, 'red', 0, 2900, 180, 4)
for y in range(400, 2800, 500): P(d, 'flag', 4, y, 0); P(d, 'flag', 170, y + 250, 1)
H(d, 'skier', 60, 0, 6.0); H(d, 'skier', 120, 0, 7.0)
J.append(d)

# 9 TERRAIN PARK  (side)
d = job('terrain', 'TERRAIN PARK', 'ski', ['slalom'], 2600, 67, 15.2, 9, start=[90, 2560], bonus=True)
for k, y in enumerate(range(200, 2400, 260)):
    P(d, 'ramp', 10 if k % 2 == 0 else 130, y)
    if k % 2: P(d, 'rail', 70, y + 140, 40)
    else: P(d, 'mogul', 80, y + 140)
for y in range(400, 2400, 600): H(d, 'pedx', 40, y)
H(d, 'skier', 90, 0, 6.0)
J.append(d)

# 10 GONDOLA TOP
d = job('gondola', 'GONDOLA TOP', 'ski', ['slalom'], 3000, 75, 15.4, 7, start=[90, 2960])
P(d, 'big', 35, 60, SH['GONDOLA']); G(d, 'wood', 0, 140, 180, 300)
for x in (10, 60, 110, 160): P(d, 'bench', x, 300)
for y in range(600, 2900, 280): P(d, 'pylon', 160 if (y // 280) % 2 else 6, y)
for y in range(700, 2900, 400): P(d, 'rock', 70, y, 20)
H(d, 'skier', 50, 0, 6.5); H(d, 'skier', 120, 0, 7.5); H(d, 'pedx', 40, 350); H(d, 'cannon', 2, 1800, 0.3, 7.5, 60)
J.append(d)

# 11 APRES-SKI
d = job('apres', 'APRES-SKI', 'ski', ['gondola'], 2800, 69, 15.6, 7, start=[90, 40])
G(d, 'wood', 0, 0, 180, 2800)
P(d, 'big', 35, 80, SH['APRES']); P(d, 'stage', 50, 1300); P(d, 'speaker', 36, 1310); P(d, 'speaker', 134, 1310)
for r, y in enumerate(range(400, 2600, 110)): P(d, 'table', 6 if r % 2 else 148, y, r % 4)
for y in range(500, 2600, 300): H(d, 'pedx', 40, y, (y // 300) % 2)
H(d, 'thrower', 90, 2000); P(d, 'tub', 80, 2300); P(d, 'tub', 80, 800)
J.append(d)

# 12 SNOWSHOE TRAIL  (side)
d = job('snowshoe', 'SNOWSHOE TRAIL', 'ski', ['apres'], 2600, 68, 15.6, 9, start=[90, 2560], bonus=True)
for k, y in enumerate(range(100, 2500, 46)):
    for x in range(0, 180, 18):
        side = (k // 6) % 2
        if (side == 0 and x < 110) or (side == 1 and x > 66):
            if (x // 18 + k) % 3 == 0: P(d, 'pine', x, y, 22)
H(d, 'pedx', 60, 1200); H(d, 'dog', 90, 2000)
J.append(d)

# 13 BLACK RUN
d = job('blackrun', 'BLACK RUN', 'ski', ['apres'], 3200, 80, 15.8, 7, start=[90, 2960 + 200])
for k, y in enumerate(range(300, 3000, 300)): G(d, 'ice', 10 if k % 2 else 100, y, 70, 120)
forest_edges(d, 3200, 100)
for x in (40, 80, 120, 150): H(d, 'skier', x, 0, 4.5 + x / 80)
for y in range(500, 3000, 500): P(d, 'rock', 70, y, 18)
J.append(d)

# 14 GLACIER
d = job('glacier', 'GLACIER', 'ski', ['blackrun'], 3200, 79, 16.0, 7, start=[90, 40])
for k, y in enumerate(range(200, 3100, 230)):
    G(d, 'ice', 0, y, 180, 30)
    P(d, 'rock', 6 if k % 2 == 0 else 150, y + 70, 24); P(d, 'rock', 70 if k % 2 else 90, y + 150, 14)
H(d, 'skier', 60, 0, 7.0); H(d, 'cannon', 2, 1500, 0.3, 7.0, 64); H(d, 'cannon', 158, 2600, 2.8, 7.0, 64)
J.append(d)

# 15 THE GRAND SLALOM  (boss)
d = job('grandslalom', 'THE GRAND SLALOM', 'ski', ['glacier'], 3400, 80, 16.6, 9, start=[90, 3360], boss=True)
slalom(d, 300, 3200, 200, 24, 60)
for y in range(140, 3400, 300): d['data']['decor'].append(['bunting', 0, y, 180])
for x in (50, 130): H(d, 'skier', x, 0, 5.5 + x / 100)
for k, y in enumerate(range(800, 3200, 800)): H(d, 'cannon', 2 if k % 2 == 0 else 160, y, 0.3 if k % 2 == 0 else 2.8, 7.5, 60)
P(d, 'big', 35, 40, SH['LIFT'])
H(d, 'chaser', 90, 3100, 'snowball', 5)
J.append(d)

ids = [j['id'] for j in J]
POS = {}
for k, i in enumerate(ids):
    y = 2926 - k * 61
    x = 40 if k % 2 == 0 else 140
    if i in ('terrain', 'snowshoe'): x = 20 if k % 2 == 0 else 160
    if i == 'grandslalom': x = 90
    POS[i] = [x, y]
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/ski.json', mappos=POS, landmark=LM, bossStars={'grandslalom': 24},
       story=['THE SKI RESORT IS BURIED!', 'THE PISTES ARE CLOSED', 'AND THE LIFTS ARE STUCK.', 'WATCH OUT FOR SKIERS!'])
