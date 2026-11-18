"""New Winter speed check (Nov 18): winter 1 to the New Winter gate (300 of 360 stars), then winter 2 with the frost
stars it earns (+10% coins each; frost = 5 + floor(sqrt(coins earned in the winter / 1e6))), starting from the shovel
(goldFor(2) = 0). Shipped ladder (ladder3_keepsuper_wide). Winter 2 shown with this winter's skill and with a player who
already knows every job (first tries as good as their best)."""
import sys, os, math, statistics as st; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ladder4 as L
loader = dict(name='FRONT LOADER', cost=2.5e6, width=52, speed=80, value=7.5)
ice = dict(name='ICEBREAKER', cost=1.8e8, width=62, speed=132, value=18)
for t in L.GAME_TOOLS:
    if t['id'] == 'snowcat': t['cost'] = 6.5e6
    if t['id'] == 'rotary': t['cost'] = 18e6
caps = {'snowcat': (max(1.06, 0.97 * 104 / 92), 1.25, 18e6), 'rotary': (1.15, 1.25, 72e6), 'loader': (1.08, 1.06, 6.5e6), 'super': (1.15, 1.30, 6.5e6)}
S = int(sys.argv[1]) if len(sys.argv) > 1 else 4
def summary(label, R):
    m = lambda f: st.mean(f(r) for r in R)
    print('%-34s %4.0f runs (%.1f h)  stars %3.0f  earned %.2e  machines %s' % (label, m(lambda r: r['runs']), m(lambda r: r['runs']) * 1.5 / 60, m(lambda r: r['stars']), m(lambda r: r['earned']),
          {k: round(st.mean(r['ev'][k] for r in R if k in r['ev'])) for k in ['super', 'loader', 'snowcat', 'rotary', 'icebreaker'] if any(k in r['ev'] for r in R)}))
W1, _ = L.go(loader, ice, caps=caps, seeds=S, stopStars=300)
summary('winter 1 to 300 stars', W1)
frost = 5 + math.floor(math.sqrt(st.mean(r['earned'] for r in W1) / 1e6)); mult = 1 + 0.10 * frost
print('frost stars after winter 1: %d -> coins x%.1f' % (frost, mult))
W2, _ = L.go(loader, ice, caps=caps, seeds=S, stopStars=300, coinMult=mult)
summary('winter 2, same skill', W2)
W2s, _ = L.go(loader, ice, caps=caps, seeds=S, stopStars=300, coinMult=mult, effFirst=0.62, effGain=0.0)
summary('winter 2, knows the jobs', W2s)
w1 = st.mean(r['runs'] for r in W1)
print('winter 2 / winter 1: same skill %.0f%%, knows the jobs %.0f%%' % (100 * st.mean(r['runs'] for r in W2) / w1, 100 * st.mean(r['runs'] for r in W2s) / w1))
