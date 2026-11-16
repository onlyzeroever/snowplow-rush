"""New regular machines: Wheel Loader (Harbour), Glacier Titan (Pass), Icebreaker (North). Uses econ9 (missions, pity),
with machine upgrade caps mirroring the game's mspec(), and Wild Rides floored to your best base machine's clearing rate."""
import econ9 as e, copy, statistics as st, json
GAME_TOOLS = json.load(open('/home/claude/sim/tools.json'))
NEW = {'loader': dict(id='loader', name='WHEEL LOADER', cost=2.2e6, width=42, speed=82, value=8),
       'titan': dict(id='titan', name='GLACIER TITAN', cost=6e7, width=50, speed=112, value=17),
       'icebreaker': dict(id='icebreaker', name='ICEBREAKER', cost=2.2e8, width=52, speed=124, value=22)}
def ladder(with_new):
    base = [t for t in GAME_TOOLS if not t.get('winter')]
    rides = [t for t in GAME_TOOLS if t.get('winter')]
    if with_new:
        i = [t['id'] for t in base].index('super'); base.insert(i + 1, NEW['loader'])
        base += [NEW['titan'], NEW['icebreaker']]
    return base, rides
def game_specs(cfg, base, rides):
    spec = {}; L = cfg['levels']
    for i, t in enumerate(base + rides):
        n = (base + rides)[i + 1] if i + 1 < len(base + rides) else None
        isBase = i < len(base)
        if t['id'] == 'super': scap, wcap, nxt = 1.15, 1.3, n['cost']
        elif i > 5:
            last = i >= len(base) - 1
            scap = max(1.06, 0.97 * n['speed'] / t['speed']) if (not last and n) else 1.15
            wcap = 1.25; nxt = n['cost'] if (not last and n) else t['cost'] * (4 if isBase else 1.5)
        else: scap = 0.97 * n['speed'] / t['speed']; wcap = 0.95 * n['width'] / t['width']; nxt = n['cost']
        spec[t['id']] = dict(width=t['width'], speed=t['speed'], value=t['value'], cost=t['cost'], speedPer=(scap - 1) / L, sizePer=(wcap - 1) / L, max=L,
                             upBase=max(8, round(nxt * cfg['costFrac'])))
    return spec
def go(with_new, seeds=8, **kw):
    base, rides = ladder(with_new)
    e.TOOLS[:] = base + rides; e.BASE = len(base)
    orig = e.machine_specs; e.machine_specs = lambda cfg: game_specs(cfg, base, rides)
    out = []
    for s in range(seeds):
        cfg = copy.deepcopy(e.CFG); cfg.update(effFirst=0.45, effGain=0.03, effMax=0.62, costFrac=0.06, costGrowth=1.45); cfg['value']['growth'] = 1.72
        cfg['bossStars'] = dict(cfg['bossStars'], icepalace=20); cfg.update(rides=True, rideMatch=True, pity=8, seed=s, ridesAfter=[t['id'] for t in base].index('rotary')); cfg.update(kw)
        res = e.run(cfg, maxRuns=900); f = res['first']
        ev = {}
        for r, x in res['events']:
            if x.startswith('MACHINE'): ev.setdefault(x.split()[1], r)
        def start(a): return min([f[j['id']]['run'] for j in e.JOBS if j['area'] == a and j['id'] in f] or [999])
        areas = {a: start(a) for a in e.AREA_SEQ}
        north = [l for l in res['log'] if l['r'] >= areas['north']]
        allm = sorted([0] + list(ev.values()) + [len(res['log'])])
        gaps = [b - a for a, b in zip(allm, allm[1:])]
        out.append(dict(runs=len(res['log']), ev=ev, areas=areas, north=len(north), rep=sum(1 for l in north if l['kind'] == 'grind'), maxgap=max(gaps), gaps=gaps))
    e.machine_specs = orig
    return out, [t['id'] for t in base + rides]
for label, wn in (('TODAY (8 regular machines + 5 Wild Rides)', False), ('WITH LOADER, TITAN, ICEBREAKER', True)):
    R, ids = go(wn)
    print(label)
    print('  winter 1 done in %.0f runs (~%.1f h at 1.5 min/run); North: %.0f runs, %.0f replays; longest stretch with no new machine: %.0f runs' % (
        st.mean(r['runs'] for r in R), st.mean(r['runs'] for r in R) * 1.5 / 60, st.mean(r['north'] for r in R), st.mean(r['rep'] for r in R), st.mean(r['maxgap'] for r in R)))
    print('  area starts', {a: round(st.mean(r['areas'][a] for r in R)) for a in e.AREA_SEQ})
    print('  machines at runs', {m: round(st.mean(r['ev'][m] for r in R if m in r['ev'])) for m in ids if any(m in r['ev'] for r in R)})
