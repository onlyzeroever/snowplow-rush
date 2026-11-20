# LAB rev 3d (Alex, Nov 21 01:03, on the twists):
#  1. Round-Up: "sheep are really hard to control, buggy and frustrating, sometimes trapped" -> push them with the
#     blade: a sheep just ahead of the blade walks ahead of it at the plow's speed (drawn toward the blade's middle),
#     so it goes where you drive; turn sharply and it slips off. Sheep beside or behind the plow just step aside.
#     Pressed against a pen fence a sheep slides along it to the gate and walks in. A pushed sheep that cannot move
#     hops to a free spot beside it. No more bouncing off props (they stop and slide instead).
#  2. Dig-Out: no lines round the car (pulsing frame and side bars gone); each side's drift shrinks as you dig it.
#  3. Power Cut: the old headlight style is back (fading sections stay).
#  5. Slalom: more gates (about every 190px instead of 320).
#  6. Avalanche: no rock shelters (felt like a weird tunnel); outrun the wave; the last 50px of the map are safe.
#  Present Hunt: the buried ones are SECRET PRESENTS, purple with gold ribbon, so nobody mixes them up with the
#  presents lying on the snow.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---- 1. Round-Up ----
rep("mxs=hz.horse?24:hz.stray?75:34;","mxs=hz.horse?24:hz.stray?130:34;")
rep("if(chaserFree(hz,nx,hz.y)&&(unst||mClear('sheep',hz,nx,hz.y)))hz.x=nx;else hz.vx*=-0.5;if(chaserFree(hz,hz.x,ny)&&(unst||mClear('sheep',hz,hz.x,ny)))hz.y=ny;else hz.vy*=-0.5;",
    "if(chaserFree(hz,nx,hz.y)&&(unst||mClear('sheep',hz,nx,hz.y)))hz.x=nx;else hz.vx*=hz.stray?0:-0.5;if(chaserFree(hz,hz.x,ny)&&(unst||mClear('sheep',hz,hz.x,ny)))hz.y=ny;else hz.vy*=hz.stray?0:-0.5;")
rep("MODES.roundup={name:'ROUND-UP',sub:'HERD THE SHEEP INTO THE PEN',rule:'COME FROM BEHIND TO HERD THEM',",
    "MODES.roundup={name:'ROUND-UP',sub:'HERD THE SHEEP INTO THE PEN',rule:'PUSH THE SHEEP WITH YOUR BLADE',")
rep("how:['SHEEP HAVE ESCAPED ALL OVER THE','MAP. THEY RUN AWAY FROM YOUR','PLOW, SO COME FROM BEHIND AND','STEER THEM INTO THE PEN. EACH','ONE PAYS. ALL HOME: GOLD GIFT!'],",
    "how:['SHEEP HAVE ESCAPED ALL OVER THE','MAP. NUDGE ONE WITH YOUR BLADE','AND IT WALKS AHEAD OF IT. TURN','GENTLY OR IT SLIPS OFF. GUIDE IT','INTO THE PEN. ALL HOME: GOLD GIFT!'],")

# ---- 2. Dig-Out ----
rep("for(const [lx,ly,lr] of lumps)pixCircle(b,cx+lx,cy+ly+1,Math.max(1,Math.round(lr*k)+1));b.fillStyle='#a6c2ea';for(const [lx,ly,lr] of lumps)pixCircle(b,cx+lx,cy+ly+1,Math.max(1,Math.round(lr*k)));b.fillStyle='#f4f8ff';for(const [lx,ly,lr] of lumps)pixCircle(b,cx+lx,cy+ly-1,Math.max(1,Math.round(lr*k)-1));const pu=Math.floor(tNow*3)%2;b.strokeStyle='rgba(255,176,74,'+(pu?0.9:0.5)+')';b.lineWidth=1;b.strokeRect(hz.x-6.5,hz.y-6.5,35,43);}",
    "for(const [lx,ly,lr] of lumps){const q=dgK(hz,lx,ly);if(q>0.05)pixCircle(b,cx+lx,cy+ly+1,Math.max(1,Math.round(lr*q)+1));}b.fillStyle='#a6c2ea';for(const [lx,ly,lr] of lumps){const q=dgK(hz,lx,ly);if(q>0.05)pixCircle(b,cx+lx,cy+ly+1,Math.max(1,Math.round(lr*q)));}b.fillStyle='#f4f8ff';for(const [lx,ly,lr] of lumps){const q=dgK(hz,lx,ly);if(q>0.05)pixCircle(b,cx+lx,cy+ly-1,Math.max(1,Math.round(lr*q)-1));}}")
i=s.find("if(Math.hypot(P.x-cx,P.y-cy)<130){const sp2=hz.sp||[];const mk2=")
j=s.find("text(b,'DIG ALL 4 SIDES',cx,hz.y-18,'#ffffff',{align:'center'});}",i)
assert i>0 and j>i,(i,j)
j+=len("text(b,'DIG ALL 4 SIDES',cx,hz.y-18,'#ffffff',{align:'center'});}")
s=s[:i]+"if(Math.hypot(P.x-cx,P.y-cy)<130)text(b,'DIG OUT '+(hz.sdone||0)+'/'+(hz.sact||4)+' SIDES',cx,hz.y-18,'#ffffff',{align:'center'});"+s[j:]

# ---- 3. Power Cut: the old headlights ----
rep("""    const vs=VSPEC[tool().id]||{hh:6},fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],L2=lightCone(P.f),G2=lightGlow(),fx=Math.round(P.x+fv[0]*(vs.hh-2)),fy=Math.round(P.y-cy+fv[1]*(vs.hh-2));
    x.drawImage(L2.c,fx-L2.o,fy-L2.o);x.drawImage(G2.c,Math.round(P.x)-G2.o,Math.round(P.y-cy)-G2.o);
    x.globalCompositeOperation='source-over';x.drawImage(L2.t,fx-L2.o,fy-L2.o);b.drawImage(NB2,0,cy);},""",
"""    const px=P.x,py=P.y-cy,fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f];for(let k=0;k<9;k++){const d=8+k*10,r=6+k*3.2;x.fillStyle='rgba(0,0,0,'+(0.6-k*0.045).toFixed(2)+')';pixCircle(x,Math.round(px+fv[0]*d),Math.round(py+fv[1]*d),Math.round(r));}
    x.fillStyle='rgba(0,0,0,0.6)';pixCircle(x,Math.round(px),Math.round(py),16);x.globalCompositeOperation='source-over';
    x.fillStyle='rgba(255,240,180,0.08)';for(let k=2;k<9;k+=2){const d=8+k*10,r=6+k*3.2;pixCircle(x,Math.round(px+fv[0]*d),Math.round(py+fv[1]*d),Math.round(r*0.8));}b.drawImage(NB2,0,cy);},""")

# ---- 5. Slalom: more gates ----
rep("n=Math.max(4,Math.min(12,Math.floor((g.ph-200)/320)))","n=Math.max(6,Math.min(20,Math.floor((g.ph-200)/190)))")

# ---- 6. Avalanche: no shelters ----
rep("S.sh=[];for(let y=100;y<g.ph-90;y+=360){const p=labSpot(g,30,22,y,Math.min(g.ph-50,y+300),rn,{edge:true,margin:3});if(p){S.sh.push({x:p.x,y:p.y,w:30,h:22});labBlock(g,p.x,p.y,30,5);labPaint(g,p.x-2,p.y-2,34,28);}}","S.sh=[];")
rep("if(A.fy-A.y0>=S.len||A.fy>G.ph-4)","if(A.fy-A.y0>=S.len||A.fy>G.ph-50)")
rep("rule:'SIREN? DRIVE DOWNHILL OR HIDE!'","rule:'SIREN? DRIVE AWAY DOWNHILL!'")
rep("'AVALANCHE! DRIVE DOWNHILL OR HIDE'","'AVALANCHE! DRIVE DOWNHILL!'")
rep("how:['AT THE SIREN A WALL OF SNOW','RUSHES DOWN THE MAP: DRIVE AWAY','FROM IT OR DUCK INTO A ROCK','SHELTER. DODGE THE TUMBLING','BOULDERS. CAUGHT? YOU GET BURIED.'],",
    "how:['AT THE SIREN A WALL OF SNOW','RUSHES DOWN THE MAP. DRIVE AWAY','FROM IT AND DODGE THE TUMBLING','BOULDERS. THE VERY BOTTOM IS SAFE.','CAUGHT? YOU GET BURIED.'],")

# ---- Present Hunt: secret presents ----
rep("presents:{name:'PRESENT HUNT',sub:'DIG UP THE GOLDEN PRESENTS',mod:{mode:'presenthunt'}","presents:{name:'PRESENT HUNT',sub:'DIG UP THE SECRET PRESENTS',mod:{mode:'presenthunt'}")
rep("MODES.presenthunt={name:'PRESENT HUNT',sub:'DIG UP THE GOLDEN PRESENTS',rule:'FOLLOW THE JINGLE, DIG THEM UP',",
    "MODES.presenthunt={name:'PRESENT HUNT',sub:'DIG UP THE SECRET PRESENTS',rule:'FOLLOW THE CHIME, DIG THEM UP',")
rep("how:['5 GOLDEN PRESENTS ARE BURIED','UNDER THE SNOW. LISTEN: THE','JINGLE GETS FASTER AS YOU GET','CLOSE, AND THE SNOW TWINKLES.','PLOW THE SPOT TO DIG ONE UP!'],",
    "how:['5 SECRET PRESENTS (PURPLE AND','GOLD) ARE BURIED IN THE SNOW.','THE CHIME GETS FASTER AS YOU GET','CLOSE, AND THE SNOW TWINKLES.','PLOW THE SPOT TO DIG ONE UP!'],")
rep("labPay(gp.x,gp.y-16,1.5,'GOLDEN PRESENT!','#ffd23f');","labPay(gp.x,gp.y-16,1.5,'SECRET PRESENT!','#c4a0f5');")
rep("labObj('GOLD PRESENTS',L.found,S.n);","labObj('SECRET PRESENTS',L.found,S.n);")
rep("b.drawImage(GOLDP,gp.x-4,y);","b.drawImage(SECRETP,gp.x-5,y-3);")

rep("loadSave();save.sess=(save.sess||0)+1;",r"""// ================= LAB rev 3d (Nov 21) =================
const SECRETP=spr(["....Y.Y....","...YWYWY...","....YYY....","KKKKKYKKKKK","KPPPPYPPPPK","KPpPPYPPpPK","KYYYYYYYYYK","KPPPPYPPPPK","KPpPPYPPpPK","KPPPPYPPPPK","KKKKKKKKKKK"],{P:'#8a5cd6',p:'#b48cf0',Y:'#ffd23f',W:'#ffffff'});
function dgK(hz,lx,ly){if(!hz.sp)return 1;const sd=ly<-10?0:ly>12?2:lx<0?3:1,v=hz.sp[sd];if(v==null||v<0)return 0;return 1-Math.min(1,v/(G.def.teach?0.7:0.8));}
MODES.roundup.tick=function(dt,tid,L){const S=G.lab;if(!S.pens||!S.pens.length||!S.sheep.length)return;if(L.home==null)L.home=0;
  const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],pv=Math.hypot(P.vx||0,P.vy||0),br=tid==='ufo'?null:bladeRect(tid,P.x,P.y,P.f,bladeCells()*2);
  const Z=br?(fv[1]?{x:br.x-3,y:fv[1]<0?br.y-18:br.y+br.h-2,w:br.w+6,h:20}:{x:fv[0]<0?br.x-18:br.x+br.w-2,y:br.y-3,w:20,h:br.h+6}):null;
  const loose=S.sheep.filter(h=>!h.penned);
  for(const hz of S.sheep){hz.t=99;if(hz.penned){const pn=hz.pen;hz.hx=pn.ix+pn.iw/2-4;hz.hy=pn.iy+pn.ih/2-3;hz.vx+=(hz.hx-hz.x)*2*dt;hz.vy+=(hz.hy-hz.y)*2*dt;continue;}
    hz.hx=hz.x;hz.hy=hz.y;const sx=hz.x+4.5,sy=hz.y+3;let tx=0,ty=0;const inZ=!!Z&&pv>4&&sx>Z.x&&sx<Z.x+Z.w&&sy>Z.y&&sy<Z.y+Z.h;
    if(inZ){const sp=pv*1.08+8;tx=fv[0]*sp;ty=fv[1]*sp;if(fv[1])tx+=(br.x+br.w/2-sx)*0.7;else ty+=(br.y+br.h/2-sy)*0.7;hz.pushT=(hz.pushT||0)+dt;
      if(!(hz.alert>0)){hz.alert=0.9;if(Math.random()<0.5)addFloat(sx,hz.y-8,'BAA!','#ffffff',0.6);}}
    else{hz.pushT=0;const dx=sx-P.x,dy=sy-P.y,d=Math.hypot(dx,dy);if(d<32){const k=1-d/32;tx=dx/(d||1)*(14+30*k);ty=dy/(d||1)*(14+30*k);}}
    for(const o of loose){if(o===hz)continue;const ox=o.x-hz.x,oy=o.y-hz.y,od=Math.hypot(ox,oy);if(od<9){tx-=ox/(od||1)*14;ty-=oy/(od||1)*14;}}
    for(const pn of S.pens){if(sx<pn.x-6||sx>pn.x+pn.w+6)continue;for(const [fy,inDir] of [[pn.y+6,1],[pn.y+pn.h-1,-1]]){const off=sy-fy;if(Math.abs(off)<13&&off*inDir<0&&(inZ||Math.hypot(hz.vx,hz.vy)>6)){const gx=pn.cx-sx;if(Math.abs(gx)>7)tx+=Math.sign(gx)*Math.min(45,Math.abs(gx)*3);else{tx+=gx*3;ty+=inDir*45;}}}}
    if(hz.x<14)tx+=(14-hz.x)*7;if(hz.x>G.pw-23)tx-=(hz.x-(G.pw-23))*7;if(hz.y<22)ty+=(22-hz.y)*7;if(hz.y>G.ph-28)ty-=(hz.y-(G.ph-28))*7;
    const kk=Math.min(1,dt*(inZ?14:6));hz.vx+=(tx-hz.vx)*kk;hz.vy+=(ty-hz.vy)*kk;if(hz.alert>0)hz.alert-=dt;
    if(hz.pushT>0){const mv=Math.hypot(hz.x-(hz.lx!=null?hz.lx:hz.x),hz.y-(hz.ly!=null?hz.ly:hz.y));hz.stk=mv<0.3?(hz.stk||0)+dt:0;
      if(hz.stk>0.8){hz.stk=0;for(const off of [10,-10,16,-16,22,-22]){const nx=hz.x+(fv[1]?off:0),ny=hz.y+(fv[0]?off:0);if(nx>4&&nx<G.pw-13&&ny>8&&ny<G.ph-10&&chaserFree(hz,nx,ny)&&mClear('sheep',hz,nx,ny)){hz.x=nx;hz.y=ny;hz.vx=hz.vy=0;labBurst(hz.x+4,hz.y+3,4,'snow',30);break;}}}}
    hz.lx=hz.x;hz.ly=hz.y;
    for(const pn of S.pens){if(hz.x>=pn.ix&&hz.x+hz.w<=pn.ix+pn.iw&&hz.y>=pn.iy&&hz.y+hz.h<=pn.iy+pn.ih){hz.penned=1;hz.pen=pn;L.home++;labPay(hz.x+4,hz.y-12,1,'BAA! HOME');labTime(hz.x+4,hz.y-3,3);sfx('moo',0,{rate:1.8,vol:0.6});labRing(hz.x+4,hz.y+3,10);hz.heart=1.5;
      if(L.home>=S.sheep.length)labGoldGift(P.x,P.y-38,'ALL SHEEP HOME!');break;}}}
  for(const hz of S.sheep)if(hz.heart>0)hz.heart-=dt;L.near=0;labObj('SHEEP',L.home,S.sheep.length);
  const vis=loose.filter(h=>h.y>camY-10&&h.y<camY+VIEW_H+10);
  if(vis.length){const pn=nearest(S.pens.map(q=>({x:q.cx,y:q.cy})));L.tgt=pn?{x:pn.x,y:pn.y,col:'#c98d4a'}:null;}else{const h=nearest(loose.map(q=>({x:q.x+4,y:q.y+3})));L.tgt=h?{x:h.x,y:h.y,col:'#ffffff'}:null;}};
loadSave();save.sess=(save.sess||0)+1;""")
open(f,'w',encoding='utf-8').write(s)
print('p159 lab rev 3d: blade-push sheep, prettier dig-out, old headlights, more slalom gates, no avalanche shelters, secret presents')
