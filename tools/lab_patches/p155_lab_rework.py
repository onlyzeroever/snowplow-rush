# LAB rev 3 (Alex + partner, Nov 20 22:34): twist feedback.
#  - Round-Up: real herding (flight zone around the plow, sheep run straight away from it, flock, slide along edges,
#    no auto-pull to the gate), sheep spread over the map, one pen (two on long maps) placed where it cuts nothing off.
#  - Dig-Out: a car comes free only when all four sides are dug out (side markers).
#  - Power Cut: 3-4 sections, each lit for a while then fading; light every section at once to restore the power;
#    dithered pixel-art headlight beam instead of the blocky one.
#  - Thin Ice: towed back to the last solid ground, 3s grace, the ice round you refreezes (no fall-in loops).
#  - Avalanche: outrun it - after the siren a wall of snow chases you down the map; get ahead or into a shelter.
#  - Lost Penguins: bring each chick to its own family (matching colours), families call when you carry their chick.
#  - Every twist: edge arrows only as hints (first 3s, then after 15s without progress), the reward shown up front,
#    a gold gift for completing the twist, and the twist's result on the end-of-job screen.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---- shared: hints, progress, card, results ----
rep("function labArrow(tx,ty,col){const sx=tx,","function labArrow(tx,ty,col){if(!labHintOn())return;const sx=tx,")
rep("function labTick(dt,tid){const M=labM();if(!M||run.ended)return;run.lab=run.lab||{t:0};run.lab.t+=dt;if(M.tick)M.tick(dt,tid,run.lab);}",
    "function labTick(dt,tid){const M=labM();if(!M||run.ended)return;run.lab=run.lab||{t:0};const L=run.lab;L.t+=dt;L.idle=(L.idle||0)+dt;if(L.hintT>0)L.hintT-=dt;if(L.idle>=15){L.hintT=4;L.idle=0;}if(M.tick)M.tick(dt,tid,L);"
    "if(M.goal&&!L.gift&&M.goal(L))labGoldGift(P.x,P.y-38,M.goalText||'DONE!');}")
rep("function labObj(label,n,of,extra){run.lobj={label,n,of,extra:extra||''};}",
    "function labObj(label,n,of,extra){if(run.lab&&(!run.lobj||run.lobj.n!==n))run.lab.idle=0;run.lobj={label,n,of,extra:extra||''};labRes(label,n,of);}\n"
    "function labRes(label,n,of){const M=labM();run.labRes={name:M?M.name:'',label,n,of,gift:!!(run.lab&&run.lab.gift)};}")
rep("if(t<3.6&&!run.ended){const a=t<0.25?t/0.25:t>3.1?(3.6-t)/0.5:1,",
    "if(t<(G.def.teach?5:4)&&!run.ended){const cd=G.def.teach?5:4,a=t<0.25?t/0.25:t>cd-0.5?(cd-t)/0.5:1,")
rep("panel(8,y,164,36,'#13306b',M.col);","panel(8,y,164,M.bonus?46:36,'#13306b',M.col);")
rep("text(b,M.rule,W/2,y+23,'#ffffff',{align:'center',outline:null});b.globalAlpha=1;}}",
    "text(b,M.rule,W/2,y+23,'#ffffff',{align:'center',outline:null});if(M.bonus){const bw2=textW(M.bonus);b.drawImage(SPR.present,Math.round(W/2-bw2/2-6),y+31);text(b,M.bonus,W/2+5,y+33,'#ffd23f',{align:'center',outline:null});}b.globalAlpha=1;}}")
# objective box: a little present while the gift is still to be won
rep("panel(2,VIEW_Y+2,w,h,done?'#3a5a12':'#13306b',done?'#ffd23f':M.col);",
    "panel(2,VIEW_Y+2,w+(M.bonus?10:0),h,done?'#3a5a12':'#13306b',done?'#ffd23f':M.col);if(M.bonus)b.drawImage(SPR.present,2+w,VIEW_Y+6+(h>20?3:0));")
# end-of-job screen: how the twist went
rep("  let ly=py+122;if(r.bonus>0){",
    "  let ly=py+122;if(run.labRes&&!r.challenge){const q=run.labRes;text(b,q.label+' '+q.n+(q.of!=null?'/'+q.of:'')+(q.gift?'  GOLD GIFT!':''),W/2,ly,q.gift?'#ffd23f':'#9fd8ff',{align:'center'});ly+=10;}if(r.bonus>0){")

# ---- sheep: herded strays skip the base flee and the random wander ----
rep("const fr2=hz.horse?26:44;if(d<fr2){","const fr2=hz.stray?0:hz.horse?26:44;if(d<fr2){")
rep("if(hz.t<=0){hz.t=rnd(1.5,3.5);hz.vx+=rnd(-10,10);hz.vy+=rnd(-8,8);}","if(hz.t<=0&&!hz.stray){hz.t=rnd(1.5,3.5);hz.vx+=rnd(-10,10);hz.vy+=rnd(-8,8);}")
rep("mxs=hz.horse?24:34;","mxs=hz.horse?24:hz.stray?75:34;")
rep("const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y)&&mClear('sheep',hz,nx,hz.y))hz.x=nx;else hz.vx*=-0.5;if(chaserFree(hz,hz.x,ny)&&mClear('sheep',hz,hz.x,ny))hz.y=ny;else hz.vy*=-0.5;",
    "const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt,unst=hz.stray&&!mClear('sheep',hz,hz.x,hz.y);if(chaserFree(hz,nx,hz.y)&&(unst||mClear('sheep',hz,nx,hz.y)))hz.x=nx;else hz.vx*=-0.5;if(chaserFree(hz,hz.x,ny)&&(unst||mClear('sheep',hz,hz.x,ny)))hz.y=ny;else hz.vy*=-0.5;")

# lab props (pen fences, forts) are thin: movers may stand next to / pass between them (the glitch check kept sheep out of the pen gate)
rep("  for(const o of g.obstacles)add({x:o.sx,y:o.sy,w:o.spr.width,h:o.spr.height,","  for(const o of g.obstacles)if(!o.lab)add({x:o.sx,y:o.sy,w:o.spr.width,h:o.spr.height,")

# ---- Dig-Out: all four sides ----
rep("g.hazards.push(hz);if(g.pullBlocks)g.pullBlocks.push([p.x+1,p.y,22,28,hz]);S.cars.push(hz);",
    "hz.sides=[[],[],[],[]];for(const i of hz.ring){const px=(i%g.cols)*2,py=((i/g.cols)|0)*2;hz.sides[py+2<=p.y?0:py>=p.y+28?2:px+2<=p.x+1?3:1].push(i);}\n"
    "      g.hazards.push(hz);if(g.pullBlocks)g.pullBlocks.push([p.x+1,p.y,22,28,hz]);S.cars.push(hz);")
rep("if(hz.buried&&!hz.rf){hz.rf=1;hz.ring=hz.ring.filter(i=>!(G.nc&&G.nc[i])&&G.type[i]!==T_BLOCK);}",
    "if(hz.buried&&!hz.rf){hz.rf=1;const okc=i=>!(G.nc&&G.nc[i])&&G.type[i]!==T_BLOCK;hz.ring=hz.ring.filter(okc);if(hz.sides)hz.sides=hz.sides.map(a=>a.filter(okc));}")
rep("if(hz.buried){let c2=0;for(const i of hz.ring)if(G.depth[i]<CLEAR_T)c2++;hz.prog=hz.ring.length?c2/hz.ring.length:1;",
    "if(hz.buried){const need=G.def.teach?0.7:0.8;let act=0,dn=0;hz.sp=hz.sides.map(a=>{if(a.length<4)return -1;act++;let c2=0;for(const i of a)if(G.depth[i]<CLEAR_T)c2++;const p2=c2/a.length;if(p2>=need)dn++;return p2;});"
    "hz.sdone=dn;hz.sact=act;hz.prog=act?dn/act*0.7:0.7;if(dn<act&&dn>(hz.sdn||0)){sfx('crunch',0,{vol:0.5,rate:1.2});labBurst(hz.x+11,hz.y+14,8,'snow',40);addFloat(hz.x+11,hz.y-26,dn+'/'+act+' SIDES','#ffb04a',0.8);}hz.sdn=dn;")
rep("if(L.dn>=S.n){labPay(P.x,P.y-38,3,'ALL CARS FREE!','#7fe08a');sfx('fanfare');}","if(L.dn>=S.n)labGoldGift(P.x,P.y-38,'ALL CARS FREE!');")
rep("if(Math.hypot(P.x-cx,P.y-cy)<130){const bw=28,p2=Math.min(1,(hz.prog||0)/0.7);R(b,cx-bw/2-1,hz.y-10,bw+2,5,K);R(b,cx-bw/2,hz.y-9,Math.round(bw*p2),3,p2>0.7?'#7fe08a':'#ffb04a');text(b,'DIG OUT',cx,hz.y-18,'#ffffff',{align:'center'});}",
    "if(Math.hypot(P.x-cx,P.y-cy)<130){const sp2=hz.sp||[];const mk2=(i,x,y,w,h)=>{if(sp2[i]==null||sp2[i]<0)return;const ok=sp2[i]>=(G.def.teach?0.7:0.8);R(b,x-1,y-1,w+2,h+2,K);R(b,x,y,w,h,ok?'#7fe08a':'#ffb04a');if(!ok){const f2=Math.max(0,Math.min(1,sp2[i]/(G.def.teach?0.7:0.8)));if(w>h)R(b,x,y,Math.round(w*f2),h,'#ffe08a');else R(b,x,y+h-Math.round(h*f2),w,Math.round(h*f2),'#ffe08a');}};"
    "mk2(0,cx-7,hz.y-9,14,2);mk2(2,cx-7,hz.y+hz.h+8,14,2);mk2(3,hz.x-10,cy-7,2,14);mk2(1,hz.x+hz.w+9,cy-7,2,14);text(b,'DIG ALL 4 SIDES',cx,hz.y-18,'#ffffff',{align:'center'});}")
rep("MODES.digout={name:'DIG-OUT',sub:'FREE THE SNOWED-IN CARS',rule:'PLOW ROUND THE BURIED CARS',col:'#ffb04a',",
    "MODES.digout={name:'DIG-OUT',sub:'FREE THE SNOWED-IN CARS',rule:'DIG OUT ALL 4 SIDES OF A CAR',bonus:'FREE ALL CARS: GOLD GIFT',col:'#ffb04a',")

# ---- Thin Ice: tow to solid ground, grace, refreeze ----
rep("if(L.sunk>0){L.sunk-=dt;P.vx=P.vy=0;if(L.sunk<=0){P.x=L.safe.x;P.y=L.safe.y;",
    "if(L.sunk>0){L.sunk-=dt;P.vx=P.vy=0;if(L.sunk<=0){const dst=L.land||{x:G.start.x,y:G.start.y};P.x=dst.x;P.y=dst.y;L.grace=3;"
    "tiThaw(g,S,P.x,P.y,48);if(L.fallAt&&L.prevFall!=null&&L.fallAt.t-L.prevFall<12)tiThaw(g,S,L.fallAt.x,L.fallAt.y,110);")
rep("P.inv=Math.max(P.inv,1);addFloat(P.x,P.y-26,'TOWED OUT','#ffffff',1.1);",
    "P.inv=Math.max(P.inv,1);addFloat(P.x,P.y-26,'TOWED TO THE SHORE','#ffffff',1.1);")
rep("    if(tid==='ufo'||!run.moved||L.t<1)return;\n    const fp=footprint(tid,P.x,P.y,P.f),x0=Math.max(0,(fp.x+1)>>1)",
    "    if(tid==='ufo'||!run.moved||L.t<1)return;\n    if(L.grace>0){L.grace-=dt;let on=0;const f3=footprint(tid,P.x,P.y,P.f);for(let cy=Math.max(0,f3.y>>1);cy<=Math.min(g.rows-1,(f3.y+f3.h)>>1);cy++)for(let cx=Math.max(0,f3.x>>1);cx<=Math.min(cols-1,(f3.x+f3.w)>>1);cx++)if(g.type[cy*cols+cx]===T_ICE)on++;if(!on)L.land={x:P.x,y:P.y};return;}\n"
    "    const fp=footprint(tid,P.x,P.y,P.f),x0=Math.max(0,(fp.x+1)>>1)")
rep("    L.moved+=Math.hypot(P.x-L.px,P.y-L.py);L.px=P.x;L.py=P.y;",
    "    if(n===0)L.land={x:P.x,y:P.y};labObj('SPLOOSHES',L.falls||0,null);\n    L.moved+=Math.hypot(P.x-L.px,P.y-L.py);L.px=P.x;L.py=P.y;")
rep("    if(n>=4&&holes/n>=S.thr){L.sunk=1.3;L.falls++;",
    "    if(n>=4&&holes/n>=S.thr){L.sunk=1.3;L.falls++;L.prevFall=L.fallAt?L.fallAt.t:null;L.fallAt={x:P.x,y:P.y,t:now};")
rep("MODES.thinice={name:'THIN ICE',sub:\"DON'T CROSS YOUR TRACKS\",rule:\"DON'T CROSS YOUR OWN TRACKS\",col:'#7ad3ff',",
    "MODES.thinice={name:'THIN ICE',sub:\"DON'T CROSS YOUR TRACKS\",rule:\"DON'T CROSS YOUR OWN TRACKS\",bonus:'3 STARS, NO SPLOOSH: GOLD GIFT',col:'#7ad3ff',\n"
    "  goal(L){return G.cleared/G.clearable*100>=G.def.stars[2]&&!(L.falls>0)&&L.ti;},goalText:'DRY RUN!',")

# ---- Slalom: the clean run is the gold gift ----
rep("if(!L.clean&&L.pass>=S.n&&L.miss===0&&S.n){L.clean=1;labPay(P.x,P.y-38,3,'CLEAN RUN!','#7fe08a');sfx('fanfare');}",
    "if(!L.clean&&L.pass>=S.n&&L.miss===0&&S.n){L.clean=1;labGoldGift(P.x,P.y-38,'CLEAN RUN!');}")
rep("MODES.slalom={name:'SLALOM',sub:'CHAIN THE FLAG GATES',rule:'DRIVE BETWEEN THE FLAGS',col:'#ff6a7a',",
    "MODES.slalom={name:'SLALOM',sub:'CHAIN THE FLAG GATES',rule:'DRIVE BETWEEN THE FLAGS',bonus:'EVERY GATE, NO MISS: GOLD GIFT',col:'#ff6a7a',")

# ---- new modes + helpers (they replace p151's Round-Up, Power Cut, Avalanche and Lost Penguins) ----
rep("loadSave();save.sess=(save.sess||0)+1;",r"""// ================= LAB rev 3 (Nov 20) =================
function labHintOn(){const L=run.lab;if(!L)return false;return !!L.urgent||L.t<3||L.hintT>0;}
function labGoldGift(x,y,label){const L=run.lab;if(!L||L.gift)return 0;L.gift=1;const c=Math.max(1,Math.round(labUnit()*5));earn(c);
  addFloat(x,y-12,label||'DONE!','#7fe08a',2);addFloat(x,y-2,'GOLD GIFT'+cplus(c),'#ffd23f',2.2);sfx('fanfare');sfx('gift');buzz(40);shake=Math.max(shake,0.15);
  const CF=['#ff4fa3','#ffd23f','#7ad3ff','#9cff7a','#ff7a3a','#ffffff'];for(let k=0;k<40;k++)particles.push({x,y,vx:rnd(-70,70),vy:rnd(-40,20),z:4,vz:rnd(30,70),life:rnd(1,1.5),t:0,kind:'conf',c:CF[k%6]});
  for(let k=0;k<14;k++)particles.push({x,y,vx:rnd(-50,50),vy:rnd(-40,10),z:3,vz:rnd(30,70),life:0.8,t:0,kind:'coin'});if(run.labRes)run.labRes.gift=true;return c;}
function labTid(){return TOOLS[useIdx()].id;}
// what the machine can reach from the start: summed table of solid cells, BFS over a 4px grid of machine centres
function labSolid(g,extra){const cols=g.cols,rows=g.rows,W1=cols+1,sol=new Uint8Array(cols*rows);for(let i=0;i<cols*rows;i++)if(g.type[i]===T_BLOCK)sol[i]=1;
  const mark=(x,y,w,h)=>{for(let cy=Math.max(0,Math.floor(y/2));cy<Math.min(rows,Math.ceil((y+h)/2));cy++)for(let cx=Math.max(0,Math.floor(x/2));cx<Math.min(cols,Math.ceil((x+w)/2));cx++)sol[cy*cols+cx]=1;};
  for(const o of g.obstacles)mark(o.x,o.y,o.w,o.h);for(const r of extra||[])mark(r.x,r.y,r.w,r.h);
  const S2=new Int32Array((rows+1)*W1);for(let y=0;y<rows;y++){let a=0;for(let x=0;x<cols;x++){a+=sol[y*cols+x];S2[(y+1)*W1+x+1]=S2[y*W1+x+1]+a;}}return {S:S2,W1,cols,rows};}
function labHit(T,x,y,w,h){const x0=Math.floor(x/2),y0=Math.floor(y/2),x1=Math.ceil((x+w)/2),y1=Math.ceil((y+h)/2);if(x0<0||y0<0||x1>T.cols||y1>T.rows)return true;return T.S[y1*T.W1+x1]-T.S[y0*T.W1+x1]-T.S[y1*T.W1+x0]+T.S[y0*T.W1+x0]>0;}
function labReachGrid(g,tid,extra){const T=labSolid(g,extra),st=4,gw=Math.floor(g.pw/st),gh=Math.floor(g.ph/st),f0=footprint(tid,0,0,0),f1=footprint(tid,0,0,1),seen=new Uint8Array(gw*gh);
  const ok=(gx,gy)=>{const x=gx*st,y=gy*st;return !labHit(T,x+f0.x,y+f0.y,f0.w,f0.h)||!labHit(T,x+f1.x,y+f1.y,f1.w,f1.h);};
  let sx=Math.round(g.start.x/st),sy=Math.round(g.start.y/st);if(!ok(sx,sy)){let f=0;for(let d=1;d<8&&!f;d++)for(const [ax,ay] of [[d,0],[-d,0],[0,d],[0,-d]])if(!f&&ok(sx+ax,sy+ay)){sx+=ax;sy+=ay;f=1;}}
  const q=[sy*gw+sx];seen[q[0]]=1;for(let i=0;i<q.length;i++){const k=q[i],x=k%gw,y=(k/gw)|0;for(const [ax,ay] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+ax,ny=y+ay;if(nx<0||ny<0||nx>=gw||ny>=gh)continue;const nk=ny*gw+nx;if(seen[nk])continue;if(ok(nx,ny)){seen[nk]=1;q.push(nk);}}}
  return {seen,gw,gh,st,n:q.length};}
// placing r (solid) must cut nothing off: every point reachable before and well away from r stays reachable
function labNoCut(g,tid,base,r,extra){const R2=labReachGrid(g,tid,(extra||[]).concat([r])),cx=r.x+r.w/2,cy=r.y+r.h/2,far=60+Math.max(r.w,r.h)/2;
  for(let k=0;k<base.seen.length;k++)if(base.seen[k]&&!R2.seen[k]){const x=(k%base.gw)*base.st,y=((k/base.gw)|0)*base.st;if(Math.hypot(x-cx,y-cy)>far)return false;}return true;}
function labCanReach(base,x,y,rad){const st=base.st;for(let dy=-rad;dy<=rad;dy+=st)for(let dx=-rad;dx<=rad;dx+=st){const gx=Math.round((x+dx)/st),gy=Math.round((y+dy)/st);if(gx<0||gy<0||gx>=base.gw||gy>=base.gh)continue;if(base.seen[gy*base.gw+gx])return true;}return false;}

// ---------- ROUND-UP: herd stray sheep from all over the map into the pen ----------
function penBuild(g,x,y,w,h,rn){const pen={x,y,w,h,cx:x+w/2,cy:y+h/2,ix:x+3,iy:y+8,iw:w-6,ih:h-11,gx0:x+14,gx1:x+w-14};const hs=fenceH(14),vs=fenceV(h-5);
  labFence(g,x,y+5,14,3,hs,x,y);labFence(g,x+w-14,y+5,14,3,hs,x+w-14,y);labFence(g,x,y+h-3,14,3,hs,x,y+h-8);labFence(g,x+w-14,y+h-3,14,3,hs,x+w-14,y+h-8);
  labFence(g,x,y+5,3,h-5,vs,x-1,y+5);labFence(g,x+w-3,y+5,3,h-5,vs,x+w-4,y+5);
  const hc=mk(pen.iw,pen.ih),hg=hc.getContext('2d');for(let py=0;py<pen.ih;py++)for(let px=0;px<pen.iw;px++){const v=(px*3+py*5+((px*py)%3))%7;hg.fillStyle=v<2?'#d9b45a':v<5?'#e8c872':'#f2da8f';hg.fillRect(px,py,1,1);}
  for(let k=0;k<pen.iw*pen.ih/14;k++){hg.fillStyle='#b8913a';hg.fillRect(Math.floor(rn()*pen.iw),Math.floor(rn()*pen.ih),2,1);}pen.hay=hc;
  labBlock(g,pen.ix,pen.iy,pen.iw,pen.ih);labPaint(g,x-2,y-2,w+4,h+6);return pen;}
MODES.roundup={name:'ROUND-UP',sub:'HERD THE SHEEP INTO THE PEN',rule:'COME FROM BEHIND TO HERD THEM',bonus:'ALL SHEEP HOME: GOLD GIFT',col:'#c98d4a',
  how:['SHEEP HAVE ESCAPED ALL OVER THE','MAP. THEY RUN AWAY FROM YOUR','PLOW, SO COME FROM BEHIND AND','STEER THEM INTO THE PEN. EACH','ONE PAYS. ALL HOME: GOLD GIFT!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+17),tid=labTid(),np=(!g.def.teach&&g.ph>1700)?2:1,ns=g.def.teach?3:4,W2=56,H2=44,extra=[];
    S.pens=[];S.sheep=[];S.R0=g.def.teach?56:50;
    for(let k=0;k<np;k++){const yc=g.ph*(np===1?0.5:(k===0?0.3:0.7)),base=labReachGrid(g,tid,extra);let pen=null;
      for(let tr=0;tr<40&&!pen;tr++){const sp=160+tr*14,p=labSpot(g,W2+16,H2+28,Math.max(30,yc-sp),Math.min(g.ph-30,yc+sp),rn,{margin:2,xin:4,avoid:[{x:g.start.x,y:g.start.y,r:90}].concat(S.pens.map(q=>({x:q.cx,y:q.cy,r:260})))});if(!p)continue;
        const r={x:p.x+8,y:p.y+14,w:W2,h:H2};if(labNoCut(g,tid,base,r,extra))pen=r;}
      if(!pen)continue;extra.push(pen);S.pens.push(penBuild(g,pen.x,pen.y,W2,H2,rn));}
    if(!S.pens.length)return;const fin=labReachGrid(g,tid,extra);
    for(let j=0;j<ns;j++){const pn=S.pens[j%S.pens.length];let q=null;
      for(let tr=0;tr<40&&!q;tr++){const r1=(g.def.teach?220:300)+Math.max(0,tr-20)*8,c=labSpot(g,10,8,0,g.ph,rn,{near:{x:pn.cx,y:pn.cy,r0:110,r1},margin:6,avoid:S.pens.map(p2=>({x:p2.cx,y:p2.cy,r:95})).concat([{x:g.start.x,y:g.start.y,r:60}],S.sheep.map(h=>({x:h.x,y:h.y,r:70})))});
        if(c&&c.x>=14&&c.x<=g.pw-24&&c.y>=24&&c.y<=g.ph-30&&labCanReach(fin,c.x+5,c.y+4,34))q=c;}
      if(!q)continue;const hz={kind:'sheep',stray:1,horse:false,col:0,x:q.x,y:q.y,w:9,h:6,hx:q.x,hy:q.y,vx:0,vy:0,t:99,anim:rn()*2};g.hazards.push(hz);S.sheep.push(hz);}},
  tick(dt,tid,L){const S=G.lab;if(!S.pens||!S.pens.length||!S.sheep.length)return;if(L.home==null)L.home=0;
    const fp=footprint(tid,P.x,P.y,P.f),pcx=P.x,pcy=P.y,R=S.R0+Math.max(fp.w,fp.h)*0.5,hs=Math.hypot(P.vx||0,P.vy||0);L.R=R;L.pc={x:pcx,y:pcy};let near=0;const loose=S.sheep.filter(h=>!h.penned);
    for(const hz of S.sheep){hz.t=99;if(hz.penned){const pn=hz.pen;hz.hx=pn.ix+pn.iw/2-4;hz.hy=pn.iy+pn.ih/2-3;hz.vx+=(hz.hx-hz.x)*2*dt;hz.vy+=(hz.hy-hz.y)*2*dt;continue;}
      hz.hx=hz.x;hz.hy=hz.y;const sx=hz.x+4.5,sy=hz.y+3,dx=sx-pcx,dy=sy-pcy,d=Math.hypot(dx,dy);let tx=0,ty=0;if(d<R+46)near++;
      if(d<R){const k=1-d/R,sp=(22+30*k)*Math.max(1,moveSpeed()/40);let ux=dx/(d||1),uy=dy/(d||1);if(hs>8){const hx=P.vx/hs,hy=P.vy/hs;if(hx*ux+hy*uy>0.2){ux=ux*0.55+hx*0.45;uy=uy*0.55+hy*0.45;const nn=Math.hypot(ux,uy)||1;ux/=nn;uy/=nn;}}tx=ux*sp;ty=uy*sp;if(!(hz.alert>0)){hz.alert=0.7;if(Math.random()<0.6)addFloat(sx,hz.y-8,'BAA!','#ffffff',0.6);}}
      let fx=0,fy=0,fn=0;for(const o of loose){if(o===hz)continue;const ox=o.x-hz.x,oy=o.y-hz.y,od=Math.hypot(ox,oy);if(od<36){fn++;fx+=o.vx;fy+=o.vy;if(od<11){tx-=ox/(od||1)*14;ty-=oy/(od||1)*14;}else if(d>=R){tx+=ox*0.3;ty+=oy*0.3;}}}
      if(fn&&d<R){tx+=fx/fn*0.35;ty+=fy/fn*0.35;}
      const mv=Math.hypot(hz.vx,hz.vy);if(mv>8)for(const pn of S.pens){if(hz.x>=pn.ix&&hz.x+hz.w<=pn.ix+pn.iw&&hz.y>=pn.iy-2&&hz.y+hz.h<=pn.iy+pn.ih+2)continue;for(const gy of [pn.y+6,pn.y+pn.h-1]){const ey=gy-sy,ex=pn.cx-sx;if(Math.abs(ey)<30&&Math.abs(ex)<32&&ey*hz.vy>0)tx+=ex*1.8*(1-Math.abs(ey)/30);}}
      if(hz.x<14)tx+=(14-hz.x)*7;if(hz.x>G.pw-23)tx-=(hz.x-(G.pw-23))*7;if(hz.y<22)ty+=(22-hz.y)*7;if(hz.y>G.ph-28)ty-=(hz.y-(G.ph-28))*7;
      const kk=Math.min(1,dt*(d<R?7:2.5));hz.vx+=(tx-hz.vx)*kk;hz.vy+=(ty-hz.vy)*kk;if(hz.alert>0)hz.alert-=dt;
      if(tid!=='ufo'&&overlap(fp,hz)){const dd=d||1;hz.vx+=dx/dd*60;hz.vy+=dy/dd*60;}
      for(const pn of S.pens){if(hz.x>=pn.ix&&hz.x+hz.w<=pn.ix+pn.iw&&hz.y>=pn.iy&&hz.y+hz.h<=pn.iy+pn.ih){hz.penned=1;hz.pen=pn;L.home++;labPay(hz.x+4,hz.y-12,1,'BAA! HOME');labTime(hz.x+4,hz.y-3,3);sfx('moo',0,{rate:1.8,vol:0.6});labRing(hz.x+4,hz.y+3,10);hz.heart=1.5;
        if(L.home>=S.sheep.length)labGoldGift(P.x,P.y-38,'ALL SHEEP HOME!');break;}}}
    for(const hz of S.sheep)if(hz.heart>0)hz.heart-=dt;L.near=near;labObj('SHEEP',L.home,S.sheep.length);
    const vis=loose.filter(h=>h.y>camY-10&&h.y<camY+VIEW_H+10);
    if(vis.length){const pn=nearest(S.pens.map(q=>({x:q.cx,y:q.cy})));L.tgt=pn?{x:pn.x,y:pn.y,col:'#c98d4a'}:null;}else{const h=nearest(loose.map(q=>({x:q.x+4,y:q.y+3})));L.tgt=h?{x:h.x,y:h.y,col:'#ffffff'}:null;}},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,L.tgt.col);},
  over(cy){const L=run.lab;if(!L||!L.near||!L.pc||tool().id==='ufo')return;const cx=L.pc.x,cy2=L.pc.y,Rr=L.R;for(let a=0;a<48;a+=2){const an=a/48*Math.PI*2+tNow*0.7,x=Math.round(cx+Math.cos(an)*Rr),y=Math.round(cy2+Math.sin(an)*Rr);R(b,x,y,2,2,'rgba(27,31,59,0.25)');R(b,x,y-1,2,2,'rgba(255,214,140,0.85)');}},
  ents(ents,top,bot){const S=G.lab,L=run.lab;if(!S.pens)return;for(const pn of S.pens){if(pn.y>bot+20||pn.y+pn.h<top-20)continue;
      ents.push({base:-1e9+3,draw:()=>{b.drawImage(pn.hay,pn.ix,pn.iy);const p=Math.floor(tNow*3)%2;for(const [gy,dir] of [[pn.y-3-p,1],[pn.y+pn.h+3+p,-1]])for(let q=0;q<3;q++){R(b,pn.cx-1-q,gy-dir*q,1,1,'rgba(201,141,74,0.9)');R(b,pn.cx+q,gy-dir*q,1,1,'rgba(201,141,74,0.9)');}}});}
    for(const hz of S.sheep){if(hz.y<top-20||hz.y>bot+20)continue;
      if(hz.heart>0)ents.push({base:hz.y+20,draw:()=>{const y=Math.round(hz.y-10-(1.5-hz.heart)*6);R(b,hz.x+2,y,2,1,'#ff4f7a');R(b,hz.x+5,y,2,1,'#ff4f7a');R(b,hz.x+2,y+1,5,1,'#ff4f7a');R(b,hz.x+3,y+2,3,1,'#ff4f7a');R(b,hz.x+4,y+3,1,1,'#ff4f7a');}});
      else if(hz.alert>0.35&&!hz.penned)ents.push({base:hz.y+20,draw:()=>{R(b,Math.round(hz.x+3),Math.round(hz.y-12),3,6,K);R(b,Math.round(hz.x+4),Math.round(hz.y-11),1,3,'#ffffff');R(b,Math.round(hz.x+4),Math.round(hz.y-7),1,1,'#ffffff');}});}}};

// ---------- POWER CUT: light every section at once before the lights fade ----------
const LIGHTC={};
function lightCone(f){if(LIGHTC[f])return LIGHTC[f];const N=160,o=N/2,c=mk(N,N),g=c.getContext('2d'),t=mk(N,N),tg=t.getContext('2d'),fv=[[0,-1],[1,0],[0,1],[-1,0]][f],B=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){const dx=x-o,dy=y-o,al=dx*fv[0]+dy*fv[1],sd=Math.abs(dx*fv[1]-dy*fv[0]);let v=0;
    if(al>0&&al<78){const half=5+al*0.45;if(sd<half){const e=1-sd/half,fall=al<34?1:1-(al-34)/44;v=Math.min(1,e*1.7)*fall*1.2;}}
    const th=(B[(y&3)*4+(x&3)]+0.5)/16;if(v>th){g.fillStyle=v>0.62?'rgba(0,0,0,1)':'rgba(0,0,0,0.7)';g.fillRect(x,y,1,1);tg.fillStyle=v>0.62?'rgba(255,238,170,0.16)':'rgba(255,238,170,0.08)';tg.fillRect(x,y,1,1);}}
  return LIGHTC[f]={c,t,o};}
let GLOWC=null;function lightGlow(){if(GLOWC)return GLOWC;const N=44,o=N/2,c=mk(N,N),g=c.getContext('2d'),B=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5];
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){const r=Math.hypot(x-o,y-o),v=r<10?1:1-(r-10)/12;if(v>(B[(y&3)*4+(x&3)]+0.5)/16){g.fillStyle=v>0.6?'rgba(0,0,0,1)':'rgba(0,0,0,0.7)';g.fillRect(x,y,1,1);}}return GLOWC={c,o};}
MODES.powercut={name:'POWER CUT',sub:'TURN THE LIGHTS BACK ON',rule:'LIGHT EVERY SECTION AT ONCE',bonus:'ALL LIT AT ONCE: GOLD GIFT',col:'#ffd23f',
  how:['THE PARK IS DARK. DRIVE ONTO A','GLOWING POWER BOX TO LIGHT ITS','PART OF THE PARK, BUT THE LIGHTS','FADE AFTER A WHILE. GET EVERY','SECTION LIT AT ONCE: GOLD GIFT!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+23),tid=labTid(),base=labReachGrid(g,tid),n=g.def.teach?3:(g.ph>1800?4:3),bands=labBands(g,n);S.boxes=[];S.LIT=g.def.teach?60:38;
    for(let k=0;k<n;k++){const [y0,y1]=bands[k];let p=null;for(let tr=0;tr<40&&!p;tr++){const q=labSpot(g,16,16,y0,y1,rn,{margin:tr<20?14:8,xin:tr<20?24:16,avoid:[{x:g.start.x,y:g.start.y,r:k===0?50:90}]});if(q&&labCanReach(base,q.x+8,q.y+8,30))p=q;}
      if(p)S.boxes.push({x:p.x+8,y:p.y+8,left:0,ever:0,litT:0,y0,y1});}
    const oc=mk(g.pw,g.ph),o=oc.getContext('2d');o.fillStyle='rgba(8,12,36,0.86)';o.fillRect(0,0,g.pw,g.ph);g.night=oc;S.n=S.boxes.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.boxes||!S.boxes.length)return;if(L.on==null){L.on=0;L.done=0;}
    for(const bx of S.boxes){if(bx.left>0){bx.litT+=dt;if(!L.done){bx.left-=dt;if(bx.left<=0){bx.left=0;addFloat(bx.x,bx.y-24,'LIGHTS OUT!','#ff9aa8',1);sfx('cend');}}}
      if(labTouch(tid,{x:bx.x-7,y:bx.y-7,w:14,h:14})){const was=bx.left>0;if(!was||bx.left<S.LIT-3){bx.left=S.LIT;if(!was){bx.litT=0;sfx('stomp');sfx('gold');shake=Math.max(shake,0.2);buzz(30);labRing(bx.x,bx.y,20);labBurst(bx.x,bx.y,16,'coin',60);
          addFloat(bx.x,bx.y-30,'POWER ON!','#ffd23f',1.4);if(!bx.ever){bx.ever=1;labPay(bx.x,bx.y-20,1,'');labTime(bx.x,bx.y-10,4);}else{labPay(bx.x,bx.y-20,0.3,'');labTime(bx.x,bx.y-10,1);}}else{addFloat(bx.x,bx.y-26,'TOPPED UP','#ffd23f',0.7);sfx('click');}}}}
    const lit=S.boxes.filter(q=>q.left>0).length;L.on=lit;
    if(!L.done&&lit>=S.n){L.done=1;for(const bx of S.boxes)bx.left=1e9;addFloat(P.x,P.y-48,'POWER RESTORED!','#7fe08a',2);labGoldGift(P.x,P.y-38,'THE PARK IS OPEN!');L.party=3;}
    if(L.party>0){L.party-=dt;if(Math.random()<dt*10)labBurst(rnd(20,G.pw-20),camY+rnd(20,VIEW_H*0.6),8,'coin',40);}
    let soon=null;if(!L.done)for(const bx of S.boxes)if(bx.left>0&&(soon==null||bx.left<soon))soon=bx.left;
    labObj('LIT',lit,S.n,L.done?'RESTORED':soon!=null?'FADES '+Math.ceil(soon)+'S':'');L.tgt=nearest(S.boxes,q=>!(q.left>0));},
  night(cy){const S=G.lab;if(!NB2)NB2=mk(W,VIEW_H);const x=NB2.getContext('2d');x.globalCompositeOperation='source-over';x.clearRect(0,0,W,VIEW_H);x.drawImage(G.night,0,cy,W,VIEW_H,0,0,W,VIEW_H);
    x.globalCompositeOperation='destination-out';
    for(const bx of S.boxes||[]){if(!(bx.left>0))continue;const k=Math.min(1,bx.litT/1.2),fade=Math.min(1,bx.left/2.5),fl=bx.left<6&&bx.left<1e8&&Math.random()<0.18?0.55:1,a0=fade*fl;
      if(k<1){x.fillStyle='rgba(0,0,0,'+a0.toFixed(2)+')';pixCircle(x,bx.x,Math.round(bx.y-cy),Math.round(16+k*280));}
      else for(const [m,a] of [[0,1],[8,0.55],[16,0.3]]){x.fillStyle='rgba(0,0,0,'+(a*a0).toFixed(2)+')';x.fillRect(0,bx.y0-cy-m,W,bx.y1-bx.y0+m*2);}}
    const vs=VSPEC[tool().id]||{hh:6},fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],L2=lightCone(P.f),G2=lightGlow(),fx=Math.round(P.x+fv[0]*(vs.hh-2)),fy=Math.round(P.y-cy+fv[1]*(vs.hh-2));
    x.drawImage(L2.c,fx-L2.o,fy-L2.o);x.drawImage(G2.c,Math.round(P.x)-G2.o,Math.round(P.y-cy)-G2.o);
    x.globalCompositeOperation='source-over';x.drawImage(L2.t,fx-L2.o,fy-L2.o);b.drawImage(NB2,0,cy);},
  over(cy){const S=G.lab;for(const bx of S.boxes||[]){if(bx.y<cy-40||bx.y>cy+VIEW_H+40)continue;const x=bx.x,y=bx.y;
    if(!(bx.left>0)){const p=0.5+0.5*Math.sin(tNow*5);b.fillStyle='rgba(255,210,63,'+(0.16+0.16*p).toFixed(2)+')';pixCircle(b,x,y,Math.round(13+p*6));b.fillStyle='rgba(255,239,122,0.12)';b.fillRect(x-2,y-60,5,60);
      R(b,x-7,y-7,14,14,K);R(b,x-6,y-6,12,12,'#ffd23f');for(let q=-6;q<6;q+=4)R(b,x+q,y-6,2,12,'#13306b');R(b,x-4,y-4,8,8,K);R(b,x-3,y-3,6,6,'#ffef7a');
      R(b,x,y-3,2,2,'#d8364b');R(b,x-1,y-1,3,1,'#d8364b');R(b,x-1,y,2,2,'#d8364b');if(Math.floor(tNow*3)%2)text(b,bx.ever?'RELIGHT':'POWER',x,y-17,'#ffd23f',{align:'center'});}
    else{R(b,x-7,y-7,14,14,K);R(b,x-6,y-6,12,12,'#7fe08a');R(b,x-3,y-3,6,6,'#ffffff');if(bx.left<1e8){const fr=bx.left/S.LIT,n2=24;for(let a=0;a<n2;a++){if(a/n2>fr)break;const an=-Math.PI/2+a/n2*Math.PI*2;R(b,Math.round(x+Math.cos(an)*10),Math.round(y+Math.sin(an)*10),1,1,bx.left<6?'#ff6a5a':'#ffd23f');}}}}},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ffd23f');}};

// ---------- AVALANCHE: outrun the wave (or hide in a shelter) ----------
function avShelter(x,y){const S=G.lab;return !!(S.sh&&S.sh.some(s=>x>s.x-2&&x<s.x+s.w+2&&y>s.y-2&&y<s.y+s.h+8));}
MODES.avalanche={name:'AVALANCHE',sub:'OUTRUN THE AVALANCHE',rule:'SIREN? DRIVE DOWNHILL OR HIDE!',col:'#ff6a5a',
  how:['NOW AND THEN THE MOUNTAIN LETS','GO. AT THE SIREN A WALL OF SNOW','RUSHES DOWN THE MAP: DRIVE AWAY','FROM IT OR DUCK INTO A ROCK','SHELTER. CAUGHT? YOU GET BURIED.'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+53);S.first=g.def.teach?12:10;S.every=g.def.teach?999:24;S.spd=g.def.teach?50:62;S.len=g.def.teach?320:420;S.need=g.def.teach?1:3;
    S.sh=[];for(let y=100;y<g.ph-90;y+=360){const p=labSpot(g,30,22,y,Math.min(g.ph-50,y+300),rn,{edge:true,margin:3});if(p){S.sh.push({x:p.x,y:p.y,w:30,h:22});labBlock(g,p.x,p.y,30,5);labPaint(g,p.x-2,p.y-2,34,28);}}
    MODES.avalanche.bonus=g.def.teach?'ESCAPE IT: GOLD GIFT':'ESCAPE 3 IN A ROW: GOLD GIFT';},
  tick(dt,tid,L){const S=G.lab;let A=L.av;if(!A)A=L.av={ph:'calm',t:S.first,n:0,esc:0,row:0,buried:0};L.urgent=A.ph==='warn'||A.ph==='wave';
    if(A.buried>0){A.buried-=dt;P.vx=P.vy=0;if(A.buried<=0)addFloat(P.x,P.y-28,'DUG OUT!','#ffffff',0.9);}
    if(A.ph==='calm'){A.t-=dt;if(A.t<=0&&run.time>8){A.ph='warn';A.t=A.tt=G.def.teach?4.5:3.5;A.sir=0;addFloat(P.x,P.y-32,'AVALANCHE!','#ff6a5a',1.4);}}
    else if(A.ph==='warn'){A.t-=dt;A.sir-=dt;if(A.sir<=0){A.sir=0.6;sfx('warn',0,{rate:0.75,vol:0.6});}shake=Math.max(shake,0.03+0.08*(1-A.t/A.tt));
      if(A.t<=0){A.ph='wave';A.fy=Math.max(4,camY-20);A.y0=A.fy;A.res=0;A.spd=clamp(moveSpeed()*(G.def.teach?0.72:0.85),36,96);sfx('squall');sfx('stomp');}}
    else if(A.ph==='wave'){A.fy+=(A.spd||S.spd)*dt;shake=Math.max(shake,0.1+0.1*Math.max(0,1-Math.abs(A.fy-P.y)/160));
      if(Math.random()<0.5){const x=rnd(4,G.pw-4),y=A.fy-rnd(0,24);if(y>2&&y<G.ph-2&&!avShelter(x,y))addSnowCircle(G,x,y,rnd(5,9),rnd(0.35,0.55));}
      const safe=avShelter(P.x,P.y);
      if(!A.res&&A.fy>=P.y-8&&!safe){A.res=1;A.n++;A.row=0;A.buried=2;P.stun=Math.max(P.stun,2);P.inv=Math.max(P.inv,2.6);P.vx=P.vy=0;shake=0.45;buzz(80);sfx('stomp');addFloat(P.x,P.y-32,'BURIED!','#ff6a5a',1.5);if(run.combo>=2){run.combo=0;run.comboProg=0;sfx('cend');}addSnowCircle(G,P.x,P.y,22,0.7);}
      if(A.fy-A.y0>=S.len||A.fy>G.ph-4){A.ph='calm';A.t=S.every+rnd(-2,3);if(!A.res){A.n++;A.esc++;A.row++;labPay(P.x,P.y-32,1.5,avShelter(P.x,P.y)?'SHELTERED!':'ESCAPED!','#7fe08a');labTime(P.x,P.y-22,3);sfx('win');if(A.row>=S.need)labGoldGift(P.x,P.y-44,A.row>1?A.row+' IN A ROW!':'YOU MADE IT!');}}}
    if(A.n)labRes('ESCAPED',A.esc,A.n);},
  over(cy){const S=G.lab,A=run.lab&&run.lab.av;
    for(const s of S.sh||[]){if(s.y<cy-30||s.y>cy+VIEW_H+30)continue;const x=s.x,y=s.y;R(b,x,y+4,s.w,s.h-4,'rgba(27,31,59,0.35)');R(b,x-1,y,s.w+2,7,K);R(b,x,y+1,s.w,5,'#7a869c');R(b,x,y+1,s.w,2,'#f4f8ff');R(b,x+2,y+6,4,s.h-6,K);R(b,x+3,y+6,2,s.h-7,'#8793a8');R(b,x+s.w-6,y+6,4,s.h-6,K);R(b,x+s.w-5,y+6,2,s.h-7,'#8793a8');
      if(A&&A.ph!=='calm'&&Math.floor(tNow*4)%2)text(b,'SHELTER',x+s.w/2,y-9,'#7fe08a',{align:'center'});}
    if(!A)return;
    if(A.ph==='warn'){const k=1-A.t/A.tt,yt=Math.round(camY);for(let x=0;x<W;x+=8){const hh=4+Math.round(((x*7)%11)*k*0.6)+Math.round(Math.sin(tNow*30+x)*k*2);R(b,x,yt,8,hh+2,K);R(b,x,yt,8,hh,'#eef4fc');}}
    if(A.ph==='wave'){const y=Math.round(A.fy);R(b,0,y,W,16,'rgba(27,31,59,0.3)');R(b,0,y+16,W,8,'rgba(27,31,59,0.14)');b.fillStyle='#dfe9f7';b.fillRect(0,y-90,W,90);b.fillStyle='#c3d4ec';b.fillRect(0,y-14,W,12);
      for(let x=0;x<W;x+=6){const h=5+((x*13+Math.floor(tNow*24))%8);R(b,x,y-3,6,h+1,K);R(b,x,y-3,6,h,'#eef4fc');R(b,x,y-4+h,6,1,'#9fb4d8');}
      for(let k=0;k<11;k++){const bx=(k*23+Math.floor(tNow*(70+k*9)))%(W+20)-10,by=y-6-((k*17)%40),r=3+(k%4);b.fillStyle=K;pixCircle(b,bx,by,r+1);b.fillStyle='#ffffff';pixCircle(b,bx,by,r);b.fillStyle='#c6d9f3';b.fillRect(bx-r+1,by+r-2,r*2-1,1);}
      for(let k=0;k<6;k++)particles.push({x:rnd(0,W),y:y+rnd(-4,6),vx:rnd(-30,30),vy:rnd(40,90),z:3,vz:rnd(10,40),life:0.5,t:0,kind:'snow'});R(b,0,y-90,W,2,'#9fb4d8');}
    if(A.buried>0){b.fillStyle='#e8f0fa';pixCircle(b,Math.round(P.x),Math.round(P.y+2),17);b.fillStyle='#ffffff';pixCircle(b,Math.round(P.x-4+Math.sin(tNow*30)),Math.round(P.y-3),9);if(Math.floor(tNow*4)%2)text(b,'DIG DIG!',P.x,P.y-24,'#ffffff',{align:'center'});}},
  screen(){const A=run.lab&&run.lab.av;if(!A)return;
    if(A.ph==='warn'){if(Math.floor(tNow*6)%2){panel(10,VIEW_Y+20,160,15,'#5c0e1e','#ff6a5a');text(b,'AVALANCHE! DRIVE DOWNHILL OR HIDE',W/2,VIEW_Y+24,'#ffffff',{align:'center',outline:null});}text(b,''+Math.ceil(A.t),W/2,VIEW_Y+40,'#ff6a5a',{align:'center',scale:2});}
    if(A.ph==='wave'&&A.fy<camY+VIEW_H){const d=Math.max(0,Math.round(P.y-A.fy));if(Math.floor(tNow*6)%2)text(b,d<60?'GO GO GO!':'KEEP GOING!',W/2,VIEW_Y+VIEW_H-30,d<60?'#ff6a5a':'#ffffff',{align:'center',scale:2});}
    if(A.ph!=='calm'){const S=G.lab,s=nearest((S.sh||[]).map(q=>({x:q.x+q.w/2,y:q.y+q.h/2})),q=>q.y>P.y-200&&q.y<P.y+260);if(s)labArrow(s.x,s.y,'#7fe08a');}}};

// ---------- LOST PENGUINS: bring each chick back to its own family ----------
const PCOL=['#ff6a7a','#7fe08a','#ffd23f','#c4a0f5'];
const CHICK_FR=[spr(["..KKK..",".KKKKK.",".KWKWK.",".KWWWK.","KGGGGGK","KGGGGGK",".KGGGK.","..O.O.."],{G:'#9aa4b8',W:'#f4f8ff',O:'#ff9a3c'}),spr(["..KKK..",".KKKKK.",".KWKWK.",".KWWWK.","KGGGGGK","KGGGGGK",".KGGGK.",".O...O."],{G:'#9aa4b8',W:'#f4f8ff',O:'#ff9a3c'})];
MODES.penguins={name:'LOST PENGUINS',sub:'REUNITE THE CHICKS',rule:'TAKE EACH CHICK TO ITS FAMILY',bonus:'ALL REUNITED: GOLD GIFT',col:'#9fd8ff',
  how:['PENGUIN CHICKS ARE LOST IN THE','FOG. FOLLOW THEIR PEEPS, PICK ONE','UP, AND TAKE IT TO THE FAMILY','WITH THE SAME COLOUR. FAMILIES','CALL OUT WHEN YOU HAVE THEIR CHICK.'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+41),tid=labTid(),base=labReachGrid(g,tid),n=g.def.teach?2:(g.ph>4000?4:3);S.fam=[];S.chicks=[];
    const pengs=g.hazards.filter(h=>h.kind==='sheep'&&h.peng),used=new Set(),grps=[];
    for(const h of pengs){if(used.has(h))continue;const grp=pengs.filter(o=>!used.has(o)&&Math.hypot(o.x-h.x,o.y-h.y)<46);if(grp.length<2)continue;grp.forEach(o=>used.add(o));
      const cx=grp.reduce((a,o)=>a+o.x,0)/grp.length+4,cy=grp.reduce((a,o)=>a+o.y,0)/grp.length+3;if(labCanReach(base,cx,cy,44)&&Math.hypot(cx-g.start.x,cy-g.start.y)>90)grps.push({x:cx,y:cy,ad:grp});}
    const fixAd=f=>{for(const a of f.ad){a.stray=1;a.hx=a.x;a.hy=a.y;a.vx=a.vy=0;}};
    grps.sort((a,c)=>a.y-c.y);for(const q of grps)if(S.fam.length<n&&S.fam.every(f=>Math.abs(f.y-q.y)>240))S.fam.push(q);
    const bands=labBands(g,n);for(let k=0;S.fam.length<n&&k<n*3;k++){const [y0,y1]=bands[k%n];if(S.fam.some(f=>f.y>=y0&&f.y<y1))continue;
      const p=labSpot(g,26,14,y0,y1,rn,{margin:8,xin:16,avoid:S.fam.map(f=>({x:f.x,y:f.y,r:220})).concat([{x:g.start.x,y:g.start.y,r:90}])});if(!p||!labCanReach(base,p.x+13,p.y+7,44))continue;
      const ad=[0,1].map(j=>{const hz={kind:'sheep',peng:true,horse:false,col:0,x:p.x+j*13,y:p.y+(j?2:0),w:8,h:6,hx:p.x+j*13,hy:p.y+(j?2:0),vx:0,vy:0,t:rn()*3,anim:rn()*2};g.hazards.push(hz);return hz;});S.fam.push({x:p.x+13,y:p.y+7,ad});}
    S.fam.forEach((f,k)=>{f.col=PCOL[k%PCOL.length];f.k=k;fixAd(f);});
    for(const f of S.fam){let q=null;const far=Math.max(170,Math.min(320,g.ph*0.12));for(let tr=0;tr<80&&!q;tr++){const c=labSpot(g,10,10,0,g.ph,rn,{near:{x:f.x,y:f.y,r0:far,r1:far+260+Math.max(0,tr-40)*10},margin:6,avoid:S.fam.map(o=>({x:o.x,y:o.y,r:o===f?far:120})).concat([{x:g.start.x,y:g.start.y,r:70}],S.chicks.map(o=>({x:o.x,y:o.y,r:100})))});if(c&&c.x>=16&&c.x<=g.pw-26&&labCanReach(base,c.x+5,c.y+5,30))q=c;}
      if(q)S.chicks.push({x:q.x+5,y:q.y+5,st:'lost',fam:f,ping:rn()*2.4,pt:9,hop:0,t:0});}
    S.n=S.chicks.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.chicks||!S.chicks.length)return;if(!L.tr){L.tr=[];L.home=0;L.inv0=P.inv;}
    const last=L.tr[L.tr.length-1];if(!last||Math.hypot(P.x-last.x,P.y-last.y)>=2){L.tr.push({x:P.x,y:P.y});if(L.tr.length>600)L.tr.splice(0,L.tr.length-600);}
    if(P.inv>L.inv0+0.3){const f=S.chicks.filter(c=>c.st==='follow');if(f.length){for(const c of f){c.st='lost';c.x=clamp(c.x+rnd(-16,16),6,G.pw-6);c.y=clamp(c.y+rnd(-12,12),6,G.ph-6);c.ping=0;}addFloat(P.x,P.y-32,'PEEP PEEP! THEY SCATTERED','#ff9aa8',1.2);sfx('cend');}}
    L.inv0=P.inv;const hl=(VSPEC[tid]?VSPEC[tid].hh:6)+5;let k=0;
    for(const c of S.chicks){if(c.st==='lost'){c.ping-=dt;c.pt+=dt;if(c.ping<=0){c.ping=2.4;c.pt=0;}
        if(Math.hypot(P.x-c.x,P.y-c.y)<20||labTouch(tid,{x:c.x-5,y:c.y-5,w:10,h:10})){c.st='follow';sfx('gift',0,{rate:1.6});addFloat(c.x,c.y-12,'PEEP!','#ffffff',0.8);labRing(c.x,c.y,8);}}
      else if(c.st==='follow'){const d=hl+(k+1)*11;let acc=0,pt=null;for(let j=L.tr.length-1;j>0;j--){acc+=Math.hypot(L.tr[j].x-L.tr[j-1].x,L.tr[j].y-L.tr[j-1].y);if(acc>=d){pt=L.tr[j-1];break;}}
        if(pt){c.x+=(pt.x-c.x)*Math.min(1,dt*10);c.y+=(pt.y-c.y)*Math.min(1,dt*10);}c.hop+=dt;k++;
        for(const f of S.fam){if(Math.hypot(c.x-f.x,c.y-f.y)>38&&Math.hypot(P.x-f.x,P.y-f.y)>=50)continue;if(f===c.fam){c.st='in';c.t=0;c.tx=f.x-2+((f.home||0)%3)*4;c.ty=f.y+6;f.home=(f.home||0)+1;f.joy=2;L.home++;labPay(f.x,f.y-22,1.2,'REUNITED!','#9fd8ff');labTime(f.x,f.y-12,3);sfx('gift');labRing(f.x,f.y,14);
            if(L.home>=S.n)labGoldGift(P.x,P.y-42,'ALL FAMILIES TOGETHER!');}else if(!(f.no>0)){f.no=2;addFloat(f.x,f.y-20,'NOT OURS!','#ff9aa8',0.9);sfx('deny');}break;}}
      else if(c.st==='in'){c.t+=dt;const q=Math.min(1,c.t/0.5);c.x+=(c.tx-c.x)*q;c.y+=(c.ty-c.y)*q;}}
    for(const f of S.fam){if(f.no>0)f.no-=dt;if(f.joy>0)f.joy-=dt;f.call=S.chicks.some(c=>c.st==='follow'&&c.fam===f);}
    const fol=S.chicks.filter(c=>c.st==='follow');labObj('REUNITED',L.home,S.n,fol.length?'+'+fol.length+' WITH YOU':'');
    if(fol.length){const f=fol[0].fam;L.tgt={x:f.x,y:f.y,col:f.col};}else{const c=nearest(S.chicks,q=>q.st==='lost');L.tgt=c?{x:c.x,y:c.y,col:'#9fd8ff'}:null;}},
  ents(ents,top,bot){const S=G.lab;if(!S.chicks)return;
    for(const f of S.fam){if(f.y<top-30||f.y>bot+30)continue;ents.push({base:f.y-8,draw:()=>{b.fillStyle='rgba(27,31,59,0.18)';pixCircle(b,Math.round(f.x),Math.round(f.y+2),15);b.fillStyle=f.col;for(let a=0;a<24;a+=2){const an=a/24*Math.PI*2;b.fillRect(Math.round(f.x+Math.cos(an)*15),Math.round(f.y+2+Math.sin(an)*9),2,1);}}});
      for(const ad of f.ad||[])if(ad.y>top-20&&ad.y<bot+20)ents.push({base:ad.y+ad.h+0.2,draw:()=>{R(b,Math.round(ad.x)+1,Math.round(ad.y)-1,6,2,K);R(b,Math.round(ad.x)+2,Math.round(ad.y)-1,4,1,f.col);}});
      if(f.joy>0)ents.push({base:f.y+40,draw:()=>{const y=Math.round(f.y-20-(2-f.joy)*6);R(b,f.x-2,y,2,1,'#ff4f7a');R(b,f.x+1,y,2,1,'#ff4f7a');R(b,f.x-2,y+1,5,1,'#ff4f7a');R(b,f.x-1,y+2,3,1,'#ff4f7a');R(b,f.x,y+3,1,1,'#ff4f7a');}});}
    for(const c of S.chicks){if(c.y<top-10||c.y>bot+10)continue;ents.push({base:c.y+3,draw:()=>{const mv=c.st==='follow'?Math.floor(c.hop*8)%2:Math.floor(tNow*2+c.x)%2;const x=Math.round(c.x-3),y=Math.round(c.y-6-(c.st==='follow'&&mv?1:0));b.drawImage(CHICK_FR[mv],x,y);R(b,x+1,y+4,5,1,c.fam.col);}});}},
  over(cy){const S=G.lab;if(!S.chicks)return;labFog(cy,G.def.teach?0.84:0.9);
    for(const c of S.chicks){if(c.st!=='lost'||c.pt>0.9||c.y<cy-40||c.y>cy+VIEW_H+40)continue;const r=Math.round(4+c.pt*28),a=(1-c.pt/0.9)*0.9;b.strokeStyle='rgba(63,134,214,'+a.toFixed(2)+')';b.lineWidth=1;b.beginPath();b.arc(c.x,c.y,r,0,Math.PI*2);b.stroke();
      if(c.pt<0.5)text(b,'PEEP',c.x,c.y-r-8,'#3f86d6',{align:'center',outline:null});}
    for(const f of S.fam){if(!f.call||f.y<cy-60||f.y>cy+VIEW_H+60)continue;const ph=(tNow*1.2+f.k*0.3)%1,r=Math.round(6+ph*34);b.strokeStyle=f.col;b.globalAlpha=1-ph;b.lineWidth=2;b.beginPath();b.arc(f.x,f.y,r,0,Math.PI*2);b.stroke();b.globalAlpha=1;b.lineWidth=1;
      if(ph<0.5)text(b,'OUR CHICK!',f.x,f.y-r-10,f.col,{align:'center'});}},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,L.tgt.col);}};
function tiThaw(g,S,x,y,r){const fx=S.fx.getContext('2d'),cols=g.cols;for(let cy=Math.max(0,Math.floor((y-r)/2));cy<=Math.min(g.rows-1,Math.floor((y+r)/2));cy++)for(let cx=Math.max(0,Math.floor((x-r)/2));cx<=Math.min(cols-1,Math.floor((x+r)/2));cx++){
  const dx=cx*2+1-x,dy=cy*2+1-y;if(dx*dx+dy*dy>r*r)continue;const i=cy*cols+cx;if(S.st[i]){if(S.st[i]===2)S.nh--;S.st[i]=0;fx.clearRect(cx*2,cy*2,2,2);}}}
loadSave();save.sess=(save.sess||0)+1;""")
open(f,'w',encoding='utf-8').write(s)
print('p155 lab rework: herding round-up, 4-side dig-out, timed power sections + new beam, safe thin ice, outrun avalanche, penguin families, hints + gold gifts')
