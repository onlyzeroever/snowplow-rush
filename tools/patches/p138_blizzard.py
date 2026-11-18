import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Alex, Nov 19 (playing the Blizzard preview on his phone):
# 1. Blizzard Weekend didn't feel different. Event jobs now have a real blizzard: wind gusts that are signalled
#    (arrows + GUST!) and then push the machine sideways for ~2.5 s (big machines less), snow streaking past,
#    a white-out pulse, extra snow blown back in during gusts, and squalls (the existing snow dumps). Coins stay x2.
# 2. Bugs he found:
#    - the shopping trolley read as "a black thing with a red line": redrawn as a side-view trolley that faces its way
#    - thrown snowballs were a black 3 px square ("little moving black thing"): now a white ball with an outline
#    - grannies just showed "..." and never did anything: they now call "CLEAR MY PATH, DEAR!" when you're near
#      and their path blinks yellow until it's clear (then they walk out and tip you, as before)
#    - string lights / banners ended in mid-air: a little post now holds up any end that isn't at the edge or on something
#    - parked cars backed out 30 px and drove straight back in: now they back out, turn, drive off along the aisle,
#      come back later and park again. They wait and beep if you're in the way. Only parked cars block.
#    - two messages on the same spot ("COMBO OVER" + "DODGED!") overlapped: messages now stack.

# --- 1. blizzard: event mods
rep("blizzard:{name:'BLIZZARD WEEKEND',sub:'HEAVY SNOW, DOUBLE COINS',mod:{snow:1.6,value:2},",
    "blizzard:{name:'BLIZZARD WEEKEND',sub:'GUSTS, SQUALLS, DOUBLE COINS',mod:{snow:1.4,value:2,squall:11,gust:1},")
rep("if(m.snow)c.snowfall=L.snowfall*m.snow;",
    "if(m.snow)c.snowfall=L.snowfall*m.snow;if(m.squall)c.squall=L.squall?Math.min(L.squall,m.squall):m.squall;if(m.gust)c.gust=1;")
# gusts: update (next to the snowfall)
rep("  // snowfall\n  run.snowAcc+=G.def.snowfall*dt;",
r"""  // blizzard gusts (event jobs): calm, then a signalled gust that pushes the machine sideways
  if(G.def.gust&&!run.ended&&!run.sweep){if(!run.bz){run.bz={phase:'calm',t:3.5,dir:1,wind:12};BZF.forEach((f2,i)=>{f2.x=(i*37)%W;f2.y=HUD_H+(i*53)%VIEW_H;});
      if((save.bzTips||0)<3){save.bzTips=(save.bzTips||0)+1;addFloat(G.pw/2,P.y-34,'BLIZZARD!','#9fd8ff',2.4);addFloat(G.pw/2,P.y-25,'HOLD ON IN THE GUSTS','#ffffff',2.4);}}
    const z=run.bz;z.t-=dt;
    if(z.phase==='calm'){z.wind+=(12*z.dir-z.wind)*Math.min(1,dt*2);if(z.t<=0){z.phase='warn';z.t=1.3;z.dir=Math.random()<0.5?-1:1;sfx('warn');addFloat(clamp(P.x,40,G.pw-40),P.y-26,z.dir>0?'GUST >>>':'<<< GUST','#9fd8ff',1.3);}}
    else if(z.phase==='warn'){z.wind+=(40*z.dir-z.wind)*Math.min(1,dt*2);if(z.t<=0){z.phase='blow';z.t=2.6;sfx('whoosh',0,{vol:0.55,rate:0.7});shake=Math.max(shake,0.12);}}
    else{z.wind+=(130*z.dir-z.wind)*Math.min(1,dt*4);if(z.t<=0){z.phase='calm';z.t=rnd(5.5,8.5);}
      else{const hw=((VSPEC[tid]||{}).hw||6),ramp=Math.min(1,(2.6-z.t)/0.4,z.t/0.5+0.2),wx=z.dir*16/(1+Math.max(0,hw-6)/12)*ramp*dt;
        if(wx&&!(P.stun>0)&&!blockedBy(footprint(tid,P.x+wx,P.y,P.f)))P.x+=wx;run.snowAcc+=G.def.snowfall*1.2*dt;}}
    for(const f2 of BZF){f2.x+=(z.wind*f2.k)*dt;f2.y+=f2.vy*dt;if(f2.x>W+4)f2.x-=W+8;if(f2.x<-4)f2.x+=W+8;if(f2.y>HUD_H+VIEW_H)f2.y=HUD_H-2;}}
  // snowfall
  run.snowAcc+=G.def.snowfall*dt;""")
# gust visuals: streaking snow, white-out pulse, warning arrows
rep("function overlayOpen(){",
r"""const BZF=[];for(let i=0;i<70;i++)BZF.push({x:0,y:0,k:0.6+(i%5)*0.15,vy:22+(i%7)*6,d:i%3===0?2:1});
function drawBlizzard(){const z=run.bz;if(!z||!G||!G.def.gust)return;const blow=z.phase==='blow';
  if(blow){const a=0.12+0.08*Math.sin(tNow*7);b.fillStyle='rgba(240,246,255,'+a.toFixed(3)+')';b.fillRect(0,HUD_H,W,VIEW_H);}
  for(const f2 of BZF){const x=Math.round(f2.x),y=Math.round(f2.y),len=Math.min(9,Math.round(Math.abs(z.wind)*f2.k/20));
    if(len>=2){R(b,z.wind>0?x-len:x,y,len,1,'rgba(140,168,212,0.8)');R(b,z.wind>0?x-1:x,y,2,1,'#ffffff');}else{R(b,x,y,f2.d,f2.d,'rgba(150,175,215,0.85)');R(b,x,y,1,1,'#ffffff');}}
  if(z.phase!=='calm'){const k=z.phase==='blow'?1:0.4;for(let i=0;i<9;i++){const yy=HUD_H+20+((i*47+Math.floor(tNow*3)*13)%(VIEW_H-40)),ln=10+(i%3)*5,xx=Math.round(((tNow*Math.abs(z.wind)*1.6+i*61)%(W+40))-20);const sx=z.dir>0?xx:W-xx;if(Math.random()<k)R(b,sx,yy,ln,1,'rgba(120,150,200,0.55)');}}
  if(z.phase==='warn'&&Math.floor(tNow*6)%2===0){const yy=HUD_H+VIEW_H/2-20;for(let k=0;k<3;k++){const ax=z.dir>0?6+k*8:W-12-k*8;text(b,z.dir>0?'>':'<',ax,yy,'#9fd8ff');text(b,z.dir>0?'>':'<',ax,yy+30,'#9fd8ff');}}}
function overlayOpen(){""")
rep("drawChaserArrows();drawLeftArrow();drawHUD();drawBottomBar();drawCoinFly();",
    "drawBlizzard();drawChaserArrows();drawLeftArrow();drawHUD();drawBottomBar();drawCoinFly();")

# --- 2a. shopping trolley: side view, faces the way it rolls
rep('function cartSprite(){return spr(["KKKKKKKKKK","KcKcKcKcKK","KCKCKCKCKK","KcKcKcKcKK","KCKCKCKCKK","KcKcKcKcKK","KKKKKKKKKK","KRRRRRRRRK","KKKKKKKKKK",".XK....KX."],{c:\'#c6d0e0\',C:\'#e8eef6\',R:\'#e03a4e\',X:\'#2a2a36\'});}',
    'function cartSprite(){return spr(["KK............","KRK...........",".KRKKKKKKKKKKK","..KCcCcCcCcCcK","..KcCcCcCcCcCK","..KCcCcCcCcCcK","...KcCcCcCcCK.","...KKKKKKKKKK.","....K......K..","...KKKKKKKKKK.","...KXK....KXK.","....K......K.."],{c:\'#9fb0c8\',C:\'#e8eef6\',R:\'#e03a4e\',X:\'#55607a\'});}')
rep("const CART=cartSprite(),","const CART=cartSprite(),CARTL=flipH(CART),")
rep("else if(hz.kind==='cart')ents.push({base:hz.y+hz.h,draw:()=>b.drawImage(CART,hx,hy)});",
    "else if(hz.kind==='cart')ents.push({base:hz.y+hz.h,draw:()=>b.drawImage(hz.vx<0?CARTL:CART,hx-2,hy-3)});")

# --- 2b. snowballs: a white ball with an outline and a ground shadow
rep("R(b,Math.round(x)-1,Math.round(y)-1,3,3,K);R(b,Math.round(x),Math.round(y),1,1,'#ffffff');R(b,Math.round(bl.x0+(bl.x1-bl.x0)*k),Math.round(bl.y0+(bl.y1-bl.y0)*k),2,1,'rgba(40,50,90,0.35)');",
    "const gx=Math.round(bl.x0+(bl.x1-bl.x0)*k),gy=Math.round(bl.y0+(bl.y1-bl.y0)*k),X=Math.round(x),Y=Math.round(y);R(b,gx-1,gy+1,4,1,'rgba(40,50,90,0.28)');R(b,X-2,Y-1,5,3,K);R(b,X-1,Y-2,3,5,K);R(b,X-1,Y-1,3,3,'#ffffff');R(b,X,Y,2,2,'#dfe9f8');R(b,X-1,Y-1,1,1,'#ffffff');")

# --- 2c. grannies: say what they need, show the path
rep("run.nbT-=dt;for(const nb of G.neighbours){",
    "run.nbT-=dt;for(const nb of G.neighbours){\n    if(nb.state==='wait'&&!nb.asked&&Math.hypot(P.x-nb.x,P.y-nb.y)<70){nb.asked=1;addFloat(clamp(nb.x,46,G.pw-46),nb.y-30,'CLEAR MY PATH, DEAR!','#ffd23f',1.8);}")
rep("for(const nb of G.neighbours){if(nb.y<top||nb.y>bot)continue;ents.push({base:nb.y+1,draw:()=>{const nx=Math.round(nb.x),ny=Math.round(nb.y);",
    "for(const nb of G.neighbours){if(nb.y<top||nb.y>bot)continue;\n    if(nb.state==='wait'&&Math.hypot(P.x-nb.x,P.y-nb.y)<120&&Math.floor(tNow*2.5)%2===0)for(const rc of nb.rects){const [x0,y0,w0,h0]=rc;for(let xx=x0;xx<x0+w0;xx+=3){R(b,xx,y0,2,1,'#ffd23f');R(b,xx,y0+h0-1,2,1,'#ffd23f');}for(let yy=y0;yy<y0+h0;yy+=3){R(b,x0,yy,1,2,'#ffd23f');R(b,x0+w0-1,yy,1,2,'#ffd23f');}}\n    ents.push({base:nb.y+1,draw:()=>{const nx=Math.round(nb.x),ny=Math.round(nb.y);")

# --- 2d. posts under string lights / banners whose ends would hang in mid-air
rep("for(const p of D.over||[]){const f=OVERS[p[0]];if(!f)continue;const ok=p[0]+'|'+p[3]+'|'+p[4];let sp=OVC.get(ok);if(!sp){sp=f(p[3],p[4]);OVC.set(ok,sp);}g.over.push({spr:sp,sx:p[1],sy:p[2]});}",
    "for(const p of D.over||[]){const f=OVERS[p[0]];if(!f)continue;const ok=p[0]+'|'+p[3]+'|'+p[4];let sp=OVC.get(ok);if(!sp){sp=f(p[3],p[4]);OVC.set(ok,sp);}g.over.push({spr:sp,sx:p[1],sy:p[2],k:p[0]});}")
rep("for(const p of Q.over||[]){const f=OVERS[p[0]];if(f)g.over.push({spr:f(p[3],p[4]),sx:p[1],sy:p[2]});}}",
    "for(const p of Q.over||[]){const f=OVERS[p[0]];if(f)g.over.push({spr:f(p[3],p[4]),sx:p[1],sy:p[2],k:p[0]});}}")
rep("ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();",
    "for(const o of G.over)if((o.k==='lights'||o.k==='banner')&&o.sy+30>top&&o.sy<bot){if(!o.posts){o.posts=[];for(const ex of [o.sx,o.sx+o.spr.width-1]){if(ex<=3||ex>=G.pw-4)continue;const ey=o.sy+(o.k==='banner'?2:1);\n      if(G.obstacles.some(q=>ex>=q.sx-1&&ex<=q.sx+q.spr.width&&ey+6>=q.sy&&ey<=q.sy+q.spr.height))continue;o.posts.push([ex,ey]);}}\n    for(const [ex,ey] of o.posts)ents.push({base:ey+15,draw:()=>{R(b,ex-1,ey-1,3,17,K);R(b,ex,ey,1,15,'#a8673a');R(b,ex-1,ey-2,3,1,'#f4f8ff');R(b,ex-2,ey+15,5,1,'rgba(60,80,130,0.25)');}});}\n  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();")

# --- 2e. parked cars: back out, drive off along the aisle, come back later, park
rep("for(const p of D.pull||[]){const c=CAR_PAL[(p[2]||0)%5];g.hazards.push({kind:'pull',x:p[0],y:p[1],w:22,h:28,home:p[1],state:'park',t:rnd(2,8),spr:carSprite(c[0],c[1])});",
    "for(const p of D.pull||[]){const c=CAR_PAL[(p[2]||0)%5];g.hazards.push({kind:'pull',x:p[0],y:p[1],w:22,h:28,home:p[1],hx:p[0],body:c[0],dir:1,state:'park',t:rnd(2,8),spr:carSprite(c[0],c[1])});")
rep("""      else if(hz.state==='out'){hz.y+=26*dt;if(hz.y>=hz.home+30){hz.y=hz.home+30;hz.state='wait';hz.t=1.4;}}
      else if(hz.state==='wait'){if(hz.t<=0)hz.state='in';}""",
"""      else if(hz.state==='out'){if(hz.hx==null)hz.hx=hz.x;hz.y+=26*dt;if(hz.y>=hz.home+30){hz.y=hz.home+30;hz.state='turn';hz.t=0.35;hz.dir=hz.exit||((hz.x+11<G.pw/2)?-1:1);}}
      else if(hz.state==='turn'){if(hz.t<=0)hz.state='leave';continue;}
      else if(hz.state==='leave'||hz.state==='arrive'){const r={x:hz.x-4+hz.dir*3,y:hz.home+37,w:30,h:14};
        if(overlap(r,pr)){if(!hz.honk){hz.honk=1;sfx('warn');addFloat(hz.x+11,hz.home+30,'BEEP BEEP!','#ffd23f',0.8);}continue;}hz.honk=0;hz.x+=hz.dir*42*dt;
        if(hz.state==='leave'&&(hz.x<-36||hz.x>G.pw+14)){hz.state='away';hz.t=rnd(5,9);}
        else if(hz.state==='arrive'&&((hz.dir>0&&hz.x>=hz.hx)||(hz.dir<0&&hz.x<=hz.hx))){hz.x=hz.hx;hz.state='turn2';hz.t=0.35;}continue;}
      else if(hz.state==='away'){if(hz.t<=0){hz.dir=-hz.dir;hz.x=hz.dir>0?-36:G.pw+14;hz.state='arrive';}continue;}
      else if(hz.state==='turn2'){if(hz.t<=0){if(overlap({x:hz.hx,y:hz.home,w:22,h:28},pr)){if(!hz.honk){hz.honk=1;sfx('warn');addFloat(hz.hx+11,hz.home+30,'BEEP BEEP!','#ffd23f',0.8);}hz.t=0.4;}else{hz.honk=0;hz.state='in';}}continue;}
      else if(hz.state==='wait'){if(hz.t<=0)hz.state='in';}""")
rep("else if(hz.state==='in'){hz.y-=26*dt;if(hz.y<=hz.home){hz.y=hz.home;hz.state='park';hz.t=rnd(5,9);pullSpot(hz,false);}}",
    "else if(hz.state==='in'){hz.y-=26*dt;if(hz.y<=hz.home){hz.y=hz.home;hz.state='park';hz.t=rnd(6,10);pullSpot(hz,false);}}")
rep("g.hazards.push({kind:'pull',x:bx+2,y:ry+4,w:22,h:28,home:ry+4,state:'park',t:rnd(2,8),spr:carSprite(c[0],c[1])});",
    "g.hazards.push({kind:'pull',x:bx+2,y:ry+4,w:22,h:28,home:ry+4,hx:bx+2,body:c[0],dir:1,state:'park',t:rnd(2,8),spr:carSprite(c[0],c[1])});")
rep("function carSideSprite(a){","function carSideOf(col){const c=mk(30,14),g=c.getContext('2d');R(g,2,3,26,8,K);R(g,3,4,24,6,col);R(g,8,1,13,4,K);R(g,9,2,11,3,'#8fd3ff');R(g,3,4,24,1,PAL.W);R(g,4,10,6,4,K);R(g,20,10,6,4,K);R(g,26,5,2,2,'#ffe9a8');R(g,2,4,1,2,'#e03a4e');return c;}\nfunction carSideSprite(a){")
rep("if(hz.state==='park'){if(hz.t<=0&&Math.abs(P.y-hz.y)<150){hz.state='warn';",
    "if(hz.state==='park'){if(hz.t<=0&&Math.abs(P.y-hz.y)<150&&hz.exit===undefined)hz.exit=pullExit(hz);if(hz.t<=0&&!hz.exit)hz.t=1e9;if(hz.t<=0&&Math.abs(P.y-hz.y)<150){hz.state='warn';")
rep("function pullSpot(hz,free){",
    "function pullExit(hz){const g=G,hx=hz.hx!=null?hz.hx:hz.x,y0=hz.home+28,hit=r=>g.obstacles.some(o=>o.x<r.x+r.w&&r.x<o.x+o.w&&o.y<r.y+r.h&&r.y<o.y+o.h)||g.scenery.some(o=>{const t=o.sy+(o.spr.padTop||0);return o.sx<r.x+r.w&&r.x<o.sx+o.spr.width&&t<r.y+r.h&&r.y<o.sy+o.spr.height;})||g.hazards.some(q=>q!==hz&&q.kind==='pull'&&q.x<r.x+r.w&&r.x<q.x+q.w&&q.home<r.y+r.h&&r.y<q.home+q.h)||(()=>{for(let y=Math.max(0,r.y);y<Math.min(g.ph,r.y+r.h);y+=2)for(let x=Math.max(0,r.x);x<Math.min(g.pw,r.x+r.w);x+=2)if(g.type[(y>>1)*g.cols+(x>>1)]===T_BLOCK)return true;return false;})();\n  if(hit({x:hx,y:y0,w:22,h:30}))return 0;const near=(hx+11<g.pw/2)?-1:1;for(const d of [near,-near]){const r=d<0?{x:-40,y:y0+2,w:hx+44,h:24}:{x:hx+18,y:y0+2,w:g.pw+40-hx-18,h:24};if(!hit(r))return d;}return 0;}\nfunction pullSpot(hz,free){")
# only a stationary car blocks you
rep("for(const hz of G.hazards)if((hz.kind==='thrower'||hz.kind==='ped'||(hz.kind==='pull'&&hz.state!=='out'&&hz.state!=='in'))&&overlap(r,hz))m.set(hz,ovA(r,hz));",
    "for(const hz of G.hazards)if((hz.kind==='thrower'||hz.kind==='ped'||(hz.kind==='pull'&&(hz.state==='park'||hz.state==='warn'||hz.state==='turn'||hz.state==='turn2')))&&overlap(r,hz))m.set(hz,ovA(r,hz));")
rep("for(const hz of G.hazards)if(((hz.kind==='barrier'&&hz.closed)||hz.kind==='thrower'||hz.kind==='ped'||(hz.kind==='pull'&&hz.state!=='out'&&hz.state!=='in'))&&overlap(r,hz)&&!ignOK(r,hz,hz,1)){G.lastOb=hz;return 'ob';}",
    "for(const hz of G.hazards)if(((hz.kind==='barrier'&&hz.closed)||hz.kind==='thrower'||hz.kind==='ped'||(hz.kind==='pull'&&(hz.state==='park'||hz.state==='warn'||hz.state==='turn'||hz.state==='turn2')))&&overlap(r,hz)&&!ignOK(r,hz,hz,1)){G.lastOb=hz;return 'ob';}")
rep("else if(hz.kind==='pull')ents.push({base:hz.y+hz.h,draw:()=>{",
    "else if(hz.kind==='pull'&&hz.state==='away')continue;\n    else if(hz.kind==='pull'&&(hz.state==='leave'||hz.state==='arrive')){if(!hz.sR){hz.sR=carSideOf(hz.body||'#d8364b');hz.sL=flipH(hz.sR);}const sp=hz.dir>0?hz.sR:hz.sL;ents.push({base:hz.home+51,draw:()=>b.drawImage(sp,hx-4,hz.home+37)});}\n    else if(hz.kind==='pull')ents.push({base:hz.y+hz.h,draw:()=>{")

# --- 2f. messages stack instead of overlapping
rep("function addFloat(x,y,s,c,life){floats.push({x,y,s,c,t:0,life:life||0.9});}",
    "function addFloat(x,y,s,c,life){if(typeof s==='string'&&s[0]!=='+')for(let k=0;k<3;k++){if(floats.some(f=>f.t<0.6&&typeof f.s==='string'&&f.s[0]!=='+'&&Math.abs(f.x-x)<40&&Math.abs(f.y-y)<8))y-=9;else break;}floats.push({x,y,s,c,t:0,life:life||0.9});}")

open(f,'w',encoding='utf-8').write(s)
print('p138 blizzard gusts + squalls for Blizzard Weekend; trolley, snowballs, grannies, light posts, pull-out cars, stacked messages')
