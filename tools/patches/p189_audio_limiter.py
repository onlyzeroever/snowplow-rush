# A limiter on the master output, and a slightly quieter coin (tester review, Nov 26, check 31: "coins maybe slight but
# tinny at higher volumes"). Nothing stopped the engine, scrape, crunch, combo and coin sounds from adding up past full
# scale, so at high phone volume the peaks clipped and sounded harsh. The coin sample is all 1-6 kHz (no body), the
# range phone speakers push hardest. Pros put a limiter on the master bus: master -> limiter -> speakers. Falls back to
# the old direct connection if the browser has no DynamicsCompressor. Coin 0.32 -> 0.27 (about -1.5 dB).
# Live web game, app and lab.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("master=AC.createGain();master.gain.value=0.9;master.connect(AC.destination);",
    "master=AC.createGain();master.gain.value=0.9;"
    "try{const lim=AC.createDynamicsCompressor();lim.threshold.value=-9;lim.knee.value=6;lim.ratio.value=12;"
    "lim.attack.value=0.003;lim.release.value=0.2;master.connect(lim);lim.connect(AC.destination);}"
    "catch(e){master.connect(AC.destination);}")
rep("coin:0.32,", "coin:0.27,")
open(f,'w',encoding='utf-8').write(s)
