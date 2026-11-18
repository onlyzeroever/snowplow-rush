import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# First-session fixes from the Nov 18 first-15-minutes audit (PostHog data + a fresh-phone walkthrough).
# 1. One tap to play: a brand-new player's first tap on the title goes straight into job 1 (was 5 taps, 15-20 s).
#    The privacy notice moves to the title screen (small print, shown until seen) with a settings cog,
#    so it no longer covers job 1 on the map. The suburbs story now shows after job 1 and reads that way.
# 2. Job 1 is a sure win: the driveway gets 90 s (was 60) and stars at 30/55/80% (was 35/60/85).
#    Real first tries ended at 41-80% at 60 s; nobody got 3 stars first time.
# 3. No "watch an ad for +15 seconds" pop-up in a player's first 3 jobs.
# 4. The results title says how it went: NICE WORK! / GREAT JOB! / SUPERB! (was TIME'S UP! even with 2 stars).
# 5. Daily jobs and the weekly race wait until the player has done 4 jobs (or has stars on 3 jobs):
#    no daily pop-up straight after job 1, no daily or weekly buttons in the first few minutes.
# 6. The job card says TIME 60S / PAY x1.3 and STARS AT 35%, 60%, 85% CLEARED (was BEST 0% x1 PAY 60S).

# 1. title: notice + cog, one tap into job 1
rep("text(b,'PLAYTEST V0.8.0',W/2,304,'#8fa8cc',{align:'center',outline:null});",
    "text(b,'PLAYTEST V0.8.0',W/2,304,'#8fa8cc',{align:'center',outline:null});\n"
    "  if(!offlineGain){button('tgear',W-20,2,18,17,'blue',null,()=>{settingsOpen=true;sfx('click');});b.drawImage(SPR.gear,W-15,6);\n"
    "    if(!save.privSeen){const c='#5b7bab';text(b,'WE COUNT PLOWS, NOT PEOPLE.',W/2,274,c,{align:'center',outline:null});text(b,'WE MAY RECORD YOUR FIRST PLAYS,',W/2,282,c,{align:'center',outline:null});text(b,'ANONYMOUSLY. WE NEVER SELL IT.',W/2,290,c,{align:'center',outline:null});}}")
rep("function overlayOpen(){",
    "function titleGo(){sfx('click');const fresh=!save.privSeen;if(fresh){save.privSeen=true;track('privacy_notice',{choice:'title'});persist();}\n"
    "  if(fresh&&!(save.fbRuns>0)&&!save.best.some(v=>v>0)){track('ftue_direct');startLevelUI(0);return;}goMap();}\n"
    "function overlayOpen(){")
rep("if(state==='title'){if(!offlineGain)goMap();return;}","if(state==='title'){if(!offlineGain)titleGo();return;}")
rep("if(e.key===' '&&state==='title')goMap();","if(e.key===' '&&state==='title'&&!offlineGain&&!overlayOpen())titleGo();")
rep("suburbs:['THE BIG SNOW IS HERE!','THE WHOLE TOWN IS BURIED.','GRAB A SHOVEL AND START','WITH YOUR OWN DRIVEWAY.']",
    "suburbs:['THE BIG SNOW IS HERE!','THE WHOLE TOWN IS BURIED.','YOUR DRIVEWAY WAS JUST','THE START. HELP THE STREET!']")

# 2. job 1 is a sure win
rep("{id:'driveway',name:'DRIVEWAY',     area:'suburbs',h:260, time:60,value:1,   stars:[35,60,85],",
    "{id:'driveway',name:'DRIVEWAY',     area:'suburbs',h:260, time:90,value:1,   stars:[30,55,80],")

# 3. no +15 s ad pop-up in the first 3 jobs
rep("if(!run.contUsed&&!run.challenge&&st<3){","if(!run.contUsed&&!run.challenge&&st<3&&(save.fbRuns||0)>=3){")

# 4. results title
rep("text(b,r.allClear?'ALL CLEAR!':close?'SO CLOSE!':\"TIME'S UP!\",W/2,py+10,fl?'#ffffff':r.allClear?'#7fe08a':close?'#ffd23f':'#ffffff',{align:'center',scale:2});",
    "const hd=r.allClear?'ALL CLEAR!':close?'SO CLOSE!':(r.challenge||!r.stars)?\"TIME'S UP!\":['','NICE WORK!','GREAT JOB!','SUPERB!'][Math.min(3,r.stars)];\n"
    "  text(b,hd,W/2,py+10,fl?'#ffffff':r.allClear?'#7fe08a':close?'#ffd23f':(!r.challenge&&r.stars>=3)?'#ffd23f':'#ffffff',{align:'center',scale:2});")

# 5. daily + weekly wait for job 4
rep("function dailyAdd(type,n,setTo){if(!save.daily)return;",
    "function dailyOn(){if(save.dailyEver)return true;if((save.fbRuns||0)>=4||save.best.filter(v=>v>0).length>=3){save.dailyEver=true;return true;}return false;}\n"
    "function dailyAdd(type,n,setTo){if(!save.daily||!dailyOn())return;")
rep("else if(dailyNew()&&(save.ach.first||save.best.some(v=>v>0)))dailyOpen='new';","else if(dailyNew()&&dailyOn())dailyOpen='new';")
rep("button('daily',114,2-hop,20,17,'red',null,()=>{ensureDaily();dailyOpen=true;sfx('click');});b.drawImage(SPR.cal,119,6-hop);if(dn)badge(127,0,''+dn);else if(dNew)badge(127,0,'!');",
    "if(dailyOn()){button('daily',114,2-hop,20,17,'red',null,()=>{ensureDaily();dailyOpen=true;sfx('click');});b.drawImage(SPR.cal,119,6-hop);if(dn)badge(127,0,''+dn);else if(dNew)badge(127,0,'!');}")
rep("button('weekly',29,by,44,18,'gold','WEEKLY',()=>{weeklyOpen=true;weeklyTab=0;save.weeklySeen=weekNo();sfx('click');persist();});if(!weeklyState().claimed&&save.weeklySeen!==weekNo()){R(b,68,by-2,6,6,K);R(b,69,by-1,4,4,'#e8283f');}",
    "if(dailyOn()){button('weekly',29,by,44,18,'gold','WEEKLY',()=>{weeklyOpen=true;weeklyTab=0;save.weeklySeen=weekNo();sfx('click');persist();});if(!weeklyState().claimed&&save.weeklySeen!==weekNo()){R(b,68,by-2,6,6,K);R(b,69,by-1,4,4,'#e8283f');}}")

# 6. plain job card
rep("text(b,'BEST '+save.best[i]+'%   x'+L.value+' PAY   '+L.time+'S',W/2,160,'#ffd23f',{align:'center',outline:null});text(b,'STARS AT '+L.stars.join(' / ')+'%',W/2,170,'#9fc0e8',{align:'center',outline:null});",
    "text(b,(save.best[i]>0?'BEST '+save.best[i]+'%   ':'')+'TIME '+L.time+'S   PAY x'+L.value,W/2,160,'#ffd23f',{align:'center',outline:null});text(b,'STARS AT '+L.stars.join('%, ')+'% CLEARED',W/2,170,'#9fc0e8',{align:'center',outline:null});")

# safety: the job card never draws before the map art exists
rep("R(b,51,47,78,56,K);b.drawImage(mapArt,clamp(lm[0]-19,0,W-38)","R(b,51,47,78,56,K);if(mapArt)b.drawImage(mapArt,clamp(lm[0]-19,0,W-38)")
open(f,'w',encoding='utf-8').write(s)
print('p134 first session: one tap into job 1, notice on title, 90 s driveway, no early +15 s pop-up, happier results title, dailies after job 4, plain job card')
