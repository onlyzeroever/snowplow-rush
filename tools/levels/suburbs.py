"""The 9 new Suburbs jobs, as data levels. Run: python3 suburbs.py -> suburbs.json"""
import json, math

def job(id, **kw):
    d = dict(id=id, ground=[], props=[], hazards=[], circles=[], paint=[], decor=[], neighbours=[], pull=[])
    d.update(kw); return d
def G(d, t, x, y, w, h): d['ground'].append([t, x, y, w, h])
def P(d, k, x, y, a=None): d['props'].append([k, x, y] + ([a] if a is not None else []))
def H(d, k, x, y, *a): d['hazards'].append([k, x, y] + list(a))
def pines(d, pts):
    for x, y, s in pts: P(d, 'pine', x, y, s)

J = {}

# ---------------------------------------------------------------- 7. CORNER SHOP
# Start on the street at the bottom, work up through the car park to the shop. Two customers wait for a
# path to the door (tips), two cars back out of their bays, a runaway trolley rolls round the car park.
d = job('cornershop', start=[90, 572])
G(d, 'grass', 0, 0, 180, 600)
G(d, 'conc', 0, 64, 180, 40)                       # forecourt
G(d, 'asph', 24, 104, 132, 280)                    # car park
G(d, 'conc', 4, 104, 20, 280); G(d, 'conc', 156, 104, 20, 280)   # side pavements
for x in range(26, 160, 26): G(d, 'wht', x, 108, 2, 34); G(d, 'wht', x, 236, 2, 34)   # bay lines, rows 1 and 2
G(d, 'wht', 24, 196, 132, 2)                       # centre line between the two aisles
for k in range(5): G(d, 'yel' if k % 2 else 'wht', 82, 290 + k * 14, 16, 10)   # hatched crossing to the street
G(d, 'conc', 0, 384, 180, 14); G(d, 'asph', 0, 398, 180, 40); G(d, 'conc', 0, 438, 180, 14)
for x in range(4, 180, 16): G(d, 'wht', x, 417, 8, 2)
G(d, 'conc', 78, 452, 24, 148)                     # path down to the start
G(d, 'conc', 20, 518, 12, 30); G(d, 'conc', 148, 518, 12, 30)   # house paths
P(d, 'shop', 62, 0, 0)                             # the corner shop
P(d, 'smallhouse', 4, 0, 1); P(d, 'smallhouse', 132, 0, 3)
P(d, 'crate', 50, 44); P(d, 'crate', 50, 30); P(d, 'trash', 120, 50); P(d, 'trash', 128, 50); P(d, 'kiosk', 120, 64, 2)
P(d, 'phonebox', 150, 70); P(d, 'postbox', 34, 76); P(d, 'lamp', 6, 76); P(d, 'lamp', 168, 76)
# row 1 bays (y108..142): parked cars and two that pull out
P(d, 'car', 28, 110, 1)
d['pull'] += [[53, 110, 2], [131, 110, 0]]
# row 2 bays (y236..270)
P(d, 'car', 54, 238, 3); P(d, 'car', 80, 238, 0); P(d, 'car', 132, 238, 1)
P(d, 'bollard', 12, 150); P(d, 'bollard', 12, 250); P(d, 'bollard', 163, 150); P(d, 'bollard', 163, 250)
P(d, 'planter', 26, 340); P(d, 'planter', 140, 340); P(d, 'trash', 128, 300); P(d, 'trash', 136, 300); P(d, 'trash', 144, 300); P(d, 'trash', 60, 354); P(d, 'cone', 112, 346); P(d, 'cone', 120, 352)
# the street and the houses at the bottom
P(d, 'smallhouse', 4, 470, 2); P(d, 'smallhouse', 132, 470, 4)
P(d, 'hedge', 0, 548, 16); P(d, 'hedge', 50, 548, 22); P(d, 'hedge', 108, 548, 22); P(d, 'hedge', 164, 548, 16)
P(d, 'mailbox', 52, 532); P(d, 'mailbox', 122, 532); P(d, 'snowman', 58, 470); P(d, 'gnome', 116, 476); P(d, 'gnome', 64, 504)
pines(d, [(4, 566, 24), (152, 566, 26), (110, 572, 18)])
H(d, 'cart', 70, 200); H(d, 'thrower', 120, 500)
d['neighbours'] = [
    dict(rects=[[8, 84, 12, 128], [8, 78, 76, 12]], path=[[14, 210], [14, 84], [84, 84]]),
    dict(rects=[[160, 84, 12, 236], [96, 78, 76, 12]], path=[[166, 318], [166, 84], [96, 84]])]
J['cornershop'] = d

# ---------------------------------------------------------------- 8. PLAYGROUND
# A railed playground inside a park loop. Four corners of kit to plow round, kids that throw and kids that run.
d = job('playground', start=[90, 36])
G(d, 'grass', 0, 0, 180, 640)
G(d, 'conc', 78, 0, 24, 560)                       # path through the middle
G(d, 'conc', 4, 104, 172, 16); G(d, 'conc', 4, 104, 26, 470); G(d, 'conc', 150, 104, 26, 470); G(d, 'conc', 4, 560, 172, 14)  # park loop
G(d, 'conc', 41, 302, 98, 36)                     # cross path inside
for k in range(6): G(d, 'yel' if k % 2 else 'wht', 82, 360 + k * 14, 16, 10)   # hopscotch
d['circles'] += [['ice', 90, 606, 26]]             # frozen pond
P(d, 'hedge', 0, 70, 60); P(d, 'hedge', 120, 70, 60); P(d, 'planter', 48, 40); P(d, 'planter', 118, 40)
P(d, 'oak', 10, 10); P(d, 'oak', 148, 14); P(d, 'bench', 20, 40); P(d, 'bench', 144, 46)
# railings with gates top, bottom, left and right
P(d, 'rail', 38, 128, 27); P(d, 'rail', 115, 128, 27)
P(d, 'rail', 38, 532, 27); P(d, 'rail', 115, 532, 27)
P(d, 'railv', 36, 128, 164); P(d, 'railv', 36, 350, 189); P(d, 'railv', 139, 128, 164); P(d, 'railv', 139, 350, 189)
# top-left: swings and a climbing frame; top-right: slide, roundabout, seesaw
P(d, 'swing', 42, 148); P(d, 'swing', 42, 186); P(d, 'climb', 43, 238)
P(d, 'slide', 124, 146); P(d, 'roundabout', 116, 196); P(d, 'seesaw', 108, 262)
# bottom-left: sandpit and benches; bottom-right: climbing frame, swings, slide
P(d, 'sandpit', 42, 360); P(d, 'bench', 44, 420); P(d, 'bench', 46, 470); P(d, 'trash', 44, 500)
P(d, 'climb', 114, 364); P(d, 'swing', 112, 430); P(d, 'slide', 124, 476)
P(d, 'snowman', 46, 286); P(d, 'snowman', 124, 300)
# outside the rails
P(d, 'lamp', 60, 86); P(d, 'lamp', 114, 86)
P(d, 'oak', 2, 590); P(d, 'oak', 156, 588); P(d, 'bench', 50, 600); P(d, 'bench', 118, 600); P(d, 'reed', 64, 590); P(d, 'reed', 112, 620)
pines(d, [(34, 584, 20), (130, 616, 22)])
H(d, 'thrower', 64, 290); H(d, 'thrower', 124, 512); H(d, 'pedx', 40, 316); H(d, 'pedx', 120, 450, 1); H(d, 'ped', 12, 250)
J['playground'] = d

# ---------------------------------------------------------------- 9. ALLOTMENTS
# Rows of raised beds with gaps you can just fit down, sheds and greenhouses at the ends, a dog on the main path.
d = job('allotments', start=[90, 40])
G(d, 'grass', 0, 0, 180, 700)
G(d, 'conc', 74, 0, 32, 700)                        # main path
blocks = ['beds2', 'shed', 'beds4', 'open', 'green', 'beds2']
for side, x0 in (('L', 6), ('R', 110)):
    for k, y0 in enumerate(range(52, 640, 100)):
        kind = blocks[(k + (0 if side == 'L' else 3)) % len(blocks)]
        if kind == 'beds2':
            P(d, 'plot', x0, y0, 64); P(d, 'plot', x0, y0 + 30, 64); P(d, 'barrel', x0 + (58 if side == 'L' else 0), y0 + 50)
        elif kind == 'beds4':
            P(d, 'plot', x0, y0, 26); P(d, 'plot', x0 + 38, y0, 26); P(d, 'plot', x0, y0 + 30, 26); P(d, 'plot', x0 + 38, y0 + 30, 26)
            P(d, 'gnome', x0 + 28, y0 + 14)
        elif kind == 'shed':
            P(d, 'shed', x0 + (0 if side == 'L' else 36), y0 - 8, k % 3); P(d, 'plot', x0 + (34 if side == 'L' else 0), y0 + 4, 30); P(d, 'plot', x0, y0 + 36, 64)
        elif kind == 'green':
            P(d, 'greenhouse', x0 + (2 if side == 'L' else 32), y0 - 4); P(d, 'plot', x0 + (40 if side == 'L' else 0), y0 + 2, 24); P(d, 'plot', x0, y0 + 36, 64)
        elif kind == 'open':
            P(d, 'scarecrow', x0 + 26, y0 + 4); P(d, 'gnome', x0 + 6, y0 + 30); P(d, 'gnome', x0 + 52, y0 + 34); P(d, 'barrel', x0 + 4, y0 + 2); P(d, 'crate', x0 + 48, y0)
for y in (150, 350, 550): P(d, 'lamp', 66, y)
pines(d, [(0, 4, 22), (156, 2, 24), (2, 660, 24), (154, 664, 22)])
H(d, 'dog', 84, 330); H(d, 'thrower', 140, 168); H(d, 'thrower', 34, 470); H(d, 'ped', 96, 560, 1)
J['allotments'] = d

# ---------------------------------------------------------------- 10. DOG PARK
# Start at the gate at the bottom. An agility course, a slalom of poles, a field with four dogs off the lead.
d = job('dogpark', start=[90, 690])
G(d, 'grass', 0, 0, 180, 720)
G(d, 'conc', 76, 600, 28, 120); G(d, 'conc', 6, 600, 168, 16)     # entrance path and a path along the fence
d['circles'] += [['ice', 50, 230, 16], ['ice', 126, 160, 14], ['ice', 140, 300, 12]]
P(d, 'rail', 0, 588, 60); P(d, 'rail', 120, 588, 60)                # fence with the gate
P(d, 'bench', 20, 640); P(d, 'bench', 150, 640); P(d, 'trash', 30, 664); P(d, 'trash', 146, 664); P(d, 'lamp', 54, 650); P(d, 'lamp', 122, 650)
pines(d, [(2, 676, 24), (154, 680, 22)])
# agility course (y 400..580): hurdles in a zigzag and a slalom
for k, (x, y) in enumerate([(70, 450), (110, 490), (70, 530)]): P(d, 'hurdle', x, y)
for k in range(4): P(d, 'pole', 60 + k * 18, 400)
P(d, 'kennel', 160, 430); P(d, 'kennel', 160, 456); P(d, 'kennel', 160, 482)
# the field (y 110..380)
P(d, 'oak', 16, 120); P(d, 'oak', 140, 220); P(d, 'oak', 30, 320); P(d, 'oak', 84, 150); P(d, 'oak', 150, 340); P(d, 'bench', 84, 260); P(d, 'trash', 100, 262)
P(d, 'tub', 100, 330); P(d, 'hedge', 54, 196, 30); P(d, 'hedge', 110, 120, 24)
for x, y in [(126, 452), (122, 532)]: P(d, 'tires', x, y)
P(d, 'hedge', 0, 392, 20); P(d, 'hedge', 160, 392, 20)
# top: the pet shop and the owners' benches
P(d, 'shop', 62, 0, 9); P(d, 'bench', 20, 70); P(d, 'bench', 146, 70); P(d, 'lamp', 4, 40); P(d, 'lamp', 170, 40)
G(d, 'conc', 0, 66, 180, 30)
pines(d, [(4, 0, 22), (150, 0, 24)])
H(d, 'dog', 60, 160); H(d, 'dog', 120, 250); H(d, 'dog', 50, 340); H(d, 'dog', 110, 480)
H(d, 'ped', 10, 200); H(d, 'ped', 166, 300, 1)
J['dogpark'] = d

# ---------------------------------------------------------------- 11. TENNIS CLUB  (new: ball machines)
# Three courts, nets you plow round, lines that appear as you clear. Ball machines fire across the courts.
d = job('tennis', start=[90, 86])
G(d, 'grass', 0, 0, 180, 760)
G(d, 'conc', 0, 58, 180, 44)
P(d, 'big', 35, 0, 8); P(d, 'planter', 10, 64); P(d, 'planter', 156, 64); P(d, 'bench', 28, 88); P(d, 'bench', 140, 88); P(d, 'trash', 60, 90)
pines(d, [(2, 4, 24), (152, 6, 24)])
for k in range(3):
    y0 = 110 + k * 212
    G(d, 'asph', 16, y0, 148, 200)
    G(d, 'wht', 24, y0 + 6, 132, 2); G(d, 'wht', 24, y0 + 192, 132, 2); G(d, 'wht', 24, y0 + 6, 2, 188); G(d, 'wht', 154, y0 + 6, 2, 188)
    G(d, 'wht', 40, y0 + 6, 2, 188); G(d, 'wht', 138, y0 + 6, 2, 188)
    G(d, 'wht', 40, y0 + 52, 100, 2); G(d, 'wht', 40, y0 + 146, 100, 2); G(d, 'wht', 89, y0 + 52, 2, 96)
    P(d, 'net', 50, y0 + 96, 80)
    if k < 2: P(d, 'rail', 14, y0 + 203, 46); P(d, 'rail', 120, y0 + 203, 46)
    P(d, 'bench', 2, y0 + 92); P(d, 'bench', 166, y0 + 92)
H(d, 'balls', 165, 110 + 40, -1, 3.0)
H(d, 'balls', 3, 322 + 150, 1, 2.8)
H(d, 'balls', 165, 534 + 36, -1, 2.6); H(d, 'balls', 3, 534 + 156, 1, 2.6)
J['tennis'] = d

# ---------------------------------------------------------------- 12. HIGH STREET
# Shops both sides, a bus running down the street, shoppers on the pavements and at the crossings.
d = job('highst', start=[90, 36])
G(d, 'conc', 0, 0, 180, 820)
G(d, 'asph', 56, 0, 68, 820)
for y in range(8, 820, 24): G(d, 'wht', 89, y, 2, 12)
for yz in (250, 560):
    for k in range(8): G(d, 'wht', 58 + k * 8, yz, 5, 24)
left = [2, 10, None, 1, 6, 11, None, 4, 5, 12, 7]
right = [3, 13, 9, None, 14, 7, 2, None, 6, 15, 1]
for side, x, seq in (('L', 0, left), ('R', 136, right)):
    y = 0
    for a in seq:
        if a is None:
            P(d, 'trash', x + 4, y + 2); P(d, 'trash', x + 33, y + 2); y += 30; continue
        P(d, 'shopv', x, y, a); y += 74
for y in range(60, 820, 120): P(d, 'lamp', 46, y); P(d, 'lamp', 128, y + 60)
for y in (180, 480, 740): P(d, 'bollard', 50, y); P(d, 'bollard', 126, y + 30)
P(d, 'postbox', 46, 330); P(d, 'phonebox', 126, 410); P(d, 'bench', 44, 640); P(d, 'planter', 124, 120); P(d, 'planter', 124, 700)
P(d, 'car', 100, 140, 2); P(d, 'car', 100, 440, 4); d['pull'] += [[99, 300, 1], [99, 650, 3]]
for y in (120, 420, 720): d['decor'].append(['bunting', 44, y, 92])
H(d, 'taxi', 60, -60, 2)
H(d, 'ped', 47, 100); H(d, 'ped', 127, 260, 1); H(d, 'ped', 47, 600, 1); H(d, 'ped', 127, 700)
H(d, 'pedx', 64, 258); H(d, 'pedx', 110, 570, 1)
J['highst'] = d

# ---------------------------------------------------------------- 13. SLEDGING HILL  (side job; new: snow cannons)
# Sledgers fly across, two snow cannons blow fresh snow back over the slope. Jam them by plowing into them.
d = job('sledhill', start=[90, 672])
G(d, 'grass', 0, 0, 180, 700)
G(d, 'conc', 60, 630, 60, 70)
P(d, 'stall', 4, 640, 0); P(d, 'kiosk', 156, 646, 1); P(d, 'bench', 40, 610); P(d, 'bench', 124, 610); P(d, 'lamp', 40, 650); P(d, 'lamp', 134, 650)
pines(d, [(2, 600, 26), (156, 596, 24), (0, 420, 22), (158, 300, 24), (4, 180, 26), (156, 120, 22), (60, 60, 20), (110, 40, 24)])
for x, y in [(40, 540), (130, 500), (70, 380), (120, 260), (36, 200), (90, 120)]: P(d, 'snowman', x, y)
for x, y in [(20, 470), (150, 400), (84, 300), (24, 300), (140, 180)]: P(d, 'hay', x, y)
P(d, 'oak', 80, 8); P(d, 'bench', 40, 30); P(d, 'bench', 126, 30)
pines(d, [(50, 450, 18), (62, 458, 22), (118, 340, 20), (130, 330, 16), (40, 250, 20), (100, 200, 18), (112, 196, 22)])
for x, y, h in [(30, 330, 90), (146, 470, 80), (96, 420, 60), (70, 140, 70)]: G(d, 'ice', x, y, 10, h)
P(d, 'fence', 0, 540, 50); P(d, 'fence', 168, 530, 60)
H(d, 'cannon', 2, 236, 0.35, 6.5, 70); H(d, 'cannon', 160, 420, math.pi - 0.35, 6.5, 70)
H(d, 'sled', 0, 0, [3, 5]); H(d, 'thrower', 140, 560); H(d, 'thrower', 40, 120)
J['sledhill'] = d

# ---------------------------------------------------------------- 14. FOUNTAIN SQUARE
# A big paved square with rings round a frozen fountain, café tables, a market, and people everywhere.
d = job('fountainsq', start=[90, 40])
G(d, 'conc', 0, 0, 180, 860)
G(d, 'asph', 0, 60, 180, 36)
for k in range(8): G(d, 'wht', 58 + k * 8, 66, 5, 24)
cx, cy = 90, 430
d['circles'] += [['yel', cx, cy, 72], ['conc', cx, cy, 68], ['wht', cx, cy, 48], ['conc', cx, cy, 46], ['ice', cx, cy, 26]]
G(d, 'asph', 0, 790, 180, 36)
for x in range(4, 180, 16): G(d, 'wht', x, 807, 8, 2)
P(d, 'shop', 4, 0, 2); P(d, 'shop', 120, 0, 1)
P(d, 'fountain', cx - 12, cy - 12)
for a in range(4):
    ang = math.pi / 4 + a * math.pi / 2; P(d, 'statue', round(cx + math.cos(ang) * 58) - 4, round(cy + math.sin(ang) * 58) - 8)
for a in range(8):
    if a % 2 == 0: ang = a * math.pi / 4; P(d, 'lamp', round(cx + math.cos(ang) * 84) - 3, round(cy + math.sin(ang) * 84) - 20)
for x, y in [(20, 120), (140, 120), (20, 728), (140, 728)]: P(d, 'planter', x, y)
# café terrace
for k, (x, y) in enumerate([(8, 150), (40, 150), (114, 150), (148, 150), (24, 190), (130, 190)]): P(d, 'table', x, y, k % 4)
P(d, 'kiosk', 150, 214, 3); P(d, 'phonebox', 4, 250); P(d, 'postbox', 168, 256)
for y in (330, 530): P(d, 'bench', 6, y); P(d, 'bench', 162, y)
# market rows
for k in range(3): P(d, 'stall', 4 + k * 71, 610, k); P(d, 'stall', 4 + k * 71, 680, k + 2)
P(d, 'oak', 6, 744); P(d, 'oak', 152, 744); P(d, 'bench', 40, 760); P(d, 'bench', 124, 760)
H(d, 'ped', 30, 300); H(d, 'ped', 150, 520, 1); H(d, 'pedx', 30, 580); H(d, 'pedx', 130, 760, 1); H(d, 'pedx', 60, 236, 1)
H(d, 'thrower', 160, 380); H(d, 'thrower', 20, 470); H(d, 'dog', 100, 300)
J['fountainsq'] = d

# ---------------------------------------------------------------- 15. BLOCK PARTY  (boss)
# The whole street is out, and Mrs. Grimshaw is NOT happy about it: she hunts you all job. Party tables to slalom,
# a stage with a snow machine, dodgeball machines, food stalls, cars leaving and a granny who wants a path to the fun.
# A 48px+ lane runs the full street so every machine (up to the Super Plow and Wild Rides) gets through.
d = job('blockparty', start=[90, 36])
G(d, 'grass', 0, 0, 180, 1000)
G(d, 'asph', 50, 0, 80, 1000); G(d, 'conc', 38, 0, 12, 1000); G(d, 'conc', 130, 0, 12, 1000)
for y in range(10, 1000, 30): G(d, 'wht', 89, y, 2, 14)
for y in range(140, 1000, 160): d['decor'].append(['bunting', 40, y, 100])
def barrier(y):
    for x in (52, 62, 118, 128): P(d, 'cone', x, y)
# 1: the closed road
barrier(70); P(d, 'smallhouse', 0, 0, 0); P(d, 'smallhouse', 138, 0, 2); P(d, 'barrel', 40, 64); P(d, 'barrel', 134, 64)
# 2: party tables, one per row, alternating sides: a slalom
for r, y in enumerate(range(170, 400, 44)): P(d, 'table', 52 if r % 2 == 0 else 102, y, r % 4)
P(d, 'smallhouse', 0, 170, 3); P(d, 'smallhouse', 138, 230, 4); P(d, 'smallhouse', 0, 330, 1)
H(d, 'thrower', 150, 330); H(d, 'pedx', 60, 236); H(d, 'pedx', 110, 320, 1)
# 3: the stage on the left, its snow machine on the right
P(d, 'stage', 4, 432); P(d, 'speaker', 86, 436)
H(d, 'cannon', 150, 482, math.pi * 0.72, 7.0, 64)
H(d, 'pedx', 70, 500); H(d, 'pedx', 110, 520, 1)
P(d, 'smallhouse', 0, 500, 2); pines(d, [(160, 526, 18)])
# 4: food stalls, BBQs and the dodgeball machines
P(d, 'stall', 36, 560, 0); P(d, 'stall', 114, 560, 3); P(d, 'bbq', 44, 612); P(d, 'bbq', 126, 612)
H(d, 'balls', 124, 652, -1, 2.6); H(d, 'balls', 40, 720, 1, 2.6)
P(d, 'hay', 60, 684); P(d, 'hay', 108, 694); P(d, 'table', 100, 750, 2)
P(d, 'smallhouse', 138, 600, 0); P(d, 'smallhouse', 0, 650, 4)
# 5: houses, cars leaving, a granny, another snow machine, the far barrier
P(d, 'smallhouse', 0, 820, 3); P(d, 'smallhouse', 138, 860, 1)
d['pull'] += [[104, 800, 1], [56, 900, 4]]
H(d, 'dog', 90, 860); H(d, 'cannon', 152, 940, math.pi * 0.85, 7.0, 60)
d['neighbours'] = [dict(rects=[[16, 868, 78, 14]], path=[[22, 868], [50, 875], [90, 875]])]
barrier(980); P(d, 'snowman', 84, 940)
pines(d, [(150, 760, 22), (4, 940, 24)])
# Mrs. Grimshaw comes out of her house after 6 seconds
H(d, 'chaser', 152, 284, 'grimshaw', 6)
J['blockparty'] = d

META = {'cornershop': (600, 70, 1.65, 5), 'playground': (640, 70, 1.7, 5), 'allotments': (700, 75, 1.75, 5), 'dogpark': (720, 80, 1.8, 6),
        'tennis': (760, 75, 1.85, 6), 'highst': (820, 62, 1.9, 6), 'sledhill': (700, 74, 1.9, 7), 'fountainsq': (860, 84, 1.95, 6), 'blockparty': (1000, 90, 2.0, 8)}
for k, v in J.items():
    h, t, val, pr = META[k]; v.update(h=h, time=t, value=val, presents=pr, stars=v.get('stars', [35, 60, 85]), area='suburbs', name=k.upper())
    for f in ('circles', 'paint', 'decor', 'neighbours', 'pull'):
        if not v[f]: v.pop(f)
json.dump(J, open('/home/claude/levels/suburbs.json', 'w'))
print('jobs', list(J))
