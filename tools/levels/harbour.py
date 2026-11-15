"""Frozen Harbour: 15 jobs (12 main, 2 side, 1 boss). The frozen sea is ice: once it's clear, you slide.
New mechanics: forklifts trundling round the docks (Container Yard), barriers that close after a warning
(Drawbridge, Canal Locks, Customs). Boss: the Harbour Festival, with the Forklift after you.  -> harbour.json"""
from common import *

J = []
SH = dict(FISH=39, WARE=40, CUSTOMS=41, MASTER=42, FERRIES=43, BOATSHED=44, ARCADE=33)
def quay_edge(d, x, y0, y1, step=60):
    for y in range(y0, y1, step): P(d, 'bollard', x, y)

# 1 FISH MARKET
d = job('fishmarket', 'FISH MARKET', 'harbour', ['openingday'], 2600, 62, 10.8, 7, start=[90, 2560])
G(d, 'conc', 0, 0, 180, 2600)
P(d, 'big', 35, 2300, SH['FISH'])
for y in range(300, 2200, 150): P(d, 'stall', 4, y, (y // 150) % 4); P(d, 'stall', 146, y + 70, (y // 150 + 1) % 4)
for y in range(400, 2200, 300): P(d, 'crate', 82, y); P(d, 'barrel', 96, y + 6)
H(d, 'gull', 60, 600, 5); H(d, 'gull', 100, 1500, 5); H(d, 'pedx', 40, 1000); H(d, 'pedx', 120, 1900, 1); H(d, 'cart', 80, 1200)
P(d, 'car', 140, 60, 4); P(d, 'car', 10, 60, 1)
J.append(d)

# 2 QUAYSIDE
d = job('quay', 'QUAYSIDE', 'harbour', ['fishmarket'], 2800, 66, 11.0, 7, start=[50, 40])
G(d, 'conc', 0, 0, 104, 2800); G(d, 'ice', 104, 0, 76, 2800); G(d, 'wht', 102, 0, 2, 2800)
quay_edge(d, 96, 100, 2700, 140)
for k, y in enumerate(range(150, 2700, 330)): P(d, 'boat', 132 if k % 2 else 112, y, k % 4)
for y in range(250, 2700, 260): P(d, 'crate', 10, y); P(d, 'crate', 26, y); P(d, 'anchor', 60, y + 120)
H(d, 'gull', 50, 800, 6); H(d, 'gull', 40, 2000, 5); H(d, 'pedx', 30, 1400); H(d, 'thrower', 70, 2300)
J.append(d)

# 3 LIGHTHOUSE POINT
d = job('lighthouse', 'LIGHTHOUSE POINT', 'harbour', ['quay'], 2600, 63, 11.2, 7, start=[90, 2560])
G(d, 'grass', 0, 0, 180, 2600); G(d, 'ice', 0, 0, 30, 2600); G(d, 'ice', 150, 0, 30, 2600)
P(d, 'lighthouse', 77, 40); C(d, 'conc', 90, 100, 40)
for k, y in enumerate(range(250, 2400, 160)): P(d, 'rock', 4 if k % 2 else 152, y, 24); P(d, 'rock', 40 if k % 3 == 0 else 120, y + 80, 14)
for y in range(400, 2400, 400): P(d, 'bench', 84, y)
H(d, 'gull', 70, 700, 6); H(d, 'gull', 110, 1700, 5); H(d, 'thrower', 30, 1200)
J.append(d)

# 4 CONTAINER YARD  (new: forklifts)
d = job('containers', 'CONTAINER YARD', 'harbour', ['lighthouse'], 3000, 68, 11.4, 7, start=[90, 2960])
G(d, 'asph', 0, 0, 180, 3000)
for k, y in enumerate(range(150, 2800, 120)):
    if k % 2 == 0: P(d, 'container', 2, y, k % 6); P(d, 'container', 2, y + 16, (k + 1) % 6); P(d, 'container', 134, y, (k + 2) % 6)
    else: P(d, 'container', 66, y, k % 6); P(d, 'container', 66, y + 16, (k + 3) % 6)
for y in range(400, 2800, 500): H(d, 'forklift', 40 if (y // 500) % 2 else 120, y + 60, (y // 500) % 2)
for x in range(4, 180, 24): G(d, 'yel', x, 2860, 12, 3)
H(d, 'thrower', 150, 1300)
J.append(d)

# 5 BOATYARD
d = job('boatyard', 'BOATYARD', 'harbour', ['containers'], 2800, 64, 11.6, 7, start=[90, 40])
G(d, 'conc', 0, 0, 180, 2200); G(d, 'wood', 60, 2200, 60, 300); G(d, 'ice', 0, 2500, 180, 300)
P(d, 'big', 35, 60, SH['BOATSHED'])
for k, y in enumerate(range(300, 2100, 220)): P(d, 'boat', 6 if k % 2 == 0 else 144, y, k % 4); P(d, 'barrel', 110 if k % 2 == 0 else 60, y + 100)
H(d, 'forklift', 90, 900, 1); H(d, 'forklift', 90, 1700, 0); H(d, 'gull', 100, 2600, 6); H(d, 'pedx', 40, 1300)
J.append(d)

# 6 FERRY TERMINAL
d = job('ferry', 'FERRY TERMINAL', 'harbour', ['boatyard'], 3000, 69, 11.8, 7, start=[90, 2960])
G(d, 'asph', 0, 600, 180, 2400); G(d, 'ice', 0, 0, 180, 600)
P(d, 'hull', 45, 120)
for x in (60, 116):
    for y in range(900, 2500, 70): G(d, 'wht', x, y, 2, 30)
for k, y in enumerate(range(900, 2500, 210)): d['data']['pull'].append([12 + (k % 3) * 58, y, k % 5])
P(d, 'big', 35, 2600, SH['FERRIES']); H(d, 'barrier', 50, 800, 80, 5.0)
H(d, 'ped', 160, 1500); H(d, 'gull', 60, 300, 6)
J.append(d)

# 7 DRAWBRIDGE  (new: barriers close after a warning)
d = job('drawbridge', 'DRAWBRIDGE', 'harbour', ['ferry'], 3000, 71, 12.0, 7, start=[90, 40])
G(d, 'conc', 0, 0, 180, 3000)
for k, yc in enumerate((500, 1100, 1700, 2300)):
    G(d, 'ice', 0, yc, 180, 120); G(d, 'wood', 50, yc, 80, 120)
    P(d, 'rail', 0, yc - 6, 50); P(d, 'rail', 130, yc - 6, 50); P(d, 'rail', 0, yc + 120, 50); P(d, 'rail', 130, yc + 120, 50)
    H(d, 'barrier', 50, yc - 14, 80, 4.5 + k * 0.4)
for y in range(200, 2900, 600): P(d, 'crate', 10, y); P(d, 'lamp', 160, y + 200)
H(d, 'gull', 100, 800, 5); H(d, 'forklift', 90, 2000, 0); H(d, 'pedx', 40, 1400)
J.append(d)

# 8 ICE FISHING
d = job('icefish', 'ICE FISHING', 'harbour', ['drawbridge'], 2800, 66, 12.2, 7, start=[90, 2760])
G(d, 'ice', 0, 0, 180, 2800); G(d, 'conc', 0, 2600, 180, 200)
for k, y in enumerate(range(150, 2500, 190)):
    P(d, 'hut', 8 if k % 2 == 0 else 156, y, k % 4); C(d, 'asph', 30 if k % 2 == 0 else 150, y + 30, 3)
    if k % 3 == 1: P(d, 'hut', 82, y + 90, (k + 1) % 4)
for y in range(300, 2500, 500): H(d, 'pedx', 40, y, (y // 500) % 2)
H(d, 'gull', 60, 1200, 6); H(d, 'thrower', 120, 2000)
J.append(d)

# 9 PIER ARCADE  (side)
d = job('pier', 'PIER ARCADE', 'harbour', ['icefish'], 2400, 61, 12.2, 9, start=[90, 2360], bonus=True)
G(d, 'ice', 0, 0, 180, 2400); G(d, 'wood', 20, 0, 140, 2400)
for y in range(100, 2300, 120): P(d, 'bollard', 20, y); P(d, 'bollard', 155, y)
P(d, 'big', 35, 40, SH['ARCADE'])
for y in range(400, 2200, 300): P(d, 'stall', 26 if (y // 300) % 2 else 124, y, (y // 300) % 4)
for y in range(550, 2200, 600): P(d, 'balloons', 80, y)
H(d, 'gull', 70, 900, 6); H(d, 'gull', 100, 1800, 6); H(d, 'pedx', 40, 1200)
J.append(d)

# 10 CUSTOMS HOUSE
d = job('customs', 'CUSTOMS HOUSE', 'harbour', ['icefish'], 3000, 70, 12.4, 7, start=[90, 2960])
G(d, 'asph', 0, 0, 180, 3000); P(d, 'big', 35, 60, SH['CUSTOMS'])
for k, y in enumerate(range(600, 2700, 500)):
    P(d, 'booth', 82, y, k % 3); H(d, 'barrier', 8, y + 30, 70, 5.0); H(d, 'barrier', 102, y + 30, 70, 5.6)
    for x in range(4, 180, 30): G(d, 'wht', x, y + 60, 16, 2)
H(d, 'forklift', 40, 1300, 1); H(d, 'forklift', 140, 2200, 1); H(d, 'ped', 160, 900)
J.append(d)

# 11 CANAL LOCKS
d = job('locks', 'CANAL LOCKS', 'harbour', ['customs'], 3000, 69, 12.6, 7, start=[90, 40])
G(d, 'grass', 0, 0, 180, 3000); G(d, 'ice', 60, 0, 60, 3000); G(d, 'conc', 0, 0, 60, 3000); G(d, 'conc', 120, 0, 60, 3000)
for k, y in enumerate(range(400, 2800, 600)): H(d, 'barrier', 60, y, 60, 5.0 + (k % 2)); P(d, 'boat', 76, y + 120, k % 4)
for y in range(200, 2900, 400): P(d, 'bench', 20, y); P(d, 'lamp', 160, y + 200)
H(d, 'gull', 140, 1300, 5); H(d, 'pedx', 20, 1800); H(d, 'thrower', 150, 600)
J.append(d)

# 12 GULL ISLAND  (side)
d = job('gullisland', 'GULL ISLAND', 'harbour', ['locks'], 2400, 61, 12.6, 9, start=[90, 2360], bonus=True)
G(d, 'ice', 0, 0, 180, 2400); C(d, 'grass', 90, 1200, 70); C(d, 'grass', 90, 600, 60); C(d, 'grass', 90, 1800, 60)
P(d, 'lighthouse', 77, 1150)
for (x, y) in [(20, 300), (140, 500), (30, 900), (140, 1500), (20, 2000), (150, 2100)]: P(d, 'rock', x, y, 20)
for y in range(300, 2300, 400): H(d, 'gull', 70, y, 6)
J.append(d)

# 13 SHIPYARD
d = job('shipyard', 'SHIPYARD', 'harbour', ['locks'], 3200, 71, 12.8, 7, start=[90, 3160])
G(d, 'conc', 0, 0, 180, 3200); G(d, 'ice', 40, 300, 100, 1200)
P(d, 'hull', 45, 900); P(d, 'gantry', 55, 600)
for y in range(1700, 3000, 220): P(d, 'container', 2, y, (y // 220) % 6); P(d, 'container', 134, y + 100, (y // 220 + 2) % 6)
for y in range(1800, 3000, 400): H(d, 'forklift', 90, y, (y // 400) % 2)
P(d, 'gantry', 55, 100); H(d, 'cannon', 2, 1300, 0.2, 7.0, 60)
J.append(d)

# 14 ICEBREAKER DOCK
d = job('icebreaker', 'ICEBREAKER DOCK', 'harbour', ['shipyard'], 3200, 71, 13.0, 7, start=[90, 40])
G(d, 'conc', 0, 0, 180, 1400); G(d, 'ice', 0, 1400, 180, 1800)
P(d, 'big', 35, 60, SH['MASTER']); P(d, 'hull', 45, 1700)
for k, y in enumerate(range(300, 1300, 200)): P(d, 'container', 2 if k % 2 else 134, y, k % 6); H(d, 'barrier', 50, y + 100, 80, 5.0 + k % 2)
H(d, 'cannon', 2, 2200, 0.2, 7.0, 64); H(d, 'cannon', 160, 2600, 3.0, 7.0, 64); H(d, 'gull', 100, 1500, 6); H(d, 'forklift', 90, 700, 0)
J.append(d)

# 15 HARBOUR FESTIVAL  (boss)
d = job('festival', 'HARBOUR FESTIVAL', 'harbour', ['icebreaker'], 3400, 75, 13.4, 9, start=[90, 3360], boss=True)
G(d, 'conc', 0, 0, 180, 3400); G(d, 'ice', 120, 0, 60, 3400)
for y in range(140, 3400, 240): d['data']['decor'].append(['bunting', 0, y, 120])
for k, y in enumerate(range(200, 3200, 400)): P(d, 'boat', 136, y, k % 4)
for y in range(300, 3200, 300): P(d, 'stall', 4, y, (y // 300) % 4)
for k, y in enumerate((900, 1800, 2700)): H(d, 'barrier', 40, y, 70, 5.0 + k * 0.5)
H(d, 'gull', 80, 600, 6); H(d, 'gull', 80, 2200, 6); H(d, 'pedx', 40, 1300); H(d, 'pedx', 60, 2500, 1)
H(d, 'chaser', 100, 3000, 'forklift', 5)
J.append(d)

ids = [j['id'] for j in J]
POS = {}
for k, i in enumerate(ids):
    y = 3890 - k * 61
    x = 40 if k % 2 == 0 else 140
    if i in ('pier', 'gullisland'): x = 20 if k % 2 == 0 else 160
    if i == 'festival': x = 90
    POS[i] = [x, y]
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/harbour.json', mappos=POS, landmark=LM, bossStars={'festival': 26},
       story=['THE HARBOUR HAS FROZEN!', 'THE BOATS ARE STUCK FAST', 'AND THE DOCKS ARE BURIED.', 'MIND THE ICE: IT IS SLIPPY!'])
