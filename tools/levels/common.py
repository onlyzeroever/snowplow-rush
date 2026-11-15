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
    out = dict(jobs=jobs, **extra)
    json.dump(out, open(path, 'w'))
    print('wrote', path, [j['id'] for j in jobs])
