# Starter Pack clock that visibly ticks (tester review, Nov 26, check 17: "shows with number but doesn't count down").
# The pop-up said "FOR THE NEXT 48 HOURS" (fixed text) and the shop card "ENDS IN 47H 59M" (changes once a minute),
# so a real 48-hour offer looked frozen. Both now show the live time left with seconds (ENDS IN 47:59:12). The offer
# really does end 48 hours after it first appears and never comes back on the same terms (honest-price rule).
# HELD from the live web game (the Starter Pack is app-only, p173); in the app and the lab.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function fmtLeft(ms){",
    "function fmtClock(ms){const t=Math.max(0,Math.ceil(ms/1000)),h=Math.floor(t/3600),m=Math.floor(t/60)%60,x=t%60;"
    "return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(x).padStart(2,'0');}\nfunction fmtLeft(ms){")
rep("text(b,'ENDS IN '+fmtLeft(stL),17,y+31,'#e8283f',{outline:null});",
    "text(b,'ENDS IN '+fmtClock(stL),17,y+31,'#e8283f',{outline:null});")
rep("text(b,'FOR THE NEXT 48 HOURS',W/2,y+101,'#9fc0e8',{align:'center',outline:null});",
    "text(b,'ENDS IN '+fmtClock(starterLeft()||STARTER_MS),W/2,y+101,'#ffd23f',{align:'center',outline:null});")
open(f,'w',encoding='utf-8').write(s)
