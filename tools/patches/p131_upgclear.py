import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Clearer upgrades (Alex, Nov 18). A tester thought swapping machines wiped upgrades; the data shows it never does
# (319 buys, no level ever bought twice). New machines simply start fresh. Say so on screen:
# - the bar under UPGRADES names the machine they belong to ("PLOW TRUCK UPGRADES", or "...: FRESH UPGRADES" while all
#   three are still at level 0), as rides already did;
# (the machine rows already carry the machine's name; snow value and helpers don't, as they're shared)
rep("R(b,8,36,164,9,'rgba(19,48,107,0.85)');text(b,t,W/2,37,'#ffd23f',{align:'center',outline:null});}}",
    "R(b,8,36,164,9,'rgba(19,48,107,0.85)');text(b,t,W/2,37,'#ffd23f',{align:'center',outline:null});}\n"
    "    else{const m=TOOLS[u],mn=SHORT_NAME[m.id]||m.name,ml=mLv(m.id),fresh=save.tool>0&&!ml.speed&&!ml.size&&!ml.bumper;let t=mn+(fresh?': FRESH UPGRADES':' UPGRADES');if(textW(t)>164)t=fresh?'NEW MACHINE: FRESH UPGRADES':'THIS MACHINE\\'S UPGRADES';"
    "R(b,8,36,164,9,'rgba(19,48,107,0.85)');text(b,t,W/2,37,fresh?'#7fe08a':'#ffd23f',{align:'center',outline:null});}}")
open(f,'w',encoding='utf-8').write(s)
print('p131 upgrades screen names the machine they belong to, and says FRESH UPGRADES for a new one')
