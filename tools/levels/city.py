"""City part 2: 9 new jobs after the airport, played with the Super Plow (and the truck).
New mechanics: trams on a timetable (Train Station), junction cross-traffic (Downtown Junction), wind between the
towers (Skyline Plaza). Boss: the New Year Parade, with the Warden on your tail.  python3 city.py -> city.json"""
from common import *

J = []
def kerb_lights(d, x, y0, y1, step=120):
    for y in range(y0, y1, step): P(d, 'lamp', x, y)

# ---------------------------------------------------------------- CITY HALL
d = job('cityhall', 'CITY HALL', 'city', ['airport'], 2400, 58, 6.2, 7, start=[90, 2360])
G(d, 'asph', 0, 0, 180, 2400)
G(d, 'conc', 0, 1500, 180, 820)                                    # the civic plaza
for k in range(10): G(d, 'wht', 30, 1520 + k * 8, 120, 3)           # steps up to the hall
P(d, 'big', 35, 1440, 22)
for x in (6, 22, 150, 166): P(d, 'flag', x, 1600, (x // 16) % 4)
C(d, 'wht', 50, 1800, 26); C(d, 'conc', 50, 1800, 23); P(d, 'fountain', 37, 1787)
C(d, 'wht', 130, 1980, 26); C(d, 'conc', 130, 1980, 23); P(d, 'fountain', 117, 1967)
for x, y in [(130, 1760), (50, 2000)]: P(d, 'statue', x, y)
for x, y in [(4, 1700), (164, 1700), (4, 2100), (164, 2100)]: P(d, 'planter', x, y)
for x, y in [(80, 1900), (96, 1900), (80, 2160), (96, 2160)]: P(d, 'bench', x, y)
H(d, 'ped', 20, 1900); H(d, 'ped', 150, 2050, 1); H(d, 'pedx', 60, 2240); H(d, 'thrower', 150, 1880)
# avenue up to the old town hall square (y 0-1440): offices both sides, traffic in the middle lane
for y in range(0, 1250, 104): P(d, 'tower', 0, y, (y // 104) % 5); P(d, 'tower', 130, y + 40, (y // 104 + 2) % 5)
for y in range(20, 1440, 24): G(d, 'wht', 89, y, 2, 12)
H(d, 'taxi', 96, -60, 0); H(d, 'taxi', 62, 600, 1)
kerb_lights(d, 52, 60, 1400); kerb_lights(d, 124, 120, 1400)
d['data']['pull'] += [[56, 300, 1], [102, 900, 3]]
J.append(d)

# ---------------------------------------------------------------- TRAIN STATION  (new: trams)
# Platforms between parked trains, a tram line that runs up and down all job long, the taxi rank.
d = job('station', 'TRAIN STATION', 'city', ['cityhall'], 2800, 68, 6.4, 7, start=[70, 2760])
G(d, 'conc', 0, 0, 180, 2800)
# the tram line on the right (x 140-170): rails painted, a tram running
for x in (144, 164): G(d, 'asph', x, 0, 3, 2800)
H(d, 'taxi', 144, 200, 4); H(d, 'taxi', 144, 1600, 5)
# station building and concourse (y 2300-2700)
P(d, 'big', 4, 2300, 23); P(d, 'busstop', 100, 2560); P(d, 'kiosk', 6, 2640, 1)
for x in (14, 44, 74): P(d, 'car', x, 2440, 2)                     # taxi rank (yellow cabs)
H(d, 'ped', 110, 2400); H(d, 'pedx', 30, 2520)
# platforms (y 300-2200): tracks with parked trains, platforms between them 52 wide
for k, x in enumerate((0, 74)):
    P(d, 'track', x, 300, 1900); P(d, 'train', x, 420 + k * 300, 238)
for y in range(400, 2200, 260): P(d, 'bench', 24, y); P(d, 'bench', 98, y + 120)
for y in range(500, 2200, 400): P(d, 'kiosk', 24, y, 2)
H(d, 'ped', 40, 900); H(d, 'ped', 112, 1500, 1); H(d, 'thrower', 116, 700)
# goods yard at the top
G(d, 'asph', 0, 0, 130, 280)
for x, y in [(6, 40), (34, 40), (62, 40), (6, 120), (62, 140)]: P(d, 'crate', x, y)
P(d, 'barrel', 100, 60); P(d, 'barrel', 110, 60); P(d, 'tires', 96, 200)
J.append(d)

# ---------------------------------------------------------------- HOSPITAL
# Keep the ambulance route clear (a paramedic waits for it), the helipad, a busy car park.
d = job('hospital', 'HOSPITAL', 'city', ['station'], 2600, 75, 6.6, 7, start=[90, 40])
G(d, 'asph', 0, 0, 180, 2600)
P(d, 'big', 35, 80, 24); G(d, 'conc', 0, 138, 180, 160)
G(d, 'red', 60, 160, 60, 120)                                       # ambulance bay
for k in range(4): G(d, 'yel', 64 + k * 14, 170, 8, 100)
d['data']['neighbours'] = [dict(rects=[[60, 300, 60, 600]], path=[[90, 900], [90, 300], [90, 170]])]
C(d, 'yel', 90, 1200, 46); C(d, 'asph', 90, 1200, 42); d['data']['paint'] += [['H', 82, 1188, 3]]
# car park (y 1350-2300) with pull cars and bays
for y in range(1360, 2300, 120):
    for x in range(4, 176, 30): G(d, 'wht', x, y, 2, 34)
    P(d, 'car', 6 if (y // 120) % 2 else 126, y + 2, (y // 120) % 5)
    if (y // 120) % 3 == 0: d['data']['pull'].append([96, y + 2, 2])
H(d, 'cart', 90, 1700); H(d, 'ped', 40, 1500); H(d, 'ped', 150, 2000, 1)
for x, y in [(0, 2380), (60, 2400), (120, 2380)]: P(d, 'oak', x, y)
P(d, 'bench', 30, 2500); P(d, 'bench', 140, 2500); H(d, 'pedx', 60, 2540)
kerb_lights(d, 4, 400, 1300, 200); kerb_lights(d, 170, 500, 1300, 200)
J.append(d)

# ---------------------------------------------------------------- MUSEUM
# The museum steps, a formal garden of hedges (paths 50 wide), sculptures, food trucks for the crowds.
d = job('museum', 'MUSEUM', 'city', ['hospital'], 2600, 71, 6.8, 7, start=[90, 2560])
G(d, 'conc', 0, 0, 180, 2600)
P(d, 'museum', 30, 40)
for k in range(8): G(d, 'wht', 24, 106 + k * 7, 132, 3)
for x, y in [(6, 60), (160, 60)]: P(d, 'statue', x, y)
# the formal garden (y 300-1700): hedge beds in a grid, paths 52 wide between them
G(d, 'grass', 0, 300, 180, 1400)
for r in range(6):
    y = 340 + r * 220
    for x in ((10, 118) if r % 2 == 0 else (64,)):
        wallbox(d, x, y, x + 52, y + 120, [('t', x + 16, x + 36)], kind='hedge')
        P(d, 'statue', x + 22, y + 54)
for y in range(400, 1700, 300): P(d, 'bench', 4, y); P(d, 'bench', 164, y + 150)
H(d, 'ped', 92, 900); H(d, 'thrower', 20, 1300); H(d, 'pedx', 60, 1680)
# the queue and the food trucks (y 1750-2500)
for k in range(5): P(d, 'foodtruck', 4 + (k % 2) * 150, 1780 + k * 140, k % 3)
for y in range(1800, 2500, 180): P(d, 'bollard', 90, y)
H(d, 'pedx', 40, 2000); H(d, 'pedx', 120, 2300, 1); H(d, 'ped', 60, 2200)
J.append(d)

# ---------------------------------------------------------------- CHINATOWN
d = job('chinatown', 'CHINATOWN', 'city', ['museum'], 2800, 66, 7.0, 7, start=[90, 40])
G(d, 'asph', 0, 0, 180, 2800); G(d, 'red', 46, 0, 88, 2800)
for y in range(150, 2800, 220): d['data']['decor'].append(['lanterns', 40, y, 100])
names = [25, 26, 27]
y = 100
while y < 2650:
    P(d, 'shopv', 0, y, names[(y // 90) % 3]); P(d, 'shopv', 136, y + 36, names[(y // 90 + 1) % 3])
    y += 150
for y in range(260, 2700, 300): P(d, 'stall', 50 if (y // 300) % 2 else 100, y, (y // 300) % 4)
for y in range(200, 2700, 260): P(d, 'lamp', 46 if (y // 260) % 2 else 128, y)
H(d, 'pedx', 60, 500); H(d, 'pedx', 100, 1100, 1); H(d, 'pedx', 60, 1700); H(d, 'pedx', 110, 2300, 1); H(d, 'ped', 70, 800); H(d, 'ped', 108, 2000, 1)
H(d, 'thrower', 90, 1400); H(d, 'cart', 80, 2500)
J.append(d)

# ---------------------------------------------------------------- DOWNTOWN JUNCTION  (new: cross traffic)
# Three busy cross streets: cars come through after a warning. Towers on the corners, a taxi in the avenue.
d = job('junction', 'DOWNTOWN JUNCTION', 'city', ['chinatown'], 3000, 81, 7.2, 7, start=[90, 2960])
G(d, 'asph', 0, 0, 180, 3000)
for y in range(0, 3000, 24): G(d, 'wht', 89, y, 2, 12)
for k, yc in enumerate((600, 1400, 2200)):
    G(d, 'asph', 0, yc, 180, 50)
    for x in range(4, 180, 16): G(d, 'wht', x, yc + 24, 8, 2)
    for kk in range(8): G(d, 'wht', 50 + kk * 10, yc - 30, 6, 24); G(d, 'wht', 50 + kk * 10, yc + 56, 6, 24)
    H(d, 'cross', 0, yc + 8, 1, 4.5, 'car'); H(d, 'cross', 0, yc + 30, -1, 5.0, 'car')
for yb in (100, 760, 1560, 2360):
    P(d, 'tower', 0, yb, (yb // 100) % 5); P(d, 'tower', 130, yb + 60, (yb // 100 + 1) % 5)
    if yb < 2300: P(d, 'towerw', 0, yb + 130, (yb // 100 + 2) % 5)
H(d, 'taxi', 96, 0, 0); H(d, 'ped', 54, 400); H(d, 'ped', 120, 1800, 1)
for y in range(300, 2900, 500): P(d, 'hydrant', 52, y); P(d, 'trash', 122, y + 200)
J.append(d)

# ---------------------------------------------------------------- ICE RINK  (side job)
# A huge rink: once it's clear it's slippery. Skaters zip across. Hot chocolate at the side.
d = job('icerink', 'ICE RINK', 'city', ['junction'], 2200, 64, 7.2, 9, start=[90, 2160], bonus=True)
G(d, 'conc', 0, 0, 180, 2200)
G(d, 'ice', 10, 300, 160, 1500)
wallbox(d, 8, 298, 172, 1802, [('b', 60, 120), ('t', 60, 120), ('l', 900, 960), ('r', 1100, 1160)], kind='rail')
for y in range(420, 1700, 200): H(d, 'pedx', 30 if (y // 200) % 2 else 120, y, (y // 200) % 2)
P(d, 'big', 35, 1880, 30); P(d, 'kiosk', 6, 2000, 3); P(d, 'kiosk', 156, 2000, 1); P(d, 'bench', 40, 2100); P(d, 'bench', 130, 2100)
for x in range(10, 170, 40): P(d, 'pine', x, 40, 22)
P(d, 'stage', 50, 120); H(d, 'thrower', 150, 200)
J.append(d)

# ---------------------------------------------------------------- SKYLINE PLAZA  (wind between the towers)
d = job('skyline', 'SKYLINE PLAZA', 'city', ['junction'], 3200, 73, 7.4, 7, start=[90, 40], squall=1)
G(d, 'conc', 0, 0, 180, 3200)
for k, y in enumerate(range(120, 3000, 260)):
    if k % 2 == 0: P(d, 'towerw', 0, y, k % 5); P(d, 'tower', 130, y + 80, (k + 1) % 5)
    else: P(d, 'tower', 0, y + 60, (k + 2) % 5); P(d, 'towerw', 110, y, (k + 3) % 5)
for k, y in enumerate(range(120 + 150, 3000, 520)): P(d, 'foodtruck', 77, y, k % 3)
for k, y in enumerate(range(120 + 200, 3000, 260)): P(d, 'planter', 58 if k % 2 else 108, y)
H(d, 'pedx', 60, 700); H(d, 'pedx', 100, 1500, 1); H(d, 'pedx', 60, 2300); H(d, 'cart', 80, 1100); H(d, 'thrower', 90, 2700)
J.append(d)

# ---------------------------------------------------------------- NEW YEAR PARADE  (boss)
# Floats roll across the route at the junctions, crowds behind the barriers, lanterns overhead, and the
# Warden wants to give you a ticket.
d = job('parade', 'NEW YEAR PARADE', 'city', ['skyline'], 3400, 91, 7.6, 9, start=[90, 3360], boss=True)
G(d, 'asph', 0, 0, 180, 3400); G(d, 'red', 40, 0, 100, 3400)
for y in range(100, 3400, 240): d['data']['decor'].append(['lanterns' if (y // 240) % 2 else 'bunting', 36, y, 108])
for k, yc in enumerate((500, 1200, 1900, 2600)):
    G(d, 'asph', 0, yc, 180, 40); H(d, 'cross', 0, yc + 8, 1 if k % 2 == 0 else -1, 6.5, 'float')
for y in range(60, 3360, 140):
    if any(abs(y - yc) < 90 for yc in (500, 1200, 1900, 2600)): continue
    P(d, 'rail', 0, y, 34); P(d, 'rail', 146, y, 34)
for y in range(300, 3300, 420): H(d, 'ped', 10, y); H(d, 'ped', 160, y + 200, 1)
for y in range(700, 3300, 700): P(d, 'foodtruck', 4, y, (y // 700) % 3); P(d, 'foodtruck', 150, y + 300, (y // 700 + 1) % 3)
P(d, 'stage', 50, 60); P(d, 'speaker', 36, 70); P(d, 'speaker', 134, 70)
H(d, 'thrower', 60, 1500); H(d, 'thrower', 120, 2900)
H(d, 'chaser', 160, 3000, 'warden', 5)
J.append(d)

POS = {'cityhall': [50, 5404], 'station': [138, 5352], 'hospital': [44, 5290], 'museum': [136, 5232], 'chinatown': [52, 5170],
       'junction': [134, 5110], 'icerink': [24, 5040], 'skyline': [140, 5030], 'parade': [86, 4950]}
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/city.json', mappos=POS, landmark=LM, bossStars={'parade': 25})
