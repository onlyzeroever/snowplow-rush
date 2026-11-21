# Alex, Nov 21 20:23/20:47: "why is the gap so big? ... the rest needs tidying up" / "do we need the next job button?
# We removed the switcher cause it was cluttered ... what would the pros do?"
# p148 widened WEEKLY and SHOP into the old map/list switcher's place, but new players don't have WEEKLY (or the daily
# calendar) until the daily jobs unlock after 4 runs, so their bottom row was the chest, a 66 px hole, then SHOP.
# Pros keep a menu's layout the same from the first minute and show what's coming as dimmed, locked buttons, so nothing
# jumps around when it unlocks. So: WEEKLY and the calendar sit in their places from the start, grey with a padlock;
# a tap says how many jobs until they unlock. No extra buttons.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function drawMapChrome(){",
    "function unlockMsg(what){const n=Math.max(1,4-(save.fbRuns||0));return what+' UNLOCK IN '+n+' JOB'+(n>1?'S':'');}\n"
    "function drawMapChrome(){")
rep("if(dailyOn()){button('daily',114,2-hop,20,17,'red',null,()=>{ensureDaily();dailyOpen=true;sfx('click');});b.drawImage(SPR.cal,119,6-hop);if(dn)badge(127,0,''+dn);else if(dNew)badge(127,0,'!');}",
    "if(dailyOn()){button('daily',114,2-hop,20,17,'red',null,()=>{ensureDaily();dailyOpen=true;sfx('click');});b.drawImage(SPR.cal,119,6-hop);if(dn)badge(127,0,''+dn);else if(dNew)badge(127,0,'!');}\n"
    "  else{button('dailyLock',114,2,20,17,'grey',null,()=>{sfx('deny');showToast(unlockMsg('DAILY JOBS'),'#9fd8ff');});b.globalAlpha=0.4;b.drawImage(SPR.cal,119,6);b.globalAlpha=1;b.drawImage(SPR.lock,126,9);}")
rep("const ww=LIST_TOGGLE?44:62,sx=LIST_TOGGLE?121:95,sw=LIST_TOGGLE?40:66;",
    "const ww=LIST_TOGGLE?44:62,sx=LIST_TOGGLE?121:95,sw=LIST_TOGGLE?40:66;\n"
    "  if(!LIST_TOGGLE&&!dailyOn()){button('weeklyLock',29,by,ww,18,'grey','WEEKLY',()=>{sfx('deny');showToast(unlockMsg('WEEKLY CHALLENGES'),'#9fd8ff');});b.drawImage(SPR.lock,29+ww-12,by+5);}")
open(f,'w',encoding='utf-8').write(s)
print('p169 map: WEEKLY and the daily calendar in place from the start, locked until the daily jobs unlock')
