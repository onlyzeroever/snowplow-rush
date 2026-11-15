import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# THEME PARK KIT: rides and park furniture, bumper cars that bounce round their arena, the roller coaster
# rushing across after a warning, ghosts in the haunted house, and the park's giant mascot as the boss chaser.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function ferrisSprite(){const c=mk(72,86),g=c.getContext('2d'),cx=36,cy=36,r=30;g.fillStyle=K;for(let a=0;a<120;a++){const t=a/120*Math.PI*2;g.fillRect(Math.round(cx+Math.cos(t)*r)-1,Math.round(cy+Math.sin(t)*r)-1,3,3);}
  for(let k=0;k<12;k++){const t=k/12*Math.PI*2;for(let d=2;d<r;d+=2)R(g,Math.round(cx+Math.cos(t)*d),Math.round(cy+Math.sin(t)*d),1,1,'#8793a8');}
  for(let k=0;k<12;k++){const t=k/12*Math.PI*2,px=Math.round(cx+Math.cos(t)*r),py=Math.round(cy+Math.sin(t)*r);R(g,px-4,py,8,7,K);R(g,px-3,py+1,6,5,['#d8364b','#ffc727','#3f86d6','#33b24a','#9b5fd6','#f07a1a'][k%6]);R(g,px-3,py+1,6,1,PAL.W);}
  R(g,cx-12,cy,4,50,K);R(g,cx+8,cy,4,50,K);R(g,cx-11,cy,2,49,'#c6d0e0');R(g,cx+9,cy,2,49,'#c6d0e0');R(g,cx-4,cy-4,9,9,K);R(g,cx-3,cy-3,7,7,'#ffc727');R(g,cx-20,cy+48,40,4,K);R(g,cx-19,cy+49,38,2,'#8793a8');return c;}
function carouselSprite(){const c=mk(40,40),g=c.getContext('2d');for(let r=0;r<12;r++){const hw=4+r*1.6|0;R(g,20-hw-1,r,hw*2+2,1,K);for(let x=-hw;x<hw;x++)R(g,20+x,r,1,1,((x+40)>>2)%2?'#d8364b':'#f4f8ff');}R(g,18,0,4,2,'#ffc727');
  R(g,0,12,40,3,K);R(g,1,12,38,2,'#ffc727');for(let k=0;k<5;k++){const x=3+k*8;R(g,x+2,15,1,12,'#c6d0e0');R(g,x,20+(k%2)*3,6,5,K);R(g,x+1,21+(k%2)*3,4,3,['#f4f8ff','#e8c87a','#9b5fd6'][k%3]);}
  g.fillStyle=K;for(let x=0;x<40;x++){const y=28+Math.round(Math.sin(x/40*Math.PI)*4);R(g,x,y,1,40-y,K);}for(let x=1;x<39;x++){const y=29+Math.round(Math.sin(x/40*Math.PI)*4);R(g,x,y,1,Math.max(0,39-y),'#e8c87a');}R(g,1,28,38,1,PAL.W);return c;}
function boothSprite(a){const col=['#d8364b','#3f86d6','#33b24a'][a%3];const c=mk(18,24),g=c.getContext('2d');R(g,0,0,18,6,K);for(let x=1;x<17;x+=4){R(g,x,1,2,4,col);R(g,x+2,1,2,4,'#f4f8ff');}R(g,1,0,16,1,PAL.W);
  R(g,1,6,16,18,K);R(g,2,6,14,17,'#f4f8ff');R(g,4,8,10,7,K);R(g,5,9,8,5,'#8fd3ff');R(g,2,17,14,2,col);return c;}
function turnstileSprite(){const c=mk(8,12),g=c.getContext('2d');R(g,2,0,4,12,K);R(g,3,1,2,10,'#8793a8');R(g,0,4,8,2,K);R(g,1,4,6,1,'#c6d0e0');R(g,3,0,2,1,PAL.W);return c;}
function coasterSprite(w,h){const c=mk(w,h),g=c.getContext('2d');const hz=w>=h;
  if(hz){for(let x=2;x<w;x+=10){R(g,x,4,2,h-4,K);R(g,x,4,1,h-5,'#8793a8');}R(g,0,0,w,5,K);R(g,0,1,w,1,'#d8364b');R(g,0,3,w,1,'#d8364b');for(let x=1;x<w;x+=3)R(g,x,2,1,1,'#55607a');R(g,0,0,w,1,PAL.W);}
  else{for(let y=4;y<h;y+=10){R(g,0,y,w,2,K);R(g,0,y,w,1,'#8793a8');}R(g,1,0,5,h,K);R(g,2,0,1,h,'#d8364b');R(g,4,0,1,h,'#d8364b');R(g,1,0,1,h,PAL.W);}return c;}
function helterSprite(){const c=mk(26,56),g=c.getContext('2d');for(let r=0;r<10;r++){const hw=2+r;R(g,13-hw-1,r,hw*2+2,1,K);R(g,13-hw,r,hw*2,1,r%2?'#d8364b':'#ffc727');}
  R(g,5,10,16,44,K);R(g,6,10,14,43,'#f4f8ff');for(let y=12;y<52;y+=8){for(let x=0;x<16;x++)R(g,5+x,y+Math.round(x*0.4),1,3,'#ffc727');}R(g,0,50,26,6,K);R(g,1,51,24,4,'#ffc727');R(g,6,10,14,2,PAL.W);return c;}
function dropSprite(){const c=mk(22,92),g=c.getContext('2d');R(g,8,0,6,92,K);R(g,9,0,4,91,'#c6d0e0');for(let y=4;y<88;y+=6)R(g,9,y,4,1,'#8793a8');R(g,2,30,18,10,K);R(g,3,31,16,8,'#d8364b');for(let x=4;x<18;x+=4)R(g,x,33,2,4,'#ffc727');
  R(g,6,0,10,4,K);R(g,7,1,8,2,'#ffc727');R(g,0,84,22,8,K);R(g,1,85,20,6,'#8793a8');return c;}
function balloonsSprite(){const c=mk(16,28),g=c.getContext('2d');const cols=['#d8364b','#ffc727','#3f86d6','#33b24a','#9b5fd6'];for(let k=0;k<5;k++){const x=2+(k%3)*4+(k>2?2:0),y=(k>2?6:0);g.fillStyle=K;pixCircle(g,x+2,y+3,3);g.fillStyle=cols[k];pixCircle(g,x+2,y+3,2);R(g,x+2,y+6,1,8,'#55607a');}
  R(g,5,18,6,6,K);R(g,6,18,4,5,'#f2c7a5');R(g,4,22,8,6,K);R(g,5,23,6,4,'#3f86d6');return c;}
function popcornSprite(){const c=mk(16,20),g=c.getContext('2d');R(g,1,0,14,4,K);R(g,2,1,12,2,'#d8364b');R(g,2,4,12,10,K);R(g,3,5,10,8,'#8fd3ff');for(const [x,y] of [[4,8],[7,9],[10,8],[5,11],[9,11]])R(g,x,y,2,2,'#fff4c8');
  R(g,1,14,14,4,K);R(g,2,14,12,3,'#d8364b');R(g,2,18,3,2,K);R(g,11,18,3,2,K);return c;}
function cupSprite(a){const col=['#d8364b','#3f86d6','#9b5fd6','#33b24a'][a%4];const c=mk(18,14),g=c.getContext('2d');g.fillStyle=K;for(let y=0;y<14;y++){const hw=Math.round(9*Math.sqrt(Math.max(0,1-((y-7)/7.5)**2)));g.fillRect(9-hw,y,hw*2,1);}
  g.fillStyle=col;for(let y=1;y<13;y++){const hw=Math.round(8*Math.sqrt(Math.max(0,1-((y-7)/6.6)**2)));g.fillRect(9-hw,y,hw*2,1);}R(g,4,4,10,5,'#f4f8ff');R(g,5,5,8,3,'#e8c87a');R(g,4,1,10,1,PAL.W);return c;}
function holeSprite(a){const c=mk(10,16),g=c.getContext('2d');R(g,2,0,1,12,K);R(g,3,1,6,4,K);R(g,3,2,5,2,['#d8364b','#ffc727','#3f86d6'][a%3]);g.fillStyle=K;pixCircle(g,3,13,2);return c;}
function bumperCarSprite(a){const col=['#d8364b','#ffc727','#3f86d6','#33b24a','#9b5fd6'][a%5];const c=mk(14,14),g=c.getContext('2d');R(g,0,2,14,10,K);R(g,1,3,12,8,col);R(g,1,3,12,2,PAL.W);R(g,4,5,6,4,'#2a2a36');R(g,5,0,1,4,K);R(g,5,0,1,3,'#c6d0e0');R(g,0,10,14,4,K);R(g,1,11,12,2,'#2a2a36');return c;}
function ghostSprite(fr){const c=mk(12,14),g=c.getContext('2d');R(g,2,0,8,2,K);R(g,1,1,10,11,K);R(g,2,1,8,10,'#f4f8ff');R(g,4,4,1,2,K);R(g,7,4,1,2,K);R(g,5,7,2,2,K);for(let x=1;x<11;x+=2)R(g,x,12+((x+fr)%4<2?0:1),2,2,K);return c;}
function mascotSprite(fr){const c=mk(20,26),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,10,8,8);g.fillStyle='#c98d4a';pixCircle(g,10,8,7);g.fillStyle=K;pixCircle(g,4,2,3);pixCircle(g,16,2,3);g.fillStyle='#c98d4a';pixCircle(g,4,2,2);pixCircle(g,16,2,2);
  R(g,6,6,2,2,K);R(g,12,6,2,2,K);R(g,7,10,6,3,'#f4e0c0');R(g,9,10,2,1,K);R(g,8,12,4,1,'#d8364b');R(g,3,15,14,8,K);R(g,4,15,12,7,'#d8364b');R(g,8,16,4,2,'#ffc727');R(g,0,16,4,5,K);R(g,16,16,4,5,K);R(g,1,17,2,3,'#c98d4a');R(g,17,17,2,3,'#c98d4a');
  const l=fr?1:0;R(g,4+l,22,5,4,K);R(g,11-l,22,5,4,K);R(g,5+l,23,3,2,'#c98d4a');R(g,12-l,23,3,2,'#c98d4a');return c;}
SHOPS.push(['TICKETS','#ffc727','#e29a1c','#d8364b'],['SOUVENIRS','#9b5fd6','#6b4fa8','#ffc727'],['ARCADE','#13306b','#0b1838','#ff4fa3'],['HAUNTED HOUSE','#4a3a6a','#2a1f40','#9fd8ff'],['BURGERS','#f07a1a','#c25a10','#ffc727'],['ICE CREAM','#ffb6d0','#e07a8a','#3f86d6'],['GHOST TRAIN','#2a2a36','#1b1f3b','#d8f03a'],['LOG FLUME','#3f86d6','#2a5fa8','#ffc727']);
Object.assign(PROPS,{
  ferris:{make:()=>ferrisSprite(),foot:()=>[14,70,44,16]},
  carousel:{make:()=>carouselSprite(),foot:()=>[0,12,40,28]},
  booth:{arg:0,min:0,max:2,make:a=>boothSprite(a),foot:()=>[0,6,18,18]},
  turnstile:{make:()=>turnstileSprite(),foot:()=>[0,4,8,8]},
  coaster:{arg:80,min:10,max:180,make:a=>coasterSprite(a,14),foot:a=>[0,0,a,6]},
  coasterv:{arg:80,min:10,max:600,make:a=>coasterSprite(7,a),foot:a=>[0,0,7,a]},
  helter:{make:()=>helterSprite(),foot:()=>[0,36,26,20]},
  droptower:{make:()=>dropSprite(),foot:()=>[0,76,22,16]},
  balloons:{make:()=>balloonsSprite(),foot:()=>[4,20,8,8]},
  popcorn:{make:()=>popcornSprite(),foot:()=>[0,8,16,12]},
  cup:{arg:0,min:0,max:3,make:a=>cupSprite(a),foot:()=>[0,2,18,12]},
  hole:{arg:0,min:0,max:2,make:a=>holeSprite(a),foot:()=>[1,8,4,4]}});
CHASERS.mascot={name:'BENNY BEAR',frames:[mascotSprite(0),mascotSprite(1)],w:14,h:7,ox:3,oy:19,speed:1.0,lines:['HUG TIME!','SMILE FOR THE PHOTO!','WELCOME TO THE PARK!!','COME BACK, FRIEND!','HAVE A MAGICAL DAY!'],catchLine:'BEAR HUG!',col:'#ffc727'};
const GHOST_FR=[ghostSprite(0),ghostSprite(1)],BUMPER_FR=[0,1,2,3,4].map(k=>bumperCarSprite(k));
Object.assign(HAZ,{bumper:{bumper:1},ghost:{make:(x,y,a)=>({kind:'ped',ghost:true,x,y,w:8,h:5,vy:0,vx:a?-12:12,spr:GHOST_FR[0],t:0,say:0})}});
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("    else if(H.balls){",
    "    else if(H.bumper){const n=h[3]||4;for(let k=0;k<n;k++){const a=rnd(0,Math.PI*2);g.hazards.push({kind:'bumper',x:h[1]+(k%3)*18,y:h[2]+((k/3)|0)*18,w:12,h:9,vx:Math.cos(a)*34,vy:Math.sin(a)*34,spr:BUMPER_FR[k%5],cool:0});}}\n"
    "    else if(H.balls){")
# cross skin: the coaster (fast, long)
rep("const d=h[3]||1,sk=h[5]||'farm',spr=sk==='car'?carSideSprite((h[1]+h[2])%5):sk==='float'?floatSprite():crossSprite();",
    "const d=h[3]||1,sk=h[5]||'farm',spr=sk==='car'?carSideSprite((h[1]+h[2])%5):sk==='float'?floatSprite():sk==='coaster'?trainSprite(90,'#d8364b'):crossSprite();")
rep("speed:sk==='car'?70:sk==='float'?28:46});}","speed:sk==='car'?70:sk==='float'?28:sk==='coaster'?120:46,rot:sk==='coaster'});}")
rep("y:h[2],w:spr.width-2,h:12,dir:d,","y:h[2],w:sk==='coaster'?88:spr.width-2,h:sk==='coaster'?20:12,dir:d,")
# update: bumper cars bounce off everything
rep("    else if(hz.kind==='sheep'){",
r"""    else if(hz.kind==='bumper'){if(hz.cool>0)hz.cool-=dt;const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y))hz.x=nx;else{hz.vx*=-1;if(hz.cool<=0&&Math.abs(P.y-hz.y)<100){sfx('bump',0,{vol:0.25,rate:1.4});hz.cool=0.4;}}
      if(chaserFree(hz,hz.x,ny))hz.y=ny;else hz.vy*=-1;
      for(const o2 of G.hazards)if(o2!==hz&&o2.kind==='bumper'&&overlap(hz,o2)){const t2=hz.vx;hz.vx=o2.vx;o2.vx=t2;const t3=hz.vy;hz.vy=o2.vy;o2.vy=t3;}
      if(tid!=='ufo'&&overlap(pr,hz)){hit('ob');addFloat(hz.x+6,hz.y-10,'BUMP!','#ffd23f',0.6);hz.vx=Math.sign(hz.x-P.x||1)*Math.abs(hz.vx);hz.vy=Math.sign(hz.y-P.y||1)*Math.abs(hz.vy);}continue;}
    else if(hz.kind==='sheep'){""")
rep("    else if(hz.kind==='sheep')ents.push({base:hz.y+hz.h,draw:()=>{",
r"""    else if(hz.kind==='bumper')ents.push({base:hz.y+hz.h,draw:()=>{R(b,hx,hy+hz.h,hz.w,2,'rgba(27,31,59,0.22)');b.drawImage(hz.spr,hx-1,hy-4);}});
    else if(hz.kind==='ped'&&hz.ghost)ents.push({base:hz.y+hz.h,draw:()=>{b.save();b.globalAlpha=0.55+0.35*Math.sin(tNow*3+hz.x);b.drawImage(GHOST_FR[Math.floor(hz.t*4)%2],hx-2,hy-10+Math.round(Math.sin(tNow*4+hz.x)*2));b.restore();}});
    else if(hz.kind==='sheep')ents.push({base:hz.y+hz.h,draw:()=>{""")
# the coaster train is drawn lying sideways
rep("        if(hz.state==='go'){if(hz.dir<0){",
    "        if(hz.state==='go'&&hz.rot){b.save();b.translate(Math.round(hz.x)+hz.w/2,hy+6);b.rotate(hz.dir>0?Math.PI/2:-Math.PI/2);b.drawImage(hz.spr,-12,-hz.spr.height/2);b.restore();}\n        else if(hz.state==='go'){if(hz.dir<0){")
open(f,'w',encoding='utf-8').write(s);print('p52 ok')
