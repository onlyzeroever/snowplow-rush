import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# SUBURBS KIT: everything the 9 new Suburbs jobs need, as data-level building blocks.
#  - new props: railings, tennis net, kennel, shed, greenhouse, raised beds, scarecrow, playground kit,
#    dog agility, phone box, bus stop, post box, party tables, BBQ, stage, speakers, planters, round trees,
#    bollards, shop fronts
#  - new hazards: ball machine (fires tennis balls across a court, with a 0.75s aim line first) and
#    snow cannon (sprays fresh snow over ground you've cleared; plow into it to jam it for 9s)
#  - walkers that cross sideways, traffic lanes (cars and the bus), cars that pull out, neighbours,
#    painted ground text, circles, bunting, faster sled crossings
#  - the boss gate: Block Party needs 25 stars from the other Suburbs jobs
# ---------------------------------------------------------------------------------------------
KIT=r"""
function railSprite(w,h){const c=mk(w,h),g=c.getContext('2d');
  if(w>=h){R(g,0,1,w,2,K);R(g,0,5,w,1,K);R(g,0,2,w,1,'#2f6f8a');for(let x=0;x<w-1;x+=6){R(g,x,0,2,h,K);}R(g,w-2,0,2,h,K);R(g,0,0,w,1,PAL.W);R(g,0,1,w,1,'#c6d9f3');}
  else{R(g,0,0,w,h,K);R(g,1,0,w-2,h,'#2f6f8a');for(let y=0;y<h-1;y+=6){R(g,0,y,w,2,K);R(g,1,y,w-2,1,'#5aa0c0');}R(g,1,0,1,h,PAL.W);R(g,0,h-2,w,2,K);}return c;}
function netSprite(w){const c=mk(w,8),g=c.getContext('2d');R(g,0,0,3,8,K);R(g,w-3,0,3,8,K);R(g,1,1,1,7,'#c6d9f3');R(g,w-2,1,1,7,'#c6d9f3');
  R(g,3,1,w-6,5,K);for(let x=3;x<w-3;x++)for(let y=2;y<5;y++)if((x+y)%2)R(g,x,y,1,1,'#8793a8');R(g,3,1,w-6,1,PAL.W);return c;}
function ballMachineSprite(d){const c=mk(12,12),g=c.getContext('2d');R(g,1,0,10,5,K);R(g,2,1,8,3,'#55607a');for(const [x,y] of [[3,1],[5,2],[7,1],[8,2],[4,3]])R(g,x,y,2,1,'#d7f03a');
  R(g,0,4,12,7,K);R(g,1,5,10,5,'#1f7a5c');R(g,1,5,10,1,'#33b24a');R(g,d>0?9:0,6,3,3,K);R(g,d>0?10:1,7,1,1,'#d7f03a');R(g,2,10,2,2,K);R(g,8,10,2,2,K);return c;}
function cannonSprite(ang){const c=mk(18,18),g=c.getContext('2d');R(g,3,14,2,4,K);R(g,13,14,2,4,K);R(g,8,13,2,5,K);
  g.fillStyle=K;pixCircle(g,9,9,6);g.fillStyle='#c6d9f3';pixCircle(g,9,9,5);g.fillStyle='#8793a8';pixCircle(g,9,9,3);R(g,8,6,2,6,K);R(g,6,8,6,2,K);
  const bx=Math.round(9+Math.cos(ang)*6),by=Math.round(9+Math.sin(ang)*6);R(g,bx-3,by-3,6,6,K);R(g,bx-2,by-2,4,4,'#3f86d6');R(g,5,3,8,1,PAL.W);return c;}
function kennelSprite(){const c=mk(18,16),g=c.getContext('2d');for(let r=0;r<6;r++){const ins=5-r;R(g,ins,r,18-ins*2,1,K);if(18-ins*2>2)R(g,ins+1,r,16-ins*2,1,r<2?PAL.W:'#d8364b');}
  R(g,0,6,18,1,K);R(g,1,7,16,9,K);R(g,2,7,14,8,'#c98d4a');for(let x=4;x<16;x+=3)R(g,x,7,1,8,'#a8673a');R(g,6,9,6,7,K);R(g,7,10,4,6,'#2a2a36');R(g,1,6,16,1,PAL.w);return c;}
function shedSprite(a){const w2=[['#8fbf5a','#5e8a3a'],['#3f86d6','#2a5fa8'],['#c98d4a','#8a5a2c']][a%3];const c=mk(28,26),g=c.getContext('2d');
  R(g,0,0,28,10,K);R(g,1,1,26,8,'#7a4a2a');R(g,1,1,26,5,PAL.W);R(g,1,6,26,1,PAL.w);R(g,1,10,26,16,K);R(g,2,10,24,15,w2[0]);for(let x=5;x<26;x+=4)R(g,x,10,1,15,w2[1]);
  R(g,11,13,7,13,K);R(g,12,14,5,12,'#a8673a');R(g,15,19,1,1,'#ffc727');R(g,3,13,6,6,K);R(g,4,14,4,4,'#8fd3ff');R(g,20,13,6,6,K);R(g,21,14,4,4,'#8fd3ff');return c;}
function greenhouseSprite(){const c=mk(30,22),g=c.getContext('2d');R(g,0,0,30,22,K);R(g,1,1,28,7,'#cfe9f7');R(g,1,1,28,4,PAL.W);R(g,1,8,28,13,'#9fd4f4');
  for(let x=1;x<29;x+=7)R(g,x,1,1,20,'#f4f8ff');R(g,1,8,28,1,'#f4f8ff');R(g,1,14,28,1,'#e8f6ff');for(const [x,y] of [[3,16],[9,17],[19,16],[24,17]])R(g,x,y,3,3,'#33b24a');R(g,12,11,6,10,K);R(g,13,12,4,9,'#cfe9f7');return c;}
function plotSprite(w){const c=mk(w,10),g=c.getContext('2d');R(g,0,0,w,10,K);R(g,1,1,w-2,8,'#8a5a34');R(g,1,1,w-2,1,'#c98d4a');R(g,1,8,w-2,1,'#55321d');R(g,2,3,w-4,4,'#4a3020');
  for(let x=3;x<w-4;x+=5){R(g,x,2,3,3,'#33b24a');R(g,x+1,2,1,1,PAL.W);}return c;}
function scarecrowSprite(){const c=mk(14,22),g=c.getContext('2d');R(g,6,10,2,12,K);R(g,0,9,14,2,K);R(g,1,9,12,1,'#a8673a');R(g,4,0,6,3,K);R(g,2,3,10,2,K);R(g,5,1,4,2,'#7a4a2a');R(g,3,3,8,1,'#7a4a2a');R(g,4,1,6,1,PAL.W);
  R(g,4,5,6,5,K);R(g,5,5,4,4,'#e8c87a');R(g,5,6,1,1,K);R(g,8,6,1,1,K);R(g,3,11,8,8,K);R(g,4,12,6,6,'#3f86d6');R(g,5,13,1,1,'#ffc727');R(g,8,15,1,1,'#ffc727');R(g,1,8,1,3,'#e8c87a');R(g,12,8,1,3,'#e8c87a');return c;}
function roundaboutSprite(){const c=mk(22,16),g=c.getContext('2d');g.fillStyle=K;for(let dy=-7;dy<=7;dy++){const dx=Math.round(11*Math.sqrt(Math.max(0,1-(dy/7.6)**2)));g.fillRect(11-dx,8+dy,dx*2,1);}
  const cols=['#d8364b','#ffc727','#3f86d6','#33b24a'];for(let dy=-6;dy<=6;dy++){const dx=Math.round(10*Math.sqrt(Math.max(0,1-(dy/6.6)**2)));for(let x=11-dx;x<11+dx;x++){const a=Math.atan2(dy*1.6,x-10.5);g.fillStyle=cols[(((a+Math.PI)/(Math.PI/2))|0)%4];g.fillRect(x,8+dy,1,1);}}
  g.fillStyle=PAL.W;for(let dy=-6;dy<=-3;dy++){const dx=Math.round(10*Math.sqrt(Math.max(0,1-(dy/6.6)**2)))-2;g.fillRect(11-dx,8+dy,dx*2,1);}R(g,10,1,2,8,K);R(g,4,3,14,2,K);R(g,5,3,12,1,'#c6d9f3');return c;}
function seesawSprite(){const c=mk(30,8),g=c.getContext('2d');R(g,0,2,30,4,K);R(g,1,3,28,2,'#d8364b');R(g,1,3,28,1,PAL.W);R(g,12,1,6,7,K);R(g,13,2,4,5,'#55607a');R(g,1,0,4,8,K);R(g,2,1,2,6,'#ffc727');R(g,25,0,4,8,K);R(g,26,1,2,6,'#ffc727');return c;}
function climbSprite(){const c=mk(24,22),g=c.getContext('2d');R(g,0,0,24,3,K);R(g,1,1,22,1,'#ffc727');R(g,0,0,24,1,PAL.W);for(const x of [0,22])R(g,x,0,2,22,K);for(let y=6;y<20;y+=5)R(g,1,y,22,1,K);
  for(let x=6;x<22;x+=5)R(g,x,3,1,16,'#3f86d6');R(g,0,19,24,3,K);R(g,1,20,22,1,'#3f86d6');return c;}
function sandpitSprite(){const c=mk(32,22),g=c.getContext('2d');R(g,0,0,32,22,K);R(g,1,1,30,20,'#c98d4a');R(g,1,1,30,2,PAL.W);R(g,4,4,24,14,K);R(g,5,5,22,12,'#f4f8ff');R(g,7,8,6,3,'#e8d9b0');R(g,16,12,6,2,'#e8d9b0');
  R(g,20,5,4,5,K);R(g,21,6,2,3,'#d8364b');R(g,9,13,3,2,'#3f86d6');return c;}
function hurdleSprite(){const c=mk(16,8),g=c.getContext('2d');R(g,0,0,3,8,K);R(g,13,0,3,8,K);R(g,1,1,1,7,'#f4f8ff');R(g,14,1,1,7,'#f4f8ff');R(g,3,2,10,3,K);for(let x=3;x<13;x+=4){R(g,x,3,2,1,'#d8364b');R(g,x+2,3,2,1,'#f4f8ff');}return c;}
function poleSprite(){const c=mk(4,12),g=c.getContext('2d');R(g,0,0,4,12,K);R(g,1,1,2,10,'#f4f8ff');R(g,1,3,2,2,'#d8364b');R(g,1,7,2,2,'#d8364b');return c;}
function phoneboxSprite(){const c=mk(12,24),g=c.getContext('2d');R(g,0,0,12,24,K);R(g,1,1,10,22,'#d8364b');R(g,1,1,10,2,PAL.W);R(g,2,4,8,2,K);R(g,3,4,6,1,'#f4f8ff');
  for(let y=7;y<20;y+=4){R(g,2,y,8,3,K);R(g,3,y,2,2,'#cfe9f7');R(g,7,y,2,2,'#cfe9f7');}R(g,1,21,10,2,'#a82639');return c;}
function busstopSprite(){const c=mk(30,20),g=c.getContext('2d');R(g,0,0,27,4,K);R(g,1,1,25,2,PAL.W);R(g,0,4,2,14,K);R(g,25,4,2,14,K);R(g,2,5,23,8,'#9fd4f4');R(g,2,5,23,1,'#d8f2ff');
  R(g,3,12,21,3,K);R(g,4,12,19,1,'#c98d4a');R(g,27,0,2,20,K);R(g,26,0,4,5,K);R(g,27,1,2,3,'#ffc727');return c;}
function postboxSprite(){const c=mk(8,14),g=c.getContext('2d');R(g,1,0,6,2,K);R(g,0,2,8,12,K);R(g,1,1,6,1,PAL.W);R(g,1,2,6,11,'#d8364b');R(g,1,2,6,1,PAL.W);R(g,2,5,4,1,K);R(g,3,8,2,2,'#ffc727');return c;}
function tableSprite(a){const cl=['#d8364b','#3f86d6','#33b24a','#9b5fd6'][a%4];const c=mk(26,12),g=c.getContext('2d');R(g,0,0,26,9,K);R(g,1,1,24,7,'#f4f8ff');
  for(let y=1;y<8;y+=2)for(let x=1+((y>>1)%2)*2;x<25;x+=4)R(g,x,y,2,2,cl);R(g,1,7,24,1,'#c6d9f3');R(g,2,9,2,3,K);R(g,22,9,2,3,K);
  R(g,4,2,5,3,K);R(g,5,2,3,2,'#ffc727');R(g,11,3,4,3,K);R(g,12,3,2,2,'#e07a8a');R(g,17,2,5,3,K);R(g,18,2,3,2,'#a8673a');return c;}
function bbqSprite(){const c=mk(12,12),g=c.getContext('2d');R(g,0,0,12,6,K);R(g,1,1,10,4,'#2a2a36');R(g,2,2,8,1,'#f07a1a');R(g,3,1,2,1,'#c6d9f3');R(g,7,1,2,1,'#c6d9f3');R(g,2,6,2,6,K);R(g,8,6,2,6,K);R(g,4,8,4,1,K);return c;}
function stageSprite(){const c=mk(80,34),g=c.getContext('2d');R(g,0,0,80,34,K);R(g,1,1,78,14,'#2a2a36');R(g,1,1,78,2,PAL.W);R(g,12,4,56,9,K);R(g,13,5,54,7,'#9b5fd6');
  text(g,'BLOCK PARTY',40,6,'#ffffff',{align:'center',outline:null});R(g,1,15,78,18,'#a8673a');for(let y=19;y<33;y+=4)R(g,1,y,78,1,'#7a4a2a');R(g,1,15,78,2,PAL.W);
  for(const x of [2,68]){R(g,x,12,10,18,K);R(g,x+1,13,8,16,'#55607a');g.fillStyle=K;pixCircle(g,x+5,17,2);pixCircle(g,x+5,24,3);R(g,x+1,13,8,1,PAL.W);}return c;}
function speakerSprite(){const c=mk(10,14),g=c.getContext('2d');R(g,0,0,10,14,K);R(g,1,1,8,12,'#55607a');R(g,1,1,8,1,PAL.W);g.fillStyle=K;pixCircle(g,5,4,1);pixCircle(g,5,9,3);g.fillStyle='#8793a8';pixCircle(g,5,9,1);return c;}
function planterSprite(){const c=mk(14,20),g=c.getContext('2d');g.drawImage(pineSprite(14),1,0);R(g,0,12,14,8,K);R(g,1,13,12,6,'#8793a8');R(g,1,13,12,1,PAL.W);R(g,1,17,12,1,'#6a7896');return c;}
function oakSprite(){const c=mk(22,24),g=c.getContext('2d');R(g,9,15,4,9,K);R(g,10,15,2,8,'#7a4a2a');g.fillStyle=K;pixCircle(g,11,10,10);g.fillStyle='#2f8a4a';pixCircle(g,11,10,9);g.fillStyle='#3fa85a';pixCircle(g,13,12,5);
  g.fillStyle='#f4f8ff';pixCircle(g,9,6,5);R(g,4,10,6,1,'#c6d9f3');R(g,14,5,3,1,'#f4f8ff');return c;}
function bollardSprite(){const c=mk(5,9),g=c.getContext('2d');R(g,0,0,5,9,K);R(g,1,1,3,7,'#55607a');R(g,1,1,3,2,PAL.W);R(g,1,5,3,1,'#ffc727');return c;}
function buntingSprite(w){const c=mk(w,9),g=c.getContext('2d');const cols=['#d8364b','#ffc727','#3f86d6','#33b24a','#9b5fd6'];const sag=x=>Math.round(3*Math.sin(x/w*Math.PI));
  for(let x=0;x<w;x++)R(g,x,sag(x),1,1,K);for(let x=3,k=0;x<w-5;x+=6,k++){const y=sag(x)+1;for(let r=0;r<4;r++)R(g,x+(r>>1),y+r,5-r,1,K);for(let r=0;r<3;r++)R(g,x+1+(r>>1),y+r,3-r,1,cols[k%5]);}return c;}
const SHOPS=[['CORNER SHOP','#3f86d6','#2a5fa8','#d8364b'],['BAKERY','#e8c87a','#c98d4a','#a8673a'],['CAFE','#e07a8a','#b04a5a','#7a1f33'],['BOOKS','#8fbf5a','#5e8a3a','#1f7a5c'],
  ['FLOWERS','#f4f8ff','#c6d9f3','#ff4fa3'],['TOYS','#ffc727','#e29a1c','#9b5fd6'],['BUTCHER','#f4f8ff','#c6d9f3','#d8364b'],['CHEMIST','#c6d9f3','#8793a8','#33b24a'],['CLUBHOUSE','#e8eef8','#c6d9f3','#1f7a5c'],['PET SHOP','#9b5fd6','#6b4fa8','#ffc727'],
  ['BANK','#c6d9f3','#8793a8','#13306b'],['BARBER','#f4f8ff','#c6d9f3','#3f86d6'],['DELI','#8fbf5a','#5e8a3a','#d8364b'],['SHOES','#e07a8a','#b04a5a','#13306b'],['PIZZA','#e8c87a','#c98d4a','#33b24a'],['GIFTS','#9b7fd6','#6b4fa8','#ff4fa3']];
Object.assign(PROPS,{
  rail:{arg:60,min:12,max:180,make:a=>railSprite(a,7),foot:a=>[0,1,a,5]},
  railv:{arg:60,min:12,max:400,make:a=>railSprite(5,a),foot:a=>[0,0,5,a]},
  net:{arg:120,min:30,max:176,make:a=>netSprite(a),foot:a=>[0,3,a,4]},
  kennel:{make:()=>kennelSprite(),foot:()=>[1,6,16,10]},
  shed:{arg:0,min:0,max:2,make:a=>shedSprite(a),foot:()=>[0,8,28,18]},
  greenhouse:{make:()=>greenhouseSprite(),foot:()=>[0,4,30,18]},
  plot:{arg:50,min:12,max:120,make:a=>plotSprite(a),foot:a=>[0,0,a,10]},
  scarecrow:{make:()=>scarecrowSprite(),foot:()=>[3,16,8,6]},
  roundabout:{make:()=>roundaboutSprite(),foot:()=>[1,3,20,12]},
  seesaw:{make:()=>seesawSprite(),foot:()=>[0,2,30,5]},
  climb:{make:()=>climbSprite(),foot:()=>[0,12,24,10]},
  sandpit:{make:()=>sandpitSprite(),foot:()=>[0,0,32,22]},
  hurdle:{make:()=>hurdleSprite(),foot:()=>[0,3,16,5]},
  pole:{make:()=>poleSprite(),foot:()=>[0,7,4,5]},
  phonebox:{make:()=>phoneboxSprite(),foot:()=>[0,12,12,12]},
  busstop:{make:()=>busstopSprite(),foot:()=>[0,10,30,8]},
  postbox:{make:()=>postboxSprite(),foot:()=>[0,6,8,8]},
  table:{arg:0,min:0,max:3,make:a=>tableSprite(a),foot:()=>[0,2,26,9]},
  bbq:{make:()=>bbqSprite(),foot:()=>[0,4,12,8]},
  stage:{make:()=>stageSprite(),foot:()=>[0,6,80,28]},
  speaker:{make:()=>speakerSprite(),foot:()=>[0,6,10,8]},
  planter:{make:()=>planterSprite(),foot:()=>[0,12,14,8]},
  oak:{make:()=>oakSprite(),foot:()=>[7,17,8,7]},
  bollard:{make:()=>bollardSprite(),foot:()=>[0,4,5,5]},
  shop:{arg:0,min:0,max:40,make:a=>{const S=SHOPS[a%SHOPS.length];return buildingSprite(56,60,S[1],S[2],S[0],S[3],a*7+3);},foot:()=>[0,0,56,60]},
  shopv:{arg:0,min:0,max:40,make:a=>{const S=SHOPS[a%SHOPS.length];return buildingSprite(44,72,S[1],S[2],S[0],S[3],a*5+1);},foot:()=>[0,0,44,72]},
  big:{arg:0,min:0,max:40,make:a=>{const S=SHOPS[a%SHOPS.length];return bigBuilding(110,58,S[1],S[2],S[0],S[3]);},foot:()=>[0,0,110,58]},
});
Object.assign(HAZ,{
  pedx:{make:(x,y,a)=>({kind:'ped',x,y,w:8,h:5,vy:0,vx:a?-15:15,spr:SPR.peds[((x+y)>>1)%3],t:0,say:0})},
  taxi:{make:(x,y,a)=>{const bus=(a|0)>=2,d=(a|0)%2?-1:1,cc=CAR_PAL[(x+y)%5];return {kind:'taxi',x,y,w:bus?24:22,h:bus?52:28,vy:d*(bus?28:36),dir:d,big:true,spr:bus?BUS:carSprite(cc[0],cc[1],false,false)};}},
  balls:{balls:1},cannon:{cannon:1}});
"""
rep("function buildFromData(g,D,setT,ob){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  for(const r of D.ground||[])setT(GROUND_T[r[0]]!=null?GROUND_T[r[0]]:T_GRASS,r[1],r[2],r[3],r[4]);",
    "  for(const r of D.ground||[])setT(GROUND_T[r[0]]!=null?GROUND_T[r[0]]:T_GRASS,r[1],r[2],r[3],r[4]);\n"
    "  for(const c of D.circles||[])if(setCircle)setCircle(GROUND_T[c[0]]!=null?GROUND_T[c[0]]:T_WHT,c[1],c[2],c[3]);\n"
    "  for(const p of D.paint||[])if(paintText)paintText(p[0],p[1],p[2],p[3]||2);\n"
    "  for(const d of D.decor||[])if(d[0]==='bunting')g.decor.push({spr:buntingSprite(d[3]||60),x:d[1],y:d[2]});\n"
    "  for(const n of D.neighbours||[])g.neighbours.push({rects:n.rects,path:n.path,x:n.path[0][0],y:n.path[0][1],state:'wait',t:0});\n"
    "  for(const p of D.pull||[]){const c=CAR_PAL[(p[2]||0)%5];g.hazards.push({kind:'pull',x:p[0],y:p[1],w:22,h:28,home:p[1],state:'park',t:rnd(2,8),spr:carSprite(c[0],c[1])});g.pullBlocks.push([p[0]+1,p[1],22,28]);}")
rep("    if(H.spawner){if(!g.spawners.some(s2=>s2.kind===H.spawner))g.spawners.push({kind:H.spawner,every:[5,8],t:4});}",
    "    if(H.spawner){if(!g.spawners.some(s2=>s2.kind===H.spawner))g.spawners.push({kind:H.spawner,every:h[3]&&h[3].length?h[3]:[5,8],t:4});}\n"
    "    else if(H.balls){const d=h[3]||1,o=ob(ballMachineSprite(d),h[1],h[2],1,5,10,6);g.hazards.push({kind:'balls',x:h[1],y:h[2],w:12,h:12,dir:d,per:h[4]||2.8,t:rnd(0.6,2),state:'idle',shots:[],mx:h[1]+(d>0?12:0),my:h[2]+7,ob:o});}\n"
    "    else if(H.cannon){const ang=h[3]!=null?h[3]:Math.PI/2,o=ob(cannonSprite(ang),h[1],h[2],2,8,14,9);g.hazards.push({kind:'cannon',x:h[1],y:h[2],w:18,h:18,ang,per:h[4]||6.5,range:h[5]||62,t:rnd(1.5,3),state:'idle',jam:0,immune:0,acc:0,mx:h[1]+9+Math.cos(ang)*8,my:h[2]+9+Math.sin(ang)*8,ob:o});}")
rep("  if(L.data){buildFromData(g,L.data,setT,ob);}","  if(L.data){buildFromData(g,L.data,setT,ob,setCircle,paintText);}")

# walkers can cross sideways
rep("else if(hz.kind==='ped'){hz.t+=dt;hz.say-=dt;const ny=hz.y+hz.vy*dt,r={x:hz.x,y:ny,w:hz.w,h:hz.h};let bad=ny<10||ny+hz.h>G.ph-10;",
    "else if(hz.kind==='ped'){hz.t+=dt;hz.say-=dt;const nx=hz.x+(hz.vx||0)*dt,ny=hz.y+hz.vy*dt,r={x:nx,y:ny,w:hz.w,h:hz.h};let bad=ny<10||ny+hz.h>G.ph-10||nx<2||nx+hz.w>G.pw-2;")
rep("      if(bad)hz.vy*=-1;else hz.y=ny;continue;}","      if(bad){hz.vy*=-1;if(hz.vx)hz.vx*=-1;}else{hz.x=nx;hz.y=ny;}continue;}")

# ball machines and snow cannons
rep("    else if(hz.kind==='ped'){hz.t+=dt;hz.say-=dt;",
r"""    else if(hz.kind==='balls'){hz.t-=dt;const onScr=Math.abs(P.y-hz.y)<150;
      if(hz.state==='idle'){if(hz.t<=0&&onScr){hz.state='wind';hz.t=0.75;sfx('tick',0,{vol:0.5,rate:1.3});}}
      else if(hz.state==='wind'){if(hz.t<=0){hz.state='idle';hz.t=hz.per+rnd(-0.4,0.4);hz.shots.push({x:hz.mx,y:hz.my,vx:hz.dir*118});sfx('throw',0,{rate:1.5,vol:0.55});}}
      for(const s2 of hz.shots){s2.x+=s2.vx*dt;const br={x:s2.x-2,y:s2.y-2,w:4,h:4};if(s2.x<-6||s2.x>G.pw+6){s2.dead=true;continue;}
        if(tid!=='ufo'&&overlap(pr,br)){s2.dead=true;hit('hz',SPILL_HAZARD*0.5);addFloat(P.x,P.y-22,'THWACK!','#d7f03a',0.9);continue;}
        for(const o of G.obstacles)if(o!==hz.ob&&overlap(br,o)){s2.dead=true;break;}}
      hz.shots=hz.shots.filter(s2=>!s2.dead);continue;}
    else if(hz.kind==='cannon'){hz.t-=dt;if(hz.immune>0)hz.immune-=dt;
      if(hz.jam>0){hz.jam-=dt;if(hz.jam<=0){hz.state='idle';hz.t=1.5;hz.immune=3;addFloat(hz.x+9,hz.y-10,'WHIRR...','#9fd8ff',0.8);}continue;}
      if(tid!=='ufo'&&!(hz.immune>0)&&overlap(bwr,{x:hz.x,y:hz.y+4,w:hz.w,h:hz.h-2})){hz.jam=9;hz.state='jam';const bonus=Math.round(BASE_CELL_VALUE*G.def.value*valueMult()*40);earn(bonus);
        addFloat(hz.x+9,hz.y-12,'JAMMED!'+cplus(bonus),'#ffd23f',1.1);sfx('flump');buzz(25);shake=0.12;for(let k=0;k<10;k++)particles.push({x:hz.x+9,y:hz.y+6,vx:rnd(-40,40),vy:rnd(-30,10),z:3,vz:rnd(20,50),life:0.5,t:0,kind:'snow'});continue;}
      if(hz.state==='idle'){if(hz.t<=0&&Math.abs(P.y-hz.y)<170){hz.state='wind';hz.t=0.9;sfx('warn',0,{vol:0.4,rate:0.8});}}
      else if(hz.state==='wind'){if(hz.t<=0){hz.state='spray';hz.t=1.5;sfx('squall',0,{vol:0.45,rate:1.3});}}
      else if(hz.state==='spray'){hz.acc+=dt*70;while(hz.acc>=1){hz.acc--;const a=hz.ang+rnd(-0.5,0.5),d=rnd(12,hz.range),px=hz.mx+Math.cos(a)*d,py=hz.my+Math.sin(a)*d;
          if(px>2&&px<G.pw-2&&py>2&&py<G.ph-2)addSnowCircle(G,px,py,4,0.3);if(Math.random()<0.6)particles.push({x:hz.mx,y:hz.my,vx:Math.cos(a)*rnd(60,110),vy:Math.sin(a)*rnd(60,110),z:6,vz:rnd(10,40),life:0.55,t:0,kind:'snow'});}
        if(hz.t<=0){hz.state='idle';hz.t=hz.per+rnd(-0.5,0.5);}}
      continue;}
    else if(hz.kind==='ped'){hz.t+=dt;hz.say-=dt;""")
rep("    else if(hz.kind==='ped')ents.push({base:hz.y+hz.h,draw:()=>b.drawImage(hz.spr,hx-2,hy-9+(Math.floor(hz.t*6)%2))});",
r"""    else if(hz.kind==='ped')ents.push({base:hz.y+hz.h,draw:()=>b.drawImage(hz.spr,hx-2,hy-9+(Math.floor(hz.t*6)%2))});
    else if(hz.kind==='balls')ents.push({base:hz.y+hz.h+1,draw:()=>{if(hz.state==='wind'){for(let x=hz.mx+hz.dir*6;x>-2&&x<G.pw+2;x+=hz.dir*6)R(b,Math.round(x),Math.round(hz.my),3,1,'rgba(215,240,58,0.6)');
        if(Math.floor(tNow*10)%2===0)text(b,'!',hx+6,hy-12,'#ff4a4a',{align:'center'});}
      for(const s2 of hz.shots){const sx=Math.round(s2.x),sy2=Math.round(s2.y);R(b,sx-2,sy2+1,4,1,'rgba(27,31,59,0.25)');R(b,sx-2,sy2-3,4,4,K);R(b,sx-1,sy2-2,2,2,'#d7f03a');}}});
    else if(hz.kind==='cannon')ents.push({base:hz.y+hz.h+1,draw:()=>{if(hz.state==='wind'&&Math.floor(tNow*10)%2===0)text(b,'!',hx+9,hy-12,'#ff4a4a',{align:'center'});
      if(hz.jam>0){R(b,hx+1,hy+1,16,9,K);R(b,hx+2,hy+2,14,7,'#f4f8ff');R(b,hx+3,hy+2,5,1,'#ffffff');R(b,hx+2,hy+8,14,1,'#c6d9f3');if(hz.jam<2&&Math.floor(tNow*8)%2===0)R(b,hx+8,hy-2,2,3,'#9fd8ff');}}});""")

# ---------------- the boss gate ----------------
rep("function levelGateOK(i){","const BOSS_STARS={blockparty:25};\nfunction areaStars(a){let n=0;LEVELS.forEach((L,i)=>{if(L.area===a&&!L.boss&&levelAvail(i))n+=save.stars[i]||0;});return n;}\n"
    "function bossShort(i){const L=LEVELS[i];return L&&L.boss?Math.max(0,(BOSS_STARS[L.id]||0)-areaStars(L.area)):0;}\nfunction levelGateOK(i){")
rep("const i2=LEVELS.indexOf(L);if(save.stars[i2]>0||save.best[i2]>0)return true;return L.from.some(id=>save.stars[lvIdx(id)]>0);}",
    "const i2=LEVELS.indexOf(L);if(save.stars[i2]>0||save.best[i2]>0)return true;if(bossShort(i2)>0)return false;return L.from.some(id=>save.stars[lvIdx(id)]>0);}")
rep("  if(!levelReach(i))return 'FINISH '+L.from.map(id=>LEVELS[lvIdx(id)].name).join(' OR ');",
    "  if(!levelReach(i)){if(bossShort(i)>0&&L.from.some(id=>save.stars[lvIdx(id)]>0))return 'NEEDS '+BOSS_STARS[L.id]+' '+AREAS[L.area].name+' STARS ('+areaStars(L.area)+')';return 'FINISH '+L.from.map(id=>LEVELS[lvIdx(id)].name).join(' OR ');}")
rep("upg:{lvOf,","get checkLast(){return CHECK_LAST;},fp:footprint,blk:blockedBy,bossShort,areaStars,upg:{lvOf,")
# the checker keeps its last coverage map so tests can show exactly which snow a machine can't reach
rep("  const reachPct=reach/g.clearable*100,need=g.clearable*L.stars[2]/100","  CHECK_LAST={C,g};const reachPct=reach/g.clearable*100,need=g.clearable*L.stars[2]/100")
rep("const CHECK_EFF=0.75;","let CHECK_LAST=null;const CHECK_EFF=0.75;")
# map: the locked boss shows how many Suburbs stars you have toward the 25
rep("  if(!small&&(st!=='locked'||stars>0)){R(b,x-10,y+r,21,7,K);",
    "  if((st==='locked'||st==='far')&&L.boss&&bossShort(i)>0&&L.from.some(id=>save.stars[lvIdx(id)]>0)){const s2=areaStars(L.area)+'/'+BOSS_STARS[L.id],w2=textW(s2)+13,lx=x-Math.round(w2/2);R(b,lx,y+r,w2,9,K);R(b,lx+1,y+r+1,w2-2,7,'#7a4a00');b.drawImage(SPR.star,lx+2,y+r+2);text(b,s2,lx+10,y+r+2,'#ffd23f',{outline:null});}\n"
    "  if(!small&&(st!=='locked'||stars>0)){R(b,x-10,y+r,21,7,K);")
open(f,'w',encoding='utf-8').write(s);print('p46 ok')
