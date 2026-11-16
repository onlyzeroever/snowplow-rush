import econ6 as e, copy, sys, json
def go(costs=None, vg=1.72, cf=0.06, cg=1.45, show=False, **kw):
    cfg = copy.deepcopy(e.CFG); cfg.update(effFirst=0.45, effGain=0.03, effMax=0.62, costFrac=cf, costGrowth=cg, costs=costs or {}); cfg['value']['growth'] = vg; cfg.update(kw)
    res = e.run(cfg, maxRuns=900)
    ev = [(x[0], x[1]) for x in res['events'] if x[1].startswith('MACHINE') or x[1].startswith('TOLL')]
    f = res['first']
    def start(a): return min([f[j['id']]['run'] for j in e.JOBS if j['area'] == a and j['id'] in f] or [None])
    def done(a): return max([f[j['id']].get('firstStar', 9999) for j in e.JOBS if j['area'] == a and j['id'] in f] or [None])
    areas = {a: (start(a), done(a)) for a in e.AREA_SEQ}
    if show: e.report(res, cfg)
    return dict(ev=ev, areas=areas, runs=len(res['log']), grind=sum(1 for l in res['log'] if l['kind'] == 'grind')), res
if __name__ == '__main__':
    o, res = go(show='-v' in sys.argv)
    print('purchases', o['ev']); print('areas (start, done)', o['areas']); print('runs', o['runs'], 'grind runs', o['grind'])
