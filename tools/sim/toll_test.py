import tune6 as t
for toll in (500000, 350000, 300000):
    for saver in (True, False):
        o, res = t.go(jobs={'stadium': {'toll': toll}}, saver=saver)
        d = dict((x[1].split()[1], x[0]) for x in o['ev'])
        ev = res['events']; st = [e for e in ev if 'stadium' in e[1]]
        print(toll, 'saver' if saver else 'spender', 'toll paid run', d.get('stadium'), 'super', d.get('super'), 'stadium stars', st[:2], 'city', o['areas']['city'], 'runs', o['runs'], 'grind', o['grind'], flush=True)
