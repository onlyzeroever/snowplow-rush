import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Premium "rewards without ads" (Alex, Nov 17): Premium players had to press a "PREMIUM: x2" button for rewards that are
# always worth taking. Now those rewards apply by themselves and the screen says so, which is how ad-free passes
# usually work. Rewards that are a real choice (the +15 s continue, gems in the shop) keep their buttons.
# 1. Results: the x2 on the run's coins is paid as the results open, shown as a gold line where the button was.
rep("const adBtn=(x,w)=>save.pro?button('rad',x,py+148,w,16,'gold',w>80?'PREMIUM: x2 COINS':'PREMIUM: x2',()=>{run.adUsed=true;const rw=Math.floor(run.earned);save.coins+=rw;sfx('buy');showToast('+'+fmt(rw)+' COINS','#ffd23f');persist();})",
    "if(save.pro&&canAd){run.adUsed=true;run.proDbl=Math.floor(run.earned);save.coins+=run.proDbl;sfx('buy');persist();if(canBoost)showToast('PREMIUM x2: +'+fmt(run.proDbl)+' COINS','#ffd23f');}\n"
    "    if(run.proDbl&&!canBoost){R(b,18,py+148,144,16,'#3a2a08');R(b,19,py+149,142,14,'#7a5a14');b.drawImage(SPR.coin,30,py+152);text(b,'PREMIUM x2:  +'+fmt(run.proDbl),W/2+5,py+153,'#ffd23f',{align:'center'});}\n"
    
    "    const adBtn=(x,w)=>save.pro?null")
# 2. Welcome back: helpers' coins are doubled on arrival for Premium; one COLLECT button, a PREMIUM x2 tag on the amount.
rep("offlineGain=helperIncome()*Math.min(offCap(),away)*OFFLINE_RATE;save.coins+=offlineGain;",
    "offlineGain=helperIncome()*Math.min(offCap(),away)*OFFLINE_RATE*(save.pro?2:1);save.coins+=offlineGain;")
rep("button('collect',22,168,66,14,'green','COLLECT',()=>{offlineGain=0;sfx('buy');goMap();});\n    button('offad',",
    "button('collect',save.pro?52:22,168,save.pro?76:66,14,'green','COLLECT',()=>{offlineGain=0;sfx('buy');goMap();});\n    if(!save.pro)button('offad',")
rep("text(b,full?'FULL! THEY STOP AFTER '+fmtDur(offCap()):'THEY WORK UP TO '+fmtDur(offCap())+' WHILE AWAY',W/2,155,full?'#ffd23f':'#9fc0e8',{align:'center',outline:null});",
    "text(b,save.pro?(full?'FULL! ':'')+'PREMIUM x2, UP TO '+fmtDur(offCap()):full?'FULL! THEY STOP AFTER '+fmtDur(offCap()):'THEY WORK UP TO '+fmtDur(offCap())+' WHILE AWAY',W/2,155,save.pro||full?'#ffd23f':'#9fc0e8',{align:'center',outline:null});")
# durations: "12H" not "12H 0M"
rep("return d?d+'D '+h+'H':h?h+'H '+m+'M':Math.max(1,m)+'M';}","return d?d+'D'+(h?' '+h+'H':''):h?h+'H'+(m?' '+m+'M':''):Math.max(1,m)+'M';}")
open(f,'w',encoding='utf-8').write(s)
print('p120 premium rewards apply by themselves')
