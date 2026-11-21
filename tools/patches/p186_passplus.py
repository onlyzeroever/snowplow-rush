# EVENT PASS+ (Alex, Nov 22 01:40: "include the event pass plus straight away"): a second pass tier, $4.99 (store id
# event_pass_plus): the Event Pass plus 300 flakes right away (the first four rewards for a fresh player). Most pass games
# sell two paid tiers; the $4.99 option also makes the $2.99 pass the easy yes. HELD from the live web game; in the app.
# Switchable per event without an app update: an events.json entry with "plus": false hides it for that weekend.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("IAP.ids.evpass='event_pass';IAP.consumable.evpass=1;","IAP.ids.evpass='event_pass';IAP.consumable.evpass=1;IAP.ids.evplus='event_pass_plus';IAP.consumable.evplus=1;")
rep("if(P('evpass'))SHOP.evPass.price=P('evpass');","if(P('evpass'))SHOP.evPass.price=P('evpass');if(P('evplus'))SHOP.evPassPlus.price=P('evplus');")
rep("EVENTS.push({id:String(e.id||e.start),kind:e.kind,start:st,end:en});","EVENTS.push({id:String(e.id||e.start),kind:e.kind,start:st,end:en,plus:e.plus!==false});")
# EVENT PASS+
rep("SHOP.evPass={price:'$2.99',gems:250};","SHOP.evPass={price:'$2.99',gems:250};SHOP.evPassPlus={price:'$4.99',flakes:300,on:true};")
rep("const d=EVENT_DEFS[ev.kind],pn=EV_PAINT[ev.kind]||EV_PAINT.blizzard,x=14,y=58,w=152,h=196;",
    "const d=EVENT_DEFS[ev.kind],pn=EV_PAINT[ev.kind]||EV_PAINT.blizzard,PL=!!(SHOP.evPassPlus&&SHOP.evPassPlus.on&&ev.plus!==false),x=14,w=152,h=PL?228:196,y=Math.round(156-h/2),dy=PL?32:0;")
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
print('p186 EVENT PASS+ ($4.99, +300 flakes), switchable per event')
