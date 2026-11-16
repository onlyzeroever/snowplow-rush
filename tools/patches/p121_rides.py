import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Wild Rides (Alex, Nov 17): they stay rare, random and buyable, with three fixes.
# 1. Never worse on day one. A fresh ride used to clear 9-31% slower than a maxed Rotary (and test drives and missions
#    ran it with no upgrades at all). A ride you get now starts at the upgrade levels that match the best machine you
#    own, and test drives and missions use those same levels, so the ride always feels like a step up, with its higher
#    coin value and its trick on top.
rep("function bladeCells(t){t=t||tool();return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*((chal()||drv()||msn())?0:mLv(t.id).size))));}",
    "function rideLvFor(t){return (drv()||msn())&&run.rideLv&&run.rideId===t.id?run.rideLv:null;}\n"
    "function bladeCells(t){t=t||tool();const rl=rideLvFor(t);return Math.min(80,Math.round(t.width*(1+mspec(t.id).sizePer*(chal()?0:rl?rl.size:(drv()||msn())?0:mLv(t.id).size))));}\n"
    "function rateOf(id,lv){const t=TOOLS[toolIdx(id)],sp=mspec(id);return t.speed*(1+sp.speedPer*lv.speed)*Math.min(80,Math.round(t.width*(1+sp.sizePer*lv.size)));}\n"
    "function bestOwned(except){let best=0,bump=0;for(let j=0;j<=Math.min(save.tool,TOOLS.length-1);j++){const id=TOOLS[j].id;if(id===except)continue;const m=mLv(id);best=Math.max(best,rateOf(id,m));bump=Math.max(bump,m.bumper||0);}return {rate:best,bumper:bump};}\n"
    "function matchLv(id){const b0=bestOwned(id),lv={speed:0,size:0,bumper:b0.bumper};while(rateOf(id,lv)<b0.rate&&(lv.speed<MUP_LV||lv.size<MUP_LV)){if(lv.size<=lv.speed&&lv.size<MUP_LV)lv.size++;else if(lv.speed<MUP_LV)lv.speed++;else lv.size++;}return lv;}\n"
    "function giveMatch(i){const id=TOOLS[i].id,lv=matchLv(id),m=mLv(id);m.speed=Math.max(m.speed,lv.speed);m.size=Math.max(m.size,lv.size);m.bumper=Math.max(m.bumper||0,lv.bumper);}")
rep("function curLv(){if(chal()||drv()||msn())return ZERO_LV;",
    "function curLv(){if(chal())return ZERO_LV;if(drv()||msn()){const rl=run.rideLv;return rl?{speed:rl.speed,size:rl.size,bumper:rl.bumper,value:save.lv.value,helpers:save.lv.helpers}:ZERO_LV;}")
rep("function grantRide(i){if(i<0||save.tool>=i)return false;save.tool=i;",
    "function grantRide(i){if(i<0||save.tool>=i)return false;giveMatch(i);save.tool=i;")
rep("save.coins-=c;save.tool=n;save.use=n;_tc.k='';sfx('fanfare');","save.coins-=c;if(TOOLS[n].winter)giveMatch(n);save.tool=n;save.use=n;_tc.k='';sfx('fanfare');")
rep("run.mission=LEVELS[idx].tool;G.driveKey=null;","run.mission=LEVELS[idx].tool;run.rideId=run.mission;run.rideLv=matchLv(run.mission);G.driveKey=null;")
rep("run.drive=t.id;run.driveT=SHOP.driveSecs;","run.drive=t.id;run.rideId=t.id;run.rideLv=matchLv(t.id);run.driveT=SHOP.driveSecs;")
# 2. Pity timer. Parts stay random (45%, then 30% a job), but after PART_PITY-1 eligible jobs without finding one,
#    every job has a part until you find it.
rep("if(n<3&&Math.random()<(n===0?0.45:0.3)){",
    "if(n<3&&(Math.random()<(n===0?0.45:0.3)||(save.partDry||0)>=PART_PITY-1)){")
rep("function checkPart(br){const pt=G.part;if(!pt||pt.found||!overlap(br,{x:pt.x-5,y:pt.y-5,w:10,h:10}))return;pt.found=true;",
    "const PART_PITY=8;   // the 8th job in a row without a part always has one\n"
    "function checkPart(br){const pt=G.part;if(!pt||pt.found||!overlap(br,{x:pt.x-5,y:pt.y-5,w:10,h:10}))return;pt.found=true;save.partDry=0;")
rep("function endRound(allClear){\n  run.ended=true;",
    "function endRound(allClear){\n  if(!run.challenge&&!run.mission&&!(G.part&&G.part.found)){const ri=nextRideIdx();if(ri>=0&&((save.parts||{})[TOOLS[ri].id]||0)<3)save.partDry=(save.partDry||0)+1;}\n  run.ended=true;")
# 3. Tease earlier. From the Super Plow on (Theme Park), a Monster Truck test drive can turn up before you own the
#    Rotary (half the jobs until you've tried it, then 1 in 10). Parts still only drop after the Rotary. Buying the ride
#    outright before then would skip the Snowcat and Rotary, so the offer after an early drive is the Wild Ride Pass,
#    which hands over each ride as soon as it can be yours.
rep("function nextRideIdx(){",
    "function teaseRideIdx(){const ri=nextRideIdx();if(ri>=0)return ri;return save.tool>=toolIdx('super')&&save.tool<toolIdx('rotary')?BASE_TOOLS:-1;}\n"
    "function nextRideIdx(){")
rep("g.driveKey=null;{const ri=nextRideIdx();if(ri>=0&&!LEVELS[idx].tool){const first=!(save.rideSeen&&save.rideSeen[TOOLS[ri].id]);if(Math.random()<(first?0.5:SHOP.driveChance)){",
    "g.driveKey=null;{const ri=teaseRideIdx();if(ri>=0&&!LEVELS[idx].tool){const first=!(save.rideSeen&&save.rideSeen[TOOLS[ri].id]),early=ri!==nextRideIdx();if(Math.random()<(first?0.5:early?0.1:SHOP.driveChance)){")
rep("unstick();if(save.ridePass)grantRide(dk.ri);persist();}","unstick();if(save.ridePass&&dk.ri===nextRideIdx())grantRide(dk.ri);persist();}")
rep("if(offerRide&&t>0.6){const ti=run.drove,T3=TOOLS[ti],pr=SHOP.rides[T3.id];b.fillStyle='rgba(11,24,56,0.6)';b.fillRect(0,0,W,H);panel(16,80,148,156,'#13306b','#ffd23f');",
    "if(offerRide&&t>0.6&&run.drove!==nextRideIdx()){const T3=TOOLS[run.drove];b.fillStyle='rgba(11,24,56,0.6)';b.fillRect(0,0,W,H);panel(16,80,148,156,'#13306b','#ffd23f');\n"
    "    text(b,'ENJOYED THE TEST DRIVE?',W/2,88,'#ffd23f',{align:'center'});R(b,62,100,56,44,'#cfe3f8');drawToolIcon(T3.id,70,102,40);\n"
    "    text(b,'ITS PARTS DROP AFTER YOU',W/2,150,'#ffffff',{align:'center',outline:null});text(b,'OWN THE ROTARY BLOWER',W/2,158,'#ffffff',{align:'center',outline:null});\n"
    "    if(!save.ridePass){button('rop',24,170,132,18,'gold','WILD RIDE PASS '+SHOP.ridePass.price,()=>{buyRidePass();run.offerShut=true;});text(b,'ALL 5 RIDES, AS THEY UNLOCK',W/2,192,'#9fc0e8',{align:'center',outline:null});}\n"
    "    else text(b,'YOUR PASS HANDS IT OVER THEN',W/2,178,'#ffd23f',{align:'center',outline:null});\n"
    "    button('ron',24,204,132,16,'blue','GOT IT',()=>{run.offerShut=true;sfx('click');});}\n"
    "  else if(offerRide&&t>0.6){const ti=run.drove,T3=TOOLS[ti],pr=SHOP.rides[T3.id];b.fillStyle='rgba(11,24,56,0.6)';b.fillRect(0,0,W,H);panel(16,80,148,156,'#13306b','#ffd23f');")
# the shop's Wild Ride tab: say when test drives start, now that they come earlier
rep("['TEST DRIVES BEGIN ONCE YOU','OWN THE ROTARY BLOWER']","save.tool>=toolIdx('super')?['TEST DRIVES CAN TURN UP NOW.','PARTS DROP AFTER THE ROTARY']:['TEST DRIVES BEGIN ONCE YOU','OWN THE SUPER PLOW']")
# Garage peek at the next Wild Ride: lead with the parts route (and its count), then the New Winter route.
rep("text(b,'ARRIVES IN WINTER '+t.winter,W/2,192,'#ffd23f',{align:'center'});\n    const ts=totalStars(),need=starsNeeded();text(b,'EARN '+need+' STARS, THEN',W/2,206,'#ffffff',{align:'center',outline:null});text(b,'START A NEW WINTER',W/2,215,'#ffffff',{align:'center',outline:null});",
    "const pn=(save.parts||{})[t.id]||0,afterRot=save.tool>=toolIdx('rotary');text(b,afterRot?'PARTS FOUND: '+pn+' OF 3':'PARTS DROP AFTER THE ROTARY',W/2,192,'#ffd23f',{align:'center'});\n"
    "    const ts=totalStars(),need=starsNeeded();text(b,'OR EARN '+need+' STARS AND',W/2,206,'#ffffff',{align:'center',outline:null});text(b,'START WINTER '+t.winter,W/2,215,'#ffffff',{align:'center',outline:null});")
open(f,'w',encoding='utf-8').write(s)
print('p121 wild rides: day-one match, pity timer (8), early test drives')
