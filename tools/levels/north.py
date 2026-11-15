"""The Frozen North (finale): 15 jobs (12 main, 2 side, 1 boss). New mechanics: dog sleds racing across (Husky
Camp onwards), penguin huddles that scatter (Penguin Bay). Lots of ice. Final boss: The Ice Palace, with the polar
bear.  -> north.json"""
from common import *

import north_pro
J = [f() for f in north_pro.ALL]

# longer late-game jobs (Nov 16): same layouts stretched vertically so rounds don't get shorter at the end
STRETCH = {'icepalace': 1.75, 'aurora': 1.9, 'spires': 1.9}
for j in J: stretch(j, STRETCH.get(j['id'], 1.6))

ids = [j['id'] for j in J]
POS = {}
for k, i in enumerate(ids):
    y = 1006 - k * 62
    x = 40 if k % 2 == 0 else 140
    if i in ('snowmen', 'northpole'): x = 20 if k % 2 == 0 else 160
    if i == 'icepalace': x = 90
    POS[i] = [x, y]
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/north.json', mappos=POS, landmark=LM, bossStars={'icepalace': 24},
       story=['THE FROZEN NORTH AT LAST!', 'PENGUINS, HUSKIES AND', 'THE ICE PALACE ITSELF.', 'THIS IS THE BIG ONE!'])
