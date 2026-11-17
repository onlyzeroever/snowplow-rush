import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Wild Rides become their own collection (plan doc decision 1).
#  - Owning a ride no longer means owning every machine before it: save.rides holds rides, save.tool is the best regular
#    machine (always < BASE_TOOLS). Old saves move their rides across.
#  - A ride clears 15% faster and earns 15% more per cell than your best regular machine (its upgrades and Mk II included),
#    and keeps its own shape: the Dragon is narrow and quick, the Mech wide. Rides have no upgrades of their own; with a
#    ride in use, the Upgrades screen upgrades your best machine and the ride follows.
#  - Rides can be had from the Super Plow on (test drive, then gems or the Ride Pass); parts still drop after the Rotary;
#    coins buy them from the winter shown. Rides still come in order.
rep("const BASE_TOOLS=8;",
    "const BASE_TOOLS=8;\n"
    "function owns(i){return i>=0&&i<TOOLS.length&&(i<BASE_TOOLS?i<=save.tool:!!(save.rides&&save.rides[TOOLS[i].id])||i<=save.tool);}  // (save.tool past the ladder: only test scripts)\n"
    "function rideNextIdx(){for(let i=BASE_TOOLS;i<TOOLS.length;i++)if(!owns(i))return i;return -1;}\n"
    "function ridesOwned(){let n=0;for(let i=BASE_TOOLS;i<TOOLS.length;i++)if(owns(i))n++;return n;}\n"
    "const RIDE_BOOST=1.15,RIDE_WIDE={monster:1.04,jet:0.92,mech:1.12,dragon:0.86,ufo:1};\n"
    "// what a ride is built on: the fastest-clearing regular machine you own and the best coins per cell, upgrades and Mk II in\n"
    "function rideBase(){let w=8,sp=32,rate=0,v=1,bump=0;for(let j=0;j<=Math.min(save.tool,BASE_TOOLS-1);j++){const t=TOOLS[j],m=mLv(t.id),ms=mspec(t.id),mk=isMk2(t.id),\n"
    "  wj=Math.min(80,Math.round(t.width*(1+ms.sizePer*m.size))),sj=t.speed*(1+ms.speedPer*m.speed)*(mk?MK2_SPEED:1);if(wj*sj>rate){rate=wj*sj;w=wj;sp=sj;}v=Math.max(v,t.value*(mk?MK2_COINS:1));bump=Math.max(bump,m.bumper||0);}\n"
    "  return {w,sp,v,bump};}\n"
    "function rideTool(i){const t=TOOLS[i],b=rideBase(),w=Math.max(8,Math.min(80,Math.round(b.w*Math.sqrt(RIDE_BOOST)*(RIDE_WIDE[t.id]||1))));\n"
    "  return Object.assign({},t,{width:w,speed:Math.round(RIDE_BOOST*b.w*b.sp/w*10)/10,value:Math.round(b.v*RIDE_BOOST*100)/100,ride:true,bump:b.bump});}")
# load: move rides out of the machine index
rep("  save.tool=Math.max(0,Math.min(TOOLS.length-1,Math.floor(num(save.tool,0))));if(save.use!=null){const u=Math.floor(num(save.use,-1));save.use=(u<0||u>save.tool)?null:u;}",
    "  save.tool=Math.max(0,Math.min(TOOLS.length-1,Math.floor(num(save.tool,0))));{const r0=(save.rides&&typeof save.rides==='object')?save.rides:{},r={};for(let j=BASE_TOOLS;j<TOOLS.length;j++)if(r0[TOOLS[j].id]===true||j<=save.tool)r[TOOLS[j].id]=true;save.rides=r;\n"
    "    if(save.tool>=BASE_TOOLS){save.tool=BASE_TOOLS-1;if(save.mlv&&typeof save.mlv==='object')for(let j=BASE_TOOLS;j<TOOLS.length;j++){const m=save.mlv[TOOLS[j].id];if(m&&typeof m==='object'){m.speed=0;m.size=0;}}}}\n"
    "  if(save.use!=null){const u=Math.floor(num(save.use,-1));save.use=owns(u)?u:null;}")
# the machine in use: rides are built from your best machine; drives and missions too
rep("function tool(){if(chal())return TOOLS[toolIdx(run.challenge)];if(drv())return TOOLS[toolIdx(run.drive)];if(msn())return TOOLS[toolIdx(run.mission)];const ui2=useIdx(),g=save.gold==null?-1:save.gold,k=ui2+'|'+g;if(_tc.k===k)return _tc.v;const t=TOOLS[ui2];let v=t;",
    "function tool(){if(chal())return TOOLS[toolIdx(run.challenge)];if(drv())return run.rideT||(run.rideT=rideTool(toolIdx(run.drive)));if(msn())return run.rideT||(run.rideT=rideTool(toolIdx(run.mission)));const ui2=useIdx(),g=save.gold==null?-1:save.gold,k=ui2+'|'+g;if(_tc.k===k)return _tc.v;const t=TOOLS[ui2];let v=ui2>=BASE_TOOLS?rideTool(ui2):t;")
rep("function curLv(){if(chal())return ZERO_LV;if(drv()||msn()){const rl=run.rideLv;return rl?{speed:rl.speed,size:rl.size,bumper:rl.bumper,value:save.lv.value,helpers:save.lv.helpers}:ZERO_LV;}",
    "function curLv(){if(chal())return ZERO_LV;{const t=tool();if(t.ride)return {speed:0,size:0,bumper:t.bump||0,value:save.lv.value,helpers:save.lv.helpers};}")
rep("function rideLvFor(t){return (drv()||msn())&&run.rideLv&&run.rideId===t.id?run.rideLv:null;}\n","")
rep("function bladeCells(t){t=t||tool();const rl=rideLvFor(t);return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()?0:rl?rl.size:(drv()||msn())?0:mLv(t.id).size))));}",
    "function bladeCells(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()||t.ride?0:mLv(t.id).size))));}")
rep("function rateOf(id,lv){const t=TOOLS[toolIdx(id)],sp=mspec(id);return t.speed*(1+sp.speedPer*lv.speed)*Math.min(80,Math.round(t.width*(1+sp.sizePer*lv.size)));}\n","")
rep("function bestOwned(except){let best=0,bump=0;for(let j=0;j<=Math.min(save.tool,TOOLS.length-1);j++){const id=TOOLS[j].id;if(id===except)continue;const m=mLv(id);best=Math.max(best,rateOf(id,m));bump=Math.max(bump,m.bumper||0);}return {rate:best,bumper:bump};}\n","")
rep("function matchLv(id){const b0=bestOwned(id),lv={speed:0,size:0,bumper:b0.bumper};while(rateOf(id,lv)<b0.rate&&(lv.speed<MUP_LV||lv.size<MUP_LV)){if(lv.size<=lv.speed&&lv.size<MUP_LV)lv.size++;else if(lv.speed<MUP_LV)lv.speed++;else lv.size++;}return lv;}\n","")
rep("function giveMatch(i){const id=TOOLS[i].id,lv=matchLv(id),m=mLv(id);m.speed=Math.max(m.speed,lv.speed);m.size=Math.max(m.size,lv.size);m.bumper=Math.max(m.bumper||0,lv.bumper);}\n","")
# upgrades go to your best machine while you drive a ride
rep("function curMachine(){return TOOLS[useIdx()].id;}","function curMachine(){const u=useIdx();return TOOLS[u>=BASE_TOOLS?save.tool:u].id;}")
rep("  save.coins-=c;if(MACHINE_UPG.includes(k))mLv(curMachine())[k]++;else save.lv[k]++;sfx('buy');buzz(15);vcache.clear();",
    "  save.coins-=c;if(MACHINE_UPG.includes(k))mLv(curMachine())[k]++;else save.lv[k]++;sfx('buy');buzz(15);vcache.clear();_tc.k='';")
# missions and test drives
rep("run.mission=LEVELS[idx].tool;run.rideId=run.mission;run.rideLv=matchLv(run.mission);","run.mission=LEVELS[idx].tool;run.rideT=null;")
rep("run.drive=t.id;run.rideId=t.id;run.rideLv=matchLv(t.id);","run.drive=t.id;run.rideT=rideTool(dk.ri);")
rep("unstick();if(save.ridePass&&dk.ri===nextRideIdx())grantRide(dk.ri);persist();}","unstick();if(save.ridePass&&dk.ri===rideNextIdx())grantRide(dk.ri);persist();}")
rep("function missionOn(i){const L=LEVELS[i];return !!(L&&L.area==='secret'&&L.tool&&save&&save.parts&&(save.parts[L.tool]||0)>=3&&save.tool<toolIdx(L.tool));}",
    "function missionOn(i){const L=LEVELS[i];return !!(L&&L.area==='secret'&&L.tool&&save&&save.parts&&(save.parts[L.tool]||0)>=3&&!owns(toolIdx(L.tool)));}")
rep("if(L.tool)return save.tool>=toolIdx(L.tool)||missionOn(i);","if(L.tool)return owns(toolIdx(L.tool))||missionOn(i);")
rep("if(L.tool&&save.tool<toolIdx(L.tool))return 'NEEDS THE '","if(L.tool&&!owns(toolIdx(L.tool)))return 'NEEDS THE '")
# which ride is next, where parts and drives come from
rep("function teaseRideIdx(){const ri=nextRideIdx();if(ri>=0)return ri;return save.tool>=toolIdx('super')&&save.tool<toolIdx('rotary')?BASE_TOOLS:-1;}",
    "function teaseRideIdx(){return save.tool>=toolIdx('super')?rideNextIdx():-1;}")
rep("function nextRideIdx(){const r=toolIdx('rotary');if(save.tool<r)return -1;const i=save.tool+1;return (i<TOOLS.length&&TOOLS[i].winter)?i:-1;}",
    "function nextRideIdx(){return save.tool>=toolIdx('rotary')?rideNextIdx():-1;}  // the ride whose parts drop")
rep("function rideForSale(){const i=nextRideIdx();return (i>=0&&save.rideSeen&&save.rideSeen[TOOLS[i].id])?i:-1;}",
    "function rideForSale(){const i=teaseRideIdx();return (i>=0&&save.rideSeen&&save.rideSeen[TOOLS[i].id])?i:-1;}")
rep("function grantRide(i){if(i<0||save.tool>=i)return false;giveMatch(i);save.tool=i;save.use=i;",
    "function grantRide(i){if(i<BASE_TOOLS||i>=TOOLS.length||owns(i))return false;save.rides=save.rides||{};save.rides[TOOLS[i].id]=true;save.use=i;")
rep("const first=!(save.rideSeen&&save.rideSeen[TOOLS[ri].id]),early=ri!==nextRideIdx();","const first=!(save.rideSeen&&save.rideSeen[TOOLS[ri].id]),early=save.tool<toolIdx('rotary');")
# regular machines only through buyTool; rides with coins from their winter, in order
rep("function buyTool(){const n=save.tool+1;if(n>=TOOLS.length||!toolAvail(n)){sfx('deny');if(n<TOOLS.length)showToast('UNLOCKS IN WINTER '+TOOLS[n].winter,'#9fd8ff');return;}const c=TOOLS[n].cost;",
    "function buyRideCoins(i){if(i!==rideNextIdx()||!toolAvail(i)){sfx('deny');return;}const c=TOOLS[i].cost;if(save.coins<c){sfx('deny');showToast('NEED '+fmt(c)+' COINS','#ff9aa8');return;}save.coins-=c;grantRide(i);}\n"
    "function buyTool(){const n=save.tool+1;if(n>=BASE_TOOLS){sfx('deny');return;}const c=TOOLS[n].cost;")
rep("  save.coins-=c;if(TOOLS[n].winter)giveMatch(n);save.tool=n;save.use=n;_tc.k='';sfx('fanfare');buzz(30);vcache.clear();showToast((TOOLS[n].winter?'WILD RIDE: ':'NEW TOOL: ')+TOOLS[n].name,'#ffd23f');",
    "  save.coins-=c;save.tool=n;save.use=n;_tc.k='';sfx('fanfare');buzz(30);vcache.clear();showToast('NEW TOOL: '+TOOLS[n].name,'#ffd23f');")
rep("  const nt=save.tool+1;if(nt<TOOLS.length&&toolAvail(nt)&&state!=='play'){","  const nt=save.tool+1;if(nt<BASE_TOOLS&&state!=='play'){")
rep("  const n=save.tool+1;if(n<TOOLS.length&&toolAvail(n))opts.push(","  const n=save.tool+1;if(n<BASE_TOOLS)opts.push(")
# using machines
rep("function useIdx(){const u=save.use;return (u==null||u<0||u>save.tool)?save.tool:u;}","function useIdx(){const u=save.use;return (u==null||!owns(u))?save.tool:u;}")
rep("function equip(i){if(i<0||i>save.tool)return;","function equip(i){if(!owns(i))return;")
# dev + test-runner shortcuts
rep("['MACHINES','blue',()=>{save.tool=TOOLS.length-1;","['MACHINES','blue',()=>{save.tool=BASE_TOOLS-1;save.rides={};for(let j=BASE_TOOLS;j<TOOLS.length;j++)save.rides[TOOLS[j].id]=true;")
rep("save.story={suburbs:true,farm:true,city:true};save.tool=TOOLS.length-1;","save.story={suburbs:true,farm:true,city:true};save.tool=BASE_TOOLS-1;save.rides={};for(let j=BASE_TOOLS;j<TOOLS.length;j++)save.rides[TOOLS[j].id]=true;")
# garage
rep("function nextRide(){return TOOLS.findIndex((t,i)=>i>=BASE_TOOLS&&!toolAvail(i));}","function nextRide(){return rideNextIdx();}")
rep("const got=TOOLS.filter((t,i)=>i>=BASE_TOOLS&&i<=save.tool).length;","const got=ridesOwned();")
rep("    if(wild&&!toolAvail(i)){// a Wild Ride you can't get yet: silhouette only",
    "    if(wild&&!owns(i)&&!(i===nr&&toolAvail(i))){// a Wild Ride you haven't got: silhouette only")
rep("    const owned=i<=save.tool,next=i===save.tool+1,afford=save.coins>=t.cost,cur=i===use,gold=isGold(t.id);",
    "    const owned=owns(i),next=wild?i===nr:i===save.tool+1,afford=save.coins>=t.cost,cur=i===use,gold=isGold(t.id),RT=wild?rideTool(i):null;")
rep("    const T2=(cur&&!chal())?tool():t;","    const T2=(cur&&!chal())?tool():RT||t;")
rep("text(b,!owned&&!next?'AFTER '+TOOLS[i-1].name:'x'+(cur?T2.value:t.value)+' COINS',x+37,y+22,",
    "text(b,!owned&&!next?'AFTER '+TOOLS[i-1].name:wild?'BEST MACHINE +15%':'x'+(cur?T2.value:t.value)+' COINS',x+37,y+22,")
rep("    else if(next){button('tool',x+w-46,y+3,42,26,afford?'orange':'grey',null,buyTool);",
    "    else if(next){button('tool',x+w-46,y+3,42,26,afford?'orange':'grey',null,wild?()=>buyRideCoins(i):buyTool);")
# peek: the next ride, and a way to get it now once you've driven it
rep("function drawRidePeek(){const tid=ridePeek,ti=toolIdx(tid),t=TOOLS[ti],isNext=ti===nextRide();",
    "function drawRidePeek(){const tid=ridePeek,ti=toolIdx(tid),t=TOOLS[ti],isNext=ti===nextRide(),sale=rideForSale()===ti;")
rep("  button('pkclose',54,246,72,18,'blue','DONE',()=>{ridePeek=null;sfx('click');});}",
    "  if(sale){const pr=SHOP.rides[t.id];button('pkgem',20,246,72,18,(save.gems||0)>=pr[1]?'purple':'grey',pr[1]+' GEMS',()=>{if(buyRide(ti,true))ridePeek=null;});button('pkclose',96,246,64,18,'blue','DONE',()=>{ridePeek=null;sfx('click');});}\n"
    "  else button('pkclose',54,246,72,18,'blue','DONE',()=>{ridePeek=null;sfx('click');});}")
# shop
rep("const msg=nx<0?(save.tool<toolIdx('rotary')?save.tool>=toolIdx('super')?['TEST DRIVES CAN TURN UP NOW.','PARTS DROP AFTER THE ROTARY']:['TEST DRIVES BEGIN ONCE YOU','OWN THE SUPER PLOW']:['YOU OWN EVERY','WILD RIDE SO FAR']):",
    "const msg=rideNextIdx()<0?['YOU OWN EVERY','WILD RIDE!']:nx<0?(save.tool>=toolIdx('super')?['TEST DRIVES CAN TURN UP NOW.','PARTS DROP AFTER THE ROTARY']:['TEST DRIVES BEGIN ONCE YOU','OWN THE SUPER PLOW']):")
# after a test drive: any time you don't own it, the keep-it offer (no more 'parts drop later' screen)
rep("  const offerRide=!r.challenge&&run.drove!=null&&save.tool<run.drove&&!run.offerShut;","  const offerRide=!r.challenge&&run.drove!=null&&!owns(run.drove)&&!run.offerShut;")
rep("  if(offerRide&&t>0.6&&run.drove!==nextRideIdx()){","  if(false){")
# a new winter shows its ride only if you don't have it
rep("const m=TOOLS.find(t=>t.winter===w);if(m)rideReveal={tid:m.id,t:0};","const m=TOOLS.find(t=>t.winter===w);if(m&&!owns(toolIdx(m.id)))rideReveal={tid:m.id,t:0};")
# upgrade titles name the machine the upgrade goes to (your best machine while a ride is in use)
rep("function upName(k){if(MACHINE_UPG.includes(k)){const t=TOOLS[useIdx()],","function upName(k){if(MACHINE_UPG.includes(k)){const t=TOOLS[toolIdx(curMachine())],")
rep("function upNameOld(k){return MACHINE_UPG.includes(k)?TOOLS[useIdx()].name","function upNameOld(k){return MACHINE_UPG.includes(k)?TOOLS[toolIdx(curMachine())].name")
# test hooks
rep("nextRideIdx:()=>nextRideIdx(),","nextRideIdx:()=>nextRideIdx(),rideNextIdx:()=>rideNextIdx(),owns:i=>owns(i),rideTool:i=>rideTool(i),buyRideCoins:i=>buyRideCoins(i),")
open(f,'w',encoding='utf-8').write(s)
print('p125 Wild Ride collection: own rides apart from the ladder, +15% on your best machine')
