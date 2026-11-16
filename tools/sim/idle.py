import econ7 as e, copy, sys
def go(**kw):
    cfg = copy.deepcopy(e.CFG); cfg.update(effFirst=0.45, effGain=0.03, effMax=0.62, costFrac=0.06, costGrowth=1.45); cfg['value']['growth'] = 1.72
    cfg['bossStars'] = dict(cfg['bossStars'], icepalace=kw.pop('ice', 24))
    cfg.update(kw)
    res = e.run(cfg, maxRuns=900)
    ev = {x[1]: x[0] for x in res['events'] if x[1].startswith('MACHINE')}
    f = res['first']
    north = [l for l in res['log'] if l['r'] >= min(f[j['id']]['run'] for j in e.JOBS if j['area'] == 'north' and j['id'] in f)]
    return dict(runs=len(res['log']), mach=[ev.get('MACHINE ' + m) for m in ('pusher', 'blower', 'tractor', 'truck', 'super', 'snowcat', 'rotary')],
                north=len(north), north_rep=sum(1 for l in north if l['kind'] == 'grind'), off=res['off'])
base = go(ice=20)
print('no idle at all      runs %d  machines at runs %s  North %d runs (%d replays)' % (base['runs'], base['mach'], base['north'], base['north_rep']))
for name, S in (('evening player: 10 runs a day, away ~23 h', dict(runs=10, away=[23.5])), ('twice a day: 8 runs, away 9 h / 14 h', dict(runs=8, away=[9, 14]))):
    print(name)
    for cap in (2, 6, 8, 12):
        o = go(ice=20, session=dict(S, cap=cap)); off = o['off']
        days = o['runs'] / S['runs'] / (1 if S['runs'] == 10 else 2)
        print('  cap %2d h: runs %d (%.0f days)  machines %s  North %d runs (%d replays)  idle = %.0f%% of all coins, %.1f runs of coins per return' % (
            cap, o['runs'], days, o['mach'], o['north'], o['north_rep'], 100 * off['coins'] / (off['coins'] + off['run']), off['coins'] / max(1, off['sessions']) / (off['run'] / o['runs'])))
