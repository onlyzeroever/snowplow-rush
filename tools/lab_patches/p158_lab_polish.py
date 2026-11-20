# LAB rev 3c (Alex, Nov 21 00:34): UI and feel pass on the new modes.
#  - Objective box: the gold-gift icon is the gold present, vertically centred with room to the border; a green tick
#    once the gift is won; in Present Hunt the icon bobs faster as you get closer (the HOT/WARM/COLD words are gone).
#  - Intro card bonus line uses the gold present too.
#  - Present Hunt: the hint sound is a chime (star1) that gets louder, higher and faster as you close in (the old
#    tick was too quiet to hear on a phone).
#  - Yeti: prefers open ground (cells next to walls, props and the map sides cost more), leaps half as far (40-75px).
#  - Snowball Roll: after a smash (or at the start) you roll a new ball by plowing fresh snow; a ball wedged in a
#    prop, or a small one knocked hard, crumbles (no pay) so you can roll another; the map edges slope the ball back
#    toward the middle.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---- objective box + card icon ----
rep("panel(2,VIEW_Y+2,w+(M.bonus?10:0),h,done?'#3a5a12':'#13306b',done?'#ffd23f':M.col);if(M.bonus)b.drawImage(SPR.present,2+w,VIEW_Y+6+(h>20?3:0));",
    "panel(2,VIEW_Y+2,w+(M.bonus?12:0),h,done?'#3a5a12':'#13306b',done?'#ffd23f':M.col);if(M.bonus){const L0=run.lab||{},pr=L0.prox||0,ix=2+w+1,iy=VIEW_Y+2+Math.round((h-8)/2)-(pr>0?Math.round(Math.abs(Math.sin(tNow*(3+pr*12)))*(1+pr*2)):0);b.drawImage(GOLDP,ix,iy);"
    "if(L0.gift){R(b,ix+4,iy+4,5,5,K);R(b,ix+5,iy+6,1,1,'#7fe08a');R(b,ix+6,iy+7,1,1,'#7fe08a');R(b,ix+7,iy+5,1,2,'#7fe08a');}}")
rep("if(M.bonus){const bw2=textW(M.bonus);b.drawImage(SPR.present,Math.round(W/2-bw2/2-6),y+31);","if(M.bonus){const bw2=textW(M.bonus);b.drawImage(GOLDP,Math.round(W/2-bw2/2-6),y+31);")

# ---- Present Hunt: chime, no hot/cold words, proximity for the icon ----
rep("L.nd=nd;if(near&&nd<180){L.jt-=dt;if(L.jt<=0){const k=nd/180;L.jt=0.18+k*1.1;sfx('tick',0,{rate:1.7+(1-k)*0.6,vol:0.12+0.4*(1-k)});near.ping=0.25;}}",
    "L.nd=nd;L.prox=near&&nd<180?1-nd/180:0;if(near&&nd<180){L.jt-=dt;if(L.jt<=0){const k=nd/180;L.jt=0.22+k*1.0;sfx('star1',0,{rate:0.95+(1-k)*0.45,vol:0.35+0.6*(1-k)});near.ping=0.25;}}")
rep("labObj('GOLD PRESENTS',L.found,S.n,near&&nd<180?(nd<45?'HOT!':nd<100?'WARM':'COLD'):'');","labObj('GOLD PRESENTS',L.found,S.n);")

# ---- Yeti: open ground, shorter leaps ----
rep("  for(let k=0;k<n;k++){if(pass[k]&&d[k]>=1e9)pass[k]=0;if(pass[k])F[k]=-1.3*d[k];}",
    "  for(let k=0;k<n;k++){if(pass[k]&&d[k]>=1e9)pass[k]=0;if(pass[k])F[k]=-1.3*d[k];}\n"
    "  const cl=new Uint8Array(n).fill(9),cq=[];for(let k=0;k<n;k++){const x=k%cols,y=(k/cols)|0;if(!pass[k]){cl[k]=0;cq.push(k);}else if(x===0||x===cols-1){cl[k]=1;cq.push(k);}}\n"
    "  for(let i=0;i<cq.length;i++){const k=cq[i],x=k%cols,y=(k/cols)|0;if(cl[k]>=4)continue;for(const [ax,ay] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+ax,ny=y+ay;if(nx<0||ny<0||nx>=cols||ny>=rows)continue;const nk=ny*cols+nx;if(cl[nk]>cl[k]+1){cl[nk]=cl[k]+1;cq.push(nk);}}}")
rep("  return {cs,cols,rows,y0,F,pass};}",
    "  for(let k=0;k<n;k++)if(pass[k])F[k]+=Math.max(0,4-cl[k])*1.8;\n  return {cs,cols,rows,y0,F,pass};}")
rep("if(dd<60||dd>125)continue;","if(dd<40||dd>75)continue;")
rep("Y.leap={x0:Y.x,y0:Y.y,x1,y1,t:0,dur:0.6};","Y.leap={x0:Y.x,y0:Y.y,x1,y1,t:0,dur:0.45};")

# ---- Snowball Roll: roll a new ball from plowed snow, crumbling, edge slope ----
rep("  tick(dt,tid,L){if(L.gone>0){L.gone-=dt;if(L.gone<=0){const nb=rollSpawn(L,tid);if(nb)L.ball=nb;else L.gone=0.3;}return;}\n    let B=L.ball;if(!B){B=L.ball=rollSpawn(L,tid);if(!B)return;}",
    "  tick(dt,tid,L){if(L.need==null){L.need=1;L.acc=0;}if(L.gone>0){L.gone-=dt;if(L.gone<=0){L.need=1;L.acc=0;}return;}\n"
    "    if(L.need){L.acc+=run.lastGot||0;const need=ROLL_NEED;labObj('NEW BALL',Math.min(100,Math.floor(L.acc/need*100))+'%',null,'PLOW SNOW');if(L.acc>=need){const nb=rollSpawn(L,tid);if(nb){nb.snow=need*0.6;nb.r=Math.min(26,5+Math.sqrt(nb.snow)*0.3);L.ball=nb;L.need=0;addFloat(nb.x,nb.y-14,'NEW SNOWBALL!','#ffffff',1);sfx('flump',0,{rate:1.2,vol:0.6});labBurst(nb.x,nb.y,8,'snow',40);}}return;}\n"
    "    let B=L.ball;if(!B){L.need=1;L.acc=0;return;}")
rep("if(pushed){const o=rollHit(B,B.x,B.y);if(o){if(B.r>=8&&o!=='edge')rollSmash(B,L,Math.hypot(P.vx||0,P.vy||0));else{B.x=clamp(B.x,B.r+1,G.pw-B.r-1);B.y=clamp(B.y,B.r+1,G.ph-B.r-1);}if(L.gone>0)return;}}",
    "if(pushed){const o=rollHit(B,B.x,B.y);if(o){if(o==='edge'){B.x=clamp(B.x,B.r+1,G.pw-B.r-1);B.y=clamp(B.y,B.r+1,G.ph-B.r-1);}else if(B.r>=8)rollSmash(B,L,Math.hypot(P.vx||0,P.vy||0));else rollCrumble(B,L);if(L.gone>0)return;}}\n"
    "    {const r3=B.r*0.82;for(const ob of G.obstacles){const bx3={x:B.x-r3,y:B.y-r3,w:r3*2,h:r3*2};if(!overlap(bx3,ob))continue;const ox=Math.min(bx3.x+bx3.w,ob.x+ob.w)-Math.max(bx3.x,ob.x),oy=Math.min(bx3.y+bx3.h,ob.y+ob.h)-Math.max(bx3.y,ob.y);\n      if(Math.min(ox,oy)>4){rollCrumble(B,L);return;}if(ox<oy){const sgn=B.x<ob.x+ob.w/2?-1:1;B.x+=sgn*(ox+0.1);if(B.vx*sgn<0)B.vx=0;}else{const sgn=B.y<ob.y+ob.h/2?-1:1;B.y+=sgn*(oy+0.1);if(B.vy*sgn<0)B.vy=0;}}}\n"
    "    {const m=B.r+24;if(B.x<m)B.vx+=70*dt;if(B.x>G.pw-m)B.vx-=70*dt;if(B.y<m)B.vy+=70*dt;if(B.y>G.ph-m)B.vy-=70*dt;}")
rep("      if(o!=='edge'&&imp>34&&B.r>=8){rollSmash(B,L,imp);return;}",
    "      if(o!=='edge'&&imp>34&&B.r>=8){rollSmash(B,L,imp);return;}if(o!=='edge'&&imp>34){rollCrumble(B,L);return;}")
rep("MODES.snowroll={name:'SNOWBALL ROLL',sub:'GROW A GIANT SNOWBALL',rule:'PUSH IT, GROW IT, SMASH IT',",
    "MODES.snowroll={name:'SNOWBALL ROLL',sub:'GROW A GIANT SNOWBALL',rule:'PLOW A BALL, ROLL IT, SMASH IT',")
rep("how:['PUSH THE SNOWBALL WITH YOUR PLOW:','IT ROLLS ON BY ITSELF AND GROWS','ON FRESH SNOW. SEND IT HARD INTO','A WALL TO SMASH IT AND CASH IN.','A SOFT KNOCK JUST BREAKS BITS OFF.'],",
    "how:['PLOW SNOW AND A SNOWBALL ROLLS UP','IN FRONT OF YOU. PUSH IT: IT ROLLS','ON AND GROWS ON FRESH SNOW. SEND','IT HARD INTO A WALL TO CASH IN.','THEN PLOW UP A NEW ONE!'],")

# ---- Black Ice (Alex 00:40: "hard to hold a drift for that long"): tiers sooner, wider drift angle, longer grace ----
rep("const tier=L.dr>=3?3:L.dr>=1.6?2:L.dr>=0.6?1:0;if(tier>(L.tier||0))","const tier=driftTier(L.dr);if(tier>(L.tier||0))")
rep("else if(L.dr>0){L.off+=dt;if(L.off>0.25){if(L.dr>=0.6){const tier=L.dr>=3?3:L.dr>=1.6?2:1;","else if(L.dr>0){L.off+=dt;if(L.off>0.4){if(L.dr>=DRIFT_T[0]){const tier=driftTier(L.dr);")
rep("const mult=1+0.25*(L.ch-1),u=Math.min(3,0.25*L.dr*L.dr+0.3*L.dr)*mult;","const mult=1+0.25*(L.ch-1),u=driftPay(L.dr)*mult;")
rep("over(cy){const L=run.lab;if(L&&L.dr>0.6){const tier=L.dr>=3?3:L.dr>=1.6?2:1,","over(cy){const L=run.lab;if(L&&L.dr>DRIFT_T[0]){const tier=driftTier(L.dr),")
rep("c=Math.round(labUnit()*Math.min(3,0.25*L.dr*L.dr+0.3*L.dr)*mult);","c=Math.round(labUnit()*driftPay(L.dr)*mult);")
rep("f2=tier===3?1:tier===2?(L.dr-1.6)/1.4:(L.dr-0.6)/1;","f2=tier===3?1:(L.dr-DRIFT_T[tier-1])/(DRIFT_T[tier]-DRIFT_T[tier-1]);")
rep("ice=G.depth[fi]<CLEAR_T,drifting=ice&&sp>moveSpeed()*0.4&&cos<0.85&&!(P.stun>0);","ice=G.depth[fi]<CLEAR_T,drifting=ice&&sp>moveSpeed()*0.35&&cos<0.92&&!(P.stun>0);")

# ---- Snow Day (Alex 00:40: "if the snow is coming down twice as fast surely parts should be getting re-covered?") ----
rep("    labObj('MEGA',L.n,3,L.mega>0?Math.ceil(L.mega)+'S LEFT':Math.floor(L.meter*100)+'%');},",
    "    {const y0=Math.max(0,Math.floor(camY/2)-10),y1=Math.min(G.rows-1,Math.floor((camY+VIEW_H)/2)+10),K2=Math.round(150*dt*30);for(let q=0;q<K2;q++){const cy=y0+((Math.random()*(y1-y0+1))|0),cx=(Math.random()*G.cols)|0,i=cy*G.cols+cx;if(G.type[i]===T_BLOCK||(G.nc&&G.nc[i]))continue;const d=G.depth[i];if(d<0.92)setDepth(G,i,Math.min(1,d+0.12));}}\n"
    "    labObj('MEGA',L.n,3,L.mega>0?Math.ceil(L.mega)+'S LEFT':Math.floor(L.meter*100)+'%');},")
rep("  screen(){const L=run.lab;if(!L||L.meter==null)return;const x=W/2-40,",
    "  screen(){const L=run.lab;if(!L||L.meter==null)return;sdFlakes();const x=W/2-40,")
rep("how:['THE SNOW COMES DOWN TWICE AS','FAST. EVERY SCOOP FILLS THE SNOW','DAY METER. FULL: 8 SECONDS OF','MEGA BLADE, MORE SPEED AND','DOUBLE COINS. COINS X1.5.'],",
    "how:['IT IS SNOWING HARD: CLEARED','GROUND FILLS BACK IN. EVERY SCOOP','FILLS THE SNOW DAY METER. FULL:','8 SECONDS OF MEGA BLADE, SPEED','AND DOUBLE COINS. COINS X1.5.'],")
rep("MODES.snowday={name:'SNOW DAY',sub:'FILL THE METER, GO MEGA',rule:'PLOW TO FILL THE METER',","MODES.snowday={name:'SNOW DAY',sub:'FILL THE METER, GO MEGA',rule:'IT FILLS BACK IN: KEEP PLOWING',")

rep("loadSave();save.sess=(save.sess||0)+1;",r"""// ================= LAB rev 3c (Nov 21) =================
const ROLL_NEED=40,DRIFT_T=[0.5,1.1,1.8];
function driftTier(d){return d>=DRIFT_T[2]?3:d>=DRIFT_T[1]?2:d>=DRIFT_T[0]?1:0;}
function driftPay(d){return Math.min(3,0.7*d*d+0.4*d);}
const SDF=[];function sdFlakes(){if(!SDF.length)for(let k=0;k<70;k++)SDF.push({x:Math.random()*W,y:VIEW_Y+Math.random()*VIEW_H,v:rnd(24,60),s:Math.random()<0.25?2:1});
  b.fillStyle='rgba(255,255,255,0.85)';for(const q of SDF){q.y+=q.v/60;q.x-=q.v/240;if(q.y>VIEW_Y+VIEW_H){q.y=VIEW_Y-2;q.x=Math.random()*W;}if(q.x<-2)q.x+=W+4;b.fillRect(Math.round(q.x),Math.round(q.y),q.s,q.s);}}
function rollCrumble(B,L){labBurst(B.x,B.y,Math.round(8+B.r),'snow',50);for(let k=0;k<6;k++)particles.push({x:B.x,y:B.y,vx:rnd(-40,40),vy:rnd(-30,20),z:2,vz:rnd(15,40),life:0.45,t:0,kind:'clump'});
  addFloat(B.x,B.y-B.r-8,'CRUMBLED! PLOW A NEW ONE','#c6d9f3',1.1);sfx('flump',0,{vol:0.5,rate:0.9});addSnowCircle(G,B.x,B.y,Math.max(4,B.r*0.7),0.4);L.gone=0.5;}
// ---------- TIME ATTACK rev 3c (Alex 00:40: "checkpoint zones should be smaller, something you drive through"; "hard to
// race and collect snow"): gates you steer through instead of lines across the map; each segment's time comes from the
// real drivable path between gates (machine-sized BFS) at 0.65x your speed; every gate pays a little ----
function taGate(g,y,k,rn){const gw=44,xs=[g.pw*0.28,g.pw*0.5,g.pw*0.72];for(const dy of [0,-18,18,-36,36,-60,60])for(let q=0;q<3;q++){const cx=Math.round(xs[(k+q)%3]+(rn()-0.5)*16),yy=Math.round(y+dy);
    if(yy<40||yy>g.ph-30||cx-gw/2<8||cx+gw/2>g.pw-8)continue;if(labRect(g,cx-gw/2-3,yy-18,gw+6,26))return {cx,y:yy,gw};}return null;}
function taPath(R,ax,ay,bx,by){const st=R.st,gw=R.gw,gh=R.gh,cell=(x,y)=>{let best=-1,bd=1e9;const gx=Math.round(x/st),gy=Math.round(y/st);for(let dy=-3;dy<=3;dy++)for(let dx=-3;dx<=3;dx++){const X=gx+dx,Y=gy+dy;if(X<0||Y<0||X>=gw||Y>=gh)continue;const k=Y*gw+X;if(R.seen[k]&&dx*dx+dy*dy<bd){bd=dx*dx+dy*dy;best=k;}}return best;};
  const a=cell(ax,ay),t=cell(bx,by);if(a<0||t<0)return -1;const d=new Int32Array(gw*gh).fill(-1),q=[a];d[a]=0;for(let i=0;i<q.length;i++){const k=q[i];if(k===t)return d[k]*st;const x=k%gw,y=(k/gw)|0;
    for(const [ax2,ay2] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+ax2,ny=y+ay2;if(nx<0||ny<0||nx>=gw||ny>=gh)continue;const nk=ny*gw+nx;if(!R.seen[nk]||d[nk]>=0)continue;d[nk]=d[k]+1;q.push(nk);}}return -1;}
MODES.timeattack={name:'TIME ATTACK',sub:'GATE TO GATE',rule:'DRIVE THROUGH EACH GATE IN TIME',bonus:'REACH THE FINISH: GOLD GIFT',arrows:1,col:'#7fe08a',
  how:['THE CLOCK IS SHORT. DRIVE','THROUGH EACH CHECKPOINT GATE:','IT ADDS TIME, PAYS, AND SHOWS','YOUR SPLIT AGAINST YOUR BEST.','REACH THE FINISH FOR A BONUS!'],
  post(g){const S=g.lab,st=g.start.y,yT=60,yB=g.ph-60,down=st<g.ph/2,tid=labTid(),v=Math.max(30,moveSpeed()*0.65),rn=srng(hashS(g.def.id)+71),R=labReachGrid(g,tid),legs=[];let y=st,dir=down?1:-1,tot=0;
    while(tot<900||!legs.length){const end=dir>0?yB:yT,len=Math.abs(end-y);if(len<40&&legs.length)break;legs.push({y0:y,y1:end,dir,len});tot+=len;y=end;dir=-dir;if(legs.length>6)break;}
    const n=Math.max(3,Math.min(9,Math.round((tot-80)/300))),at=d=>{let a=d;for(const L2 of legs){if(a<=L2.len)return {y:Math.round(L2.y0+L2.dir*a),dir:L2.dir};a-=L2.len;}const L3=legs[legs.length-1];return {y:L3.y1,dir:L3.dir};};
    S.cps=[];let px=g.start.x,py=g.start.y,pd=down?1:-1;
    for(let k=1;k<=n;k++){const q=at(80+(tot-80)*k/n-(k===n?8:0)),gt=taGate(g,q.y,k,rn);if(!gt||!labCanReach(R,gt.cx,gt.y,14))continue;const pth=taPath(R,px,py,gt.cx,gt.y),dist=pth>0?pth:Math.hypot(gt.cx-px,gt.y-py)*1.4;
      S.cps.push({cx:gt.cx,y:gt.y,gw:gt.gw,dir:q.dir,st:0,seg:dist/v+2+(q.dir!==pd?1.5:0)});px=gt.cx;py=gt.y;pd=q.dir;}
    S.seg=S.cps.map(c=>c.seg);g.def.time=Math.round((S.seg[0]||10)+5);S.down=down;S.key=g.def.id+':g';},
  tick(dt,tid,L){const S=G.lab;if(!S.cps||!S.cps.length)return;if(L.k==null){L.k=0;L.py=P.y;L.e=0;L.lastTick=99;L.miss=0;}L.e+=dt;if(L.miss>0)L.miss-=dt;
    const c=S.cps[L.k];if(c&&L.py!==P.y&&(L.py-c.y)*(P.y-c.y)<=0&&Math.sign(P.y-L.py)===c.dir){
      if(Math.abs(P.x-c.cx)<=c.gw/2-1){c.st=1;c.e=L.e;const best=((save.labTA||{})[S.key]||[]),last=L.k===S.cps.length-1,diff=best[L.k]!=null?L.e-best[L.k]:null;c.diff=diff;
        if(!last){const add=Math.round(S.seg[L.k+1]*10)/10;run.time+=add;addFloat(P.x,P.y-30,'CHECKPOINT! +'+add.toFixed(1)+'S','#7fe08a',1.3);labPay(c.cx,c.y-20,0.3,'');sfx('time');sfx('combo',0,{rate:1+L.k*0.06});labRing(c.cx,c.y,c.gw/2);}
        else{L.fin=1;const left=Math.max(0,run.time);addFloat(P.x,P.y-40,'FINISH! '+L.e.toFixed(1)+'S','#ffd23f',2);labPay(P.x,P.y-28,Math.min(4,left*0.15),'TIME BONUS');const rec=!best.length||L.e<best[best.length-1];
          if(rec){save.labTA=save.labTA||{};save.labTA[S.key]=S.cps.map(q=>Math.round(q.e*10)/10);persist();addFloat(P.x,P.y-52,'NEW RECORD!','#7fe08a',2);}labGoldGift(P.x,P.y-64,'FINISHED!');}
        if(diff!=null)addFloat(P.x,P.y-42,(diff<=0?'-':'+')+Math.abs(diff).toFixed(1),diff<=0?'#7fe08a':'#ff6a5a',1.3);L.k++;}
      else if(!(L.miss>0)){L.miss=1.2;addFloat(P.x,P.y-24,'MISSED THE GATE!','#ff9aa8',0.9);sfx('deny');}}
    L.py=P.y;if(!L.fin&&run.time<10&&run.time>0){const s2=Math.ceil(run.time);if(s2!==L.lastTick){L.lastTick=s2;sfx('tick',0,{rate:s2<=3?1.6:1.2,vol:0.6});}}
    labObj('GATE',Math.min(L.k,S.cps.length),S.cps.length,L.fin?'DONE '+(S.cps[S.cps.length-1].e||0).toFixed(1)+'S':'');const nx=S.cps[L.k];L.tgt=nx&&(nx.y<camY-4||nx.y>camY+VIEW_H+4)?{x:nx.cx,y:nx.y}:null;},
  screen(){const L=run.lab,S=G.lab;if(!L||!S.cps||L.k==null)return;if(L.tgt)labArrow(L.tgt.x,L.tgt.y,'#7fe08a');if(run.ended)return;
    const t=Math.max(0,run.time),hot=!L.fin&&t<5,col=L.fin?'#7fe08a':hot?(Math.floor(tNow*6)%2?'#ff4a4a':'#ffffff'):t<10?'#ffd23f':'#ffffff';text(b,L.fin?'FINISHED':t.toFixed(1),W/2,VIEW_Y+26,col,{align:'center',scale:2});
    const best=(save.labTA||{})[S.key];if(best&&best.length&&!L.fin)text(b,'BEST '+best[best.length-1].toFixed(1)+'S',W/2,VIEW_Y+44,'#9fd8ff',{align:'center'});},
  ents(ents,top,bot){const S=G.lab,L=run.lab;if(!S.cps)return;const kk=L&&L.k!=null?L.k:0;S.cps.forEach((c,k)=>{if(c.y<top-30||c.y>bot+30||k>kk+1||(c.st&&k<kk-1))return;const last=k===S.cps.length-1,nxt=kk===k,x0=Math.round(c.cx-c.gw/2),x1=Math.round(c.cx+c.gw/2);
      ents.push({base:c.y+1,draw:()=>{b.globalAlpha=c.st?0.35:nxt?1:0.55;const col=last?'#ffd23f':'#7fe08a',on=nxt&&Math.floor(tNow*4)%2;
        for(let x=x0+3;x<x1-2;x+=4)R(b,x,c.y-1,2,2,last?(((x>>2)%2)?K:'#ffffff'):(on?'#ffffff':col));
        for(const px of [x0,x1-2]){R(b,px-1,c.y-17,4,18,K);R(b,px,c.y-16,2,17,'#e8eef8');}R(b,x0-1,c.y-19,x1-x0+2,5,K);for(let x=x0;x<x1;x+=3)R(b,x,c.y-18,3,3,last?((((x-x0)/3|0)%2)?'#ffffff':K):((((x-x0)/3|0)%2)?col:'#ffffff'));
        text(b,last?'FINISH':''+(k+1),c.cx,c.y-28,last?'#ffd23f':col,{align:'center'});
        if(nxt)for(const ax of [x0-8,x1+5])for(let i=0;i<4;i++){const yy=c.dir>0?c.y-12+i:c.y-3-i;R(b,ax-3+i,yy,7-i*2,1,K);R(b,ax-2+i,yy,Math.max(1,5-i*2),1,col);}b.globalAlpha=1;}});});}};
loadSave();save.sess=(save.sess||0)+1;""")
open(f,'w',encoding='utf-8').write(s)
print('p158 lab rev 3c: gold-gift icon + alignment, present chime, open-ground yeti with shorter leaps, plow-a-new-snowball, crumbling, edge slope')
