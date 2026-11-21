# The BIG Snow Bank (Alex, Nov 22 01:49: "yes agree" to launching with it). After a player opens their first Snow Bank,
# a bigger jar takes its place: 800 gems, opens at 440, fills twice as fast (+10 a job, +4 a star), $4.99 (store id
# snow_bank_big). Pros raise the piggy bank's price after the first purchase; only buyers ever see this jar; UP TO 2X
# VALUE stays computed from the prices on show. HELD from the live web game; in the app. Preview: ?review=all&bank2.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("IAP.ids.bank='snow_bank';IAP.consumable.bank=1;",
    "IAP.ids.bank='snow_bank';IAP.consumable.bank=1;IAP.ids.bank2='snow_bank_big';IAP.consumable.bank2=1;")
rep("if(P('bank'))SHOP.bank.price=P('bank');","if(P('bank'))BANK1.price=P('bank');if(P('bank2'))BANK2.price=P('bank2');")
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
open(f,'w',encoding='utf-8').write(s)
print('p187 big Snow Bank after the first ($4.99, 800 gems, opens at 440)')
