import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# PROTOTYPE (Alex, Nov 19 04:00-04:06): "build like 10 different event types for me and my partner to test" and
# "I'm open to trying all of these twists, can we prototype them please? Don't push to main, we should test first."
# Everything here is OFF in the live game. It switches on only with ?lab in the URL or on a Vercel preview
# (lab.snowplowrush.app / *.vercel.app, the `lab` branch). There:
#  - EVENT LAB screen (LAB button on the map): 12 events (Blizzard, Present Hunt + 10 new) and 7 area twists,
#    each with 4 jobs from different areas to try.
#  - Area twists are on in their own areas (2nd job of each area teaches it, then every 4th job):
#    Farmland mud, City slush spray, Theme Park after dark, Harbour thin ice, Ski snowmaking, Pass wind, North whiteout.
#  - New events: Night Shift, Whiteout, Black Ice, Gold Rush, Snowball Fight, Yeti Hunt, Shooting Stars, Snow Day,
#    Hailstorm, Time Attack.

rep("  presents:{name:'PRESENT HUNT',sub:'PRESENTS EVERYWHERE',mod:{presents:4},prize:{trail:'sparkle',gems:60},col:'#ff8fc8'}};",
"""  presents:{name:'PRESENT HUNT',sub:'PRESENTS EVERYWHERE',mod:{presents:4},prize:{trail:'sparkle',gems:60},col:'#ff8fc8'},
  nightshift:{name:'NIGHT SHIFT',sub:'DARK STREETS, HEADLIGHTS ON',mod:{night:1,value:2},prize:{gems:60},col:'#ffd23f'},
  whiteout:{name:'WHITEOUT',sub:'YOU ONLY SEE AROUND YOU',mod:{fog:1,value:2},prize:{gems:60},col:'#e8f0ff'},
  blackice:{name:'BLACK ICE',sub:'CLEARED GROUND IS SLIPPERY',mod:{blackice:1,value:2},prize:{gems:60},col:'#7ad3ff'},
  goldrush:{name:'GOLD RUSH',sub:'GOLDEN SNOW PAYS 5X',mod:{goldsnow:1},prize:{gems:60},col:'#ffd23f'},
  snowball:{name:'SNOWBALL FIGHT',sub:'KIDS EVERYWHERE, BONK THEM',mod:{throwers:1,value:1.5},prize:{gems:60},col:'#ff8fb0'},
  yeti:{name:'YETI HUNT',sub:'A YETI IS ON YOUR TAIL',mod:{yeti:1,value:2},prize:{gems:60},col:'#9fd8ff'},
  stars:{name:'SHOOTING STARS',sub:'CATCH FALLING STARS',mod:{stars:1},prize:{gems:60},col:'#ffef7a'},
  snowday:{name:'SNOW DAY',sub:'GIANT BLADE, 3X SNOWFALL',mod:{bigblade:1,snow:3,value:1.5},prize:{gems:60},col:'#ffffff'},
  hail:{name:'HAILSTORM',sub:'DODGE THE HAIL',mod:{hail:1,value:2},prize:{gems:60},col:'#c6d0e0'},
  timeattack:{name:'TIME ATTACK',sub:'HALF TIME, TRIPLE COINS',mod:{half:1,value:3,clocks:1},prize:{gems:60},col:'#7fe08a'}};
const EV_FLAGS=['night','fog','blackice','goldsnow','throwers','yeti','stars','bigblade','hail','clocks','mud','slush','thinice','cannons'];
const PROTO=new URLSearchParams(location.search).has('lab')||/^lab\\./.test(location.hostname)||/\\.vercel\\.app$/.test(location.hostname);
const TWISTS={farm:{k:'mud',name:'MUD',sub:'THAWED MUD SLOWS YOU DOWN',tip:['MUD!','IT SLOWS YOU DOWN'],col:'#c98d4a'},
  city:{k:'slush',name:'SLUSH SPRAY',sub:'CARS SPRAY SLUSH ON YOUR LANES',tip:['SLUSH SPRAY!','CARS MESS UP YOUR LANES'],col:'#c6d0e0'},
  themepark:{k:'night',name:'AFTER DARK',sub:'NIGHT JOBS, HEADLIGHTS ON',tip:['AFTER DARK!','FOLLOW YOUR HEADLIGHTS'],col:'#ffd23f'},
  harbour:{k:'thinice',name:'THIN ICE',sub:'DON\\'T STOP ON THE ICE',tip:['THIN ICE!','KEEP MOVING ON THE ICE'],col:'#7ad3ff'},
  ski:{k:'cannons',name:'SNOWMAKING',sub:'CANNONS RE-SNOW THE RUNS',tip:['SNOWMAKING!','JAM THE CANNONS'],col:'#f4f8ff'},
  pass:{k:'wind',name:'WINDY PASS',sub:'MILD GUSTS PUSH YOU',tip:['WINDY!','HOLD ON IN THE GUSTS'],col:'#9fd8ff'},
  north:{k:'fog',name:'WHITEOUT',sub:'YOU ONLY SEE AROUND YOU',tip:['WHITEOUT!','YOU ONLY SEE NEAR YOU'],col:'#e8f0ff'}};
function areaJobs(a){const o=[];LEVELS.forEach((L,i)=>{if(L.area===a&&!L.tool&&!L.boss)o.push(i);});return o;}
function twistJobs(a){return areaJobs(a).filter((i,k)=>k===1||(k>1&&(k-1)%4===0));}
function twistOf(idx){if(!PROTO)return null;const L=LEVELS[idx],T=L&&TWISTS[L.area];return T&&twistJobs(L.area).includes(idx)?L.area:null;}""")

# lab events: every kind available at once, the map banner shows the one you last picked
rep("function evNow(){const t=Date.now();return EVENTS.find(e=>t>=e.start&&t<e.end)||null;}",
    "if(PROTO){const t=Date.now();for(const k in EVENT_DEFS)EVENTS.push({id:'lab-'+k,kind:k,start:t-1000,end:t+72*3600e3,test:true,lab:true});}\n"
    "let labOpen=false,labPick=null,labKind=null,labReopen=false,labTab=0;\n"
    "function evNow(){if(PROTO)return EVENTS.find(e=>e.lab&&e.kind===labKind)||null;const t=Date.now();return EVENTS.find(e=>t>=e.start&&t<e.end)||null;}")

# build: event mods + area twists
rep("  LEVELS[idx]=c;try{return buildLevel(idx);}finally{LEVELS[idx]=L;}}",
    "  if(m.half)c.time=Math.round(L.time*0.5);for(const k of EV_FLAGS)if(m[k])c['ev_'+k]=1;\n"
    "  LEVELS[idx]=c;try{const g=buildLevel(idx);evPost(g,m);return g;}finally{LEVELS[idx]=L;}}")
rep("function evBuild(idx,opts){const ev=opts&&opts.event?EVENTS.find(e=>e.id===opts.event):null;if(!ev)return buildLevel(idx);",
    "function evBuild(idx,opts){const ev=opts&&opts.event?EVENTS.find(e=>e.id===opts.event):null;\n"
    "  if(!ev){const ta=(opts&&opts.twist)||twistOf(idx);if(!ta)return buildLevel(idx);const T=TWISTS[ta],L=LEVELS[idx],c=Object.assign({},L);c.twist=ta;\n"
    "    if(T.k==='wind'){c.gust=1;c.gustMild=1;}else if(T.k==='fog'){c.ev_fog=1;c.fogMild=1;}else c['ev_'+T.k]=1;\n"
    "    LEVELS[idx]=c;try{const g=buildLevel(idx);evPost(g,{[T.k]:1});return g;}finally{LEVELS[idx]=L;}}")

# gold snow / mud patches show in the snow; clearing gold pays 5x
rep("c=snowCol(px,py,g.mark[i]&&sy===1,SNOW,SNOW2,g);",
    "c=snowCol(px,py,g.mark[i]&&sy===1,SNOW,SNOW2,g);if(g.gold&&g.gold[i])c=((px+py*3)%5?[255,222,110]:[255,244,190]);else if(g.mud&&g.mud[i])c=((px*3+py)%4?[214,200,182]:[190,172,150]);")
rep("function clearCell(i,acc){if(G.type[i]===T_BLOCK)return;const d=G.depth[i];if(d>0.03){acc.got+=d;if(d>0.3)acc.cnt++;if(d>0.6)acc.fresh++;setDepth(G,i,0);}}",
    "function clearCell(i,acc){if(G.type[i]===T_BLOCK)return;const d=G.depth[i];if(d>0.03){acc.got+=d;if(G.gold&&G.gold[i]){acc.gold=(acc.gold||0)+d;G.gold[i]=0;}if(d>0.3)acc.cnt++;if(d>0.6)acc.fresh++;setDepth(G,i,0);}}")
rep("if(got>0){const coins=got*cellVal*comboMult;",
    "if(acc.gold>0.2){if(Math.random()<0.6)particles.push({x:P.x+rnd(-8,8),y:P.y+rnd(-8,4),vx:rnd(-24,24),vy:rnd(-34,-10),z:4,vz:rnd(20,40),life:0.6,t:0,kind:'coin'});if(acc.gold>0.6)sfx('coin',0,{vol:0.35});}\n"
    "  if(got>0){const coins=(got+4*(acc.gold||0))*cellVal*comboMult;")

# movement: snow day is faster; black ice and mud
rep("const gust=!!(run.bz&&run.bz.phase==='blow'),full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1);",
    "const gust=!!(run.bz&&run.bz.phase==='blow'),onMud=!!(G.mud&&G.mud[(clamp(Math.floor(P.y/2),0,G.rows-1))*G.cols+clamp(Math.floor(P.x/2),0,G.cols-1)]),"
    "full=moveSpeed()*(run.boost?BOOST_SPEED:1)*(gust?0.8:1)*(G.def.ev_bigblade?1.2:1)*(onMud?0.55:1);"
    "if(onMud&&Math.hypot(P.vx,P.vy)>8&&Math.random()<dt*14)particles.push({x:P.x+rnd(-6,6),y:P.y+rnd(-2,4),vx:rnd(-30,30),vy:rnd(-20,5),z:2,vz:rnd(15,35),life:0.5,t:0,kind:'mud'});")
rep("onIce=G.type[fi]===T_ICE&&G.depth[fi]<CLEAR_T;","onIce=(G.type[fi]===T_ICE||!!G.def.ev_blackice)&&G.depth[fi]<CLEAR_T;")
rep("case 'flame':","case 'mud':R(b,px,py,2,2,k<0.5?'#7a5634':'#9a7450');break;\n      case 'flame':")
rep("function bladeCells(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()||t.ride?0:mLv(t.id).size))));}",
    "function bladeCells(t){t=t||tool();const big=state==='play'&&G&&G.def&&G.def.ev_bigblade?1.7:1;return Math.min(80*big,Math.round(t.width*big*(1+mspec(t.id).sizePer*(chal()||t.ride?0:mLv(t.id).size))));}")

# mild wind for the Pass twist
rep("str=52/(1+Math.max(0,hw-6)/18)*ramp*gs","str=52*(G.def.gustMild?0.55:1)/(1+Math.max(0,hw-6)/18)*ramp*gs")
rep("if(z.t<=0){z.phase='calm';z.t=rnd(4.5,7);}","if(z.t<=0){z.phase='calm';z.t=G.def.gustMild?rnd(7,10):rnd(4.5,7);}")
rep("addFloat(G.pw/2,P.y-34,'BLIZZARD!'","addFloat(G.pw/2,P.y-34,G.def.gustMild?'WINDY!':'BLIZZARD!'")

# per-frame event / twist logic
rep("  // snowfall\n","  if(G.def.ev_stars||G.def.ev_hail||G.clocks||G.def.ev_slush||G.def.ev_thinice||G.def.twist)evTick(dt,tid);\n  // snowfall\n")
# drawing: event objects, night and fog
rep("if(G.night)b.drawImage(G.night,0,cy,W,VIEW_H,0,cy,W,VIEW_H);",
    "evDraw(cy);if(G.night){if(G.def.ev_night)drawNightEv(cy);else b.drawImage(G.night,0,cy,W,VIEW_H,0,cy,W,VIEW_H);}if(G.def.ev_fog)drawFogEv(cy);")
# lab screen
rep("function overlayOpen(){return !!(ridePeek||","function overlayOpen(){return !!(labOpen||ridePeek||")
rep("if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();","if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();\n  if(PROTO&&state==='map')drawLab();")

rep("function sprAlpha(c){",r"""// ---------------- PROTOTYPE: events + area twists (Nov 19) ----------------
function evFree(g,x,y,r){for(let dy=-r;dy<=r;dy+=2)for(let dx=-r;dx<=r;dx+=2){const cx=(x+dx)>>1,cy=(y+dy)>>1;if(cx<0||cy<0||cx>=g.cols||cy>=g.rows)return false;if(g.type[cy*g.cols+cx]===T_BLOCK)return false;}return true;}
function evSpots(g,n,r,y0,seed){const out=[],rn=srng(seed||7);for(let k=0;k<n*60&&out.length<n;k++){const band=(out.length+0.5)/n,y=Math.round(y0+(g.ph-y0-20)*(band+(rn()-0.5)/n)),x=Math.round(14+rn()*(g.pw-28));
  if(y<y0||y>g.ph-12||!evFree(g,x,y,r)||out.some(p=>Math.hypot(p.x-x,p.y-y)<r*3))continue;out.push({x,y});}return out;}
function evMask(g,pts,rmin,rvar){const m=new Uint8Array(g.cols*g.rows);for(const p of pts){const r=rmin+((p.x*7+p.y)%rvar);for(let cy=Math.max(0,(p.y-r)>>1);cy<=Math.min(g.rows-1,(p.y+r)>>1);cy++)for(let cx=Math.max(0,(p.x-r)>>1);cx<=Math.min(g.cols-1,(p.x+r)>>1);cx++){const dx=cx*2+1-p.x,dy=cy*2+1-p.y;if(dx*dx+dy*dy<=r*r&&g.type[cy*g.cols+cx]!==T_BLOCK)m[cy*g.cols+cx]=1;}}return m;}
function evRepaint(g){for(let cy=0;cy<g.rows;cy++)for(let cx=0;cx<g.cols;cx++)paintCell(g,cx,cy);for(const t of g.tiles)t.x.putImageData(g.img,0,-t.y0,0,t.y0,g.pw,t.h);if(g.dB)g.dB.clear();g.dirty=null;}
function evBlock(g,x,y,w,h){for(let cy=Math.max(0,Math.floor(y/2));cy<Math.min(g.rows,Math.ceil((y+h)/2));cy++)for(let cx=Math.max(0,Math.floor(x/2));cx<Math.min(g.cols,Math.ceil((x+w)/2));cx++){const i=cy*g.cols+cx;if(g.type[i]===T_BLOCK)continue;const bd=Math.floor(cy*2/g.bandH);
  if(!(g.nc&&g.nc[i])){g.clearable--;g.bandTot[bd]--;if(g.depth[i]<CLEAR_T){g.cleared--;g.bandClr[bd]--;}}g.type[i]=T_BLOCK;}}
function evPost(g,m){
  if(m.blackice)for(let k=0;k<g.ground.length;k+=3){g.ground[k]=g.ground[k]*0.45+190*0.55;g.ground[k+1]=g.ground[k+1]*0.45+224*0.55;g.ground[k+2]=g.ground[k+2]*0.45+252*0.55;}
  if(m.goldsnow)g.gold=evMask(g,evSpots(g,Math.max(4,Math.round(g.ph/230)),10,g.start.y+30,g.ph),10,7);
  if(m.mud){const pts=evSpots(g,Math.max(4,Math.round(g.ph/200)),9,g.start.y+40,g.ph*7+1);g.mud=evMask(g,pts,9,8);for(let i=0;i<g.mud.length;i++)if(g.mud[i]){const cx=i%g.cols,cy=(i/g.cols)|0;for(let sy=0;sy<2;sy++)for(let sx=0;sx<2;sx++){const o=((cy*2+sy)*g.pw+cx*2+sx)*3,dk=(cx+cy+sx)%3?0:12;g.ground[o]=110-dk;g.ground[o+1]=80-dk;g.ground[o+2]=52-dk;}}}
  if(m.blackice||m.goldsnow||m.mud)evRepaint(g);
  if(m.throwers)for(const p of evSpots(g,Math.max(3,Math.round(g.ph/240)),7,g.start.y+60,g.ph*3+11))g.hazards.push({kind:'thrower',x:p.x-4,y:p.y-5,w:8,h:5,sx:p.x,sy:p.y,state:'idle',cd:rnd(1,3),ball:null,t:0});
  if(m.yeti){const C=CHASERS.yeti;let sp=null;for(let d=40;d<200&&!sp;d+=8)for(const dx of [0,-30,30,-60,60]){const x=clamp(g.start.x+dx,12,g.pw-28),y=g.start.y-d;if(y>8&&evFree(g,x+8,y+4,10)){sp={x,y};break;}}
    if(!sp)for(let d=70;d<220&&!sp;d+=8)for(const dx of [0,-30,30]){const x=clamp(g.start.x+dx,12,g.pw-28),y=g.start.y+d;if(evFree(g,x+8,y+4,10)){sp={x,y};break;}}
    sp=sp||{x:g.start.x,y:Math.max(10,g.start.y-40)};g.hazards.push({kind:'chaser',skin:'yeti',C,x:sp.x,y:sp.y,w:C.w,h:C.h,state:'wait',t:5,map:0,say:3,anim:0,vx:0,vy:0,lunge:null,dir:[0,1]});}
  if(m.clocks)g.clocks=evSpots(g,Math.max(3,Math.round(g.ph/380)),6,g.start.y+40,g.ph*5+3).map(p=>({x:p.x,y:p.y,taken:false}));
  if(m.cannons){const n=Math.max(2,Math.round(g.ph/700));let k=0;for(let y=Math.max(g.start.y+120,160);y<g.ph-60&&k<n;y+=Math.round((g.ph-200)/n)){const left=k%2===0;let x=null;
      if(left){for(let xx=4;xx<g.pw/2;xx+=2)if(evFree(g,xx+9,y+9,9)){x=xx;break;}}else{for(let xx=g.pw-22;xx>g.pw/2;xx-=2)if(evFree(g,xx+9,y+9,9)){x=xx;break;}}
      if(x==null)continue;const ang=left?0.15:Math.PI-0.15,spr=cannonSprite(ang),fz=frostOf(spr),o={spr:fz,src:spr,sx:x,sy:y-(fz.padTop||0),x:x+2,y:y+8,w:14,h:9,bld:false};o.base=o.y+o.h;g.obstacles.push(o);evBlock(g,o.x,o.y,o.w,o.h);
      g.hazards.push({kind:'cannon',x,y,w:18,h:18,ang,per:5.5,range:70,t:rnd(1.5,3),state:'idle',jam:0,immune:0,acc:0,mx:x+9+Math.cos(ang)*8,my:y+9+Math.sin(ang)*8,ob:o});k++;}}
  if(m.night)evNight(g);}
function evNight(g){const Ls=g.lights.slice(),D=g.def.data||{};for(const p of D.props||[])if(['lamp','lantpost','stonelamp','lighthouse','tlight'].includes(p[0]))Ls.push({x:p[1]+4,y:p[2]+4,r:p[0]==='lighthouse'?44:30});
  for(const o of g.scenery.concat(g.obstacles))if(o.spr.width>=40&&o.spr.height>=30&&!o.wild)Ls.push({x:Math.round(o.sx+o.spr.width/2),y:Math.round(o.base-4),r:16,c:'#ffd890'});
  const oc=mk(g.pw,g.ph),o=oc.getContext('2d');o.fillStyle='rgba(8,12,36,0.8)';o.fillRect(0,0,g.pw,g.ph);o.globalCompositeOperation='destination-out';
  for(const l of Ls)for(const f of [1,0.72,0.48]){o.fillStyle='rgba(0,0,0,0.33)';pixCircle(o,Math.round(l.x),Math.round(l.y),Math.round(l.r*f));}
  o.globalCompositeOperation='source-over';for(const l of Ls){o.fillStyle=l.c?hexA(l.c,0.16):'rgba(255,205,110,0.16)';pixCircle(o,Math.round(l.x),Math.round(l.y),Math.round(l.r*0.7));}g.night=oc;}
let NB=null,FB=null;
function drawNightEv(cy){if(!NB)NB=mk(W,VIEW_H);const x=NB.getContext('2d');x.globalCompositeOperation='source-over';x.clearRect(0,0,W,VIEW_H);x.drawImage(G.night,0,cy,W,VIEW_H,0,0,W,VIEW_H);
  x.globalCompositeOperation='destination-out';const px=P.x,py=P.y-cy,fv=[[0,-1],[1,0],[0,1],[-1,0]][P.f];
  for(let k=0;k<9;k++){const d=8+k*10,r=6+k*3.2;x.fillStyle='rgba(0,0,0,'+(0.55-k*0.04).toFixed(2)+')';pixCircle(x,Math.round(px+fv[0]*d),Math.round(py+fv[1]*d),Math.round(r));}
  x.fillStyle='rgba(0,0,0,0.6)';pixCircle(x,Math.round(px),Math.round(py),14);x.globalCompositeOperation='source-over';x.fillStyle='rgba(255,240,180,0.09)';
  for(let k=2;k<9;k+=2){const d=8+k*10,r=6+k*3.2;pixCircle(x,Math.round(px+fv[0]*d),Math.round(py+fv[1]*d),Math.round(r*0.8));}b.drawImage(NB,0,cy);}
function drawFogEv(cy){if(!FB)FB=mk(W,VIEW_H);const x=FB.getContext('2d'),mild=!!G.def.fogMild;x.globalCompositeOperation='source-over';x.clearRect(0,0,W,VIEW_H);x.fillStyle=mild?'rgba(232,240,252,0.86)':'rgba(232,240,252,0.95)';x.fillRect(0,0,W,VIEW_H);
  for(let k=0;k<14;k++){const yy=(k*41+Math.floor(tNow*8))%VIEW_H,xx=((k*67+tNow*14)%(W+60))-30;x.fillStyle='rgba(255,255,255,0.5)';x.fillRect(Math.round(xx),yy,40,3);}
  x.globalCompositeOperation='destination-out';const px=Math.round(P.x),py=Math.round(P.y-cy),s2=mild?1.3:1;for(const [r,a] of [[68,0.25],[58,0.3],[48,0.35],[38,0.5],[28,0.9]]){x.fillStyle='rgba(0,0,0,'+a+')';pixCircle(x,px,py,Math.round(r*s2));}b.drawImage(FB,0,cy);}
function evTick(dt,tid){
  if(G.def.twist&&!run.twTip){run.twTip=1;const T=TWISTS[G.def.twist];if(T&&T.k!=='wind'){addFloat(G.pw/2,P.y-34,T.tip[0],T.col,2.4);addFloat(G.pw/2,P.y-25,T.tip[1],'#ffffff',2.4);}}
  if(G.def.ev_stars){run.stars=run.stars||[];run.starT=(run.starT==null?2:run.starT)-dt;if(run.starT<=0&&run.stars.length<4){run.starT=rnd(2.2,3.6);for(let k=0;k<12;k++){const x=Math.round(rnd(16,G.pw-16)),y=Math.round(clamp(camY+rnd(40,VIEW_H-40),20,G.ph-20));if(evFree(G,x,y,4)){run.stars.push({x,y,t:0});break;}}}
    for(const s2 of run.stars){s2.t+=dt;if(s2.t>=1.1&&!s2.landed){s2.landed=1;particles.push({x:s2.x,y:s2.y,vx:0,vy:0,z:0,vz:0,life:0.35,t:0,kind:'ring',r:9});sfx('tick',0,{rate:1.6,vol:0.5});}
      if(s2.landed&&!s2.got&&Math.hypot(P.x-s2.x,P.y-s2.y)<12){s2.got=1;if((run.starGem||0)<5){run.starGem=(run.starGem||0)+1;save.gems=(save.gems||0)+1;addFloat(s2.x,s2.y-12,'+1 GEM','#ff8fc8',1.1);}
        else{const c=Math.round(BASE_CELL_VALUE*G.def.value*valueMult()*30);earn(c);addFloat(s2.x,s2.y-12,'STAR'+cplus(c),'#ffef7a',1.1);}sfx('gift');for(let k=0;k<8;k++)particles.push({x:s2.x,y:s2.y,vx:rnd(-40,40),vy:rnd(-40,10),z:3,vz:rnd(20,50),life:0.5,t:0,kind:'coin'});}}
    run.stars=run.stars.filter(s2=>!s2.got&&s2.t<8.1);}
  if(G.def.ev_hail){run.hail=run.hail||[];run.hailT=(run.hailT==null?2.5:run.hailT)-dt;if(run.hailT<=0){run.hailT=rnd(1.6,2.8);const n=Math.random()<0.5?2:1;for(let k=0;k<n;k++)run.hail.push({x:Math.round(clamp(P.x+rnd(-55,55),10,G.pw-10)),y:Math.round(clamp(P.y+rnd(-70,40),10,G.ph-10)),t:0,r:9});}
    for(const h of run.hail){h.t+=dt;if(h.t>=1.3&&!h.hit){h.hit=1;shake=Math.max(shake,0.08);sfx('crunch',0,{vol:0.6});for(let k=0;k<10;k++)particles.push({x:h.x,y:h.y,vx:rnd(-50,50),vy:rnd(-40,20),z:2,vz:rnd(20,45),life:0.45,t:0,kind:'snow'});
      if(tid!=='ufo'&&P.inv<=0&&Math.hypot(P.x-h.x,P.y-h.y)<h.r+4){P.stun=Math.max(P.stun,0.7);P.inv=1.2;addFloat(P.x,P.y-24,'BONK! HAIL','#c6d9f3',0.9);buzz(30);}}}
    run.hail=run.hail.filter(h=>h.t<1.7);}
  if(G.clocks)for(const c of G.clocks)if(!c.taken&&Math.hypot(P.x-c.x,P.y-c.y)<12){c.taken=true;run.time+=5;addFloat(c.x,c.y-12,'+5 SECONDS','#9fd8ff',1.2);sfx('time');}
  if(G.def.ev_slush){run.slT=(run.slT||0)-dt;if(run.slT<=0){run.slT=0.12;for(const hz of G.hazards){const on=hz.y+60>camY&&hz.y-60<camY+VIEW_H;if(!on)continue;
      if(hz.kind==='taxi'){const yy=hz.y+hz.h/2;for(const sx of [hz.x-3,hz.x+hz.w+3])if(sx>2&&sx<G.pw-2&&yy>2&&yy<G.ph-2){addSnowCircle(G,sx,yy,4,0.35);if(Math.random()<0.4)particles.push({x:sx,y:yy,vx:(sx<hz.x?-1:1)*rnd(30,60),vy:rnd(-10,10),z:3,vz:rnd(10,30),life:0.4,t:0,kind:'snow'});}}
      else if(hz.kind==='cross'&&hz.state==='go'){const xx=hz.x+hz.w/2;for(const sy of [hz.y-3,hz.y+hz.h+3])if(xx>2&&xx<G.pw-2&&sy>2&&sy<G.ph-2)addSnowCircle(G,xx,sy,4,0.35);}}}}
  if(G.def.ev_thinice){const fi=(clamp(Math.floor(P.y/2),0,G.rows-1))*G.cols+clamp(Math.floor(P.x/2),0,G.cols-1),ice=G.type[fi]===T_ICE&&G.depth[fi]<CLEAR_T,slow=Math.hypot(P.vx,P.vy)<10;
    run.crk=ice&&slow&&!(P.stun>0)?(run.crk||0)+dt:Math.max(0,(run.crk||0)-dt*2);if(run.crk>0.5&&!run.crkWarn){run.crkWarn=1;addFloat(P.x,P.y-26,'CRACK... MOVE!','#7ad3ff',0.9);sfx('tick',0,{rate:0.7});}
    if(run.crk<0.2)run.crkWarn=0;if(run.crk>1.4){run.crk=0;run.crkWarn=0;P.stun=1.1;P.inv=1.6;shake=0.2;sfx('splat');addFloat(P.x,P.y-26,'SPLOOSH!','#7ad3ff',1.1);buzz(40);for(let k=0;k<16;k++)particles.push({x:P.x,y:P.y,vx:rnd(-50,50),vy:rnd(-40,20),z:2,vz:rnd(25,55),life:0.6,t:0,kind:'snow'});}}}
function evDraw(cy){
  if(G.gold){const t=Math.floor(tNow*6);for(let k=0;k<40;k++){const i=(Math.imul(k*977+t*131,2654435761)>>>0)%G.gold.length;if(!G.gold[i]||G.depth[i]<0.3)continue;const x=(i%G.cols)*2,y=((i/G.cols)|0)*2;if(y<cy-4||y>cy+VIEW_H+4)continue;R(b,x,y-1,1,3,'#ffffff');R(b,x-1,y,3,1,'#ffffff');R(b,x,y,1,1,'#ffd23f');}}
  if(G.def.ev_thinice&&run.crk>0.1){const k=Math.min(1,run.crk/1.4),px=Math.round(P.x),py=Math.round(P.y);for(let a=0;a<6;a++){const an=a*1.05+0.3,len=Math.round(4+k*14);for(let d=3;d<len;d+=2)R(b,Math.round(px+Math.cos(an)*d+Math.sin(d*0.7)*1.2),Math.round(py+Math.sin(an)*d*0.7),1,1,'rgba(40,70,120,0.85)');}}
  if(G.clocks)for(const c of G.clocks)if(!c.taken&&c.y>cy-20&&c.y<cy+VIEW_H+20){const bob=Math.floor(tNow*3+c.x)%2;R(b,c.x-4,c.y+3,9,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.watch,c.x-4,c.y-6-bob);if(Math.floor(tNow*2+c.x)%3===0){R(b,c.x+4,c.y-9,1,3,'#ffffff');R(b,c.x+3,c.y-8,3,1,'#ffffff');}}
  if(run.hail)for(const h of run.hail){const k=Math.min(1,h.t/1.3);if(!h.hit){b.fillStyle='rgba(216,54,75,'+(0.16+0.22*k).toFixed(2)+')';pixCircle(b,h.x,h.y,Math.round(h.r*(1.4-0.4*k)));
      for(let a=0;a<16;a++){const an=a/16*Math.PI*2;R(b,Math.round(h.x+Math.cos(an)*h.r),Math.round(h.y+Math.sin(an)*h.r*0.8),1,1,'#ff4a5a');}const hy=Math.round(h.y-(1-k)*90);R(b,h.x-2,hy-2,5,5,K);R(b,h.x-1,hy-1,3,3,'#e8f4ff');R(b,h.x-1,hy-1,1,1,'#ffffff');}
    else{R(b,h.x-3,h.y-1,7,3,'#c6d9f3');R(b,h.x-2,h.y-2,5,1,'#ffffff');}}
  if(run.stars)for(const s2 of run.stars){if(!s2.landed){const k=s2.t/1.1,sx=Math.round(s2.x+(1-k)*40),sy=Math.round(s2.y-(1-k)*110);b.fillStyle='rgba(255,239,122,'+(0.15+0.3*k).toFixed(2)+')';pixCircle(b,s2.x,s2.y,Math.round(3+5*k));
      for(let q=1;q<6;q++)R(b,sx+q*3,sy-q*7,2,2,'rgba(255,239,122,'+(0.6-q*0.1).toFixed(2)+')');b.drawImage(SPR.bigStar,sx-4,sy-4);}
    else if(!(s2.t>6.5&&Math.floor(tNow*8)%2===0)){const bob=Math.floor(tNow*4+s2.x)%2;R(b,s2.x-4,s2.y+4,9,2,'rgba(27,31,59,0.22)');b.drawImage(SPR.bigStar,s2.x-4,s2.y-6-bob);if(Math.floor(tNow*3+s2.x)%2===0){R(b,s2.x+5,s2.y-9,1,3,'#ffffff');R(b,s2.x+4,s2.y-8,3,1,'#ffffff');}}}}
// ---- the lab screen ----
const LAB_JOBS={blizzard:['maple','lot','lane','switchbacks'],presents:['maple','village','parade','northpole'],nightshift:['maple','lot','carousel','quay'],whiteout:['lane','skischool','summit','icefield'],
  blackice:['culdesac','pond','icerink','frozenlake'],goldrush:['gardens','village','street','mainst'],snowball:['school','playground','shops','games'],yeti:['park','farmyard','mansion','chalets'],
  stars:['orchard','airport','lighthouse','aurora'],snowday:['driveway','highst','stadium','bluerun'],hail:['retreat','cityhall','containers','hairpin'],timeattack:['gardens','lot','food','gullisland']};
const LAB_TXT={blizzard:['GUSTS SHOVE YOUR PLOW SIDEWAYS.','SQUALLS DUMP SNOW. COINS X2.'],presents:['FOUR TIMES THE PRESENTS.','DIG THEM OUT FOR TREATS.'],nightshift:['IT IS DARK. YOUR HEADLIGHTS','AND THE LAMPS LIGHT THE WAY.','COINS X2.'],
  whiteout:['THICK FOG: YOU ONLY SEE','AROUND YOUR PLOW. COINS X2.'],blackice:['EVERYTHING YOU CLEAR TURNS','TO ICE. YOU SLIDE! COINS X2.'],goldrush:['GOLDEN SNOW PATCHES PAY 5X.','GET THEM FIRST.'],
  snowball:['KIDS EVERYWHERE THROW SNOWBALLS.','PLOW INTO THEM TO SNOW THEM IN.','COINS X1.5.'],yeti:['A YETI CHASES YOU ALL JOB.','KEEP MOVING! COINS X2.'],stars:['STARS FALL FROM THE SKY.','DRIVE OVER THEM: 5 GEMS A JOB,','THEN COINS.'],
  snowday:['GIANT BLADE, FASTER PLOW,','BUT SNOW FALLS 3X AS FAST.','COINS X1.5.'],hail:['HAIL LANDS IN THE RED RINGS.','DODGE IT OR GET DAZED. X2.'],timeattack:['HALF THE TIME, TRIPLE COINS.','CLOCKS ADD 5 SECONDS.']};
function labStart(i,opts,kind){labOpen=false;labReopen=true;if(kind)labKind=kind;sfx('go');startLevelUI(i,opts);}
function drawLab(){if(labReopen&&!overlayOpen()&&!pendingStart){labReopen=false;labOpen=true;}
  if(!labOpen){if(!overlayOpen())button('labbtn',W-36,MAP_VY+3,32,14,'purple','LAB',()=>{labOpen=true;sfx('click');});return;}
  b.fillStyle='rgba(11,24,56,0.86)';b.fillRect(0,0,W,H);panel(6,22,168,282,'#13306b','#c4a0f5');
  if(labPick==null){text(b,'PROTOTYPE LAB',W/2,29,'#c4a0f5',{align:'center',scale:2});
    button('labt0',14,44,74,14,labTab===0?'purple':'navy','EVENTS',()=>{labTab=0;sfx('click');});button('labt1',92,44,74,14,labTab===1?'purple':'navy','AREA TWISTS',()=>{labTab=1;sfx('click');});
    const rows=labTab===0?Object.keys(EVENT_DEFS).map(k=>({k,d:EVENT_DEFS[k]})):Object.keys(TWISTS).map(a=>({k:'tw:'+a,d:TWISTS[a]}));
    rows.forEach((r,n)=>{const y=62+n*18;card(12,y,156,16,'#eef3fb',r.d.col);text(b,r.d.name,18,y+3,'#13306b',{outline:null});text(b,r.d.sub,18,y+9,'#5a6b8c',{outline:null});btn('labr'+n,12,y,156,16,()=>{labPick=r.k;sfx('click');});});
    button('labclose',62,286,56,14,'grey','CLOSE',()=>{labOpen=false;sfx('click');});return;}
  const tw=labPick.startsWith('tw:'),a=tw?labPick.slice(3):null,d=tw?TWISTS[a]:EVENT_DEFS[labPick];
  text(b,d.name,W/2,30,d.col,{align:'center',scale:2});text(b,tw?'AREA TWIST: '+a.toUpperCase():'EVENT',W/2,46,'#9fc0e8',{align:'center',outline:null});
  const lines=tw?[d.sub+'.',a==='pass'?'MILDER THAN THE BLIZZARD.':'ON ABOUT 1 IN 4 '+a.toUpperCase()+' JOBS.','THE FIRST ONE TEACHES IT.']:LAB_TXT[labPick]||[d.sub];
  lines.forEach((l,n)=>text(b,l,W/2,58+n*9,'#ffffff',{align:'center',outline:null}));
  text(b,'PICK A JOB',W/2,94,'#ffd23f',{align:'center',outline:null});
  const jobs=tw?twistJobs(a):(LAB_JOBS[labPick]||[]).map(id=>LEVELS.findIndex(L=>L.id===id)).filter(i=>i>=0);
  jobs.slice(0,4).forEach((i,n)=>{const L=LEVELS[i],y=104+n*30;card(14,y,152,26,'#eef3fb','#9fc0e8');text(b,L.name,20,y+5,'#13306b',{outline:null});text(b,(AREAS&&AREAS[L.area]&&AREAS[L.area].name)||L.area.toUpperCase(),20,y+14,'#5a6b8c',{outline:null});
    button('labj'+n,124,y+5,38,16,'green','PLAY',()=>labStart(i,tw?{twist:a}:{event:'lab-'+labPick},tw?null:labPick));});
  button('labback',14,286,70,14,'grey','BACK',()=>{labPick=null;sfx('click');});button('labx',96,286,70,14,'grey','CLOSE',()=>{labOpen=false;sfx('click');});}
function sprAlpha(c){""")

# analytics: lab plays are tagged build=lab so they never mix with tester numbers (dashboard filters non-live builds)
rep("build:DEV_MODE?'dev':REVIEW_MODE?'review':'live'","build:DEV_MODE?'dev':(new URLSearchParams(location.search).has('lab')||/^lab\\./.test(location.hostname)||/\\.vercel\\.app$/.test(location.hostname))?'lab':REVIEW_MODE?'review':'live'",2)

open(f,'w',encoding='utf-8').write(s)
print('p143 prototype lab: 10 new events + 7 area twists (only with ?lab or on a vercel preview)')
