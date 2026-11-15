"""City part 2: 9 new jobs after the airport, played with the Super Plow (and the truck).
New mechanics: trams on a timetable (Train Station), junction cross-traffic (Downtown Junction), wind between the
towers (Skyline Plaza). Boss: the New Year Parade, with the Warden on your tail.  python3 city.py -> city.json"""
from common import *

J = []
def kerb_lights(d, x, y0, y1, step=120):
    for y in range(y0, y1, step): P(d, 'lamp', x, y)

# ---------------------------------------------------------------- CITY HALL (pro pass: city_pro.py)
import city_pro
J.append(city_pro.cityhall())

# ---------------------------------------------------------------- TRAIN STATION (pro pass)
J.append(city_pro.station())

# ---------------------------------------------------------------- HOSPITAL (pro pass)
J.append(city_pro.hospital())

# ---------------------------------------------------------------- MUSEUM (pro pass)
J.append(city_pro.museum())

# ---------------------------------------------------------------- CHINATOWN (pro pass)
J.append(city_pro.chinatown())

# ---------------------------------------------------------------- DOWNTOWN JUNCTION (pro pass)
J.append(city_pro.junction())

# ---------------------------------------------------------------- ICE RINK (pro pass)
J.append(city_pro.icerink())

# ---------------------------------------------------------------- SKYLINE PLAZA (pro pass)
J.append(city_pro.skyline())

# ---------------------------------------------------------------- NEW YEAR PARADE (pro pass)
J.append(city_pro.parade())

POS = {'cityhall': [50, 5404], 'station': [138, 5352], 'hospital': [44, 5290], 'museum': [136, 5232], 'chinatown': [52, 5170],
       'junction': [134, 5110], 'icerink': [24, 5040], 'skyline': [140, 5030], 'parade': [86, 4950]}
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/city.json', mappos=POS, landmark=LM, bossStars={'parade': 25})
