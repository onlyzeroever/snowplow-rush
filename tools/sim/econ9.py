"""Snowplow Rush economy sim v5: per-machine upgrades.
Mirrors the game: coins = cells * BASE_CELL_VALUE * job.value * valueMult * combo, star bonus, presents,
helpers income, machines and per-machine upgrades (speed, width, bumper) + global (value, helpers).
A 'typical player' plays forward, replays for stars when stuck, and buys greedily.
"""
import json, math, sys, copy
JOBS = json.load(open('/home/claude/sim/jobs.json'))
TOOLS = json.load(open('/home/claude/sim/tools.json'))
BASE_CELL_VALUE = 0.03
STAR_BONUS = 50
AREA_SEQ = ['suburbs', 'farm', 'city', 'themepark', 'harbour', 'ski', 'pass', 'north']
BASE = 8

CFG = dict(
    speeds={'shovel': 32, 'pusher': 38, 'blower': 44, 'tractor': 52, 'truck': 62, 'super': 74, 'snowcat': 92, 'rotary': 104},
    widthCap=0.95, speedCap=0.97, lastCap=(1.15, 1.30), levels=6, bumperLevels=5,
    costFrac=0.018, costGrowth=1.5,
    value=dict(base=30, growth=1.62, max=20, per=0.12),
    helpers=dict(base=120, growth=1.75, max=20, per=0.4),
    combo=1.35, presentsTaken=0.55, hazardLoss=0.05,
    effFirst=0.60, effGain=0.035, effMax=0.74, eff3=0.75,
    menuSecs=15, dailyEvery=10,
    bossStars={'blockparty': 25, 'harvestfair': 25, 'parade': 25, 'openingday': 26, 'festival': 26, 'grandslalom': 24, 'blizzard': 24, 'icepalace': 24},
    jobs={},  # per-job overrides {id: {time:, value:, stars:}}
)

def machine_specs(cfg):
    base = [t for t in TOOLS[:BASE]]
    spec = {}
    for i, t in enumerate(base):
        sp = cfg['speeds'].get(t['id'], t['speed'])
        if t['id'] == 'super':
            scap, wcap = cfg['lastCap']; nxtCost = base[i + 1]['cost']
        elif i + 1 < len(base):
            n = base[i + 1]; nsp = cfg['speeds'].get(n['id'], n['speed'])
            scap = cfg['speedCap'] * nsp / sp; wcap = cfg['widthCap'] * n['width'] / t['width']
            nxtCost = n['cost']
        else:
            scap, wcap = cfg['lastCap']; nxtCost = t['cost'] * 4
        L = cfg['levels']
        spec[t['id']] = dict(width=t['width'], speed=sp, value=t['value'], cost=t['cost'],
                             speedPer=(scap - 1) / L, sizePer=(wcap - 1) / L, max=L,
                             upBase=max(8, round(nxtCost * cfg['costFrac'])))
    for t in TOOLS[BASE:]:
        L = cfg['levels']
        spec[t['id']] = dict(width=t['width'], speed=t['speed'], value=t['value'], cost=t['cost'], speedPer=0.15 / L, sizePer=0.25 / L, max=L,
                             upBase=round(t['cost'] * 1.5 * cfg['costFrac']))
    return spec

def run(cfg, maxRuns=600, verbose=False, stop_area=None):
    for t in TOOLS:
        t.setdefault('cost0', t['cost']); t['cost'] = cfg.get('costs', {}).get(t['id'], t['cost0'])
    spec = machine_specs(cfg)
    order = [j for j in JOBS if j['area'] in AREA_SEQ]
    order.sort(key=lambda j: (AREA_SEQ.index(j['area']), j['i']))  # placeholder; play order handled by unlock graph
    idx = {j['id']: j for j in JOBS}
    for jid, o in cfg['jobs'].items():
        if jid in idx: idx[jid].update(o)
    owned = 0  # index of best machine owned
    mlv = {t['id']: dict(speed=0, size=0, bumper=0) for t in TOOLS}
    import random as _r; RNG = _r.Random(cfg.get('seed', 1)); RIDES = dict(on=cfg.get('rides', False), parts=0, tries=0, after=cfg.get('ridesAfter', 7))
    glv = dict(value=0, helpers=0)
    coins = 0.0; stars = {j['id']: 0 for j in JOBS}; tries = {j['id']: 0 for j in JOBS}; tolls = set(); fails = {j['id']: 0 for j in JOBS}
    log = []; events = []; first = {}
    def mach(): return TOOLS[owned]['id']
    def width(m=None):
        m = m or mach(); s = spec[m]; return min(80, round(s['width'] * (1 + s['sizePer'] * mlv[m]['size'])))
    OFF = dict(coins=0, run=0, sessions=0)
    BST = {'on': False}
    def speed(m=None):
        m = m or mach(); s = spec[m]; return s['speed'] * (1 + s['speedPer'] * mlv[m]['speed']) * (1.25 if BST['on'] else 1)
    def vmult(): return spec[mach()]['value'] * (1 + cfg['value']['per'] * glv['value'])
    def ucost(k):
        if k in ('speed', 'size'):
            return math.floor(spec[mach()]['upBase'] * cfg['costGrowth'] ** mlv[mach()][k])
        if k == 'bumper':
            return math.floor(spec[mach()]['upBase'] * 1.2 * cfg['costGrowth'] ** mlv[mach()][k])
        u = cfg[k]; return math.floor(u['base'] * u['growth'] ** glv[k])
    def umaxed(k):
        if k in ('speed', 'size'): return mlv[mach()][k] >= spec[mach()]['max']
        if k == 'bumper': return mlv[mach()][k] >= cfg['bumperLevels']
        return glv[k] >= cfg[k]['max']
    def area_stars(a): return sum(stars[x['id']] for x in JOBS if x['area'] == a and not x.get('boss'))
    def reach(j):
        if j['area'] == 'secret': return False
        if j.get('boss') and area_stars(j['area']) < cfg['bossStars'].get(j['id'], 0): return False
        if not j['from']: return True
        return any(stars[f] > 0 for f in j['from'] if f in stars)
    def gate_ok(j):
        if not j['gate']: return True
        return owned >= [t['id'] for t in TOOLS].index(j['gate'])
    def opened(j): return reach(j) and gate_ok(j) and (not j['toll'] or j['id'] in tolls)
    def attempt(j, eff):
        clr_px = j['clr'] * 4
        rate = width() * 2 * speed() * eff
        T = j['time'] * (1 + 0.25 * j['presents'] * cfg['presentsTaken'] * 4 / j['time'] / 4)
        cleared = min(clr_px * 0.985, rate * T * (1 - 0.03))
        pct = cleared / clr_px * 100
        cells = cleared / 4
        c = cells * BASE_CELL_VALUE * j['value'] * vmult() * cfg['combo'] * (1 - cfg['hazardLoss'])
        c += j['presents'] * cfg['presentsTaken'] * 0.5 * 250 * j['value'] * vmult()
        c += glv['helpers'] * cfg['helpers']['per'] * vmult() * (j['time'] + cfg['menuSecs'])
        return pct, c
    def t3(j, eff=None):  # seconds a skilled player needs for 3 stars with the current kit
        eff = eff or cfg['eff3']; need = j['clr'] * 4 * j['stars'][2] / 100
        return need / (width() * 2 * speed() * eff)
    total_stars = lambda: sum(stars.values())
    playable = [j for j in JOBS if j['area'] in AREA_SEQ]
    for r in range(1, maxRuns + 1):
        if RIDES['on'] and owned >= RIDES['after'] and owned + 1 < len(TOOLS) and owned + 1 >= BASE and RIDES['parts'] >= 3:
            ri = owned + 1; t = TOOLS[ri]; mj = next(x for x in JOBS if x.get('tool') == t['id'])
            RIDES['tries'] += 1
            eff = min(cfg['effMax'], cfg['effFirst'] + cfg['effGain'] * (RIDES['tries'] - 1))
            base_rate = t['width'] * 2 * t['speed']
            if cfg.get('rideMatch'): base_rate = max(base_rate, width() * 2 * speed())
            pct = min(98.5, base_rate * eff * mj['time'] * 0.97 / (mj['clr'] * 4) * 100)
            coins += pct / 100 * mj['clr'] * BASE_CELL_VALUE * mj['value'] * t['value'] * cfg['combo']
            if pct >= mj['stars'][1]:
                owned = ri; RIDES['parts'] = 0; RIDES['tries'] = 0; events.append((r, 'MACHINE ' + t['id']))
                if cfg.get('rideMatch'):
                    best = max(width() * 2 * speed() for _ in [0])
                    lv = mlv[t['id']]; sp = spec[t['id']]
                    while (t['width'] * (1 + sp['sizePer'] * lv['size'])) * 2 * (t['speed'] * (1 + sp['speedPer'] * lv['speed'])) < best and (lv['size'] < sp['max'] or lv['speed'] < sp['max']):
                        if lv['size'] <= lv['speed'] and lv['size'] < sp['max']: lv['size'] += 1
                        else: lv['speed'] += 1
            log.append(dict(r=r, job=mj['id'], kind='mission', pct=round(pct), coins=round(coins), m=mach(), lv={}, g=dict(glv)))
            continue
        open_ = [j for j in playable if opened(j)]
        # forward first: the newest open job that can still gain a star with a decent attempt
        cand = None
        for j in sorted(open_, key=lambda j: (AREA_SEQ.index(j['area']), -j['i'] if False else j['i']), reverse=True):
            eff = min(cfg['effMax'], cfg['effFirst'] + cfg['effGain'] * tries[j['id']])
            pct, _ = attempt(j, eff)
            s = sum(pct >= t for t in j['stars'])
            if stars[j['id']] == 0 or (s > stars[j['id']] and stars[j['id']] < 2):
                cand = j; break
        kind = 'progress'
        if cand is None:
            # grind: best coins per run among open jobs, prefer ones that can give a new star
            best = None
            for j in open_:
                eff = min(cfg['effMax'], cfg['effFirst'] + cfg['effGain'] * tries[j['id']])
                pct, c = attempt(j, eff); s = sum(pct >= t for t in j['stars'])
                gap = min([t - pct for t in j['stars'] if t > pct] or [999])
                score = c + (10 ** 9 if s > stars[j['id']] else 0) - gap * 1e6
                if best is None or score > best[0]: best = (score, j)
            cand = best[1]; kind = 'grind'
        j = cand; eff = min(cfg['effMax'], cfg['effFirst'] + cfg['effGain'] * tries[j['id']])
        if j['id'] not in first:
            first[j['id']] = dict(run=r, machine=mach(), lv=dict(mlv[mach()]), glv=dict(glv), t3=round(t3(j), 1), d=round(t3(j) / j['time'], 2))
        BST['on'] = cfg.get('boost', True) and fails[j['id']] >= 3 and stars[j['id']] < 3
        if BST['on']: fails[j['id']] = 0
        pct, c = attempt(j, eff); tries[j['id']] += 1; BST['on'] = False
        s = sum(pct >= t for t in j['stars']); prev = stars[j['id']]
        fails[j['id']] = 0 if s > prev else fails[j['id']] + 1
        bonus = sum(STAR_BONUS * j['value'] * (k + 1) for k in range(prev, s))
        if s > prev:
            stars[j['id']] = s; events.append((r, '%s %d*' % (j['id'], s))); kind = 'star'
            if 'firstStar' not in first[j['id']]: first[j['id']]['firstStar'] = r
            if s == 3: first[j['id']]['three'] = r
        coins += c + bonus
        if RIDES['on'] and owned >= RIDES['after'] and owned + 1 < len(TOOLS) and owned + 1 >= BASE and RIDES['parts'] < 3 and (RNG.random() < (0.45 if RIDES['parts'] == 0 else 0.3) or (cfg.get('pity') and RIDES.get('dry', 0) >= cfg['pity'] - 1)): RIDES['parts'] += 1; RIDES['dry'] = 0
        elif RIDES['on'] and owned >= RIDES['after'] and owned + 1 < len(TOOLS) and owned + 1 >= BASE and RIDES['parts'] < 3: RIDES['dry'] = RIDES.get('dry', 0) + 1
        S = cfg.get('session')
        if S:
            if r % S['runs'] == 0:
                aw = S['away'][(r // S['runs']) % len(S['away'])] * 3600
                g = glv['helpers'] * cfg['helpers']['per'] * vmult() * min(S['cap'] * 3600, aw) * 0.5
                coins += g; OFF['coins'] += g; OFF['sessions'] += 1
            OFF['run'] += c + bonus
        if cfg['dailyEvery'] and r % cfg['dailyEvery'] == 0:
            best_pay = max([x['value'] for x in open_] + [1]); coins += 150 * best_pay * vmult()
        first[j['id']].setdefault('pcts', []).append(round(pct))
        # shopping
        while True:
            # tolls for jobs you've reached
            paid = False
            for x in playable:
                if x['toll'] and x['id'] not in tolls and reach(x) and coins >= x['toll']:
                    coins -= x['toll']; tolls.add(x['id']); events.append((r, 'TOLL ' + x['id'])); paid = True
            if paid: continue
            if owned + 1 < BASE and coins >= TOOLS[owned + 1]['cost']:
                coins -= TOOLS[owned + 1]['cost']; owned += 1; events.append((r, 'MACHINE ' + mach())); continue
            # saving: a toll or a gate machine stands between you and the next job -> only small upgrades
            goals = [x['toll'] for x in playable if x['toll'] and x['id'] not in tolls and reach(x)]
            goals += [TOOLS[owned + 1]['cost'] for x in playable if owned + 1 < BASE and x['gate'] and reach(x) and not gate_ok(x)]
            goal = min(goals) if goals else None
            opts = [k for k in ('speed', 'size', 'value') if not umaxed(k)]
            if not opts: opts = [k for k in ('helpers', 'bumper') if not umaxed(k)]
            if not opts: break
            cheapest = min(ucost(k) for k in opts)
            if not umaxed('helpers') and ucost('helpers') < cheapest * 1.5: opts.append('helpers')
            if not umaxed('bumper') and ucost('bumper') < cheapest * 0.8: opts.append('bumper')
            k = min(opts, key=ucost)
            if goal and cfg.get('saver', True) and ucost(k) > 0.1 * goal: break
            if coins >= ucost(k):
                coins -= ucost(k)
                if k in ('speed', 'size', 'bumper'): mlv[mach()][k] += 1
                else: glv[k] += 1
                continue
            break
        log.append(dict(r=r, job=j['id'], kind=kind, pct=round(pct), coins=round(coins), m=mach(), lv=dict(mlv[mach()]), g=dict(glv)))
        if stop_area:
            done = all(stars[x['id']] > 0 for x in playable if x['area'] == stop_area)
            if done: break
        if all(stars[x['id']] > 0 for x in playable): break
    return dict(log=log, events=events, first=first, stars=stars, spec=spec, off=OFF)

def report(res, cfg):
    first = res['first']; log = res['log']
    print('machine purchases:', [e for e in res['events'] if e[1].startswith('MACHINE') or e[1].startswith('TOLL')])
    print('%-11s %-7s %4s %4s %5s %5s %s' % ('job', 'mach', 'run', '1st*', 'd', 'lvS/W', 'pcts'))
    for j in sorted(JOBS, key=lambda j: first.get(j['id'], {}).get('run', 9999)):
        f = first.get(j['id'])
        if not f: continue
        print('%-11s %-7s %4d %4s %5.2f %2d/%-2d %s' % (j['id'], f['machine'], f['run'], f.get('firstStar', '-'), f['d'], f['lv']['speed'], f['lv']['size'], f['pcts'][:6]))
    # streaks of runs without any new star / purchase
    longest = cur = 0
    ev_runs = set(e[0] for e in res['events'])
    for l in log:
        cur = 0 if l['r'] in ev_runs else cur + 1; longest = max(longest, cur)
    areas = {}
    for a in AREA_SEQ:
        rs = [first[j['id']].get('firstStar', 9999) for j in JOBS if j['area'] == a and j['id'] in first]
        areas[a] = max(rs) if rs else None
    print('runs total', len(log), '| area done at run', areas, '| longest dry streak', longest,
          '| grind runs', sum(1 for l in log if l['kind'] == 'grind'))

if __name__ == '__main__':
    res = run(CFG); report(res, CFG)
