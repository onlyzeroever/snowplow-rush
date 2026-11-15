import tune6, econ5 as e, json, copy
from collections import defaultdict
desired = {'harbour': 1.08, 'ski': 1.14, 'pass': 1.2, 'north': 1.28}
times = {j['id']: j['time'] for j in e.JOBS}
def sim(sc, ro):
    o, res = tune6.go({'snowcat': sc, 'rotary': ro}, jobs={k: {'time': v} for k, v in times.items()})
    f = res['first']; A = defaultdict(list)
    for j in e.JOBS:
        if j['id'] in f and j['area'] in desired: A[j['area']].append(f[j['id']]['d'])
    ev = {k: v for v, k in o['ev']}
    return o, {a: sum(v) / len(v) for a, v in A.items()}, ev
best = None
for it in range(5):
    # prices: snowcat lands as the Ski Resort opens, the Rotary as the Pass opens
    res_p = []
    for sc in (3e6, 4e6, 5e6, 6.5e6, 8e6):
        for ro in (1e7, 1.4e7, 1.8e7, 2.4e7):
            o, d, ev = sim(sc, ro); a = o['areas']
            err = abs((ev.get('MACHINE snowcat', 999) - a['ski'][0])) + abs((ev.get('MACHINE rotary', 999) - a['pass'][0]))
            res_p.append((err, sc, ro))
    err, sc, ro = min(res_p)
    o, d, ev = sim(sc, ro)
    print('iter', it, 'prices %.1fM %.1fM' % (sc / 1e6, ro / 1e6), 'buy', ev.get('MACHINE snowcat'), ev.get('MACHINE rotary'), 'areas', {k: v for k, v in o['areas'].items() if k in desired}, 'd', {k: round(v, 2) for k, v in d.items()}, 'runs', o['runs'], 'grind', o['grind'])
    for j in e.JOBS:
        if j['area'] in desired and j['area'] in d:
            times[j['id']] = max(28, round(times[j['id']] * d[j['area']] / desired[j['area']]))
    best = (sc, ro)
json.dump(dict(prices=best, times={j['id']: times[j['id']] for j in e.JOBS if j['area'] in desired}), open('/home/claude/sim/calib_out.json', 'w'))
