"""Shared helpers for writing data jobs. Rules every job must pass (checked by subcheck.js with all 11 machines):
kid tools reach >=97%, every other machine >=90%; start >=36px from the top/bottom edge with room to turn;
main lanes >=48px wide; no hazard closer than ~60px to the start."""
import json, math, random

def job(id, name, area, frm, h, time, value, presents=6, start=None, **kw):
    d = dict(id=id, name=name, area=area, **{'from': frm}, h=h, time=time, value=value, presents=presents,
             stars=kw.pop('stars', [35, 60, 85]), snowfall=kw.pop('snowfall', 120), squall=kw.pop('squall', 0))
    d.update(kw)
    d['data'] = dict(ground=[], props=[], hazards=[], circles=[], paint=[], decor=[], neighbours=[], pull=[],
                     start=start or [90, h - 40])
    return d
def G(d, t, x, y, w, h): d['data']['ground'].append([t, x, y, w, h])
def C(d, t, cx, cy, r): d['data']['circles'].append([t, cx, cy, r])
def P(d, k, x, y, a=None): d['data']['props'].append([k, x, y] + ([a] if a is not None else []))
def H(d, k, x, y, *a): d['data']['hazards'].append([k, x, y] + list(a))
def pines(d, pts):
    for x, y, s in pts: P(d, 'pine', x, y, s)
def field(d, x, y, w, h, step=6):
    """a ploughed field: dirt with rows of winter grass, revealed in stripes"""
    G(d, 'dirt', x, y, w, h)
    for yy in range(y + 2, y + h - 1, step): G(d, 'grass', x, yy, w, 2)
def wallbox(d, x0, y0, x1, y1, gaps, kind='stonewall'):
    """rectangle of walls; gaps = list of (side, a, b) with side in 'tblr' and a..b the open span"""
    th = 8 if kind == 'stonewall' else 7 if kind == 'rail' else 10
    hk, vk = (kind, kind + 'v') if kind != 'hedge' else ('hedge', 'hedgev')
    def run(side, a0, a1):
        cuts = sorted([(a, b) for s, a, b in gaps if s == side])
        cur = a0
        for a, b in cuts + [(a1, a1)]:
            if a > cur:
                if side in 'tb': P(d, hk, cur, y0 if side == 't' else y1 - th, a - cur)
                else: P(d, vk, x0 if side == 'l' else x1 - (5 if kind == 'rail' else th), cur, a - cur)
            cur = max(cur, b)
    run('t', x0, x1); run('b', x0, x1); run('l', y0 + th, y1 - th); run('r', y0 + th, y1 - th)
def finish(jobs, path, **extra):
    for j in jobs:
        dd = j['data']
        for f in ('circles', 'paint', 'decor', 'neighbours', 'pull'):
            if not dd[f]: dd.pop(f)
    import os
    tf = path + '.times.json'
    if os.path.exists(tf):
        T = json.load(open(tf))
        for j in jobs:
            if j['id'] in T: j['time'] = T[j['id']]
    df = path + '.drops.json'
    if os.path.exists(df):
        DR = json.load(open(df))
        for j in jobs:
            gone = [(k, x, y) for i, k, x, y in DR if i == j['id']]
            if gone: j['data']['props'] = [p for p in j['data']['props'] if (p[0], p[1], p[2]) not in gone]
    out = dict(jobs=jobs, **extra)
    json.dump(out, open(path, 'w'))
    print('wrote', path, [j['id'] for j in jobs])

# ================================ PRO KIT helpers (p56_prokit) ================================
# grounds: grass asph conc yel wht ice dirt wood red + cobble pave tile slab blue green gravel piste stone orange purple mosaic deck sand
def _l(d, k):
    dd = d['data']; dd.setdefault(k, []); return dd[k]
def dec(d, kind, x, y, a=None, b=None):
    e = [kind, int(x), int(y)]
    if a is not None or b is not None: e += [a if a is not None else 0]
    if b is not None: e += [b]
    _l(d, 'decals').append(e)
def scen(d, kind, x, y, a=None, noblock=False):
    e = [kind, int(x), int(y)] + ([a] if a is not None or noblock else [])
    if noblock: e += [1]
    _l(d, 'scen').append(e)
def over(d, kind, x, y, a=None, b=None):
    e = [kind, int(x), int(y)] + ([a] if a is not None else []) + ([b] if b is not None else []); _l(d, 'over').append(e)
def wild(d, kind, x, y, w, h, seed=1, dens=0.75, step=9):
    _l(d, 'wilds').append([kind, int(x), int(y), int(w), int(h), seed, dens, step])
def carve(d, w, pts):
    _l(d, 'carves').append([w] + [int(v) for p in pts for v in p])
def clear(d, x, y, w, h, t=None):
    """a rectangular clearing in a wild area (wild cells inside it are open ground)"""
    _l(d, 'clears').append([int(x), int(y), int(w), int(h)])
    if t: G(d, t, x, y, w, h)
def path(d, t, w, pts):
    _l(d, 'paths').append([t, w] + [int(v) for p in pts for v in p])
def rng(seed): return random.Random(seed)
def street_v(d, x, w, y0, y1, centre='dash', ground='asph', kerbs=True):
    """a road running up the screen: kerbstones at both sides, centre markings"""
    G(d, ground, x, y0, w, y1 - y0)
    if kerbs: dec(d, 'kerb', x - 2, y0, y1 - y0); dec(d, 'kerb', x + w, y0, y1 - y0)
    if centre == 'dash': dec(d, 'dashv', x + w // 2 - 1, y0 + 4, y1 - y0 - 8)
    elif centre == 'dyl': dec(d, 'dyl', x + w // 2 - 2, y0, y1 - y0)
def street_h(d, y, h, x0=0, x1=180, centre='dash', ground='asph', kerbs=True, zebras=None):
    G(d, ground, x0, y, x1 - x0, h)
    if kerbs: dec(d, 'kerbh', x0, y - 2, x1 - x0); dec(d, 'kerbh', x0, y + h, x1 - x0)
    if centre == 'dash': dec(d, 'dashh', x0 + 4, y + h // 2 - 1, x1 - x0 - 8)
    elif centre == 'dyl': dec(d, 'dylh', x0, y + h // 2 - 2, x1 - x0)
    for zx, zw in (zebras or []): dec(d, 'zebrah', zx, y + 2, zw, h - 4)
def furniture_line(d, x, y0, y1, seed, kinds, gap=(34, 60), jitter=3):
    """street furniture down a pavement at irregular spacing (never a fixed step)"""
    r = rng(seed); y = y0 + r.randint(0, gap[0] // 2)
    while y < y1:
        k = r.choice(kinds)
        if isinstance(k, tuple): P(d, k[0], x + r.randint(-jitter, jitter), y, k[1])
        else: P(d, k, x + r.randint(-jitter, jitter), y)
        y += r.randint(*gap)
def trees_line(d, x, y0, y1, seed, gap=(46, 74), size=(22, 30), grate=True, scenery=False):
    r = rng(seed); y = y0 + r.randint(0, 20)
    while y < y1:
        s = r.randint(*size); tx = x - (round(s * 0.9) >> 1)
        if grate: dec(d, 'grate', x - 8, y + s - 12)
        (scen if scenery else P)(d, 'stree', tx, y, s)
        y += r.randint(*gap)
def scatter(d, kinds, rect, n, seed, minsep=18, scenery=False):
    """n props at random inside rect (x,y,w,h) keeping minsep apart"""
    r = rng(seed); x0, y0, w, h = rect; pts = []
    for _ in range(n * 30):
        if len(pts) >= n: break
        x, y = x0 + r.random() * w, y0 + r.random() * h
        if all((x - a) ** 2 + (y - b) ** 2 >= minsep * minsep for a, b in pts):
            pts.append((x, y)); k = r.choice(kinds)
            if isinstance(k, tuple): (scen if scenery else P)(d, k[0], int(x), int(y), k[1])
            else: (scen if scenery else P)(d, k, int(x), int(y))
    return pts
def facade_row(d, side, y0, y1, seed, kinds=(('shopv', None),), x=None, gap=(0, 0)):
    """a row of building fronts down one edge as blocking scenery; returns the gaps left between them"""
    r = rng(seed); y = y0; gaps = []
    W = {'shop': (56, 60), 'shopv': (44, 72), 'tower': (50, 96), 'towerw': (70, 80), 'big': (110, 58), 'house': (40, 40)}
    while y < y1:
        k, a = r.choice(kinds); w, h = W.get(k, (44, 72))
        if y + h > y1: break
        xx = x if x is not None else (0 if side == 'l' else 180 - w)
        scen(d, k, xx, y, a if a is not None else r.randint(0, 9)); y += h
        g = r.randint(*gap)
        if g: gaps.append((y, y + g)); y += g
    return gaps

# ================================ AUTO-DRESS: fill bare edges with area-appropriate clutter ================================
_FEET = None
def _feet():
    global _FEET
    if _FEET is None: _FEET = json.load(open('/home/claude/levels/feet.json'))
    return _FEET
def occupancy(d, pad=6):
    """coarse 4px occupancy grid from props, scenery and wild areas"""
    dd = d['data']; h = d['h']; W, H = 45, h // 4 + 1; occ = bytearray(W * H)
    def mark(x0, y0, x1, y1):
        for yy in range(max(0, int(y0) // 4), min(H, int(y1) // 4 + 1)):
            for xx in range(max(0, int(x0) // 4), min(W, int(x1) // 4 + 1)): occ[yy * W + xx] = 1
    F = _feet()
    for p in dd.get('props', []) + dd.get('scen', []):
        f = F.get(p[0])
        if not f: continue
        ft = f['foot']; a = p[3] if len(p) > 3 else None
        if a is not None and p[0] in ('rail', 'stonewall', 'hedge', 'wall', 'works', 'planterl', 'stand', 'crowd', 'container', 'plot', 'icewall', 'coaster'):
            ft = [ft[0], ft[1], a, ft[3]]
        if a is not None and p[0] in ('railv', 'stonewallv', 'hedgev', 'fence', 'wallv', 'icewallv', 'coasterv', 'track', 'train'):
            ft = [ft[0], ft[1], ft[2], a]
        mark(p[1] + ft[0] - pad, p[2] - pad, p[1] + ft[0] + ft[2] + pad, p[2] + ft[1] + ft[3] + pad)
    for w in dd.get('wilds', []): mark(w[1] - pad, w[2] - pad, w[1] + w[3] + pad, w[2] + w[4] + pad)
    for hz in dd.get('hazards', []):
        if hz[0] in ('cross',): mark(0, hz[2] - 20, 180, hz[2] + 30)
    for c in dd.get('carves', []): pass
    return occ, W, H
def autodress(d, palette, seed, edge=34, chance=0.55, keep_y=(60, None), avoid=('ice',), rows=64):
    """drop small clusters of palette props flush to the left/right edges wherever an edge band is bare"""
    r = rng(seed); occ, W, H = occupancy(d); F = _feet(); h = d['h']
    y1 = keep_y[1] if keep_y[1] is not None else h - 60
    bad = [g for g in d['data']['ground'] if g[0] in avoid]
    def ground_bad(x, y): return any(g[1] <= x < g[1] + g[3] and g[2] <= y < g[2] + g[4] for g in bad)
    added = 0
    for y in range(keep_y[0], y1, rows):
        for side in ('l', 'r'):
            if r.random() > chance: continue
            k = r.choice(palette); kind, arg = (k if isinstance(k, tuple) else (k, None))
            f = F.get(kind)
            if not f: continue
            fw, fh = f['w'], f['h']; x = 2 if side == 'l' else 178 - fw; yy = y + r.randint(0, rows - fh - 4) if rows > fh + 6 else y
            if x < 0 or fw > edge + 12: continue
            cells = [(cx, cy) for cy in range(max(0, yy // 4), min(H, (yy + fh) // 4 + 1)) for cx in range(max(0, x // 4), min(W, (x + fw) // 4 + 1))]
            if any(occ[cy * W + cx] for cx, cy in cells) or ground_bad(x + fw // 2, yy + fh // 2): continue
            P(d, kind, x, yy, arg) if arg is not None else P(d, kind, x, yy)
            for cx, cy in cells: occ[cy * W + cx] = 1
            added += 1
    return added


# ================================ vertical stretch (longer late-game jobs, same layout) ================================
_VLEN_PROPS = ('railv', 'snowfencev', 'icewallv', 'rocknet', 'carpet', 'stonewallv', 'hedgev', 'wallv', 'track', 'coasterv', 'containerv', 'fence')
_VLEN_DECALS = ('kerb', 'dashv', 'edge', 'dyl', 'rails')
def stretch(d, s):
    """stretch a job vertically by s: positions, lengths along y and ground heights scale; sizes across stay, so every
    gap is at least as wide as before (fit is never worse)"""
    if s == 1: return d
    Y = lambda v: int(round(v * s))
    h0 = d['h']; d['h'] = Y(h0); dd = d['data']
    sx, sy = d['start'] if 'start' in d else dd.get('start', [90, 40])
    ny = d['h'] - (h0 - sy) if sy > h0 / 2 else sy
    if 'start' in d: d['start'] = [sx, ny]
    if 'start' in dd: dd['start'] = [sx, ny]
    for g in dd.get('ground', []): y0, y1 = Y(g[2]), Y(g[2] + g[4]); g[2] = y0; g[4] = max(1, y1 - y0)
    for c in dd.get('circles', []): c[2] = Y(c[2])
    for p in dd.get('props', []) + dd.get('scen', []):
        p[2] = Y(p[2])
        if p[0] in _VLEN_PROPS and len(p) > 3 and isinstance(p[3], (int, float)): p[3] = Y(p[3])
    for e in dd.get('decals', []):
        e[2] = Y(e[2])
        if e[0] in _VLEN_DECALS and len(e) > 3: e[3] = Y(e[3])
        if e[0] == 'hatch' and len(e) > 4: e[4] = Y(e[4])
    for o in dd.get('over', []):
        o[2] = Y(o[2])
        if o[0] in ('liftline', 'gondola') and len(o) > 3: o[3] = Y(o[3])
        if o[0] in ('shed', 'tunnel') and len(o) > 4: o[4] = Y(o[4])
    for w in dd.get('wilds', []): w[2] = Y(w[2]); w[4] = Y(w[4])
    for c in dd.get('clears', []): c[1] = Y(c[1]); c[3] = Y(c[3])
    for c in dd.get('carves', []):
        for i in range(2, len(c), 2): c[i] = Y(c[i])
    for p in dd.get('paths', []):
        for i in range(3, len(p), 2): p[i] = Y(p[i])
    for e in dd.get('decor', []): e[2] = Y(e[2])
    for e in dd.get('pull', []): e[1] = Y(e[1])
    for hz in dd.get('hazards', []):
        k = hz[0]; hz[2] = Y(hz[2])
        if k == 'taxi' and len(hz) > 5: hz[4] = Y(hz[4]); hz[5] = Y(hz[5])
        if k in ('skier', 'rockfall') and len(hz) > 4 and isinstance(hz[4], list):
            ln = hz[4]
            for i in range(1, len(ln), 2): ln[i] = Y(ln[i])
    return d
