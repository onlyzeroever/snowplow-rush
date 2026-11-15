"""Mountain Pass: 15 jobs (12 main, 2 side, 1 boss). New mechanics: rockfall (rocks come down after a warning
arrow), whiteout gusts (squall). Boss: The Blizzard Pass, with the Yeti.  -> pass.json"""
from common import *

J = []
SH = dict(HUT=50, WEATHER=51)
def road(d, h): G(d, 'asph', 40, 0, 100, h); G(d, 'wht', 40, 0, 2, h); G(d, 'wht', 138, 0, 2, h)
def poles(d, h, step=120):
    for y in range(60, h - 40, step): P(d, 'snowpole', 32, y); P(d, 'snowpole', 144, y + 60)
def cliffs(d, h, step=110, y0=30):
    for k, y in enumerate(range(y0, h - 30, step)): P(d, 'rock', 0, y, 28 + (k % 3) * 4); P(d, 'rock', 148, y + 50, 28 + ((k + 1) % 3) * 2)
def serp(d, y0, y1, gap=56, step=170):
    """guard rails from alternate sides, leaving a 56-wide way round: a switchback road"""
    for k, y in enumerate(range(y0, y1, step)):
        if k % 2 == 0: P(d, 'rail', 0, y, 180 - gap)
        else: P(d, 'rail', gap, y, 180 - gap)

d = job('hairpin', 'HAIRPIN BEND', 'pass', ['grandslalom'], 3000, 75, 17.0, 7, start=[90, 2960]); serp(d, 300, 2800, 70)
for k, y in enumerate(range(300, 2800, 170)): P(d, 'warnsign', 80, y + 70)
H(d, 'thrower', 120, 1500); J.append(d)
d = job('snowshed', 'SNOW SHED', 'pass', ['hairpin'], 3000, 72, 17.3, 7, start=[90, 40]); road(d, 3000)
for k, y in enumerate(range(200, 2800, 400)): P(d, 'icewallv', 30, y, 200); P(d, 'icewallv', 140, y + 100, 200)
poles(d, 3000, 240); H(d, 'pedx', 60, 1300); J.append(d)
d = job('tunnel', 'TUNNEL MOUTH', 'pass', ['snowshed'], 3000, 71, 17.6, 7, start=[90, 2960]); road(d, 3000)
for k, y in enumerate(range(300, 2700, 600)): P(d, 'tunnel', 0 if k % 2 == 0 else 90, y)
cliffs(d, 3000, 200); poles(d, 3000, 300); J.append(d)
d = job('rockfall', 'ROCKFALL ROAD', 'pass', ['tunnel'], 3000, 72, 17.9, 7, start=[90, 40]); road(d, 3000); cliffs(d, 3000, 130)
for x in (60, 100, 130): H(d, 'rockfall', x, 0, 5.0 + x / 50)
for y in range(400, 2900, 500): P(d, 'warnsign', 34, y)
J.append(d)
d = job('mhut', 'MOUNTAIN HUT', 'pass', ['rockfall'], 2800, 67, 18.2, 7, start=[90, 2760])
P(d, 'big', 35, 60, SH['HUT'])
for k, y in enumerate(range(300, 2600, 220)):
    P(d, 'cairn', 10 if k % 2 == 0 else 156, y)
    if k % 3 == 0: P(d, 'bench', 80, y + 110)
    else: P(d, 'rock', 70, y + 110, 18)
cliffs(d, 2800, 240); H(d, 'dog', 90, 1500); H(d, 'pedx', 40, 900); J.append(d)
d = job('avalanche', 'AVALANCHE FENCES', 'pass', ['mhut'], 3000, 73, 18.5, 7, start=[90, 40], squall=1)
for k, y in enumerate(range(200, 2900, 150)): P(d, 'stonewall' if k % 3 == 0 else 'rail', 0 if k % 2 == 0 else 60, y, 120)
H(d, 'rockfall', 150, 0, 6.0); J.append(d)
d = job('weather', 'WEATHER STATION', 'pass', ['avalanche'], 3000, 71, 18.8, 7, start=[90, 2960])
P(d, 'big', 35, 80, SH['WEATHER']); P(d, 'mast', 6, 300); P(d, 'mast', 156, 600)
for y in range(900, 2800, 300): P(d, 'container', 2 if (y // 300) % 2 else 134, y, (y // 300) % 6)
cliffs(d, 3000, 260); H(d, 'cannon', 2, 1800, 0.3, 7.0, 64); J.append(d)
d = job('waterfall', 'FROZEN WATERFALL', 'pass', ['weather'], 2600, 67, 18.8, 9, start=[90, 2560], bonus=True)
G(d, 'ice', 30, 0, 120, 2600)
for k, y in enumerate(range(200, 2400, 200)): P(d, 'spire', 34 if k % 2 == 0 else 130, y)
cliffs(d, 2600, 200); J.append(d)
d = job('viewpoint', 'VIEWPOINT', 'pass', ['weather'], 2800, 68, 19.1, 7, start=[90, 40])
G(d, 'asph', 0, 0, 180, 900)
for y in range(80, 860, 120):
    for x in range(4, 176, 30): G(d, 'wht', x, y, 2, 40)
d['data']['pull'] += [[8, 200, 1], [128, 440, 3], [68, 680, 0]]
P(d, 'stonewall', 0, 2600, 70); P(d, 'stonewall', 110, 2600, 70)
for y in range(1000, 2500, 300): P(d, 'statue', 20, y); P(d, 'bench', 140, y + 150)
cliffs(d, 2800, 300); H(d, 'pedx', 60, 1500); J.append(d)
d = job('gorge', 'BRIDGE GORGE', 'pass', ['viewpoint'], 3000, 71, 19.4, 7, start=[90, 2960])
for k, yc in enumerate((600, 1500, 2300)):
    G(d, 'ice', 0, yc, 180, 140); G(d, 'wood', 40, yc, 100, 140); P(d, 'rail', 0, yc - 7, 40); P(d, 'rail', 140, yc - 7, 40); P(d, 'rail', 0, yc + 140, 40); P(d, 'rail', 140, yc + 140, 40)
    P(d, 'railv', 36, yc, 140); P(d, 'railv', 139, yc, 140)
cliffs(d, 3000, 200); H(d, 'rockfall', 70, 0, 6.5); J.append(d)
d = job('switchbacks', 'SWITCHBACKS', 'pass', ['gorge'], 3200, 77, 19.7, 7, start=[90, 40]); serp(d, 200, 3000, 56, 140)
H(d, 'rockfall', 40, 0, 6.0); H(d, 'rockfall', 140, 0, 7.0); J.append(d)
d = job('icecaves', 'ICE CAVES', 'pass', ['switchbacks'], 2600, 68, 19.7, 9, start=[90, 2560], bonus=True)
for k, y in enumerate(range(150, 2400, 130)):
    for x in ((10, 120) if k % 2 == 0 else (64,)): P(d, 'spire', x, y); P(d, 'rock', x + 24, y + 40, 16)
G(d, 'ice', 0, 0, 180, 2600); J.append(d)
d = job('cliffroad', 'CLIFF ROAD', 'pass', ['switchbacks'], 3200, 74, 20.0, 7, start=[90, 3160]); road(d, 3200); cliffs(d, 3200, 90)
for x in (60, 120): H(d, 'rockfall', x, 0, 4.5 + x / 60)
poles(d, 3200, 200); J.append(d)
d = job('summit', 'SUMMIT PASS', 'pass', ['cliffroad'], 3200, 78, 20.4, 7, start=[90, 40], squall=1)
for k, y in enumerate(range(200, 3000, 200)): P(d, 'snowpole', 50, y); P(d, 'snowpole', 126, y); P(d, 'cairn', 4 if k % 2 else 160, y + 100)
H(d, 'rockfall', 90, 0, 6.0); H(d, 'cannon', 2, 2000, 0.3, 7.0, 64); J.append(d)
d = job('blizzard', 'THE BLIZZARD PASS', 'pass', ['summit'], 3400, 78, 21.0, 9, start=[90, 3360], boss=True, squall=1)
road(d, 3400); cliffs(d, 3400, 140, 1500); serp(d, 400, 1400, 70, 200)
for x in (60, 120): H(d, 'rockfall', x, 0, 5.5 + x / 60)
for y in range(1600, 3200, 400): P(d, 'warnsign', 34, y)
H(d, 'cannon', 2, 2400, 0.3, 7.0, 64); H(d, 'chaser', 150, 3000, 'yeti', 5); J.append(d)

ids = [j['id'] for j in J]
POS = {}
for k, i in enumerate(ids):
    y = 1966 - k * 61
    x = 40 if k % 2 == 0 else 140
    if i in ('waterfall', 'icecaves'): x = 20 if k % 2 == 0 else 160
    if i == 'blizzard': x = 90
    POS[i] = [x, y]
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/pass.json', mappos=POS, landmark=LM, bossStars={'blizzard': 24},
       story=['THE MOUNTAIN PASS IS SHUT!', 'ROCKS, ICE AND BLIZZARDS', 'STAND BETWEEN YOU AND', 'THE FROZEN NORTH.'])
