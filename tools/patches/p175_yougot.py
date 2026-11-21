# "YOU GOT" card after a purchase (Nov 21, shop v2 follow-up). HELD from the live web game; in the lab and the app build.
#  - Premium, Starter Pack, gem packs and the Wild Ride Pass end on a card that lists what was just added (icons in one
#    column, words in one column, sparkles round the title), instead of a toast that is gone in a second
#  - on the web the card says nothing was charged (test shop)
#  - a Wild Ride bought in the shop (money or gems) closes the shop and plays the existing NEW WILD RIDE reveal
#  - youGot(title, rows) is there for the Snow Bank and the Event Pass
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function drawShop(){",
    "let gotCard=null;\n"
    "function youGot(title,rows){gotCard={title,rows,t:0};}\n"
    "function drawGot(dt){const G=gotCard;G.t+=dt||0.016;const n=G.rows.length,x=14,w=152,test=!IAP.native(),h=84+n*12+(test?9:0),y=Math.round(152-h/2);\n"
    "  b.fillStyle='rgba(11,24,56,0.86)';b.fillRect(0,0,W,H);btn('gotbg',0,0,W,H,()=>{});panel(x,y,w,h,'#13306b','#ffd23f');\n"
    "  for(let q=0;q<12;q++){const a=q*0.52+G.t*1.4,r=46+((G.t*20+q*7)%16);const px=Math.round(W/2+Math.cos(a)*r),py=Math.round(y+16+Math.sin(a)*r*0.22);if(py>y+3&&py<y+30&&px>x+4&&px<x+w-6)R(b,px,py,2,2,['#ffd23f','#c4a0f5','#ff4fa3','#5fb4ff'][q%4]);}\n"
    "  text(b,'YOU GOT',W/2,y+9,'#ffd23f',{align:'center',scale:2});text(b,G.title,W/2,y+28,'#9fc0e8',{align:'center',outline:null});\n"
    "  G.rows.forEach((r,i)=>{const yy=y+42+i*12,ic=r[0];if(ic)b.drawImage(ic,x+22+Math.floor((9-ic.width)/2),yy+3-Math.floor(ic.height/2));text(b,r[1],x+34,yy+1,r[2]||'#ffffff',{outline:null});});\n"
    "  if(test)text(b,'TEST MODE: NOTHING WAS CHARGED',W/2,y+h-37,'#7fe08a',{align:'center',outline:null});\n"
    "  button('gotok',x+36,y+h-26,w-72,18,'orange','NICE!',()=>{gotCard=null;sfx('click');});}\n"
    "function drawShop(){")
rep("if(shopOpen)drawShop();\n  if(ovA<1){b.restore();b.globalAlpha=1;}","if(shopOpen)drawShop();\n  if(ovA<1){b.restore();b.globalAlpha=1;}\n  if(gotCard)drawGot(dtD);")
rep("(evOpen&&state==='map'));}","(evOpen&&state==='map')||!!gotCard);}")
# what each purchase gives, on the card
rep("showToast('PREMIUM! +'+fmt(add)+' COINS','#ffd23f');",
    "youGot('PREMIUM',[[SPR.coin,'x2 COINS FOREVER','#ffd23f'],[SPR.trophy,'REWARDS WITHOUT ADS'],[SPR.star,'GOLD PAINT, ALL MACHINES'],[SPR.helper,'12H HELPER SHED'],[SPR.coinS,'+'+fmt(add)+' COINS NOW','#ffd23f']]);")
rep("showToast('STARTER PACK! +'+SHOP.starter.gems+' GEMS','#ffd23f');",
    "youGot('STARTER PACK',[[SPR.gem,'+'+SHOP.starter.gems+' GEMS','#ff8fc8'],[SPR.coin,'+'+fmt(add)+' COINS','#ffd23f'],[SPR.star,'THE EXPLORER OUTFIT']]);")
rep("function buyRidePass(){if(save.ridePass)return;save.ridePass=true;sfx('fanfare');showToast('WILD RIDE PASS!','#ffd23f');const i=rideForSale();if(i>=0)grantRide(i);persist();}",
    "function buyRidePass(){if(save.ridePass)return;save.ridePass=true;sfx('fanfare');const i=rideForSale(),got=i>=0&&grantRide(i);\n"
    "  youGot('WILD RIDE PASS',[[SPR.star,'EVERY WILD RIDE IS YOURS'],[null,'THE MOMENT IT APPEARS','#9fc0e8']].concat(got?[[SPR.check,TOOLS[i].name+': IN THE GARAGE','#7fe08a']]:[]));persist();}")
rep("showToast('+'+n2(add)+' GEMS'+(first?' (FIRST BUY x2)':'')+(IAP.native()?'':' (TEST)'),'#ff8fc8');",
    "youGot(n2(g.gems)+' GEM PACK',[[SPR.gem,'+'+n2(add)+' GEMS','#ff8fc8']].concat(first?[[null,'FIRST BUY: DOUBLED','#ff8fc8']]:[]));")
# a Wild Ride bought in the shop: the NEW WILD RIDE reveal
rep("button('sride',50,y+19,52,13,'green',pr[0],()=>buyRide(ri,false));",
    "button('sride',50,y+19,52,13,'green',pr[0],()=>{if(buyRide(ri,false)){shopOpen=false;rideReveal={tid:T3.id,t:0};}});")
rep("()=>buyRide(ri,true));}","()=>{if(buyRide(ri,true)){shopOpen=false;rideReveal={tid:T3.id,t:0};}});}")
rep("IAP.buy('ride_'+TOOLS[i].id,()=>{if(g(i,false)){ridePeek=null;",
    "IAP.buy('ride_'+TOOLS[i].id,()=>{if(g(i,false)){if(shopOpen){shopOpen=false;rideReveal={tid:TOOLS[i].id,t:0};}ridePeek=null;")
open(f,'w',encoding='utf-8').write(s)
print('p175 YOU GOT card after purchases; the NEW WILD RIDE reveal for rides bought in the shop')
