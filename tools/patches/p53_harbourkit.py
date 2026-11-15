import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# FROZEN HARBOUR KIT: containers, boats, a lighthouse, gantry cranes; forklifts trundling round the docks;
# gulls that scatter; barriers (drawbridges and lock gates) that close after a warning; the forklift boss chaser.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function containerSprite(w,h,a){const col=['#d8364b','#3f86d6','#33b24a','#ffc727','#f07a1a','#9b5fd6'][a%6];const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,col);
  if(w>=h){for(let x=3;x<w-2;x+=3)R(g,x,2,1,h-4,'rgba(0,0,0,0.22)');}else{for(let y=3;y<h-2;y+=3)R(g,2,y,w-4,1,'rgba(0,0,0,0.22)');}R(g,1,1,w-2,3,PAL.W);return c;}
function boatSprite(a){const col=['#d8364b','#3f86d6','#33b24a','#f4f8ff'][a%4];const c=mk(30,64),g=c.getContext('2d');g.fillStyle=K;for(let y=0;y<64;y++){const hw=y<16?Math.round(15*Math.sqrt(y/16)):y>58?15-(y-58)*2:15;g.fillRect(15-hw,y,hw*2,1);}
  g.fillStyle=col;for(let y=1;y<63;y++){const hw=(y<16?Math.round(14*Math.sqrt(y/16)):y>58?14-(y-58)*2:14)-1;g.fillRect(15-hw,y,hw*2,1);}R(g,7,26,16,20,K);R(g,8,27,14,18,'#f4f8ff');R(g,9,29,12,4,'#8fd3ff');R(g,8,27,14,3,PAL.W);R(g,14,10,2,16,'#55607a');R(g,6,52,18,2,'#2a2a36');return c;}
function lighthouseSprite(){const c=mk(26,70),g=c.getContext('2d');R(g,9,0,8,4,K);R(g,10,1,6,2,'#d8364b');R(g,8,4,10,8,K);R(g,9,5,8,6,'#ffe9a8');R(g,7,12,12,3,K);
  for(let y=15;y<62;y++){const hw=5+Math.round((y-15)*0.12);R(g,13-hw-1,y,hw*2+2,1,K);R(g,13-hw,y,hw*2,1,((y-15)>>3)%2?'#d8364b':'#f4f8ff');}R(g,10,50,6,10,K);R(g,11,51,4,9,'#3a2a20');R(g,0,62,26,8,K);R(g,1,63,24,6,'#8793a8');return c;}
function dockGantrySprite(){const c=mk(70,74),g=c.getContext('2d');R(g,0,0,70,8,K);R(g,1,1,68,6,'#ffc727');for(let x=3;x<68;x+=6)R(g,x,2,3,4,'#c98a12');R(g,28,8,14,10,K);R(g,29,9,12,8,'#55607a');R(g,34,18,2,20,K);R(g,30,38,10,4,K);
  for(const x of [2,60]){R(g,x,8,8,62,K);R(g,x+1,8,6,61,'#ffc727');for(let y=12;y<66;y+=6)R(g,x+1,y,6,1,'#c98a12');}R(g,0,66,14,8,K);R(g,56,66,14,8,K);return c;}
function hullSprite(){const c=mk(90,170),g=c.getContext('2d');g.fillStyle=K;for(let y=0;y<170;y++){const hw=y<40?Math.round(45*Math.sqrt(y/40)):y>160?45-(y-160)*3:45;g.fillRect(45-hw,y,hw*2,1);}
  g.fillStyle='#d8364b';for(let y=2;y<168;y++){const hw=(y<40?Math.round(44*Math.sqrt(y/40)):y>160?44-(y-160)*3:44)-2;g.fillRect(45-hw,y,hw*2,1);}R(g,10,50,70,90,'#2a2a36');for(let y=56;y<136;y+=20)R(g,14,y,62,14,'#3f86d6');
  R(g,20,140,50,24,K);R(g,21,141,48,22,'#f4f8ff');for(let x=24;x<66;x+=6)R(g,x,146,3,3,'#8fd3ff');R(g,40,4,10,30,'#ffc727');return c;}
function hutSprite(a){const col=['#d8364b','#3f86d6','#33b24a','#ffc727'][a%4];const c=mk(16,16),g=c.getContext('2d');for(let r=0;r<5;r++){R(g,7-r,r,2+r*2,1,K);}R(g,1,5,14,1,PAL.W);R(g,1,5,14,11,K);R(g,2,6,12,9,col);R(g,6,9,4,6,K);R(g,2,6,12,1,PAL.W);return c;}
function anchorSprite(){const c=mk(14,16),g=c.getContext('2d');R(g,6,0,3,14,K);R(g,7,1,1,12,'#55607a');R(g,3,2,9,3,K);R(g,4,3,7,1,'#55607a');R(g,0,10,4,4,K);R(g,11,10,4,4,K);R(g,2,13,11,3,K);R(g,3,13,9,1,'#55607a');return c;}
function forkliftSprite(fr){const c=mk(16,22),g=c.getContext('2d');R(g,2,0,2,8,K);R(g,12,0,2,8,K);R(g,2,6,12,2,K);R(g,0,8,16,12,K);R(g,1,9,14,10,'#ffc727');R(g,4,10,8,6,'#2a2a36');R(g,5,10,6,2,'#8fd3ff');R(g,1,9,14,1,PAL.W);
  const l=fr?1:0;R(g,0,18+l,4,4,K);R(g,12,18+l,4,4,K);R(g,0,9+l,2,4,K);return c;}
function gullSprite(fr){const c=mk(12,8),g=c.getContext('2d');R(g,3,2,6,4,K);R(g,4,3,4,2,'#f4f8ff');R(g,8,2,3,2,K);R(g,10,3,2,1,'#ffc727');if(fr){R(g,0,0,4,2,K);R(g,1,0,2,1,'#c6d0e0');}else{R(g,0,4,4,2,K);R(g,1,4,2,1,'#c6d0e0');}R(g,4,6,1,2,'#f07a1a');return c;}
function bridgeBarSprite(w){const c=mk(w,8),g=c.getContext('2d');R(g,0,1,w,6,K);for(let x=1;x<w-1;x+=8){R(g,x,2,4,4,'#d8364b');R(g,x+4,2,4,4,'#f4f8ff');}R(g,1,2,w-2,1,PAL.W);return c;}
SHOPS.push(['FISH MARKET','#9fd4f4','#6fb4e0','#13306b'],['WAREHOUSE','#8793a8','#6a7896','#ffc727'],['CUSTOMS','#e8e0cc','#d6cdb4','#13306b'],['HARBOUR MASTER','#f4f8ff','#c6d9f3','#d8364b'],['FERRIES','#3f86d6','#2a5fa8','#ffc727'],['BOAT SHED','#a8673a','#7a4a2a','#f4f8ff']);
function rockSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,2,0,w-4,h,K);R(g,0,2,w,h-3,K);R(g,1,2,w-2,h-4,'#8793a8');R(g,2,1,w-4,1,'#8793a8');R(g,1,h-3,w-2,1,'#6a7896');R(g,Math.floor(w/2),2,1,h-5,'#6a7896');R(g,2,1,w-5,2,PAL.W);R(g,1,2,3,1,PAL.W);return c;}
Object.assign(PROPS,{
  rock:{arg:24,min:8,max:60,make:a=>rockSprite(a,Math.max(8,Math.round(a*0.66))),foot:a=>[0,2,a,Math.max(6,Math.round(a*0.66)-2)]},
  container:{arg:0,min:0,max:5,make:a=>containerSprite(44,16,a),foot:()=>[0,0,44,16]},
  containerv:{arg:0,min:0,max:5,make:a=>containerSprite(16,44,a),foot:()=>[0,0,16,44]},
  boat:{arg:0,min:0,max:3,make:a=>boatSprite(a),foot:()=>[1,0,28,64]},
  lighthouse:{make:()=>lighthouseSprite(),foot:()=>[0,50,26,20]},
  gantry:{make:()=>dockGantrySprite(),foot:()=>[0,60,70,14]},
  hull:{make:()=>hullSprite(),foot:()=>[0,0,90,170]},
  hut:{arg:0,min:0,max:3,make:a=>hutSprite(a),foot:()=>[1,5,14,11]},
  anchor:{make:()=>anchorSprite(),foot:()=>[0,8,14,8]}});
CHASERS.forklift={name:'THE FORKLIFT',frames:[forkliftSprite(0),forkliftSprite(1)],w:14,h:9,ox:1,oy:12,speed:1.05,lines:['BEEP BEEP BEEP!','OUT OF MY LANE!','LOADING BAY, MOVE IT!','HONK HONK!'],catchLine:'FORKED!',col:'#ffc727'};
const GULL_FR=[gullSprite(0),gullSprite(1)],FORK_FR=[forkliftSprite(0),forkliftSprite(1)],BAR_SPR={};
Object.assign(HAZ,{forklift:{forklift:1},gull:{gull:1},barrier:{barrier:1}});
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("    else if(H.balls){",
    "    else if(H.forklift){const a=(h[3]||0)?Math.PI/2:0;g.hazards.push({kind:'bumper',fork:true,x:h[1],y:h[2],w:14,h:10,vx:Math.cos(a)*26,vy:Math.sin(a)*26,spr:FORK_FR[0],cool:0,turn:rnd(2,5)});}\n"
    "    else if(H.gull){const n=h[3]||5;for(let k=0;k<n;k++)g.hazards.push({kind:'sheep',gull:true,flock:h[1]*1000+h[2],x:h[1]+(k%3)*12,y:h[2]+((k/3)|0)*10,w:8,h:5,hx:h[1],hy:h[2],vx:0,vy:0,t:rnd(0,3),anim:rnd(0,2)});}\n"
    "    else if(H.barrier){const w=h[3]||60;g.hazards.push({kind:'barrier',x:h[1],y:h[2],w,h:8,per:h[4]||5,t:rnd(1,h[4]||5),closed:false,warn:0,spr:bridgeBarSprite(w)});}\n"
    "    else if(H.balls){")
# forklifts turn now and then (they are bumpers that drive); gulls fly off when the plow comes, and come back
rep("    else if(hz.kind==='bumper'){if(hz.cool>0)hz.cool-=dt;",
    "    else if(hz.kind==='bumper'){if(hz.cool>0)hz.cool-=dt;if(hz.fork){hz.turn-=dt;if(hz.turn<=0){hz.turn=rnd(2,5);const t2=hz.vx;hz.vx=hz.vy;hz.vy=-t2;if(Math.random()<0.5){hz.vx*=-1;hz.vy*=-1;}}}")
rep("      if(tid!=='ufo'&&overlap(pr,hz)){hit('ob');addFloat(hz.x+6,hz.y-10,'BUMP!','#ffd23f',0.6);",
    "      if(tid!=='ufo'&&overlap(pr,hz)){hit('ob');addFloat(hz.x+6,hz.y-10,hz.fork?'BEEP!':'BUMP!','#ffd23f',0.6);")
rep("    else if(hz.kind==='bumper')ents.push({base:hz.y+hz.h,draw:()=>{R(b,hx,hy+hz.h,hz.w,2,'rgba(27,31,59,0.22)');b.drawImage(hz.spr,hx-1,hy-4);}});",
    "    else if(hz.kind==='bumper')ents.push({base:hz.y+hz.h,draw:()=>{R(b,hx,hy+hz.h,hz.w,2,'rgba(27,31,59,0.22)');if(hz.fork){b.save();b.translate(hx+hz.w/2,hy+hz.h/2);b.rotate(Math.atan2(hz.vy,hz.vx)+Math.PI/2);b.drawImage(FORK_FR[Math.floor(tNow*6)%2],-8,-11);b.restore();}else b.drawImage(hz.spr,hx-1,hy-4);}});\n"
    "    else if(hz.kind==='barrier')ents.push({base:hz.y+hz.h,draw:()=>{if(hz.closed)b.drawImage(hz.spr,hx,hy);else{R(b,hx,hy+2,3,4,K);R(b,hx+hz.w-3,hy+2,3,4,K);}if(hz.warn>0&&Math.floor(tNow*8)%2===0){R(b,hx-1,hy-6,5,5,'#ffd23f');R(b,hx+hz.w-4,hy-6,5,5,'#ffd23f');for(let x=hx+4;x<hx+hz.w-4;x+=6)R(b,x,hy+3,3,1,'rgba(255,210,63,0.7)');}}});")
# barriers: open/close on a timer with a warning; never close on top of you
rep("    else if(hz.kind==='bumper'){","    else if(hz.kind==='barrier'){hz.t-=dt;if(hz.warn>0){hz.warn-=dt;if(hz.warn<=0){if(overlap(pr,{x:hz.x,y:hz.y-6,w:hz.w,h:hz.h+12}))hz.warn=0.3;else{hz.closed=true;hz.t=hz.per;sfx('bump',0,{vol:0.3,rate:0.6});}}}\n"
    "      else if(hz.t<=0){if(hz.closed){hz.closed=false;hz.t=hz.per;}else{hz.warn=1.2;sfx('tick',0,{vol:0.5,rate:1.6});}}continue;}\n    else if(hz.kind==='bumper'){")
rep("  for(const hz of G.hazards)if((hz.kind==='thrower'||hz.kind==='ped'||(hz.kind==='pull'&&hz.state!=='out'&&hz.state!=='in'))&&overlap(r,hz)&&!ignOK(r,hz,hz,1)){G.lastOb=hz;return 'ob';}",
    "  for(const hz of G.hazards)if(((hz.kind==='barrier'&&hz.closed)||hz.kind==='thrower'||hz.kind==='ped'||(hz.kind==='pull'&&hz.state!=='out'&&hz.state!=='in'))&&overlap(r,hz)&&!ignOK(r,hz,hz,1)){G.lastOb=hz;return 'ob';}")
# gull frames
rep("const mv=Math.hypot(hz.vx,hz.vy)>6?Math.floor(hz.anim*8)%2:0,fr=hz.horse?HORSE_FR[hz.col+mv]:SHEEP_FR[mv];",
    "const mv=Math.hypot(hz.vx,hz.vy)>6?Math.floor(hz.anim*8)%2:0,fr=hz.gull?GULL_FR[Math.floor(hz.anim*10)%2]:hz.horse?HORSE_FR[hz.col+mv]:SHEEP_FR[mv];")
rep("if(Math.random()<0.4)addFloat(hz.x+4,hz.y-8,hz.horse?'NEIGH!':'BAA!','#ffffff',0.6);}}","if(Math.random()<0.4)addFloat(hz.x+4,hz.y-8,hz.gull?'SQUAWK!':hz.horse?'NEIGH!':'BAA!','#ffffff',0.6);}}")
rep("if(tid!=='ufo'&&overlap(pr,hz)){hit('ob');addFloat(hz.x+4,hz.y-8,hz.horse?'NEIGH!':'BAA!','#ffffff',0.7);",
    "if(tid!=='ufo'&&!hz.gull&&overlap(pr,hz)){hit('ob');addFloat(hz.x+4,hz.y-8,hz.horse?'NEIGH!':'BAA!','#ffffff',0.7);")
open(f,'w',encoding='utf-8').write(s);print('p53 ok')
