import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
# ---- 1. Cars that pull out (Nov 16 tester report) --------------------------------------------------------------
# The parked spot was marked as "not part of the job", which is drawn as solid snow, so a pulled-out car left a
# car-shaped patch of snow nobody could plow. Now the spot is bare dry ground while the car is out, blocked again
# when it parks.
rep("g.pullBlocks.push([p[0]+1,p[1],22,28]);}","g.pullBlocks.push([p[0]+1,p[1],22,28,g.hazards[g.hazards.length-1]]);}")
rep("g.pullBlocks.push([bx+2,ry+4,22,28]);}","g.pullBlocks.push([bx+2,ry+4,22,28,g.hazards[g.hazards.length-1]]);}")
rep("for(const r of g.pullBlocks)setT(T_BLOCK,r[0],r[1],r[2],r[3]);",
    "for(const r of g.pullBlocks){const hz=r[4];if(hz){hz.cells=[];for(let cy=Math.max(0,Math.floor(r[1]/2));cy<Math.min(rows,Math.ceil((r[1]+r[3])/2));cy++)for(let cx=Math.max(0,Math.floor(r[0]/2));cx<Math.min(cols,Math.ceil((r[0]+r[2])/2));cx++){const i=cy*cols+cx;hz.cells.push(i,g.type[i]);}}setT(T_BLOCK,r[0],r[1],r[2],r[3]);}")
rep("else if(hz.state==='warn'){if(hz.t<=0)hz.state='out';}","else if(hz.state==='warn'){if(hz.t<=0){hz.state='out';pullSpot(hz,true);}}")
rep("if(hz.y<=hz.home){hz.y=hz.home;hz.state='park';hz.t=rnd(5,9);}","if(hz.y<=hz.home){hz.y=hz.home;hz.state='park';hz.t=rnd(5,9);pullSpot(hz,false);}")
rep("function setCellBlock(i,block,t){","function pullSpot(hz,free){const c=hz.cells;if(!c)return;for(let k=0;k<c.length;k+=2){if(c[k+1]===T_BLOCK)continue;if(free)setCellBlock(c[k],false,c[k+1]);else setCellBlock(c[k],true);}}\nfunction setCellBlock(i,block,t){")
# ---- 2. Snow the machine can never reach no longer counts -------------------------------------------------------
# A reachability scan found jobs where 1-19% of the snow sits where the current machine physically cannot get its
# blade (tight gaps, pockets behind props), so 100% was impossible. At job start we flood-fill every spot the
# machine fits (facing up/down and left/right, turning only where it fits both ways) and mark every snow cell no
# blade position can touch; those cells stay snowy but are left out of the percentage.
rep("function setDepth(g,i,v){const old=g.depth[i];if(old===v)return;g.depth[i]=v;const cy=(i/g.cols)|0,b=Math.floor(cy*2/g.bandH);\n  if(old>=CLEAR_T&&v<CLEAR_T){g.cleared++;g.bandClr[b]++;}else if(old<CLEAR_T&&v>=CLEAR_T){g.cleared--;g.bandClr[b]--;}",
    "function setDepth(g,i,v){const old=g.depth[i];if(old===v)return;g.depth[i]=v;const cy=(i/g.cols)|0,b=Math.floor(cy*2/g.bandH);\n  if(!(g.nc&&g.nc[i])){if(old>=CLEAR_T&&v<CLEAR_T){g.cleared++;g.bandClr[b]++;}else if(old<CLEAR_T&&v>=CLEAR_T){g.cleared--;g.bandClr[b]--;}}")
rep("function setCellBlock(i,block,t){const old=G.type[i]===T_BLOCK;if(old===block)return;const cy=(i/G.cols)|0,b=Math.floor(cy*2/G.bandH);\n  if(block){if(G.depth[i]<CLEAR_T){G.cleared--;G.bandClr[b]--;}G.clearable--;G.bandTot[b]--;G.type[i]=T_BLOCK;}\n  else{G.type[i]=t;G.depth[i]=0;G.clearable++;G.cleared++;G.bandTot[b]++;G.bandClr[b]++;",
    "function setCellBlock(i,block,t){const old=G.type[i]===T_BLOCK;if(old===block)return;const cy=(i/G.cols)|0,b=Math.floor(cy*2/G.bandH),cnt=!(G.nc&&G.nc[i]);\n  if(block){if(cnt){if(G.depth[i]<CLEAR_T){G.cleared--;G.bandClr[b]--;}G.clearable--;G.bandTot[b]--;}G.type[i]=T_BLOCK;}\n  else{G.type[i]=t;G.depth[i]=0;if(cnt){G.clearable++;G.cleared++;G.bandTot[b]++;G.bandClr[b]++;}")
rep("function wildHit(r){","""function markReach(g){try{g.nc=null;g.ncN=0;const tid=tool().id;if(tid==='ufo')return;const bw=bladeCells()*2,cols=g.cols,rows=g.rows,W1=cols+1,PW=g.pw,PH=g.ph;
  const occ=new Int32Array(W1*(rows+1)),blk=(x,y,w,h)=>{const x0=Math.max(0,Math.floor(x/2)),y0=Math.max(0,Math.floor(y/2)),x1=Math.min(cols,Math.ceil((x+w)/2)),y1=Math.min(rows,Math.ceil((y+h)/2));for(let cy=y0;cy<y1;cy++)for(let cx=x0;cx<x1;cx++)occ[(cy+1)*W1+cx+1]=1;};
  for(const o of g.obstacles)blk(o.x,o.y,o.w,o.h);for(const hz of g.hazards)if(hz.kind==='pull')blk(hz.x,hz.home,hz.w,hz.h);
  for(let cy=1;cy<=rows;cy++){let run2=0;for(let cx=1;cx<=cols;cx++){run2+=occ[cy*W1+cx];occ[cy*W1+cx]=run2+occ[(cy-1)*W1+cx];}}
  const ws=g.wsat||null,FP=[footprint(tid,0,0,2),footprint(tid,0,0,1)],BL=[0,1,2,3].map(f=>bladeRect(tid,0,0,f,bw));
  const nx=Math.floor(PW/2)+1,ny=Math.floor(PH/2)+1,N=nx*ny,seen=new Uint8Array(N*2),q=new Int32Array(N*2);let qh=0,qt=0;
  const fits=(k,o)=>{const f=FP[o],rx=(k%nx)*2+f.x,ry=((k/nx)|0)*2+f.y;if(rx<0||ry<0||rx+f.w>PW||ry+f.h>PH)return false;const x0=Math.floor(rx/2),y0=Math.floor(ry/2),x1=Math.ceil((rx+f.w)/2),y1=Math.ceil((ry+f.h)/2);
    if(occ[y1*W1+x1]-occ[y0*W1+x1]-occ[y1*W1+x0]+occ[y0*W1+x0]>0)return false;if(ws&&ws[y1*W1+x1]-ws[y0*W1+x1]-ws[y1*W1+x0]+ws[y0*W1+x0]>0)return false;return true;};
  const sk=Math.round(g.start.y/2)*nx+Math.round(g.start.x/2);for(const o of [0,1])if(fits(sk,o)){seen[sk*2+o]=1;q[qt++]=sk*2+o;}if(!qt)return;
  const cov=new Int32Array(W1*(rows+1)),add=(x,y,r)=>{const rx=x+r.x,ry=y+r.y,x0=Math.max(0,Math.floor(rx/2)),y0=Math.max(0,Math.floor(ry/2)),x1=Math.min(cols,Math.ceil((rx+r.w)/2)),y1=Math.min(rows,Math.ceil((ry+r.h)/2));if(x1<=x0||y1<=y0)return;cov[y0*W1+x0]++;cov[y0*W1+x1]--;cov[y1*W1+x0]--;cov[y1*W1+x1]++;};
  while(qh<qt){const st=q[qh++],k=st>>1,o=st&1,x=(k%nx)*2,y=((k/nx)|0)*2;
    if(o){add(x,y,BL[1]);add(x,y,BL[3]);}else{add(x,y,BL[0]);add(x,y,BL[2]);}
    const t2=k*2+(1-o);if(!seen[t2]){seen[t2]=1;if(fits(k,1-o))q[qt++]=t2;}
    const a=o?(x>0?k-1:-1):(y>0?k-nx:-1),c=o?(x+2<=PW?k+1:-1):(k+nx<N?k+nx:-1);
    if(a>=0&&!seen[a*2+o]){seen[a*2+o]=1;if(fits(a,o))q[qt++]=a*2+o;}if(c>=0&&!seen[c*2+o]){seen[c*2+o]=1;if(fits(c,o))q[qt++]=c*2+o;}}
  for(let cy=0;cy<=rows;cy++){let run2=0;for(let cx=0;cx<=cols;cx++){run2+=cov[cy*W1+cx];cov[cy*W1+cx]=run2+(cy>0?cov[(cy-1)*W1+cx]:0);}}
  const nc=new Uint8Array(cols*rows);let n=0;for(let cy=0;cy<rows;cy++)for(let cx=0;cx<cols;cx++){const i=cy*cols+cx;if(g.type[i]===T_BLOCK||cov[cy*W1+cx]>0)continue;nc[i]=1;n++;}
  if(n>g.clearable*0.35)return;
  for(let i=0;i<cols*rows;i++)if(nc[i]){const b2=Math.floor(((i/cols)|0)*2/g.bandH);g.clearable--;g.bandTot[b2]--;if(g.depth[i]<CLEAR_T){g.cleared--;g.bandClr[b2]--;}}
  g.nc=nc;g.ncN=n;}catch(e){g.nc=null;}}
function wildHit(r){""")
rep("camY=clamp(P.y-VIEW_H*0.55,0,Math.max(0,G.ph-VIEW_H));particles=[];floats=[];pickups=[];paused=false;",
    "markReach(G);camY=clamp(P.y-VIEW_H*0.55,0,Math.max(0,G.ph-VIEW_H));particles=[];floats=[];pickups=[];paused=false;")
# ---- 3. Auto-finish at 98% with a clean sweep ---------------------------------------------------------------------
# Once 98% of the reachable snow is gone, every last speck (reachable or not) melts away in a quick wave from the
# plow with sparkles, then ALL CLEAR. Stars are unchanged; this only removes the "ended on 99%" frustration.
rep("const CLEAR_T=0.5;","const CLEAR_T=0.5;\nconst FINISH_AT=98;")
rep("if(pct>=99.5)endRound(true);else if(run.time<=0)","if(pct>=FINISH_AT)startSweep();else if(run.time<=0)")
rep("function updatePlay(dt){\n  if(run.ended){updateFx(dt);return;}\n  if(run.offer)return;",
    "function updatePlay(dt){\n  if(run.ended){updateFx(dt);return;}\n  if(run.offer)return;\n  if(run.sweep){sweepUpdate(dt);return;}")
rep("function endRound(allClear){","""function startSweep(){if(run.sweep||run.ended)return;const n=G.cols*G.rows,L2=[];for(let i=0;i<n;i++)if(G.type[i]!==T_BLOCK&&G.depth[i]>0.04)L2.push(i);
  const cols=G.cols,d=new Float32Array(L2.length);L2.forEach((i,k)=>{const dx=(i%cols)*2+1-P.x,dy=((i/cols)|0)*2+1-P.y;d[k]=Math.sqrt(dx*dx+dy*dy);});
  const ord=L2.map((_,k)=>k).sort((a,c)=>d[a]-d[c]);run.sweep={t:0,k:0,idx:Int32Array.from(ord.map(k=>L2[k])),d:Float32Array.from(ord.map(k=>d[k]))};run.swept=true;
  joy=null;dpad=null;P.vx=0;P.vy=0;stopLoops();sfx('gold');addFloat(P.x,P.y-26,'CLEAN SWEEP!','#9fd8ff',1.3);}
function sweepUpdate(dt){const s=run.sweep;s.t+=dt;const rad=s.t>=0.95?1e9:30+s.t/0.95*240;let spawned=0;const top=camY-10,bot=camY+VIEW_H+10;
  while(s.k<s.idx.length&&s.d[s.k]<=rad){const i=s.idx[s.k++];setDepth(G,i,0);const x=(i%G.cols)*2+1,y=((i/G.cols)|0)*2+1;
    if(y>top&&y<bot&&spawned<26&&Math.random()<0.22){spawned++;particles.push({x,y,vx:rnd(-8,8),vy:rnd(-14,-4),z:0,vz:rnd(10,30),life:rnd(0.35,0.6),t:0,kind:'spark'});}}
  updateFx(dt);flushLevel(G);if(s.t>=1.25){run.sweep=null;endRound(true);}}
function endRound(allClear){""")
# ---- 4. Leftover finder from 90% ------------------------------------------------------------------------------------
# Remaining snow that still counts twinkles, and if the nearest patch is off screen an arrow at the edge points to it.
rep("const pct=G.cleared/G.clearable*100;if(pct>=FINISH_AT)startSweep();",
    "const pct=G.cleared/G.clearable*100;leftScan(dt,pct);if(pct>=FINISH_AT)startSweep();")
rep("function startSweep(){","""function leftScan(dt,pct){if(pct<90){run.left=null;return;}run.lfT=(run.lfT||0)-dt;run.twT=(run.twT||0)-dt;
  if(run.lfT<=0){run.lfT=0.4;const cols=G.cols,n=cols*G.rows,nc=G.nc,top=camY,bot=camY+VIEW_H;let best=-1,bd=1e18;const on=[];
    for(let i=0;i<n;i++){if(G.depth[i]<CLEAR_T||G.type[i]===T_BLOCK||(nc&&nc[i]))continue;const x=(i%cols)*2+1,y=((i/cols)|0)*2+1,dx=x-P.x,dy=y-P.y,d2=dx*dx+dy*dy;if(d2<bd){bd=d2;best=i;}if(y>top&&y<bot&&on.length<160)on.push(i);}
    run.left=best<0?null:{x:(best%cols)*2+1,y:((best/cols)|0)*2+1,on};}
  const L3=run.left;if(L3&&L3.on.length&&run.twT<=0){run.twT=0.12;for(let k=0;k<2;k++){const i=L3.on[(Math.random()*L3.on.length)|0];particles.push({x:(i%G.cols)*2+1+rnd(-1,1),y:((i/G.cols)|0)*2+1,vx:0,vy:0,z:1,vz:rnd(6,16),life:0.45,t:0,kind:'spark'});}}}
function drawLeftArrow(){if(!run||run.ended||run.sweep||!run.left)return;const L3=run.left,top=camY,bot=camY+VIEW_H;if(L3.y>top+4&&L3.y<bot-4)return;
  const up=L3.y<=top,ax=clamp(Math.round(L3.x),7,W-8),bob=Math.floor(tNow*4)%2,ay=up?VIEW_Y+3+bob:VIEW_Y+VIEW_H-13-bob;
  for(let i=0;i<5;i++)R(b,ax-i-1,up?ay+i-1:ay+5-i,i*2+3,1,K);for(let i=0;i<4;i++)R(b,ax-i,up?ay+i:ay+3-i,i*2+1,1,'#9fe6ff');
  const dd=Math.round(Math.abs(L3.y-(up?top:bot))/10);text(b,'SNOW '+dd+'M',ax,up?ay+7:ay-8,'#ffffff',{align:'center'});}
function startSweep(){""")
rep("drawChaserArrows();drawHUD();","drawChaserArrows();drawLeftArrow();drawHUD();")
# analytics: record whether the finish sweep fired and how much snow was out of reach for this machine
rep("weekly:!!run.challenge,score:R2.challenge?R2.challenge.score:null}));","weekly:!!run.challenge,score:R2.challenge?R2.challenge.score:null,swept:!!run.swept,unreach_pct:G&&G.ncN?Math.round(G.ncN/(G.clearable+G.ncN)*1000)/10:0}));")
open(f,'w',encoding='utf-8').write(s)
print('p99 fair finish: auto-finish 98, unreachable snow excluded, leftover finder, pulled-out car spots')
