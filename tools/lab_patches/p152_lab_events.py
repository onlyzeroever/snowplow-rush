import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Weekend events rebuilt around one clear verb each: race (Gold Rush, Time Attack), chase (Yeti Hunt), grow and cash in
# (Snowball Roll), drift (Black Ice), power fantasy (Snow Day), smash (Snowball Fight), catch (Star Shower).
rep("onIce=G.type[fi]===T_ICE&&G.depth[fi]<CLEAR_T;","onIce=(G.type[fi]===T_ICE||G.def.mode==='blackice')&&G.depth[fi]<CLEAR_T;")
rep("full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1)*(G.def.deep?deepSlow(tid,dt):1);",
    "full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1)*(G.def.deep?deepSlow(tid,dt):1)*(G.def.mode==='snowday'?1.2:1);")
rep("if(tid==='monster'&&o.crush){crushOb(o);continue;}","if((tid==='monster'||o.fort)&&o.crush){if(o.fort)fortSmash(o);crushOb(o);continue;}")

rep("function sprAlpha(c){",r"""// ================= LAB rev 2: WEEKEND EVENTS =================
const NUG_SPR=spr(["..KKKK..",".KYYYWK.","KYYWYYYK","KYYYYyYK","KYyYYYyK",".KyyyyK.","..KKKK.."],{Y:'#ffd23f',W:'#ffffff',y:'#c98a12'});
function nugSpot(r0,r1){for(let k=0;k<90;k++){const a=Math.random()*Math.PI*2,d=r0+Math.random()*(r1-r0),x=Math.round(P.x+Math.cos(a)*d),y=Math.round(P.y+Math.sin(a)*d*1.3);
  if(x<14||x>G.pw-14||y<14||y>G.ph-14)continue;if(labReach(x,y)&&labRect(G,x-6,y-6,12,12))return {x,y};}return null;}
function timerDots(x,y,r,f,col){const n=16,on=Math.ceil(n*f);for(let a=0;a<n;a++){const an=-Math.PI/2+a/n*Math.PI*2;R(b,Math.round(x+Math.cos(an)*r),Math.round(y+Math.sin(an)*r),1,1,a<on?col:'rgba(27,31,59,0.25)');}}
// ---------- GOLD RUSH: one nugget at a time; get there before its timer; chain them ----------
MODES.goldrush={name:'GOLD RUSH',sub:'RACE TO THE GOLD NUGGETS',rule:'RACE TO EACH GOLD NUGGET',col:'#ffd23f',
  how:['ONE GOLD NUGGET AT A TIME POPS','UP NEAR YOU. REACH IT BEFORE ITS','TIMER RUNS OUT AND THE NEXT ONE','PAYS MORE (UP TO X6). TOO SLOW','AND THE CHAIN RESETS.'],
  tick(dt,tid,L){if(L.found==null){L.found=0;L.chain=0;L.nug=null;L.wait=1.5;}
    if(!L.nug){L.wait-=dt;if(L.wait<=0){const p=nugSpot(70,170)||nugSpot(40,240);if(p){L.nug={x:p.x,y:p.y,t:0,max:6+Math.hypot(p.x-P.x,p.y-P.y)/55};sfx('tick',0,{rate:1.8,vol:0.5});}else L.wait=0.5;}}
    else{const n=L.nug;n.t+=dt;
      if(labTouch(tid,{x:n.x-6,y:n.y-6,w:12,h:12})){L.found++;L.chain=Math.min(6,L.chain+1);labPay(n.x,n.y-14,0.25*L.chain,'GOLD X'+L.chain);sfx('gold');labRing(n.x,n.y,12);labBurst(n.x,n.y,12,'coin',60);L.nug=null;L.wait=0.25;}
      else if(n.t>=n.max){addFloat(n.x,n.y-14,'TOO SLOW!','#ff9aa8',0.9);if(L.chain>=2)sfx('cend');L.chain=0;L.nug=null;L.wait=0.6;}}
    labObj('GOLD',L.found,null,L.chain>1?'X'+L.chain:'');L.tgt=L.nug;},
  ents(ents,top,bot){const L=run.lab;if(!L||!L.nug)return;const n=L.nug;ents.push({base:n.y+4,draw:()=>{const bo=Math.floor(tNow*4)%2,f=1-n.t/n.max;R(b,n.x-4,n.y+3,9,2,'rgba(27,31,59,0.25)');
    b.fillStyle='rgba(255,210,63,0.22)';pixCircle(b,n.x,n.y,Math.round(9+Math.sin(tNow*6)*2));b.drawImage(NUG_SPR,n.x-4,n.y-5-bo);if(Math.floor(tNow*5)%3===0){R(b,n.x+4,n.y-8,1,3,'#ffffff');R(b,n.x+3,n.y-7,3,1,'#ffffff');}
    timerDots(n.x,n.y-1,12,f,f<0.3&&Math.floor(tNow*8)%2?'#ff4a4a':'#ffd23f');}});},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ffd23f');}};
// ---------- YETI HUNT: the yeti runs; corner it and bump it five times ----------
MODES.yetihunt={name:'YETI HUNT',sub:'CATCH THE PRESENT THIEF',rule:'BUMP THE YETI 5 TIMES',col:'#9fd8ff',
  how:['A YETI HAS STOLEN A SACK OF','PRESENTS AND RUNS FROM YOU.','CHASE IT, CORNER IT AND BUMP IT:','EACH BUMP DROPS A PRESENT. FIVE','BUMPS AND IT GIVES UP THE LOT!'],
  tick(dt,tid,L){let Y=L.yeti;if(!Y){if(L.t<1.5)return;const p=nugSpot(90,150)||nugSpot(60,220);if(!p)return;Y=L.yeti={x:p.x-8,y:p.y-4,w:16,h:8,inv:0,hits:0,st:'run',an:0,think:0,dir:null};addFloat(p.x,p.y-26,'THERE IT IS!','#9fd8ff',1.2);sfx('warn',0,{rate:0.7,vol:0.4});}
    Y.an+=dt;if(Y.st==='done')return;if(Y.inv>0)Y.inv-=dt;const cx=Y.x+8,cy=Y.y+4,d=Math.hypot(cx-P.x,cy-P.y),base=moveSpeed()*0.7*(Y.inv>0?1.25:1)*(d<50?1.12:1);
    Y.think-=dt;if(Y.think<=0){Y.think=0.18;let best=null,bs=-1e9;for(let k=0;k<16;k++){const a=k/16*Math.PI*2,ux=Math.cos(a),uy=Math.sin(a);let free=0;for(let st=6;st<=30;st+=6){if(chaserFree(Y,Y.x+ux*st,Y.y+uy*st))free=st;else break;}
        const sc=Math.hypot(cx+ux*free-P.x,cy+uy*free-P.y)+free*0.8+Math.random()*6-(free<6?60:0);if(sc>bs){bs=sc;best={ux,uy};}}Y.dir=best;}
    if(d<170&&Y.dir){const nx=Y.x+Y.dir.ux*base*dt,ny=Y.y+Y.dir.uy*base*dt;if(chaserFree(Y,nx,Y.y))Y.x=nx;if(chaserFree(Y,Y.x,ny))Y.y=ny;Y.mv=1;}else Y.mv=0;
    if(Y.inv<=0&&labTouch(tid,{x:Y.x-2,y:Y.y-8,w:Y.w+4,h:Y.h+10})){Y.hits++;Y.inv=1.4;sfx('stomp');shake=Math.max(shake,0.15);buzz(25);labBurst(cx,cy,10,'snow',60);
      if(Y.hits>=5){Y.st='done';labPay(cx,cy-32,4,'YETI GIVES UP!','#7fe08a');sfx('fanfare');addFloat(cx,cy-22,'OK OK! TAKE THEM!','#ffffff',1.6);}
      else{labPay(cx,cy-24,0.7,'OOF! A PRESENT');addFloat(cx,cy-34,['RAWR!','GRRR!','NOT FAIR!','STOP IT!'][Y.hits%4],'#ffffff',0.9);}}
    labObj('YETI',Y.hits,5);L.tgt=Y.st!=='done'?{x:cx,y:cy}:null;},
  ents(ents,top,bot){const L=run.lab,Y=L&&L.yeti;if(!Y||Y.y<top-30||Y.y>bot+30)return;const C=CHASERS.yeti;ents.push({base:Y.y+Y.h,draw:()=>{if(Y.inv>0&&Math.floor(tNow*12)%2)return;
    R(b,Math.round(Y.x)-1,Math.round(Y.y)+Y.h-2,Y.w+2,2,'rgba(27,31,59,0.25)');const fr=C.frames[Y.mv?Math.floor(Y.an*8)%2:0];b.drawImage(fr,Math.round(Y.x-C.ox),Math.round(Y.y-C.oy));
    if(Y.st!=='done'){for(let k=0;k<Math.max(1,5-Y.hits);k++)b.drawImage(SPR.present,Math.round(Y.x+10+(k%2)*4),Math.round(Y.y-C.oy+2-k*3));}else text(b,'GIVE UP!',Y.x+8,Y.y-C.oy-8,'#ffffff',{align:'center'});}});},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#9fd8ff');}};
// ---------- SNOWBALL ROLL: push a growing snowball; smash it into something to cash in ----------
MODES.snowroll={name:'SNOWBALL ROLL',sub:'GROW A GIANT SNOWBALL',rule:'BIG BALL = BIG SMASH BONUS',col:'#ffffff',
  how:['A SNOWBALL ROLLS IN FRONT OF YOUR','PLOW AND GROWS AS IT PICKS UP','SNOW (IT CLEARS A WIDE PATH TOO).','SMASH IT INTO A WALL TO CASH IN:','THE BIGGER IT IS, THE BIGGER THE PAY.'],
  tick(dt,tid,L){let B=L.ball;if(!B)B=L.ball={r:5,snow:0,x:P.x,y:P.y,roll:0,smash:0,best:5,n:0};
    if(B.smash>0){B.smash-=dt;if(B.smash<=0){B.r=5;B.snow=0;}return;}
    const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],sp=VSPEC[tid],front=(sp?sp.hh+sp.bt:6)+2,tx=P.x+fv[0]*(front+B.r),ty=P.y+fv[1]*(front+B.r);B.roll+=Math.hypot(tx-B.x,ty-B.y);B.x=tx;B.y=ty;
    const acc={got:0,cnt:0,fresh:0},r2=B.r*B.r;for(let cy=Math.max(0,Math.floor((B.y-B.r)/2));cy<=Math.min(G.rows-1,Math.floor((B.y+B.r)/2));cy++)for(let cx=Math.max(0,Math.floor((B.x-B.r)/2));cx<=Math.min(G.cols-1,Math.floor((B.x+B.r)/2));cx++){const ddx=cx*2+1-B.x,ddy=cy*2+1-B.y;if(ddx*ddx+ddy*ddy<=r2)clearCell(cy*G.cols+cx,acc);}
    if(acc.got>0){B.snow+=acc.got;earn(acc.got*BASE_CELL_VALUE*G.def.value*valueMult());}
    B.r=Math.min(26,5+Math.sqrt(B.snow)*0.3);B.best=Math.max(B.best,B.r);
    let hit=B.x-B.r<1||B.x+B.r>G.pw-1||B.y-B.r<1||B.y+B.r>G.ph-1;if(!hit){const bx={x:B.x-B.r*0.8,y:B.y-B.r*0.8,w:B.r*1.6,h:B.r*1.6};for(const o of G.obstacles)if(overlap(bx,o)){hit=true;break;}
      if(!hit)for(const hz of G.hazards)if(typeof hz.x==='number'&&hz.w&&hz.kind!=='skier'&&!(hz.kind==='cross'&&hz.state!=='go')&&overlap(bx,hz)){hit=true;break;}}
    if(hit&&B.r>=7){const u=Math.pow(B.r/5,2)*0.22;B.n++;labPay(B.x,B.y-B.r-8,u,B.r>=22?'MEGA SMASH!':B.r>=14?'BIG SMASH!':'SMASH!');labBurst(B.x,B.y,Math.round(10+B.r*1.5),'snow',40+B.r*3);labRing(B.x,B.y,B.r+6);
      shake=Math.max(shake,0.1+B.r/80);sfx('crunch');if(B.r>=14){sfx('stomp');buzz(30);}addSnowCircle(G,B.x,B.y,B.r*0.8,0.4);B.smash=0.6;}
    else if(hit){B.r=5;B.snow=0;}
    labObj('BALL',Math.round(B.r),26,B.r>=10?'X'+(Math.pow(B.r/5,2)).toFixed(1):'');},
  ents(ents,top,bot){const L=run.lab,B=L&&L.ball;if(!B||B.smash>0)return;ents.push({base:B.y+B.r,draw:()=>{const x=Math.round(B.x),y=Math.round(B.y),r=Math.round(B.r);
    b.fillStyle='rgba(27,31,59,0.22)';b.fillRect(x-r,y+r-1,r*2,3);b.fillStyle=K;pixCircle(b,x,y,r+1);b.fillStyle='#c6d9f3';pixCircle(b,x,y,r);b.fillStyle='#f4f8ff';pixCircle(b,x-Math.round(r*0.15),y-Math.round(r*0.15),Math.round(r*0.85));
    b.fillStyle='#ffffff';pixCircle(b,x-Math.round(r*0.35),y-Math.round(r*0.4),Math.max(1,Math.round(r*0.3)));
    for(let k=0;k<5;k++){const an=B.roll/Math.max(4,r)+k*1.26,dx=Math.cos(an)*r*0.6,dy=Math.sin(an)*r*0.6;R(b,Math.round(x+dx),Math.round(y+dy*0.8),2,1,'#9fb4d8');}
    if(r>=24&&Math.floor(tNow*6)%2)text(b,'MAX!',x,y-r-10,'#ffd23f',{align:'center'});}});}};
// ---------- BLACK ICE: everything you clear is slippery; drift for coins ----------
MODES.blackice={name:'BLACK ICE',sub:'SLIDE, DRIFT, SCORE',rule:'DRIFT ON THE ICE FOR COINS',col:'#7ad3ff',
  how:['EVERYTHING YOU CLEAR TURNS TO','BLACK ICE AND YOU SLIDE. TURN','WHILE YOU SLIDE TO DRIFT: THE','LONGER THE DRIFT, THE BIGGER THE','PAYOUT. CRASH AND YOU LOSE IT.'],
  post(g){for(let k=0;k<g.ground.length;k+=3){g.ground[k]=g.ground[k]*0.45+190*0.55;g.ground[k+1]=g.ground[k+1]*0.45+224*0.55;g.ground[k+2]=g.ground[k+2]*0.45+252*0.55;}labPaint(g,0,0,g.pw,g.ph);},
  tick(dt,tid,L){if(L.dr==null){L.dr=0;L.best=0;L.off=0;L.inv0=P.inv;L.sc=0;}const sp=Math.hypot(P.vx,P.vy),fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],cos=sp>1?(P.vx*fv[0]+P.vy*fv[1])/sp:1;
    const fi=(clamp(Math.floor(P.y/2),0,G.rows-1))*G.cols+clamp(Math.floor(P.x/2),0,G.cols-1),ice=G.depth[fi]<CLEAR_T,drifting=ice&&sp>moveSpeed()*0.4&&cos<0.85&&!(P.stun>0);
    if(P.inv>L.inv0+0.3&&L.dr>0.3){addFloat(P.x,P.y-30,'WIPEOUT!','#ff9aa8',0.9);L.dr=0;}L.inv0=P.inv;
    if(drifting){const before=L.dr;L.dr+=dt*sp/40;L.off=0;if(Math.random()<dt*24){const bx=P.x-fv[0]*10,by=P.y-fv[1]*10;particles.push({x:bx+rnd(-6,6),y:by+rnd(-4,4),vx:-P.vx*0.3+rnd(-20,20),vy:-P.vy*0.3+rnd(-20,20),z:1,vz:rnd(5,20),life:0.4,t:0,kind:'snow'});}
      if(Math.floor(L.dr*3)!==Math.floor(before*3))sfx('scrape',0,{vol:0.22,rate:1.3+Math.min(0.6,L.dr*0.1)});}
    else if(L.dr>0){L.off+=dt;if(L.off>0.25){if(L.dr>=0.6){const u=Math.min(3,0.25*L.dr*L.dr+0.3*L.dr);labPay(P.x,P.y-26,u,L.dr>=3?'MEGA DRIFT!':L.dr>=1.6?'GREAT DRIFT!':'DRIFT!','#7ad3ff');L.best=Math.max(L.best,L.dr);L.sc++;}L.dr=0;}}
    labObj('DRIFTS',L.sc,null,L.dr>0.3?'+'+Math.round(L.dr*10):'');},
  over(cy){const L=run.lab;if(L&&L.dr>0.6){const k=Math.min(1,L.dr/3);text(b,'DRIFT '+Math.round(L.dr*10),P.x,P.y-30-Math.round(k*4),k>0.9?'#ffd23f':'#7ad3ff',{align:'center',scale:k>0.5?2:1});}}};
// ---------- SNOW DAY: mega blade, faster plow, three times the snow ----------
MODES.snowday={name:'SNOW DAY',sub:'MEGA BLADE, MOUNTAINS OF SNOW',rule:'MEGA BLADE! PLOW IT ALL',col:'#e8f0ff',
  how:['A MEGA BLADE AND A FASTER PLOW,','BUT THE SNOW COMES DOWN TWO AND A','HALF TIMES AS FAST. JUST PLOW.','COINS X1.5.'],
  tick(dt,tid,L){const g2=run.lastGot||0;if(g2>2.5){if(Math.random()<0.5){const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f];labBurst(P.x+fv[0]*22+rnd(-12,12),P.y+fv[1]*22+rnd(-6,6),3,'snow',80);}shake=Math.max(shake,Math.min(0.06,g2/150));}
    L.big=(L.big||0)+(g2>4?dt:-dt);if(L.big>1.4){L.big=0;addFloat(P.x,P.y-28,['MEGA PLOW!','SNOWNADO!','UNSTOPPABLE!'][Math.floor(Math.random()*3)],'#ffffff',0.9);sfx('whoosh',0,{vol:0.4});}else if(L.big<0)L.big=0;}};
// ---------- TIME ATTACK: half time, triple coins; a clock always waits ahead ----------
MODES.timeattack={name:'TIME ATTACK',sub:'HALF TIME, CHASE THE CLOCKS',rule:'GRAB CLOCKS FOR MORE TIME',col:'#7fe08a',
  how:['HALF THE TIME, TRIPLE THE COINS.','A CLOCK ALWAYS WAITS SOMEWHERE','NEAR YOU: GRAB IT FOR +5 SECONDS','AND THE NEXT ONE APPEARS.'],
  tick(dt,tid,L){if(L.got==null){L.got=0;L.ck=null;L.w=1;}if(!L.ck){L.w-=dt;if(L.w<=0){const p=nugSpot(80,170)||nugSpot(40,240);if(p)L.ck={x:p.x,y:p.y};else L.w=0.5;}}
    else if(labTouch(tid,{x:L.ck.x-6,y:L.ck.y-6,w:12,h:12})){L.got++;labTime(L.ck.x,L.ck.y-12,5);labRing(L.ck.x,L.ck.y,12);L.ck=null;L.w=0.4;}
    labObj('CLOCKS',L.got,null);L.tgt=L.ck;},
  ents(ents,top,bot){const L=run.lab,c=L&&L.ck;if(!c)return;ents.push({base:c.y+4,draw:()=>{const bo=Math.floor(tNow*3+c.x)%2;R(b,c.x-4,c.y+3,9,2,'rgba(27,31,59,0.22)');b.fillStyle='rgba(127,224,138,0.25)';pixCircle(b,c.x,c.y,Math.round(9+Math.sin(tNow*6)*2));b.drawImage(SPR.watch,c.x-4,c.y-6-bo);}});},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#7fe08a');}};
// ---------- SNOWBALL FIGHT: kids behind snow forts; ram the forts ----------
function fortSpr(){const c=mk(30,16),g=c.getContext('2d');R(g,0,5,30,11,K);R(g,1,6,28,9,'#e8f0fa');for(let x=0;x<30;x+=8){R(g,x,1,6,5,K);R(g,x+1,2,4,4,'#f4f8ff');}
  for(let x=1;x<29;x+=7)R(g,x,9,6,1,'#b8cbe6');R(g,4,12,6,1,'#b8cbe6');R(g,16,12,7,1,'#b8cbe6');R(g,1,14,28,1,'#9fb4d8');R(g,2,6,26,1,'#ffffff');return c;}
function fortSmash(o){const S=G.lab;S.smashed=(S.smashed||0)+1;const cx=o.x+o.w/2,cy=o.y+o.h/2;labBurst(cx,cy,30,'snow',90);labRing(cx,cy,18);shake=Math.max(shake,0.25);buzz(40);sfx('crunch');sfx('stomp');
  labPay(cx,cy-18,1,'KAPOW!');if(o.kid){o.kid.state='buried';o.kid.t=30;addFloat(o.kid.sx,o.kid.sy-16,'WAAAH!','#ffffff',1);}
  if(S.smashed>=S.n){labPay(P.x,P.y-38,3,'ALL FORTS DOWN!','#7fe08a');sfx('fanfare');}}
MODES.forts={name:'SNOWBALL FIGHT',sub:'SMASH THE SNOW FORTS',rule:'RAM THE SNOW FORTS',col:'#ff8fb0',
  how:['KIDS HAVE BUILT SNOW FORTS AND','PELT YOU FROM BEHIND THEM. RAM A','FORT TO SMASH IT AND SNOW IN THE','KID. SMASH THEM ALL FOR A BONUS.','COINS X1.5.'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+53),n=Math.max(3,Math.min(7,Math.round(g.ph/400))),bands=labBands(g,n);S.forts=[];S.smashed=0;
    for(let k=0;k<n;k++){const [y0,y1]=bands[k];const p=labSpot(g,30,26,y0,y1,rn,{margin:12,xin:14,avoid:[{x:g.start.x,y:g.start.y,r:70}]});if(!p)continue;
      const sp2=fortSpr(),o={spr:sp2,src:sp2,sx:p.x,sy:p.y+8,x:p.x+1,y:p.y+14,w:28,h:8,bld:false,crush:1,fort:1,lab:1};o.base=o.y+o.h;g.obstacles.push(o);labBlock(g,o.x,o.y,o.w,o.h);
      const kid={kind:'thrower',x:p.x+11,y:p.y+4,w:8,h:5,sx:p.x+15,sy:p.y+9,state:'idle',cd:rn()*2+1,ball:null,t:0,fortKid:1};g.hazards.push(kid);o.kid=kid;S.forts.push(o);}
    S.n=S.forts.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.forts)return;labObj('FORTS',S.smashed||0,S.n);const nx=nearest(S.forts.filter(o=>G.obstacles.includes(o)).map(o=>({x:o.x+14,y:o.y+4})));L.tgt=nx;},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ff8fb0');}};
// ---------- STAR SHOWER: a shower of six stars every few seconds; catch the set ----------
MODES.stars={name:'STAR SHOWER',sub:'CATCH THE FALLING STARS',rule:'CATCH ALL SIX STARS',col:'#ffef7a',
  how:['EVERY FEW SECONDS A SHOWER OF SIX','STARS LANDS NEAR YOU. EACH STAR','YOU CATCH IN A SHOWER PAYS MORE.','CATCH ALL SIX FOR A GEM (UP TO 5','A JOB). THEY FADE FAST!'],
  tick(dt,tid,L){if(L.caught==null){L.caught=0;L.t2=3;L.st=[];L.gem=0;L.k=0;}
    L.t2-=dt;if(L.t2<=0&&!L.st.length){L.t2=9;L.k=0;const c=nugSpot(60,110)||{x:P.x,y:P.y-60};for(let q=0;q<6;q++)for(let tries=0;tries<30;tries++){const x=Math.round(c.x+rnd(-36,36)),y=Math.round(c.y+rnd(-30,30));
        if(x>8&&x<G.pw-8&&y>8&&y<G.ph-8&&labReach(x,y)&&!L.st.some(q2=>Math.hypot(q2.x-x,q2.y-y)<12)){L.st.push({x,y,t:-q*0.12});break;}}addFloat(c.x,c.y-34,'STAR SHOWER!','#ffef7a',1.2);sfx('whoosh',0,{rate:1.4});}
    for(const s2 of L.st){s2.t+=dt;if(s2.t>=1&&!s2.land){s2.land=1;labRing(s2.x,s2.y,8);sfx('tick',0,{rate:1.6,vol:0.4});}
      if(s2.land&&!s2.got&&labTouch(tid,{x:s2.x-5,y:s2.y-5,w:10,h:10})){s2.got=1;L.k++;L.caught++;labPay(s2.x,s2.y-12,0.12*L.k,'STAR X'+L.k,'#ffef7a');sfx('gift',0,{rate:1+L.k*0.1});
        if(L.k===6){if(L.gem<5){L.gem++;save.gems=(save.gems||0)+1;addFloat(P.x,P.y-38,'PERFECT! +1 GEM','#ff8fc8',1.4);}else labPay(P.x,P.y-38,1,'PERFECT!','#ff8fc8');sfx('fanfare');}}}
    L.st=L.st.filter(s2=>!s2.got&&s2.t<5.5);labObj('STARS',L.caught,null,L.st.length?L.k+'/6':'');L.tgt=nearest(L.st,q=>q.land);},
  ents(ents,top,bot){const L=run.lab;if(!L||!L.st)return;for(const s2 of L.st){if(s2.y<top-120||s2.y>bot+20)continue;ents.push({base:s2.y+4,draw:()=>{
    if(!s2.land){if(s2.t<0)return;const k=s2.t,sx=Math.round(s2.x+(1-k)*40),sy=Math.round(s2.y-(1-k)*110);b.fillStyle='rgba(255,239,122,'+(0.15+0.3*k).toFixed(2)+')';pixCircle(b,s2.x,s2.y,Math.round(3+5*k));
      for(let q=1;q<6;q++)R(b,sx+q*3,sy-q*7,2,2,'rgba(255,239,122,'+(0.6-q*0.1).toFixed(2)+')');b.drawImage(SPR.bigStar,sx-4,sy-4);}
    else if(!(s2.t>4.3&&Math.floor(tNow*10)%2)){const bo=Math.floor(tNow*4+s2.x)%2;R(b,s2.x-4,s2.y+4,9,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.bigStar,s2.x-4,s2.y-6-bo);}}});}},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ffef7a');}};
function sprAlpha(c){""")
open(f,'w',encoding='utf-8').write(s)
print('p152 lab events: gold rush, yeti hunt, snowball roll, black ice, snow day, time attack, snowball fight, star shower')
