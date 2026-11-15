"""Ski Resort: 15 jobs (12 main, 2 side, 1 boss). New mechanics: skiers racing down after a warning arrow (Blue
Run onwards); snow guns re-cover the pistes (Snow Guns). Boss: The Grand Slalom, with a runaway snowball.  -> ski.json"""
from common import *

import ski_pro
J = [f() for f in ski_pro.ALL]

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
