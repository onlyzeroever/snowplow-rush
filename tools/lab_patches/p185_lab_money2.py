# Lab only (Alex, Nov 22: "however the pros would do it ... open to including what the pros add later"):
#  - a BIG Snow Bank after the first one is opened: 800 gems, opens at 440, fills twice as fast, $4.99 (store id snow_bank_big).
#    Pros raise the piggy bank's price after the first purchase; only buyers ever see this jar. UP TO 2X VALUE stays computed.
#  - EVENT PASS+: the Event Pass plus a 300-flake head start (the first four rewards for a fresh player), $4.99 (event_pass_plus).
#    Most passes offer a second, pricier tier; SHOP.evPassPlus.on switches it (lab: on).
#  - previews: ?review=all&bank2 (big jar with 500 gems inside)
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("IAP.ids.bank='snow_bank';IAP.consumable.bank=1;",
    "IAP.ids.bank='snow_bank';IAP.consumable.bank=1;IAP.ids.bank2='snow_bank_big';IAP.consumable.bank2=1;IAP.ids.evplus='event_pass_plus';IAP.consumable.evplus=1;")
rep("if(P('bank'))SHOP.bank.price=P('bank');","if(P('bank'))BANK1.price=P('bank');if(P('bank2'))BANK2.price=P('bank2');if(P('evplus'))SHOP.evPassPlus.price=P('evplus');")
# the jar you see depends on whether you have opened one before
rep("const BANK_PREVIEW=REVIEW_MODE&&/[?&]bank\\b/.test(location.search);",
    "const BANK_PREVIEW=REVIEW_MODE&&/[?&]bank2?\\b/.test(location.search),BANK2_PREVIEW=REVIEW_MODE&&/[?&]bank2\\b/.test(location.search);\n"
    "const BANK1=SHOP.bank,BANK2={price:'$4.99',open:440,max:800,perJob:10,perStar:4,from:10,seed:0,big:true};\n"
    "Object.defineProperty(SHOP,'bank',{get(){return save&&save.bank&&(save.bank.broken||0)>=1?BANK2:BANK1;},set(v){},configurable:true});")
rep("function bankOn(){if(BANK_PREVIEW&&!save.bank)save.bank={g:250};",
    "function bankOn(){if(BANK2_PREVIEW&&!save.bank)save.bank={g:500,broken:1,seen:true,intro:true};if(BANK_PREVIEW&&!save.bank)save.bank={g:250};")
rep("function bankBuy(){if(bankG()<SHOP.bank.open){sfx('deny');return;}\n  IAP.buy('bank',()=>{const n=bankG();if(n<SHOP.bank.open)return;",
    "function bankBuy(){const B0=SHOP.bank;if(bankG()<B0.open){sfx('deny');return;}\n  IAP.buy(B0.big?'bank2':'bank',()=>{const n=bankG();if(n<B0.open)return;")
rep("track('iap_test',{item:'snow_bank',gems:n,price:SHOP.bank.price});","track('iap_test',{item:B0.big?'snow_bank_big':'snow_bank',gems:n,price:B0.price});")
rep("youGot('SNOW BANK',[[SPR.gem,'+'+n+' GEMS','#ff8fc8'],[null,'THE JAR STARTS AGAIN','#9fc0e8']]);",
    "youGot(B0.big?'BIG SNOW BANK':'SNOW BANK',[[SPR.gem,'+'+n+' GEMS','#ff8fc8'],[null,B0.big?'THE BIG JAR STARTS AGAIN':'NEXT: A BIG JAR, 800 GEMS','#9fc0e8']]);")
rep("text(b,'SNOW BANK',W/2,y+8,'#ffd23f',{align:'center',scale:2});text(b,'GEMS PILE UP AS YOU PLAY',W/2,y+24,",
    "text(b,SHOP.bank.big?'BIG SNOW BANK':'SNOW BANK',W/2,y+8,'#ffd23f',{align:'center',scale:2});text(b,SHOP.bank.big?'IT FILLS TWICE AS FAST':'GEMS PILE UP AS YOU PLAY',W/2,y+24,")
# EVENT PASS+
rep("SHOP.evPass={price:'$2.99',gems:250};","SHOP.evPass={price:'$2.99',gems:250};SHOP.evPassPlus={price:'$4.99',flakes:300,on:true};")
rep("const d=EVENT_DEFS[ev.kind],pn=EV_PAINT[ev.kind]||EV_PAINT.blizzard,x=14,y=58,w=152,h=196;",
    "const d=EVENT_DEFS[ev.kind],pn=EV_PAINT[ev.kind]||EV_PAINT.blizzard,PL=!!(SHOP.evPassPlus&&SHOP.evPassPlus.on),x=14,w=152,h=PL?228:196,y=Math.round(156-h/2),dy=PL?32:0;")
rep("button('passbuy',x+26,y+106,w-52,20,'green',SHOP.evPass.price,()=>evPassBuy(false),{scale:textW(SHOP.evPass.price,2)<=w-60?2:1});\n  text(b,'OR',W/2,y+131,",
    "button('passbuy',x+26,y+106,w-52,20,'green',SHOP.evPass.price,()=>evPassBuy(false),{scale:textW(SHOP.evPass.price,2)<=w-60?2:1});\n"
    "  if(PL){button('passplus',x+26,y+130,w-52,18,'gold','PASS+  '+SHOP.evPassPlus.price,()=>evPassBuy(false,true));text(b,'ALSO +'+SHOP.evPassPlus.flakes+' FLAKES RIGHT NOW',W/2,y+151,'#ffd23f',{align:'center',outline:null});}\n"
    "  text(b,'OR',W/2,y+131+dy,")
rep("button('passgem',x+26,y+140,w-52,18,okG?'purple':'grey',null,()=>evPassBuy(true));priceRow(SPR.gemS,''+SHOP.evPass.gems+' GEMS',W/2,y+146,'#ffffff');\n  if(!okG)text(b,'YOU HAVE '+(save.gems||0)+' GEMS',W/2,y+162,",
    "button('passgem',x+26,y+140+dy,w-52,18,okG?'purple':'grey',null,()=>evPassBuy(true));priceRow(SPR.gemS,''+SHOP.evPass.gems+' GEMS',W/2,y+146+dy,'#ffffff');\n  if(!okG)text(b,'YOU HAVE '+(save.gems||0)+' GEMS',W/2,y+162+dy,")
rep("button('passno',x+46,y+172,w-92,16,'navy','NOT NOW',()=>{passOpen=false;sfx('click');});}","button('passno',x+46,y+172+dy,w-92,16,'navy','NOT NOW',()=>{passOpen=false;sfx('click');});}")
rep("function evPassBuy(gems){const ev=evNow();if(!ev||passOwned(ev))return;\n  const grant=()=>{const e=evSave(ev),before=e.flakes;save.evPass=ev.id;e.flakes*=2;",
    "function evPassBuy(gems,plus){const ev=evNow();if(!ev||passOwned(ev))return;\n  const grant=()=>{const e=evSave(ev),before=e.flakes;save.evPass=ev.id;e.flakes*=2;if(plus){e.flakes+=SHOP.evPassPlus.flakes;save.evPassPlus=ev.id;}")
rep("youGot('EVENT PASS',[[SPR.star,'x2 FLAKES, ALL EVENT','#ffd23f'],[null,'FLAKES SO FAR: '+before+' TO '+e.flakes,'#9fc0e8'],[paintIcon(ev.kind),EV_PAINT[ev.kind][0]+' MACHINE PAINT']].concat(",
    "youGot(plus?'EVENT PASS+':'EVENT PASS',[[SPR.star,'x2 FLAKES, ALL EVENT','#ffd23f']].concat(plus?[[SPR.star,'+'+SHOP.evPassPlus.flakes+' FLAKES HEAD START','#ffd23f']]:[],[[null,'FLAKES SO FAR: '+before+' TO '+e.flakes,'#9fc0e8'],[paintIcon(ev.kind),EV_PAINT[ev.kind][0]+' MACHINE PAINT']]).concat(")
rep("else IAP.buy('evpass',()=>{track('iap_test',{item:'event_pass',price:SHOP.evPass.price,event:ev.kind});grant();});}",
    "else IAP.buy(plus?'evplus':'evpass',()=>{track('iap_test',{item:plus?'event_pass_plus':'event_pass',price:plus?SHOP.evPassPlus.price:SHOP.evPass.price,event:ev.kind});grant();});}")
open(f,'w',encoding='utf-8').write(s)
print('p185 lab: big Snow Bank after the first ($4.99, 800 gems), EVENT PASS+ ($4.99, +300 flakes)')
