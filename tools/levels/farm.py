"""Farmland part 2: 9 new jobs (7 main, 1 side, 1 boss), played mostly with the tractor.
New mechanics: sheep flocks that scatter from the plow (Sheep Fields), farm traffic that crosses a lane after a
warning (Windmill Hill). Boss: the Harvest Fair, with the Goose hunting you.  Run: python3 farm.py -> farm.json"""
import random
from common import *

J = []

# ---------------------------------------------------------------- all nine jobs: pro pass in farm_pro.py
import farm_pro
for f in farm_pro.ALL: J.append(f())

# ---------------------------------------------------------------- map: the Farmland part 2 band (6062-6622)
POS = {'milkshed': [40, 6584], 'treefarm': [140, 6532], 'sheepfields': [44, 6470], 'stables': [140, 6414], 'farmcafe': [52, 6352],
       'windmill': [138, 6296], 'maze': [26, 6224], 'mill': [130, 6222], 'harvestfair': [86, 6130]}
LM = {k: [v[0] + (14 if v[0] < 90 else -14), v[1] - 22] for k, v in POS.items()}
finish(J, '/home/claude/levels/farm.json', mappos=POS, landmark=LM, relink={'shops': ['harvestfair']},
       edgevia={'harvestfair>shops': [[90, 6090], [92, 6040]]}, bossStars={'harvestfair': 25})
