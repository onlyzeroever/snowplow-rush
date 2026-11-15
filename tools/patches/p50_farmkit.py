import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# FARMLAND KIT: props for the 9 new farm jobs, a sheep flock that scatters from the plow, farm traffic that
# crosses a lane after a warning, and the farm boss chaser: the angry goose.
# ---------------------------------------------------------------------------------------------
KIT=r"""
function stoneWallSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);const cols=['#8793a8','#9aa6ba','#7a869c','#a8b2c4'];
  for(let y=1;y<h-1;y+=3)for(let x=1+((y/3|0)%2)*3;x<w-1;x+=6){R(g,x,y,Math.min(5,w-1-x),2,cols[(x*7+y*3)%4]);}R(g,0,0,w,2,PAL.W);if(h>w)R(g,0,0,2,h,PAL.W);return c;}
function churnSprite(){const c=mk(7,10),g=c.getContext('2d');R(g,1,0,5,2,K);R(g,0,2,7,8,K);R(g,1,3,5,6,'#c6d0e0');R(g,1,3,5,1,'#f4f8ff');R(g,2,0,3,1,'#8793a8');R(g,1,6,5,1,'#8793a8');return c;}
function troughSprite(){const c=mk(24,8),g=c.getContext('2d');R(g,0,0,24,8,K);R(g,1,1,22,5,'#8a5a34');R(g,2,2,20,3,'#9fd4f4');R(g,2,2,20,1,'#ffffff');R(g,2,6,2,2,K);R(g,20,6,2,2,K);return c;}
function parkedTractorSprite(a){const body=['#d8364b','#33b24a','#3f86d6'][a%3];const c=mk(18,28),g=c.getContext('2d');
  R(g,0,14,6,12,K);R(g,12,14,6,12,K);R(g,1,15,4,10,'#2a2a36');R(g,13,15,4,10,'#2a2a36');for(let y=16;y<25;y+=2){R(g,1,y,4,1,'#55607a');R(g,13,y,4,1,'#55607a');}
  R(g,2,2,4,7,K);R(g,12,2,4,7,K);R(g,3,3,2,5,'#2a2a36');R(g,13,3,2,5,'#2a2a36');R(g,4,0,10,26,K);R(g,5,1,8,24,body);R(g,5,13,8,9,'#cfe9f7');R(g,5,13,8,2,PAL.W);R(g,6,2,6,2,'#f4f8ff');R(g,5,1,8,1,PAL.W);return c;}
function trailerSprite(){const c=mk(22,40),g=c.getContext('2d');R(g,10,0,2,6,K);R(g,0,5,22,32,K);R(g,1,6,20,30,'#a8673a');for(let y=8;y<34;y+=9)for(let x=2;x<19;x+=9){R(g,x,y,8,7,K);R(g,x+1,y+1,6,5,'#e8c87a');R(g,x+1,y+1,6,1,PAL.W);R(g,x+1,y+3,6,1,'#c9a85a');}
  R(g,0,30,3,8,K);R(g,19,30,3,8,K);return c;}
function windmillSprite(){const c=mk(44,66),g=c.getContext('2d');
  for(let r=0;r<40;r++){const hw=8+Math.round(r*0.22);R(g,22-hw-1,24+r,hw*2+2,1,K);R(g,22-hw,24+r,hw*2,1,r%6<1?'#d6dee9':'#f4f8ff');}R(g,18,54,8,10,K);R(g,19,55,6,9,'#7a4a2a');R(g,13,36,5,5,K);R(g,14,37,3,3,'#8fd3ff');
  for(let r=0;r<10;r++){const hw=Math.round(r*1.1)+1;R(g,22-hw-1,15+r,hw*2+2,1,K);R(g,22-hw,15+r,hw*2,1,r<4?PAL.W:'#7a4a2a');}
  const sail=(dx,dy)=>{for(let k=3;k<21;k++){const x=22+Math.round(dx*k),y=21+Math.round(dy*k);R(g,x-2,y-2,5,5,K);}for(let k=3;k<21;k++){const x=22+Math.round(dx*k),y=21+Math.round(dy*k);R(g,x-1,y-1,3,3,(k%4<2)?'#f4f8ff':'#c98d4a');}};
  sail(0.72,-0.72);sail(-0.72,0.72);sail(0.72,0.72);sail(-0.72,-0.72);g.fillStyle=K;pixCircle(g,22,21,3);g.fillStyle='#a8673a';pixCircle(g,22,21,2);return c;}
function marqueeSprite(a){const c1=['#d8364b','#3f86d6','#33b24a'][a%3];const c=mk(60,40),g=c.getContext('2d');for(let r=0;r<16;r++){const hw=Math.round(8+r*1.38);R(g,30-hw-1,r,hw*2+2,1,K);for(let x=-hw;x<hw;x++)R(g,30+x,r,1,1,((x+60)>>2)%2?c1:'#f4f8ff');}
  R(g,0,16,60,24,K);R(g,1,16,58,23,'#f4f8ff');for(let x=1;x<59;x+=8)R(g,x,16,4,23,c1);R(g,1,16,58,3,K);R(g,22,24,16,15,K);R(g,23,25,14,14,'#3a2a20');R(g,26,0,8,3,PAL.W);R(g,29,0,2,2,K);return c;}
function sacksSprite(){const c=mk(16,10),g=c.getContext('2d');for(const [x,y] of [[0,3],[5,4],[10,3],[3,0],[8,0]]){R(g,x,y,6,6,K);R(g,x+1,y+1,4,4,'#e8d9b0');R(g,x+2,y,2,1,'#c9a85a');}R(g,3,0,5,1,PAL.W);return c;}
function sheepSprite(fr){const c=mk(11,9),g=c.getContext('2d');R(g,1,1,8,6,K);R(g,0,2,10,4,K);R(g,1,2,8,4,'#f4f8ff');R(g,2,1,6,1,'#f4f8ff');R(g,2,3,1,1,'#d6dee9');R(g,6,4,1,1,'#d6dee9');
  R(g,8,2,3,4,K);R(g,9,3,1,2,'#2a2a36');const l=fr?1:0;R(g,2+l,7,1,2,K);R(g,7-l,7,1,2,K);return c;}
function horseSprite(fr,col){const c=mk(17,13),g=c.getContext('2d');R(g,2,3,11,6,K);R(g,3,4,9,4,col);R(g,3,4,9,1,PAL.W);R(g,11,0,5,6,K);R(g,12,1,3,4,col);R(g,15,3,2,3,K);R(g,11,1,1,4,'#2a2a36');R(g,0,3,3,2,K);R(g,0,4,2,4,'#2a2a36');
  const l=fr?1:0;for(const x of [3+l,5-l,10+l,12-l])R(g,x,9,2,4,K);return c;}
function gooseSprite(fr){const c=mk(12,13),g=c.getContext('2d');R(g,6,0,4,5,K);R(g,7,1,2,3,'#f4f8ff');R(g,8,2,1,1,K);R(g,10,2,2,2,K);R(g,10,2,2,1,'#f07a1a');R(g,6,4,3,4,K);R(g,7,4,1,4,'#f4f8ff');
  R(g,0,6,10,5,K);R(g,1,7,8,3,'#f4f8ff');R(g,1,7,3,1,'#d6dee9');R(g,0,6,2,2,K);const l=fr?1:0;R(g,3+l,11,2,2,'#f07a1a');R(g,6-l,11,2,2,'#f07a1a');return c;}
function crossSprite(){const c=mk(44,16),g=c.getContext('2d');
  R(g,0,2,24,12,K);R(g,1,3,22,10,'#a8673a');for(let x=2;x<21;x+=7){R(g,x,4,6,8,K);R(g,x+1,5,4,6,'#e8c87a');R(g,x+1,5,4,1,PAL.W);}R(g,22,7,4,2,K);
  R(g,26,0,8,16,K);R(g,27,1,6,14,'#2a2a36');R(g,34,3,10,10,K);R(g,35,4,8,8,'#33b24a');R(g,35,4,8,2,PAL.W);R(g,37,6,4,4,'#cfe9f7');R(g,40,1,4,3,K);R(g,40,12,4,3,K);return c;}
SHOPS.push(['FARM SHOP','#e8c87a','#c98d4a','#33b24a'],['DAIRY','#f4f8ff','#c6d9f3','#3f86d6'],['STABLES','#c98d4a','#8a5a2c','#7a1f33'],['THE MILL','#e8d9b0','#c9a85a','#7a4a2a'],['SHOW RING','#f4f8ff','#c6d9f3','#d8364b'],['TEA ROOM','#e07a8a','#b04a5a','#13306b']);
Object.assign(PROPS,{
  stonewall:{arg:60,min:8,max:180,make:a=>stoneWallSprite(a,8),foot:a=>[0,0,a,8]},
  stonewallv:{arg:60,min:8,max:400,make:a=>stoneWallSprite(8,a),foot:a=>[0,0,8,a]},
  churn:{make:()=>churnSprite(),foot:()=>[0,4,7,6]},
  trough:{make:()=>troughSprite(),foot:()=>[0,0,24,8]},
  tractor:{arg:0,min:0,max:2,make:a=>parkedTractorSprite(a),foot:()=>[0,0,18,28]},
  trailer:{make:()=>trailerSprite(),foot:()=>[0,4,22,34]},
  windmill:{make:()=>windmillSprite(),foot:()=>[10,40,24,26]},
  marquee:{arg:0,min:0,max:2,make:a=>marqueeSprite(a),foot:()=>[0,14,60,26]},
  sacks:{make:()=>sacksSprite(),foot:()=>[0,2,16,8]}});
CHASERS.goose={name:'THE GOOSE',frames:[gooseSprite(0),gooseSprite(1)],w:10,h:6,ox:1,oy:7,speed:1.05,lines:['HONK!','HONK HONK!','HISSSSS!','HONK!!!','*FLAP FLAP*'],catchLine:'HONK!!',col:'#ffffff'};
const SHEEP_FR=[sheepSprite(0),sheepSprite(1)],HORSE_FR=[['#a8673a',0],['#a8673a',1],['#55321d',0],['#55321d',1],['#e8d9b0',0],['#e8d9b0',1]].map(([c2,f2])=>horseSprite(f2,c2));
Object.assign(HAZ,{sheep:{sheep:1},cross:{cross:1}});
"""
rep("function buildFromData(g,D,setT,ob,setCircle,paintText){",KIT+"function buildFromData(g,D,setT,ob,setCircle,paintText){")
rep("    else if(H.balls){",
    "    else if(H.sheep){const n=h[3]||5,horse=h[4]==='horse';for(let k=0;k<n;k++)g.hazards.push({kind:'sheep',horse,col:(k%3)*2,flock:h[1]*1000+h[2],x:h[1]+(k%3)*(horse?20:12),y:h[2]+((k/3)|0)*(horse?14:10),w:horse?14:9,h:horse?7:6,hx:h[1],hy:h[2],vx:0,vy:0,t:rnd(0,3),anim:rnd(0,2)});}\n"
    "    else if(H.cross){const d=h[3]||1;g.hazards.push({kind:'cross',lane:h[2],x:d>0?-50:g.pw+8,y:h[2],w:42,h:12,dir:d,per:h[4]||7,t:rnd(1,4),state:'idle',spr:crossSprite()});}\n"
    "    else if(H.balls){")

# --- update: sheep drift as a flock, scatter from the plow; farm traffic warns then crosses ---
rep("    else if(hz.kind==='chaser'){const C=hz.C;",
r"""    else if(hz.kind==='sheep'){hz.t-=dt;hz.anim+=dt;const dx=hz.x-P.x,dy=hz.y-P.y,d=Math.hypot(dx,dy);
      const fr2=hz.horse?26:44;if(d<fr2){const k=(fr2-d)/fr2*(hz.horse?40:70);hz.vx+=dx/(d||1)*k*dt*4;hz.vy+=dy/(d||1)*k*dt*4;if(!hz.baa||hz.baa<=0){hz.baa=rnd(2,4);if(Math.random()<0.4)addFloat(hz.x+4,hz.y-8,hz.horse?'NEIGH!':'BAA!','#ffffff',0.6);}}
      if(hz.baa>0)hz.baa-=dt;if(hz.t<=0){hz.t=rnd(1.5,3.5);hz.vx+=rnd(-10,10);hz.vy+=rnd(-8,8);}
      hz.vx+=(hz.hx-hz.x)*0.15*dt;hz.vy+=(hz.hy-hz.y)*0.15*dt;hz.vx*=Math.pow(0.4,dt);hz.vy*=Math.pow(0.4,dt);const sp=Math.hypot(hz.vx,hz.vy),mxs=hz.horse?24:34;if(sp>mxs){hz.vx*=mxs/sp;hz.vy*=mxs/sp;}
      const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y))hz.x=nx;else hz.vx*=-0.5;if(chaserFree(hz,hz.x,ny))hz.y=ny;else hz.vy*=-0.5;
      if(tid!=='ufo'&&overlap(pr,hz)){hit('ob');addFloat(hz.x+4,hz.y-8,hz.horse?'NEIGH!':'BAA!','#ffffff',0.7);hz.vx+=Math.sign(dx||1)*40;hz.vy+=Math.sign(dy||1)*30;}continue;}
    else if(hz.kind==='cross'){const near=Math.abs(P.y-hz.lane)<170;
      if(hz.state==='idle'){hz.t-=dt;if(hz.t<=0&&near){hz.state='warn';hz.t=1.4;hz.x=hz.dir>0?-46:G.pw+4;sfx('horn',0,{vol:0.5,rate:0.8});}}
      else if(hz.state==='warn'){hz.t-=dt;if(hz.t<=0)hz.state='go';}
      else{hz.x+=hz.dir*46*dt;if(tid!=='ufo'&&overlap(pr,{x:hz.x+2,y:hz.y+1,w:hz.w-4,h:hz.h-2})){hit('hz',SPILL_HAZARD);addFloat(P.x,P.y-22,'TOOT TOOT!','#ffd23f',0.9);}
        if((hz.dir>0&&hz.x>G.pw+4)||(hz.dir<0&&hz.x<-46)){hz.state='idle';hz.t=hz.per+rnd(-1,1);}}
      continue;}
    else if(hz.kind==='chaser'){const C=hz.C;""")
rep("    else if(hz.kind==='chaser')ents.push({base:hz.y+hz.h,draw:()=>{",
r"""    else if(hz.kind==='sheep')ents.push({base:hz.y+hz.h,draw:()=>{const mv=Math.hypot(hz.vx,hz.vy)>6?Math.floor(hz.anim*8)%2:0,fr=hz.horse?HORSE_FR[hz.col+mv]:SHEEP_FR[mv];R(b,hx,hy+hz.h-1,hz.w,2,'rgba(27,31,59,0.22)');
        if(hz.vx<-2){b.save();b.translate(hx+hz.w,0);b.scale(-1,1);b.drawImage(fr,-1,hy-(hz.horse?6:3));b.restore();}else b.drawImage(fr,hx-1,hy-(hz.horse?6:3));}});
    else if(hz.kind==='cross')ents.push({base:hz.y+hz.h,draw:()=>{if(hz.state==='warn'&&Math.floor(tNow*8)%2===0){const ex=hz.dir>0?4:G.pw-10;R(b,ex-1,hy-2,8,14,K);R(b,ex,hy-1,6,12,'#ffd23f');text(b,'!',ex+3,hy+1,'#13306b',{align:'center',outline:null});
          for(let x=hz.dir>0?14:G.pw-20;x>0&&x<G.pw;x+=hz.dir*8)R(b,x,hy+5,4,1,'rgba(255,210,63,0.6)');}
        if(hz.state==='go'){if(hz.dir<0){b.save();b.translate(Math.round(hz.x)+hz.w+1,0);b.scale(-1,1);b.drawImage(hz.spr,0,hy-2);b.restore();}else b.drawImage(hz.spr,Math.round(hz.x)-1,hy-2);}}});
    else if(hz.kind==='chaser')ents.push({base:hz.y+hz.h,draw:()=>{""")
# new ground types: dirt farm tracks, wooden decks/piers, red courts and running tracks
rep("const T_GRASS=0,T_ASPH=1,T_CONC=2,T_YEL=3,T_WHT=4,T_ICE=5,T_BLOCK=9;","const T_GRASS=0,T_ASPH=1,T_CONC=2,T_YEL=3,T_WHT=4,T_ICE=5,T_DIRT=6,T_WOOD=7,T_RED=8,T_BLOCK=9;")
rep("      case T_YEL:return [0xf2,0xd1,0x4a];case T_WHT:return [0xec,0xef,0xf4];",
    "      case T_YEL:return [0xf2,0xd1,0x4a];case T_WHT:return [0xec,0xef,0xf4];\n"
    "      case T_DIRT:return n<3?[0x8a,0x6a,0x4a]:n<6?[0x7a,0x5a,0x3c]:[0x96,0x76,0x54];\n"
    "      case T_WOOD:return y%6===0?[0x6b,0x4a,0x2c]:(x+((y/6|0)*13))%24===0?[0x7a,0x55,0x33]:n<4?[0xa8,0x7a,0x4a]:[0x9a,0x6e,0x40];\n"
    "      case T_RED:return n<3?[0xc8,0x52,0x4e]:[0xb4,0x44,0x42];")
rep("const GROUND_T={grass:T_GRASS,asph:T_ASPH,conc:T_CONC,yel:T_YEL,wht:T_WHT,ice:T_ICE};","const GROUND_T={grass:T_GRASS,asph:T_ASPH,conc:T_CONC,yel:T_YEL,wht:T_WHT,ice:T_ICE,dirt:T_DIRT,wood:T_WOOD,red:T_RED};")
open(f,'w',encoding='utf-8').write(s);print('p50 ok')
