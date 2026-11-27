# Corner Shop: the two grandmas live in the houses either side of the shop (tester, Nov 27: "these grannies might be in
# the wrong place, they want paths clearing and live very top of map"). They stood halfway down the car park pavements
# and, once their path was clear, walked up through lampposts, the bins and the phone box to the shop. Now each one
# waits at her own front door at the top and asks for the pavement in front of the shops; when it is clear she walks
# round the crates / phone box / bins (never through a prop) and in at the shop door. Left: door x 24-36 -> under the
# crates (feet at y 78) -> shop door x 98. Right: door x 161-172 -> above the phone box (y 64) -> x 140 -> y 78 ->
# shop door x 112 (they finish side by side, not on top of each other). Live web game, app and lab.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep('"neighbours":[{"rects":[[8,84,12,128],[8,78,76,12]],"path":[[14,210],[14,84],[84,84]]},{"rects":[[160,84,12,236],[96,78,76,12]],"path":[[166,318],[166,84],[96,84]]}]',
    '"neighbours":[{"rects":[[16,48,96,36]],"path":[[24,50],[24,78],[98,78],[98,60]]},{"rects":[[100,48,78,36]],"path":[[166,50],[166,64],[140,64],[140,78],[112,78],[112,60]]}]')
open(f,'w',encoding='utf-8').write(s)
