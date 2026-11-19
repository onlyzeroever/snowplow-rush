import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# LAB rev 2 (Alex, Nov 19 19:38: "these LTMs are an ok start, but need massively improving ... go all out").
# Replaces the first lab (p143). Every mode now changes WHAT YOU DO, shows its rule up front, and pays out loudly.
# Still OFF in the live game: only with ?lab in the URL or on the lab preview (lab.snowplowrush.app / *.vercel.app).
#  - Area twists (one per area, teach-first): Round-Up (farm), Dig-Out (city), Power Cut (theme park), Thin Ice (harbour),
#    Slalom (ski), Avalanche (pass), Lost Penguins (north).
#  - Weekend events: Blizzard, Present Hunt (as live) + Gold Rush, Yeti Hunt, Snowball Roll, Black Ice, Snow Day,
#    Time Attack, Snowball Fight, Star Shower.
#  - Plow sizes: NEW / OLD switch on the lab screen (p153).

# ---- event defs, lab switch, twists ----
rep("  presents:{name:'PRESENT HUNT',sub:'PRESENTS EVERYWHERE',mod:{presents:4},prize:{trail:'sparkle',gems:60},col:'#ff8fc8'}};",
"""  presents:{name:'PRESENT HUNT',sub:'PRESENTS EVERYWHERE',mod:{presents:4},prize:{trail:'sparkle',gems:60},col:'#ff8fc8'},
  goldrush:{name:'GOLD RUSH',sub:'RACE TO THE GOLD NUGGETS',mod:{mode:'goldrush'},prize:{gems:60},col:'#ffd23f'},
  yetihunt:{name:'YETI HUNT',sub:'CATCH THE PRESENT THIEF',mod:{mode:'yetihunt',value:1.5},prize:{gems:60},col:'#9fd8ff'},
  snowroll:{name:'SNOWBALL ROLL',sub:'GROW A GIANT SNOWBALL',mod:{mode:'snowroll'},prize:{gems:60},col:'#ffffff'},
  blackice:{name:'BLACK ICE',sub:'SLIDE, DRIFT, SCORE',mod:{mode:'blackice',value:1.5},prize:{gems:60},col:'#7ad3ff'},
  snowday:{name:'SNOW DAY',sub:'MEGA BLADE, MOUNTAINS OF SNOW',mod:{mode:'snowday',snow:2.5,value:1.5},prize:{gems:60},col:'#e8f0ff'},
  timeattack:{name:'TIME ATTACK',sub:'HALF TIME, CHASE THE CLOCKS',mod:{mode:'timeattack',value:3,half:1},prize:{gems:60},col:'#7fe08a'},
  forts:{name:'SNOWBALL FIGHT',sub:'SMASH THE SNOW FORTS',mod:{mode:'forts',value:1.5},prize:{gems:60},col:'#ff8fb0'},
  stars:{name:'STAR SHOWER',sub:'CATCH THE FALLING STARS',mod:{mode:'stars'},prize:{gems:60},col:'#ffef7a'}};
const PROTO=new URLSearchParams(location.search).has('lab')||/^lab\\./.test(location.hostname)||/\\.vercel\\.app$/.test(location.hostname);
const TWISTS={farm:'roundup',city:'digout',themepark:'powercut',harbour:'thinice',ski:'slalom',pass:'avalanche',north:'penguins'};
const TW_JOBS={harbour:['quay','drawbridge','locks','icebreaker']};   // thin ice needs a frozen harbour: skip the jobs with no ice
const TW_ALSO={roundup:['park','icefield'],digout:['maple','village'],powercut:['maple','cityhall'],thinice:['pond','frozenlake'],slalom:['sledhill','summit'],avalanche:['bluerun','aurora'],penguins:['gardens','quay']};
function areaJobs(a){const o=[];LEVELS.forEach((L,i)=>{if(L.area===a&&!L.tool&&!L.boss)o.push(i);});return o;}
function twistJobs(a){if(TW_JOBS[a])return TW_JOBS[a].map(id=>LEVELS.findIndex(L=>L.id===id)).filter(i=>i>=0);return areaJobs(a).filter((i,k)=>k===1||(k>1&&(k-1)%4===0));}
function twistOf(idx){if(!PROTO||new URLSearchParams(location.search).has('notwist'))return null;const L=LEVELS[idx];return L&&TWISTS[L.area]&&twistJobs(L.area).includes(idx)?L.area:null;}""")

# lab events: every kind available at once; the map banner shows the one you last picked
rep("function evNow(){const t=Date.now();return EVENTS.find(e=>t>=e.start&&t<e.end)||null;}",
    "if(PROTO){const t=Date.now();for(const k in EVENT_DEFS)EVENTS.push({id:'lab-'+k,kind:k,start:t-1000,end:t+72*3600e3,test:true,lab:true});}\n"
    "let labOpen=false,labPick=null,labKind=null,labReopen=false,labTab=0;\n"
    "function evNow(){if(PROTO)return EVENTS.find(e=>e.lab&&e.kind===labKind)||null;const t=Date.now();return EVENTS.find(e=>t>=e.start&&t<e.end)||null;}")

# build: events with a mode, and area twists
rep("  LEVELS[idx]=c;try{return buildLevel(idx);}finally{LEVELS[idx]=L;}}",
    "  if(m.mode)c.mode=m.mode;if(m.half)c.time=Math.round(L.time*0.55);\n"
    "  LEVELS[idx]=c;try{const g=buildLevel(idx);labPost(g);return g;}finally{LEVELS[idx]=L;}}")
rep("function evBuild(idx,opts){const ev=opts&&opts.event?EVENTS.find(e=>e.id===opts.event):null;if(!ev)return buildLevel(idx);",
    "function evBuild(idx,opts){const ev=opts&&opts.event?EVENTS.find(e=>e.id===opts.event):null;\n"
    "  if(!ev){const ta=(opts&&opts.twist)||twistOf(idx),mk2=ta&&TWISTS[ta];if(!mk2)return buildLevel(idx);const L=LEVELS[idx],c=Object.assign({},L);\n"
    "    c.mode=mk2;c.twist=ta;c.teach=twistJobs(ta)[0]===idx;LEVELS[idx]=c;try{const g=buildLevel(idx);labPost(g);return g;}finally{LEVELS[idx]=L;}}")

# per-frame mode logic, drawing layers, screen layer
rep("  // snowfall\n","  if(G.def.mode)labTick(dt,tid);\n  // snowfall\n")
rep("  ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();","  if(G.def.mode)labEnts(ents,top,bot);ents.sort((a,c)=>a.base-c.base);for(const e of ents)e.draw();")
rep("  if(G.night)b.drawImage(G.night,0,cy,W,VIEW_H,0,cy,W,VIEW_H);\n",
    "  {const M=labM();if(G.night){if(M&&M.night)M.night(cy);else b.drawImage(G.night,0,cy,W,VIEW_H,0,cy,W,VIEW_H);}if(M&&M.over)M.over(cy);}\n")
rep("drawBlizzard();drawChaserArrows();drawLeftArrow();drawHUD();","drawBlizzard();drawChaserArrows();drawLeftArrow();if(G.def.mode)labScreen();drawHUD();")
rep("  const got=acc.got,cnt=acc.cnt;","  const got=acc.got,cnt=acc.cnt;run.lastGot=got;")
# lab screen on the map
rep("function overlayOpen(){return !!(ridePeek||","function overlayOpen(){return !!(labOpen||ridePeek||")
rep("if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();","if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();\n  if(PROTO&&state==='map')drawLab();")
# analytics: lab plays are tagged build=lab so they never mix with tester numbers
rep("build:DEV_MODE?'dev':REVIEW_MODE?'review':'live'","build:DEV_MODE?'dev':(new URLSearchParams(location.search).has('lab')||/^lab\\./.test(location.hostname)||/\\.vercel\\.app$/.test(location.hostname))?'lab':REVIEW_MODE?'review':'live'",2)

rep("function sprAlpha(c){",r"""// ================= LAB rev 2: shared mode machinery =================
const MODES={};
function labM(){return G&&G.def&&G.def.mode?MODES[G.def.mode]||null:null;}
function hashS(s){let h=2166136261;for(const ch of String(s)){h^=ch.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;}
// is a rect clear of walls, props, scenery and parked things?
function labRect(g,x,y,w,h){if(x<2||y<2||x+w>g.pw-2||y+h>g.ph-2)return false;
  for(let cy=y>>1;cy<=(y+h-1)>>1;cy++)for(let cx=x>>1;cx<=(x+w-1)>>1;cx++)if(g.type[cy*g.cols+cx]===T_BLOCK)return false;
  for(const o of g.obstacles)if(o.x<x+w&&x<o.x+o.w&&o.y<y+h&&y<o.y+o.h)return false;
  for(const o of g.scenery){const t=o.sy+(o.spr.padTop||0);if(o.sx<x+w&&x<o.sx+o.spr.width&&t<y+h&&y<o.sy+o.spr.height)return false;}
  for(const q of g.hazards)if(['pull','thrower','cannon','barrier'].includes(q.kind)&&q.x<x+w&&x<q.x+(q.w||8)&&q.y<y+h&&y<q.y+(q.h||8))return false;
  return true;}
// a free w x h spot (top-left) in the band [y0,y1); opt: edge (hug a side), margin, avoid:[{x,y,r}], near:{x,y,r0,r1}
function labSpot(g,w,h,y0,y1,rn,opt){opt=opt||{};const m=opt.margin||0;
  for(let k=0;k<240;k++){let x,y;
    if(opt.near){const a=rn()*Math.PI*2,d=opt.near.r0+rn()*(opt.near.r1-opt.near.r0);x=Math.round(opt.near.x+Math.cos(a)*d-w/2);y=Math.round(opt.near.y+Math.sin(a)*d-h/2);}
    else{const xi=opt.xin||6;x=opt.edge?(rn()<0.5?Math.round(4+rn()*16):Math.round(g.pw-w-4-rn()*16)):Math.round(xi+rn()*(g.pw-w-xi*2));y=Math.round(y0+rn()*Math.max(1,y1-y0-h));}
    if(y<y0||y+h>y1)continue;if(opt.avoid&&opt.avoid.some(a=>Math.hypot(a.x-(x+w/2),a.y-(y+h/2))<a.r))continue;
    if(labRect(g,x-m,y-m,w+m*2,h+m*2))return {x,y};}return null;}
function labBands(g,n,skip){const a=[],lo=12,hi=g.ph-12,start=g.start.y,top=start<g.ph/2;for(let k=0;k<n;k++){const f0=k/n,f1=(k+1)/n;let y0=lo+(hi-lo)*f0,y1=lo+(hi-lo)*f1;a.push([Math.round(y0),Math.round(y1)]);}return top?a:a.reverse();}
// repaint a region of the ground after changing g.ground / depths
function labPaint(g,x,y,w,h){const cx0=Math.max(0,x>>1),cx1=Math.min(g.cols-1,(x+w)>>1),cy0=Math.max(0,y>>1),cy1=Math.min(g.rows-1,(y+h)>>1);
  for(let cy=cy0;cy<=cy1;cy++)for(let cx=cx0;cx<=cx1;cx++)paintCell(g,cx,cy);const py0=cy0*2,py1=cy1*2+2;
  for(const t of g.tiles){const a=Math.max(py0,t.y0),z=Math.min(py1,t.y0+t.h);if(z>a)t.x.putImageData(g.img,0,-t.y0,0,a,g.pw,z-a);}}
function labBlock(g,x,y,w,h){for(let cy=Math.max(0,Math.floor(y/2));cy<Math.min(g.rows,Math.ceil((y+h)/2));cy++)for(let cx=Math.max(0,Math.floor(x/2));cx<Math.min(g.cols,Math.ceil((x+w)/2));cx++){const i=cy*g.cols+cx;if(g.type[i]===T_BLOCK)continue;const bd=Math.floor(cy*2/g.bandH);
  if(!(g.nc&&g.nc[i])){g.clearable--;g.bandTot[bd]--;if(g.depth[i]<CLEAR_T){g.cleared--;g.bandClr[bd]--;}}g.type[i]=T_BLOCK;}}
function labNoCount(g,i){if(!g.nc)g.nc=new Uint8Array(g.cols*g.rows);if(g.nc[i]||g.type[i]===T_BLOCK)return;const bd=Math.floor(((i/g.cols)|0)*2/g.bandH);g.clearable--;g.bandTot[bd]--;if(g.depth[i]<CLEAR_T){g.cleared--;g.bandClr[bd]--;}g.nc[i]=1;}
// pay-outs: one unit = 2.5% of the snow on this map, so a bonus feels the same on a small or a huge job
function labUnit(){return Math.max(8,G.clearable/40)*BASE_CELL_VALUE*G.def.value*valueMult();}
function labPay(x,y,u,label,col){const c=Math.max(1,Math.round(labUnit()*u));earn(c);addFloat(x,y,(label||'')+cplus(c),col||'#ffd23f',1.3);
  for(let k=0;k<Math.min(18,6+u*6);k++)particles.push({x,y,vx:rnd(-55,55),vy:rnd(-60,5),z:3,vz:rnd(20,55),life:0.7,t:0,kind:'coin'});sfx('coin');return c;}
function labTime(x,y,s){run.time+=s;addFloat(x,y,'+'+s+' SECONDS','#9fd8ff',1.2);sfx('time');}
function labBurst(x,y,n,kind,sp){for(let k=0;k<n;k++)particles.push({x:x+rnd(-3,3),y:y+rnd(-3,3),vx:rnd(-1,1)*(sp||50),vy:rnd(-1,0.4)*(sp||50),z:2,vz:rnd(15,45),life:rnd(0.4,0.8),t:0,kind:kind||'snow'});}
function labRing(x,y,r){particles.push({x,y,vx:0,vy:0,z:0,vz:0,life:0.4,t:0,kind:'ring',r:r||10});}
function labObj(label,n,of,extra){run.lobj={label,n,of,extra:extra||''};}
// touching something counts with the plow body or the blade (the blade reaches corners the body can't)
function labTouch(tid,r){if(overlap(footprint(tid,P.x,P.y,P.f),r))return true;if(tid==='ufo')return Math.hypot(P.x-(r.x+r.w/2),P.y-(r.y+r.h/2))<24;return overlap(bladeRect(tid,P.x,P.y,P.f,bladeCells()*2),r);}
// can this machine's blade reach that spot? (markReach marks what it can't)
function labReach(x,y){const i=(clamp(y,0,G.ph-1)>>1)*G.cols+(clamp(x,0,G.pw-1)>>1);return G.type[i]!==T_BLOCK&&!(G.nc&&G.nc[i]);}
function labMove(o,dx,dy){for(let r=6;r<=90;r+=6)for(let a=0;a<12;a++){const x=Math.round(o.x+Math.cos(a/12*Math.PI*2)*r),y=Math.round(o.y+Math.sin(a/12*Math.PI*2)*r);
  if(x<14||x>G.pw-14||y<14||y>G.ph-14)continue;if(labReach(x,y)&&labReach(x-dx,y-dy)&&labReach(x+dx,y+dy)&&labRect(G,x-dx,y-dy,dx*2,dy*2)){o.x=x;o.y=y;return true;}}return false;}
function labPost(g){const M=MODES[g.def.mode];g.lab={};if(M&&M.post)M.post(g);}
function labTick(dt,tid){const M=labM();if(!M||run.ended)return;run.lab=run.lab||{t:0};run.lab.t+=dt;if(M.tick)M.tick(dt,tid,run.lab);}
function labEnts(ents,top,bot){const M=labM();if(M&&M.ents)M.ents(ents,top,bot);}
// arrow at the screen edge pointing at something off screen
function labArrow(tx,ty,col){const sx=tx,sy=ty-camY+VIEW_Y;if(sy>VIEW_Y+8&&sy<VIEW_Y+VIEW_H-8&&sx>6&&sx<W-6)return;
  const cx=W/2,cy=VIEW_Y+VIEW_H/2,dx=sx-cx,dy=sy-cy,k=Math.min((W/2-12)/Math.max(0.001,Math.abs(dx)),(VIEW_H/2-14)/Math.max(0.001,Math.abs(dy))),ax=cx+dx*k,ay=cy+dy*k,an=Math.atan2(dy,dx),pu=Math.sin(tNow*8)*1.5;
  const tip=[ax+Math.cos(an)*(7+pu),ay+Math.sin(an)*(7+pu)],l=[ax+Math.cos(an+2.4)*7,ay+Math.sin(an+2.4)*7],r2=[ax+Math.cos(an-2.4)*7,ay+Math.sin(an-2.4)*7];
  b.fillStyle=K;b.beginPath();b.moveTo(tip[0]+Math.cos(an)*1.5,tip[1]+Math.sin(an)*1.5);b.lineTo(l[0]+Math.cos(an+2.4)*1.5,l[1]+Math.sin(an+2.4)*1.5);b.lineTo(r2[0]+Math.cos(an-2.4)*1.5,r2[1]+Math.sin(an-2.4)*1.5);b.closePath();b.fill();
  b.fillStyle=col||'#ffd23f';b.beginPath();b.moveTo(tip[0],tip[1]);b.lineTo(l[0],l[1]);b.lineTo(r2[0],r2[1]);b.closePath();b.fill();}
function labScreen(){const M=labM();if(!M)return;if(M.screen)M.screen();
  const o=run.lobj;if(o){const done=o.of!=null&&o.n>=o.of,l2=o.of==null?''+o.n:o.n+'/'+o.of,w=Math.max(textW(o.label),textW(l2),textW(o.extra||''))+8,h=o.extra?27:20,cx=2+Math.round(w/2);
    panel(2,VIEW_Y+2,w,h,done?'#3a5a12':'#13306b',done?'#ffd23f':M.col);text(b,o.label,cx,VIEW_Y+5,'#9fc0e8',{align:'center',outline:null});text(b,l2,cx,VIEW_Y+12,done?'#ffd23f':'#ffffff',{align:'center',outline:null});if(o.extra)text(b,o.extra,cx,VIEW_Y+19,'#ffd23f',{align:'center',outline:null});}
  const t=run.lab?run.lab.t:0;if(t<3.6&&!run.ended){const a=t<0.25?t/0.25:t>3.1?(3.6-t)/0.5:1,y=VIEW_Y+46-Math.round((1-Math.min(1,t/0.25))*16);b.globalAlpha=Math.max(0,Math.min(1,a));
    panel(8,y,164,36,'#13306b',M.col);text(b,(G.def.teach?'NEW! ':'')+M.name,W/2,y+5,M.col,{align:'center',scale:2});text(b,M.rule,W/2,y+23,'#ffffff',{align:'center',outline:null});b.globalAlpha=1;}}
// ---------------- the lab screen ----------------
const LAB_EV=['blizzard','presents','goldrush','yetihunt','snowroll','blackice','snowday','timeattack','forts','stars'];
const LAB_JOBS={blizzard:['maple','lot','lane','switchbacks'],presents:['maple','village','parade','northpole'],goldrush:['gardens','village','street','mainst'],yetihunt:['park','farmyard','mansion','chalets'],
  snowroll:['driveway','orchard','stadium','bluerun'],blackice:['culdesac','pond','icerink','frozenlake'],snowday:['driveway','highst','stadium','bluerun'],timeattack:['gardens','lot','food','gullisland'],
  forts:['school','playground','shops','games'],stars:['orchard','airport','lighthouse','aurora']};
const LAB_HOW={blizzard:['GUSTS SHOVE YOUR PLOW SIDEWAYS.','SQUALLS DUMP SNOW. COINS X2.'],presents:['FOUR TIMES THE PRESENTS.','DIG THEM OUT FOR TREATS.']};
function labStart(i,opts,kind){labOpen=false;labReopen=true;if(kind)labKind=kind;sfx('go');startLevelUI(i,opts);}
function drawLab(){if(labReopen&&!overlayOpen()&&!pendingStart){labReopen=false;labOpen=true;}
  if(!labOpen){if(!overlayOpen())button('labbtn',W-36,MAP_VY+3,32,14,'purple','LAB',()=>{labOpen=true;sfx('click');});return;}
  b.fillStyle='rgba(11,24,56,0.88)';b.fillRect(0,0,W,H);panel(6,20,168,288,'#13306b','#c4a0f5');
  if(labPick==null){text(b,'PROTOTYPE LAB',W/2,27,'#c4a0f5',{align:'center',scale:2});
    button('labt0',14,42,74,14,labTab===0?'purple':'navy','EVENTS',()=>{labTab=0;sfx('click');});button('labt1',92,42,74,14,labTab===1?'purple':'navy','AREA TWISTS',()=>{labTab=1;sfx('click');});
    const rows=labTab===0?LAB_EV.filter(k=>EVENT_DEFS[k]).map(k=>({k,name:EVENT_DEFS[k].name,sub:EVENT_DEFS[k].sub,col:EVENT_DEFS[k].col})):Object.keys(TWISTS).map(a=>{const M=MODES[TWISTS[a]]||{};return {k:'tw:'+a,name:M.name||a,area:(AREAS&&AREAS[a]&&AREAS[a].name||a.toUpperCase()),sub:M.sub||'',col:M.col||'#ffffff'};});
    rows.forEach((r,n)=>{const y=60+n*19;card(12,y,156,17,'#eef3fb',r.col);text(b,r.name,18,y+3,'#13306b',{outline:null});if(r.area)text(b,r.area,164,y+3,'#8a9ab8',{align:'right',outline:null});text(b,r.sub,18,y+10,'#5a6b8c',{outline:null});btn('labr'+n,12,y,156,17,()=>{labPick=r.k;sfx('click');});});
    {const m=labSizeMode();button('labsz',14,270,152,14,m==='old'?'grey':m==='small'?'blue':'green',m==='small'?'SIZES: SMALL - NARROW BLADES':m==='old'?'SIZES: OLD - AS LIVE':'SIZES: NEW - FOLDING WINGS',()=>{save.labSize=m==='new'?'small':m==='small'?'old':'new';vcache.clear();_tc.k='';persist();sfx('click');});}
    button('labclose',62,289,56,14,'grey','CLOSE',()=>{labOpen=false;sfx('click');});return;}
  const tw=labPick.startsWith('tw:'),a=tw?labPick.slice(3):null,mk2=tw?TWISTS[a]:(EVENT_DEFS[labPick].mod.mode||null),M=mk2?MODES[mk2]:null,d=tw?M:EVENT_DEFS[labPick];
  text(b,d.name,W/2,28,d.col,{align:'center',scale:2});text(b,tw?'AREA TWIST: '+((AREAS&&AREAS[a]&&AREAS[a].name)||a.toUpperCase()):'WEEKEND EVENT',W/2,44,'#9fc0e8',{align:'center',outline:null});
  const lines=(M&&M.how)||LAB_HOW[labPick]||[d.sub];lines.forEach((l,n)=>text(b,l,W/2,55+n*8,'#ffffff',{align:'center',outline:null}));
  const yj=58+lines.length*8+4;text(b,tw?'ITS 4 JOBS + 2 ELSEWHERE':'PICK A JOB',W/2,yj,'#ffd23f',{align:'center',outline:null});
  const jobs=(tw?twistJobs(a).concat((TW_ALSO[mk2]||[]).map(id=>LEVELS.findIndex(L=>L.id===id))):(LAB_JOBS[labPick]||[]).map(id=>LEVELS.findIndex(L=>L.id===id))).filter(i=>i>=0).slice(0,6);
  jobs.forEach((i,n)=>{const L=LEVELS[i],y=yj+10+n*22;card(14,y,152,20,'#eef3fb',n>=4&&tw?'#c4a0f5':'#9fc0e8');text(b,L.name,20,y+4,'#13306b',{outline:null});text(b,(AREAS&&AREAS[L.area]&&AREAS[L.area].name)||L.area.toUpperCase(),20,y+11,'#5a6b8c',{outline:null});
    button('labj'+n,124,y+3,38,14,'green','PLAY',()=>labStart(i,tw?{twist:a}:{event:'lab-'+labPick},tw?null:labPick));});
  button('labback',14,289,70,14,'grey','BACK',()=>{labPick=null;sfx('click');});button('labx',96,289,70,14,'grey','CLOSE',()=>{labOpen=false;sfx('click');});}
function sprAlpha(c){""")

open(f,'w',encoding='utf-8').write(s)
print('p150 lab core: modes, lab screen, pay-outs, arrows, objective pill, mode card')
