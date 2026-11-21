# Shop v2 (Alex, Nov 21 21:34: "take a look at the store in depth ... like the pros do"). Lab first.
#  - a free gift opens every visit: the free ad gems move from the second tab to the top of OFFERS (a free reward in
#    the shop gives a reason to open it every day); the map's SHOP button says FREE until the shop is opened that day
#    (only once the daily jobs are on, so new players see nothing new)
#  - one hero offer: the Starter Pack while it is on (shown as its contents, with a real 48-hour countdown that starts
#    when it is first offered; after that it is gone for good, never back on the same terms), otherwise Premium in full
#  - Premium as a compact card while the Starter Pack is the hero
#  - one button colour per way of paying: green = money, purple = gems, blue = free
#  - not enough gems for a coin bag or a Wild Ride: the shop jumps to the gem packs and outlines the smallest pack
#    that covers the gap ("NEED 210 MORE GEMS"); it clears once the gems are there
#  - tighter gem rows (same prices, labels and first-buy double as p170)
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# --- helpers
rep("function drawShop(){",
    "const STARTER_MS=48*3600e3;let shopNeed=null;\n"
    "function starterLeft(){if(save.starter)return 0;const o=save.offers||{};if(!o.starter)return 0;if(!save.starterT){save.starterT=Date.now();persist();}return Math.max(0,STARTER_MS-(Date.now()-save.starterT));}\n"
    "function fmtLeft(ms){const m=Math.ceil(ms/60000);return m>=60?Math.floor(m/60)+'H '+String(m%60).padStart(2,'0')+'M':m+'M';}\n"
    "function shopFreeGems(){const k=todayKey();if(!save.adGems||save.adGems.date!==k)save.adGems={date:k,n:0};save.adGems.n++;\n"
    "  if(save.pro){save.gems=(save.gems||0)+SHOP.adGems;showToast('+'+SHOP.adGems+' GEMS (PREMIUM: NO AD)','#ff8fc8');sfx('buy');}else{IAP.ad('free_gems',{t:2.5,reward:SHOP.adGems,gems:true,onFail:()=>{if(save.adGems)save.adGems.n=Math.max(0,save.adGems.n-1);persist();}});sfx('click');}persist();}\n"
    "function playIcon(x,y){const P=[[0,0],[0,1],[0,2],[0,3],[0,4],[1,1],[1,2],[1,3],[2,2]];for(const q of P)R(b,x+q[0]-1,y+q[1]-1,3,3,K);for(const q of P)R(b,x+q[0],y+q[1],1,1,'#ffffff');}\n"
    "function drawShop(){if(save.shopDay!==todayKey()){save.shopDay=todayKey();persist();}")
rep("function drawSettings(){","{const o=openShop;openShop=function(){shopNeed=null;return o.apply(this,arguments);};}\nfunction drawSettings(){")
# --- the starter offer: its 48 hours start when it is first offered
rep("if(!save.starter&&!o.starter&&(((save.sess||0)>=2&&runs>=5)||runs>=12)){offerOpen='starter';o.starter=true;}",
    "if(!save.starter&&!o.starter&&(((save.sess||0)>=2&&runs>=5)||runs>=12)){offerOpen='starter';o.starter=true;save.starterT=Date.now();}")
rep("text(b,'ONE PER PLAYER. A THANK-YOU',W/2,y+92,'#9fc0e8',{align:'center',outline:null});text(b,'FOR PLAYING EARLY!',W/2,y+101,'#9fc0e8',{align:'center',outline:null});",
    "text(b,'ONE PER PLAYER. IN THE SHOP',W/2,y+92,'#9fc0e8',{align:'center',outline:null});text(b,'FOR THE NEXT 48 HOURS',W/2,y+101,'#9fc0e8',{align:'center',outline:null});")
rep("button('ofbuy',x+26,y+116,w-52,20,'gold',SHOP.premium.price,","button('ofbuy',x+26,y+116,w-52,20,'green',SHOP.premium.price,")
# --- tabs and DONE clear a pending "need gems"
rep("button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;","button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;shopNeed=null;")
rep("button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;","button('sclose',92,284,76,20,'orange','DONE',()=>{shopOpen=false;shopNeed=null;")
# --- OFFERS tab
a=s.find("  if(shopTab===0){\n    {const y=70;card(12,y,156,66,");z_mark="    text(b,'NO RANDOM BOXES, EVER',W/2,276,'#9fc0e8',{align:'center',outline:null});}\n"
z=s.find(z_mark,a);assert a>0 and z>a,(a,z)
s=s[:a]+(
"  if(shopTab===0){let y=70;\n"
# free gift
"    {const left=adGemsLeft(),on=left>0;card(12,y,156,19,on?'#e6f3ff':'#eef3fb',on?'#2f7fd6':'#9fc0e8');b.drawImage(SPR.gem,17,y+6);\n"
"      text(b,on?'+'+SHOP.adGems+' FREE GEMS':'FREE GEMS',28,y+3,on?'#c2185b':'#7d8aa0',{outline:null});text(b,on?left+' LEFT TODAY':'MORE TOMORROW',28,y+10,'#4f6fa0',{outline:null});\n"
"      if(on){const oy=button('sad',118,y+3,46,13,'blue',save.pro?'CLAIM':'FREE',shopFreeGems);if(!save.pro)playIcon(125,y+6+oy);}\n"
"      else button('sad',118,y+3,46,13,'grey','SOON',()=>sfx('deny'));y+=22;}\n"
# hero: starter pack
"    const stL=starterLeft();\n"
"    if(stL>0){card(12,y,156,46,'#eefaf0','#33b24a');text(b,'STARTER PACK',17,y+4,'#1f7a33',{outline:null});R(b,120,y+3,44,9,'#e8283f');text(b,'3X VALUE',142,y+5,'#ffffff',{align:'center',outline:null});\n"
"      const tile=(tx,ic,iw,t,c)=>{R(b,tx,y+14,32,19,'#d3f0d9');b.drawImage(ic,tx+16-Math.floor(iw/2),y+16);text(b,t,tx+16,y+25,c,{align:'center',outline:null});};\n"
"      tile(17,SPR.gem,7,''+SHOP.starter.gems,'#c2185b');tile(51,SPR.coin,7,fmt(runPay()*SHOP.starter.coinRuns),'#a8740a');tile(85,SPR.star,5,'OUTFIT','#13306b');\n"
"      button('sst',120,y+16,44,16,'green',SHOP.starter.price,shopBuyStarter);\n"
"      text(b,'ENDS IN '+fmtLeft(stL),17,y+37,'#e8283f',{outline:null});text(b,'ONE PER PLAYER',164,y+37,'#4f6fa0',{align:'right',outline:null});y+=49;\n"
"      if(!save.pro){card(12,y,156,30,'#fffaf0','#ffd23f');b.drawImage(SPR.trophy,17,y+4);text(b,'PREMIUM',29,y+5,'#a8740a',{outline:null});\n"
"        ['x2 COINS FOREVER','REWARDS WITHOUT ADS'].forEach((q,k)=>{R(b,17,y+16+k*8,3,3,'#33b24a');text(b,q,23,y+15+k*8,'#13306b',{outline:null});});\n"
"        button('spro',120,y+4,44,14,'green',SHOP.premium.price,shopBuyPremium);text(b,'PAY ONCE',142,y+21,'#a8740a',{align:'center',outline:null});y+=33;}}\n"
# hero: premium in full
"    else if(!save.pro){card(12,y,156,58,'#fffaf0','#ffd23f');b.drawImage(SPR.trophy,17,y+4);text(b,'PREMIUM',29,y+5,'#a8740a',{outline:null});\n"
"      ['x2 COINS FOREVER','REWARDS WITHOUT ADS','GOLD PAINT, ALL MACHINES','12H HELPER SHED (WAS 6H)','+ '+SHOP.premium.coinRuns+' RUNS OF COINS NOW'].forEach((q,k)=>{R(b,17,y+17+k*8,3,3,'#33b24a');text(b,q,23,y+16+k*8,'#13306b',{outline:null});});\n"
"      button('spro',120,y+4,44,14,'green',SHOP.premium.price,shopBuyPremium);text(b,'PAY ONCE',142,y+21,'#a8740a',{align:'center',outline:null});y+=61;}\n"
"    else{card(12,y,156,32,'#fff6d8','#ffd23f');b.drawImage(SPR.trophy,17,y+4);text(b,'PREMIUM IS ON. THANK YOU!',29,y+5,'#a8740a',{outline:null});\n"
"      text(b,'x2 COINS, REWARDS WITHOUT ADS,',17,y+15,'#13306b',{outline:null});text(b,'GOLD PAINT AND THE 12H SHED',17,y+23,'#13306b',{outline:null});y+=35;}\n"
# gem packs
"    {const gy=y+2,fx2=!save.gemBuys,n2=v=>v.toLocaleString('en-US'),bi=gemBest();let need=shopNeed?shopNeed.cost-(save.gems||0):0;if(shopNeed&&need<=0){shopNeed=null;need=0;}\n"
"    let hi=-1;if(need>0){hi=SHOP.gems.findIndex(g=>g.gems*(fx2?2:1)>=need);if(hi<0)hi=SHOP.gems.length-1;}\n"
"    text(b,need>0?'NEED '+need+' MORE GEMS':'GEMS',14,gy,need>0?'#ff9aa8':'#9fc0e8',{outline:null});if(fx2)text(b,need>0?'FIRST BUY x2':'FIRST BUY: DOUBLE GEMS',166,gy,'#ff8fc8',{align:'right',outline:null});\n"
"    SHOP.gems.forEach((g,i)=>{const y=gy+8+i*16,best=i===bi;if(i===hi&&(tNow-shopNeed.t>1.2||Math.floor(tNow*5)%2===0))R(b,10,y-1,160,17,'#ff4fa3');\n"
"      card(12,y,156,15,best?'#fff6d8':'#eef3fb',best?'#ffd23f':'#9fc0e8');\n"
"      for(let k=0;k<=Math.min(4,i);k++)b.drawImage(SPR.gem,16+k*4,y+4-(k%2));\n"
"      let tx=44;text(b,n2(g.gems),tx,y+5,'#13306b',{outline:null});tx+=textW(n2(g.gems))+3;\n"
"      if(fx2){text(b,'x2',tx,y+5,'#e0397a',{outline:null});tx+=textW('x2')+3;}\n"
"      {const gb=gemBonus(i);if(gb){text(b,gb,tx,y+5,'#1f7a33',{outline:null});tx+=textW(gb)+3;}}\n"
"      if(best){const t=textW('BEST VALUE')+4<=116-tx?'BEST VALUE':'BEST',tw=textW(t)+4;if(tw<=116-tx){R(b,tx,y+3,tw,9,'#e8283f');text(b,t,tx+2,y+5,'#ffffff',{outline:null});}}\n"
"      button('sg'+i,118,y+1,46,13,'green',g.price,()=>IAP.buy(g.id,()=>{const first=!save.gemBuys,add=g.gems*(first?2:1);save.gemBuys=(save.gemBuys||0)+1;track('iap_test',{item:'gems_'+g.gems,price:g.price});save.gems=(save.gems||0)+add;sfx('buy');buzz(20);showToast('+'+n2(add)+' GEMS'+(first?' (FIRST BUY x2)':'')+(IAP.native()?'':' (TEST)'),'#ff8fc8');persist();}));});\n"
"    text(b,'NO RANDOM BOXES, EVER',W/2,gy+8+5*16+3,'#9fc0e8',{align:'center',outline:null});}\n")+s[z+len(z_mark):]
# --- COINS + RIDES: free gems moved out; rides move up; gems = purple, money = green; short of gems -> the gem packs
a=s.find("    {const left=adGemsLeft();\n      if(left>0)button('sad',12,146,156,14,'purple',");z_mark="      else button('sad',12,146,156,14,'grey','NO MORE FREE GEMS TODAY',()=>sfx('deny'));}\n"
z=s.find(z_mark,a);assert a>0 and z>a,(a,z);s=s[:a]+s[z+len(z_mark):]
rep("text(b,'WILD RIDES',14,166,'#9fc0e8',{outline:null});","text(b,'WILD RIDES',14,154,'#9fc0e8',{outline:null});")
rep("const ri=rideForSale(),nx=nextRideIdx(),y=174;","const ri=rideForSale(),nx=nextRideIdx(),y=162;")
rep("{const y=212;card(12,y,156,30,save.ridePass?","{const y=200;card(12,y,156,30,save.ridePass?")
rep("text(b,'MORE FREE GEMS: DAILY JOBS (+'+SHOP.dailyGems+')',W/2,250,'#ff8fc8',{align:'center',outline:null});text(b,'AND TROPHIES (+'+SHOP.trophyGems+')',W/2,258,'#ff8fc8',{align:'center',outline:null});",
    "text(b,'MORE FREE GEMS: DAILY JOBS (+'+SHOP.dailyGems+')',W/2,238,'#ff8fc8',{align:'center',outline:null});text(b,'AND TROPHIES (+'+SHOP.trophyGems+')',W/2,246,'#ff8fc8',{align:'center',outline:null});")
rep("button('sride',50,y+19,52,13,'gold',pr[0],()=>buyRide(ri,false));","button('sride',50,y+19,52,13,'green',pr[0],()=>buyRide(ri,false));")
rep("button('spass',124,pc>0?y+11:y+7,40,16,'gold',SHOP.ridePass.price,buyRidePass);","button('spass',124,pc>0?y+11:y+7,40,16,'green',SHOP.ridePass.price,buyRidePass);")
rep("button('sb'+i,122,y+2,42,16,ok?'green':'grey',null,()=>{if((save.gems||0)<bg.cost){sfx('deny');showToast('NEED '+bg.cost+' GEMS','#ff9aa8');return;}",
    "button('sb'+i,122,y+2,42,16,ok?'purple':'grey',null,()=>{if((save.gems||0)<bg.cost){sfx('deny');showToast('NEED '+(bg.cost-(save.gems||0))+' MORE GEMS','#ff9aa8');shopNeed={cost:bg.cost,t:tNow};shopTab=0;return;}")
rep("if(gems){if((save.gems||0)<pr[1]){sfx('deny');showToast('NEED '+pr[1]+' GEMS','#ff9aa8');return false;}",
    "if(gems){if((save.gems||0)<pr[1]){sfx('deny');showToast('NEED '+(pr[1]-(save.gems||0))+' MORE GEMS','#ff9aa8');if(shopOpen){shopNeed={cost:pr[1],t:tNow};shopTab=0;}return false;}")
# --- the map's SHOP button says FREE until the shop has been opened today (once the daily jobs are on)
rep("  if(dailyOn()&&!save.starter&&!(save.offers&&save.offers.seenShop)){R(b,156,by-2,6,6,K);R(b,157,by-1,4,4,'#e8283f');}",
    "  if(dailyOn()&&save.shopDay!==todayKey()&&adGemsLeft()>0){const tw=textW('FREE')+4;R(b,sx+sw-tw-1,by-5,tw+2,9,K);R(b,sx+sw-tw,by-4,tw,7,'#e8283f');text(b,'FREE',sx+sw-tw+2,by-3,'#ffffff',{outline:null});}\n"
    "  else if(dailyOn()&&!save.starter&&!(save.offers&&save.offers.seenShop)){R(b,156,by-2,6,6,K);R(b,157,by-1,4,4,'#e8283f');}")
open(f,'w',encoding='utf-8').write(s)
print('p173 lab shop v2: free gift on top, one hero offer, 48 h starter, one colour per way of paying, need-gems jump')
