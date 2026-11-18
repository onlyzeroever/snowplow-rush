"""Ladder v3: Front Loader (after the Super Plow) + Icebreaker (North finale), on sim v10 (real combos, Mk II).
Machine upgrade caps are an explicit table so the Snowcat and Rotary keep exactly today's caps and upgrade prices;
only the Super Plow changes (its caps now point at the Loader, like the early machines)."""
import econ11 as e, copy, statistics as st, json, math
GAME_TOOLS = json.load(open('/home/claude/sim/tools.json'))
# combo per machine, from real job_end data (Nov 2026): early machines ~2.2-2.5 (few props), Plow Truck 1.56, Super 1.8.
# Later machines have no data yet: assume 1.7.
COMBO = dict(shovel=2.2, pusher=2.2, blower=2.3, tractor=2.0, truck=1.6, super=1.8, loader=1.7, snowcat=1.7, rotary=1.7, icebreaker=1.7)
L = 6
def build(loader=None, ice=None):
    base = [dict(t) for t in GAME_TOOLS if not t.get('winter')]
    rides = [dict(t) for t in GAME_TOOLS if t.get('winter')]
    if loader: base.insert([t['id'] for t in base].index('super') + 1, dict(loader, id='loader'))
    if ice: base.append(dict(ice, id='icebreaker'))
    return base, rides
def specs(cfg, base, rides, caps):
    spec = {}; ids = [t['id'] for t in base]
    cost = {t['id']: t['cost'] for t in base}
    for i, t in enumerate(base):
        n = base[i + 1] if i + 1 < len(base) else None
        if t['id'] in caps: scap, wcap, nxt = caps[t['id']]
        elif t['id'] == 'super' and (not n or n['id'] == 'snowcat'): scap, wcap, nxt = 1.15, 1.3, n['cost']   # today
        elif i < 6 or t['id'] == 'super': scap = 0.97 * n['speed'] / t['speed']; wcap = 0.95 * n['width'] / t['width']; nxt = n['cost']
        else:
            last = n is None
            scap = 1.15 if last else max(1.06, 0.97 * n['speed'] / t['speed']); wcap = 1.25; nxt = t['cost'] * 4 if last else n['cost']
        spec[t['id']] = dict(width=t['width'], speed=t['speed'], value=t['value'], cost=t['cost'], speedPer=(scap - 1) / L, sizePer=(wcap - 1) / L, max=L,
                             upBase=max(8, round(nxt * cfg['costFrac'])), caps=(round(scap, 3), round(wcap, 3)))
    for t in rides:
        spec[t['id']] = dict(width=t['width'], speed=t['speed'], value=t['value'], cost=t['cost'], speedPer=0.15 / L, sizePer=0.25 / L, max=L,
                             upBase=round(t['cost'] * 1.5 * cfg['costFrac']), caps=(1.15, 1.25))
    return spec
# today's Snowcat and Rotary, frozen whatever comes after them
FROZEN = {'snowcat': (max(1.06, 0.97 * 104 / 92), 1.25, 18e6), 'rotary': (1.15, 1.25, 18e6 * 4)}
def go(loader=None, ice=None, seeds=6, caps=None, comboScale=1.0, **kw):
    base, rides = build(loader, ice)
    e.TOOLS[:] = base + rides; e.BASE = len(base)
    cp = dict(FROZEN); cp.update(caps or {})
    orig = e.machine_specs; e.machine_specs = lambda cfg: specs(cfg, base, rides, cp)
    out = []
    for s in range(seeds):
        cfg = copy.deepcopy(e.CFG); cfg.update(effFirst=0.45, effGain=0.03, effMax=0.62, costFrac=0.06, costGrowth=1.45); cfg['value']['growth'] = 1.72
        cfg['bossStars'] = dict(cfg['bossStars'], icepalace=20)
        cfg.update(rides=False, seed=s, comboBy=COMBO, comboScale=comboScale, ridesAfter=[t['id'] for t in base].index('rotary')); cfg.update(kw)
        res = e.run(cfg, maxRuns=1400); f = res['first']
        ev = {}
        for r, x in res['events']:
            if x.startswith('MACHINE') or x.startswith('MK2'): ev.setdefault(x.replace('MACHINE ', '').replace('MK2 ', 'mk2:'), r)
        def start(a): return min([f[j['id']]['run'] for j in e.JOBS if j['area'] == a and j['id'] in f] or [999])
        areas = {a: start(a) for a in e.AREA_SEQ}
        north = [l for l in res['log'] if l['r'] >= areas['north']]
        mruns = sorted([0] + [v for k, v in ev.items() if not k.startswith('mk2')] + [len(res['log'])])
        gaps = [b - a for a, b in zip(mruns, mruns[1:])]
        out.append(dict(runs=len(res['log']), ev=ev, areas=areas, north=len(north), rep=sum(1 for l in north if l['kind'] == 'grind'), maxgap=max(gaps), gaps=gaps,
                        spec=res['spec'], log=res['log'], earned=res['earned'], stars=res['total_stars']))
    e.machine_specs = orig
    return out, [t['id'] for t in base]
def show(label, R, ids):
    m = lambda f: st.mean(f(r) for r in R)
    print(label)
    print('  winter 1: %.0f runs (~%.1f h at 1.5 min/run) | North: %.0f runs, %.0f replays | longest stretch with no new machine: %.0f runs' % (
        m(lambda r: r['runs']), m(lambda r: r['runs']) * 1.5 / 60, m(lambda r: r['north']), m(lambda r: r['rep']), m(lambda r: r['maxgap'])))
    print('  areas start at run', {a: round(m(lambda r: r['areas'][a])) for a in e.AREA_SEQ})
    keys = [k for k in ids] + ['mk2:' + k for k in ids]
    print('  bought at run', {k: round(st.mean(r['ev'][k] for r in R if k in r['ev'])) for k in keys if any(k in r['ev'] for r in R)})
