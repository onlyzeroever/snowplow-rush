import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Store audit fixes (Nov 18, task 92).
# 1. Premium: no "was $7.99" strike price (it was never sold at $7.99; a made-up "was" price breaks UK/EU pricing rules
#    and store guidelines). Says PAY ONCE instead. Benefits ordered by value: x2 coins first.
# 2. Starter pack: 250 gems (was 200) and a "2X VALUE" tag, which is true even at the best gem-pack rate
#    (250 gems ~ $3.57 at 70 gems/$ + 10 runs of coins ~ $0.69 = $4.26 for $1.99, plus an outfit sold nowhere else).
# 3. A SHOP button on the map (the shop was only reachable from the small + by the coins: 8 opens from 5 testers).
# 4. Offers at the right moments, never during a job, at most one a day, always easy to close:
#    - starter pack once, from a player's 2nd session after 5+ jobs (or after 12 jobs);
#    - Premium after a player's 5th ad in a day ("every reward without the ad"), at most 3 times, 3+ days apart.
# 5. Tracking: shop_tab, offer_show, offer_tap (buy / later), and a session count (save.sess).

# 5. session count
rep("\nloadSave();\nlet offlineAway=0;","\nloadSave();save.sess=(save.sess||0)+1;\nlet offlineAway=0;")

# 1. premium card
rep("['NO ADS, EVER','REWARDS WITHOUT ADS','x2 COINS FOREVER','GOLD PAINT, ALL MACHINES','COIN PACK + 12H HELPER SHED']",
    "['x2 COINS FOREVER','REWARDS WITHOUT ADS','GOLD PAINT, ALL MACHINES','12H HELPER SHED (WAS 6H)','+ '+SHOP.premium.coinRuns+' RUNS OF COINS NOW']")
rep("else{text(b,SHOP.premium.was,144,y+5,'#9aa6ba',{align:'center',outline:null});R(b,134,y+8,21,1,'#e03a4e');button('spro',124,y+14,40,16,'gold',SHOP.premium.price,shopBuyPremium);text(b,'LAUNCH',144,y+33,'#e03a4e',{align:'center',outline:null});}",
    "else{button('spro',124,y+6,40,16,'gold',SHOP.premium.price,shopBuyPremium);text(b,'PAY ONCE',144,y+25,'#a8740a',{align:'center',outline:null});}")

# 2. starter pack
rep("starter:{price:'$1.99',gems:200,coinRuns:10}","starter:{price:'$1.99',gems:250,coinRuns:10}")
rep("if(save.starter)button('sst',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));else button('sst',124,y+7,40,16,'green',SHOP.starter.price,shopBuyStarter);}",
    "if(save.starter)button('sst',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));else{R(b,124,y+2,40,8,'#e8283f');text(b,'2X VALUE',144,y+3,'#ffffff',{align:'center',outline:null});button('sst',124,y+11,40,16,'green',SHOP.starter.price,shopBuyStarter);}}")

# 5. shop tabs
rep("button('stab0',12,52,76,14,shopTab===0?'gold':'navy','OFFERS',()=>{shopTab=0;sfx('click');});",
    "button('stab0',12,52,76,14,shopTab===0?'gold':'navy','OFFERS',()=>{shopTab=0;track('shop_tab',{tab:'offers'});sfx('click');});")
rep("button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;sfx('click');});",
    "button('stab1',92,52,76,14,shopTab===1?'gold':'navy','COINS + RIDES',()=>{shopTab=1;track('shop_tab',{tab:'coins_rides'});sfx('click');});")

# 3. shop button on the map
rep("// map / list toggle",
    "button('shopb',121,by,40,18,'green','SHOP',()=>{shopTab=0;save.offers=save.offers||{};save.offers.seenShop=true;openShop();});\n"
    "  if(dailyOn()&&!save.starter&&!(save.offers&&save.offers.seenShop)){R(b,156,by-2,6,6,K);R(b,157,by-1,4,4,'#e8283f');}\n"
    "  // map / list toggle")

# 4. offers
rep("function overlayOpen(){",
    "let offerOpen=null;\n"
    "function adCount(){const k=todayKey();if(!save.adDay||save.adDay.date!==k)save.adDay={date:k,n:0};save.adDay.n++;}\n"
    "function offerPick(){if(TEST_MODE&&!save.offerTest)return;if(!save.privSeen||offerOpen)return;const o=save.offers=save.offers||{},today=todayKey();if(o.last===today)return;\n"
    "  const ads=save.adDay&&save.adDay.date===today?save.adDay.n:0,runs=save.fbRuns||0;\n"
    "  if(!save.starter&&!o.starter&&(((save.sess||0)>=2&&runs>=5)||runs>=12)){offerOpen='starter';o.starter=true;}\n"
    "  else if(!save.pro&&(o.proN||0)<3&&ads>=5&&(o.proDay==null||dayIdx()-o.proDay>=3)){offerOpen='premium';o.proN=(o.proN||0)+1;o.proDay=dayIdx();}\n"
    "  if(offerOpen){o.last=today;track('offer_show',{kind:offerOpen,runs,sess:save.sess||0,ads});persist();}}\n"
    "function drawOffer(){const k=offerOpen,x=14,y=70,w=152,h=168;b.fillStyle='rgba(11,24,56,0.8)';b.fillRect(0,0,W,H);panel(x,y,w,h,'#13306b','#ffd23f');\n"
    "  const later=()=>{track('offer_tap',{kind:k,choice:'later'});offerOpen=null;sfx('click');};\n"
    "  const row=(ic,t,yy,c)=>{if(ic)b.drawImage(ic,x+22,yy);text(b,t,x+(ic?34:22),yy+1,c||'#ffffff',{outline:null});};\n"
    "  if(k==='starter'){text(b,'STARTER PACK',W/2,y+9,'#ffd23f',{align:'center',scale:2});R(b,W/2-24,y+27,48,9,'#e8283f');text(b,'2X VALUE',W/2,y+28,'#ffffff',{align:'center',outline:null});\n"
    "    row(SPR.gem,SHOP.starter.gems+' GEMS',y+46,'#ff8fc8');row(SPR.coin,fmt(runPay()*SHOP.starter.coinRuns)+' COINS ('+SHOP.starter.coinRuns+' RUNS)',y+60,'#ffd23f');row(SPR.star,'THE EXPLORER OUTFIT',y+74);\n"
    "    text(b,'ONE PER PLAYER. A THANK-YOU',W/2,y+92,'#9fc0e8',{align:'center',outline:null});text(b,'FOR PLAYING EARLY!',W/2,y+101,'#9fc0e8',{align:'center',outline:null});\n"
    "    button('ofbuy',x+26,y+116,w-52,20,'green',SHOP.starter.price,()=>{track('offer_tap',{kind:k,choice:'buy'});offerOpen=null;shopBuyStarter();},{scale:2});}\n"
    "  else{text(b,'PREMIUM',W/2,y+9,'#ffd23f',{align:'center',scale:2});text(b,'SKIP THE ADS, KEEP THE REWARDS',W/2,y+28,'#9fc0e8',{align:'center',outline:null});\n"
    "    row(SPR.trophy,'EVERY REWARD, NO AD',y+44);row(SPR.coin,'x2 COINS FOREVER',y+58,'#ffd23f');row(SPR.star,'GOLD PAINT, ALL MACHINES',y+72);row(null,'+ 12H HELPER SHED, COIN PACK',y+86,'#9fc0e8');\n"
    "    text(b,'PAY ONCE, KEEP IT FOR GOOD',W/2,y+101,'#9fc0e8',{align:'center',outline:null});\n"
    "    button('ofbuy',x+26,y+116,w-52,20,'gold',SHOP.premium.price,()=>{track('offer_tap',{kind:k,choice:'buy'});offerOpen=null;shopBuyPremium();},{scale:2});}\n"
    "  button('ofno',x+46,y+142,w-92,16,'navy','NOT NOW',later);}\n"
    "function overlayOpen(){")
rep("||(storyOpen&&state==='map'));}","||(storyOpen&&state==='map')||(offerOpen&&state==='map'));}")
rep("if(storyOpen&&state==='map')drawStory();","if(storyOpen&&state==='map')drawStory();\n  if(offerOpen&&state==='map'&&!storyOpen)drawOffer();")
rep("{storyOpen=ar;break;}}}}\n  persist();}","{storyOpen=ar;break;}}}}\n  if(!overlayOpen())offerPick();\n  persist();}")
rep("track('ad_watched',{kind:adScreen.gems?'free_gems':adScreen.onDone?'reward':'coins',screen:state});",
    "track('ad_watched',{kind:adScreen.gems?'free_gems':adScreen.onDone?'reward':'coins',screen:state});adCount();")
rep("function startLevel(idx,opts){","function startLevel(idx,opts){offerOpen=null;")

open(f,'w',encoding='utf-8').write(s)
print('p135 store: no made-up was-price, Premium benefits by value, starter 250 gems + 2X VALUE, SHOP button on the map, starter/Premium offers at set moments (1 a day max), shop_tab/offer_show/offer_tap tracking')
