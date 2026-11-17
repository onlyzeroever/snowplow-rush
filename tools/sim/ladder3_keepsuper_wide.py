import sys, json, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ladder3 as L, statistics as st
lc, sc, rc, ic = [float(x) for x in sys.argv[1:5]]
lw, ls, lv = 52, 80, 7.5
loader = dict(name='FRONT LOADER', cost=lc, width=lw, speed=ls, value=lv) if lc else None
iw, isp = (int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (66, 136)
ice = dict(name='ICEBREAKER', cost=ic, width=iw, speed=isp, value=18) if ic else None
for t in L.GAME_TOOLS:
    if t['id'] == 'snowcat': t['cost'] = sc
    if t['id'] == 'rotary': t['cost'] = rc
caps = {'snowcat': (max(1.06, 0.97 * 104 / 92), 1.25, rc), 'rotary': (1.15, 1.25, 72e6)}
if loader: caps['loader'] = (1.08, 1.06, sc); caps['super'] = (1.15, 1.30, 6.5e6)
import os
kw = json.loads(os.environ.get('KW', '{}'))
R, ids = L.go(loader, ice, caps=caps, seeds=int(sys.argv[5]) if len(sys.argv) > 5 else 6, **kw)
L.show('L %.1fM S %.1fM R %.0fM I %.0fM' % (lc / 1e6, sc / 1e6, rc / 1e6, ic / 1e6), R, ids)
print('  gaps', [round(st.mean(r['gaps'][i] for r in R)) for i in range(len(R[0]['gaps']))])
# rate of the machine you drive when the next one is bought, vs the new one's base
for r in R[:3]:
    sp = r['spec']; prev = None
    for l in r['log']:
        if prev and l['m'] != prev['m']:
            a, b = sp[prev['m']], sp[l['m']]; lvp = prev['lv']
            ra = a['width'] * (1 + a['sizePer'] * lvp.get('size', 0)) * a['speed'] * (1 + a['speedPer'] * lvp.get('speed', 0))
            print('   %s lv%s -> %s: clearing %+.0f%%, coins/cell %+.0f%%' % (prev['m'], (lvp.get('speed'), lvp.get('size')), l['m'], (b['width'] * b['speed'] / ra - 1) * 100, (b['value'] / a['value'] - 1) * 100))
        prev = l
