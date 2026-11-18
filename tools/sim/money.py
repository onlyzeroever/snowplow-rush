"""Snowplow Rush money sim (Nov 18). Conservative by default, as Alex asked.

Per 1,000 installs: how many players of each kind, what each brings, lifetime value (LTV) at day 30/90/365,
the most we could pay per install and still break even, and money per month at a few install rates.

Sources for the ranges (searched Nov 18, 2026, see the plan doc):
- Retention: median casual D1 ~22%, D7 ~4%; top 10% D1 ~40%, D7 ~12% (earlier research, logged in the plan doc).
- Payers 1-3% of installs; 77% of payers buy within 2 weeks; first buys $1-5 (earlier research).
- Rewarded eCPM: US ~$16.5 Android / ~$19.6 iOS; top-tier markets $10-30. Worldwide mixes are much lower.
- Ads ARPDAU, casual ads-only: $0.01-0.05. Hybrid casual blended: $0.15-0.50.
- CPI: casual $1.41 iOS / $0.14 Android (Liftoff); $2.50 / $1.50 (Business of Apps); US simulation $4.23 / $2.50 (AppsFlyer Q3 2026).
- Store fee 15% (small business programmes); VAT/GST and refunds take a few % more.
"""
import json, math, random, sys

SCEN = {
  # retention points, rewarded views per active player per day, blended rewarded eCPM ($), share of players who ever watch,
  # share of installs who ever buy, payer mix (small/mid/big) and their average gross spend, store net
  'conservative': dict(d1=0.22, d7=0.04, d30=0.012, views=1.2, ecpm=7.0, watch=0.40,
                       conv=0.010, mix=(0.70, 0.25, 0.05), spend=(3.0, 15.0, 40.0), spend_rep=(3.0, 18.0, 60.0), net=0.75),
  'base':         dict(d1=0.30, d7=0.08, d30=0.025, views=2.0, ecpm=10.0, watch=0.50,
                       conv=0.020, mix=(0.65, 0.27, 0.08), spend=(3.5, 18.0, 40.0), spend_rep=(3.5, 22.0, 80.0), net=0.80),
  'hopeful':      dict(d1=0.40, d7=0.12, d30=0.045, views=3.0, ecpm=14.0, watch=0.60,
                       conv=0.035, mix=(0.60, 0.30, 0.10), spend=(4.0, 20.0, 40.0), spend_rep=(4.0, 25.0, 100.0), net=0.82),
}
# "today's shop" = one-offs only (Premium, Wild Rides, Ride Pass, starter pack): a big fan runs out at ~$40.
# "with repeat buys" = + Winter Pass, Event Pass, gem/coin packs, limited-time offers (the plan's Phase 3).

def retention(sc):
    """r[d] for d=0..365, r[0]=1. Power-law between the points; after D30 a slow tail."""
    pts = [(1, sc['d1']), (7, sc['d7']), (30, sc['d30']), (90, sc['d30']*0.45), (180, sc['d30']*0.28), (365, sc['d30']*0.15)]
    r = [1.0]
    for d in range(1, 366):
        for (a, ra), (b, rb) in zip(pts, pts[1:]):
            if a <= d <= b:
                k = math.log(rb/ra)/math.log(b/a); r.append(ra*(d/a)**k); break
    return r

def model(name, repeat=False, sc=None):
    sc = dict(SCEN[name], **(sc or {}))
    r = retention(sc)
    cum = [0.0]
    for d in range(366): cum.append(cum[-1]+r[d])          # cum[n] = active days in days 0..n-1
    days = {30: cum[31], 90: cum[91], 365: cum[366]}
    # buyers come from players who stay: if retention changes, the share who buy moves with play time
    ref = SCEN[name]; rr = retention(ref); ref_days = sum(rr[:366])
    sc['conv'] = sc['conv']*(days[365]/ref_days)
    ad_day = sc['views']*sc['ecpm']/1000                     # $ per active player per day
    spend = sc['spend_rep'] if repeat else sc['spend']
    arppu = sum(m*s for m, s in zip(sc['mix'], spend))
    iap_total = sc['conv']*arppu*sc['net']                   # $ per install, lifetime (1 year)
    # when it comes in: one-off buys mostly early (77% of first buys within 14 days); repeat buys follow play time
    one_off = sum(m*min(s, sc['spend'][i]) for i, (m, s) in enumerate(zip(sc['mix'], spend)))/arppu
    first = lambda d: 1-math.exp(-d/9.4)                      # first(14) ~ 0.77
    iap = {k: iap_total*(one_off*first(k) + (1-one_off)*days[k]/days[365]) for k in days}
    ads = {k: days[k]*ad_day for k in days}
    ltv = {k: ads[k]+iap[k] for k in days}
    return dict(name=name, repeat=repeat, r=r, days=days, ad_day=ad_day, arppu=arppu, iap=iap, ads=ads, ltv=ltv, sc=sc)

def types_per_1000(m):
    sc = m['sc']; n = 1000
    payers = n*sc['conv']; non = n-payers
    watchers = non*sc['watch']; free = non-watchers
    spend = sc['spend_rep'] if m['repeat'] else sc['spend']
    ads_total = m['ads'][365]*n
    rows = [('Free, never watches an ad', free, 0.0),
            ('Ad watcher', watchers, ads_total/max(1, watchers))]
    for lab, mix, s in zip(('Small buyer (~$5)', 'Medium buyer (~$20)', 'Big fan ($50+)'), sc['mix'], spend):
        rows.append((lab, payers*mix, s*sc['net']))
    return rows

def monte_carlo(m, trials=4000, n=1000, seed=7):
    """Spread of IAP money from 1,000 installs: few buyers, so luck matters a lot."""
    rnd = random.Random(seed); sc = m['sc']; spend = sc['spend_rep'] if m['repeat'] else sc['spend']; out = []
    for _ in range(trials):
        k = sum(1 for _ in range(n) if rnd.random() < sc['conv'])
        tot = 0.0
        for _ in range(k):
            u = rnd.random(); i = 0 if u < sc['mix'][0] else 1 if u < sc['mix'][0]+sc['mix'][1] else 2
            tot += spend[i]*math.exp(rnd.gauss(-0.18, 0.6))*sc['net']   # lognormal around the type average
        out.append(tot)
    out.sort(); q = lambda p: out[int(p*(len(out)-1))]
    return dict(p10=q(0.10), p50=q(0.50), p90=q(0.90))

def monthly(m, per_day):
    """Steady state after a year of the same installs per day."""
    dau = per_day*m['days'][365]
    rev = per_day*30*m['ltv'][365]
    return dict(installs_day=per_day, dau=round(dau), month=round(rev))

def report():
    res = {}
    for name in SCEN:
        for rep in (False, True):
            m = model(name, rep); key = name+('+repeat' if rep else '')
            res[key] = dict(
                active_days_per_install={k: round(v, 2) for k, v in m['days'].items()},
                ads_per_active_day=round(m['ad_day'], 4), arppu_gross=round(m['arppu'], 2),
                ltv={k: round(v, 3) for k, v in m['ltv'].items()},
                ads={k: round(v, 3) for k, v in m['ads'].items()}, iap={k: round(v, 3) for k, v in m['iap'].items()},
                per1000=[(a, round(b, 1), round(c, 2), round(b*c)) for a, b, c in types_per_1000(m)],
                iap_spread_per1000={k: round(v) for k, v in monte_carlo(m).items()},
                months=[monthly(m, x) for x in (50, 300, 1000)])
    # what moves money most (conservative + repeat buys, LTV at 1 year)
    base = model('conservative', True)['ltv'][365]
    levers = {
      'D1 +8 pts (22->30%), D7 4->6%, D30 1.2->1.8%': dict(d1=0.30, d7=0.06, d30=0.018),
      'Ads seen per day 1.2->2.0': dict(views=2.0),
      'Buyers 1.0%->2.0% of installs': dict(conv=0.02),
      'eCPM $7->$10 (more US/UK/iOS players)': dict(ecpm=10.0),
    }
    res['levers'] = {k: round(model('conservative', True, v)['ltv'][365]/base-1, 3) for k, v in levers.items()}
    res['levers']['Repeat buys (passes, packs, offers) vs one-offs only'] = round(base/model('conservative', False)['ltv'][365]-1, 3)
    # what it takes to pay for installs: LTV at 1 year vs typical casual CPI
    res['breakeven'] = {k: round(v['ltv'][365], 2) for k, v in res.items() if isinstance(v, dict) and 'ltv' in v}
    res['levers_base_ltv365'] = round(base, 3)
    return res

if __name__ == '__main__':
    out = report()
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/sim/money_out.json', 'w'), indent=1)
    for k, v in out.items():
        if not (isinstance(v, dict) and 'ltv' in v): print(k, v); continue
        print(f"\n== {k}: active days/install {v['active_days_per_install']}  ARPPU ${v['arppu_gross']}")
        print('   LTV', v['ltv'], ' ads', v['ads'], ' iap', v['iap'])
        for row in v['per1000']: print('   ', row)
        print('   IAP per 1,000 installs p10/p50/p90', v['iap_spread_per1000'])
        print('   months', v['months'])
