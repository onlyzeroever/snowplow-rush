import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# The seven area twists, rebuilt so each one changes what you do (Alex: "the ice cracks you can't see it ... the cars
# I can't tell what happens ... the mud is small patches you can already see which don't really do much").
# stray sheep (Round-Up) get nudged by the plow instead of counting as a crash
rep("if(tid!=='ufo'&&!hz.gull&&overlap(pr,hz)){hit('ob');","if(tid!=='ufo'&&!hz.gull&&!hz.stray&&overlap(pr,hz)){hit('ob');")

rep("function sprAlpha(c){",r"""// ================= LAB rev 2: AREA TWISTS =================
const FISH_FR=[spr(["..KKK...",".KCCCK.K","KCWCCCKK",".KCCCK.K","..KKK..."],{C:'#7fb0e0',W:'#ffffff'}),spr(["........","..KKK..K",".KCWCCKK","KCCCCCK.",".KKKKK.."],{C:'#7fb0e0',W:'#ffffff'})];
const FLAGC={};function flagSpr(col,fr){const k=col+fr;if(FLAGC[k])return FLAGC[k];const c=mk(9,17),g=c.getContext('2d');R(g,0,1,2,16,K);R(g,0,1,1,15,'#e8eef8');const w=fr?6:7;R(g,2,1,w,7,K);R(g,2,2,w-1,5,col);R(g,2,2,w-1,1,'rgba(255,255,255,0.7)');R(g,2,6,w-1,1,'rgba(0,0,0,0.25)');return FLAGC[k]=c;}
function fenceH(w){const c=mk(w,9),g=c.getContext('2d');R(g,0,2,w,2,K);R(g,0,2,w,1,'#c98d4a');R(g,0,5,w,2,K);R(g,0,5,w,1,'#a8673a');R(g,0,1,w,1,'#f4f8ff');
  for(let x=0;x<w;x+=8){const px=Math.min(x,w-3);R(g,px,0,3,9,K);R(g,px+1,1,1,7,'#8a5530');R(g,px,0,3,1,'#ffffff');}return c;}
function fenceV(h){const c=mk(5,h),g=c.getContext('2d');R(g,1,0,3,h,K);R(g,2,0,1,h,'#c98d4a');for(let y=0;y<h;y+=8){const py=Math.min(y,h-4);R(g,0,py,5,4,K);R(g,1,py+1,3,2,'#8a5530');R(g,1,py,3,1,'#ffffff');}return c;}
function labFence(g,x,y,w,h,spr2,sx,sy){const o={spr:spr2,src:spr2,sx,sy,x,y,w,h,bld:false,lab:1};o.base=o.y+o.h;g.obstacles.push(o);labBlock(g,x,y,w,h);return o;}
let NB2=null,FB2=null;
function labFog(cy,a){if(!FB2)FB2=mk(W,VIEW_H);const x=FB2.getContext('2d');x.globalCompositeOperation='source-over';x.clearRect(0,0,W,VIEW_H);x.fillStyle='rgba(232,240,252,'+a+')';x.fillRect(0,0,W,VIEW_H);
  for(let k=0;k<14;k++){const yy=(k*41+Math.floor(tNow*8))%VIEW_H,xx=((k*67+tNow*14)%(W+60))-30;x.fillStyle='rgba(255,255,255,0.5)';x.fillRect(Math.round(xx),yy,40,3);}
  x.globalCompositeOperation='destination-out';const px=Math.round(P.x),py=Math.round(P.y-cy);for(const [r,al] of [[72,0.25],[60,0.3],[48,0.35],[38,0.5],[28,0.9]]){x.fillStyle='rgba(0,0,0,'+al+')';pixCircle(x,px,py,r);}
  x.globalCompositeOperation='source-over';b.drawImage(FB2,0,cy);}
function nearest(list,f){let best=null,bd=1e9;for(const q of list){if(f&&!f(q))continue;const d=Math.hypot(q.x-P.x,q.y-P.y);if(d<bd){bd=d;best=q;}}return best;}

// ---------- THIN ICE (harbour): the ice cracks where you drive; drive on cracked ice again (or stop on it) and it breaks ----------
function tiCrack(g,S,fp){const x=S.fx.getContext('2d');for(let k=0;k<4;k++){const px=fp.x+2+Math.random()*(fp.w-4),py=fp.y+2+Math.random()*(fp.h-4),br=2+((Math.random()*3)|0);
  for(let j=0;j<br;j++){let a=Math.random()*Math.PI*2,qx=px,qy=py;const len=3+((Math.random()*6)|0);for(let st=0;st<len;st++){qx+=Math.cos(a);qy+=Math.sin(a)*0.8;a+=(Math.random()-0.5)*1.2;
    const ix=Math.round(qx),iy=Math.round(qy);if(ix<0||iy<0||ix>=g.pw-1||iy>=g.ph)break;const ci=(iy>>1)*g.cols+(ix>>1);if(S.st[ci]!==1)break;
    x.fillStyle=st<3?'#1f4878':'#3a6aa6';x.fillRect(ix,iy,1,1);if(st%2===0){x.fillStyle='rgba(255,255,255,0.95)';x.fillRect(ix+1,iy,1,1);}}}}}
MODES.thinice={name:'THIN ICE',sub:"DON'T CROSS YOUR TRACKS",rule:"DON'T CROSS YOUR OWN TRACKS",col:'#7ad3ff',
  how:['THE FROZEN HARBOUR CRACKS WHERE','YOU DRIVE. DRIVE ON CRACKED ICE','AGAIN, OR STOP ON IT, AND IT','BREAKS. FALL IN: YOU GET TOWED.','PLAN YOUR LANES. HOLES REFREEZE.','BREAKING ICE CAN FLIP UP A FISH!'],
  post(g){const n=g.cols*g.rows,S=g.lab;S.st=new Uint8Array(n);S.t=new Float32Array(n);S.fx=mk(g.pw,g.ph);S.cq=[];S.ci=0;S.hq=[];S.hi=0;S.nh=0;
    S.keep=g.def.teach?2.0:1.4;S.thr=g.def.teach?0.75:0.62;S.thaw=g.def.teach?8:13;S.heal=g.def.teach?16:26;let ice=0;for(let i=0;i<n;i++)if(g.type[i]===T_ICE)ice++;S.ice=ice;},
  tick(dt,tid,L){const g=G,S=g.lab;if(!S.st||!S.ice)return;const now=L.t,cols=g.cols,fx=S.fx.getContext('2d');
    if(!L.ti){L.ti=1;L.safe={x:P.x,y:P.y};L.sunk=0;L.brkT=0;L.crkT=0;L.creak=0;L.moved=0;L.px=P.x;L.py=P.y;L.falls=0;L.fish=[];L.fishT=0;}
    while(S.ci<S.cq.length&&now-S.cq[S.ci][1]>S.heal){const q=S.cq[S.ci++];if(S.st[q[0]]===1&&S.t[q[0]]===q[1]){S.st[q[0]]=0;fx.clearRect((q[0]%cols)*2,((q[0]/cols)|0)*2,2,2);}}
    while(S.hi<S.hq.length&&now-S.hq[S.hi][1]>S.thaw){const q=S.hq[S.hi++];if(S.st[q[0]]===2&&S.t[q[0]]===q[1]){S.st[q[0]]=0;S.nh--;}}
    L.fishT-=dt;for(const fh of L.fish){fh.t+=dt;if(!fh.got&&Math.hypot(P.x-fh.x,P.y-fh.y)<13){fh.got=1;labPay(fh.x,fh.y-10,0.35,'FRESH FISH!','#7fb0e0');sfx('gift',0,{rate:1.3});}}L.fish=L.fish.filter(fh=>!fh.got&&fh.t<5);
    if(L.sunk>0){L.sunk-=dt;P.vx=P.vy=0;if(L.sunk<=0){P.x=L.safe.x;P.y=L.safe.y;const f2=footprint(tid,P.x,P.y,P.f);
        for(let cy=Math.max(0,f2.y>>1);cy<=Math.min(g.rows-1,(f2.y+f2.h)>>1);cy++)for(let cx=Math.max(0,f2.x>>1);cx<=Math.min(cols-1,(f2.x+f2.w)>>1);cx++){const i=cy*cols+cx;if(S.st[i]){if(S.st[i]===2)S.nh--;S.st[i]=0;fx.clearRect(cx*2,cy*2,2,2);}}
        P.inv=Math.max(P.inv,1);addFloat(P.x,P.y-26,'TOWED OUT','#ffffff',1.1);sfx('whoosh');labRing(P.x,P.y,14);}return;}
    if(tid==='ufo'||!run.moved||L.t<1)return;
    const fp=footprint(tid,P.x,P.y,P.f),x0=Math.max(0,(fp.x+1)>>1),x1=Math.min(cols-1,(fp.x+fp.w-2)>>1),y0=Math.max(0,(fp.y+1)>>1),y1=Math.min(g.rows-1,(fp.y+fp.h-2)>>1);
    let n=0,holes=0,old=0,fresh=0,brk=0;
    for(let cy=y0;cy<=y1;cy++)for(let cx=x0;cx<=x1;cx++){const i=cy*cols+cx;if(g.type[i]!==T_ICE)continue;n++;const st=S.st[i];
      if(st===0){S.st[i]=1;S.t[i]=now;S.cq.push([i,now]);fresh++;fx.fillStyle='rgba(38,82,140,0.2)';fx.fillRect(cx*2,cy*2,2,2);}
      else if(st===1){const a=now-S.t[i];if(a>S.keep){S.st[i]=2;S.t[i]=now;S.hq.push([i,now]);S.nh++;brk++;fx.clearRect(cx*2,cy*2,2,2);}else if(a>S.keep*0.5)old++;}
      else holes++;}
    L.moved+=Math.hypot(P.x-L.px,P.y-L.py);L.px=P.x;L.py=P.y;
    if(fresh&&L.moved>4){L.moved=0;tiCrack(g,S,fp);L.crkT-=1;if(L.crkT<=0){L.crkT=5;sfx('crunch',0,{vol:0.2,rate:0.5+Math.random()*0.2});}}
    if(brk){L.brkT-=dt;if(L.brkT<=0){L.brkT=0.16;sfx('splat',0,{vol:0.4,rate:1.3});shake=Math.max(shake,0.1);buzz(15);}labBurst(fp.x+Math.random()*fp.w,fp.y+Math.random()*fp.h,Math.min(8,brk),'snow',45);
      if(!L.crackSaid||now-L.crackSaid>1.6){L.crackSaid=now;addFloat(P.x,P.y-26,'CRACK!','#7ad3ff',0.8);}
      if(brk>=5&&L.fishT<=0&&Math.random()<0.4){L.fishT=2.5;const fx2=clamp(P.x+rnd(-26,26),8,g.pw-8),fy2=clamp(P.y+rnd(-30,30),8,g.ph-8);L.fish.push({x:fx2,y:fy2,t:0});addFloat(fx2,fy2-12,'A FISH!','#ffffff',0.8);}}
    if(n>=4&&old/n>0.3){L.creak+=dt;if(L.creak>0.2&&(!L.creakSaid||now-L.creakSaid>1.3)){L.creakSaid=now;addFloat(P.x,P.y-30,'IT IS GIVING WAY! MOVE!','#ff9aa8',0.9);sfx('tick',0,{rate:0.5,vol:0.6});}}else L.creak=0;
    if(n>=4&&holes/n>=S.thr){L.sunk=1.3;L.falls++;P.stun=1.4;P.inv=2.6;P.vx=P.vy=0;shake=0.35;buzz(60);sfx('splat');sfx('deny');addFloat(P.x,P.y-30,'SPLOOSH!','#7ad3ff',1.4);
      if(run.combo>=2){run.combo=0;run.comboProg=0;sfx('cend');}labBurst(P.x,P.y,26,'snow',70);labRing(P.x,P.y,16);return;}
    if(holes===0&&brk===0&&old===0){L.safeT=(L.safeT||0)+dt;if(n===0||L.safeT>0.3){L.safeT=0;L.safe={x:P.x,y:P.y};}}else L.safeT=0;},
  ents(ents,top,bot){const g=G,S=g.lab;if(!S.st||!S.ice)return;const L=run.lab||{};
    ents.push({base:-1e9+1,draw:()=>{const y0=Math.max(0,Math.floor(top)),hh=Math.min(g.ph,Math.ceil(bot))-y0;if(hh>0)b.drawImage(S.fx,0,y0,g.pw,hh,0,y0,g.pw,hh);
      const now=L.t||0,cols=g.cols;for(let k=S.hi;k<S.hq.length;k++){const q=S.hq[k],i=q[0];if(S.st[i]!==2||S.t[i]!==q[1])continue;const x=(i%cols)*2,y=((i/cols)|0)*2;if(y<top-2||y>bot+2)continue;
        const left=S.thaw-(now-q[1]),hs=Math.imul(i,2654435761)>>>0;R(b,x,y,2,2,left<1.5?'#a9cdee':left<4?'#3f75b0':'#174680');
        if(left>=4&&(x+y+Math.floor(tNow*6))%11===0)R(b,x,y,2,1,'#3a72b0');if(left<4&&hs%3===0)R(b,x+(hs>>3&1),y,1,1,'#e8f4ff');
        const eL=S.st[i-1]!==2,eR=S.st[i+1]!==2,eU=S.st[i-cols]!==2,eD=S.st[i+cols]!==2;
        if(eU){R(b,x,y-(hs&1),2,1+(hs&1),'#ffffff');R(b,x,y+1,2,1,'#9fc8ee');}if(eD){R(b,x,y+1,2,1,'#cfe6fb');R(b,x+(hs>>2&1),y+2,1,1,'#7aa8d8');}
        if(eL){R(b,x-((hs>>4)&1),y,1+((hs>>4)&1),2,'#d8ecff');}if(eR){R(b,x+1,y,1+((hs>>5)&1),2,'#b8d8f4');}
        if(left>=4&&!eL&&!eR&&!eU&&!eD&&hs%29===0){const bo=Math.floor(tNow*2+i)%2;R(b,x-1,y-1+bo,4,3,'#7aa8d8');R(b,x-1,y-2+bo,4,2,'#f4f8ff');}}}});
    for(const fh of L.fish||[])if(fh.y>top-10&&fh.y<bot+10)ents.push({base:fh.y+3,draw:()=>{const fr=Math.floor(tNow*8)%2;b.drawImage(FISH_FR[fr],Math.round(fh.x-4),Math.round(fh.y-3-(fr?2:0)));}});
    if(L.sunk>0)ents.push({base:P.y+400,draw:()=>{const k=1-L.sunk/1.3;b.fillStyle='rgba(29,79,140,0.78)';pixCircle(b,Math.round(P.x),Math.round(P.y+3),Math.round(13+k*5));
      b.fillStyle='rgba(216,236,255,0.95)';for(let a=0;a<14;a++){const an=a/14*Math.PI*2+tNow*2;b.fillRect(Math.round(P.x+Math.cos(an)*(14+k*5)),Math.round(P.y+3+Math.sin(an)*(10+k*4)),2,1);}
      if(Math.floor(tNow*5)%2)text(b,'GLUG!',P.x,P.y-22,'#ffffff',{align:'center'});}});}};

// ---------- DIG-OUT (city): cars buried in drifts; plow all round one to free it ----------
MODES.digout={name:'DIG-OUT',sub:'FREE THE SNOWED-IN CARS',rule:'PLOW ROUND THE BURIED CARS',col:'#ffb04a',
  how:['CARS ARE BURIED IN SNOWDRIFTS','AND THEIR DRIVERS ARE STUCK.','PLOW ALL ROUND A CAR TO DIG IT','OUT: THE DRIVER TIPS YOU AND','DRIVES OFF. FREE THEM ALL: BONUS!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+11),n=g.def.teach?3:Math.max(3,Math.min(5,Math.round(g.ph/650))),bands=labBands(g,n),av=[{x:g.start.x,y:g.start.y,r:70}];S.cars=[];
    for(let k=0;k<n;k++){const [y0,y1]=bands[k];let p=null;for(let tr=0;tr<12&&!p;tr++){const q=labSpot(g,24,30,y0,y1,rn,{margin:tr<8?16:10,avoid:av});if(!q)continue;q.x-=q.x&1;q.y-=q.y&1;const back=labRect(g,q.x,q.y+28,22,30),L2=labRect(g,2,q.y+32,q.x+2,23),R2=labRect(g,q.x+18,q.y+32,g.pw-2-(q.x+18),23);if(back&&(L2||R2))p=q;else if(tr===11)p=q;}if(!p)continue;
      const c=CAR_PAL[(k*2+1)%5],hz={kind:'pull',x:p.x,y:p.y,w:22,h:28,home:p.y,hx:p.x,body:c[0],dir:1,state:'park',t:1e9,spr:carSprite(c[0],c[1]),buried:1,cells:[],ring:[],side:p.x<g.pw/2?1:-1,ped:SPR.peds[k%SPR.peds.length]};
      for(let cy=p.y>>1;cy<(p.y+28)>>1;cy++)for(let cx=(p.x+1)>>1;cx<(p.x+23)>>1;cx++){const i=cy*g.cols+cx;if(g.type[i]===T_BLOCK)continue;hz.cells.push(i,g.type[i]);setDepth(g,i,0);}
      labBlock(g,p.x+1,p.y,22,28);
      for(let cy=Math.max(0,(p.y-10)>>1);cy<Math.min(g.rows,(p.y+38)>>1);cy++)for(let cx=Math.max(0,(p.x-8)>>1);cx<Math.min(g.cols,(p.x+32)>>1);cx++){const i=cy*g.cols+cx;if(g.type[i]===T_BLOCK||(g.nc&&g.nc[i]))continue;setDepth(g,i,Math.max(g.depth[i],1));hz.ring.push(i);}
      g.hazards.push(hz);if(g.pullBlocks)g.pullBlocks.push([p.x+1,p.y,22,28,hz]);S.cars.push(hz);av.push({x:p.x+12,y:p.y+14,r:60});labPaint(g,p.x-12,p.y-12,48,54);}
    S.n=S.cars.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.cars)return;if(L.dn==null)L.dn=0;const pr=footprint(tid,P.x,P.y,P.f);
    for(const hz of S.cars){
      if(hz.buried&&!hz.rf){hz.rf=1;hz.ring=hz.ring.filter(i=>!(G.nc&&G.nc[i])&&G.type[i]!==T_BLOCK);}
      if(hz.buried){let c2=0;for(const i of hz.ring)if(G.depth[i]<CLEAR_T)c2++;hz.prog=hz.ring.length?c2/hz.ring.length:1;
        if(!hz.said&&Math.hypot(P.x-(hz.x+11),P.y-(hz.y+14))<110){hz.said=1;addFloat(hz.x+11,hz.y-22,'HELP! SNOWED IN!','#ffffff',1.6);sfx('horn',0,{vol:0.3,rate:1.3});}
        if(hz.prog>=0.7){hz.buried=0;hz.freed=1;hz.t=0.9;hz.exit=undefined;L.dn++;labBurst(hz.x+11,hz.y+12,24,'snow',65);labRing(hz.x+11,hz.y+14,18);
          labPay(hz.x+11,hz.y-12,1,'THANKS!');labTime(hz.x+11,hz.y-2,3);sfx('horn',0,{vol:0.6});shake=Math.max(shake,0.12);hz.flash=1.2;
          if(L.dn>=S.n){labPay(P.x,P.y-38,3,'ALL CARS FREE!','#7fe08a');sfx('fanfare');}}}
      else if(hz.freed){if(hz.flash>0)hz.flash-=dt;if(hz.state==='park'&&overlap(pr,{x:hz.hx-2,y:hz.home+24,w:26,h:40}))hz.t=Math.max(hz.t,0.4);if(hz.state==='away')hz.dead=true;}}
    labObj('CARS',L.dn,S.n);const nx=nearest(S.cars.map(h=>({x:h.x+11,y:h.y+14,h})),q=>q.h.buried);L.tgt=nx;},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ffb04a');},
  ents(ents,top,bot){const S=G.lab;if(!S.cars)return;for(const hz of S.cars){if(hz.dead||hz.y>bot+40||hz.y<top-60)continue;const cx=hz.x+11,cy=hz.y+14;
    if(hz.buried){const k=1-Math.min(1,(hz.prog||0)/0.7);ents.push({base:hz.y+hz.h+0.5,draw:()=>{
        if(k>0.04){const lumps=[[-13,-8,6],[-14,2,7],[-12,11,6],[13,-8,6],[14,2,7],[12,11,6],[-7,16,6],[2,17,7],[9,15,5],[-3,-13,5],[4,-12,4]];b.fillStyle='rgba(27,31,59,0.35)';for(const [lx,ly,lr] of lumps)pixCircle(b,cx+lx,cy+ly+1,Math.max(1,Math.round(lr*k)+1));b.fillStyle='#a6c2ea';for(const [lx,ly,lr] of lumps)pixCircle(b,cx+lx,cy+ly+1,Math.max(1,Math.round(lr*k)));b.fillStyle='#f4f8ff';for(const [lx,ly,lr] of lumps)pixCircle(b,cx+lx,cy+ly-1,Math.max(1,Math.round(lr*k)-1));const pu=Math.floor(tNow*3)%2;b.strokeStyle='rgba(255,176,74,'+(pu?0.9:0.5)+')';b.lineWidth=1;b.strokeRect(hz.x-6.5,hz.y-6.5,35,43);}
        const px=hz.side>0?hz.x+27:hz.x-13,fr=Math.floor(tNow*3)%2;if(hz.ped)b.drawImage(hz.ped,px,hz.y+6-fr);
        if(Math.hypot(P.x-cx,P.y-cy)<130){const bw=28,p2=Math.min(1,(hz.prog||0)/0.7);R(b,cx-bw/2-1,hz.y-10,bw+2,5,K);R(b,cx-bw/2,hz.y-9,Math.round(bw*p2),3,p2>0.7?'#7fe08a':'#ffb04a');text(b,'DIG OUT',cx,hz.y-18,'#ffffff',{align:'center'});}}});}
    else if(hz.freed&&hz.flash>0&&Math.floor(tNow*8)%2===0&&hz.state==='park')ents.push({base:hz.y+hz.h+1,draw:()=>{R(b,hz.x+1,hz.y+23,5,3,'#fff6b0');R(b,hz.x+16,hz.y+23,5,3,'#fff6b0');}});}}};

// ---------- ROUND-UP (farm): stray sheep; push them into the pens ----------
MODES.roundup={name:'ROUND-UP',sub:'HERD SHEEP INTO PENS',rule:'PUSH THE SHEEP INTO THE PENS',col:'#c98d4a',
  how:['SHEEP HAVE GOT OUT. THEY RUN','FROM YOUR PLOW, SO DRIVE ROUND','BEHIND ONE AND PUSH IT TOWARD A','PEN GATE. EACH SHEEP HOME PAYS','AND ADDS TIME. ALL HOME: BONUS!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+17),np=g.def.teach?1:Math.max(1,Math.min(3,Math.round(g.ph/600))),per=g.def.teach?3:2,bands=labBands(g,np);S.pens=[];S.sheep=[];S.lure=g.def.teach?34:26;
    const av=[{x:g.start.x,y:g.start.y,r:60}];
    for(let k=0;k<np;k++){const [y0,y1]=bands[k];const p=labSpot(g,52,40,y0,y1,rn,{margin:12,avoid:av});if(!p)continue;const x=p.x,y=p.y;av.push({x:x+26,y:y+20,r:120});
      const pen={x,y,w:52,h:40,cx:x+26,cy:y+22,ix:x+3,iy:y+8,iw:46,ih:29};S.pens.push(pen);
      const hs=fenceH(14),vs=fenceV(35);labFence(g,x,y+5,14,3,hs,x,y);labFence(g,x+38,y+5,14,3,hs,x+38,y);labFence(g,x,y+37,14,3,hs,x,y+32);labFence(g,x+38,y+37,14,3,hs,x+38,y+32);
      labFence(g,x,y+5,3,35,vs,x-1,y+5);labFence(g,x+49,y+5,3,35,vs,x+48,y+5);
      {const hc=mk(pen.iw,pen.ih),hg=hc.getContext('2d');for(let py=0;py<pen.ih;py++)for(let px=0;px<pen.iw;px++){const v=(px*3+py*5+((px*py)%3))%7;hg.fillStyle=v<2?'#d9b45a':v<5?'#e8c872':'#f2da8f';hg.fillRect(px,py,1,1);}for(let k=0;k<pen.iw*pen.ih/14;k++){hg.fillStyle='#b8913a';hg.fillRect(Math.floor(rn()*pen.iw),Math.floor(rn()*pen.ih),2,1);}pen.hay=hc;}
      labBlock(g,pen.ix,pen.iy,pen.iw,pen.ih);
      labPaint(g,x-2,y-2,56,46);
      for(let j=0;j<per;j++){const q=labSpot(g,10,8,0,g.ph,rn,{near:{x:pen.cx,y:pen.cy,r0:g.def.teach?40:55,r1:g.def.teach?80:130},margin:4});if(!q)continue;
        const hz={kind:'sheep',stray:1,horse:false,col:0,flock:-7,x:q.x,y:q.y,w:9,h:6,hx:q.x,hy:q.y,vx:0,vy:0,t:rn()*3,anim:rn()*2};g.hazards.push(hz);S.sheep.push(hz);}}},
  tick(dt,tid,L){const S=G.lab;if(!S.pens)return;if(L.home==null)L.home=0;const pr=footprint(tid,P.x,P.y,P.f);
    for(const hz of S.sheep){if(hz.penned){const pn=hz.pen;hz.hx=pn.ix+pn.iw/2-4;hz.hy=pn.iy+pn.ih/2-3;hz.vx+=(hz.hx-hz.x)*2*dt;hz.vy+=(hz.hy-hz.y)*2*dt;continue;}
      hz.hx=hz.x;hz.hy=hz.y;const dx=hz.x+4.5-P.x,dy=hz.y+3-P.y,d=Math.hypot(dx,dy);
      if(d<64){let fx=dx/(d||1),fy=dy/(d||1);if(!chaserFree(hz,hz.x+fx*6,hz.y+fy*6)){const pn=nearest(S.pens.map(q=>({x:q.cx,y:q.cy})))||{x:G.pw/2};const sx=Math.sign(pn.x-hz.x-4.5)||1;fx=sx;fy=0;if(!chaserFree(hz,hz.x+sx*6,hz.y))fx=-sx;}
        const k=(64-d)/64*60;hz.vx+=fx*k*dt*4;hz.vy+=fy*k*dt*4;}
      if(tid!=='ufo'&&overlap(pr,hz)){hz.vx+=Math.sign(dx||1)*90*dt*6;hz.vy+=Math.sign(dy||1)*70*dt*6;if(!(hz.baa>0)){hz.baa=1.2;addFloat(hz.x+4,hz.y-8,'BAA!','#ffffff',0.6);}}
      for(const pn of S.pens){const gy=hz.y+3<pn.cy?pn.y:pn.y+pn.h;if(Math.abs(hz.x+4.5-pn.cx)<S.lure&&Math.abs(hz.y+3-gy)<S.lure*0.8){hz.vx+=(pn.cx-hz.x-4.5)*5*dt;hz.vy+=(pn.cy-hz.y-3)*5*dt;}
        if(hz.x>=pn.ix&&hz.x+hz.w<=pn.ix+pn.iw&&hz.y>=pn.iy&&hz.y+hz.h<=pn.iy+pn.ih){hz.penned=1;hz.pen=pn;L.home++;labPay(hz.x+4,hz.y-12,1,'BAA! HOME');labTime(hz.x+4,hz.y-3,3);sfx('moo',0,{rate:1.8,vol:0.6});labRing(hz.x+4,hz.y+3,10);hz.heart=1.5;
          if(L.home>=S.sheep.length){labPay(P.x,P.y-38,3,'ALL SHEEP HOME!','#7fe08a');sfx('fanfare');}break;}}}
    for(const hz of S.sheep)if(hz.heart>0)hz.heart-=dt;
    labObj('SHEEP',L.home,S.sheep.length);const loose=S.sheep.filter(h=>!h.penned);
    const vis=loose.filter(h=>h.y>camY-10&&h.y<camY+VIEW_H+10&&Math.hypot(h.x-P.x,h.y-P.y)<120);
    if(vis.length){const pn=nearest(S.pens.map(q=>({x:q.cx,y:q.cy})));L.tgt=pn?{x:pn.x,y:pn.y,col:'#c98d4a'}:null;}else{const h=nearest(loose.map(q=>({x:q.x+4,y:q.y+3})));L.tgt=h?{x:h.x,y:h.y,col:'#ffffff'}:null;}},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,L.tgt.col);},
  ents(ents,top,bot){const S=G.lab;if(!S.pens)return;for(const pn of S.pens){if(pn.y>bot+20||pn.y+pn.h<top-20)continue;
      ents.push({base:-1e9+3,draw:()=>{b.drawImage(pn.hay,pn.ix,pn.iy);const p=Math.floor(tNow*3)%2;for(const [gy,dir] of [[pn.y-3-p,1],[pn.y+pn.h+3+p,-1]])for(let q=0;q<3;q++){R(b,pn.cx-1-q,gy-dir*q,1,1,'rgba(201,141,74,0.9)');R(b,pn.cx+q,gy-dir*q,1,1,'rgba(201,141,74,0.9)');}}});}
    for(const hz of S.sheep)if(hz.heart>0&&hz.y>top&&hz.y<bot)ents.push({base:hz.y+20,draw:()=>{const y=Math.round(hz.y-10-(1.5-hz.heart)*6);R(b,hz.x+2,y,2,1,'#ff4f7a');R(b,hz.x+5,y,2,1,'#ff4f7a');R(b,hz.x+2,y+1,5,1,'#ff4f7a');R(b,hz.x+3,y+2,3,1,'#ff4f7a');R(b,hz.x+4,y+3,1,1,'#ff4f7a');}});}};

// ---------- POWER CUT (theme park): dark park; find the power boxes to light each part back up ----------
MODES.powercut={name:'POWER CUT',sub:'TURN THE LIGHTS BACK ON',rule:'FIND THE POWER BOXES',col:'#ffd23f',
  how:['THE PARK HAS LOST POWER AND IT','IS PITCH DARK. FOLLOW THE ARROW','TO EACH GLOWING POWER BOX AND','DRIVE ONTO IT: THAT PART OF THE','PARK LIGHTS UP. ALL ON: BONUS!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+23),n=g.def.teach?2:3,bands=labBands(g,n);S.boxes=[];
    for(let k=0;k<n;k++){const [y0,y1]=bands[k];const av2=[{x:g.start.x,y:g.start.y,r:k===0?50:90}],p=labSpot(g,16,16,y0,y1,rn,{margin:18,xin:26,avoid:av2})||labSpot(g,16,16,y0,y1,rn,{margin:12,xin:20,avoid:av2});if(p)S.boxes.push({x:p.x+8,y:p.y+8,on:0,litT:0,y0,y1});}
    const oc=mk(g.pw,g.ph),o=oc.getContext('2d');o.fillStyle='rgba(8,12,36,0.86)';o.fillRect(0,0,g.pw,g.ph);g.night=oc;S.n=S.boxes.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.boxes)return;if(L.on==null){L.on=0;for(const bx of S.boxes)if(!labReach(bx.x,bx.y))labMove(bx,8,8);}
    for(const bx of S.boxes){if(bx.on){bx.litT+=dt;continue;}
      if(labTouch(tid,{x:bx.x-7,y:bx.y-7,w:14,h:14})){bx.on=1;bx.litT=0;L.on++;sfx('stomp');sfx('gold');shake=Math.max(shake,0.2);buzz(30);labRing(bx.x,bx.y,20);labBurst(bx.x,bx.y,16,'coin',60);
        addFloat(bx.x,bx.y-30,'POWER ON!','#ffd23f',1.4);labPay(bx.x,bx.y-20,1.2,'');labTime(bx.x,bx.y-10,5);
        if(L.on>=S.n){addFloat(P.x,P.y-48,'THE PARK IS OPEN!','#7fe08a',2);labPay(P.x,P.y-38,3,'ALL LIGHTS ON!','#7fe08a');sfx('fanfare');L.party=3;}}}
    if(L.party>0){L.party-=dt;if(Math.random()<dt*10)labBurst(rnd(20,G.pw-20),camY+rnd(20,VIEW_H*0.6),8,'coin',40);}
    labObj('POWER',L.on,S.n);L.tgt=nearest(S.boxes,q=>!q.on);},
  night(cy){const S=G.lab;if(!NB2)NB2=mk(W,VIEW_H);const x=NB2.getContext('2d');x.globalCompositeOperation='source-over';x.clearRect(0,0,W,VIEW_H);x.drawImage(G.night,0,cy,W,VIEW_H,0,0,W,VIEW_H);
    x.globalCompositeOperation='destination-out';
    for(const bx of S.boxes||[]){if(!bx.on)continue;const k=Math.min(1,bx.litT/1.2);if(k<1){x.fillStyle='rgba(0,0,0,1)';pixCircle(x,bx.x,Math.round(bx.y-cy),Math.round(16+k*280));}
      else for(const [m,a] of [[0,1],[8,0.55],[16,0.3]]){x.fillStyle='rgba(0,0,0,'+a+')';x.fillRect(0,bx.y0-cy-m,W,bx.y1-bx.y0+m*2);}}
    const px=P.x,py=P.y-cy,fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f];for(let k=0;k<9;k++){const d=8+k*10,r=6+k*3.2;x.fillStyle='rgba(0,0,0,'+(0.6-k*0.045).toFixed(2)+')';pixCircle(x,Math.round(px+fv[0]*d),Math.round(py+fv[1]*d),Math.round(r));}
    x.fillStyle='rgba(0,0,0,0.6)';pixCircle(x,Math.round(px),Math.round(py),16);x.globalCompositeOperation='source-over';
    x.fillStyle='rgba(255,240,180,0.08)';for(let k=2;k<9;k+=2){const d=8+k*10,r=6+k*3.2;pixCircle(x,Math.round(px+fv[0]*d),Math.round(py+fv[1]*d),Math.round(r*0.8));}b.drawImage(NB2,0,cy);},
  over(cy){const S=G.lab;for(const bx of S.boxes||[]){if(bx.y<cy-40||bx.y>cy+VIEW_H+40)continue;const x=bx.x,y=bx.y;
    if(!bx.on){const p=0.5+0.5*Math.sin(tNow*5);b.fillStyle='rgba(255,210,63,'+(0.16+0.16*p).toFixed(2)+')';pixCircle(b,x,y,Math.round(13+p*6));b.fillStyle='rgba(255,239,122,0.12)';b.fillRect(x-2,y-60,5,60);
      R(b,x-7,y-7,14,14,K);R(b,x-6,y-6,12,12,'#ffd23f');for(let q=-6;q<6;q+=4)R(b,x+q,y-6,2,12,'#13306b');R(b,x-4,y-4,8,8,K);R(b,x-3,y-3,6,6,'#ffef7a');
      R(b,x,y-3,2,2,'#d8364b');R(b,x-1,y-1,3,1,'#d8364b');R(b,x-1,y,2,2,'#d8364b');if(Math.floor(tNow*3)%2)text(b,'POWER',x,y-17,'#ffd23f',{align:'center'});}
    else{R(b,x-7,y-7,14,14,K);R(b,x-6,y-6,12,12,'#7fe08a');R(b,x-3,y-3,6,6,'#ffffff');}}},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ffd23f');}};

// ---------- SLALOM (ski): flag gates down the run; chain them ----------
MODES.slalom={name:'SLALOM',sub:'CHAIN THE FLAG GATES',rule:'DRIVE BETWEEN THE FLAGS',col:'#ff6a7a',
  how:['FLAG GATES RUN DOWN THE SLOPE.','DRIVE THROUGH THEM ONE AFTER','ANOTHER TO BUILD A CHAIN: EACH','GATE PAYS MORE. MISS ONE OR HIT','A POLE: CHAIN GONE. CLEAN RUN: BONUS!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+31),gap=g.def.teach?54:44,n=Math.max(4,Math.min(12,Math.floor((g.ph-200)/320)));S.gates=[];S.gap=gap;
    const st=g.start.y,top=st<g.ph/2,ys=[];for(let k=0;k<n;k++){const f=(k+0.5)/n;ys.push(Math.round(top?st+90+(g.ph-st-150)*f:st-90-(st-60)*f));}
    const xs=[g.pw*0.3,g.pw*0.5,g.pw*0.7];ys.forEach((y,k)=>{let ok=null;for(const cx0 of [xs[k%3],xs[(k+1)%3],xs[(k+2)%3]])for(const dy of [0,-30,30,-60,60]){if(ok)break;const cx=Math.round(cx0+(rn()-0.5)*12),yy=y+dy;
        if(labRect(g,Math.round(cx-gap/2-4),yy-16,gap+8,22))ok={cx,y:yy};}if(ok)S.gates.push({cx:ok.cx,y:ok.y,st:0,col:k%2?'#3f86d6':'#d8364b',hit:0,t:0});});
    S.n=S.gates.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.gates)return;if(L.py==null){L.py=P.y;L.chain=0;L.pass=0;L.miss=0;}const fp=footprint(tid,P.x,P.y,P.f);
    for(const gt of S.gates){if(gt.st){gt.t+=dt;continue;}const lp={x:gt.cx-S.gap/2-1,y:gt.y-14,w:3,h:15},rp={x:gt.cx+S.gap/2-1,y:gt.y-14,w:3,h:15};
      if(tid!=='ufo'&&(overlap(fp,lp)||overlap(fp,rp))){gt.st=2;gt.hit=overlap(fp,lp)?-1:1;L.miss++;if(L.chain>=2)sfx('cend');L.chain=0;sfx('bump',0,{vol:0.35,rate:1.4});addFloat(gt.cx,gt.y-24,'POLE! CHAIN LOST','#ff9aa8',1);continue;}
      if(L.py!==P.y&&(L.py-gt.y)*(P.y-gt.y)<=0){if(Math.abs(P.x-gt.cx)<S.gap/2-1){gt.st=1;L.pass++;L.chain=Math.min(8,L.chain+1);sfx('combo',0,{rate:0.9+L.chain*0.08});labRing(gt.cx,gt.y-6,S.gap/2);
          labPay(gt.cx,gt.y-24,0.12*L.chain,'GATE X'+L.chain,'#ffef7a');}
        else if(Math.abs(P.x-gt.cx)<80){gt.st=2;L.miss++;if(L.chain>=2)sfx('cend');L.chain=0;addFloat(gt.cx,gt.y-24,'MISSED GATE','#ff9aa8',1);}}}
    L.py=P.y;if(!L.clean&&L.pass>=S.n&&L.miss===0&&S.n){L.clean=1;labPay(P.x,P.y-38,3,'CLEAN RUN!','#7fe08a');sfx('fanfare');}
    labObj('GATES',L.pass,S.n,L.chain>1?'X'+L.chain:'');const nx=S.gates.filter(q=>!q.st).sort((a,c)=>Math.abs(a.y-P.y)-Math.abs(c.y-P.y))[0];L.tgt=nx?{x:nx.cx,y:nx.y}:null;},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ff6a7a');},
  ents(ents,top,bot){const S=G.lab;if(!S.gates)return;for(const gt of S.gates){if(gt.y<top-20||gt.y>bot+20)continue;const fr=Math.floor(tNow*4+gt.cx)%2;
    for(const side of [-1,1]){const sx=Math.round(gt.cx+side*S.gap/2);ents.push({base:gt.y,draw:()=>{const col=gt.st===1?'#7fe08a':gt.st===2?'#9aa4b8':gt.col;
      if(gt.hit===side){const x0=side<0?sx:sx-13;R(b,x0,gt.y-3,14,3,K);R(b,x0+1,gt.y-2,12,1,'#e8eef8');R(b,side<0?sx+9:sx-14,gt.y-6,6,4,K);R(b,side<0?sx+10:sx-13,gt.y-5,4,2,col);}
      else b.drawImage(flagSpr(col,gt.st===1?0:fr),sx-1,gt.y-16);}});}
    if(!gt.st)ents.push({base:-1e9+2,draw:()=>{for(let x=gt.cx-S.gap/2+4;x<gt.cx+S.gap/2-3;x+=4)R(b,x,gt.y-1,2,1,gt.col==='#d8364b'?'rgba(216,54,75,0.5)':'rgba(63,134,214,0.5)');}});}}};

// ---------- AVALANCHE (pass): siren, get into the safe zone before the wave ----------
function avZone(){for(let k=0;k<60;k++){const p=labSpot(G,40,40,Math.max(0,camY+10),Math.min(G.ph,camY+VIEW_H-10),Math.random,{near:{x:P.x,y:P.y,r0:45,r1:105}});if(p)return {x:p.x+20,y:p.y+20,r:19};}
  for(let k=0;k<60;k++){const p=labSpot(G,40,40,0,G.ph,Math.random,{near:{x:P.x,y:P.y,r0:40,r1:160}});if(p)return {x:p.x+20,y:p.y+20,r:19};}return {x:P.x,y:P.y,r:19};}
MODES.avalanche={name:'AVALANCHE',sub:'BEAT THE WAVE TO SAFETY',rule:'GET TO THE SAFE ZONE IN TIME',col:'#ff6a5a',
  how:['NOW AND THEN THE MOUNTAIN LETS','GO. WHEN THE SIREN SOUNDS, DRIVE','INTO THE SAFE ZONE BEFORE THE','WAVE HITS, OR GET BURIED. THE','WAVE DUMPS FRESH SNOW: MORE COINS!'],
  post(g){g.lab.first=g.def.teach?13:9;g.lab.every=g.def.teach?999:20;},
  tick(dt,tid,L){const S=G.lab;let A=L.av;if(!A)A=L.av={ph:'calm',t:S.first,n:0,safe:0,buried:0};
    if(A.buried>0){A.buried-=dt;P.vx=P.vy=0;}
    if(A.ph==='calm'){A.t-=dt;if(A.t<=0&&run.time>9){A.ph='warn';A.t=A.tt=G.def.teach?6:5;A.z=avZone();A.sir=0;addFloat(P.x,P.y-32,'AVALANCHE!','#ff6a5a',1.4);}}
    else if(A.ph==='warn'){A.t-=dt;A.sir-=dt;if(A.sir<=0){A.sir=0.7;sfx('warn',0,{rate:0.8,vol:0.55});}shake=Math.max(shake,0.03+0.07*(1-A.t/A.tt));if(A.t<=0){A.ph='wave';A.wt=0;A.res=0;sfx('squall');sfx('stomp');}}
    else if(A.ph==='wave'){A.wt+=dt;const k=Math.min(1,A.wt/1.3);A.fy=camY-30+(VIEW_H+60)*k;shake=Math.max(shake,0.2);
      for(let q=0;q<6;q++){const x=rnd(4,G.pw-4),y=A.fy-rnd(0,30);if(y>2&&y<G.ph-2)addSnowCircle(G,x,y,rnd(5,10),rnd(0.35,0.6));}
      if(!A.res&&A.fy>=P.y-12){A.res=1;A.n++;if(A.z&&Math.hypot(P.x-A.z.x,P.y-A.z.y)<A.z.r+4){A.safe++;labPay(P.x,P.y-32,1,'SAFE!','#7fe08a');sfx('win');}
        else{A.buried=1.6;P.stun=Math.max(P.stun,1.6);P.inv=Math.max(P.inv,2.2);P.vx=P.vy=0;shake=0.45;buzz(80);sfx('stomp');addFloat(P.x,P.y-32,'BURIED!','#ff6a5a',1.5);if(run.combo>=2){run.combo=0;run.comboProg=0;sfx('cend');}addSnowCircle(G,P.x,P.y,22,0.6);}}
      if(A.wt>=1.3){A.ph='calm';A.t=S.every+rnd(-2,3);A.z=null;}}
    if(A.n)labObj('SAFE',A.safe,A.n);},
  over(cy){const A=run.lab&&run.lab.av;if(!A)return;
    if(A.z&&(A.ph==='warn'||A.ph==='wave')){const z=A.z;b.fillStyle='rgba(127,224,138,0.22)';pixCircle(b,z.x,z.y,z.r);for(let a=0;a<20;a++){const an=a/20*Math.PI*2+tNow*1.5;b.fillStyle=a%2?'#ffd23f':K;b.fillRect(Math.round(z.x+Math.cos(an)*z.r)-1,Math.round(z.y+Math.sin(an)*z.r*0.8)-1,3,2);}
      text(b,'SAFE',z.x,z.y-3,'#ffffff',{align:'center'});if(A.ph==='warn')text(b,''+Math.ceil(A.t),z.x,z.y-z.r-12,'#ff6a5a',{align:'center',scale:2});}
    if(A.ph==='wave'){const y=Math.round(A.fy);R(b,0,y,W,16,'rgba(27,31,59,0.3)');R(b,0,y+16,W,8,'rgba(27,31,59,0.14)');b.fillStyle='#dfe9f7';b.fillRect(0,y-60,W,60);b.fillStyle='#c3d4ec';b.fillRect(0,y-14,W,12);
      for(let x=0;x<W;x+=6){const h=5+((x*13+Math.floor(tNow*24))%8);R(b,x,y-3,6,h+1,K);R(b,x,y-3,6,h,'#eef4fc');R(b,x,y-4+h,6,1,'#9fb4d8');}
      for(let k=0;k<9;k++){const bx=(k*23+Math.floor(tNow*(70+k*9)))%(W+20)-10,by=y-6-((k*17)%34),r=3+(k%4);b.fillStyle=K;pixCircle(b,bx,by,r+1);b.fillStyle='#ffffff';pixCircle(b,bx,by,r);b.fillStyle='#c6d9f3';b.fillRect(bx-r+1,by+r-2,r*2-1,1);}
      for(let k=0;k<5;k++)particles.push({x:rnd(0,W),y:y+rnd(-4,6),vx:rnd(-30,30),vy:rnd(20,60),z:3,vz:rnd(10,40),life:0.5,t:0,kind:'snow'});R(b,0,y-60,W,2,'#9fb4d8');}
    if(A.buried>0){b.fillStyle='#e8f0fa';pixCircle(b,Math.round(P.x),Math.round(P.y+2),17);b.fillStyle='#ffffff';pixCircle(b,Math.round(P.x-4+Math.sin(tNow*30)),Math.round(P.y-3),9);if(Math.floor(tNow*4)%2)text(b,'DIG DIG!',P.x,P.y-24,'#ffffff',{align:'center'});}},
  screen(){const A=run.lab&&run.lab.av;if(!A||A.ph!=='warn')return;if(Math.floor(tNow*6)%2){panel(16,VIEW_Y+20,148,15,'#5c0e1e','#ff6a5a');text(b,'AVALANCHE! GET TO SAFETY',W/2,VIEW_Y+24,'#ffffff',{align:'center',outline:null});}if(A.z)labArrow(A.z.x,A.z.y,'#7fe08a');}};

// ---------- LOST PENGUINS (north): fog; find chicks by their peeps, lead them home in a line ----------
MODES.penguins={name:'LOST PENGUINS',sub:'LEAD THE CHICKS HOME',rule:'FIND CHICKS, LEAD THEM HOME',col:'#9fd8ff',
  how:['PENGUIN CHICKS ARE LOST IN THE','FOG. FOLLOW THEIR PEEPS, DRIVE','UP TO ONE AND IT FOLLOWS YOU.','LEAD THE LINE TO THE NEST: MORE','AT ONCE PAYS MORE. CRASH? THEY RUN.'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+41),n=g.def.teach?3:5;const ne=labSpot(g,30,22,0,g.ph,rn,{near:{x:g.start.x,y:g.start.y,r0:30,r1:80},margin:4});
    S.nest=ne?{x:ne.x+15,y:ne.y+11}:{x:g.start.x,y:clamp(g.start.y+(g.start.y<g.ph/2?50:-50),20,g.ph-20)};const bands=labBands(g,n);S.chicks=[];
    for(let k=0;k<n;k++){const [y0,y1]=bands[k];const p=labSpot(g,10,10,y0,y1,rn,{margin:14,xin:16,avoid:[{x:S.nest.x,y:S.nest.y,r:90}]})||labSpot(g,10,10,y0,y1,rn,{margin:6,avoid:[{x:S.nest.x,y:S.nest.y,r:90}]});if(p)S.chicks.push({x:p.x+5,y:p.y+5,st:'lost',ping:rn()*2.4,pt:9,hop:0,t:0});}
    S.n=S.chicks.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.chicks)return;if(!L.tr){L.tr=[];L.home=0;L.inv0=P.inv;}
    const last=L.tr[L.tr.length-1];if(!last||Math.hypot(P.x-last.x,P.y-last.y)>=2){L.tr.push({x:P.x,y:P.y});if(L.tr.length>600)L.tr.splice(0,L.tr.length-600);}
    if(P.inv>L.inv0+0.3){const f=S.chicks.filter(c=>c.st==='follow');if(f.length){for(const c of f){c.st='lost';c.x=clamp(c.x+rnd(-16,16),6,G.pw-6);c.y=clamp(c.y+rnd(-12,12),6,G.ph-6);c.ping=0;}addFloat(P.x,P.y-32,'PEEP PEEP! THEY SCATTERED','#ff9aa8',1.2);sfx('cend');}}
    L.inv0=P.inv;const hl=(VSPEC[tid]?VSPEC[tid].hh:6)+5;let k=0;
    if(!L.rf){L.rf=1;for(const c of S.chicks)if(!labReach(c.x,c.y))labMove(c,5,5);}
    for(const c of S.chicks){if(c.st==='lost'){c.ping-=dt;c.pt+=dt;if(c.ping<=0){c.ping=2.4;c.pt=0;}
        if(Math.hypot(P.x-c.x,P.y-c.y)<20||labTouch(tid,{x:c.x-5,y:c.y-5,w:10,h:10})){c.st='follow';sfx('gift',0,{rate:1.6});addFloat(c.x,c.y-12,'PEEP!','#ffffff',0.8);labRing(c.x,c.y,8);}}
      else if(c.st==='follow'){const d=hl+(k+1)*11;let acc=0,pt=null;for(let j=L.tr.length-1;j>0;j--){acc+=Math.hypot(L.tr[j].x-L.tr[j-1].x,L.tr[j].y-L.tr[j-1].y);if(acc>=d){pt=L.tr[j-1];break;}}
        if(pt){c.x+=(pt.x-c.x)*Math.min(1,dt*10);c.y+=(pt.y-c.y)*Math.min(1,dt*10);}c.hop+=dt;k++;}
      else if(c.st==='in'){c.t+=dt;if(c.t>0){const q=Math.min(1,c.t/0.4);c.x+=(c.tx-c.x)*q;c.y+=(c.ty-c.y)*q;}}}
    const f=S.chicks.filter(c=>c.st==='follow');
    if(f.length&&Math.hypot(P.x-S.nest.x,P.y-S.nest.y)<30){const n=f.length;f.forEach((c,j)=>{c.st='in';c.t=-j*0.15;c.tx=S.nest.x-8+((L.home+j)%5)*4;c.ty=S.nest.y-2+(((L.home+j)/5)|0)*4;});L.home+=n;
      labPay(S.nest.x,S.nest.y-22,0.8*n*(1+0.25*(n-1)),n>1?n+' CHICKS HOME!':'CHICK HOME!','#9fd8ff');labTime(S.nest.x,S.nest.y-12,2*n);sfx('gift');
      if(L.home>=S.n){labPay(P.x,P.y-42,3,'ALL CHICKS SAFE!','#7fe08a');sfx('fanfare');}}
    labObj('CHICKS',L.home,S.n,f.length?'+'+f.length:'');L.tgt=f.length?{x:S.nest.x,y:S.nest.y,col:'#7fe08a'}:(()=>{const c=nearest(S.chicks,q=>q.st==='lost');return c?{x:c.x,y:c.y,col:'#9fd8ff'}:null;})();},
  ents(ents,top,bot){const S=G.lab;if(!S.chicks)return;const nx=S.nest;
    if(nx.y>top-30&&nx.y<bot+30)ents.push({base:nx.y-6,draw:()=>{b.fillStyle='#c6d9f3';pixCircle(b,nx.x,nx.y,12);b.fillStyle='#e8c872';pixCircle(b,nx.x,nx.y,9);b.fillStyle='#c9a04a';pixCircle(b,nx.x,nx.y+1,6);R(b,nx.x+10,nx.y-22,1,20,K);R(b,nx.x+11,nx.y-22,6,4,'#ff6a7a');}});
    for(const c of S.chicks){if(c.y<top-10||c.y>bot+10)continue;ents.push({base:c.y+3,draw:()=>{const mv=c.st==='follow'?Math.floor(c.hop*8)%2:0;b.drawImage(PENG_FR[mv],Math.round(c.x-4),Math.round(c.y-7-(c.st==='follow'&&mv?1:0)));}});}},
  over(cy){const S=G.lab;if(!S.chicks)return;labFog(cy,G.def.teach?0.86:0.92);
    for(const c of S.chicks){if(c.st!=='lost'||c.pt>0.9||c.y<cy-40||c.y>cy+VIEW_H+40)continue;const r=Math.round(4+c.pt*28),a=(1-c.pt/0.9)*0.9;b.strokeStyle='rgba(63,134,214,'+a.toFixed(2)+')';b.lineWidth=1;b.beginPath();b.arc(c.x,c.y,r,0,Math.PI*2);b.stroke();
      if(c.pt<0.5)text(b,'PEEP',c.x,c.y-r-8,'#3f86d6',{align:'center',outline:null});}
    const nx=S.nest,p=0.5+0.5*Math.sin(tNow*4);b.fillStyle='rgba(255,106,122,'+(0.25+0.25*p).toFixed(2)+')';b.fillRect(nx.x+9,nx.y-60,4,60);text(b,'NEST',nx.x,nx.y-30,'#ff6a7a',{align:'center'});},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,L.tgt.col);}};
function sprAlpha(c){""")
open(f,'w',encoding='utf-8').write(s)
print('p151 lab twists: thin ice, dig-out, round-up, power cut, slalom, avalanche, lost penguins')
