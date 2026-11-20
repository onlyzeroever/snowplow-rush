# LAB rev 3 events (Alex, Nov 20 22:58): "always think, how would the pros do it?"
#  - Present Hunt: no more 4x presents (each one could add +4s, so it was overpowered). Normal presents, plus 5
#    golden presents buried under the snow: a jingle that speeds up as you get close (hot/cold), a twinkle up close.
#  - Gold Rush: a x6 chain brings a MOTHER LODE nugget (gold gift the first time).
#  - Yeti Hunt: he flees with a safety map (runs for open space, not corners), moves smoothly, stays below the top
#    edge, leaps clear after each bump (no pinning him), drops a present per bump; at 5 bumps his sack bursts
#    (presents to scoop up), he gives up, runs off, and comes back faster for another round.
#  - Snowball Roll: the ball is its own rolling object (push it, it keeps rolling, grows on fresh snow);
#    a hard hit into something smashes it for the pay-out, a soft knock breaks chunks off.
#  - Black Ice: drift sparks blue > orange > purple; let go for coins + a mini-turbo; back-to-back drifts chain.
#  - Snow Day: no constant shake; plowing fills a meter, then 8s of mega blade, faster plow and double coins.
#  - Time Attack: checkpoint run: short clock with tenths, every checkpoint adds time and shows your split against
#    your best, ticking under 10s, finish bonus for the time left.
#  - Snowball throwers (lab): aim ahead of you with some misses (you see the landing marker and can dodge);
#    a hit splats the screen and slows you; bat a snowball back with your blade and it buries the kid.
#  - Star Shower: stars land in a line / arc / zigzag ahead of you (sweep them in one go); every third shower a
#    shooting star runs from you.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---- event definitions (lab copies) ----
rep("presents:{name:'PRESENT HUNT',sub:'PRESENTS EVERYWHERE',mod:{presents:4}","presents:{name:'PRESENT HUNT',sub:'DIG UP THE GOLDEN PRESENTS',mod:{mode:'presenthunt'}")
rep("timeattack:{name:'TIME ATTACK',sub:'HALF TIME, CHASE THE CLOCKS',mod:{mode:'timeattack',value:3,half:1}","timeattack:{name:'TIME ATTACK',sub:'CHECKPOINT TO CHECKPOINT',mod:{mode:'timeattack',value:2}")
rep("snowday:{name:'SNOW DAY',sub:'MEGA BLADE, MOUNTAINS OF SNOW',mod:{mode:'snowday',snow:2.5,value:1.5}","snowday:{name:'SNOW DAY',sub:'FILL THE METER, GO MEGA',mod:{mode:'snowday',snow:2,value:1.5}")
# arrows that are the point of the mode (race to the nugget, the next checkpoint) always show
rep("function labHintOn(){const L=run.lab;if(!L)return false;return !!L.urgent||L.t<3||L.hintT>0;}",
    "function labHintOn(){const L=run.lab;if(!L)return false;const M=labM();return !!(M&&M.arrows)||!!L.urgent||L.t<3||L.hintT>0;}")

# ---- engine hooks: mini-turbo, splat slow-down, Snow Day mega only while it lasts ----
rep("if(run.gold>0)run.gold-=dt;","if(run.gold>0)run.gold-=dt;if(run.turbo>0)run.turbo-=dt;if(run.splat>0)run.splat-=dt;")
rep("*(G.def.mode==='snowday'?1.2:1);","*(G.def.mode==='snowday'&&run.lab&&run.lab.mega>0?1.25:1)*(run.turbo>0?1+0.45*Math.min(1,run.turbo/0.3):1)*(run.splat>0?0.65:1);")
rep("if(state==='play'&&G&&G.def&&G.def.mode==='snowday')c=Math.round(c*1.7);","if(state==='play'&&G&&G.def&&G.def.mode==='snowday'&&run&&run.lab&&run.lab.mega>0)c=Math.round(c*1.7);")
rep("if(run.boost&&!run.ended)text(b,'BOOST',4,VIEW_Y+VIEW_H-10,'#9fd8ff');","drawSplat();if(run.boost&&!run.ended)text(b,'BOOST',4,VIEW_Y+VIEW_H-10,'#9fd8ff');")

# ---- snowball throwers: lead the target (with misses), splat, deflect ----
rep("if(hz.cd<=0&&Math.hypot(P.x-hz.sx,P.y-hz.sy)<100){hz.state='wind';if(hz.revenge){hz.t=0.45;hz.tx=clamp(P.x+P.vx*0.9,4,G.pw-4);hz.ty=clamp(P.y-2+P.vy*0.9,4,G.ph-4);}else{hz.t=0.7;hz.tx=P.x;hz.ty=P.y-2;}}",
    "if(hz.cd<=0&&Math.hypot(P.x-hz.sx,P.y-hz.sy)<(hz.fortKid?130:100)){hz.state='wind';hz.t=hz.revenge?0.45:0.7;const T=hz.t+(hz.revenge?0.45:0.55),good=Math.random()<(hz.revenge?0.9:hz.fortKid?0.72:0.6),ld=good?rnd(0.85,1.05):rnd(0.15,0.55);"
    "let ax=P.x+P.vx*T*ld,ay=P.y-2+P.vy*T*ld;if(good){ax+=rnd(-3,3);ay+=rnd(-3,3);}else{const a=Math.random()*Math.PI*2,r=rnd(10,22);ax+=Math.cos(a)*r;ay+=Math.sin(a)*r;}hz.tx=clamp(ax,4,G.pw-4);hz.ty=clamp(ay,4,G.ph-4);}")
rep("else if(hz.state==='wind'){hz.t-=dt;if(hz.t<=0){hz.state='cool';hz.cd=rnd(2.5,4);",
    "else if(hz.state==='wind'){hz.t-=dt;if(hz.t<=0){hz.state='cool';hz.cd=hz.fortKid?rnd(1.5,2.4)*Math.max(0.6,1-0.08*((G.lab&&G.lab.smashed)||0)):rnd(2.5,4);")
rep("if(hz.ball){const b=hz.ball;b.t+=dt;if(b.t>=b.dur){if(overlap(pr,{x:b.x1-6,y:b.y1-5,w:12,h:10}))hit('hz',SPILL_HAZARD);",
    "if(hz.ball){const b=hz.ball;b.t+=dt;if(!b.back&&b.t<b.dur&&b.t/b.dur>0.78&&tid!=='ufo'&&!isKidTool(tid)){const k2=b.t/b.dur,gx=b.x0+(b.x1-b.x0)*k2,gy=b.y0+(b.y1-b.y0)*k2;"
    "if(overlap(bladeRect(tid,P.x,P.y,P.f,bladeCells()*2),{x:gx-4,y:gy-4,w:8,h:8})){b.back=1;b.x0=gx;b.y0=gy;b.x1=hz.sx;b.y1=hz.sy-4;b.t=0;b.dur=0.35;sfx('bump',0,{rate:1.7,vol:0.6});addFloat(gx,gy-12,'DEFLECT!','#9fd8ff',0.8);buzz(15);}}\n"
    "        if(b.back&&b.t>=b.dur){hz.ball=null;if(hz.state!=='buried'){hz.state='buried';hz.t=4.5;const bonus=Math.max(1,Math.round(labUnit()*0.8));earn(bonus);addFloat(hz.sx,hz.sy-20,'RETURN TO SENDER!'+cplus(bonus),'#ffd23f',1.3);sfx('flump');sfx('combo',0,{rate:1.3});shake=Math.max(shake,0.12);"
    "for(let k=0;k<10;k++)particles.push({x:hz.sx,y:hz.sy-4,vx:rnd(-40,40),vy:rnd(-30,10),z:3,vz:rnd(20,50),life:0.5,t:0,kind:'snow'});if(G.lab)G.lab.returns=(G.lab.returns||0)+1;}continue;}\n"
    "        if(b.t>=b.dur){if(overlap(pr,{x:b.x1-6,y:b.y1-5,w:12,h:10})){const was=P.inv;hit('hz',SPILL_HAZARD);if(!(was>0)){run.splat=1.4;splatFx();addFloat(P.x,P.y-24,'SPLAT!','#ffffff',0.9);}}")

# ---- Gold Rush: mother lode ----
rep("if(p){L.nug={x:p.x,y:p.y,t:0,max:6+Math.hypot(p.x-P.x,p.y-P.y)/55};sfx('tick',0,{rate:1.8,vol:0.5});}",
    "if(p){const big=!!L.lode;L.lode=0;L.nug={x:p.x,y:p.y,t:0,max:(big?9:6)+Math.hypot(p.x-P.x,p.y-P.y)/55,big};sfx('tick',0,{rate:1.8,vol:0.5});if(big){addFloat(p.x,p.y-28,'MOTHER LODE!','#ffd23f',1.5);sfx('warn',0,{rate:1.5,vol:0.4});}}")
rep("if(labTouch(tid,{x:n.x-6,y:n.y-6,w:12,h:12})){L.found++;L.chain=Math.min(6,L.chain+1);labPay(n.x,n.y-14,0.25*L.chain,'GOLD X'+L.chain);sfx('gold');labRing(n.x,n.y,12);labBurst(n.x,n.y,12,'coin',60);L.nug=null;L.wait=0.25;}",
    "const hb=n.big?9:6;if(labTouch(tid,{x:n.x-hb,y:n.y-hb,w:hb*2,h:hb*2})){L.found++;if(n.big){L.lodes=(L.lodes||0)+1;labPay(n.x,n.y-14,3,'MOTHER LODE!');labBurst(n.x,n.y,30,'coin',95);labRing(n.x,n.y,24);shake=Math.max(shake,0.2);buzz(30);if(L.lodes===1)labGoldGift(P.x,P.y-44,'STRUCK IT RICH!');else sfx('fanfare');L.chain=0;}"
    "else{L.chain=Math.min(6,L.chain+1);labPay(n.x,n.y-14,0.25*L.chain,'GOLD X'+L.chain);sfx('gold',0,{rate:0.9+L.chain*0.08});labRing(n.x,n.y,12);labBurst(n.x,n.y,12,'coin',60);if(L.chain>=6)L.lode=1;}L.nug=null;L.wait=0.25;}")
rep("b.fillStyle='rgba(255,210,63,0.22)';pixCircle(b,n.x,n.y,Math.round(9+Math.sin(tNow*6)*2));b.drawImage(NUG_SPR,n.x-4,n.y-5-bo);",
    "b.fillStyle='rgba(255,210,63,0.22)';pixCircle(b,n.x,n.y,Math.round((n.big?15:9)+Math.sin(tNow*6)*2));if(n.big)b.drawImage(NUG_SPR,n.x-8,n.y-10-bo,16,14);else b.drawImage(NUG_SPR,n.x-4,n.y-5-bo);")
rep("MODES.goldrush={name:'GOLD RUSH',sub:'RACE TO THE GOLD NUGGETS',rule:'RACE TO EACH GOLD NUGGET',col:'#ffd23f',",
    "MODES.goldrush={name:'GOLD RUSH',sub:'RACE TO THE GOLD NUGGETS',rule:'RACE TO EACH GOLD NUGGET',bonus:'X6 CHAIN = MOTHER LODE: GOLD GIFT',arrows:1,col:'#ffd23f',")
rep("how:['ONE GOLD NUGGET AT A TIME POPS','UP NEAR YOU. REACH IT BEFORE ITS','TIMER RUNS OUT AND THE NEXT ONE','PAYS MORE (UP TO X6). TOO SLOW','AND THE CHAIN RESETS.'],",
    "how:['ONE GOLD NUGGET AT A TIME POPS','UP NEAR YOU. REACH IT BEFORE ITS','TIMER RUNS OUT AND THE NEXT ONE','PAYS MORE. REACH X6 AND A MOTHER','LODE APPEARS. TOO SLOW: CHAIN GONE.'],")

# ---- Black Ice: spark tiers, mini-turbo, chains ----
rep("if(drifting){const before=L.dr;L.dr+=dt*sp/40;L.off=0;if(Math.random()<dt*24){",
    "if(drifting){const before=L.dr;L.dr+=dt*sp/40;L.off=0;const tier=L.dr>=3?3:L.dr>=1.6?2:L.dr>=0.6?1:0;if(tier>(L.tier||0)){L.tier=tier;sfx('combo',0,{rate:0.9+tier*0.25,vol:0.5});addFloat(P.x,P.y-36,['','BLUE SPARKS','ORANGE SPARKS','PURPLE SPARKS!'][tier],DRIFTC[tier],0.7);}"
    "if(tier&&Math.random()<dt*30){const rx=P.x-fv[0]*10,ry=P.y-fv[1]*10;particles.push({x:rx+rnd(-5,5),y:ry+rnd(-3,3),vx:rnd(-30,30)-fv[0]*20,vy:rnd(-30,30)-fv[1]*20,z:2,vz:rnd(10,30),life:0.3,t:0,kind:'conf',c:DRIFTC[tier]});}if(Math.random()<dt*24){")
rep("else if(L.dr>0){L.off+=dt;if(L.off>0.25){if(L.dr>=0.6){const u=Math.min(3,0.25*L.dr*L.dr+0.3*L.dr);labPay(P.x,P.y-26,u,L.dr>=3?'MEGA DRIFT!':L.dr>=1.6?'GREAT DRIFT!':'DRIFT!','#7ad3ff');L.best=Math.max(L.best,L.dr);L.sc++;}L.dr=0;}}",
    "else if(L.dr>0){L.off+=dt;if(L.off>0.25){if(L.dr>=0.6){const tier=L.dr>=3?3:L.dr>=1.6?2:1;L.ch=(L.t-(L.lastEnd||-9)<2.2)?Math.min(5,(L.ch||1)+1):1;L.lastEnd=L.t;const mult=1+0.25*(L.ch-1),u=Math.min(3,0.25*L.dr*L.dr+0.3*L.dr)*mult;"
    "labPay(P.x,P.y-26,u,(L.ch>1?'X'+L.ch+' ':'')+(tier===3?'MEGA DRIFT!':tier===2?'GREAT DRIFT!':'DRIFT!'),DRIFTC[tier]);run.turbo=[0,0.5,0.9,1.3][tier];addFloat(P.x,P.y-16,'MINI-TURBO!','#ffffff',0.7);sfx('whoosh',0,{rate:1.2+tier*0.1,vol:0.5});"
    "for(let k=0;k<10+tier*6;k++)particles.push({x:P.x-fv[0]*10,y:P.y-fv[1]*10,vx:-fv[0]*rnd(40,90)+rnd(-20,20),vy:-fv[1]*rnd(40,90)+rnd(-20,20),z:2,vz:rnd(10,30),life:0.35,t:0,kind:'conf',c:DRIFTC[tier]});"
    "L.best=Math.max(L.best,L.dr);L.sc++;if(tier===3){L.purp=(L.purp||0)+1;if(L.purp>=3)labGoldGift(P.x,P.y-40,'DRIFT KING!');}}L.dr=0;L.tier=0;}}")
rep("if(P.inv>L.inv0+0.3&&L.dr>0.3){addFloat(P.x,P.y-30,'WIPEOUT!','#ff9aa8',0.9);L.dr=0;}",
    "if(P.inv>L.inv0+0.3&&L.dr>0.3){addFloat(P.x,P.y-30,'WIPEOUT!','#ff9aa8',0.9);L.dr=0;L.tier=0;L.ch=0;}")
rep("labObj('DRIFTS',L.sc,null,L.dr>0.3?'+'+Math.round(L.dr*10):'');},",
    "labObj('PURPLE',L.purp||0,3,L.ch>1&&L.t-L.lastEnd<2.2?'CHAIN X'+L.ch:'');},")
rep("over(cy){const L=run.lab;if(L&&L.dr>0.6){const k=Math.min(1,L.dr/3);text(b,'DRIFT '+Math.round(L.dr*10),P.x,P.y-30-Math.round(k*4),k>0.9?'#ffd23f':'#7ad3ff',{align:'center',scale:k>0.5?2:1});}}};",
    "over(cy){const L=run.lab;if(L&&L.dr>0.6){const tier=L.dr>=3?3:L.dr>=1.6?2:1,mult=1+0.25*(((L.t-(L.lastEnd||-9)<2.2)?Math.min(5,(L.ch||1)+1):1)-1),c=Math.round(labUnit()*Math.min(3,0.25*L.dr*L.dr+0.3*L.dr)*mult);"
    "text(b,'+'+fmt(c),P.x,P.y-32-tier*2,DRIFTC[tier],{align:'center',scale:tier>=2?2:1});const w=24,f2=tier===3?1:tier===2?(L.dr-1.6)/1.4:(L.dr-0.6)/1;R(b,P.x-w/2-1,P.y-24,w+2,4,K);R(b,P.x-w/2,P.y-23,Math.round(w*Math.max(0,Math.min(1,f2))),2,DRIFTC[tier]);}}};")
rep("MODES.blackice={name:'BLACK ICE',sub:'SLIDE, DRIFT, SCORE',rule:'DRIFT ON THE ICE FOR COINS',col:'#7ad3ff',",
    "MODES.blackice={name:'BLACK ICE',sub:'SLIDE, DRIFT, SCORE',rule:'LONGER DRIFT = MORE COINS + TURBO',bonus:'3 PURPLE DRIFTS: GOLD GIFT',col:'#7ad3ff',")
rep("how:['EVERYTHING YOU CLEAR TURNS TO','BLACK ICE AND YOU SLIDE. TURN','WHILE YOU SLIDE TO DRIFT: THE','LONGER THE DRIFT, THE BIGGER THE','PAYOUT. CRASH AND YOU LOSE IT.'],",
    "how:['WHAT YOU CLEAR IS BLACK ICE.','TURN WHILE YOU SLIDE TO DRIFT:','SPARKS GO BLUE, ORANGE, PURPLE.','LET GO FOR COINS AND A TURBO.','DRIFT AGAIN FAST TO CHAIN. CRASH: LOST.'],")

# ---- Snow Day: meter -> mega blade bursts (no constant shake) ----
rep("tick(dt,tid,L){const g2=run.lastGot||0;if(g2>2.5){if(Math.random()<0.5){const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f];labBurst(P.x+fv[0]*22+rnd(-12,12),P.y+fv[1]*22+rnd(-6,6),3,'snow',80);}shake=Math.max(shake,Math.min(0.06,g2/150));}\n"
    "    L.big=(L.big||0)+(g2>4?dt:-dt);if(L.big>1.4){L.big=0;addFloat(P.x,P.y-28,['MEGA PLOW!','SNOWNADO!','UNSTOPPABLE!'][Math.floor(Math.random()*3)],'#ffffff',0.9);sfx('whoosh',0,{vol:0.4});}else if(L.big<0)L.big=0;}};",
    "tick(dt,tid,L){const g2=run.lastGot||0;if(L.meter==null){L.meter=0;L.mega=0;L.n=0;}const need=Math.max(120,G.clearable*0.09);\n"
    "    if(!(L.mega>0)){L.meter+=g2/need;if(L.meter>=1){L.meter=0;L.mega=8;L.n++;G.def.value*=2;shake=Math.max(shake,0.3);buzz(50);sfx('fanfare');sfx('whoosh');addFloat(P.x,P.y-34,'SNOW DAY! MEGA BLADE!','#ffffff',1.6);labRing(P.x,P.y,30);labBurst(P.x,P.y,30,'snow',110);if(L.n>=3)labGoldGift(P.x,P.y-48,'SNOW DAY CHAMP!');}}\n"
    "    else{L.mega-=dt;if(g2>2&&Math.random()<0.6){const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],bw=bladeCells();labBurst(P.x+fv[0]*20+rnd(-bw,bw)*Math.abs(fv[1]),P.y+fv[1]*20+rnd(-bw,bw)*Math.abs(fv[0]),2,'snow',70);}if(L.mega<=0){L.mega=0;G.def.value/=2;addFloat(P.x,P.y-28,'MEGA OVER: FILL IT AGAIN!','#e8f0ff',1.1);sfx('cend');}}\n"
    "    labObj('MEGA',L.n,3,L.mega>0?Math.ceil(L.mega)+'S LEFT':Math.floor(L.meter*100)+'%');},\n"
    "  screen(){const L=run.lab;if(!L||L.meter==null)return;const x=W/2-40,y=VIEW_Y+VIEW_H-22,w=80,f2=L.mega>0?L.mega/8:L.meter;R(b,x-1,y-1,w+2,8,K);R(b,x,y,w,6,'#13306b');R(b,x,y,Math.round(w*f2),6,L.mega>0?(Math.floor(tNow*8)%2?'#ffffff':'#ffd23f'):'#9fd8ff');"
    "text(b,L.mega>0?'MEGA BLADE!':'SNOW DAY METER',W/2,y-9,L.mega>0?'#ffd23f':'#ffffff',{align:'center'});}};")
rep("MODES.snowday={name:'SNOW DAY',sub:'MEGA BLADE, MOUNTAINS OF SNOW',rule:'MEGA BLADE! PLOW IT ALL',col:'#e8f0ff',",
    "MODES.snowday={name:'SNOW DAY',sub:'FILL THE METER, GO MEGA',rule:'PLOW TO FILL THE METER',bonus:'GO MEGA 3 TIMES: GOLD GIFT',col:'#e8f0ff',")
rep("how:['A MEGA BLADE AND A FASTER PLOW,','BUT THE SNOW COMES DOWN TWO AND A','HALF TIMES AS FAST. JUST PLOW.','COINS X1.5.'],",
    "how:['THE SNOW COMES DOWN TWICE AS','FAST. EVERY SCOOP FILLS THE SNOW','DAY METER. FULL: 8 SECONDS OF','MEGA BLADE, MORE SPEED AND','DOUBLE COINS. COINS X1.5.'],")

# ---- Snowball Fight: forts all down = gold gift ----
rep("if(S.smashed>=S.n){labPay(P.x,P.y-38,3,'ALL FORTS DOWN!','#7fe08a');sfx('fanfare');}}","if(S.smashed>=S.n)labGoldGift(P.x,P.y-38,'ALL FORTS DOWN!');}")
rep("MODES.forts={name:'SNOWBALL FIGHT',sub:'SMASH THE SNOW FORTS',rule:'RAM THE SNOW FORTS',col:'#ff8fb0',",
    "MODES.forts={name:'SNOWBALL FIGHT',sub:'SMASH THE SNOW FORTS',rule:'DODGE THE MARKERS, RAM THE FORTS',bonus:'SMASH ALL FORTS: GOLD GIFT',arrows:1,col:'#ff8fb0',")
rep("how:['KIDS HAVE BUILT SNOW FORTS AND','PELT YOU FROM BEHIND THEM. RAM A','FORT TO SMASH IT AND SNOW IN THE','KID. SMASH THEM ALL FOR A BONUS.','COINS X1.5.'],",
    "how:['KIDS PELT YOU FROM SNOW FORTS.','A RED MARKER SHOWS WHERE A BALL','WILL LAND: STEER OFF IT. OR HIT','THE BALL WITH YOUR BLADE TO SEND','IT BACK! RAM EVERY FORT: BONUS.'],")

# ---- Star Shower: patterns ahead of you, shooting stars ----
rep("L.t2-=dt;if(L.t2<=0&&!L.st.length){L.t2=9;L.k=0;const c=nugSpot(60,110)||{x:P.x,y:P.y-60};for(let q=0;q<6;q++)for(let tries=0;tries<30;tries++){const x=Math.round(c.x+rnd(-36,36)),y=Math.round(c.y+rnd(-30,30));\n"
    "        if(x>8&&x<G.pw-8&&y>8&&y<G.ph-8&&labReach(x,y)&&!L.st.some(q2=>Math.hypot(q2.x-x,q2.y-y)<12)){L.st.push({x,y,t:-q*0.12});break;}}addFloat(c.x,c.y-34,'STAR SHOWER!','#ffef7a',1.2);sfx('whoosh',0,{rate:1.4});}",
    "L.t2-=dt;if(L.t2<=0&&!L.st.length){L.t2=8;L.k=0;L.nsh=(L.nsh||0)+1;starPattern(L);if(L.nsh%3===0)shootStar(L);sfx('whoosh',0,{rate:1.4});}\n"
    "    if(L.ss){const q=L.ss;q.t+=dt;if(q.t>0.9){const dx=q.x-P.x,dy=q.y-P.y,d=Math.hypot(dx,dy)||1,sp=moveSpeed()*(d<70?0.72:0.4);let nx=q.x+dx/d*sp*dt+Math.sin(q.t*3)*12*dt,ny=q.y+dy/d*sp*dt;nx=clamp(nx,10,G.pw-10);ny=clamp(ny,10,G.ph-10);if(labReach(nx,ny)){q.x=nx;q.y=ny;}else{q.x=clamp(q.x-dy/d*sp*dt,10,G.pw-10);q.y=clamp(q.y+dx/d*sp*dt,10,G.ph-10);}"
    "if(Math.random()<dt*20)particles.push({x:q.x,y:q.y,vx:rnd(-10,10),vy:rnd(-10,10),z:3,vz:rnd(0,10),life:0.5,t:0,kind:'conf',c:'#ffef7a'});"
    "if(labTouch(tid,{x:q.x-6,y:q.y-6,w:12,h:12})){labPay(q.x,q.y-14,1.5,'SHOOTING STAR!','#ffef7a');labRing(q.x,q.y,16);labBurst(q.x,q.y,20,'coin',80);sfx('fanfare');L.ss=null;}else if(q.t>7.5){addFloat(q.x,q.y-12,'IT GOT AWAY!','#ff9aa8',0.9);L.ss=null;}}}")
rep("if(L.k===6){if(L.gem<5){","if(L.k===6){L.perf=(L.perf||0)+1;if(L.perf>=3)labGoldGift(P.x,P.y-48,'STAR CATCHER!');if(L.gem<5){")
rep("L.st=L.st.filter(s2=>!s2.got&&s2.t<5.5);labObj('STARS',L.caught,null,L.st.length?L.k+'/6':'');L.tgt=nearest(L.st,q=>q.land);},",
    "L.st=L.st.filter(s2=>!s2.got&&s2.t<5.5);labObj('PERFECT',L.perf||0,3,L.st.length?L.k+'/6':'');L.tgt=L.ss&&L.ss.t>0.9?{x:L.ss.x,y:L.ss.y}:nearest(L.st,q=>q.land);},")
rep("    else if(!(s2.t>4.3&&Math.floor(tNow*10)%2)){const bo=Math.floor(tNow*4+s2.x)%2;R(b,s2.x-4,s2.y+4,9,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.bigStar,s2.x-4,s2.y-6-bo);}}});}},",
    "    else if(!(s2.t>4.3&&Math.floor(tNow*10)%2)){const bo=Math.floor(tNow*4+s2.x)%2;R(b,s2.x-4,s2.y+4,9,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.bigStar,s2.x-4,s2.y-6-bo);}}});}\n"
    "    const q=L.ss;if(q&&q.y>top-120&&q.y<bot+20)ents.push({base:q.y+4,draw:()=>{if(q.t<0.9){const k=q.t/0.9,sx=Math.round(q.x-(1-k)*70),sy=Math.round(q.y-(1-k)*120);for(let i=1;i<8;i++)R(b,sx-i*4,sy-i*7,2,2,'rgba(255,239,122,'+(0.7-i*0.08).toFixed(2)+')');b.drawImage(SPR.bigStar,sx-4,sy-4,9,9);return;}"
    "const bo=Math.floor(tNow*8)%2;b.fillStyle='rgba(255,239,122,0.3)';pixCircle(b,Math.round(q.x),Math.round(q.y),Math.round(9+Math.sin(tNow*10)*2));R(b,Math.round(q.x)-5,Math.round(q.y)+5,11,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.bigStar,Math.round(q.x)-7,Math.round(q.y)-9-bo,14,14);}});},")
rep("MODES.stars={name:'STAR SHOWER',sub:'CATCH THE FALLING STARS',rule:'CATCH ALL SIX STARS',col:'#ffef7a',",
    "MODES.stars={name:'STAR SHOWER',sub:'CATCH THE FALLING STARS',rule:'SWEEP UP ALL SIX STARS',bonus:'3 PERFECT SHOWERS: GOLD GIFT',arrows:1,col:'#ffef7a',")
rep("how:['EVERY FEW SECONDS A SHOWER OF SIX','STARS LANDS NEAR YOU. EACH STAR','YOU CATCH IN A SHOWER PAYS MORE.','CATCH ALL SIX FOR A GEM (UP TO 5','A JOB). THEY FADE FAST!'],",
    "how:['EVERY FEW SECONDS SIX STARS LAND','IN A LINE AHEAD OF YOU. SWEEP','THEM UP: EACH ONE PAYS MORE, ALL','SIX = A GEM (UP TO 5 A JOB). WATCH','FOR SHOOTING STARS: THEY RUN!'],")

# ---- new modes and helpers ----
rep("loadSave();save.sess=(save.sess||0)+1;",r"""// ================= LAB rev 3 events (Nov 20) =================
const DRIFTC=['#ffffff','#5ab8ff','#ff9a3c','#c46bff'];
// screen splat when a snowball hits you
let SPLATS=[];
function splatFx(){SPLATS=[];const n=3+Math.floor(Math.random()*2);for(let k=0;k<n;k++){const side=k%4;SPLATS.push({x:side===0?rnd(6,40):side===1?rnd(W-40,W-6):rnd(20,W-20),y:VIEW_Y+(side===2?rnd(10,40):side===3?VIEW_H-rnd(14,50):rnd(30,VIEW_H-30)),r:rnd(9,16),d:[...Array(7)].map(()=>[rnd(-1,1),rnd(-1,1),rnd(2,5)])});}sfx('splat',0,{vol:1});buzz(40);}
function drawSplat(){if(!(run.splat>0)||!SPLATS.length)return;const a=Math.min(1,run.splat/0.5);b.globalAlpha=a*0.92;for(const q of SPLATS){b.fillStyle=K;pixCircle(b,Math.round(q.x),Math.round(q.y+1),Math.round(q.r)+1);for(const d of q.d)pixCircle(b,Math.round(q.x+d[0]*q.r*1.2),Math.round(q.y+d[1]*q.r*1.2+1),Math.round(d[2])+1);b.fillStyle='#9fb4d8';pixCircle(b,Math.round(q.x),Math.round(q.y+1),Math.round(q.r));for(const d of q.d)pixCircle(b,Math.round(q.x+d[0]*q.r*1.2),Math.round(q.y+d[1]*q.r*1.2+1),Math.round(d[2]));
  b.fillStyle='#f4f8ff';pixCircle(b,Math.round(q.x),Math.round(q.y),Math.round(q.r));for(const d of q.d)pixCircle(b,Math.round(q.x+d[0]*q.r*1.2),Math.round(q.y+d[1]*q.r*1.2),Math.round(d[2]));b.fillStyle='#ffffff';pixCircle(b,Math.round(q.x-q.r*0.3),Math.round(q.y-q.r*0.3),Math.max(1,Math.round(q.r*0.3)));}b.globalAlpha=1;}
// star shower patterns: six stars in a line / arc / zigzag / s-curve ahead of the plow
function starPattern(L){const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],sv=Math.hypot(P.vx,P.vy),hx=sv>8?P.vx/sv:fv[0],hy=sv>8?P.vy/sv:fv[1],nx=-hy,ny=hx,kind=Math.floor(Math.random()*4),amp=Math.random()<0.5?1:-1;
  for(let q=0;q<6;q++){const al=50+q*15,f=q/5,lat=kind===0?0:kind===1?amp*14*Math.sin(f*Math.PI):kind===2?(q%2?9:-9):amp*12*Math.sin(f*Math.PI*2);let ok=null;
    for(const sh of [0,6,-6,12,-12]){const x=Math.round(P.x+hx*al+nx*(lat+sh)),y=Math.round(P.y+hy*al+ny*(lat+sh));if(x>8&&x<G.pw-8&&y>8&&y<G.ph-8&&labReach(x,y)&&labRect(G,x-4,y-4,8,8)&&!L.st.some(q2=>Math.hypot(q2.x-x,q2.y-y)<10)){ok={x,y};break;}}
    if(ok)L.st.push({x:ok.x,y:ok.y,t:-q*0.1});}
  if(!L.st.length){const c=nugSpot(60,110)||{x:P.x,y:P.y-60};for(let q=0;q<6;q++)for(let tr=0;tr<30;tr++){const x=Math.round(c.x+rnd(-36,36)),y=Math.round(c.y+rnd(-30,30));if(x>8&&x<G.pw-8&&y>8&&y<G.ph-8&&labReach(x,y)&&!L.st.some(q2=>Math.hypot(q2.x-x,q2.y-y)<12)){L.st.push({x,y,t:-q*0.12});break;}}}
  const m=L.st[2]||L.st[0];if(m)addFloat(m.x,m.y-30,['STAR LINE!','STAR ARC!','STAR ZIGZAG!','STAR SWIRL!'][kind],'#ffef7a',1.1);}
function shootStar(L){const p=nugSpot(70,120);if(!p)return;L.ss={x:p.x,y:p.y,t:0};addFloat(p.x,p.y-30,'SHOOTING STAR! CATCH IT!','#ffef7a',1.4);}

// ---------- PRESENT HUNT: 5 golden presents buried in the snow; follow the jingle ----------
const GOLDP=spr(["..K..K..",".KRKKRK.","KKKKKKKK","KYYRYYYK","KRRRRRRK","KYYRYYYK","KYYRYYYK","KKKKKKKK"],{Y:'#ffd23f',R:'#ff4f7a'});
MODES.presenthunt={name:'PRESENT HUNT',sub:'DIG UP THE GOLDEN PRESENTS',rule:'FOLLOW THE JINGLE, DIG THEM UP',bonus:'FIND ALL 5: GOLD GIFT',col:'#ff8fc8',
  how:['5 GOLDEN PRESENTS ARE BURIED','UNDER THE SNOW. LISTEN: THE','JINGLE GETS FASTER AS YOU GET','CLOSE, AND THE SNOW TWINKLES.','PLOW THE SPOT TO DIG ONE UP!'],
  post(g){const S=g.lab,rn=srng(hashS(g.def.id)+61),n=5,bands=labBands(g,n);S.gp=[];
    for(let k=0;k<n;k++){const [y0,y1]=bands[k];let p=null;for(let tr=0;tr<40&&!p;tr++){const q=labSpot(g,12,12,y0,y1,rn,{margin:6,xin:12,avoid:[{x:g.start.x,y:g.start.y,r:90}].concat(S.gp.map(o=>({x:o.x,y:o.y,r:120})))});if(!q)continue;const i=((q.y+6)>>1)*g.cols+((q.x+6)>>1);if(g.type[i]===T_BLOCK||(g.nc&&g.nc[i]))continue;p=q;}
      if(!p)continue;const gp={x:p.x+6,y:p.y+6,found:0,tw:rn()*2,cells:[]};for(let cy=(gp.y-5)>>1;cy<=(gp.y+5)>>1;cy++)for(let cx=(gp.x-5)>>1;cx<=(gp.x+5)>>1;cx++){const i=cy*g.cols+cx;if(cy<0||cx<0||cy>=g.rows||cx>=g.cols||g.type[i]===T_BLOCK||(g.nc&&g.nc[i]))continue;setDepth(g,i,1);gp.cells.push(i);}S.gp.push(gp);}
    S.n=S.gp.length;},
  tick(dt,tid,L){const S=G.lab;if(!S.gp||!S.gp.length)return;if(L.found==null){L.found=0;L.jt=0;}let near=null,nd=1e9;
    for(const gp of S.gp){if(gp.found){if(gp.pop<1)gp.pop+=dt*1.6;continue;}let clr=0;for(const i of gp.cells)if(G.depth[i]<CLEAR_T)clr++;const d=Math.hypot(P.x-gp.x,P.y-gp.y);
      if((gp.cells.length&&clr/gp.cells.length>=0.5)||labTouch(tid,{x:gp.x-4,y:gp.y-4,w:8,h:8})){gp.found=1;gp.pop=0;L.found++;labPay(gp.x,gp.y-16,1.5,'GOLDEN PRESENT!','#ffd23f');labRing(gp.x,gp.y,14);labBurst(gp.x,gp.y,18,'coin',70);sfx('gift');sfx('gold',0,{rate:1.3});buzz(25);
        if(L.found>=S.n)labGoldGift(P.x,P.y-44,'ALL 5 FOUND!');continue;}
      if(d<nd){nd=d;near=gp;}}
    L.nd=nd;if(near&&nd<180){L.jt-=dt;if(L.jt<=0){const k=nd/180;L.jt=0.18+k*1.1;sfx('tick',0,{rate:1.7+(1-k)*0.6,vol:0.12+0.4*(1-k)});near.ping=0.25;}}
    for(const gp of S.gp)if(gp.ping>0)gp.ping-=dt;
    labObj('GOLD PRESENTS',L.found,S.n,near&&nd<180?(nd<45?'HOT!':nd<100?'WARM':'COLD'):'');L.tgt=near?{x:near.x,y:near.y}:null;},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#ff8fc8');},
  ents(ents,top,bot){const S=G.lab,L=run.lab;if(!S.gp)return;for(const gp of S.gp){if(gp.y<top-20||gp.y>bot+20)continue;
    if(gp.found){if(gp.pop<1)ents.push({base:gp.y+20,draw:()=>{const k=gp.pop,y=Math.round(gp.y-6-k*18);b.globalAlpha=Math.max(0,1-k*0.8);b.drawImage(GOLDP,gp.x-4,y);b.globalAlpha=1;}});continue;}
    const d=Math.hypot(P.x-gp.x,P.y-gp.y);if(d>150)continue;const per=d<50?0.6:d<100?1.1:1.8,ph=((tNow+gp.tw)%per)/per;
    if(ph<0.3||gp.ping>0)ents.push({base:gp.y+30,draw:()=>{const k=gp.ping>0?1:1-Math.abs(ph-0.15)/0.15,r=Math.max(1,Math.round(1+k*3)),x=Math.round(gp.x+Math.sin(gp.tw*7)*2),y=Math.round(gp.y-2);R(b,x-r,y,r*2+1,1,'#ffef7a');R(b,x,y-r,1,r*2+1,'#ffef7a');R(b,x,y,1,1,'#ffffff');}});}}};

// ---------- YETI HUNT: a yeti that runs for open space; bump him 5 times ----------
function yetiMap(Y){const fp0=footprint(TOOLS[useIdx()].id,0,0,0),sz=Math.max(Y.w,Math.min(fp0.w,fp0.h)),PB={w:sz,h:sz},cs=6,cols=Math.floor(G.pw/cs),y0=Math.max(24,Math.floor((Y.y-210)/cs)*cs),y1=Math.min(G.ph-12,Y.y+210),rows=Math.max(1,Math.floor((y1-y0)/cs)),n=cols*rows,pass=new Uint8Array(n),F=new Float32Array(n).fill(1e9);
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const x=c*cs+cs/2,y=y0+r*cs+cs/2;pass[r*cols+c]=chaserFree(PB,x-sz/2,y-sz/2)&&chaserFree(Y,x-Y.w/2,y-Y.h/2)?1:0;}
  const pc=clamp(Math.floor(P.x/cs),0,cols-1),pr=clamp(Math.floor((P.y-y0)/cs),0,rows-1),q=[pr*cols+pc],d=new Float32Array(n).fill(1e9);d[q[0]]=Math.max(0,(P.y<y0?y0-P.y:P.y>y1?P.y-y1:0)/cs);
  for(let i=0;i<q.length;i++){const k=q[i],x=k%cols,y=(k/cols)|0;for(const [ax,ay] of [[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+ax,ny=y+ay;if(nx<0||ny<0||nx>=cols||ny>=rows)continue;const nk=ny*cols+nx;if(!pass[nk]||d[nk]<1e9)continue;d[nk]=d[k]+1;q.push(nk);}}
  for(let k=0;k<n;k++){if(pass[k]&&d[k]>=1e9)pass[k]=0;if(pass[k])F[k]=-1.3*d[k];}
  for(let sw=0;sw<4;sw++){const fw=sw%2===0;for(let t=0;t<n;t++){const k=fw?t:n-1-t;if(!pass[k])continue;const x=k%cols,y=(k/cols)|0;let m=F[k];if(x>0&&pass[k-1])m=Math.min(m,F[k-1]+1);if(x<cols-1&&pass[k+1])m=Math.min(m,F[k+1]+1);if(y>0&&pass[k-cols])m=Math.min(m,F[k-cols]+1);if(y<rows-1&&pass[k+cols])m=Math.min(m,F[k+cols]+1);F[k]=m;}}
  return {cs,cols,rows,y0,F,pass};}
function yetiSpawn(L,round){const p=nugSpot(110,170)||nugSpot(70,230);if(!p)return null;const Y={x:p.x-8,y:Math.max(30,p.y-4),w:16,h:8,vx:0,vy:0,inv:0,hits:0,st:'run',an:0,map:null,mt:0,round:round||1,leap:null};addFloat(p.x,Y.y-26,round>1?'THE YETI IS BACK!':'THERE IT IS!','#9fd8ff',1.3);sfx('warn',0,{rate:0.7,vol:0.4});return Y;}
function yetiGift(L,x,y,n){for(let k=0;k<n;k++){const a=k/n*Math.PI*2+Math.random()*0.5,sp=rnd(30,60);L.gifts.push({x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp*0.8,z:4,vz:rnd(30,55),t:0});}}
MODES.yetihunt={name:'YETI HUNT',sub:'CATCH THE PRESENT THIEF',rule:'CORNER HIM AND BUMP HIM 5 TIMES',bonus:'CATCH HIM: GOLD GIFT',arrows:1,col:'#9fd8ff',
  how:['A YETI HAS STOLEN A SACK OF','PRESENTS. HE RUNS FOR OPEN','SPACE, SO CUT HIM OFF. EACH BUMP','DROPS A PRESENT AND HE LEAPS','AWAY. FIVE BUMPS: THE SACK BURSTS!'],
  tick(dt,tid,L){if(!L.gifts){L.gifts=[];L.caught=0;L.back=1.5;}
    for(const gq of L.gifts){gq.t+=dt;if(gq.z>0||gq.vz>0){gq.x=clamp(gq.x+gq.vx*dt,6,G.pw-6);gq.y=clamp(gq.y+gq.vy*dt,8,G.ph-6);gq.vz-=160*dt;gq.z=Math.max(0,gq.z+gq.vz*dt);if(gq.z===0&&gq.vz<0){gq.vz=0;gq.vx=gq.vy=0;}}
      if(gq.t>0.4&&Math.hypot(P.x-gq.x,P.y-gq.y)<14){gq.got=1;labPay(gq.x,gq.y-10,0.5,'PRESENT!','#ff8fc8');sfx('gift',0,{rate:1.4});}}
    L.gifts=L.gifts.filter(gq=>!gq.got&&gq.t<14);
    let Y=L.yeti;if(!Y||Y.st==='gone'){L.back-=dt;if(L.back<=0){Y=L.yeti=yetiSpawn(L,(L.caught||0)+1);if(!Y)L.back=0.5;}if(!Y||Y.st==='gone'){labObj('YETI',0,5,L.caught?'CAUGHT '+L.caught:'');L.tgt=null;return;}}
    Y.an+=dt;if(Y.inv>0)Y.inv-=dt;const cx=Y.x+8,cy=Y.y+4,d=Math.hypot(cx-P.x,cy-P.y);
    if(Y.st==='give'){Y.t-=dt;if(Y.t<=0){Y.st='leave';addFloat(cx,cy-30,'SEE YOU LATER!','#ffffff',1);}labObj('YETI',5,5);L.tgt=null;return;}
    if(Y.st==='leave'){const tx=cx<G.pw/2?-30:G.pw+30;Y.x+=Math.sign(tx-cx)*moveSpeed()*1.1*dt;Y.mv=1;if(Y.x<-26||Y.x>G.pw+10){Y.st='gone';L.back=10;}L.tgt=null;return;}
    if(Y.leap){const lp=Y.leap;lp.t+=dt;const k=Math.min(1,lp.t/lp.dur);Y.x=lp.x0+(lp.x1-lp.x0)*k;Y.y=lp.y0+(lp.y1-lp.y0)*k;Y.hz=Math.sin(k*Math.PI)*22;if(k>=1){Y.leap=null;Y.hz=0;Y.vx=Y.vy=0;labBurst(Y.x+8,Y.y+6,8,'snow',40);sfx('flump',0,{vol:0.5});}labObj('YETI',Y.hits,5);L.tgt={x:Y.x+8,y:Y.y+4};return;}
    Y.mt-=dt;if(Y.mt<=0||!Y.map){Y.mt=0.3;Y.map=yetiMap(Y);}
    const M2=Y.map,sp=moveSpeed()*(0.74+0.08*(Y.round-1))*(d<45?1.15:1)*(Y.inv>0?1.2:1);let dvx=0,dvy=0;
    if(d<190){const c0=clamp(Math.floor(cx/M2.cs),0,M2.cols-1),r0=clamp(Math.floor((cy-M2.y0)/M2.cs),0,M2.rows-1),k0=r0*M2.cols+c0;let best=k0,bv=M2.pass[k0]?M2.F[k0]:1e9;
      for(let ay=-1;ay<=1;ay++)for(let ax=-1;ax<=1;ax++){if(!ax&&!ay)continue;const c=c0+ax,r=r0+ay;if(c<0||r<0||c>=M2.cols||r>=M2.rows)continue;const k=r*M2.cols+c;if(!M2.pass[k])continue;const v=M2.F[k]+(ax&&ay?0.4:0);if(v<bv-0.01){bv=v;best=k;}}
      if(best!==k0){const tx=(best%M2.cols)*M2.cs+M2.cs/2,ty=M2.y0+((best/M2.cols)|0)*M2.cs+M2.cs/2,ex=tx-cx,ey=ty-cy,el=Math.hypot(ex,ey)||1;dvx=ex/el*sp;dvy=ey/el*sp;}
      if(!Y.said||Y.said<0){Y.said=rnd(2.5,4);if(d<90)addFloat(cx,cy-30,['RAAAWR!','CATCH ME!','TOO SLOW!','HEH HEH!'][Math.floor(Math.random()*4)],'#ffffff',0.8);}Y.said-=dt;}
    else{Y.said=0;if(Math.random()<dt*0.6)addFloat(cx,cy-30,'NYAH NYAH!','#ffffff',0.8);}
    const kk=Math.min(1,dt*7);Y.vx+=(dvx-Y.vx)*kk;Y.vy+=(dvy-Y.vy)*kk;const nx=Y.x+Y.vx*dt,ny=clamp(Y.y+Y.vy*dt,24,G.ph-12);if(chaserFree(Y,nx,Y.y))Y.x=nx;else Y.vx*=-0.3;if(chaserFree(Y,Y.x,ny))Y.y=ny;else Y.vy*=-0.3;
    Y.mv=Math.hypot(Y.vx,Y.vy)>6;if(Y.mv&&Math.random()<dt*8)particles.push({x:Y.x+8+rnd(-4,4),y:Y.y+8,vx:-Y.vx*0.2,vy:-Y.vy*0.2,z:1,vz:rnd(5,15),life:0.35,t:0,kind:'snow'});
    if(Y.inv<=0&&labTouch(tid,{x:Y.x-2,y:Y.y-8,w:Y.w+4,h:Y.h+10})){Y.hits++;Y.inv=1.1;sfx('stomp');shake=Math.max(shake,0.18);buzz(30);HITSTOP=0.07;labBurst(cx,cy,12,'snow',70);
      if(Y.hits>=5){Y.st='give';Y.t=1.6;L.caught++;yetiGift(L,cx,cy-4,8);labPay(cx,cy-36,2,'YETI CAUGHT!','#7fe08a');addFloat(cx,cy-24,'OK OK! YOU WIN!','#ffffff',1.5);if(L.caught===1)labGoldGift(P.x,P.y-48,'SACK BURST!');else sfx('fanfare');}
      else{yetiGift(L,cx,cy-4,1);addFloat(cx,cy-34,['OOF!','HEY!','NOT FAIR!','GRRR!'][Y.hits%4],'#ffffff',0.9);
        const M3=yetiMap(Y);let bk=-1,bv=1e9;for(let k=0;k<M3.F.length;k++){if(!M3.pass[k])continue;const x=(k%M3.cols)*M3.cs+M3.cs/2,y=M3.y0+((k/M3.cols)|0)*M3.cs+M3.cs/2,dd=Math.hypot(x-cx,y-cy);if(dd<60||dd>125)continue;if(M3.F[k]<bv){bv=M3.F[k];bk=k;}}
        if(bk>=0){const x1=(bk%M3.cols)*M3.cs+M3.cs/2-8,y1=M3.y0+((bk/M3.cols)|0)*M3.cs+M3.cs/2-4;Y.leap={x0:Y.x,y0:Y.y,x1,y1,t:0,dur:0.6};Y.inv=1.0;sfx('whoosh',0,{rate:0.8,vol:0.5});}Y.map=null;}}
    labObj('YETI',Y.hits,5,L.caught?'CAUGHT '+L.caught:'');L.tgt={x:cx,y:cy};},
  ents(ents,top,bot){const L=run.lab;if(!L)return;for(const gq of L.gifts||[]){if(gq.y<top-10||gq.y>bot+10)continue;ents.push({base:gq.y+4,draw:()=>{if(gq.t>11&&Math.floor(tNow*8)%2)return;R(b,Math.round(gq.x)-3,Math.round(gq.y)+3,7,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.present,Math.round(gq.x)-4,Math.round(gq.y-4-gq.z));}});}
    const Y=L.yeti;if(!Y||Y.st==='gone'||Y.y<top-40||Y.y>bot+30)return;const C=CHASERS.yeti;ents.push({base:Y.y+Y.h,draw:()=>{const hz2=Math.round(Y.hz||0);R(b,Math.round(Y.x)-1,Math.round(Y.y)+Y.h-2,Y.w+2,2,'rgba(27,31,59,0.25)');if(Y.inv>0&&!Y.leap&&Math.floor(tNow*12)%2)return;
      const fr=C.frames[Y.mv||Y.leap||Y.st==='leave'?Math.floor(Y.an*10)%2:0],sx=Math.round(Y.x-C.ox),sy=Math.round(Y.y-C.oy-hz2);b.drawImage(fr,sx,sy);
      if(Y.st==='give'){R(b,sx+21,sy-2,1,12,K);R(b,sx+22,sy-2,6,4,K);R(b,sx+22,sy-1,5,2,'#ffffff');}
      else if(Y.st!=='leave'){for(let k=0;k<Math.max(1,5-Y.hits);k++)b.drawImage(SPR.present,sx+13+(k%2)*4,sy+2-k*3);}}});},
  screen(){const L=run.lab;if(L&&L.tgt)labArrow(L.tgt.x,L.tgt.y,'#9fd8ff');}};

// ---------- SNOWBALL ROLL: the ball is its own object ----------
function rollHit(B,x,y){const r=B.r*0.82,bx={x:x-r,y:y-r,w:r*2,h:r*2};if(x-B.r<1||x+B.r>G.pw-1||y-B.r<1||y+B.r>G.ph-1)return 'edge';for(const o of G.obstacles)if(overlap(bx,o))return o;
  for(const hz of G.hazards)if(typeof hz.x==='number'&&hz.w&&hz.kind!=='skier'&&hz.kind!=='sheep'&&!(hz.kind==='cross'&&hz.state!=='go')&&overlap(bx,hz))return hz;return null;}
function rollSpawn(L,tid){const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f],sp=VSPEC[tid],front=(sp?sp.hh+sp.bt:6)+8;for(const dd of [front,front+8,front+16]){const x=P.x+fv[0]*dd,y=P.y+fv[1]*dd,B={x,y,vx:0,vy:0,r:5,snow:0,roll:0,n:(L.ball&&L.ball.n)||0,best:(L.ball&&L.ball.best)||5};if(!rollHit(B,x,y))return B;}return null;}
function rollSmash(B,L,impact){const m=Math.max(0.7,Math.min(1.4,impact/60)),u=Math.pow(B.r/5,2)*0.22*m;B.n++;labPay(B.x,B.y-B.r-8,u,B.r>=22?'MEGA SMASH!':B.r>=14?'BIG SMASH!':'SMASH!');labBurst(B.x,B.y,Math.round(10+B.r*1.5),'snow',40+B.r*3);labRing(B.x,B.y,B.r+6);
  shake=Math.max(shake,0.1+B.r/80);sfx('crunch');if(B.r>=14){sfx('stomp');buzz(30);HITSTOP=0.06;}addSnowCircle(G,B.x,B.y,B.r*0.8,0.4);if(B.r>=22){L.megas=(L.megas||0)+1;if(L.megas>=1)labGoldGift(P.x,P.y-44,'MEGA SMASH!');}L.gone=0.7;}
MODES.snowroll={name:'SNOWBALL ROLL',sub:'GROW A GIANT SNOWBALL',rule:'PUSH IT, GROW IT, SMASH IT',bonus:'A MEGA SMASH: GOLD GIFT',col:'#ffffff',
  how:['PUSH THE SNOWBALL WITH YOUR PLOW:','IT ROLLS ON BY ITSELF AND GROWS','ON FRESH SNOW. SEND IT HARD INTO','A WALL TO SMASH IT AND CASH IN.','A SOFT KNOCK JUST BREAKS BITS OFF.'],
  tick(dt,tid,L){if(L.gone>0){L.gone-=dt;if(L.gone<=0){const nb=rollSpawn(L,tid);if(nb)L.ball=nb;else L.gone=0.3;}return;}
    let B=L.ball;if(!B){B=L.ball=rollSpawn(L,tid);if(!B)return;}
    // the plow pushes the ball out of its body and blade
    const boxes=[footprint(tid,P.x,P.y,P.f)];if(tid!=='ufo')boxes.push(bladeRect(tid,P.x,P.y,P.f,bladeCells()*2));let pushed=false;
    for(const q of boxes){const px=clamp(B.x,q.x,q.x+q.w),py=clamp(B.y,q.y,q.y+q.h),ex=B.x-px,ey=B.y-py,dd=Math.hypot(ex,ey);if(dd>=B.r)continue;let nx2,ny2;if(dd>0.01){nx2=ex/dd;ny2=ey/dd;}else{const fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f];nx2=fv[0];ny2=fv[1];}
      B.x+=nx2*(B.r-dd);B.y+=ny2*(B.r-dd);const pv=(P.vx||0)*nx2+(P.vy||0)*ny2,bv=B.vx*nx2+B.vy*ny2,want=Math.max(0,pv)*1.12+6;if(bv<want){B.vx+=nx2*(want-bv);B.vy+=ny2*(want-bv);}pushed=true;}
    if(pushed){const o=rollHit(B,B.x,B.y);if(o){if(B.r>=8&&o!=='edge')rollSmash(B,L,Math.hypot(P.vx||0,P.vy||0));else{B.x=clamp(B.x,B.r+1,G.pw-B.r-1);B.y=clamp(B.y,B.r+1,G.ph-B.r-1);}if(L.gone>0)return;}}
    // roll: momentum, rolling friction (big balls roll further)
    const sp=Math.hypot(B.vx,B.vy);if(sp>0){const dec=Math.max(22,55-B.r*1.3)*dt,ns=Math.max(0,sp-dec);B.vx*=ns/sp;B.vy*=ns/sp;}
    for(const ax of [0,1]){const nx=ax?B.x:B.x+B.vx*dt,ny=ax?B.y+B.vy*dt:B.y,o=rollHit(B,nx,ny);if(!o){B.x=nx;B.y=ny;continue;}const imp=Math.abs(ax?B.vy:B.vx);
      if(o!=='edge'&&imp>34&&B.r>=8){rollSmash(B,L,imp);return;}if(ax)B.vy*=-0.35;else B.vx*=-0.35;if(imp>12&&B.snow>0){const lose=B.snow*0.14;B.snow-=lose;labBurst(B.x,B.y,6,'clump',40);sfx('flump',0,{vol:0.35,rate:1.3});addFloat(B.x,B.y-B.r-6,'CHUNKS OFF!','#c6d9f3',0.6);}}
    B.roll+=Math.hypot(B.vx,B.vy)*dt;
    const acc={got:0,cnt:0,fresh:0},r2=B.r*B.r;for(let cy=Math.max(0,Math.floor((B.y-B.r)/2));cy<=Math.min(G.rows-1,Math.floor((B.y+B.r)/2));cy++)for(let cx=Math.max(0,Math.floor((B.x-B.r)/2));cx<=Math.min(G.cols-1,Math.floor((B.x+B.r)/2));cx++){const ddx=cx*2+1-B.x,ddy=cy*2+1-B.y;if(ddx*ddx+ddy*ddy<=r2)clearCell(cy*G.cols+cx,acc);}
    if(acc.got>0){B.snow+=acc.got;earn(acc.got*BASE_CELL_VALUE*G.def.value*valueMult());}
    B.r=Math.min(26,5+Math.sqrt(B.snow)*0.3);B.best=Math.max(B.best,B.r);
    labObj('SIZE',Math.round(B.r),26,B.r>=10?'X'+(Math.pow(B.r/5,2)).toFixed(1):'');},
  ents(ents,top,bot){const L=run.lab,B=L&&L.ball;if(!B||L.gone>0)return;ents.push({base:B.y+B.r,draw:()=>{const x=Math.round(B.x),y=Math.round(B.y),r=Math.round(B.r);
    b.fillStyle='rgba(27,31,59,0.22)';b.fillRect(x-r,y+r-1,r*2,3);b.fillStyle=K;pixCircle(b,x,y,r+1);b.fillStyle='#c6d9f3';pixCircle(b,x,y,r);b.fillStyle='#f4f8ff';pixCircle(b,x-Math.round(r*0.15),y-Math.round(r*0.15),Math.round(r*0.85));
    b.fillStyle='#ffffff';pixCircle(b,x-Math.round(r*0.35),y-Math.round(r*0.4),Math.max(1,Math.round(r*0.3)));
    for(let k=0;k<5;k++){const an=B.roll/Math.max(4,r)+k*1.26,dx=Math.cos(an)*r*0.6,dy=Math.sin(an)*r*0.6;R(b,Math.round(x+dx),Math.round(y+dy*0.8),2,1,'#9fb4d8');}
    if(r>=24&&Math.floor(tNow*6)%2)text(b,'MAX!',x,y-r-10,'#ffd23f',{align:'center'});}});}};

// ---------- TIME ATTACK: checkpoint run ----------
MODES.timeattack={name:'TIME ATTACK',sub:'CHECKPOINT TO CHECKPOINT',rule:'REACH EACH CHECKPOINT IN TIME',bonus:'REACH THE FINISH: GOLD GIFT',arrows:1,col:'#7fe08a',
  how:['THE CLOCK IS SHORT. EVERY','CHECKPOINT YOU CROSS ADDS TIME','AND SHOWS YOUR SPLIT AGAINST','YOUR BEST RUN. REACH THE FINISH','FOR A BONUS. PLOW ON THE WAY!'],
  post(g){const S=g.lab,st=g.start.y,yT=50,yB=g.ph-50,down=st<g.ph/2,v=Math.max(30,moveSpeed()*0.6),legs=[];let y=st,dir=down?1:-1,tot=0;
    while(tot<900||!legs.length){const end=dir>0?yB:yT,len=Math.abs(end-y);if(len<40&&legs.length)break;legs.push({y0:y,y1:end,dir,len});tot+=len;y=end;dir=-dir;if(legs.length>6)break;}
    const n=Math.max(3,Math.min(10,Math.round((tot-80)/280))),at=d=>{let a=d;for(const L2 of legs){if(a<=L2.len)return {y:Math.round(L2.y0+L2.dir*a),dir:L2.dir};a-=L2.len;}const L3=legs[legs.length-1];return {y:L3.y1,dir:L3.dir};};
    S.cps=[];for(let k=1;k<=n;k++){const q=at(80+(tot-80)*k/n-(k===n?6:0));S.cps.push({y:q.y,dir:q.dir,st:0,rd:80+(tot-80)*k/n});}
    S.seg=S.cps.map((c,k)=>{const prev=k?S.cps[k-1]:{rd:0,dir:down?1:-1};return (c.rd-prev.rd)/v+2+(c.dir!==prev.dir?1.5:0);});g.def.time=Math.round(S.seg[0]+5);S.down=down;},
  tick(dt,tid,L){const S=G.lab;if(!S.cps)return;if(L.k==null){L.k=0;L.py=P.y;L.e=0;L.lastTick=99;}L.e+=dt;
    const c=S.cps[L.k];if(c&&L.py!==P.y&&(L.py-c.y)*(P.y-c.y)<=0&&Math.sign(P.y-L.py)===c.dir){c.st=1;c.e=L.e;const best=((save.labTA||{})[G.def.id]||[]),last=L.k===S.cps.length-1,diff=best[L.k]!=null?L.e-best[L.k]:null;c.diff=diff;
      if(!last){const add=Math.round(S.seg[L.k+1]*10)/10;run.time+=add;addFloat(P.x,P.y-30,'CHECKPOINT! +'+add.toFixed(1)+'S','#7fe08a',1.3);sfx('time');sfx('combo',0,{rate:1+L.k*0.06});labRing(P.x,P.y,18);}
      else{L.fin=1;const left=Math.max(0,run.time);addFloat(P.x,P.y-40,'FINISH! '+L.e.toFixed(1)+'S','#ffd23f',2);labPay(P.x,P.y-28,Math.min(4,left*0.15),'TIME BONUS');const rec=!best.length||L.e<best[best.length-1];
        if(rec){save.labTA=save.labTA||{};save.labTA[G.def.id]=S.cps.map(q=>Math.round(q.e*10)/10);persist();addFloat(P.x,P.y-52,'NEW RECORD!','#7fe08a',2);}labGoldGift(P.x,P.y-64,'FINISHED!');}
      if(diff!=null)addFloat(P.x,P.y-42,(diff<=0?'-':'+')+Math.abs(diff).toFixed(1),diff<=0?'#7fe08a':'#ff6a5a',1.3);L.k++;}
    L.py=P.y;if(!L.fin&&run.time<10&&run.time>0){const s2=Math.ceil(run.time);if(s2!==L.lastTick){L.lastTick=s2;sfx('tick',0,{rate:s2<=3?1.6:1.2,vol:0.6});}}
    labObj('CHECKPOINT',Math.min(L.k,S.cps.length),S.cps.length,L.fin?'DONE '+(S.cps[S.cps.length-1].e||0).toFixed(1)+'S':'');const nx=S.cps[L.k];L.tgt=nx&&(nx.y<camY-4||nx.y>camY+VIEW_H+4)?{x:P.x,y:nx.y}:null;},
  screen(){const L=run.lab,S=G.lab;if(!L||!S.cps||L.k==null)return;if(L.tgt)labArrow(L.tgt.x,L.tgt.y,'#7fe08a');if(run.ended)return;
    const t=Math.max(0,run.time),hot=!L.fin&&t<5,col=L.fin?'#7fe08a':hot?(Math.floor(tNow*6)%2?'#ff4a4a':'#ffffff'):t<10?'#ffd23f':'#ffffff';text(b,L.fin?'FINISHED':t.toFixed(1),W/2,VIEW_Y+26,col,{align:'center',scale:2});
    const best=(save.labTA||{})[G.def.id];if(best&&best.length&&!L.fin)text(b,'BEST '+best[best.length-1].toFixed(1)+'S',W/2,VIEW_Y+44,'#9fd8ff',{align:'center'});},
  ents(ents,top,bot){const S=G.lab,L=run.lab;if(!S.cps)return;S.cps.forEach((c,k)=>{if(c.y<top-20||c.y>bot+20)return;const kk=L&&L.k!=null?L.k:0;if(k>kk+1||k<kk-1)return;const last=k===S.cps.length-1,nxt=kk===k;ents.push({base:c.y+1,draw:()=>{
      const a=c.st?0.35:1;b.globalAlpha=a;for(let x=0;x<G.pw;x+=4){const ch=last?(((x>>2)+Math.floor(c.y/2))%2):0;R(b,x,c.y-1,2,2,last?(ch?K:'#ffffff'):(nxt&&Math.floor(tNow*4)%2?'#ffffff':'#7fe08a'));}
      for(const sx of [3,G.pw-5]){R(b,sx,c.y-14,2,15,K);R(b,sx+(sx<9?2:-5),c.y-14,5,4,last?'#ffffff':'#7fe08a');}text(b,last?'FINISH':'CHECKPOINT '+(k+1),G.pw/2,c.y-10,last?'#ffd23f':'#7fe08a',{align:'center'});if(nxt)for(const ax of [24,G.pw-28])for(let i=0;i<4;i++){const yy=c.dir>0?c.y-12+i:c.y-3-i;R(b,ax-3+i,yy,7-i*2,1,K);R(b,ax-2+i,yy,Math.max(1,5-i*2),1,'#7fe08a');}b.globalAlpha=1;}});});}};
loadSave();save.sess=(save.sess||0)+1;""")
open(f,'w',encoding='utf-8').write(s)
print('p156 lab events rev 3: present hunt (golden presents), mother lode, safety-map yeti, rolling snowball, drift sparks + turbo, snow day meter, checkpoint time attack, smart throwers + deflect, star patterns + shooting stars')
