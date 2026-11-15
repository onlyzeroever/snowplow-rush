import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# The original 18 jobs get the pro look on top of their hand-built layout: paving instead of plain concrete, painted
# ground detail and overhead lights/banners. Nothing that blocks; layout, size and difficulty are unchanged.
OP=json.load(open('/home/claude/levels/orig_pro.json'))
rep("const BASE_LEVELS=18;","const BASE_LEVELS=18;\nconst ORIG_PRO="+json.dumps(OP,separators=(',',':'))+";\nfor(const L of LEVELS)if(ORIG_PRO[L.id])L.pro=ORIG_PRO[L.id];")
rep("\n  g.driveKey=null;{const ri=nextRideIdx();","""
  if(L.pro&&!L.data){const Q=L.pro;if(Q.remap&&GROUND_T[Q.remap]!=null){const to=GROUND_T[Q.remap];for(let i=0;i<g.type.length;i++)if(g.type[i]===T_CONC)g.type[i]=to;}
    g.decals=(g.decals||[]).concat(Q.decals||[]);for(const p of Q.over||[]){const f=OVERS[p[0]];if(f)g.over.push({spr:f(p[3],p[4]),sx:p[1],sy:p[2]});}}
  g.driveKey=null;{const ri=nextRideIdx();""")
open(f,'w',encoding='utf-8').write(s)
