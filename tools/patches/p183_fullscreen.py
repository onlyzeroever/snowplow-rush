# Full screen on every phone shape (Alex, Nov 22: "ok awesome" to full screen on tall phones; iPhone Duo: "use the full
# display too and ensure it's optimised"). HELD from the live web game until Alex has reviewed it; in the lab and the app.
#  - tall phones: the game gets taller (320 up to 420 logical px). The top bar stays at the top, the buttons at the bottom,
#    and the map, the jobs and the lists get the extra height. Cards and pop-ups sit in the middle of the screen.
#  - safe areas (notch, Dynamic Island, home bar): the game sits inside them and the top/bottom bars carry on under them,
#    so there are no empty bands.
#  - wide screens (iPhone Duo open, iPad): the game keeps its portrait column and the world carries on either side
#    (snowy map scenery on the map, the job's surroundings in a job, the title's sky and hills, wood or garage walls),
#    with the top and bottom bars running the full width. Dimmed backgrounds dim the whole screen.
#  - jobs shorter than the screen sit in the middle with snowy ground around them.
#  - every resize (fold or unfold mid-job included) re-fits without a restart.
import sys
HELPERS=open(__file__.replace('p183_fullscreen.py','p183_helpers.js'),encoding='utf-8').read()
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---- 1. the height is no longer fixed
rep("const W=180,H=320,HUD_H=22,BAR_H=40,VIEW_Y=HUD_H,VIEW_H=H-HUD_H-BAR_H,NAV_Y=290;",
    "const W=180,HUD_H=22,BAR_H=40,VIEW_Y=HUD_H;let H=320,VIEW_H=H-HUD_H-BAR_H,NAV_Y=290;\n"
    "// full-screen layout state (p183): composite size SCW x SCH (logical px), the game column at COX,COY; UI_OY is the offset\n"
    "// of whatever is being drawn centred (cards), so taps land where things are drawn\n"
    "let SCW=180,SCH=320,COX=0,COY=0,CSC=1,UI_OY=0,OV_REC=false,FRAME_DIMS=[],TTL_OY=0,MAP_OY=0;const H_MAX=420;\n"
    "function ovOff(){return Math.max(0,Math.floor((H-320)/2));}\n"
    "function ovBegin(){const o=ovOff();OV_REC=true;b.save();if(o)b.translate(0,o);UI_OY+=o;}\n"
    "function ovEnd(){const o=ovOff();b.restore();UI_OY-=o;}\n"
    "function camTarget(){return G.ph<VIEW_H?Math.round((G.ph-VIEW_H)/2):clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);}")
rep("MAP_VY=23,MAP_VH=NAV_Y-2-MAP_VY;","MAP_VY=23;let MAP_VH=NAV_Y-2-MAP_VY;")

# ---- 2. buttons and lists drawn inside a centred card are hit where they are drawn; full-screen dims are recorded
#         (so the margins can be dimmed the same) and still cover the whole screen when the card is moved down
rep("function btn(id,x,y,w,h,fn){ui.push({id,x,y,w,h,fn});}",
    "function btn(id,x,y,w,h,fn){ui.push(x===0&&y===0&&w===W&&h===H?{id,x:-COX,y:-COY,w:SCW,h:SCH,fn}:{id,x,y:y+UI_OY,w,h,fn});}\n"
    "{const fr=b.fillRect.bind(b);b.fillRect=function(x,y,w,h){if(x===0&&y===0&&w===W&&h===H){if(OV_REC)FRAME_DIMS.push([this.fillStyle,this.globalAlpha]);if(UI_OY)return fr(0,-UI_OY,W,H+UI_OY);}return fr(x,y,w,h);};}")
rep("scrollAreas.push({key,x,y,w,h,max});","scrollAreas.push({key,x,y:y+UI_OY,w,h,max});")

# ---- 3. the camera: a job shorter than the view sits in the middle
rep("markReach(G);camY=clamp(P.y-VIEW_H*0.55,0,Math.max(0,G.ph-VIEW_H));","markReach(G);camY=camTarget();")
rep("const target=clamp(P.y-VIEW_H*0.55,0,Math.max(0,G.ph-VIEW_H));camY+=","const target=camTarget();camY+=")


# ---- 4. fit the screen: the column fills the safe area's height on tall phones; the canvas covers the whole screen
rep("#wrap{position:fixed;inset:0;z-index:1;box-sizing:border-box;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);display:flex;align-items:center;justify-content:center}",
    "#wrap{position:fixed;inset:0;z-index:1;box-sizing:border-box;padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);display:flex;align-items:center;justify-content:center}\n#c{position:absolute;left:0;top:0}")
rep("function resize(){const vw=wrap.clientWidth||innerWidth,vh=wrap.clientHeight||innerHeight;const cs=Math.min(vw/W,vh/H);const dpr=window.devicePixelRatio||1;\n  KS=Math.max(1,Math.min(window.SR_KS||8,KS_CAP,Math.ceil(cs*dpr)));cv.width=W*KS;cv.height=H*KS;cv.style.width=Math.floor(W*cs)+'px';cv.style.height=Math.floor(H*cs)+'px';ctx.imageSmoothingEnabled=false;",
    HELPERS+
    "const cbx=mk(W,320).getContext('2d');cbx.imageSmoothingEnabled=false;\n"
    "function safeIn(){let st=null;try{st=getComputedStyle(wrap);}catch(e){}const n=k=>st?parseFloat(st[k])||0:0;return{l:n('paddingLeft'),r:n('paddingRight'),t:n('paddingTop'),b:n('paddingBottom')};}\n"
    "function layoutChanged(){try{draw.snap=null;draw.cur=null;}catch(e){}try{BOOKBG=null;}catch(e){}MG.k='';}\n"
    "function resize(){const fw=wrap.clientWidth||innerWidth,fh=wrap.clientHeight||innerHeight,sa=safeIn(),sw=Math.max(60,fw-sa.l-sa.r),sh=Math.max(60,fh-sa.t-sa.b);\n"
    "  const nh=sh/sw>320/W?Math.min(H_MAX,Math.max(320,Math.round(W*sh/sw))):320;\n"
    "  if(nh!==H){H=nh;VIEW_H=H-HUD_H-BAR_H;NAV_Y=H-30;MAP_VH=NAV_Y-2-MAP_VY;buf.height=H;b.imageSmoothingEnabled=false;layoutChanged();}\n"
    "  const cs=Math.min(sw/W,sh/H);CSC=cs;SCW=Math.max(W,Math.ceil(fw/cs-0.01));SCH=Math.max(H,Math.ceil(fh/cs-0.01));COX=Math.max(0,Math.round((sa.l+(sw-W*cs)/2)/cs));COY=Math.max(0,Math.round((sa.t+(sh-H*cs)/2)/cs));\n"
    "  if(COX+W>SCW)COX=SCW-W;if(COY+H>SCH)COY=SCH-H;if(cbx.canvas.width!==SCW||cbx.canvas.height!==SCH){cbx.canvas.width=SCW;cbx.canvas.height=SCH;cbx.imageSmoothingEnabled=false;MG.k='';}\n"
    "  const dpr=window.devicePixelRatio||1;KS=Math.max(1,Math.min(window.SR_KS||8,KS_CAP,Math.ceil(cs*dpr)));cv.width=SCW*KS;cv.height=SCH*KS;cv.style.width=(SCW*cs)+'px';cv.style.height=(SCH*cs)+'px';ctx.imageSmoothingEnabled=false;")
rep("function toL(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)/r.width*W,y:(e.clientY-r.top)/r.height*H};}",
    "function toL(e){const r=cv.getBoundingClientRect();return{x:(e.clientX-r.left)/r.width*SCW-COX,y:(e.clientY-r.top)/r.height*SCH-COY};}")
# ---- 5. every frame: margins first (scenery, bars, dims), then the game column, then the logo on top of it
rep("ctx.imageSmoothingEnabled=false;ctx.drawImage(buf,0,0,W*KS,H*KS);\n  drawLogo();",
    "ctx.imageSmoothingEnabled=false;\n"
    "  if(SCW===W&&SCH===H){ctx.drawImage(buf,0,0,W*KS,H*KS);ctx.save();ctx.translate(0,(state==='title'?TTL_OY:0)*KS);drawLogo();ctx.restore();}\n"
    "  else{try{paintMargins();}catch(e){if(!paintMargins.err){paintMargins.err=1;console.error(e);}cbx.fillStyle='#0b1838';cbx.fillRect(0,0,SCW,SCH);}cbx.drawImage(buf,COX,COY);ctx.drawImage(cbx.canvas,0,0,SCW*KS,SCH*KS);\n"
    "    ctx.save();ctx.translate(COX*KS,(COY+(state==='title'?TTL_OY:0))*KS);drawLogo();ctx.restore();}\n"
    "  FRAME_DIMS=[];OV_REC=false;")

# ---- 6. cards and pop-ups sit in the middle of a tall screen (the dims still cover everything)
rep("function draw(){const dtD=Math.min(0.05,Math.max(0,tNow-(draw.t==null?tNow:draw.t)));draw.t=tNow;\n  ui=[];scrollAreas=[];",
    "function draw(){const dtD=Math.min(0.05,Math.max(0,tNow-(draw.t==null?tNow:draw.t)));draw.t=tNow;\n  ui=[];scrollAreas=[];OV_REC=false;FRAME_DIMS=[];UI_OY=0;")
rep("const ovA=ovk&&draw.ovT!=null?Math.min(1,(tNow-draw.ovT)/0.14):1;","ovBegin();const ovA=ovk&&draw.ovT!=null?Math.min(1,(tNow-draw.ovT)/0.14):1;")
rep("if(remindAsk&&state==='map'&&!adScreen&&!(IAP&&IAP.busy))drawRemindAsk();if(adScreen)drawAd();if(IAP&&IAP.busy)drawStoreBusy();",
    "if(remindAsk&&state==='map'&&!adScreen&&!(IAP&&IAP.busy))drawRemindAsk();if(adScreen)drawAd();if(IAP&&IAP.busy)drawStoreBusy();ovEnd();")
rep("drawHUD();drawBottomBar();drawCoinFly();\n  if(run.offer&&!run.ended){","drawHUD();drawBottomBar();drawCoinFly();ovBegin();\n  if(run.offer&&!run.ended){")
rep("  if(run.ended&&run.res)drawResults();}","  if(run.ended&&run.res)drawResults();ovEnd();}")
rep("if(pendingStart)try{drawLoading();}catch(e){}","if(pendingStart){ovBegin();try{drawLoading();}catch(e){}ovEnd();}")
# ---- 7. the title: the scene sits in the middle, the sky runs up to the top, the gear stays in the corner
rep("if(state==='title')drawTitle();else if(state==='map')drawMap();",
    "if(state==='title'){TTL_OY=ovOff();R(b,0,0,W,H,'#9fd0f2');b.save();b.translate(0,TTL_OY);UI_OY=TTL_OY;drawTitle();b.restore();UI_OY=0;}else if(state==='map')drawMap();")
rep("button('tgear',W-20,2,18,17,'blue',null,()=>{settingsOpen=true;sfx('click');});b.drawImage(SPR.gear,W-15,6);",
    "button('tgear',W-20,2-TTL_OY,18,17,'blue',null,()=>{settingsOpen=true;sfx('click');});b.drawImage(SPR.gear,W-15,6-TTL_OY);")
# ---- 8. a job shorter than the screen: snowy ground and pines above and below it
rep("b.save();b.beginPath();b.rect(0,VIEW_Y,W,VIEW_H);b.clip();b.translate(sx,VIEW_Y-cy+sy);\n  for(const t of G.tiles){",
    "b.save();b.beginPath();b.rect(0,VIEW_Y,W,VIEW_H);b.clip();b.translate(sx,VIEW_Y-cy+sy);\n"
    "  if(cy<0)mgScene(b,-8,cy-2,W+16,-cy+2,-8,cy-2,'#f4f8ff',0.42);if(cy+VIEW_H>G.ph)mgScene(b,-8,G.ph,W+16,cy+VIEW_H-G.ph+2,-8,G.ph,'#f4f8ff',0.42);\n"
    "  for(const t of G.tiles){")
# ---- 9. the map remembers where it is scrolled to (for the scenery either side); a drag that starts beside the map still scrolls it
rep("const oy=Math.round(Math.max(fogMinScroll(),scrollArea('map',0,MAP_VY,W,MAP_VH,MAP_H))),uiFrom=ui.length;",
    "const oy=Math.round(Math.max(fogMinScroll(),scrollArea('map',0,MAP_VY,W,MAP_VH,MAP_H))),uiFrom=ui.length;MAP_OY=oy;")
rep("  for(let i=scrollAreas.length-1;i>=0;i--){const a=scrollAreas[i];if(p.x>=a.x&&p.x<a.x+a.w&&p.y>=a.y&&p.y<a.y+a.h){",
    "  for(let i=scrollAreas.length-1;i>=0;i--){const a=scrollAreas[i],qx=a.key==='map'&&!overlayOpen()?clamp(p.x,a.x,a.x+a.w-1):p.x;if(qx>=a.x&&qx<a.x+a.w&&p.y>=a.y&&p.y<a.y+a.h){")
# ---- 10. the garage list uses the extra height
rep("const VY=44,VH=204,sy=scrollArea('garage',","const VY=44,VH=204+(NAV_Y-290),sy=scrollArea('garage',")
# ---- 11. a stick started beside the column (wide screens) is still drawn where it can be seen
rep("if(joy){const ox=Math.round(joy.ox),oy=Math.round(joy.oy);","if(joy){const jdx=Math.round(clamp(joy.ox,18,W-18)-joy.ox),ox=Math.round(joy.ox)+jdx,oy=Math.round(joy.oy);")
rep("R(b,Math.round(joy.x)-3,Math.round(joy.y)-3,7,7,'rgba(255,255,255,0.45)');","R(b,Math.round(joy.x)+jdx-3,Math.round(joy.y)-3,7,7,'rgba(255,255,255,0.45)');")
# ---- 12. the upgrade cards spread out a little on taller screens (and the block moves down to stay balanced)
rep("rows.forEach(([k,ico],i)=>{const y=45+i*48,x=4,w=172,h=44;",
    "const UX=Math.max(0,NAV_Y-290),UG=Math.min(8,Math.floor(UX/4)),US=Math.min(20,Math.floor((UX-4*UG)/2));rows.forEach(([k,ico],i)=>{const y=45+US+i*(48+UG),x=4,w=172,h=44;")
open(f,'w',encoding='utf-8').write(s)
print('p183 full screen: tall phones, safe areas, wide screens')
