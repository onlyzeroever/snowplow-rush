import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def blob(name):
    i=s.index('const '+name+'=')+len('const '+name+'=');o,e=json.JSONDecoder().raw_decode(s,i);assert json.dumps(o,separators=(',',':'),ensure_ascii=False)==s[i:e];return o,i,e
def put(o,i,e):
    global s;s=s[:i]+json.dumps(o,separators=(',',':'),ensure_ascii=False)+s[e:]
def mv(props,idx,pid,old,new):
    p=props[idx];assert p[0]==pid and p[1:3]==old,(pid,idx,p);p[1],p[2]=new
# Leftover pockets (Nov 16, part 2): the remaining spots where the bigger machines missed 1%+ more snow than the shovel.
sub,si,se=blob('SUB_DATA')
tp=sub['tennis']['props'];mv(tp,6,'pine',[2,4],[2,-12]);mv(tp,7,'pine',[152,6],[152,-12])          # corner pines up against the top edge
sl=sub['sledhill']['props'];mv(sl,0,'stall',[4,640],[0,640]);mv(sl,1,'kiosk',[156,646],[162,646])  # stall and kiosk flush to the edges
put(sub,si,se)
packs,pi_,pe=blob('AREA_PACKS');jobs={jb['id']:jb for pk in packs for jb in pk['jobs']}
np_=jobs['northpole']['data']['props'];mv(np_,0,'big',[35,64],[35,8])                                # the post office up at the end of the road
mv(np_,1,'xmastree',[4,96],[2,22]);mv(np_,2,'xmastree',[144,96],[146,22])                           # trees in the gaps beside it, not in front
ss=jobs['snowshoe']['data']['props'];mv(ss,10,'cabin',[68,128],[68,4])                             # the cabin closes the end of the trail
mh=jobs['mhut']['data']['props'];mv(mh,23,'big',[0,51],[0,8]);mv(mh,24,'flag',[124,51],[114,40]);mv(mh,25,'flag',[150,51],[128,40])
tf=jobs['treefarm']['data']['props'];mv(tf,4,'tractor',[20,386],[0,386]);mv(tf,5,'trailer',[140,618],[158,618])
hf=jobs['harvestfair']['data']['props']                                                             # arena rails 10px in from the edges, like the bumper rink
for k,pid,old,new,ln in [(29,'rail',[14,470],[4,470],58),(30,'rail',[116,470],[118,470],58),(31,'rail',[14,883],[4,883],58),(32,'rail',[116,883],[118,883],58),(33,'railv',[14,477],[4,477],None),(34,'railv',[161,477],[171,477],None)]:
    mv(hf,k,pid,old,new)
    if ln:hf[k][3]=ln
# Main Street: alleys between shops were 1-29px, too narrow for big machines and too wide to look like a party wall.
# Each run of shops is re-spaced: a gap under 20px closes (terraced shops), a gap of 20-31px opens to a 32px alley.
ms=jobs['mainst']['data']['scen'];HT={'shopv':72,'shop':60}
for side in (0,1):
    idx=sorted([i for i,b in enumerate(ms) if (b[1]<90)==(side==0) and b[0] in HT],key=lambda i:ms[i][2]);prev=None
    for i in idx:
        b=ms[i]
        if prev is not None:
            pe2=ms[prev][2]+HT[ms[prev][0]];g=b[2]-pe2
            if g<200:b[2]=pe2+(0 if g<20 else max(32,g))
        prev=i
put(packs,pi_,pe)
open(f,'w',encoding='utf-8').write(s)
print('p112 leftover pockets')
