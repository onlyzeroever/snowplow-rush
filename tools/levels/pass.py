"""Mountain Pass: 15 jobs (12 main, 2 side, 1 boss). New mechanics: rockfall (rocks come down after a warning
arrow), whiteout gusts (squall). Boss: The Blizzard Pass, with the Yeti.  -> pass.json"""
from common import *

import pass_pro
J = [f() for f in pass_pro.ALL]

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
