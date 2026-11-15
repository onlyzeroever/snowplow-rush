"""The Frozen North (finale): 15 jobs (12 main, 2 side, 1 boss). New mechanics: dog sleds racing across (Husky
Camp onwards), penguin huddles that scatter (Penguin Bay). Lots of ice. Final boss: The Ice Palace, with the polar
bear.  -> north.json"""
from common import *

J = []
SH = dict(BASE=52, PALACE=53, POST=54)
def icy(d, h): G(d, 'ice', 0, 0, 180, h)
def spires(d, h, step=160):
    for k, y in enumerate(range(100, h - 60, step)): P(d, 'spire', 4 if k % 2 == 0 else 160, y)

d = job('huskies', 'HUSKY CAMP', 'north', ['blizzard'], 3000, 68, 21.6, 7, start=[90, 2960])
for k, yc in enumerate((700, 1500, 2300)): G(d, 'conc', 0, yc - 4, 180, 30); H(d, 'cross', 0, yc, 1 if k % 2 == 0 else -1, 5.0, 'sled')
for k, y in enumerate(range(200, 2800, 260)):
    P(d, 'igloo', 4 if k % 2 == 0 else 146, y)
    if k % 3 == 0: P(d, 'crate', 80, y + 120)
H(d, 'dog', 90, 1100); H(d, 'dog', 60, 1900); J.append(d)
d = job('penguins', 'PENGUIN BAY', 'north', ['huskies'], 3000, 68, 22.0, 7, start=[90, 40]); icy(d, 3000)
for y in range(300, 2900, 450): H(d, 'peng', 60 if (y // 450) % 2 else 110, y, 7)
for y in range(200, 2900, 400): P(d, 'rock', 4 if (y // 400) % 2 else 150, y, 24)
J.append(d)
d = job('igloos', 'IGLOO VILLAGE', 'north', ['penguins'], 3000, 67, 22.4, 7, start=[90, 2960])
for k, y in enumerate(range(150, 2800, 180)):
    for x in ((6, 144) if k % 2 == 0 else (75,)): P(d, 'igloo', x, y)
H(d, 'peng', 90, 600, 5); H(d, 'pedx', 40, 1700); H(d, 'thrower', 140, 2300); J.append(d)
d = job('research', 'RESEARCH BASE', 'north', ['igloos'], 3000, 67, 22.8, 7, start=[90, 40])
P(d, 'big', 35, 80, SH['BASE']); P(d, 'mast', 6, 400); P(d, 'mast', 156, 700)
for y in range(900, 2800, 260): P(d, 'container', 2 if (y // 260) % 2 else 134, y, (y // 260) % 6)
H(d, 'cross', 0, 1500, 1, 5.5, 'sled'); H(d, 'cannon', 2, 2300, 0.3, 7.0, 64); J.append(d)
d = job('icefield', 'ICE FIELD', 'north', ['research'], 3000, 68, 23.2, 7, start=[90, 2960]); icy(d, 3000); spires(d, 3000, 140)
H(d, 'peng', 80, 1000, 6); H(d, 'peng', 90, 2200, 6); J.append(d)
d = job('frozenlake', 'FROZEN LAKE', 'north', ['icefield'], 3000, 68, 23.6, 7, start=[90, 40]); C(d, 'ice', 90, 1500, 85); C(d, 'ice', 90, 900, 70); C(d, 'ice', 90, 2100, 70)
for k, y in enumerate(range(600, 2500, 260)): P(d, 'hut', 50 if k % 2 == 0 else 116, y, k % 4)
H(d, 'peng', 60, 1800, 6); H(d, 'pedx', 40, 1200); J.append(d)
d = job('aurora', 'AURORA RIDGE', 'north', ['frozenlake'], 3200, 71, 24.0, 7, start=[90, 3160], squall=1)
for k, y in enumerate(range(200, 3000, 180)):
    P(d, 'rock', 0 if k % 2 == 0 else 150, y, 30)
    if k % 3 == 0: P(d, 'cairn', 80, y + 90)
H(d, 'rockfall', 60, 0, 6.0); H(d, 'rockfall', 120, 0, 7.5); J.append(d)
d = job('snowmen', 'SNOWMAN PARK', 'north', ['aurora'], 2600, 63, 24.0, 12, start=[90, 2560], bonus=True)
for k, y in enumerate(range(150, 2400, 90)):
    for x in ((20, 90, 160) if k % 2 == 0 else (55, 125)): P(d, 'snowman', x, y)
H(d, 'thrower', 40, 900); H(d, 'thrower', 140, 1800); J.append(d)
d = job('polartrail', 'POLAR TRAIL', 'north', ['aurora'], 3200, 72, 24.4, 7, start=[90, 40])
for k, yc in enumerate(range(500, 3000, 600)): G(d, 'conc', 0, yc - 4, 180, 30); H(d, 'cross', 0, yc, 1 if k % 2 == 0 else -1, 4.5, 'sled')
spires(d, 3200, 200); J.append(d)
d = job('spires', 'ICE SPIRES', 'north', ['polartrail'], 3200, 71, 24.8, 7, start=[90, 3160]); icy(d, 3200)
for k, y in enumerate(range(150, 3000, 120)):
    for x in ((10, 100) if k % 2 == 0 else (55, 150)): P(d, 'spire', x, y)
H(d, 'peng', 90, 1500, 6); J.append(d)
d = job('gardens2', 'PALACE GARDENS', 'north', ['spires'], 3200, 68, 25.2, 7, start=[90, 40])
for r in range(7):
    y = 200 + r * 400
    for x in ((10, 118) if r % 2 == 0 else (64,)):
        P(d, 'icewall', x, y, 52); P(d, 'icewall', x, y + 150, 52); P(d, 'icewallv', x, y + 10, 140); P(d, 'statue', x + 22, y + 70)
H(d, 'peng', 90, 1400, 5); H(d, 'thrower', 150, 2600); J.append(d)
d = job('northpole', 'NORTH POLE POST', 'north', ['gardens2'], 2600, 62, 25.2, 14, start=[90, 2560], bonus=True)
P(d, 'big', 35, 60, SH['POST'])
for y in range(400, 2400, 300): P(d, 'crate', 10, y); P(d, 'crate', 156, y + 150); P(d, 'flag', 86, y + 70, (y // 300) % 4)
H(d, 'pedx', 40, 1300); H(d, 'dog', 90, 2000); J.append(d)
d = job('palacegates', 'PALACE GATES', 'north', ['gardens2'], 3200, 70, 25.6, 7, start=[90, 3160])
for k, y in enumerate(range(400, 3000, 500)):
    P(d, 'icewall', 0, y, 62); P(d, 'icewall', 118, y, 62); H(d, 'barrier', 62, y, 56, 5.0 + (k % 2))
    P(d, 'spire', 40, y - 40); P(d, 'spire', 126, y - 40)
H(d, 'cannon', 2, 1500, 0.3, 7.0, 64); H(d, 'peng', 90, 2400, 5); J.append(d)
d = job('greathall', 'THE GREAT HALL', 'north', ['palacegates'], 3200, 63, 26.0, 7, start=[90, 40]); icy(d, 3200)
P(d, 'icewallv', 0, 0, 3200); P(d, 'icewallv', 170, 0, 3200)
for k, y in enumerate(range(300, 3000, 220)): P(d, 'spire', 40, y); P(d, 'spire', 124, y)
for y in range(500, 3000, 600): P(d, 'statue', 86, y)
H(d, 'peng', 90, 1200, 6); H(d, 'thrower', 90, 2400); J.append(d)
d = job('icepalace', 'THE ICE PALACE', 'north', ['greathall'], 3600, 75, 27.0, 10, start=[90, 3560], boss=True)
icy(d, 3600); P(d, 'big', 35, 40, SH['PALACE'])
for y in range(160, 3600, 260): d['data']['decor'].append(['bunting', 0, y, 180])
for k, y in enumerate(range(400, 3300, 500)): P(d, 'icewall', 0, y, 62); P(d, 'icewall', 118, y, 62); P(d, 'spire', 82, y + 200)
for k, yc in enumerate((900, 1900, 2900)): H(d, 'cross', 0, yc + 60, 1 if k % 2 == 0 else -1, 5.0, 'sled')
H(d, 'peng', 60, 1300, 6); H(d, 'peng', 110, 2500, 6); H(d, 'cannon', 2, 2000, 0.3, 7.0, 64)
H(d, 'chaser', 150, 3200, 'bear', 5); J.append(d)

ids = [j['id'] for j in J]
POS = {}
for k, i in enumerate(ids):
    y = 1006 - k * 62
    x = 40 if k % 2 == 0 else 140
    if i in ('snowmen', 'northpole'): x = 20 if k % 2 == 0 else 160
    if i == 'icepalace': x = 90
    POS[i] = [x, y]
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/north.json', mappos=POS, landmark=LM, bossStars={'icepalace': 28},
       story=['THE FROZEN NORTH AT LAST!', 'PENGUINS, HUSKIES AND', 'THE ICE PALACE ITSELF.', 'THIS IS THE BIG ONE!'])
