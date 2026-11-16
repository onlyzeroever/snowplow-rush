import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
def blob(name):
    i=s.index('const '+name+'=')+len('const '+name+'=');o,e=json.JSONDecoder().raw_decode(s,i);assert json.dumps(o,separators=(',',':'),ensure_ascii=False)==s[i:e];return o,i,e
def put(o,i,e):
    global s;s=s[:i]+json.dumps(o,separators=(',',':'),ensure_ascii=False)+s[e:]
def mv(props,idx,pid,old,new):
    p=props[idx];assert p[0]==pid and p[1:3]==old,(pid,idx,p);p[1],p[2]=new
# More room for the big machines (Nov 16). A reach scan of every job x every machine found the layouts where big
# machines were shut out of a pocket the small ones could clear. These moves open them without changing the jobs.
sub,si,se=blob('SUB_DATA')
cs=sub['cornershop']['props']
mv(cs,29,'mailbox',[52,532],[43,538]); mv(cs,30,'mailbox',[122,532],[128,538])   # mailboxes at the hedge ends: the lane under the houses is open
mv(cs,34,'pine',[4,566],[0,572]); mv(cs,35,'pine',[152,566],[161,572])          # pines tucked into the corners
mv(cs,6,'phonebox',[150,70],[165,70]); mv(cs,37,'bins',[156,96],[160,96])        # phone box and bins against the kerb
for k,old,new in [(1,[4,0],[0,0]),(2,[132,0],[136,0]),(23,[4,470],[0,470]),(24,[132,470],[136,470])]:mv(cs,k,'smallhouse',old,new)  # houses flush to the edges: no 4px slivers
mv(cs,5,'trash',[128,50],[122,50])
assert cs[36][:3]==['pine',110,572];del cs[36]   # the pine beside the start sealed the bottom lane
hs=sub['highst']['props']   # bins stand against the back wall of each alley instead of in the middle of it
for k,old,new in [(2,[4,150],[0,150]),(3,[33,150],[0,165]),(7,[4,402],[0,402]),(8,[33,402],[0,417]),(16,[140,224],[173,224]),(17,[169,224],[173,239]),(21,[140,476],[173,476]),(22,[169,476],[173,491])]:mv(hs,k,'trash',old,new)
tp=sub['tennis']['props'];mv(tp,1,'planter',[10,64],[36,64]);mv(tp,2,'planter',[156,64],[130,64])   # planters frame the clubhouse instead of plugging the side lanes
put(sub,si,se)
packs,pi_,pe=blob('AREA_PACKS');jobs={jb['id']:jb for pk in packs for jb in pk['jobs']}
fc=jobs['farmcafe']['data'];k=[k for k,p in enumerate(fc['props']) if p[0]=='well'][0];mv(fc['props'],k,'well',[82,1440],[82,1478])  # well out of the hedge slalom's exit
for w in fc['wilds']:
    assert w[0]=='bush' and w[4]==14;w[4]=12   # slalom hedges a touch slimmer, so the gaps between them fit the widest machines
put(packs,pi_,pe)
# Gardens (hand-built): the swing and two gnomes narrowed the left lane below a big machine's width
rep("ob(swingSprite(),20,130,0,0,26,14);ob(SPR.gnome,60,160,1,8,7,5);ob(SPR.gnome,120,250,1,8,7,5);ob(SPR.gnome,30,250,1,8,7,5);",
    "ob(swingSprite(),44,130,0,0,26,14);ob(SPR.gnome,64,166,1,8,7,5);ob(SPR.gnome,120,250,1,8,7,5);ob(SPR.gnome,42,266,1,8,7,5);")
rep("ob(houseSprite(),6,0,0,0,80,60);ob(smallHouseSprite('#a8673a','#7a4a2a','#6b3f22'),132,10,0,0,44,48);",
    "ob(houseSprite(),0,0,0,0,80,60);ob(smallHouseSprite('#a8673a','#7a4a2a','#6b3f22'),136,0,0,0,44,48);")
rep("ob(tubSprite(),136,124,1,1,14,14);","ob(tubSprite(),120,136,1,1,14,14);")

sub,si,se=blob('SUB_DATA')
al=sub['allotments']['props']   # lamps and gnomes stood in the mouths of the lanes between the plot rows
mv(al,44,'lamp',[69,150],[72,138]);mv(al,46,'lamp',[71,550],[72,532]);mv(al,10,'gnome',[34,266],[34,250]);mv(al,43,'gnome',[138,566],[137,546])
put(sub,si,se)
packs,pi_,pe=blob('AREA_PACKS');jobs={jb['id']:jb for pk in packs for jb in pk['jobs']}
lf=jobs['lift']['data']   # lift pylons (and the cable above them) 3px right: the widest machines now fit past them on the left
for k,p in enumerate(lf['props']):
    if p[0]=='pylon':mv(lf['props'],k,'pylon',[143,p[2]],[146,p[2]])
assert lf['over'][0][:2]==['liftline',135];lf['over'][0][1]=138
ch=jobs['cityhall']['data'];assert ch['scen'][9][:3]==['big',35,22];ch['scen'][9][2]=8   # city hall nearer the top edge: no strip above the roof that only small machines fit
mv(ch['props'],78,'planter',[4,40],[38,68]);mv(ch['props'],79,'planter',[164,40],[128,68])   # planters flank the door instead of sealing the side lanes
put(packs,pi_,pe)
# Cul-de-sac (hand-built): the three houses at the top left 24px alleys; the side houses sit 4px past the edges so they are 28px
rep("ob(smallHouseSprite(...walls[0]),0,6,0,0,44,48);ob(smallHouseSprite(...walls[1]),68,0,0,0,44,48);ob(smallHouseSprite(...walls[2]),136,6,0,0,44,48);",
    "ob(smallHouseSprite(...walls[0]),-4,0,0,0,44,48);ob(smallHouseSprite(...walls[1]),68,0,0,0,44,48);ob(smallHouseSprite(...walls[2]),140,0,0,0,44,48);")
open(f,'w',encoding='utf-8').write(s)
print('p109 room for big machines')
