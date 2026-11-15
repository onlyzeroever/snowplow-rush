import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# Prop audit (Nov 16): props drawn on top of each other. Found by scanning every job for sprites whose opaque
# pixels overlap (tools/audit/overlap.js); each clash moved the smallest distance to a clear spot, then re-checked.
MOVES=[["cornershop", 3, "crate", [50, 44], [46, 50]], ["cornershop", 4, "crate", [50, 30], [30, 50]], ["allotments", 44, "lamp", [66, 150], [69, 150]], ["allotments", 46, "lamp", [66, 550], [71, 550]], ["highst", 49, "planter", [124, 120], [115, 120]], ["highst", 47, "phonebox", [126, 410], [122, 410]], ["highst", 50, "planter", [124, 700], [120, 700]], ["highst", 40, "bollard", [50, 180], [54, 180]], ["highst", 28, "lamp", [46, 180], [46, 165]], ["sledhill", 4, "lamp", [40, 650], [43, 650]], ["fountainsq", 13, "planter", [20, 728], [20, 725]], ["milkshed", 26, "oak", [10, 380], [0, 381]], ["treefarm", 2, "signpost", [150, 120], [150, 115]], ["cityhall", 4, "bikerack", [30, 1846], [30, 1850]], ["cityhall", 19, "tlight", [6, 1818], [6, 1803]], ["cityhall", 36, "lamp", [3, 1463], [3, 1490]], ["cityhall", 41, "lamp", [170, 1184], [170, 1210]], ["cityhall", 72, "planterl", [0, 760], [0, 744]], ["lake", 6, "bench", [4, 1000], [4, 995]], ["fishmarket", 10, "mooring", [117, 1003], [121, 1003]], ["fishmarket", 13, "mooring", [117, 1300], [121, 1300]], ["containers", 62, "nets", [156, 576], [156, 592]], ["containers", 66, "bins", [160, 808], [160, 804]], ["containers", 79, "pots", [158, 1703], [158, 1712]], ["drawbridge", 54, "mooring", [127, 2034], [131, 2034]], ["icebreaker", 23, "lifering", [166, 706], [166, 716]], ["skischool", 15, "lamp", [60, 3795], [63, 3795]], ["chalets", 49, "lantpost", [30, 627], [30, 634]], ["chalets", 51, "lantpost", [30, 2800], [30, 2806]], ["snowguns", 23, "snowpole", [148, 4283], [136, 4283]], ["terrain", 47, "deckchair", [22, 2352], [10, 2351]], ["rockfall", 17, "rock", [56, 3270], [64, 3270]], ["waterfall", 25, "signpost", [134, 1200], [134, 1210]], ["waterfall", 30, "cairn", [30, 3450], [30, 3460]], ["cliffroad", 75, "warnsign", [20, 6330], [10, 6330]], ["research", 19, "barrel", [160, 1693], [164, 1693]], ["research", 39, "barrel", [160, 3613], [164, 3613]], ["research", 59, "barrel", [160, 5533], [164, 5533]], ["snowmen", 35, "snowman", [146, 2470], [137, 2470]], ["gardens2", 30, "icesculpt", [18, 3680], [18, 3705]], ["gardens2", 33, "xmastree", [136, 3680], [136, 3706]], ["greathall", 44, "table", [142, 3520], [142, 3524]], ["greathall", 48, "table", [142, 4640], [142, 4629]], ["greathall", 50, "table", [12, 5440], [12, 5444]], ["greathall", 53, "table", [142, 5808], [142, 5828]], ["icepalace", 18, "xmastree", [8, 4200], [19, 4200]], ["icepalace", 19, "xmastree", [140, 4375], [129, 4375]], ["icepalace", 20, "xmastree", [8, 5250], [19, 5250]], ["icepalace", 21, "xmastree", [140, 5425], [129, 5425]], ["icepalace", 64, "sleigh", [10, 1050], [18, 1050]], ["containers", 71, "crate", [164, 1120], [164, 1162]], ["containers", 88, "bench", [166, 2238], [166, 2280]], ["containers", 93, "fishbox", [164, 2522], [164, 2562]], ["lift", 28, "snowpole", [145, 2504], [134, 2504]]]
def blob(name):
    i=s.index('const '+name+'=')+len('const '+name+'=');o,e=json.JSONDecoder().raw_decode(s,i);assert json.dumps(o,separators=(',',':'),ensure_ascii=False)==s[i:e];return o,i,e
def put(o,i,e):
    global s;s=s[:i]+json.dumps(o,separators=(',',':'),ensure_ascii=False)+s[e:]
n=0
sub,si,se=blob('SUB_DATA')
for lv,pi,pid,fr,to in MOVES:
    if lv in sub:
        p=sub[lv]['props'][pi];assert p[0]==pid and p[1:3]==fr,(lv,pi,p);p[1],p[2]=to;n+=1
put(sub,si,se)
packs,pi_,pe=blob('AREA_PACKS')
jobs={jb['id']:jb for pk in packs for jb in pk['jobs']}
for lv,pi,pid,fr,to in MOVES:
    if lv in jobs:
        p=jobs[lv]['data']['props'][pi];assert p[0]==pid and p[1:3]==fr,(lv,pi,p);p[1],p[2]=to;n+=1
assert n==len(MOVES),(n,len(MOVES))
# farm shop: a parked car prop sat exactly under the car that pulls out, so two cars were drawn in one spot
fc=jobs['farmcafe']['data']['props'];assert fc[8][:3]==['car',154,552],fc[8];del fc[8]
# palace gates: the gate pillars stood behind the wall they cap; step them forward so they are drawn in front
pg=jobs['palacegates']['data']['props'];walls={(p[1],p[2]) for p in pg if p[0]=='icewall'};k=0
for p in pg:
    if p[0]=='icecol' and p[1]==4 and (0,p[2]+32) in walls:p[2]+=8;k+=1
assert k==7,k
put(packs,pi_,pe)
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:70],s.count(a));s=s.replace(a,b_)
# railway track is ground: draw it under the trains, wagons and buffers that stand on it (they were hidden under the rails)
rep("track:{arg:200,","track:{flat:1,arg:200,")
rep("o=ob(P2.make(a),p[1],p[2],f2[0],f2[1],f2[2],f2[3]);if(P2.junk)o.junk=true;","o=ob(P2.make(a),p[1],p[2],f2[0],f2[1],f2[2],f2[3]);if(P2.junk)o.junk=true;if(P2.flat)o.base=o.y-4000;")
# free-space helpers for hand-built jobs (bounding box of the frosted sprite, with a margin) + cutting runs around buildings
rep("const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,sx,sy:sy-(fz.padTop||0),x:sx+fx,y:sy+fy,w:fw,h:fh};o.base=o.y+o.h;g.obstacles.push(o);return o;};",
 "const ob=(sprC,sx,sy,fx,fy,fw,fh)=>{const fz=frostOf(sprC),o={spr:fz,sx,sy:sy-(fz.padTop||0),x:sx+fx,y:sy+fy,w:fw,h:fh};o.base=o.y+o.h;g.obstacles.push(o);return o;};\n"
 "  const fits=(sprC,sx,sy,m=2)=>{const fz=frostOf(sprC),hh=fz.height-(fz.padTop||0);return !g.obstacles.some(o=>{const oy=o.sy+(o.spr.padTop||0);return o.sx<sx+fz.width+m&&sx-m<o.sx+o.spr.width&&oy<sy+hh+m&&sy-m<o.sy+o.spr.height;});};\n"
 "  const cutSegs=(x,w,a0,a1,rects,gapT,gapB,minL)=>{let segs=[[a0,a1]];for(const [bx,by,bw,bh] of rects){if(x+w<=bx||x>=bx+bw)continue;const t=by-gapT,u=by+bh+gapB;segs=segs.flatMap(([a,c])=>c<=t||a>=u?[[a,c]]:[[a,Math.min(c,t)],[Math.max(a,u),c]].filter(([p,q])=>q-p>=minL));}return segs;};")
# maple street: a pine was planted inside the last house; move it to the open gap further up the street
rep("[150,700-30,22],[4,660,24]]","[150,534,22],[4,660,24]]")
# country lane: hedges ran straight through the farmhouse and into the barn
rep("for(let y=0;y<ph;y+=150){ob(hedgeSprite(12,120),2,y,0,0,12,120);ob(hedgeSprite(12,120),166,y+60,0,0,12,120);}\n    ob(smallHouseSprite('#f4f8ff','#c6d9f3','#7a4a2a'),130,200,0,0,44,48);ob(barnSprite(),2,520,0,0,64,50);",
 "const blds=[[130,200,44,48],[2,520,64,50]];ob(smallHouseSprite('#f4f8ff','#c6d9f3','#7a4a2a'),130,200,0,0,44,48);ob(barnSprite(),2,520,0,0,64,50);\n    for(let y=0;y<ph;y+=150){for(const [x,y0] of [[2,y],[166,y+60]])for(const [a,c] of cutSegs(x,12,y0,y0+120,blds,8,10,16))ob(hedgeSprite(12,c-a),x,a,0,0,12,c-a);}")
# farmyard + moonlit ranch: fences ran into barns, hay bales were dropped on top of fences
rep("for(let y=200;y<ph-100;y+=200){for(const x of [40,136]){if(hash(x,y)%5===0)continue;ob(fenceSprite(150),x,y,0,0,12,150);}}\n    for(let y=500;y<ph-100;y+=600){const side=(y/600|0)%2;ob(barnSprite(),side?110:6,y,0,0,64,50);ob(siloSprite(),side?86:74,y+6,1,1,21,21);}\n    for(let k=0;k<(big?26:10);k++){const x=10+hash(k,7)%150,y=150+hash(k,11)%(ph-250);if(x>70&&x<110)continue;ob(HAY,x,y,0,2,12,6);}",
 "const barns=[];for(let y=500;y<ph-100;y+=600){const side=(y/600|0)%2;barns.push([side?110:6,y,64,50]);}\n    for(let y=200;y<ph-100;y+=200){for(const x of [40,136]){if(hash(x,y)%5===0)continue;for(const [a,c] of cutSegs(x,12,y,y+150,barns,8,10,20))ob(fenceSprite(c-a),x,a,0,0,12,c-a);}}\n    for(const [bx,by] of barns){const side=bx>50;ob(barnSprite(),bx,by,0,0,64,50);ob(siloSprite(),side?86:74,by+6,1,1,21,21);}\n    for(let k=0;k<(big?26:10);k++){const x0=10+hash(k,7)%150,y=150+hash(k,11)%(ph-250);if(x0>70&&x0<110)continue;for(const dx of [0,16,-16,30,-30]){const x=x0+dx;if(x<2||x>166||(x>66&&x<110))continue;if(fits(HAY,x,y)){ob(HAY,x,y,0,2,12,6);break;}}}")
# holiday retreat: pines stood in front of cabin windows
rep("for(let y=80;y<ph;y+=70){ob(pineSprite(22),side2(y)?2:156,y,4,14,9,7);}",
 "for(let y=80;y<ph;y+=70){const x=side2(y)?2:156,ps=pineSprite(22);for(const dy of [0,-22,22,-40,40])if(fits(ps,x,y+dy)){ob(ps,x,y+dy,4,14,9,7);break;}}")
# the mansion: parked cars were dropped on the hedges; park them in the gaps between the hedge rows
rep("for(let y=300;y<ph-600;y+=400){ob(carSprite('#2a2a36','#1b1f3b'),10,y,1,2,22,28);ob(carSprite('#d8364b','#9c2a45'),148,y+100,1,2,22,28);}",
 "for(let y=300;y<ph-600;y+=400){const yl=120+90*Math.floor((y-120)/90)+36,yr=160+90*Math.floor((y+100-160)/90)+36,cl=carSprite('#2a2a36','#1b1f3b'),cr=carSprite('#d8364b','#9c2a45');if(fits(cl,10,yl))ob(cl,10,yl,1,2,22,28);if(fits(cr,148,yr))ob(cr,148,yr,1,2,22,28);}")
# junkyard: tyres and barrels were scattered on top of each other
rep("if(x>70&&x<106)continue;const o=ob(k%2?TIRES:BARREL,x,y,1,3,k%2?9:6,k%2?6:6);}","if(x>70&&x<106)continue;if(!fits(k%2?TIRES:BARREL,x,y,1))continue;const o=ob(k%2?TIRES:BARREL,x,y,1,3,k%2?9:6,k%2?6:6);}")
# mountain castle: corner towers sat behind the outer wall; the wall now stops at each tower
rep("for(let y=40;y<ph;y+=300){const hh=Math.min(300,ph-y);ob(wallSprite(14,hh),0,y,0,0,14,hh);ob(wallSprite(14,hh),166,y,0,0,14,hh);}",
 "{const cuts={0:[],166:[]};for(let y=700;y<ph-200;y+=760){const gx=[30,66,102][(y/760|0)%3];if(gx-28<14)cuts[0].push([0,y-6,14,34]);if(gx+78>166)cuts[166].push([166,y-6,14,34]);}\n    for(const wx of [0,166])for(let y=40;y<ph;y+=300){const hh=Math.min(300,ph-y);for(const [a,c] of cutSegs(wx,14,y,y+hh,cuts[wx],0,0,8))ob(wallSprite(14,c-a),wx,a,0,0,14,c-a);}}")
open(f,'w',encoding='utf-8').write(s)
print('p96 declutter:',len(MOVES),'prop moves + hand-built job fixes')
