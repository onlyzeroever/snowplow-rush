# Section 2/3 (apps): the game side of the native layer, used only when window.SRNative is there (no change on the web).
#  - save mirror: every save also goes to the native layer (phone storage + iCloud key-value / Android backup), at most
#    every 5 s and whenever the game goes to the background; on launch, if the browser storage is empty (reinstall, new
#    phone), the game starts from window.SRNativeSave[key], which the native layer injects at document start;
#  - reminders (local notifications, no server): when the game goes to the background it hands the native layer a plan:
#    helper shed full, daily gift + streak (next day 18:00), weekend event starting; the native layer replaces the
#    previous plan each time. At most one a day is the native layer's job (see APP_HANDOFF.md);
#  - the permission is asked after the player's first three-star job, with an in-game card first ("a nudge when your
#    helpers are done?"), so iOS's one-time prompt only shows to players who said yes;
#  - analytics say which app sent them (platform = ios / android from SRNative.platform, web otherwise).
# Held with p162/p163 until the apps exist.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function loadSave(){try{let s=JSON.parse(localStorage.getItem(SAVE_KEY)||'null');",
    "function loadSave(){try{let s=JSON.parse(localStorage.getItem(SAVE_KEY)||(window.SRNativeSave&&window.SRNativeSave[SAVE_KEY])||'null');")
rep("rv:RV,v:'0.8.0',", "rv:RV,v:'0.8.0',platform:(window.SRNative&&SRNative.platform)||'web',")
HOOKS = r"""
// ---------------- APP HOOKS (p165): save mirror, reminders; only when the native layer is there ----------------
const APPH={t:0,timer:0};
function appSaveMirror(now){const N=window.SRNative;if(!N||typeof N.storeSave!=='function'||window.__noPersist)return;
  const go=()=>{APPH.timer=0;APPH.t=Date.now();try{N.storeSave(SAVE_KEY,JSON.stringify(save));}catch(e){}};
  if(now||Date.now()-APPH.t>5000){if(APPH.timer){clearTimeout(APPH.timer);APPH.timer=0;}go();}else if(!APPH.timer)APPH.timer=setTimeout(go,5000-(Date.now()-APPH.t));}
{const o=persist;persist=function(){const r=o.apply(this,arguments);appSaveMirror(false);return r;};}
function reminderPlan(){const out=[],now=Date.now(),tom=new Date();tom.setDate(tom.getDate()+1);tom.setHours(18,0,0,0);
  if(save.lv&&save.lv.helpers>0)out.push({id:'shed',at:now+offCap()*1000,title:'The helper shed is full',body:'Your helpers have been plowing. Come and collect the coins!'});
  const st=save.streak;out.push({id:'daily',at:tom.getTime(),title:st&&st.n>1?'Keep your '+st.n+'-day streak going':'Your daily gift is ready',body:'One quick job keeps the snow under control.'});
  for(const e of (typeof EVENTS!=='undefined'?EVENTS:[])){if(!e||e.test||!(e.start>now))continue;const d=EVENT_DEFS[e.kind];out.push({id:'event-'+e.id,at:e.start,title:(d&&d.name?d.name:'A weekend event')+' starts now',body:'A new event is on this weekend. Jump in!'});}
  return out.filter(r=>r.at>now+60000).sort((a,c)=>a.at-c.at);}
document.addEventListener('visibilitychange',()=>{if(!document.hidden)return;appSaveMirror(true);const N=window.SRNative;
  if(N&&typeof N.scheduleReminders==='function'&&save.remindOk)try{N.scheduleReminders(reminderPlan());}catch(e){}});
// ask for reminders after the first three-star job: our own card first, the phone's one-time prompt only after a yes
var remindAsk=false;
{const o=endRound;endRound=function(){const was=run&&run.ended;const r=o.apply(this,arguments);try{const N=window.SRNative;
  if(N&&typeof N.askReminders==='function'&&run&&!was&&run.res&&run.res.stars>=3&&!save.remindAsked&&!run.challenge)remindAsk=true;}catch(e){}return r;};}
function drawRemindAsk(){const x=14,y=96,w=152,h=104;b.fillStyle='rgba(11,24,56,0.8)';b.fillRect(0,0,W,H);panel(x,y,w,h,'#13306b','#ffd23f');
  text(b,'A FRIENDLY NUDGE?',W/2,y+9,'#ffd23f',{align:'center',scale:2});
  text(b,'WE CAN TELL YOU WHEN YOUR',W/2,y+30,'#ffffff',{align:'center',outline:null});text(b,'HELPERS ARE DONE AND WHEN',W/2,y+40,'#ffffff',{align:'center',outline:null});text(b,'A WEEKEND EVENT STARTS.',W/2,y+50,'#ffffff',{align:'center',outline:null});
  text(b,'AT MOST ONE A DAY.',W/2,y+62,'#9fc0e8',{align:'center',outline:null});
  const done=yes=>{remindAsk=false;save.remindAsked=true;persist();sfx('click');if(!yes)return;const N=window.SRNative;
    Promise.resolve().then(()=>N.askReminders()).then(ok=>{save.remindOk=!!ok;persist();if(ok)showToast('NUDGES ON','#7fe08a');}).catch(()=>{});};
  button('rmyes',x+10,y+76,64,18,'green','YES PLEASE',()=>done(true));button('rmno',x+78,y+76,64,18,'navy','NO THANKS',()=>done(false));}
"""
rep("// ---------------- STORE + ADS BRIDGE (p163)", HOOKS.lstrip('\n')+"// ---------------- STORE + ADS BRIDGE (p163)")
# the card shows on the map, on top of everything else
rep("if(adScreen)drawAd();if(IAP&&IAP.busy)drawStoreBusy();",
    "if(remindAsk&&state==='map'&&!adScreen&&!(IAP&&IAP.busy))drawRemindAsk();if(adScreen)drawAd();if(IAP&&IAP.busy)drawStoreBusy();")
rep("function overlayOpen(){return !!(ridePeek||rideReveal||settingsOpen||","function overlayOpen(){return !!(ridePeek||rideReveal||(remindAsk&&state==='map')||settingsOpen||")
open(f,'w',encoding='utf-8').write(s)
print('p165 app hooks: save mirror to the phone, reminders plan, nudge card after the first three-star job')
