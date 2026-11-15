import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:90])
    s=s.replace(a,b)
# ANALYTICS (Nov 15, Alex): PostHog, US cloud. A tiny built-in tracker (no SDK): anonymous random player id, batched
# events every 15 s and when the app is hidden, an on/off switch in Settings (on by default for the playtest), nothing
# sent from test runs, dev and review builds tagged so they can be filtered out.
PH_KEY='phc_rsyr9aojYGfzg9soKfxKJ4huRSwAdKSne49SpsiGK8bH'
rep("const dt=Math.min(0.05,(now-last)/1000);last=now;","const dt=Math.min(0.05,(now-last)/1000);last=now;if(state==='play'){PH.frames++;if(now-PH.lastF>34)PH.slow++;}PH.lastF=now;")
rep("catch(err){console.error(err);}","catch(err){console.error(err);trackErr(err&&err.message,err&&err.stack);}")
rep("run.moved=true;save.tut=true;","run.moved=true;if(!save.tut)track('tutorial_done',{job:G.def.id});save.tut=true;")
rep("if(adScreen.t<=0){","if(adScreen.t<=0){track('ad_watched',{kind:adScreen.gems?'free_gems':adScreen.onDone?'reward':'coins',screen:state});")
rep("button('sg'+i,x+3,y+30,w-6,13,'green',g.price,()=>{save.gems=(save.gems||0)+g.gems;","button('sg'+i,x+3,y+30,w-6,13,'green',g.price,()=>{track('iap_test',{item:'gems_'+g.gems,price:g.price});save.gems=(save.gems||0)+g.gems;")
# Settings: an on/off switch for play data (panel grows by 22px)
rep("panel(14,60,152,170,'#13306b','#ffd23f');","panel(14,60,152,192,'#13306b','#ffd23f');")
rep("button('rst',24,176,132,16,","button('trk',24,176,132,16,save.noTrack?'grey':'blue',save.noTrack?'SHARE PLAY DATA: OFF':'SHARE PLAY DATA: ON',()=>{if(save.noTrack){save.noTrack=false;track('analytics_on');}else{track('analytics_off');phFlush(true);save.noTrack=true;}persist();sfx('click');});\n  button('rst',24,198,132,16,")
rep("button('close',54,204,72,18,'orange','DONE',()=>{settingsOpen=false;sfx('click');});}","button('close',54,226,72,18,'orange','DONE',()=>{settingsOpen=false;sfx('click');});}")
block=r"""
// ---------------- ANALYTICS (PostHog) ----------------
const PH={key:'%s',host:'https://us.i.posthog.com',q:[],sid:null,last:0,errs:0,frames:0,slow:0,lastF:0,jobT:0,rideVia:null};
function phOn(){return !TEST_MODE&&!save.noTrack&&typeof fetch==='function';}
const PH_ID=(()=>{let id=null;try{id=localStorage.getItem('sr.aid');}catch(e){}if(!id){id='p_'+Date.now().toString(36)+Math.random().toString(36).slice(2,10);try{localStorage.setItem('sr.aid',id);}catch(e){}}return id;})();
function phSession(){const now=Date.now();if(!PH.sid||now-PH.last>30*60e3)PH.sid=now.toString(36)+Math.random().toString(36).slice(2,8);PH.last=now;return PH.sid;}
function track(ev,props){try{if(!phOn())return;const t=TOOLS[useIdx()];
  const p=Object.assign({distinct_id:PH_ID,$session_id:phSession(),$lib:'snowplow-rush',$geoip_disable:true,build:DEV_MODE?'dev':REVIEW_MODE?'review':'live',v:'0.8.0',winter:winterNo(),machine:t?t.id:null,stars_total:totalStars(),coins:Math.round(save.coins),gems:save.gems||0,premium:!!save.pro},props||{});
  PH.q.push({event:ev,properties:p,timestamp:new Date().toISOString()});if(PH.q.length>=25)phFlush(false);}catch(e){}}
function phForm(batch){const ev=batch.map(e=>({event:e.event,timestamp:e.timestamp,properties:Object.assign({token:PH.key},e.properties)}));let b64='';try{b64=btoa(unescape(encodeURIComponent(JSON.stringify(ev))));}catch(e){return null;}return 'data='+encodeURIComponent(b64);}
function phSendForm(batch,final){const body=phForm(batch);if(!body)return;const url=PH.host+'/e/?compression=base64';
  try{if(final&&navigator.sendBeacon&&navigator.sendBeacon(url,new Blob([body],{type:'application/x-www-form-urlencoded'})))return;}catch(e){}
  try{fetch(url,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body,keepalive:!!final}).catch(()=>{});}catch(e){}}
function phFlush(final){if(!PH.q.length||!phOn()){if(!phOn())PH.q.length=0;return;}const batch=PH.q.splice(0,PH.q.length);
  // JSON to /batch/ first; if the browser blocks it (CORS) or it fails, fall back to the simple form post that never needs a preflight, and stick with it
  if(PH.form||final){phSendForm(batch,final);return;}
  try{fetch(PH.host+'/batch/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({api_key:PH.key,batch})}).then(r=>{if(!r.ok)throw new Error('http '+r.status);}).catch(()=>{PH.form=true;phSendForm(batch,false);});}catch(e){PH.form=true;phSendForm(batch,false);}}
function trackErr(msg,where){if(PH.errs>=5)return;PH.errs++;track('error',{msg:String(msg||'').slice(0,200),where:String(where||'').slice(0,400),screen:state});}
setInterval(()=>phFlush(false),15000);
document.addEventListener('visibilitychange',()=>{if(document.hidden){let hp={screen:state};try{if(state==='play'&&PH.jobT)Object.assign(hp,phJob(),{pct:G?Math.round(G.cleared/G.clearable*100):null,secs:Math.round((Date.now()-PH.jobT)/1000)});}catch(e){}track('app_hidden',hp);phFlush(true);}});
window.addEventListener('pagehide',()=>phFlush(true));
window.addEventListener('error',e=>trackErr(e.message,(e.filename||'')+':'+e.lineno));
window.addEventListener('unhandledrejection',e=>trackErr('promise: '+(e.reason&&e.reason.message||e.reason),''));
const phJob=()=>{const L=G&&G.def;return L?{job:L.id,area:L.area}:{};};
{const o=startLevel;startLevel=function(idx,opts){const r=o.apply(this,arguments);try{const L=LEVELS[idx];PH.jobT=Date.now();PH.frames=0;PH.slow=0;
  track('job_start',{job:L.id,area:L.area,job_no:L.area==='secret'?null:jobNo(idx),attempt:(save.fails[idx]||0)+1,stars_before:save.stars[idx]||0,weekly:!!(opts&&opts.challenge),mission:missionOn(idx),boss:!!L.boss});}catch(e){}return r;};}
{const o=endRound;endRound=function(){const was=run&&run.ended;const r=o.apply(this,arguments);try{if(run&&!was&&run.res&&!run.phDone){run.phDone=true;const R2=run.res;
  track('job_end',Object.assign(phJob(),{pct:Math.round(R2.pct),stars:R2.stars,all_clear:!!R2.allClear,earned:Math.round(run.earned||0),bonus:Math.round(R2.bonus||0),hits:run.hits||0,gifts:run.gifts||0,continue_used:!!run.contUsed,time_left:Math.round(run.time||0),secs:Math.round((Date.now()-PH.jobT)/1000),slow_frames_pct:PH.frames?Math.round(PH.slow/PH.frames*100):null,weekly:!!run.challenge,score:R2.challenge?R2.challenge.score:null}));}}catch(e){}return r;};}
for(const [nm,get,set] of [['map',()=>goMap,f=>goMap=f],['garage',()=>goGarage,f=>goGarage=f],['upgrades',()=>goUpgrades,f=>goUpgrades=f]]){const o=get();set(function(){try{if(state==='play'&&run&&!run.ended)track('job_quit',Object.assign(phJob(),{pct:G?Math.round(G.cleared/G.clearable*100):null,secs:Math.round((Date.now()-PH.jobT)/1000)}));if(state!==nm)track('screen',{name:nm,from:state});}catch(e){}return o.apply(this,arguments);});}
{const o=buyUpg;buyUpg=function(k){const c0=save.coins;const r=o.apply(this,arguments);try{if(save.coins<c0)track('upgrade_buy',{kind:k,machine:curMachine(),level:lvOf(k),cost:Math.round(c0-save.coins)});}catch(e){}return r;};}
{const o=buyTool;buyTool=function(){const t0=save.tool,c0=save.coins;const r=o.apply(this,arguments);try{if(save.tool>t0)track('machine_buy',{bought:TOOLS[save.tool].id,cost:Math.round(c0-save.coins)});}catch(e){}return r;};}
{const o=buyRide;buyRide=function(i,gems){PH.rideVia=gems?'gems':'iap_test';try{return o.apply(this,arguments);}finally{PH.rideVia=null;}};}
{const o=grantRide;grantRide=function(i){const r=o.apply(this,arguments);try{if(r)track('ride_get',{ride:TOOLS[i].id,via:PH.rideVia||(state==='play'&&run&&run.drive?'test_drive_offer':'earned')});}catch(e){}return r;};}
{const o=tryBuy;tryBuy=function(price){const c0=save.coins,g0=save.gems||0;const r=o.apply(this,arguments);try{if(r!==false&&(save.coins<c0||(save.gems||0)<g0))track('spend',{coins:Math.round(c0-save.coins),gems:g0-(save.gems||0),what:skinFor?'skin':outfitsOpen?'outfit':trailsOpen?'trail':jobInfo>=0?'road_fee':shopOpen?'shop':state});}catch(e){}return r;};}
for(const [nm,get,set] of [['premium',()=>shopBuyPremium,f=>shopBuyPremium=f],['starter',()=>shopBuyStarter,f=>shopBuyStarter=f],['ride_pass',()=>buyRidePass,f=>buyRidePass=f]]){const o=get();set(function(){const r=o.apply(this,arguments);try{track('iap_test',{item:nm});}catch(e){}return r;});}
{const o=startNewWinter;startNewWinter=function(){const r=o.apply(this,arguments);try{track('new_winter',{winter_now:winterNo()});}catch(e){}return r;};}
{const o=checkPart;checkPart=function(){const b4=JSON.stringify(save.parts||{});const r=o.apply(this,arguments);try{const a=save.parts||{};if(JSON.stringify(a)!==b4)for(const k in a)track('part_found',Object.assign(phJob(),{ride:k,parts:a[k]}));}catch(e){}return r;};}
{const o=openShop;openShop=function(){try{track('shop_open',{screen:state});}catch(e){}return o.apply(this,arguments);};}
{const o=resetSave;resetSave=function(){try{track('save_reset');}catch(e){}return o.apply(this,arguments);};}
track('session_start',{returning:!!save.tut,away_min:Math.round((offlineAway||0)/60),offline_coins:Math.round(offlineGain||0),w:innerWidth,h:innerHeight,dpr:devicePixelRatio||1,
  installed:!!((window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone),touch:'ontouchstart' in window,ios:/iPhone|iPad|iPod/.test(navigator.userAgent),android:/Android/.test(navigator.userAgent),lang:navigator.language||'',tz:(()=>{try{return Intl.DateTimeFormat().resolvedOptions().timeZone||'';}catch(e){return '';}})(),
  $set:{last_version:'0.8.0',stars_total:totalStars(),winter:winterNo(),machine_best:TOOLS[save.tool].id,premium:!!save.pro},$set_once:{first_version:'0.8.0',first_seen:new Date().toISOString().slice(0,10)}});
""" % PH_KEY
rep("keys,hit};\n})();","keys,hit};\n"+block+"})();")
open(f,'w',encoding='utf-8').write(s)
