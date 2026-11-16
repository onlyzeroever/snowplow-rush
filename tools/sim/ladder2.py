import ladder as L, statistics as st, sys
def run(prices, seeds=6):
    L.NEW['titan']['cost'], L.NEW['icebreaker']['cost'] = prices
    R, ids = L.go(True, seeds=seeds, rides=False)
    return R
def show(label, R):
    print(label)
    print('  winter 1 in %.0f runs (~%.1f h); North %.0f runs, %.0f replays; longest stretch with no new machine %.0f runs' % (
        st.mean(r['runs'] for r in R), st.mean(r['runs'] for r in R) * 1.5 / 60, st.mean(r['north'] for r in R), st.mean(r['rep'] for r in R), st.mean(r['maxgap'] for r in R)))
    print('  areas', {a: round(st.mean(r['areas'][a] for r in R)) for a in L.e.AREA_SEQ})
    print('  machines', {m: round(st.mean(r['ev'][m] for r in R if m in r['ev'])) for m in ['super','loader','snowcat','rotary','titan','icebreaker'] if any(m in r['ev'] for r in R)})
base, _ = L.go(False, seeds=6, rides=False); show('TODAY, regular machines only', base)
for pr in [(3.5e7, 9e7), (3e7, 7e7), (2.6e7, 5.5e7)]:
    show('NEW: Titan %.0fM, Icebreaker %.0fM' % (pr[0] / 1e6, pr[1] / 1e6), run(pr))
