import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Ski Resort detail: orange snow fences, ski racks, a parked groomer, deckchairs, fire pits, the chairlift line overhead,
# a start hut and a finish arch.
KIT=r"""
function snowFenceSprite(w,v){const c=v?mk(6,w):mk(w,8),g=c.getContext('2d');if(v){R(g,1,0,4,w,K);R(g,2,0,2,w,'#f07a1a');for(let y=2;y<w;y+=4)R(g,2,y,2,1,'#ffb060');for(let y=0;y<w;y+=24){R(g,0,y,6,3,K);R(g,1,y,4,2,'#55607a');}}
  else{R(g,0,1,w,6,K);R(g,0,2,w,4,'#f07a1a');for(let x=2;x<w;x+=4)R(g,x,2,1,4,'#ffb060');for(let x=0;x<w;x+=24){R(g,x,0,3,8,K);R(g,x,1,2,6,'#55607a');}R(g,0,1,w,1,PAL.W);}return c;}
function skiRackSprite(){const c=mk(24,14),g=c.getContext('2d');R(g,0,10,24,4,K);R(g,1,11,22,2,'#8a5a34');const cols=['#e03a4e','#3f86d6','#ffc727','#33b24a','#9b5fd6','#f07a1a'];for(let k=0;k<6;k++){R(g,1+k*4,0,2,11,K);R(g,1+k*4,1,1,9,cols[k]);}R(g,0,0,24,1,PAL.W);return c;}
function groomerSprite(){const c=mk(40,64),g=c.getContext('2d');drawSnowcat(g,20,38,0,skinPal('snowcat',0));drawVBlade(g,20,38-21-7,36,7,'snowcat',skinPal('snowcat',0));return c;}
function deckchairSprite(a){const c=mk(10,14),g=c.getContext('2d'),col=['#e03a4e','#3f86d6','#ffc727'][a%3];R(g,0,0,10,14,K);R(g,1,1,8,12,col);for(let y=2;y<12;y+=3)R(g,1,y,8,1,'#f4f8ff');return c;}
function firepitSprite(){const c=mk(16,14),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,8,8,6);g.fillStyle='#55607a';pixCircle(g,8,8,5);g.fillStyle='#2a2a36';pixCircle(g,8,8,3);R(g,6,4,4,5,'#f07a1a');R(g,7,2,2,4,'#ffc727');R(g,7,5,2,2,'#ffffff');return c;}
function startHutSprite(){const c=mk(60,40),g=c.getContext('2d');R(g,0,8,60,32,K);R(g,1,9,58,30,'#e03a4e');R(g,0,2,60,8,K);R(g,1,3,58,6,'#8a5a34');R(g,1,2,58,3,PAL.W);R(g,6,14,48,10,K);R(g,7,15,46,8,'#13306b');sprText(g,'START',30-sprTextW('START')/2|0,17,'#ffd23f');R(g,24,28,12,12,K);R(g,25,29,10,11,'#f4f8ff');return c;}
function liftLineOverSprite(h){const c=mk(30,h),g=c.getContext('2d');R(g,7,0,1,h,'#2a2a36');R(g,22,0,1,h,'#2a2a36');for(let y=10;y<h;y+=48){for(const [x,dir] of [[7,0],[22,1]]){const yy=dir?y+24:y;if(yy>=h-10)continue;R(g,x,yy,1,6,K);R(g,x-5,yy+5,11,6,K);R(g,x-4,yy+6,9,4,dir?'#3f86d6':'#e03a4e');R(g,x-4,yy+5,9,1,PAL.W);}}return c;}
function finishArchOverSprite(w){const c=mk(w,30),g=c.getContext('2d');for(const x of [0,w-8]){R(g,x,0,8,30,K);R(g,x+1,1,6,28,'#e03a4e');}R(g,0,2,w,14,K);R(g,1,3,w-2,12,'#13306b');for(let x=2;x<w-2;x+=8){R(g,x,3,4,4,'#f4f8ff');R(g,x+4,7,4,4,'#f4f8ff');R(g,x,11,4,4,'#f4f8ff');}R(g,(w>>1)-24,3,48,12,K);R(g,(w>>1)-23,4,46,10,'#ffc727');sprText(g,'FINISH',(w>>1)-sprTextW('FINISH')/2|0,6,'#13306b');R(g,0,2,w,2,PAL.W);return c;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  iceblock:{arg:14,","  snowfence:{arg:48,min:12,max:180,make:a=>snowFenceSprite(a,0),foot:a=>[0,1,a,6]},\n  snowfencev:{arg:48,min:12,max:400,make:a=>snowFenceSprite(a,1),foot:a=>[0,0,6,a]},\n  skirack:{make:()=>scnSpr('sr',skiRackSprite),foot:()=>[0,6,24,8]},\n  groomer:{make:()=>scnSpr('gr',groomerSprite),foot:()=>[6,8,28,52]},\n  deckchair:{arg:0,min:0,max:2,make:a=>deckchairSprite(a),foot:()=>[0,0,10,14]},\n  firepit:{make:()=>scnSpr('fp',firepitSprite),foot:()=>[1,3,14,10]},\n  starthut:{make:()=>scnSpr('sh2',startHutSprite),foot:()=>[0,10,60,30]},\n  iceblock:{arg:14,")
rep("const OVERS={parkgate:","const OVERS={liftline:a=>liftLineOverSprite(a||400),finish:a=>finishArchOverSprite(a||180),parkgate:")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
KIT2=r"""
function plX(p,y){let best=p[0],bd=1e9;for(let i=0;i+3<p.length;i+=2){const ay=p[i+1],by=p[i+3],lo=Math.min(ay,by),hi=Math.max(ay,by);if(y>=lo&&y<=hi&&hi>lo)return p[i]+(p[i+2]-p[i])*(y-ay)/(by-ay);const da=Math.abs(y-ay),db=Math.abs(y-by);if(da<bd){bd=da;best=p[i];}if(db<bd){bd=db;best=p[i+2];}}return best;}
function carpetSprite(h){const c=mk(14,h),g=c.getContext('2d');R(g,0,0,14,h,K);R(g,1,0,12,h,'#55607a');R(g,3,0,8,h,'#2a2a36');for(let y=2;y<h;y+=6)R(g,3,y,8,1,'#3a3a48');R(g,1,0,2,h,'#ffc727');R(g,11,0,2,h,'#ffc727');R(g,0,0,14,10,K);R(g,1,1,12,8,'#3f86d6');R(g,1,1,12,2,PAL.W);R(g,0,h-6,14,6,K);R(g,1,h-5,12,4,'#8793a8');return c;}
function liftStationSprite(){const c=mk(64,54),g=c.getContext('2d');R(g,4,22,56,32,K);R(g,5,23,54,30,'#8793a8');for(let y=26;y<52;y+=6)R(g,5,y,54,1,'#6a7896');R(g,0,14,64,10,K);R(g,1,15,62,8,'#e03a4e');R(g,1,14,62,3,PAL.W);
  g.fillStyle=K;pixCircle(g,32,10,10);g.fillStyle='#2a2a36';pixCircle(g,32,10,9);g.fillStyle='#55607a';pixCircle(g,32,10,6);g.fillStyle='#2a2a36';pixCircle(g,32,10,2);R(g,22,9,21,2,'#c6d0dc');
  R(g,14,30,36,12,K);R(g,15,31,34,10,'#13306b');sprText(g,'LIFT',32-sprTextW('LIFT')/2|0,33,'#ffd23f');R(g,26,44,12,10,K);R(g,27,45,10,9,'#2a2a36');return c;}
function trailMapSprite(){const c=mk(32,28),g=c.getContext('2d');R(g,4,18,3,10,K);R(g,25,18,3,10,K);R(g,0,0,32,20,K);R(g,1,1,30,18,'#f4f8ff');R(g,1,1,30,4,'#13306b');
  const L=[[3,7,'#33b24a'],[9,6,'#2f5fae'],[16,7,'#e03a4e'],[23,6,'#1b1f3b']];for(const [x,y,col] of L){for(let k=0;k<11;k++)R(g,x+((k>>1)%2),y+k,2,1,col);}R(g,2,16,28,2,'#c6d9f3');R(g,0,0,32,1,PAL.W);return c;}
function gondolaOverSprite(h){const c=mk(30,h),g=c.getContext('2d');R(g,9,0,1,h,'#2a2a36');R(g,20,0,1,h,'#2a2a36');for(let y=14;y<h-16;y+=80){for(const [x,dy,col] of [[9,0,'#e03a4e'],[20,40,'#ffc727']]){const yy=y+dy;if(yy>h-16)continue;R(g,x,yy,1,4,K);R(g,x-5,yy+4,11,13,K);R(g,x-4,yy+5,9,11,col);R(g,x-3,yy+7,7,4,'#bfe6ff');R(g,x-4,yy+5,9,1,PAL.W);}}return c;}
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){", KIT2+"\nfunction buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("  iceblock:{arg:14,","  carpet:{arg:300,min:40,max:900,make:a=>carpetSprite(a),foot:a=>[0,0,14,a]},\n  liftstation:{make:()=>scnSpr('lst',liftStationSprite),foot:()=>[4,22,56,32]},\n  trailmap:{make:()=>scnSpr('tmp',trailMapSprite),foot:()=>[2,22,28,6]},\n  iceblock:{arg:14,")
rep("const OVERS={liftline:","const OVERS={gondola:a=>gondolaOverSprite(a||400),liftline:")
# skiers (and rockfalls) can follow a carved piste: hazard arg 4 = carve index, x = 90 + offset from the piste centre
rep("lane:h[1],x:h[1],y:-40,w:8,h:6,per:h[3]||6,","lane:h[1],x:h[1],pl:(h[4]!=null&&D.carves&&D.carves[h[4]])?D.carves[h[4]].slice(1):null,off:h[1]-90,y:-40,w:8,h:6,per:h[3]||6,")
rep("if(hz.t<=0){hz.state='warn';hz.t=1.0;","if(hz.t<=0){hz.state='warn';hz.t=1.0;if(hz.pl)hz.lane=plX(hz.pl,camY+8)+hz.off;")
rep("hz.x=hz.lane+(hz.rock?0:Math.sin(hz.wob*3)*14);","hz.x=(hz.pl?plX(hz.pl,hz.y)+hz.off:hz.lane)+(hz.rock?0:Math.sin(hz.wob*3)*(hz.pl?8:14));")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
# rectangular clearings in wild areas (D.clears), and skiers that follow an explicit line (hazard arg 4 = [x,y,...])
rep("  const inC=inCarveF(D.carves||[]);","  const inC0=inCarveF(D.carves||[]),CL=D.clears||[],inC=(px,py,m)=>{const q=m||0;for(const r of CL)if(px>=r[0]-q&&px<r[0]+r[2]+q&&py>=r[1]-q&&py<r[1]+r[3]+q)return true;return inC0(px,py,m);};")
rep("pl:(h[4]!=null&&D.carves&&D.carves[h[4]])?D.carves[h[4]].slice(1):null,","pl:Array.isArray(h[4])?h[4]:(h[4]!=null&&D.carves&&D.carves[h[4]])?D.carves[h[4]].slice(1):null,")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
# more banner words for the late areas: 12 BIG AIR 13 TERRAIN PARK 14 GRAND SLALOM 15 PASS OPEN 16 SLOW DOWN
# 17 POLAR POST 18 REINDEER 19 ICE PALACE 20 WORKSHOP 21 FINISH
rep("'HARBOUR','NORTH POLE'][a%12]","'HARBOUR','NORTH POLE','BIG AIR','TERRAIN PARK','GRAND SLALOM','PASS OPEN','SLOW DOWN','POLAR POST','REINDEER','ICE PALACE','WORKSHOP','FINISH'][a%22]",2)
open(f,'w',encoding='utf-8').write(s)
