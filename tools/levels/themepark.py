"""Theme Park: 15 jobs (12 main, 2 side, 1 boss). Pro pass lives in themepark_pro.py.  python3 themepark.py -> themepark.json"""
from common import *

J = []
# all fifteen jobs: pro pass in themepark_pro.py
import themepark_pro
for f in themepark_pro.ALL: J.append(f())
themepark_pro.densify(J)

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
