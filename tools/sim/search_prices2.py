import tune6 as t
def ev(sc, ro):
    o, res = t.go(costs={'snowcat': sc, 'rotary': ro})
    d = dict((x[1].split()[1], x[0]) for x in o['ev'])
    return d.get('snowcat'), d.get('rotary'), o['areas']['harbour'][0], o['areas']['ski'][0], o['areas']['pass'][0], o['areas']['north'], o['runs'], o['grind']
for sc, ro in ((6.5e6, 18e6), (8e6, 18e6), (9e6, 24e6), (10e6, 28e6), (8e6, 30e6)):
    print(sc/1e6, ro/1e6, ev(sc, ro), flush=True)
