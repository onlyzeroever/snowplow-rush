# Section 3, money ready for the apps (audit Nov 21): one door for every price button and every rewarded ad.
# Web and tests behave exactly as before: prices shown, nothing charged, the 2.5 s test ad card.
# In the apps the native layer (Capacitor; contract in APP_HANDOFF.md) sets window.SRNative and the same buttons go to
# the App Store / Google Play and AppLovin MAX:
#   SRNative.buy(productId) -> Promise<{ok, reason?: 'cancelled'|'pending'|'error'}>
#   SRNative.owned()        -> Promise<[productId]>  silent, at launch (entitlements the store already knows)
#   SRNative.restore()      -> Promise<[productId]>  the Restore Purchases button (may ask the player to sign in)
#   SRNative.prices()       -> Promise<{productId: '£4.99'}>  shown instead of the US test prices
#   SRNative.showAd(placement) -> Promise<{ok, reason?}>  placements: continue, double_coins, free_gems, shed_double
# and calls window.srNativeReady() once it is set up. Adds Restore Purchases to Settings (Apple requires one), a
# "connecting to the store" card while a store sheet is open, and gives the reward back when a real ad fails to load
# (x2 coins button returns, free-gem count refunded, shed coins kept). Held for the lab first (money code).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# the ad finish is shared by the test card and real ads
rep("if(adScreen){adScreen.t-=dt;if(adScreen.t<=0){track('ad_watched',{kind:adScreen.gems?'free_gems':adScreen.onDone?'reward':'coins',screen:state});adCount();if(adScreen.onDone){const f=adScreen.onDone;adScreen=null;f();return;}if(adScreen.gems){save.gems=(save.gems||0)+adScreen.reward;showToast('+'+adScreen.reward+' GEMS','#ff8fc8');}else{save.coins+=adScreen.reward;showToast('+'+fmt(adScreen.reward)+' COINS','#ffd23f');}sfx('buy');adScreen=null;persist();}}",
    "if(adScreen){adScreen.t-=dt;if(adScreen.t<=0){const a=adScreen;adScreen=null;if(adFinish(a))return;}}")
# the four rewarded ads
rep("else adScreen={t:2.5,reward:0,onDone:go};", "else IAP.ad('continue',{t:2.5,reward:0,onDone:go});")
rep("run.adUsed=true;adScreen={t:2.5,reward:Math.floor(run.earned)};",
    "run.adUsed=true;IAP.ad('double_coins',{t:2.5,reward:Math.floor(run.earned),onFail:()=>{if(run)run.adUsed=false;}});")
rep("else{adScreen={t:2.5,reward:SHOP.adGems,gems:true};sfx('click');}",
    "else{IAP.ad('free_gems',{t:2.5,reward:SHOP.adGems,gems:true,onFail:()=>{if(save.adGems)save.adGems.n=Math.max(0,save.adGems.n-1);persist();}});sfx('click');}")
rep("else adScreen={t:2.5,reward:rw,onDone:fin};", "else IAP.ad('shed_double',{t:2.5,reward:rw,onDone:fin,onFail:()=>goMap()});")
# gem packs
rep("()=>{track('iap_test',{item:'gems_'+g.gems,price:g.price});save.gems=(save.gems||0)+g.gems;sfx('buy');buzz(20);showToast('+'+g.gems+' GEMS (TEST)','#ff8fc8');persist();}",
    "()=>IAP.buy(g.id,()=>{track('iap_test',{item:'gems_'+g.gems,price:g.price});save.gems=(save.gems||0)+g.gems;sfx('buy');buzz(20);showToast('+'+g.gems+' GEMS'+(IAP.native()?'':' (TEST)'),'#ff8fc8');persist();})")
# no taps while a store sheet or a real ad is open
rep("phTap('touch');if(adScreen)return;", "phTap('touch');if(adScreen||(IAP&&IAP.busy))return;")
rep("if(adScreen)drawAd();", "if(adScreen)drawAd();if(IAP&&IAP.busy)drawStoreBusy();")
# Restore Purchases in Settings
rep("panel(14,60,152,204,'#13306b','#ffd23f');\n  text(b,'SETTINGS'", "panel(14,60,152,224,'#13306b','#ffd23f');\n  text(b,'SETTINGS'")
rep("button('close',92,226,64,18,'orange','DONE',()=>{settingsOpen=false;sfx('click');});}",
    "button('close',92,226,64,18,'orange','DONE',()=>{settingsOpen=false;sfx('click');});button('restore',24,250,132,14,'navy','RESTORE PURCHASES',()=>{sfx('click');IAP.restore();});}")
BR = r"""
// ---------------- STORE + ADS BRIDGE (p163): every price button and every rewarded ad goes through IAP ----------------
function adFinish(a){track('ad_watched',{kind:a.gems?'free_gems':a.onDone?'reward':'coins',screen:state});adCount();if(a.onDone){a.onDone();return true;}
  if(a.gems){save.gems=(save.gems||0)+a.reward;showToast('+'+a.reward+' GEMS','#ff8fc8');}else{save.coins+=a.reward;showToast('+'+fmt(a.reward)+' COINS','#ffd23f');}sfx('buy');persist();return false;}
function drawStoreBusy(){if(performance.now()-IAP.busy>90000){IAP.busy=0;return;}b.fillStyle='rgba(11,24,56,0.8)';b.fillRect(0,0,W,H);panel(20,128,140,44,'#13306b','#ffd23f');
  text(b,IAP.kind==='ad'?'LOADING THE AD':'CONNECTING TO THE STORE',W/2,140,'#ffffff',{align:'center',outline:null});const n=1+Math.floor(performance.now()/350)%3;text(b,'.'.repeat(n),W/2,154,'#ffd23f',{align:'center',scale:2,outline:null});}
var IAP={busy:0,kind:null,
  // product ids: must match App Store Connect and Google Play Console exactly (APP_HANDOFF.md lists them)
  ids:{premium:'premium',starter:'starter_pack',g1:'gems_60',g2:'gems_330',g3:'gems_700',ride_monster:'ride_monster',ride_jet:'ride_jet',ride_mech:'ride_mech',ride_dragon:'ride_dragon',ride_ufo:'ride_ufo',ride_pass:'wild_ride_pass'},
  consumable:{g1:1,g2:1,g3:1},
  native(){const N=window.SRNative;return N&&typeof N.buy==='function'?N:null;},
  run(kind,fn,ok,bad){this.busy=performance.now();this.kind=kind;Promise.resolve().then(fn).then(r=>{this.busy=0;ok(r);}).catch(e=>{this.busy=0;bad(e);});},
  // web and tests: grant straight away (prices are shown, nothing is charged), as before
  buy(key,grant){const N=this.native();if(!N)return grant();if(this.busy)return false;const id=this.ids[key];if(!id){showToast('NOT FOR SALE HERE','#ff9aa8');return false;}
    this.run('buy',()=>N.buy(id),r=>{if(r&&r.ok){if(!this.consumable[key]){save.owned=save.owned||{};save.owned[id]=true;}grant();persist();}
      else showToast(r&&r.reason==='pending'?'WAITING FOR APPROVAL':r&&r.reason==='cancelled'?'PURCHASE CANCELLED':'STORE NOT AVAILABLE','#ff9aa8');},()=>showToast('STORE NOT AVAILABLE','#ff9aa8'));return false;},
  ad(placement,a){const N=window.SRNative;if(!N||typeof N.showAd!=='function'){adScreen=a;return;}if(this.busy)return;
    const fail=()=>{if(a.onFail)a.onFail();showToast('NO AD RIGHT NOW. TRY AGAIN SOON','#ff9aa8');};try{if(AC&&AC.state==='running')AC.suspend();}catch(e){}
    this.run('ad',()=>N.showAd(placement),r=>{try{if(AC)AC.resume();}catch(e){}if(r&&r.ok)adFinish(a);else fail();},()=>{try{if(AC)AC.resume();}catch(e){}fail();});},
  restore(){const N=this.native();if(!N||typeof N.restore!=='function'){showToast('NOTHING TO RESTORE (TEST MODE)','#9fd8ff');return;}if(this.busy)return;
    this.run('buy',()=>N.restore(),list=>{const n=this.applyOwned(list||[]);persist();showToast(n?'RESTORED '+n+' PURCHASE'+(n>1?'S':''):'NOTHING TO RESTORE','#ffd23f');},()=>showToast('STORE NOT AVAILABLE','#ff9aa8'));},
  // what the store says this player owns comes back without the one-time extras of a first purchase (coins, gems)
  applyOwned(list){let n=0;save.owned=save.owned||{};const has=id=>list.includes(id);
    if(has('premium')&&!save.pro){save.pro=true;_tc.k='';vcache.clear();n++;}
    if(has('starter_pack')&&!save.starter){save.starter=true;save.outfits=save.outfits||{};save.outfits.explorer=true;n++;}
    if(has('wild_ride_pass')&&!save.ridePass){save.ridePass=true;n++;const i=rideForSale();if(i>=0)grantRide(i);}
    for(const k of ['monster','jet','mech','dragon','ufo'])if(has('ride_'+k)){const i=toolIdx(k);if(i>=0&&!owns(i)){grantRide(i);n++;}}
    for(const id of list)save.owned[id]=true;return n;},
  syncOwned(){const N=this.native();if(!N||typeof N.owned!=='function')return;Promise.resolve().then(()=>N.owned()).then(list=>{if(list&&list.length&&this.applyOwned(list))persist();}).catch(()=>{});},
  prices(){const N=this.native();if(!N||typeof N.prices!=='function')return;Promise.resolve().then(()=>N.prices()).then(p=>{if(!p)return;const P=k=>p[this.ids[k]];
    if(P('premium'))SHOP.premium.price=P('premium');if(P('starter'))SHOP.starter.price=P('starter');for(const g of SHOP.gems)if(P(g.id))g.price=P(g.id);
    for(const k in SHOP.rides)if(P('ride_'+k))SHOP.rides[k][0]=P('ride_'+k);if(P('ride_pass'))SHOP.ridePass.price=P('ride_pass');}).catch(()=>{});}};
{const g=shopBuyPremium;shopBuyPremium=function(){if(save.pro)return;return IAP.buy('premium',()=>g());};}
{const g=shopBuyStarter;shopBuyStarter=function(){if(save.starter)return;return IAP.buy('starter',()=>g());};}
{const g=buyRidePass;buyRidePass=function(){if(save.ridePass)return;return IAP.buy('ride_pass',()=>g());};}
{const g=buyRide;buyRide=function(i,gems){if(gems||!TOOLS[i]||!IAP.native())return g(i,gems);
  IAP.buy('ride_'+TOOLS[i].id,()=>{if(g(i,false)){ridePeek=null;try{if(run)run.offerShut=true;}catch(e){}}});return false;};}
window.srNativeReady=()=>{IAP.prices();IAP.syncOwned();};if(window.SRNative)setTimeout(window.srNativeReady,0);
"""
rep("{const o=startNewWinter;startNewWinter=function(){", BR.lstrip('\n')+"{const o=startNewWinter;startNewWinter=function(){")
open(f,'w',encoding='utf-8').write(s)
print('p163 store + ads bridge (web unchanged; apps plug in window.SRNative), Restore Purchases in Settings')
