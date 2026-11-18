import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Ride Mastery (Alex, Nov 18). Wild Rides keep borrowing your best machine's coin upgrades, and level up by being used:
# every job finished with a ride gives 1 point + 1 per star. 5 levels (4, 12, 28, 52, 88 points, about 25 jobs).
# Each level: +2% coins with that ride and some gems (10, 10, 15, 15, 25). Level 5: its Gold Paint, free.
# Mastery is kept through New Winter, like the rides themselves.
rep("function valueMult(){return tool().value*",
    "const MAST_PTS=[4,12,28,52,88],MAST_PER=0.02,MAST_GEMS=[10,10,15,15,25];\n"
    "function mastPts(tid){return (save.mastery&&save.mastery[tid])||0;}\n"
    "function mastLv(tid){const p=mastPts(tid);let l=0;while(l<MAST_PTS.length&&p>=MAST_PTS[l])l++;return l;}\n"
    "function mastFrac(tid){const l=mastLv(tid);if(l>=MAST_PTS.length)return 1;const a=l?MAST_PTS[l-1]:0;return (mastPts(tid)-a)/(MAST_PTS[l]-a);}\n"
    "function mastAdd(tid,pts){save.mastery=save.mastery||{};const l0=mastLv(tid);save.mastery[tid]=mastPts(tid)+pts;const l1=mastLv(tid);\n"
    "  for(let l=l0+1;l<=l1;l++){save.gems=(save.gems||0)+MAST_GEMS[l-1];const nm=SHORT_NAME[tid]||TOOLS[toolIdx(tid)].name;\n"
    "    showToast(l>=MAST_PTS.length?nm+' MASTERED! GOLD PAINT':nm+' MASTERY '+l+': +'+Math.round(MAST_PER*l*100)+'% COINS','#ffd23f');try{track('mastery_up',{ride:tid,level:l});}catch(e){}}\n"
    "  if(l1>l0){sfx('fanfare');persist();}}\n"
    "function valueMult(){return (tool().ride?1+MAST_PER*mastLv(tool().id):1)*tool().value*")
# points at the end of a job done with a ride (not test drives, missions or the weekly challenge)
rep("{const o=endRound;endRound=function(){const was=run&&run.ended;const r=o.apply(this,arguments);try{if(run&&!was&&run.res&&!run.phDone){",
    "{const o=endRound;endRound=function(){const was=run&&run.ended;const r=o.apply(this,arguments);try{if(run&&!was&&run.res&&!run.mastDone){run.mastDone=true;const t=tool();if(t&&t.ride&&!run.challenge&&!run.drive&&!run.mission)mastAdd(t.id,1+(run.res.stars||0));}}catch(e){}\n"
    "  try{if(run&&!was&&run.res&&!run.phDone){")
# level 5: its Gold Paint without Premium
rep("function skinOwned(tid,i){return i===0||(i===5&&!!save.pro)||!!save.skins[tid+':'+i];}",
    "function skinOwned(tid,i){return i===0||(i===5&&(!!save.pro||(TOOLS[toolIdx(tid)]&&toolIdx(tid)>=BASE_TOOLS&&mastLv(tid)>=MAST_PTS.length)))||!!save.skins[tid+':'+i];}")
# garage: 5 mastery pips (and progress to the next) after an owned ride's name; the coin line shows the bonus
rep("text(b,(gold?'GOLDEN ':'')+t.name+(isMk2(t.id)?' MK II':''),x+37,y+5,gold?'#a8740a':'#13306b',{outline:null});",
    "text(b,(gold?'GOLDEN ':'')+t.name+(isMk2(t.id)?' MK II':''),x+37,y+5,gold?'#a8740a':'#13306b',{outline:null});\n"
    "    if(wild&&owned){const ml=mastLv(t.id),px=x+41+textW(t.name);for(let k=0;k<5;k++){R(b,px+k*6,y+4,5,5,K);R(b,px+k*6+1,y+5,3,3,k<ml?'#ffd23f':'#d6caee');if(k<ml)R(b,px+k*6+1,y+5,3,1,'#fff08a');}if(ml<5){R(b,px,y+10,29,1,'#cbbbe8');R(b,px,y+10,Math.round(29*mastFrac(t.id)),1,'#8a50d0');}}")
rep("wild?(t.id==='ufo'?'COINS +15%, THIN BEAM':'BEST MACHINE +15%'):",
    "wild?(t.id==='ufo'?(owned&&mastLv(t.id)?'THIN BEAM MASTERY +'+2*mastLv(t.id)+'%':'COINS +15%, THIN BEAM'):(owned&&mastLv(t.id)?'BEST +15% MASTERY +'+2*mastLv(t.id)+'%':'BEST MACHINE +15%')):")
open(f,'w',encoding='utf-8').write(s)
print('p132 Ride Mastery: 5 levels per ride from jobs and stars; +2% coins and gems per level, Gold Paint at 5')
