import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# FOG OF WAR: the area you're in is alive; the next one is visible but frozen under a blizzard
# haze with "?" markers and a banner saying what breaks through; everything beyond is a storm
# wall you can't scroll past (only the Frozen North's aurora glows above it). Reaching a new
# area rolls the storm back.
# ---------------------------------------------------------------------------------------------
rep("function drawWorld(dt){",r"""// ---------------- FOG OF WAR ----------------
const AREA_SEQ=['suburbs','farm','city','themepark','harbour','ski','pass','north'];
function areaReached(a){if(a===AREA_SEQ[0])return true;return LEVELS.some((L,i)=>L.area===a&&levelReach(i));}
function fogCur(){let c=0;for(let k=0;k<AREA_SEQ.length;k++)if(areaReached(AREA_SEQ[k]))c=k;return c;}
function biomeById(id){return BIOMES.find(B=>B.id===id);}
let fogAnim=null,fogStormY=-1,fogHaze=null;
// job numbers in play order: by area, then bottom to top
let JOB_NO=null;function jobNo(i){if(!JOB_NO){JOB_NO={};let n=1;const ord=LEVELS.map((L,k)=>k).filter(k=>LEVELS[k].area!=='secret').sort((a,c)=>{const A=AREA_SEQ.indexOf(LEVELS[a].area),C=AREA_SEQ.indexOf(LEVELS[c].area);return A!==C?A-C:LEVELS[c].my-LEVELS[a].my;});for(const k of ord)JOB_NO[k]=n++;}return JOB_NO[i]||i+1;}
function fogUpdate(dt){const cur=fogCur();if(save.areaSeen==null){save.areaSeen=cur;persist();}
  if(!fogAnim&&cur>save.areaSeen&&!overlayOpen()&&!plowAnim&&state==='map'){fogAnim={s:save.areaSeen,t:0};const B=biomeById(AREA_SEQ[save.areaSeen+1]);if(B)mapPan={to:clamp(B.y1-MAP_VH*0.75,0,MAP_H-MAP_VH)};sfx('squall');buzz(30);}
  let s2=save.areaSeen,p=0;if(fogAnim){fogAnim.t+=dt;p=clamp((fogAnim.t-0.7)/2.4,0,1);s2=fogAnim.s;if(fogAnim.t>3.4){save.areaSeen=fogAnim.s+1;fogAnim=null;persist();sfx('fanfare');}}
  const e=p*p*(3-2*p),hz=s2+1<AREA_SEQ.length?biomeById(AREA_SEQ[s2+1]):null,hz2=s2+2<AREA_SEQ.length?biomeById(AREA_SEQ[s2+2]):null;
  fogHaze={a:hz,aAlpha:1-e,b:fogAnim?hz2:null,bAlpha:e,banner:fogAnim?null:hz};
  fogStormY=hz?Math.round(hz.y0+((hz2?hz2.y0:0)-hz.y0)*e):-1;if(fogStormY<=0)fogStormY=-1;}
function fogMinScroll(){return fogStormY>0?Math.max(0,fogStormY-70):0;}
function fogged(y){return fogHaze&&fogHaze.a&&fogHaze.aAlpha>0.5&&y>=fogHaze.a.y0&&y<fogHaze.a.y1;}
function drawHaze(B,a,oy,sy){if(!B||a<=0.01)return;const top=Math.max(MAP_VY,sy(B.y0)),bot=Math.min(MAP_VY+MAP_VH,sy(B.y1));if(bot<=top)return;
  b.save();b.globalAlpha=a;b.fillStyle='rgba(150,168,204,0.5)';b.fillRect(0,top,W,bot-top);b.fillStyle='rgba(236,242,252,0.32)';b.fillRect(0,top,W,bot-top);
  // soft lower edge so it melts into the area you're in
  for(let k=0;k<18;k++){const y=sy(B.y1)-18+k;if(y<top||y>=bot)continue;b.fillStyle='rgba(236,242,252,'+(0.04*(18-k)/18*8).toFixed(3)+')';b.fillRect(0,y,W,1);}
  // blowing snow
  for(let k=0;k<90;k++){const span=B.y1-B.y0,yy=B.y0+((hash(k,71)%span)+tNow*(18+k%7*4))%span,xx=((hash(71,k)%W)+tNow*(30+k%5*9))%W,y=sy(yy);if(y<top||y>=bot)continue;
    R(b,Math.round(xx),y,k%3?2:3,1,'#ffffff');}
  b.restore();}
function drawStorm(oy,sy){if(fogStormY<=0)return;const edge=sy(fogStormY);if(edge<=MAP_VY)return;const bot=Math.min(MAP_VY+MAP_VH,edge);
  R(b,0,MAP_VY,W,bot-MAP_VY,'#3d4b74');
  // rolling cloud banks
  const cols=['#4a5a85','#56688f','#62749b','#4f5f8a'];
  for(let k=0;k<70;k++){const yy=fogStormY-6-(hash(k,23)%560),y=sy(yy);if(y<MAP_VY-30||y>bot+20)continue;const r=10+hash(23,k)%16,x=Math.round(((hash(k,29)%(W+80))+tNow*(5+k%6*2))%(W+80))-40;
    b.fillStyle=cols[k%4];pixCircle(b,x,y,r);}
  // a faint aurora above the storm: the Frozen North is up there somewhere
  for(let x=0;x<W;x+=2){const yy=MAP_VY+18+Math.sin(x*0.045+tNow*0.5)*8+Math.sin(x*0.13+tNow*0.8)*3,a=0.10+0.06*Math.sin(x*0.08+tNow*1.3);if(yy+10>bot-40)continue;
    R(b,x,Math.round(yy),2,8,'rgba(90,240,170,'+a.toFixed(2)+')');R(b,x,Math.round(yy)+8,2,6,'rgba(170,110,255,'+(a*0.8).toFixed(2)+')');}
  // the storm's edge: billowing white-grey puffs
  for(let x=-8;x<W+8;x+=9){const r=8+(hash(x+400,7)%5),y=edge-3+Math.round(Math.sin(x*0.21+tNow*1.4)*2);b.fillStyle='#8a9bc2';pixCircle(b,x,y,r+1);b.fillStyle='#b9c6e0';pixCircle(b,x,y-1,r);b.fillStyle='#dbe3f2';pixCircle(b,x-2,y-3,Math.max(2,r-4));}
  for(let k=0;k<50;k++){const x=((hash(k,41)%W)+tNow*(40+k%5*12))%W,y=MAP_VY+((hash(41,k)%Math.max(1,bot-MAP_VY))+tNow*(30+k%4*10))%Math.max(1,bot-MAP_VY);R(b,Math.round(x),Math.round(y),2,1,'rgba(255,255,255,0.6)');}}
function drawFogBanner(oy,sy){const B=fogHaze&&fogHaze.banner;if(!B)return;const y=sy(B.y1)-40;if(y<MAP_VY-30||y>MAP_VY+MAP_VH)return;
  const entry=LEVELS.filter(L=>L.area===B.id&&L.from.some(id=>{const F=LEVELS[lvIdx(id)];return F&&F.area!==B.id&&F.area!=='secret';}));
  let need='THE FINAL AREA - COMING SOON';if(entry.length){const F=LEVELS[lvIdx(entry[0].from[0])];need='FINISH '+F.name+' TO BREAK THROUGH';}
  const w=Math.max(textW(B.name,2)+16,textW(need)+12),x=Math.round(W/2-w/2);R(b,x,y,w,28,K);R(b,x+1,y+1,w-2,26,'#13306b');R(b,x+1,y+1,w-2,1,'#4f8fdc');
  text(b,B.name,W/2,y+4,'#ffffff',{align:'center',scale:2});text(b,need,W/2,y+19,'#9fd8ff',{align:'center',outline:null});}
function drawWorld(dt){""")

# scroll can't go past the storm; panning targets respect it too
rep("  const oy=Math.round(scrollArea('map',0,MAP_VY,W,MAP_VH,MAP_H)),uiFrom=ui.length;",
    "  fogUpdate(dt);{const mn=fogMinScroll();if(scrollY.map!=null&&scrollY.map<mn)scrollY.map=mn;if(mapPan&&mapPan.to<mn)mapPan.to=mn;}\n  const oy=Math.round(Math.max(fogMinScroll(),scrollArea('map',0,MAP_VY,W,MAP_VH,MAP_H))),uiFrom=ui.length;")
# haze and storm sit over the scenery, under gates and job markers
rep("  drawMapLive(oy,sy,vis,dt);drawPlowAnim(oy,sy,dt);",
    "  drawMapLive(oy,sy,vis,dt);drawPlowAnim(oy,sy,dt);\n  if(fogHaze){drawHaze(fogHaze.a,fogHaze.aAlpha,oy,sy);drawHaze(fogHaze.b,fogHaze.bAlpha,oy,sy);}drawStorm(oy,sy);")
rep("const li=lvIdx(gid);if(levelGateOK(li))continue;const p=gatePos(gid);if(!p||!vis(p.y,30))continue;",
    "const li=lvIdx(gid);if(levelGateOK(li))continue;const p=gatePos(gid);if(!p||!vis(p.y,30)||p.y<fogStormY)continue;")
rep("const li=lvIdx(id),L=LEVELS[li],T2=TOLLPOS[id];if(!vis(T2.y,30))continue;",
    "const li=lvIdx(id),L=LEVELS[li],T2=TOLLPOS[id];if(!vis(T2.y,30)||T2.y<fogStormY||fogged(T2.y))continue;")
# job markers: hidden in the storm, "?" in the haze
rep("LEVELS.forEach((L,i)=>{if(!vis(L.my,30))return;const st=nodeState(i),x=L.mx,y=sy(L.my);drawNode(i,x,y,st);",
    "LEVELS.forEach((L,i)=>{if(!vis(L.my,30))return;if(L.my<fogStormY)return;const st=fogged(L.my)&&!levelReach(i)?'fog':nodeState(i),x=L.mx,y=sy(L.my);drawNode(i,x,y,st);")
rep("  drawMapSnow(oy,dt);drawUfoFly(dt);","  drawFogBanner(oy,sy);drawMapSnow(oy,dt);drawUfoFly(dt);")
rep("const L=LEVELS[i],wild=L.area==='secret',stars=save.stars[i],small=st==='far'||st==='mystery',r=small?7:9;",
    "const L=LEVELS[i],wild=L.area==='secret',stars=save.stars[i],small=st==='far'||st==='mystery'||st==='fog',r=small?7:9;")
rep("if(st==='mystery'){fill='#2a2140';ring='#8a6fd6';}","if(st==='fog'){fill='#9fb0cf';ring='#e6ebf3';}else if(st==='mystery'){fill='#2a2140';ring='#8a6fd6';}")
rep("if(st==='mystery')text(b,'?',x,y-2,'#c4a0f5',{align:'center'});","if(st==='mystery')text(b,'?',x,y-2,'#c4a0f5',{align:'center'});else if(st==='fog')text(b,'?',x,y-2,'#ffffff',{align:'center'});")
rep("else text(b,''+(i+1),x,y-2,ink,{align:'center',outline:stars===3?null:K});","else text(b,''+jobNo(i),x,y-2,ink,{align:'center',outline:stars===3?null:K});")
# the list view only shows areas you can see
rep("const rows=[];for(const B of BIOMES.slice().reverse()){",
    "const rows=[];const fogMax=Math.min(AREA_SEQ.length-1,(save.areaSeen==null?fogCur():save.areaSeen)+1);for(const B of BIOMES.slice().reverse()){if(AREA_SEQ.indexOf(B.id)>fogMax)continue;")
rep("__SR={pineSprite,","__SR={pineSprite,fogCur,get fogStormY(){return fogStormY;},jobNo,")
open(f,'w',encoding='utf-8').write(s);print('p44 ok')
