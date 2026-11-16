import econ9 as e, copy, statistics as st
def go(**kw):
    cfg = copy.deepcopy(e.CFG); cfg.update(effFirst=0.45, effGain=0.03, effMax=0.62, costFrac=0.06, costGrowth=1.45); cfg['value']['growth'] = 1.72
    cfg['bossStars'] = dict(cfg['bossStars'], icepalace=kw.pop('ice', 24)); cfg.update(kw)
    res = e.run(cfg, maxRuns=900); f = res['first']
    ev = {}
    for r, x in res['events']:
        if x.startswith('MACHINE'): ev.setdefault(x.split()[1], r)
    def start(a): return min([f[j['id']]['run'] for j in e.JOBS if j['area'] == a and j['id'] in f] or [None])
    areas = {a: start(a) for a in e.AREA_SEQ}
    north = [l for l in res['log'] if l['r'] >= areas['north']]
    return dict(runs=len(res['log']), ev=ev, areas=areas, north=len(north), rep=sum(1 for l in north if l['kind'] == 'grind'), mis=sum(1 for l in res['log'] if l['kind'] == 'mission'))
for label, kw in (('before (missions, fresh rides weak)', dict(ice=20, rides=True)), ('after: day-one match + pity 8', dict(ice=20, rides=True, rideMatch=True, pity=8))):
    R = [go(seed=s, **kw) for s in range(12)]
    print(label)
    print('  runs %.0f  North starts ~run %.0f, %.0f runs there, %.0f replays, missions played %.0f' % (st.mean(r['runs'] for r in R), st.mean(r['areas']['north'] for r in R), st.mean(r['north'] for r in R), st.mean(r['rep'] for r in R), st.mean(r['mis'] for r in R)))
    for m in ('super', 'snowcat', 'rotary', 'monster', 'jet', 'mech', 'dragon', 'ufo'):
        xs = [r['ev'][m] for r in R if m in r['ev']]
        if xs: print('   %-8s run %3.0f  (%d of 12 runs-throughs)' % (m, st.mean(xs), len(xs)))
    print('  area starts', {a: round(st.mean(r['areas'][a] for r in R)) for a in e.AREA_SEQ})
