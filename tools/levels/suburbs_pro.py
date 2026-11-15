"""Suburbs, pro pass: the nine new Suburbs jobs keep their layouts and mechanics (Alex liked them), and get the new
standard of finish: real paving and paths to uncover, road markings, front gardens and hedges, street trees,
bins and bikes, ice puddles, lights and bunting overhead. Applied on top of suburbs.py's J."""
import math
from common import dec, scen, over, wild, carve, path, rng

def W(d): return {'data': d}
def G(d, t, x, y, w, h): d['ground'].append([t, x, y, w, h])
def C(d, t, x, y, r): d.setdefault('circles', []).append([t, x, y, r])
def P(d, k, x, y, a=None): d['props'].append([k, x, y] + ([a] if a is not None else []))
def H(d, k, x, y, *a): d['hazards'].append([k, x, y] + list(a))
def regrnd(d, old, new, region=None):
    """swap a ground finish for another (optionally only inside a y-range)"""
    for g in d['ground']:
        if g[0] == old and (region is None or (g[2] >= region[0] and g[2] + g[4] <= region[1])): g[0] = new


def cornershop(d):
    w = W(d)
    regrnd(d, 'conc', 'pave', (60, 110)); regrnd(d, 'conc', 'slab', (100, 390))
    for x in (40, 140): dec(w, 'manhole', x, 200)
    dec(w, 'oil', 70, 160, 6, 4); dec(w, 'oil', 120, 280, 5, 9); dec(w, 'arrow', 120, 150, 0); dec(w, 'arrow', 60, 300, 1)
    dec(w, 'kerbh', 0, 396, 180); dec(w, 'kerbh', 0, 438, 180); dec(w, 'drain', 20, 432); dec(w, 'drain', 150, 400)
    regrnd(d, 'conc', 'pave', (450, 600))
    P(d, 'news', 98, 60); P(d, 'bins', 156, 96); dec(w, 'puddle', 30, 360, 7); dec(w, 'puddle', 150, 330, 6)
    over(w, 'lights', 0, 52, 180, 1)
    for x in (26, 130): wild(w, 'bush', x - 20, 510, 16, 16, x, 0.9, 7)


def playground(d):
    w = W(d)
    regrnd(d, 'conc', 'gravel', (0, 600))
    G(d, 'blue', 40, 140, 26, 80); G(d, 'green', 112, 140, 30, 150); G(d, 'orange', 40, 352, 30, 40); G(d, 'purple', 108, 356, 32, 150)
    dec(w, 'hop', 79, 356)
    over(w, 'lights', 0, 300, 180, 2)
    P(d, 'bins', 162, 2)


def allotments(d):
    w = W(d)
    regrnd(d, 'conc', 'gravel')
    for y in (90, 290, 490): dec(w, 'puddle', 84, y, 6)
    P(d, 'signpost', 106, 8); P(d, 'barrel', 100, 640); P(d, 'barrel', 108, 640)
    over(w, 'bunting', 0, 0, 180) if False else None


def dogpark(d):
    w = W(d)
    regrnd(d, 'conc', 'gravel')
    G(d, 'green', 54, 392, 72, 190)
    for x, y in ((40, 600), (140, 600)): dec(w, 'manhole', x, y)
    P(d, 'trash', 4, 560); P(d, 'trash', 170, 560); P(d, 'signpost', 140, 620)
    for x in (0, 164): wild(w, 'park', x, 100, 16, 280, x + 3, 0.7, 10)


def tennis(d):
    w = W(d)
    for k in range(3):
        y0 = 110 + k * 212
        for g in d['ground']:
            if g[0] == 'asph' and g[2] == y0: g[0] = 'green' if k % 2 else 'blue'
        G(d, 'orange', 16, y0, 148, 6); G(d, 'orange', 16, y0 + 194, 148, 6)
    regrnd(d, 'conc', 'slab')
    over(w, 'lights', 0, 56, 180, 0)


def highst(d):
    w = W(d)
    regrnd(d, 'conc', 'slab')
    d['ground'] = [g for g in d['ground'] if not (g[0] == 'wht' and g[1] == 89)]
    d['ground'] = [g for g in d['ground'] if not (g[0] == 'wht' and g[3] == 5 and g[4] == 24)]
    dec(w, 'dashv', 89, 4, 812); dec(w, 'kerb', 54, 0, 820); dec(w, 'kerb', 124, 0, 820)
    for yz in (250, 560): dec(w, 'zebra', 56, yz, 68, 24); dec(w, 'tactile', 44, yz + 6); dec(w, 'tactile', 126, yz + 6)
    for y in (100, 400, 700): dec(w, 'manhole', 70, y); dec(w, 'manhole', 104, y + 140)
    for y in (60, 360, 660): dec(w, 'arrow', 64, y, 1); dec(w, 'arrow', 110, y + 80, 0)
    d['decor'] = []
    for y in (120, 420, 720): over(w, 'lights', 44, y, 92, y % 5)
    for y in (200, 520): dec(w, 'grate', 42, y + 14); P(d, 'stree', 39, y - 8, 22)


def sledhill(d):
    w = W(d)
    regrnd(d, 'conc', 'pave')
    for x in (0, 166): wild(w, 'forest', x, 20, 14, 560, x + 11, 0.85, 9)
    dec(w, 'puddle', 90, 560, 8)
    over(w, 'lights', 40, 600, 100, 3)
    d['props'].append(['parasol', 26, 660, 0])


def fountainsq(d):
    w = W(d)
    regrnd(d, 'conc', 'slab')
    d['ground'] = [g for g in d['ground'] if not (g[0] == 'wht' and g[2] == 66 and g[4] == 24)]
    dec(w, 'zebra', 58, 64, 64, 30); dec(w, 'dashh', 4, 77, 172); dec(w, 'kerbh', 0, 58, 180); dec(w, 'kerbh', 0, 96, 180)
    d['circles'] = [['pave', 90, 430, 76]] + d['circles']
    for c in d['circles']:
        if c[0] == 'yel': c[0] = 'cobble'
        elif c[0] == 'wht': c[0] = 'mosaic'
    for y in (300, 560): over(w, 'lights', 0, y, 180, y % 4)
    for x, y in ((30, 350), (150, 520)): dec(w, 'manhole', x, y)


def blockparty(d):
    w = W(d)
    d['ground'] = [g for g in d['ground'] if not (g[0] == 'wht' and g[1] == 89)]
    dec(w, 'dashv', 89, 6, 988); dec(w, 'kerb', 48, 0, 1000); dec(w, 'kerb', 130, 0, 1000)
    regrnd(d, 'conc', 'slab')
    for y in (100, 400, 700): dec(w, 'manhole', 64, y); dec(w, 'drain', 52, y + 120)
    d['decor'] = []
    for y in range(140, 1000, 160): over(w, 'lights' if (y // 160) % 2 else 'banner', 40, y, 100, 0)
    for k, y in enumerate((200, 340, 640, 900)): dec(w, 'starm', 70 if k % 2 else 104, y, 6)
    for i, p in enumerate(d['props']):
        if p[0] == 'stage': p.append(0)
    # the party-table slalom: every other row, set closer to the kerbs, so big machines can weave it too
    d['props'] = [p for p in d['props'] if not (p[0] == 'table' and 170 <= p[2] < 400)]
    for r, y in enumerate((170, 262, 354)): P(d, 'table', 50 if r % 2 == 0 else 104, y, r % 4)


UPLIFT = dict(cornershop=cornershop, playground=playground, allotments=allotments, dogpark=dogpark, tennis=tennis,
              highst=highst, sledhill=sledhill, fountainsq=fountainsq, blockparty=blockparty)
def apply(J):
    for k, f in UPLIFT.items():
        if k in J: f(J[k])
