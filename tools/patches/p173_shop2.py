# Shop v2 (Alex, Nov 21 21:34: "take a look at the store in depth ... like the pros do"; 22:25: OK for the app build,
# OK for the shop events). HELD from the live web game; in the lab and the app build.
#  - a free gift opens every visit: the free ad gems sit at the top of OFFERS (instant CLAIM with Premium); the map's
#    SHOP button carries a FREE tag until the shop is opened that day (only once the daily jobs are on)
#  - one hero offer: the Starter Pack while it is on (its contents as tiles, a real 48-hour countdown that starts when it
#    is first offered, then gone for good), otherwise Premium in full; Premium owners see their perks
#  - Premium lists all five perks in both cards (Alex: the short list sells less)
#  - one colour per way of paying: green = money, purple = gems, blue = free
#  - not enough gems for a coin bag or a Wild Ride: the shop jumps to the gem packs and outlines the smallest pack that
#    covers the gap; it clears once the gems are there, on the other tab or on DONE
#  - one layout grid: cards x 12-168, text from x 17, every price button in one right-hand column (x 118, 46 wide),
#    tags above a button share its width, titles on one line height, the same gap between cards
#  - pop-ups: icons centred in one column, text in one column, the same Premium perks and words as the shop
#  - events (Alex OK, Nov 21 22:25): shop_open gets `from` (map, coins, gems, skin); shop_free_gift; shop_need_gems
#    (item, need, suggested pack); iap_test gets from_need
#  - preview: ?review=all&starter shows the Starter Pack as if just offered (review saves only; ?review is off in apps)
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# --- helpers
rep("function drawShop(){",
    "const STARTER_MS=48*3600e3;let shopNeed=null,shopFrom=null;\n"
    "function starterLeft(){if(save.starter)return 0;const o=save.offers||{};if(!o.starter&&REVIEW_MODE&&/[?&]starter\\b/.test(location.search)){save.offers=o;o.starter=true;}if(!o.starter)return 0;\n"
    "  if(!save.starterT){save.starterT=Date.now();persist();}return Math.max(0,STARTER_MS-(Date.now()-save.starterT));}\n"
    "function fmtLeft(ms){const m=Math.ceil(ms/60000);return m>=60?Math.floor(m/60)+'H '+String(m%60).padStart(2,'0')+'M':m+'M';}\n"
    "function needPack(n){const fx=!save.gemBuys;let k=SHOP.gems.findIndex(g=>g.gems*(fx?2:1)>=n);if(k<0)k=SHOP.gems.length-1;return k;}\n"
    "function needGems(cost,item){const n=cost-(save.gems||0);sfx('deny');showToast('NEED '+n+' MORE GEMS','#ff9aa8');if(!shopOpen)return;shopNeed={cost,t:tNow};shopTab=0;\n"
    "  try{const g=SHOP.gems[needPack(n)];track('shop_need_gems',{item,need:n,pack:(IAP.ids&&IAP.ids[g.id])||g.id});}catch(e){}}\n"
    "function shopFreeGems(){const k=todayKey();if(!save.adGems||save.adGems.date!==k)save.adGems={date:k,n:0};save.adGems.n++;try{track('shop_free_gift',{pro:!!save.pro,left:adGemsLeft()});}catch(e){}\n"
    "  if(save.pro){save.gems=(save.gems||0)+SHOP.adGems;showToast('+'+SHOP.adGems+' GEMS (PREMIUM: NO AD)','#ff8fc8');sfx('buy');}else{IAP.ad('free_gems',{t:2.5,reward:SHOP.adGems,gems:true,onFail:()=>{if(save.adGems)save.adGems.n=Math.max(0,save.adGems.n-1);persist();}});sfx('click');}persist();}\n"
    "function playIcon(x,y){const P=[[0,0],[0,1],[0,2],[0,3],[0,4],[1,1],[1,2],[1,3],[2,2]];for(const q of P)R(b,x+q[0]-1,y+q[1]-1,3,3,K);for(const q of P)R(b,x+q[0],y+q[1],1,1,'#ffffff');}\n"
    "function openShopFrom(f){shopFrom=f;openShop();}\n"
    "function drawShop(){if(save.shopDay!==todayKey()){save.shopDay=todayKey();persist();}")
rep("function drawSettings(){","{const o=openShop;openShop=function(){shopNeed=null;return o.apply(this,arguments);};}\nfunction drawSettings(){")
# --- where the shop was opened from
rep("track('shop_open',{screen:state});","track('shop_open',{screen:state,from:shopFrom||'other'});shopFrom=null;")
rep("button('shopb',sx,by,sw,18,'green','SHOP',()=>{shopTab=0;save.offers=save.offers||{};save.offers.seenShop=true;openShop();});",
    "button('shopb',sx,by,sw,18,'green','SHOP',()=>{shopTab=0;save.offers=save.offers||{};save.offers.seenShop=true;openShopFrom('map');});")
rep("btn('coinpanel',x,y,w-12,17,openShop);const so=button('shop',x+w-13,y+2,11,13,'green',null,openShop);",
    "btn('coinpanel',x,y,w-12,17,()=>openShopFrom('coins'));const so=button('shop',x+w-13,y+2,11,13,'green',null,()=>openShopFrom('coins'));")
rep("btn('gempanel',x,y,w-12,17,openShop);const so=button('shopg',x+w-13,y+2,11,13,'green',null,openShop);",
    "btn('gempanel',x,y,w-12,17,()=>openShopFrom('gems'));const so=button('shopg',x+w-13,y+2,11,13,'green',null,()=>openShopFrom('gems'));")
rep("button('skprem',50,206,80,16,'gold','SEE PREMIUM',()=>{skinFor=null;shopTab=0;openShop();});",
    "button('skprem',50,206,80,16,'gold','SEE PREMIUM',()=>{skinFor=null;shopTab=0;openShopFrom('skin');});")

# --- pop-ups: the starter offer's 48 hours start when it is first offered; icons centred in one column, text in one
rep("if(!save.starter&&!o.starter&&(((save.sess||0)>=2&&runs>=5)||runs>=12)){offerOpen='starter';o.starter=true;}",
    "if(!save.starter&&!o.starter&&(((save.sess||0)>=2&&runs>=5)||runs>=12)){offerOpen='starter';o.starter=true;save.starterT=Date.now();}")
rep("const row=(ic,t,yy,c)=>{if(ic)b.drawImage(ic,x+22,yy);text(b,t,x+(ic?34:22),yy+1,c||'#ffffff',{outline:null});};",
    "const row=(ic,t,yy,c)=>{if(ic)b.drawImage(ic,x+22+Math.floor((9-ic.width)/2),yy+3-Math.floor(ic.height/2));text(b,t,x+34,yy+1,c||'#ffffff',{outline:null});};")
rep("text(b,'ONE PER PLAYER. A THANK-YOU',W/2,y+92,'#9fc0e8',{align:'center',outline:null});text(b,'FOR PLAYING EARLY!',W/2,y+101,'#9fc0e8',{align:'center',outline:null});",
    "text(b,'ONE PER PLAYER. IN THE SHOP',W/2,y+92,'#9fc0e8',{align:'center',outline:null});text(b,'FOR THE NEXT 48 HOURS',W/2,y+101,'#9fc0e8',{align:'center',outline:null});")
rep("row(SPR.trophy,'EVERY REWARD, NO AD',y+44);row(SPR.coin,'x2 COINS FOREVER',y+58,'#ffd23f');row(SPR.star,'GOLD PAINT, ALL MACHINES',y+72);row(null,'+ 12H HELPER SHED, COIN PACK',y+86,'#9fc0e8');\n"
    "    text(b,'PAY ONCE, KEEP IT FOR GOOD',W/2,y+101,'#9fc0e8',{align:'center',outline:null});",
    "premGold(W/2-16,y+38,32);row(SPR.coin,'x2 COINS FOREVER',y+78,'#ffd23f');row(SPR.trophy,'REWARDS WITHOUT ADS',y+90);row(SPR.star,'GOLD PAINT, ALL MACHINES',y+102);row(SPR.helper,'12H HELPER SHED (WAS 6H)',y+114);row(SPR.coinS,'+ '+fmt(runPay()*SHOP.premium.coinRuns)+' COINS NOW',y+126,'#ffd23f');\n"
    "    text(b,'PAY ONCE, KEEP IT FOR GOOD',W/2,y+139,'#9fc0e8',{align:'center',outline:null});")
rep("button('ofbuy',x+26,y+116,w-52,20,'gold',SHOP.premium.price,","button('ofbuy',x+26,y+152,w-52,20,'green',SHOP.premium.price,")
# the Premium pop-up is taller (your machine in gold on top); both pop-ups sit in the middle; NOT NOW keeps its gap to the bottom
rep("function drawOffer(){const k=offerOpen,x=14,y=70,w=152,h=168;","function drawOffer(){const k=offerOpen,x=14,w=152,h=k==='starter'?168:204,y=Math.round(156-h/2);")
rep("button('ofno',x+46,y+142,w-92,16,'navy','NOT NOW',later);}","button('ofno',x+46,y+h-26,w-92,16,'navy','NOT NOW',later);}")
# your own machine in Premium's gold paint, on a warm tile, with a glint
rep("function drawShop(){","function premGold(x,y,sz){const t0=(TOOLS[save.tool||0]||TOOLS[0]).id,tid=isKidTool(t0)?'truck':t0;R(b,x-1,y-1,sz+2,sz+2,'#e8c25a');R(b,x,y,sz,sz,'#fff1c4');R(b,x,y,sz,1,'#fffbe6');\n"
    "  try{drawToolIconTo(b,tid,x,y,sz,5);}catch(e){}const ph=(tNow*1.2)%1;if(ph<0.45){const k=Math.sin(ph/0.45*Math.PI),sx=x+sz-6,sy=y+5;R(b,sx,sy-Math.round(2*k),1,1+Math.round(4*k),'#ffffff');R(b,sx-Math.round(2*k),sy,1+Math.round(4*k),1,'#ffffff');}}\nfunction drawShop(){")

# --- tabs and DONE clear a pending "need gems"
rep("button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;","button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;shopNeed=null;")
rep("button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;","button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;shopNeed=null;")

# --- OFFERS tab (grid: cards x 12 w 156, text x 17, price column x 118 w 46, titles at y+5, 3 px between cards)
a=s.find("  if(shopTab===0){\n    {const y=70;card(12,y,156,66,");z_mark="    text(b,'NO RANDOM BOXES, EVER',W/2,276,'#9fc0e8',{align:'center',outline:null});}\n"
z=s.find(z_mark,a);assert a>0 and z>a,(a,z)
s=s[:a]+(
"  if(shopTab===0){let y=70;const perk=(q,yy)=>{R(b,17,yy+1,3,3,'#33b24a');text(b,q,23,yy,'#13306b',{outline:null});};\n"
# free gift
"    {const left=adGemsLeft(),on=left>0;card(12,y,156,19,on?'#e6f3ff':'#eef3fb',on?'#2f7fd6':'#9fc0e8');b.drawImage(SPR.gem,17,y+6);\n"
"      text(b,on?'+'+SHOP.adGems+' FREE GEMS':'FREE GEMS',28,y+3,on?'#c2185b':'#7d8aa0',{outline:null});text(b,on?left+' LEFT TODAY':'MORE TOMORROW',28,y+10,'#4f6fa0',{outline:null});\n"
"      if(on){const oy=button('sad',118,y+3,46,13,'blue',save.pro?'CLAIM':'FREE',shopFreeGems);if(!save.pro)playIcon(125,y+6+oy);}\n"
"      else button('sad',118,y+3,46,13,'grey','SOON',()=>sfx('deny'));y+=21;}\n"
# hero: starter pack
"    const stL=starterLeft();\n"
"    if(stL>0){card(12,y,156,40,'#eefaf0','#33b24a');text(b,'STARTER PACK',17,y+5,'#1f7a33',{outline:null});R(b,118,y+3,46,9,'#e8283f');text(b,'3X VALUE',141,y+5,'#ffffff',{align:'center',outline:null});\n"
"      const tile=(tx,ic,t,c)=>{R(b,tx,y+13,30,16,'#d3f0d9');b.drawImage(ic,tx+15-Math.floor(ic.width/2),y+14+Math.floor((7-ic.height)/2));text(b,t,tx+15,y+22,c,{align:'center',outline:null});};\n"
"      tile(17,SPR.gem,''+SHOP.starter.gems,'#c2185b');tile(50,SPR.coin,fmt(runPay()*SHOP.starter.coinRuns),'#a8740a');tile(83,SPR.star,'OUTFIT','#13306b');\n"
"      button('sst',118,y+13,46,16,'green',SHOP.starter.price,shopBuyStarter);\n"
"      text(b,'ENDS IN '+fmtLeft(stL),17,y+31,'#e8283f',{outline:null});text(b,'ONE PER PLAYER',164,y+31,'#4f6fa0',{align:'right',outline:null});y+=42;\n"
"      if(!save.pro){card(12,y,156,45,'#fffaf0','#ffd23f');b.drawImage(SPR.trophy,17,y+3);text(b,'PREMIUM',29,y+5,'#a8740a',{outline:null});\n"
"        R(b,17,y+16,3,3,'#ffd23f');text(b,'x2 COINS FOREVER',23,y+15,'#a8740a',{outline:null});['REWARDS WITHOUT ADS','GOLD PAINT + 12H HELPER SHED','+ '+fmt(runPay()*SHOP.premium.coinRuns)+' COINS NOW'].forEach((q,k)=>perk(q,y+22+k*7));\n"
"        button('spro',118,y+3,46,16,'green',SHOP.premium.price,shopBuyPremium);text(b,'PAY ONCE',141,y+21,'#a8740a',{align:'center',outline:null});y+=47;}}\n"
# hero: premium in full
"    else if(!save.pro){card(12,y,156,62,'#fffaf0','#ffd23f');b.drawImage(SPR.trophy,17,y+3);text(b,'PREMIUM',29,y+5,'#a8740a',{outline:null});\n"
"      R(b,17,y+16,3,3,'#ffd23f');text(b,'x2 COINS FOREVER',23,y+15,'#a8740a',{outline:null});['REWARDS WITHOUT ADS','ALL MACHINES IN GOLD','12H HELPER SHED','+ '+fmt(runPay()*SHOP.premium.coinRuns)+' COINS NOW'].forEach((q,k)=>perk(q,y+23+k*8));\n"
"      button('spro',118,y+3,46,16,'green',SHOP.premium.price,shopBuyPremium);text(b,'PAY ONCE',141,y+21,'#a8740a',{align:'center',outline:null});premGold(128,y+30,26);y+=64;}\n"
"    else{card(12,y,156,31,'#fff6d8','#ffd23f');b.drawImage(SPR.trophy,17,y+3);text(b,'PREMIUM IS ON. THANK YOU!',29,y+5,'#a8740a',{outline:null});\n"
"      text(b,'x2 COINS, REWARDS WITHOUT ADS,',17,y+15,'#13306b',{outline:null});text(b,'GOLD PAINT AND THE 12H SHED',17,y+22,'#13306b',{outline:null});y+=33;}\n"
# gem packs
"    {const gy=y,fx2=!save.gemBuys,n2=v=>v.toLocaleString('en-US'),bi=gemBest();let need=shopNeed?shopNeed.cost-(save.gems||0):0;if(shopNeed&&need<=0){shopNeed=null;need=0;}\n"
"    const hi=need>0?needPack(need):-1;\n"
"    text(b,need>0?'NEED '+need+' MORE GEMS':'GEMS',14,gy,need>0?'#ff9aa8':'#9fc0e8',{outline:null});if(fx2)text(b,need>0?'FIRST BUY x2':'FIRST BUY: DOUBLE GEMS',166,gy,'#ff8fc8',{align:'right',outline:null});\n"
"    SHOP.gems.forEach((g,i)=>{const y=gy+6+i*17,best=i===bi;\n"
"      card(12,y,156,17,best?'#fff6d8':'#eef3fb',best?'#ffd23f':'#9fc0e8');\n"
"      for(let k=0;k<=Math.min(4,i);k++)b.drawImage(SPR.gem,16+k*4,y+5-(k%2));\n"
"      let tx=44;text(b,n2(g.gems),tx,y+6,'#13306b',{outline:null});tx+=textW(n2(g.gems))+3;\n"
"      if(fx2){text(b,'x2',tx,y+6,'#e0397a',{outline:null});tx+=textW('x2')+3;}\n"
"      {const gb=gemBonus(i);if(gb){text(b,gb,tx,y+6,'#1f7a33',{outline:null});tx+=textW(gb)+3;}}\n"
"      if(best){const t=textW('BEST VALUE')+4<=114-tx?'BEST VALUE':'BEST',tw=textW(t)+4;if(tw<=114-tx){R(b,tx,y+4,tw,9,'#e8283f');text(b,t,tx+2,y+6,'#ffffff',{outline:null});}}\n"
"      button('sg'+i,118,y+2,46,13,'green',g.price,()=>IAP.buy(g.id,()=>{const first=!save.gemBuys,add=g.gems*(first?2:1),fromNeed=!!shopNeed;save.gemBuys=(save.gemBuys||0)+1;shopNeed=null;track('iap_test',{item:'gems_'+g.gems,price:g.price,from_need:fromNeed});save.gems=(save.gems||0)+add;sfx('buy');buzz(20);showToast('+'+n2(add)+' GEMS'+(first?' (FIRST BUY x2)':'')+(IAP.native()?'':' (TEST)'),'#ff8fc8');persist();}));});\n"
"    if(hi>=0&&(tNow-shopNeed.t>1.2||Math.floor(tNow*5)%2===0)){const ry=gy+6+hi*17,P='#ff4fa3';R(b,10,ry-2,160,2,P);R(b,10,ry+17,160,2,P);R(b,10,ry,2,17,P);R(b,168,ry,2,17,P);}\n"
"    text(b,'NO RANDOM BOXES, EVER',W/2,gy+6+5*17+3,'#9fc0e8',{align:'center',outline:null});}\n")+s[z+len(z_mark):]

# --- COINS + RIDES tab: free gems moved out; the same grid; gems = purple, money = green; short of gems -> the gem packs
a=s.find("    {const left=adGemsLeft();\n      if(left>0)button('sad',12,146,156,14,'purple',");z_mark="      else button('sad',12,146,156,14,'grey','NO MORE FREE GEMS TODAY',()=>sfx('deny'));}\n"
z=s.find(z_mark,a);assert a>0 and z>a,(a,z);s=s[:a]+s[z+len(z_mark):]
rep("for(let k=0;k<=i;k++)b.drawImage(SPR.coin,16+k*4,y+7-k*2);text(b,bg.name,34,y+3,'#13306b',{outline:null});",
    "for(let k=0;k<=i;k++)b.drawImage(SPR.coin,16+k*4,y+7-k*2);text(b,bg.name,34,y+4,'#13306b',{outline:null});")
rep("text(b,'= '+bg.runs+' RUNS',118,y+11,'#7d8aa0',{outline:null,align:'right'});","text(b,'= '+bg.runs+' RUNS',114,y+11,'#7d8aa0',{outline:null,align:'right'});")
rep("button('sb'+i,122,y+2,42,16,ok?'green':'grey',null,()=>{if((save.gems||0)<bg.cost){sfx('deny');showToast('NEED '+bg.cost+' GEMS','#ff9aa8');return;}",
    "button('sb'+i,118,y+2,46,16,ok?'purple':'grey',null,()=>{if((save.gems||0)<bg.cost){needGems(bg.cost,'bag_'+bg.id);return;}")
rep("priceRow(SPR.gemS,''+bg.cost,143,y+4,'#ffffff');text(b,'='+gemCash(bg.cost),143,y+12,'#e8fbe8',{align:'center',outline:null});});",
    "priceRow(SPR.gemS,''+bg.cost,141,y+4,'#ffffff');text(b,'='+gemCash(bg.cost),141,y+12,'#e8fbe8',{align:'center',outline:null});});")
rep("text(b,'WILD RIDES',14,166,'#9fc0e8',{outline:null});","text(b,'WILD RIDES',14,154,'#9fc0e8',{outline:null});")
rep("const ri=rideForSale(),nx=nextRideIdx(),y=174;","const ri=rideForSale(),nx=nextRideIdx(),y=162;")
rep("text(b,T3.name,50,y+3,'#13306b',{outline:null});text(b,'KEEP IT NOW, OR EARN IT',50,y+11,'#4f6fa0',{outline:null});",
    "text(b,T3.name,50,y+5,'#13306b',{outline:null});text(b,'KEEP IT NOW, OR EARN IT',50,y+12,'#4f6fa0',{outline:null});")
rep("button('sride',50,y+19,52,13,'gold',pr[0],()=>buyRide(ri,false));","button('sride',50,y+19,52,13,'green',pr[0],()=>buyRide(ri,false));")
rep("{const y=212;card(12,y,156,30,save.ridePass?'#fff6d8':'#eef3fb','#ffd23f');text(b,'WILD RIDE PASS',17,y+4,'#a8740a',{outline:null});text(b,'EACH WILD RIDE IS YOURS',17,y+12,'#4f6fa0',{outline:null});text(b,'AS SOON AS IT APPEARS',17,y+20,'#4f6fa0',{outline:null});",
    "{const y=200;card(12,y,156,31,save.ridePass?'#fff6d8':'#eef3fb','#ffd23f');text(b,'WILD RIDE PASS',17,y+5,'#a8740a',{outline:null});text(b,'GET EVERY WILD RIDE',17,y+12,'#4f6fa0',{outline:null});text(b,'THE MOMENT IT APPEARS',17,y+19,'#4f6fa0',{outline:null});")
rep("if(save.ridePass)button('spass',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));",
    "if(save.ridePass)button('spass',118,y+7,46,16,'grey','OWNED',()=>sfx('click'));")
rep("if(pc>0){R(b,124,y+2,40,8,'#e8283f');text(b,'SAVE '+pc+'%',144,y+3,'#ffffff',{align:'center',outline:null});}button('spass',124,pc>0?y+11:y+7,40,16,'gold',SHOP.ridePass.price,buyRidePass);",
    "if(pc>0){R(b,118,y+3,46,9,'#e8283f');text(b,'SAVE '+pc+'%',141,y+5,'#ffffff',{align:'center',outline:null});}button('spass',118,pc>0?y+12:y+7,46,16,'green',SHOP.ridePass.price,buyRidePass);")
rep("text(b,'MORE FREE GEMS: DAILY JOBS (+'+SHOP.dailyGems+')',W/2,250,'#ff8fc8',{align:'center',outline:null});text(b,'AND TROPHIES (+'+SHOP.trophyGems+')',W/2,258,'#ff8fc8',{align:'center',outline:null});",
    "text(b,'MORE FREE GEMS: DAILY JOBS (+'+SHOP.dailyGems+')',W/2,240,'#ff8fc8',{align:'center',outline:null});text(b,'AND TROPHIES (+'+SHOP.trophyGems+')',W/2,248,'#ff8fc8',{align:'center',outline:null});")
rep("if(gems){if((save.gems||0)<pr[1]){sfx('deny');showToast('NEED '+pr[1]+' GEMS','#ff9aa8');return false;}",
    "if(gems){if((save.gems||0)<pr[1]){needGems(pr[1],'ride_'+TOOLS[i].id);return false;}")

# --- map: FREE tag on the SHOP button's corner until the shop has been opened today (once the daily jobs are on)
rep("  if(dailyOn()&&!save.starter&&!(save.offers&&save.offers.seenShop)){R(b,156,by-2,6,6,K);R(b,157,by-1,4,4,'#e8283f');}",
    "  if(dailyOn()&&save.shopDay!==todayKey()&&adGemsLeft()>0){const tw=textW('FREE')+4,tx=sx+sw-tw+3;R(b,tx-1,by-6,tw+2,9,K);R(b,tx,by-5,tw,7,'#e8283f');text(b,'FREE',tx+2,by-4,'#ffffff',{outline:null});}\n"
    "  else if(dailyOn()&&!save.starter&&!(save.offers&&save.offers.seenShop)){R(b,156,by-2,6,6,K);R(b,157,by-1,4,4,'#e8283f');}")
open(f,'w',encoding='utf-8').write(s)
print('p173 shop v2: free gift, one hero offer, 48 h starter, five Premium perks, one grid, one colour per way of paying, need-gems jump, shop events')
