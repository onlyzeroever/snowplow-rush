import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
# DEV MODE (Nov 15, Alex): snowplowrush.app/dev behind the editor login. Same game, own save, a DEV tag at the top
# that opens a panel: stop the clock, play at x2/x4, hitboxes, instant 1/2/3-star win or fail, squall, Wild Ride
# parts, coins/gems, every job open, every machine, every look, New Winter, "away 2 hours", reset.
rep("const TEST_MODE=/[?&]test=1/.test(location.search),REVIEW_MODE=/[?&]review=(1|all)/.test(location.search);const SAVE_KEY=TEST_MODE?",
    "const TEST_MODE=/[?&]test=1/.test(location.search),REVIEW_MODE=/[?&]review=(1|all)/.test(location.search);const DEV_MODE=!!window.SR_DEV;\n"
    "const DEV=(()=>{let d={};if(DEV_MODE)try{d=JSON.parse(localStorage.getItem('sr.dev')||'{}')||{};}catch(e){}return Object.assign({open:false,freeze:false,speed:1,all:false,hit:false},d,{open:false});})();\n"
    "function devSave(){try{localStorage.setItem('sr.dev',JSON.stringify({freeze:DEV.freeze,speed:DEV.speed,all:DEV.all,hit:DEV.hit}));}catch(e){}}\n"
    "const SAVE_KEY=DEV_MODE?'snowplowRush.dev':TEST_MODE?")
rep("function persist(){try{","function persist(){if(window.__noPersist)return;try{")
rep("function levelOpen(i){return levelReach(i)&&levelGateOK(i)&&levelPaid(i);}","function levelOpen(i){return (DEV_MODE&&DEV.all)||(levelReach(i)&&levelGateOK(i)&&levelPaid(i));}")
rep("const levelAvail=i=>(LEVELS[i].winter||1)<=winterNo()||missionOn(i);","const levelAvail=i=>(DEV_MODE&&DEV.all)||(LEVELS[i].winter||1)<=winterNo()||missionOn(i);")
rep("run.time-=dt;","if(!(DEV_MODE&&DEV.freeze))run.time-=dt;")
rep("if(!(TEST_MODE&&window.__HOLD))try{update(dt);draw();}","if(!(TEST_MODE&&window.__HOLD))try{update(dt);if(DEV_MODE&&DEV.speed>1&&state==='play')for(let k=1;k<DEV.speed;k++)update(dt);draw();}")
rep("if(G.def.squall){if(run.squall){","if(G.def.squall||(DEV_MODE&&run.squall&&run.devSquall)){if(run.squall){")
rep("const fp=footprint(tid,P.x,P.y,P.f),pl=",
    "if(DEV_MODE&&DEV.hit)ents.push({base:1e9,draw:()=>{b.save();b.globalAlpha=0.65;b.lineWidth=1;for(const o of G.obstacles)if(o.y+o.h>top&&o.y<bot){b.strokeStyle='#ff2040';b.strokeRect(o.x+0.5,o.y+0.5,o.w-1,o.h-1);}"
    "for(const h of G.hazards)if(h.y+h.h>top&&h.y<bot){b.strokeStyle='#ffd23f';b.strokeRect(Math.round(h.x)+0.5,Math.round(h.y)+0.5,Math.max(1,h.w-1),Math.max(1,h.h-1));}"
    "const f2=footprint(tid,P.x,P.y,P.f),br2=bladeRect(tid,P.x,P.y,P.f,bwPx);b.strokeStyle='#33ff66';b.strokeRect(Math.round(f2.x)+0.5,Math.round(f2.y)+0.5,f2.w-1,f2.h-1);b.strokeStyle='#33ccff';b.strokeRect(Math.round(br2.x)+0.5,Math.round(br2.y)+0.5,br2.w-1,br2.h-1);b.restore();}});\n    const fp=footprint(tid,P.x,P.y,P.f),pl=")
rep("text(b,toast.s,W/2,y+4,toast.col,{align:'center'});}}",
    "text(b,toast.s,W/2,y+4,toast.col,{align:'center'});}\n  if(DEV_MODE)drawDev();}\n"
    "function devWin(k){if(state!=='play'||!run||run.ended){showToast('START A JOB FIRST','#ff9aa8');return;}const L=G.def,pct=k>0?(k>=3?Math.min(99,L.stars[2]+2):L.stars[k-1]+2):0;"
    "G.cleared=Math.ceil(G.clearable*pct/100);run.contUsed=true;DEV.open=false;endRound(false);}\n"
    "function devPart(){const ri=nextRideIdx();if(ri<0){showToast('OWN THE ROTARY FIRST','#ff9aa8');return;}const id=TOOLS[ri].id;save.parts=save.parts||{};const n=Math.min(3,(save.parts[id]||0)+1);save.parts[id]=n;"
    "if(n>=3){save.rideSeen=save.rideSeen||{};save.rideSeen[id]=true;}persist();showToast(TOOLS[ri].name+' PART '+n+'/3','#c4a0f5');}\n"
    "function devLooks(){for(const t of TOOLS)for(let i=1;i<=4;i++)save.skins[t.id+':'+i]=true;for(const o of OUTFITS)save.outfits[o.id]=true;for(const h of HATS)save.hats[h.id]=true;if(typeof TRAILS!=='undefined')for(const t of TRAILS)save.trails[t.id]=true;persist();vcache.clear();kidCacheClear();showToast('EVERY LOOK UNLOCKED','#7fe08a');}\n"
    "function drawDev(){const play=state==='play'&&run&&!run.ended;\n"
    "  if(!DEV.open){const lab='DEV'+(DEV.freeze?' II':'')+(DEV.speed>1?' X'+DEV.speed:''),w=textW(lab)+8,x=Math.round(W/2-w/2);R(b,x,23,w,10,K);R(b,x+1,24,w-2,8,'#d8364b');text(b,lab,W/2,25,'#ffffff',{align:'center',outline:null});btn('devtag',x-4,21,w+8,14,()=>{DEV.open=true;sfx('click');});return;}\n"
    "  ui=[];scrollAreas=[];b.fillStyle='rgba(8,14,40,0.82)';b.fillRect(0,0,W,H);panel(4,18,W-8,288,'#1b1f3b','#d8364b');text(b,'DEV MODE',W/2,24,'#ff9aa8',{align:'center',scale:2});\n"
    "  text(b,'OWN SAVE. TESTERS NEVER SEE THIS.',W/2,40,'#9fc0e8',{align:'center',outline:null});\n"
    "  const cx=[10,65,120];let y=50;const row=(lbl,items)=>{text(b,lbl,10,y,'#ffd23f',{outline:null});y+=8;items.forEach((it,k)=>{if(it)button('dev'+lbl+k,cx[k],y,50,16,it[1],it[0],it[2]);});y+=22;};\n"
    "  row('TIME',[[DEV.freeze?'CLOCK: OFF':'CLOCK: ON',DEV.freeze?'red':'green',()=>{DEV.freeze=!DEV.freeze;devSave();}],['SPEED X'+DEV.speed,DEV.speed>1?'orange':'blue',()=>{DEV.speed=DEV.speed>=4?1:DEV.speed*2;devSave();}],[DEV.hit?'HITBOX ON':'HITBOX OFF',DEV.hit?'orange':'grey',()=>{DEV.hit=!DEV.hit;devSave();}]]);\n"
    "  row('FINISH',[['1 STAR',play?'gold':'grey',()=>devWin(1)],['2 STARS',play?'gold':'grey',()=>devWin(2)],['3 STARS',play?'gold':'grey',()=>devWin(3)]]);\n"
    "  row('EVENTS',[['FAIL',play?'red':'grey',()=>devWin(0)],['SQUALL',play?'blue':'grey',()=>{if(!play)return;run.devSquall=true;run.squall={x:clamp(P.x,24,156),y:clamp(P.y-40,30,G.ph-30),r:28,t:0,dumped:false};sfx('squall');DEV.open=false;}],['RIDE PART','purple',devPart]]);\n"
    "  row('MONEY',[['+1M COINS','green',()=>{save.coins+=1e6;persist();}],['+1B COINS','green',()=>{save.coins+=1e9;persist();}],['+100 GEMS','purple',()=>{save.gems=(save.gems||0)+100;persist();}]]);\n"
    "  row('UNLOCK',[[DEV.all?'ALL JOBS: ON':'ALL JOBS',DEV.all?'orange':'grey',()=>{DEV.all=!DEV.all;devSave();}],['MACHINES','blue',()=>{save.tool=TOOLS.length-1;_tc.k='';vcache.clear();persist();showToast('EVERY MACHINE IS YOURS','#7fe08a');}],['ALL LOOKS','blue',devLooks]]);\n"
    "  row('WORLD',[['NO MONEY','grey',()=>{save.coins=0;save.gems=0;persist();}],['NEW WINTER','orange',()=>{DEV.open=false;if(play)endRound(false);startNewWinter();}],['AWAY 2H','blue',()=>{save.last=Date.now()-7200e3;if(!(save.lv.helpers>0))save.lv.helpers=1;persist();window.__noPersist=true;location.reload();}]]);\n"
    "  y+=4;button('devreset',10,y,78,18,'red','RESET SAVE',()=>{window.__noPersist=true;try{localStorage.removeItem(SAVE_KEY);}catch(e){}location.reload();});button('devclose',92,y,78,18,'blue','CLOSE',()=>{DEV.open=false;sfx('click');});\n"
    "  text(b,'COINS '+fmt(save.coins)+'  GEMS '+(save.gems||0)+'  WINTER '+winterNo(),W/2,y+24,'#9fc0e8',{align:'center',outline:null});}")
rep('function drawLogo(){','function drawLogo(){if(DEV_MODE&&DEV.open)return;')
open(f,'w',encoding='utf-8').write(s)
