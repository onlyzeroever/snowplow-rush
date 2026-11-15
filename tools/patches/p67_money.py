import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Monetisation, as agreed (design doc: Monetisation, Free vs paid, Wild Rides for sale). Test mode: nothing is charged.
#  - Snowplow Rush Premium (one-time, $4.99 launch price, was $7.99): no ads, every ad reward without the ad, x2 coins
#    forever, GOLD PAINT for every machine, a coin pack, and a 3x helper shed (offline earnings for 6 hours, not 2).
#  - Starter pack (one-time $1.99): 200 gems, a coin pack, the Explorer outfit.
#  - Wild Rides for sale: a rare TEST DRIVE pickup in jobs (once you own the Rotary Blower) lets you drive the next Wild
#    Ride for 15 seconds; afterwards it is for sale ($1.99-3.99 or gems) or you earn it as before. Wild Ride Pass ($9.99):
#    each ride is yours as it appears. No random boxes.
#  - Restore Purchases. Shop in two tabs: OFFERS, COINS & RIDES.

rep("  dailyGems:5,trophyGems:10,","  premium:{price:'$4.99',was:'$7.99',coinRuns:25,shedS:21600},\n  starter:{price:'$1.99',gems:200,coinRuns:10},\n  rides:{monster:['$1.99',200],jet:['$2.49',250],mech:['$2.99',300],dragon:['$3.49',350],ufo:['$3.99',400]},\n  ridePass:{price:'$9.99'},driveSecs:15,driveChance:0.2,\n  dailyGems:5,trophyGems:10,")

# the bigger helper shed
rep("const OFFLINE_CAP_S=7200, OFFLINE_RATE=0.5;","const OFFLINE_CAP_BASE=7200, OFFLINE_RATE=0.5;\nfunction offCap(){return (typeof save!=='undefined'&&save&&save.pro)?SHOP.premium.shedS:OFFLINE_CAP_BASE;}")
s=s.replace(',OFFLINE_CAP_S,OFFLINE_RATE}',',OFFLINE_CAP_S:OFFLINE_CAP_BASE,offCap,OFFLINE_RATE}').replace('OFFLINE_CAP_S),','offCap()),').replace('(OFFLINE_CAP_S)','(offCap())').replace('min(OFFLINE_CAP_S','min(offCap()')
assert 'OFFLINE_CAP_S'+')' not in s

# names: Pro Pack -> Premium
s=s.replace("'PRO: ","'PREMIUM: ").replace("' GEMS (PRO: NO AD)'","' GEMS (PREMIUM: NO AD)'")

# gold paint: a sixth skin on every machine, owned with Premium; fix the UFO's earn job (its own job is the ranch)
rep("ufo:'farm'};","ufo:'ranch'};\nfor(const k in SKIN_NAMES)SKIN_NAMES[k].push('GOLD PAINT');")
rep("function skinOwned(tid,i){return i===0||!!save.skins[tid+':'+i];}","function skinOwned(tid,i){return i===0||(i===5&&!!save.pro)||!!save.skins[tid+':'+i];}")
rep("function skinState(tid,i){if(skinOwned(tid,i))return 'own';","function skinState(tid,i){if(skinOwned(tid,i))return 'own';if(i===5)return 'prem';")
rep("if(i===0&&isGold(tid))Object.assign(p,GOLD_PAL,{gold:true});return p;}","if((i===0&&isGold(tid))||i===5)Object.assign(p,GOLD_PAL,{gold:true});return p;}")
rep("""  for(let k=0;k<5;k++){const x=12+k*32,y=134,sel=k===skinSel,st=skinState(tid,k);card(x,y,30,40,sel?'#fff6d8':'#eef3fb',sel?'#ffd23f':'#9fc0e8');drawToolIcon(tid,x+3,y+3,24,k);
    if(st==='own')text(b,skinIdx(tid)===k?'ON':'',x+15,y+30,'#1f7a33',{align:'center',outline:null});else if(st==='earn'){b.drawImage(SPR.trophy,x+11,y+28);}else priceDraw(skinPrice(tid,k),x+15,y+31,'#13306b','center');
    btn('sks'+k,x,y,30,40,()=>{skinSel=k;sfx('click');});}""","""  for(let k=0;k<6;k++){const x=11+k*26,y=134,sel=k===skinSel,st=skinState(tid,k);card(x,y,25,40,sel?'#fff6d8':(k===5?'#fffaf0':'#eef3fb'),sel||k===5?'#ffd23f':'#9fc0e8');drawToolIcon(tid,x+1,y+3,23,k);
    if(st==='own')text(b,skinIdx(tid)===k?'ON':'',x+12,y+30,'#1f7a33',{align:'center',outline:null});else if(st==='earn'){b.drawImage(SPR.trophy,x+8,y+28);}else if(st==='prem')text(b,'PREM',x+12,y+30,'#a8740a',{align:'center',outline:null});else priceDraw(skinPrice(tid,k),x+12,y+31,'#13306b','center');
    btn('sks'+k,x,y,25,40,()=>{skinSel=k;sfx('click');});}""")
rep("""  else if(st==='earn'){const job=LEVELS[lvIdx(SKIN_EARN_JOB[tid])];""","""  else if(st==='prem'){text(b,'COMES WITH PREMIUM',W/2,196,'#ffd23f',{align:'center',outline:null});button('skprem',50,206,80,16,'gold','SEE PREMIUM',()=>{skinFor=null;shopTab=0;openShop();});}
  else if(st==='earn'){const job=LEVELS[lvIdx(SKIN_EARN_JOB[tid])];""")

# the Explorer outfit (starter pack)
rep("e0c08a']]}},\n];\nconst EARN_TXT={","e0c08a']]}},\n  {id:'explorer', name:'EXPLORER',   price:{earn:'starter'},pal:{Y:'#f07a1a',y:'#b8501a',R:'#f07a1a',r:'#2a2a36',M:'#7a4a2a',J:'#3f5fae',T:'#2a2a36'},ov:{d:[[3,5,8,1,'#ffc727'],[2,5,1,1,'#2a2a36'],[11,5,1,1,'#2a2a36']],u:[[2,5,10,1,'#2a2a36']],s:[[8,5,4,1,'#ffc727']]}},\n];\nconst EARN_TXT={starter:'COMES IN THE STARTER PACK',")
rep("function earnMet(key){","function earnMet(key){if(key==='starter')return !!save.starter;")

# test drives: the run machine switches to the ride for a few seconds
rep("function chal(){return !!(run&&run.challenge&&state==='play');}","function chal(){return !!(run&&run.challenge&&state==='play');}\nfunction drv(){return !!(run&&run.drive&&state==='play'&&!run.ended);}")
rep("function curLv(){if(chal())return ZERO_LV;","function curLv(){if(chal()||drv())return ZERO_LV;")
rep("function tool(){if(chal())return TOOLS[toolIdx(run.challenge)];","function tool(){if(chal())return TOOLS[toolIdx(run.challenge)];if(drv())return TOOLS[toolIdx(run.drive)];")
rep("(chal()?0:mLv(t.id).size)","((chal()||drv())?0:mLv(t.id).size)")
rep("\n  g.ground=new Uint8ClampedArray(pw*ph*3);","""
  g.driveKey=null;{const ri=nextRideIdx();if(ri>=0&&!LEVELS[idx].tool){const first=!(save.rideSeen&&save.rideSeen[TOOLS[ri].id]);if(Math.random()<(first?0.5:SHOP.driveChance)){
    for(let k=0;k<300;k++){const x=20+Math.floor(Math.random()*(pw-40)),y=Math.floor(ph*0.2+Math.random()*ph*0.6);if(g.type[(y>>1)*cols+(x>>1)]!==T_BLOCK&&Math.hypot(x-g.start.x,y-g.start.y)>120){g.driveKey={x,y,ri,taken:false};break;}}}}}
  g.ground=new Uint8ClampedArray(pw*ph*3);""")
rep("save.boostNext=false;P.vx=0;P.vy=0;","save.boostNext=false;P.vx=0;P.vy=0;if(run.challenge&&G.driveKey)G.driveKey=null;")
rep("checkTreasure(br);","checkTreasure(br);checkDrive(br,dt);")
rep("function checkTreasure(br){","""function nextRideIdx(){const r=toolIdx('rotary');if(save.tool<r)return -1;const i=save.tool+1;return (i<TOOLS.length&&TOOLS[i].winter)?i:-1;}
function rideForSale(){const i=nextRideIdx();return (i>=0&&save.rideSeen&&save.rideSeen[TOOLS[i].id])?i:-1;}
function grantRide(i){if(i<0||save.tool>=i)return false;save.tool=i;save.use=i;_tc.k='';vcache.clear();sfx('fanfare');buzz(30);showToast('WILD RIDE: '+TOOLS[i].name+' IS YOURS!','#ffd23f');persist();return true;}
function buyRide(i,gems){if(i<0||!TOOLS[i])return false;const pr=SHOP.rides[TOOLS[i].id];if(!pr)return false;if(gems){if((save.gems||0)<pr[1]){sfx('deny');showToast('NEED '+pr[1]+' GEMS','#ff9aa8');return false;}save.gems-=pr[1];}return grantRide(i);}
function unstick(){const tid=tool().id;if(!blockedBy(footprint(tid,P.x,P.y,P.f)))return;for(let r=2;r<=64;r+=2)for(let a=0;a<16;a++){const x=P.x+Math.cos(a*Math.PI/8)*r,y=P.y+Math.sin(a*Math.PI/8)*r;if(!blockedBy(footprint(tid,x,y,P.f))){P.x=x;P.y=y;return;}}}
function checkDrive(br,dt){const dk=G.driveKey;
  if(dk&&!dk.taken&&overlap(br,{x:dk.x-7,y:dk.y-7,w:14,h:14})){dk.taken=true;const t=TOOLS[dk.ri];save.rideSeen=save.rideSeen||{};save.rideSeen[t.id]=true;
    run.drive=t.id;run.driveT=SHOP.driveSecs;run.drove=dk.ri;_tc.k='';showToast('TEST DRIVE: '+t.name+'!','#ffd23f');addFloat(P.x,P.y-26,t.name+'!','#ffd23f',1.6);sfx('fanfare');buzz(40);
    for(let k=0;k<18;k++)particles.push({x:dk.x,y:dk.y,vx:rnd(-50,50),vy:rnd(-40,40),z:2,vz:rnd(40,90),life:0.9,t:0,kind:'spark'});
    unstick();if(save.ridePass)grantRide(dk.ri);persist();}
  if(run.drive){run.driveT-=dt;if(run.driveT<=0){run.drive=null;_tc.k='';unstick();addFloat(P.x,P.y-24,'TEST DRIVE OVER','#ffd23f',1.4);sfx('click');}}}
let DRIVE_ICON=null;function driveIcon(){if(DRIVE_ICON)return DRIVE_ICON;const c=mk(16,16),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,8,8,7);g.fillStyle='#ffd23f';pixCircle(g,8,8,6);g.fillStyle='#3a1d6e';pixCircle(g,8,8,4);
  g.fillStyle='#ffd23f';R(g,7,4,2,9,'#ffd23f');R(g,4,7,9,2,'#ffd23f');g.fillStyle=K;pixCircle(g,8,8,2);g.fillStyle='#fff3a0';pixCircle(g,8,8,1);R(g,5,2,3,1,'#fff3a0');return DRIVE_ICON=c;}
function checkTreasure(br){""")
rep("  if(G.treasure&&!G.treasure.found&&Math.floor(tNow*1.3","  if(G.driveKey&&!G.driveKey.taken&&G.driveKey.y>top&&G.driveKey.y<bot){const dk=G.driveKey,p=Math.floor(tNow*6)%4;b.fillStyle='rgba(255,210,63,0.22)';pixCircle(b,dk.x,dk.y,9+p);b.drawImage(driveIcon(),dk.x-8,dk.y-8-(Math.floor(tNow*3)%2));}\n  if(G.treasure&&!G.treasure.found&&Math.floor(tNow*1.3")
rep("  if(LOOKTEST){button('lookc',","  if(drv()){const sc=Math.ceil(run.driveT);panel(36,HUD_H+3,108,13,'#3a1d6e');text(b,'TEST DRIVE '+TOOLS[toolIdx(run.drive)].name+' '+sc+'S',W/2,HUD_H+6,'#ffd23f',{align:'center',outline:null});}\n  if(LOOKTEST){button('lookc',")

# the offer after a test drive, on the results screen (once; never a countdown)
rep("  if(t>0.6){const canAd=!r.challenge&&!run.adUsed","  const offerRide=!r.challenge&&run.drove!=null&&save.tool<run.drove&&!run.offerShut;\n  if(t>0.6&&!offerRide){const canAd=!r.challenge&&!run.adUsed")
rep("button('rmap',67,py+176,46,22,'blue','JOBS',goMap);button('rupg',116,py+176,46,22,'green','UPGRADE',goUpgrades);}}","""button('rmap',67,py+176,46,22,'blue','JOBS',goMap);button('rupg',116,py+176,46,22,'green','UPGRADE',goUpgrades);}
  if(offerRide&&t>0.6){const ti=run.drove,T3=TOOLS[ti],pr=SHOP.rides[T3.id];b.fillStyle='rgba(11,24,56,0.6)';b.fillRect(0,0,W,H);panel(16,80,148,156,'#13306b','#ffd23f');
    text(b,'ENJOYED THE TEST DRIVE?',W/2,88,'#ffd23f',{align:'center'});R(b,62,100,56,44,'#cfe3f8');drawToolIcon(T3.id,70,102,40);text(b,'KEEP THE '+T3.name+'?',W/2,150,'#ffffff',{align:'center',outline:null});
    button('ro$',24,162,132,18,'gold','KEEP IT NOW '+pr[0],()=>{if(buyRide(ti,false))run.offerShut=true;});
    button('rog',24,184,132,16,(save.gems||0)>=pr[1]?'purple':'grey','OR '+pr[1]+' GEMS',()=>{if(buyRide(ti,true))run.offerShut=true;});
    button('ron',24,204,132,16,'blue','NOT NOW, I WILL EARN IT',()=>{run.offerShut=true;sfx('click');});
    text(b,'IT STAYS IN THE SHOP TOO',W/2,226,'#9fc0e8',{align:'center',outline:null});}}""")

# the shop: two tabs
a=s.index('function drawShop(){'); e=s.index("button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;sfx('click');});}",a)+len("button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;sfx('click');});}")
SHOPJS=r"""let shopTab=0;
function shopBuyPremium(){if(save.pro)return;save.pro=true;_tc.k='';vcache.clear();const add=runPay()*SHOP.premium.coinRuns;save.coins+=add;sfx('fanfare');buzz(30);showToast('PREMIUM! +'+fmt(add)+' COINS','#ffd23f');persist();}
function shopBuyStarter(){if(save.starter)return;save.starter=true;save.gems=(save.gems||0)+SHOP.starter.gems;const add=runPay()*SHOP.starter.coinRuns;save.coins+=add;save.outfits=save.outfits||{};save.outfits.explorer=true;sfx('fanfare');buzz(30);showToast('STARTER PACK! +'+SHOP.starter.gems+' GEMS','#ffd23f');persist();}
function buyRidePass(){if(save.ridePass)return;save.ridePass=true;sfx('fanfare');showToast('WILD RIDE PASS!','#ffd23f');const i=rideForSale();if(i>=0)grantRide(i);persist();}
function restorePurchases(){sfx('click');const got=[];if(save.pro)got.push('PREMIUM');if(save.starter)got.push('STARTER');if(save.ridePass)got.push('RIDE PASS');showToast(got.length?'RESTORED: '+got.join(', '):'NOTHING TO RESTORE','#9fd8ff');}
function drawShop(){b.fillStyle='rgba(11,24,56,0.82)';b.fillRect(0,0,W,H);panel(6,6,168,306,'#13306b','#ffd23f');
  text(b,'SHOP',W/2,13,'#ffffff',{align:'center',scale:2});text(b,'TEST MODE: NOTHING IS CHARGED',W/2,28,'#7fe08a',{align:'center',outline:null});
  R(b,12,36,156,13,'#0b1838');b.drawImage(SPR.coin,18,39);text(b,fmt(save.coins),28,40,'#ffd23f');b.drawImage(SPR.gem,100,39);text(b,fmt(save.gems||0),110,40,'#ff8fc8');
  button('stab0',12,52,76,14,shopTab===0?'gold':'navy','OFFERS',()=>{shopTab=0;sfx('click');});
  button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;sfx('click');});
  if(shopTab===0){
    {const y=70;card(12,y,156,66,save.pro?'#fff6d8':'#fffaf0','#ffd23f');b.drawImage(SPR.trophy,17,y+4);text(b,'PREMIUM',29,y+5,'#a8740a',{outline:null});
      ['NO ADS, EVER','EVERY AD REWARD, NO AD','x2 COINS FOREVER','GOLD PAINT, ALL MACHINES','COIN PACK + 3x HELPER SHED'].forEach((q,k)=>{R(b,17,y+18+k*9,3,3,'#33b24a');text(b,q,23,y+16+k*9,'#13306b',{outline:null});});
      if(save.pro)button('spro',124,y+6,40,16,'grey','OWNED',()=>sfx('click'));
      else{text(b,SHOP.premium.was,144,y+5,'#9aa6ba',{align:'center',outline:null});R(b,134,y+8,21,1,'#e03a4e');button('spro',124,y+14,40,16,'gold',SHOP.premium.price,shopBuyPremium);text(b,'LAUNCH',144,y+33,'#e03a4e',{align:'center',outline:null});}}
    {const y=140;card(12,y,156,30,save.starter?'#eef3fb':'#eefaf0','#33b24a');b.drawImage(SPR.gem,17,y+5);text(b,'STARTER PACK',28,y+4,'#1f7a33',{outline:null});
      text(b,SHOP.starter.gems+' GEMS, COINS AND',28,y+12,'#4f6fa0',{outline:null});text(b,'THE EXPLORER OUTFIT',28,y+20,'#4f6fa0',{outline:null});
      if(save.starter)button('sst',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));else button('sst',124,y+7,40,16,'green',SHOP.starter.price,shopBuyStarter);}
    text(b,'GEMS',14,176,'#9fc0e8',{outline:null});
    SHOP.gems.forEach((g,i)=>{const x=12+i*53,y=184,w=50,h=46;card(x,y,w,h,'#eef3fb',g.tag?'#ffd23f':'#9fc0e8');
      if(g.tag){R(b,x+2,y+2,w-4,7,'#e8283f');text(b,g.tag,x+w/2,y+3,'#ffffff',{align:'center',outline:null});}
      const n=1+i;for(let k=0;k<n;k++)b.drawImage(SPR.gem,x+w/2-4-(n-1)*3+k*6,y+11-(k%2));
      text(b,''+g.gems,x+w/2,y+21,'#13306b',{align:'center',outline:null});
      button('sg'+i,x+3,y+30,w-6,13,'green',g.price,()=>{save.gems=(save.gems||0)+g.gems;sfx('buy');buzz(20);showToast('+'+g.gems+' GEMS (TEST)','#ff8fc8');persist();});});
    text(b,'GEMS BUY SKINS, OUTFITS AND COINS',W/2,238,'#ff8fc8',{align:'center',outline:null});
    text(b,'NO RANDOM BOXES, EVER',W/2,248,'#9fc0e8',{align:'center',outline:null});
    button('srest',12,284,76,20,'navy','RESTORE',restorePurchases);}
  else{
    text(b,'COIN BAGS: GROW WITH YOU',14,70,'#9fc0e8',{outline:null});
    const rp=runPay();
    SHOP.bags.forEach((bg,i)=>{const y=78+i*22,amt=bg.runs*rp,ok=(save.gems||0)>=bg.cost;card(12,y,156,20,'#eef3fb','#9fc0e8');
      for(let k=0;k<=i;k++)b.drawImage(SPR.coin,16+k*4,y+7-k*2);text(b,bg.name,34,y+3,'#13306b',{outline:null});
      b.drawImage(SPR.coinS,34,y+11);text(b,'+'+fmt(amt),41,y+11,'#a8740a',{outline:null});text(b,'= '+bg.runs+' RUNS',118,y+11,'#7d8aa0',{outline:null,align:'right'});
      button('sb'+i,122,y+2,42,16,ok?'green':'grey',null,()=>{if((save.gems||0)<bg.cost){sfx('deny');showToast('NEED '+bg.cost+' GEMS','#ff9aa8');return;}
        save.gems-=bg.cost;save.coins+=amt;sfx('buy');buzz(20);showToast('+'+fmt(amt)+' COINS','#ffd23f');persist();});
      b.drawImage(SPR.gemS,130,y+7);text(b,''+bg.cost,137,y+7,'#ffffff');});
    {const left=adGemsLeft();
      if(left>0)button('sad',12,146,156,14,'purple','AD: +'+SHOP.adGems+' FREE GEMS ('+left+' LEFT)',()=>{const k=todayKey();if(!save.adGems||save.adGems.date!==k)save.adGems={date:k,n:0};save.adGems.n++;
        if(save.pro){save.gems=(save.gems||0)+SHOP.adGems;showToast('+'+SHOP.adGems+' GEMS (PREMIUM: NO AD)','#ff8fc8');sfx('buy');}else{adScreen={t:2.5,reward:SHOP.adGems,gems:true};sfx('click');}persist();});
      else button('sad',12,146,156,14,'grey','NO MORE FREE GEMS TODAY',()=>sfx('deny'));}
    text(b,'WILD RIDES',14,166,'#9fc0e8',{outline:null});
    {const ri=rideForSale(),nx=nextRideIdx(),y=174;
      if(ri>=0){const T3=TOOLS[ri],pr=SHOP.rides[T3.id];card(12,y,156,34,'#eef3fb','#ffd23f');R(b,14,y+2,32,30,'#cfe3f8');drawToolIcon(T3.id,15,y+2,30);
        text(b,T3.name,50,y+3,'#13306b',{outline:null});text(b,'KEEP IT NOW, OR EARN IT',50,y+11,'#4f6fa0',{outline:null});
        button('sride',50,y+19,52,13,'gold',pr[0],()=>buyRide(ri,false));button('srideg',106,y+19,58,13,(save.gems||0)>=pr[1]?'purple':'grey','OR '+pr[1]+' GEMS',()=>buyRide(ri,true));}
      else{card(12,y,156,34,'#eef3fb','#9fc0e8');const msg=nx<0?(save.tool<toolIdx('rotary')?['TEST DRIVES BEGIN ONCE YOU','OWN THE ROTARY BLOWER']:['YOU OWN EVERY','WILD RIDE SO FAR']):['FIND A TEST DRIVE IN A JOB','TO UNLOCK THIS OFFER'];
        text(b,msg[0],W/2,y+9,'#4f6fa0',{align:'center',outline:null});text(b,msg[1],W/2,y+19,'#4f6fa0',{align:'center',outline:null});}}
    {const y=212;card(12,y,156,30,save.ridePass?'#fff6d8':'#eef3fb','#ffd23f');text(b,'WILD RIDE PASS',17,y+4,'#a8740a',{outline:null});text(b,'EACH WILD RIDE IS YOURS',17,y+12,'#4f6fa0',{outline:null});text(b,'AS SOON AS IT APPEARS',17,y+20,'#4f6fa0',{outline:null});
      if(save.ridePass)button('spass',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));else button('spass',124,y+7,40,16,'gold',SHOP.ridePass.price,buyRidePass);}
    text(b,'MORE FREE GEMS: DAILY JOBS (+'+SHOP.dailyGems+')',W/2,250,'#ff8fc8',{align:'center',outline:null});text(b,'AND TROPHIES (+'+SHOP.trophyGems+')',W/2,258,'#ff8fc8',{align:'center',outline:null});
    button('stest',12,284,76,20,'purple','TEST: x2 COINS',()=>{const add=Math.max(1000,Math.floor(save.coins));save.coins+=add;sfx('buy');showToast('+'+fmt(add)+' TEST COINS','#c4a0f5');persist();});}
  button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;sfx('click');});}"""
s=s[:a]+SHOPJS+s[e:]
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
rep("window.__SR={","window.__MONEY={get run(){return run;},get P(){return P;},get G(){return G;},tool:()=>tool(),setShop:(o,t)=>{shopOpen=o;shopTab=t;},setState:v=>{state=v;},setSkin:(t,k)=>{skinFor=t;skinSel=k;},nextRideIdx:()=>nextRideIdx(),rideForSale:()=>rideForSale(),buyRide:(i,g)=>buyRide(i,g),premium:()=>shopBuyPremium(),starter:()=>shopBuyStarter(),offCap:()=>offCap(),toolIdx:x=>toolIdx(x),lvIdx:x=>lvIdx(x),startLevel:(i,o)=>startLevel(i,o),endRound:a=>endRound(a),TOOLS};\nwindow.__SR={")
open(f,'w',encoding='utf-8').write(s)
