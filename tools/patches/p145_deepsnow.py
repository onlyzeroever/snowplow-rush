# p145 (Alex, Nov 20 21:21): "the snow doesn't feel thicker" in the Blizzard Weekend.
# Before: "thicker" only meant snow falling back 40% faster as random specks. Now the Blizzard has DEEP SNOW:
#  - the plow bogs down while it pushes deep snow (by machine weight: shovel ~20% slower, Monster ~11%),
#    with a rhythmic chug, and a thump + burst of snow each time the blade bites into a fresh drift;
#  - a much bigger pile on the blade, clumps spilling off the ends, an engine that labours under load;
#  - taller trench walls (3 px face + lip + 3 px shadow) and wind-sculpted ripples on the snow;
#  - gusts blow loose snow back into your lanes from the windward side (dusting only: cleared stays cleared);
#  - a heavier storm: far / mid / near snowfall layers, a light whiteout veil, spindrift streaming over the
#    ground, frost at the screen edges, a stronger steady wind between gusts;
#  - Blizzard jobs get extra time to cover the slower plowing (set from bot runs).
import sys
f=sys.argv[1];s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt,(a[:90],n)
    s=s.replace(a,b)

# ---- event definition: deep snow on, card says so ----
rep("blizzard:{name:'BLIZZARD WEEKEND',sub:'GUSTS, SQUALLS, DOUBLE COINS',mod:{snow:1.4,value:2,squall:11,gust:1},",
    "blizzard:{name:'BLIZZARD WEEKEND',sub:'DEEP SNOW, GUSTS, DOUBLE COINS',mod:{snow:1.4,value:2,squall:11,gust:1,deep:1},")
rep("if(m.gust)c.gust=1;",
    "if(m.gust)c.gust=1;if(m.deep){c.deep=1;c.time=Math.round(L.time*(1+DEEP_TIME*deepDrag(TOOLS[useIdx()].id)));}")

# ---- the machine: drag, chug, bite ----
rep("const gust=!!(run.bz&&run.bz.phase==='blow'),full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1);",
    "const gust=!!(run.bz&&run.bz.phase==='blow'),full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1)*(G.def.deep?deepSlow(tid,dt):1);")
rep("  const got=acc.got,cnt=acc.cnt;",
    "  const got=acc.got,cnt=acc.cnt;if(G.def.deep)deepPush(tid,got,dt,br,moving);")
rep("sfx('scrape',90);run.sprayAcc+=got;const n=Math.min(6,Math.floor(run.sprayAcc/3));run.sprayAcc-=n*3;for(let k=0;k<n;k++)spray(br,P.f,tid);}",
    "sfx('scrape',90);run.sprayAcc+=got;const sd=G.def.deep?2:3,n=Math.min(G.def.deep?10:6,Math.floor(run.sprayAcc/sd));run.sprayAcc-=n*sd;for(let k=0;k<n;k++)spray(br,P.f,tid);"
    "if(G.def.deep&&run.dpush>0.45&&Math.random()<dt*16)deepSpill(br,P.f);}")
# sound: the scrape gets heavier and lower, the engine labours and chugs
rep("loopSet(isKidTool(tid)?'scrape_s':'scrape_l',run.scrapeLvl*0.55,0.9+0.2*Math.min(1,Math.hypot(P.vx,P.vy)/full));",
    "{const dp=G.def.deep&&run.dpush||0;loopSet(isKidTool(tid)?'scrape_s':'scrape_l',run.scrapeLvl*0.55*(1+0.6*dp),(0.9+0.2*Math.min(1,Math.hypot(P.vx,P.vy)/full))*(1-0.14*dp));}")
rep("loopSet('engine',0.16+0.22*sr,(tid==='tractor'?1.1:tid==='truck'?0.85:tid==='snowcat'?0.66:tid==='rotary'?0.6:tid==='icebreaker'?0.5:tid==='loader'?0.8:0.75)+0.45*sr);}",
    "const dp2=G.def.deep&&run.dpush||0;loopSet('engine',0.16+0.22*sr+0.16*dp2,((tid==='tractor'?1.1:tid==='truck'?0.85:tid==='snowcat'?0.66:tid==='rotary'?0.6:tid==='icebreaker'?0.5:tid==='loader'?0.8:0.75)+0.45*sr)*(1-0.17*dp2+0.05*dp2*Math.sin(tNow*13)));}")
# a much bigger pile on the blade
rep(",pl=Math.min(4,Math.round(P.load*4));",
    ",pl=G.def.deep?Math.min(isKidTool(tid)?5:7,Math.round(P.load*7)):Math.min(4,Math.round(P.load*4));")
# snow clumps
rep("      default:{const sz=k>0.8?0:",
    "      case 'clump':{R(b,px-1,py-1,3,3,'#ffffff');R(b,px-1,py+1,3,1,'#c6d9f3');R(b,px+1,py-1,1,2,'#dfe9f8');R(b,px,py-2,2,1,'#ffffff');if(p.z>1)R(b,px-1,Math.round(p.y)+2,3,1,'rgba(110,140,190,0.35)');}break;\n"
    "      default:{const sz=k>0.8?0:")

# ---- the snow: taller trench walls, wind ripples ----
rep("""  const ai=i-g.cols,above=cy>0?g.depth[ai]:0,aboveB=cy>0?g.type[ai]===T_BLOCK:true;
  const data=g.img.data,pw=g.pw;""",
"""  const ai=i-g.cols,above=cy>0?g.depth[ai]:0,aboveB=cy>0?g.type[ai]===T_BLOCK:true;
  const DP=g.def&&g.def.deep;let below2=1,below2B=true,above2=0,above2B=true,left=0,leftB=true;
  if(DP){if(cy+2<g.rows){below2=g.depth[i+2*g.cols];below2B=g.type[i+2*g.cols]===T_BLOCK;}if(cy>1){above2=g.depth[i-2*g.cols];above2B=g.type[i-2*g.cols]===T_BLOCK;}if(cx>0){left=g.depth[i-1];leftB=g.type[i-1]===T_BLOCK;}}
  const data=g.img.data,pw=g.pw;""")
rep("if(!blocked&&sy===1&&d>0.55&&below<0.3&&!belowB)c=LOOK==='i'?SN_I3:EDGEC;data[o]=c[0];",
    "if(!blocked&&sy===1&&d>0.55&&below<0.3&&!belowB)c=LOOK==='i'?SN_I3:EDGEC;"
    "else if(DP&&!blocked&&d>0.55){if(below<0.3&&!belowB)c=DS_F1;else if(below>0.55&&!belowB&&below2<0.3&&!below2B)c=sy===1?DS_F0:DS_LIP;else if(sy===0&&above<0.3&&!aboveB)c=DS_LIP;}"
    "data[o]=c[0];")
rep("let m=1;if(sy===0&&above>0.55&&!aboveB)m=0.72;",
    "let m=1;if(sy===0&&above>0.55&&!aboveB)m=DP?0.6:0.72;else if(DP){if(above>0.55&&!aboveB)m=0.76;else if(sy===0&&above2>0.55&&!above2B)m=0.9;}if(DP&&sx===0&&left>0.55&&!leftB)m*=0.86;")
rep("  const cx=i%g.cols;paintCell(g,cx,cy);paintCell(g,cx,cy-1);paintCell(g,cx,cy+1);if(g.bareDep)",
    "  const cx=i%g.cols;paintCell(g,cx,cy);paintCell(g,cx,cy-1);paintCell(g,cx,cy+1);if(g.def&&g.def.deep){paintCell(g,cx,cy-2);paintCell(g,cx,cy+2);paintCell(g,cx+1,cy);}if(g.bareDep)")
rep("function snowCol(px,py,marked,def,def2,g){\n",
    "function snowCol(px,py,marked,def,def2,g){\n"
    "  if(g&&g.def&&g.def.deep&&LOOK==='x'){const dv=g.drift?g.drift[py*g.pw+px]:0;if(dv===3)return SN_X2;if(dv===2)return SN_X1;const r=dsRip()[(py&255)*180+(px<0?0:px>179?179:px)];return r===3?SN_WH:r===2?SN_W2:r===1?SN_W1:marked?SN_W1:SN_W0;}\n")

# ---- gusts blow loose snow back into your lanes; a steady wind between gusts ----
rep("run.snowAcc+=G.def.snowfall*1.2*dt;}}",
    "run.snowAcc+=G.def.snowfall*1.2*dt;if(G.def.deep)deepDrift(z.dir,dt);}}")
rep("if(z.phase==='calm'){z.wind+=(12*z.dir-z.wind)*Math.min(1,dt*2);",
    "if(z.phase==='calm'){z.wind+=((G.def.deep?28:12)*z.dir-z.wind)*Math.min(1,dt*2);")
rep("for(const f2 of BZF){f2.x+=(z.wind*f2.k)*dt;f2.y+=f2.vy*dt;if(f2.x>W+4)f2.x-=W+8;if(f2.x<-4)f2.x+=W+8;if(f2.y>HUD_H+VIEW_H)f2.y=HUD_H-2;}}",
    "for(const f2 of BZF){f2.x+=(z.wind*f2.k)*dt;f2.y+=f2.vy*dt;if(f2.x>W+4)f2.x-=W+8;if(f2.x<-4)f2.x+=W+8;if(f2.y>HUD_H+VIEW_H)f2.y=HUD_H-2;}bzMore(dt,z);}")

# ---- the storm on screen ----
rep("function drawBlizzard(){const z=run.bz;if(!z||!G||!G.def.gust)return;const blow=z.phase==='blow';",
    "function drawBlizzard(){const z=run.bz;if(!z||!G||!G.def.gust)return;const blow=z.phase==='blow';bzBack(z);")
rep("  if(z.phase==='warn'&&Math.floor(tNow*6)%2===0){for(let r2=0;r2<4;r2++)",
    "  bzFront(z);\n  if(z.phase==='warn'&&Math.floor(tNow*6)%2===0){for(let r2=0;r2<4;r2++)")

rep("function updatePlay(dt){", r"""// ---- deep snow (Blizzard): the plow bogs down while it pushes, by machine weight ----
const DEEP_DRAG={shovel:0.25,pusher:0.25,blower:0.24,tractor:0.24,truck:0.22,super:0.2,loader:0.18,snowcat:0.17,rotary:0.15,icebreaker:0.13,monster:0.12,jet:0.12,mech:0.14,dragon:0.1,ufo:0.06},DEEP_TIME=0.65;
const DS_F0=[0xdc,0xe8,0xf8],DS_F1=[0xc4,0xd6,0xf0],DS_LIP=[0xff,0xff,0xff];
function deepDrag(tid){const k=DEEP_DRAG[tid];return k==null?0.2:k;}
function deepSlow(tid,dt){const r=run;if(r.dsk==null){r.dsk=1;r.dpush=0;r.dlow=1;r.biteT=-9;}
  const tgt=1-deepDrag(tid)*r.dpush;r.dsk+=(tgt-r.dsk)*Math.min(1,dt*(tgt<r.dsk?7:4));
  return Math.max(0.55,r.dsk*(r.dpush>0.4?1-0.05*(0.5+0.5*Math.sin(tNow*13)):1));}
function deepPush(tid,got,dt,br,moving){const r=run;if(r.dsk==null)return;
  const raw=Math.min(1,got/Math.max(0.5,bladeCells()*Math.max(8,moveSpeed())*dt*0.5));r.dpush+=(raw-r.dpush)*Math.min(1,dt*10);
  if(raw<0.2)r.dlow+=dt;else if(raw>0.55&&moving){if(r.dlow>0.35&&tNow-r.biteT>0.6){r.biteT=tNow;r.dsk=Math.max(0.6,r.dsk-0.1);deepBite(br,P.f);}r.dlow=0;}}
function deepBite(br,f){const fv=[[0,-1],[1,0],[0,1],[-1,0]][f],cx=br.x+br.w/2,cy=br.y+br.h/2,hz=f===0||f===2,half=(hz?br.w:br.h)/2;
  for(let k=0;k<12;k++){const o=rnd(-half,half);particles.push({x:cx+(hz?o:0)+fv[0]*3,y:cy+(hz?0:o)+fv[1]*3,vx:fv[0]*rnd(20,55)+rnd(-16,16),vy:fv[1]*rnd(20,55)+rnd(-16,16),z:2,vz:rnd(40,80),life:0.75,t:0,kind:k%3?'snow':'clump'});}
  sfx('crunch',120,{vol:0.5,rate:0.82});shake=Math.max(shake,0.05);buzz(8);
  if(!run.dsTip&&(save.dsTips||0)<3){run.dsTip=1;save.dsTips=(save.dsTips||0)+1;addFloat(P.x,P.y-30,'DEEP SNOW!','#9fd8ff',1.3);}}
function deepSpill(br,f){const e=(f===0||f===2)?(Math.random()<0.5?[br.x,br.y+br.h/2,-1,0]:[br.x+br.w,br.y+br.h/2,1,0]):(Math.random()<0.5?[br.x+br.w/2,br.y,0,-1]:[br.x+br.w/2,br.y+br.h,0,1]);
  particles.push({x:e[0],y:e[1],vx:e[2]*rnd(25,60)+rnd(-6,6),vy:e[3]*rnd(25,60)+rnd(-6,6),z:3,vz:rnd(35,70),life:0.8,t:0,kind:'clump'});}
// gusts blow loose snow off the drifts into your lanes, from the windward side (dusting only: under the clear line)
function deepDrift(dir,dt){const g=G,cols=g.cols,r0=Math.max(1,Math.floor(camY/2)),r1=Math.min(g.rows-2,Math.floor((camY+VIEW_H)/2));let n=Math.round(3200*dt);
  while(n-->0){const cy=r0+((Math.random()*(r1-r0))|0),cx=2+((Math.random()*(cols-4))|0);let i=cy*cols+cx;if(g.type[i]===T_BLOCK||g.depth[i]<0.55)continue;
    // a streak of loose snow blows off this drift, downwind, into the cleared ground next to it
    for(let k=0,amt=0.3;k<4;k++,amt-=0.06){const j=i+dir;if(j%cols===0||j%cols===cols-1||g.type[j]===T_BLOCK)break;const dj=g.depth[j];
      if(dj>=0.3){if(dj>=0.55&&k===0){i=j;continue;}break;}setDepth(g,j,Math.min(0.42,dj+amt));i=j;if(Math.random()<0.35)break;}}}
// wind ripples (sastrugi) on deep snow: one 180 x 256 table, tiled down the map
let DS_RIP=null;function dsRip(){if(DS_RIP)return DS_RIP;const t=new Uint8Array(180*256),dn=(x,y)=>Math.sin(x*0.05+Math.sin(y*0.045)*2.2)+Math.sin(y*0.098+Math.sin(x*0.03)*1.4);
  for(let y=0;y<256;y++)for(let x=0;x<180;x++){const n=dn(x,y);t[y*180+x]=n>1.2?(dn(x,y-1)<=1.2?3:n>1.55?2:1):0;}return DS_RIP=t;}
// the storm: far / near snowfall layers, spindrift over the ground, a whiteout veil and frost at the edges
const BZ_FAR=[],BZ_NEAR=[],BZ_SPIN=[];let FROSTV=null;
for(let i=70;i<120;i++)BZF.push({x:0,y:0,k:0.6+(i%5)*0.15,vy:22+(i%7)*6,d:i%3===0?2:1});
for(let i=0;i<130;i++)BZ_FAR.push({x:(i*29)%W,y:HUD_H+(i*47)%VIEW_H,k:0.35+(i%4)*0.08,vy:14+(i%5)*3});
for(let i=0;i<20;i++)BZ_NEAR.push({x:(i*61)%W,y:HUD_H+(i*89)%VIEW_H,k:1.25+(i%3)*0.15,vy:70+(i%4)*12,ph:i*1.3});
for(let i=0;i<6;i++)BZ_SPIN.push({x:(i*53)%W-40,y:0,n:14+(i%3)*6,ph:i*2.1,set:0});
function bzMore(dt,z){for(const f2 of BZ_FAR){f2.x+=z.wind*f2.k*dt;f2.y+=f2.vy*dt;if(f2.x>W+2)f2.x-=W+4;if(f2.x<-2)f2.x+=W+4;if(f2.y>HUD_H+VIEW_H)f2.y=HUD_H-1;}
  for(const f2 of BZ_NEAR){f2.x+=(z.wind*f2.k+Math.sin(tNow*2+f2.ph)*8)*dt;f2.y+=f2.vy*dt;if(f2.x>W+12)f2.x-=W+24;if(f2.x<-12)f2.x+=W+24;if(f2.y>HUD_H+VIEW_H+3){f2.y=HUD_H-3;f2.x=(f2.x*7+53)%W;}}
  for(const s2 of BZ_SPIN){const yy=VIEW_Y+s2.y-camY;if(!s2.set||yy<VIEW_Y-6||yy>VIEW_Y+VIEW_H+6){s2.set=1;s2.y=camY+8+((s2.ph*97+tNow*31)%(VIEW_H-16));}
    s2.x+=z.wind*1.25*dt;const L2=s2.n*4;if(s2.x>W+8)s2.x=-L2-((s2.ph*41)%60);if(s2.x<-L2-70)s2.x=W+((s2.ph*29)%40);}}
function bzBack(z){const blow=z.phase==='blow';
  if(!blow){b.fillStyle='rgba(205,220,244,'+(0.07+0.03*Math.sin(tNow*0.9)).toFixed(3)+')';b.fillRect(0,HUD_H,W,VIEW_H);}
  b.fillStyle='rgba(150,172,212,0.6)';for(const f2 of BZ_FAR)b.fillRect(Math.round(f2.x),Math.round(f2.y),1,1);
  const a=blow?0.62:0.42;for(const s2 of BZ_SPIN){const y0=VIEW_Y+s2.y-camY;for(let j=0;j<s2.n;j++){const x=Math.round(s2.x+j*4),y=Math.round(y0+Math.sin(j*0.55+tNow*4+s2.ph)*2.2);if(x<-4||x>W+4||y<VIEW_Y||y>VIEW_Y+VIEW_H)continue;
    const k2=a*Math.sin(Math.PI*(j+0.5)/s2.n);b.fillStyle='rgba(255,255,255,'+k2.toFixed(3)+')';b.fillRect(x,y,4,1);b.fillStyle='rgba(120,150,200,'+(k2*0.55).toFixed(3)+')';b.fillRect(x+1,y+1,4,1);}}}
function bzFront(z){const blow=z.phase==='blow';
  for(const f2 of BZ_NEAR){const x=Math.round(f2.x),y=Math.round(f2.y),len=Math.min(12,Math.round(Math.abs(z.wind)*f2.k/16));
    if(len>=3){const x0=z.wind>0?x-len:x;b.fillStyle='rgba(255,255,255,0.85)';b.fillRect(x0,y,len,2);b.fillStyle='rgba(110,140,190,0.45)';b.fillRect(x0+1,y+2,len,1);}
    else{b.fillStyle='rgba(110,140,190,0.5)';b.fillRect(x,y+2,2,1);b.fillRect(x+2,y,1,2);b.fillStyle='rgba(255,255,255,0.9)';b.fillRect(x-1,y,3,1);b.fillRect(x,y-1,1,3);b.fillStyle='#ffffff';b.fillRect(x,y,2,2);}}
  if(!FROSTV)FROSTV=frostVig();b.globalAlpha=blow?0.9:0.6;b.drawImage(FROSTV,0,HUD_H);b.globalAlpha=1;}
function frostVig(){const c=mk(W,VIEW_H),g=c.getContext('2d');let sd=1234567;const rr=()=>((sd=(sd*1103515245+12345)&0x7fffffff)/0x7fffffff);
  for(let y=0;y<VIEW_H;y++)for(let x=0;x<W;x++){const e=Math.min(x,W-1-x,y*1.6,(VIEW_H-1-y)*1.6);if(e>=12)continue;const p=Math.pow(1-e/12,1.7);
    g.fillStyle='rgba(150,182,230,'+(0.22*p).toFixed(3)+')';g.fillRect(x,y,1,1);
    if(rr()<p*0.8){const v=rr();g.fillStyle=v<0.4?'rgba(255,255,255,0.92)':v<0.75?'rgba(190,212,242,0.88)':'rgba(128,162,214,0.75)';g.fillRect(x,y,1,1);}}return c;}
function updatePlay(dt){""")
open(f,'w').write(s)
