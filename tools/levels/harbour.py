"""Frozen Harbour: 15 jobs. Pro pass lives in harbour_pro.py.  python3 harbour.py -> harbour.json"""
from common import *

J = []
# all fifteen jobs: pro pass in harbour_pro.py
import harbour_pro
for f in harbour_pro.ALL: J.append(f())
harbour_pro.dress(J)

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
