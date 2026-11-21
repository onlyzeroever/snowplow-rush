# Snow Bank (price doc rev 25, approved Nov 21; Alex 22:25 "build everything else we need"). LAB ONLY for now.
#  - from the 10th job: a glass jar on the map (above the book) that fills after every finished job:
#    +4 gems a job, +1 a star, up to 400 (test drives don't count); "+6" floats up from it back on the map
#  - tap it: the Snow Bank card (the jar, gems inside and what they are worth in money, a bar with the 220 mark,
#    how it fills); from 220 gems it breaks open for $2.99 (store id snow_bank, consumable); the gems go to you and
#    the jar starts again from empty
#  - honest labels: UP TO 2X VALUE only when 400 gems at the smallest pack's rate are worth 2x the bank's price in the
#    prices on show (so it follows each store's currency); a full jar says FULL (it stops filling)
#  - the jar pulses when it can be broken, and shows a red dot until the first look
#  - events: bank_open; the purchase is an iap_test like the other store items
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("window.srNativeReady=()=>{","IAP.ids.bank='snow_bank';IAP.consumable.bank=1;\nwindow.srNativeReady=()=>{")
rep("if(P('ride_pass'))SHOP.ridePass.price=P('ride_pass');","if(P('ride_pass'))SHOP.ridePass.price=P('ride_pass');if(P('bank'))SHOP.bank.price=P('bank');")
rep("function drawShop(){",
    "SHOP.bank={price:'$2.99',open:220,max:400,perJob:4,perStar:1,from:10};let bankOpen=false,bankFx=null;\n"
    "function bankOn(){return (save.fbRuns||0)>=SHOP.bank.from;}\n"
    "function bankG(){return (save.bank&&save.bank.g)||0;}\n"
    "function bankValue(){const p=priceParse(SHOP.bank.price),g0=SHOP.gems[0],p0=priceParse(g0.price);return p&&p0&&p.n>0?SHOP.bank.max*p0.n/g0.gems/p.n:0;}\n"
    "function drawJar(x,y,s,f,glow){const P=(px,py,w,h,c)=>R(b,x+px*s,y+py*s,w*s,h*s,c);\n"
    "  P(4,0,12,1,K);P(3,1,14,3,K);P(4,1,12,2,'#e8283f');P(4,3,12,1,'#a01a2c');P(6,1,3,1,'#ff8a9a');\n"
    "  P(5,4,10,1,K);P(2,5,16,1,K);P(1,6,18,1,K);P(0,7,20,14,K);P(1,21,18,1,K);P(2,22,16,1,K);P(6,4,8,1,'#bfe3ff');P(3,5,14,1,'#d7edff');P(2,6,16,1,'#d7edff');P(1,7,18,14,'#d7edff');P(2,21,16,1,'#d7edff');\n"
    "  const rows=Math.round(15*Math.max(0,Math.min(1,f)));if(rows>0){const top=22-rows;for(let r=top;r<22;r++){const inset=r>=21?2:1;P(inset,r,20-inset*2,1,r===top?'#ffc2e0':'#ff8fc8');}for(let k=1;k<rows;k+=3)P(2+((k*7)%14),top+k,2,1,'#e0397a');for(let k=2;k<rows;k+=4)P(4+((k*11)%12),top+k,1,1,'#ffffff');}\n"
    "  P(5,10,10,5,K);P(6,11,8,3,'#fff6d8');P(9,11,2,1,'#ff4fa3');P(8,12,4,1,'#ff4fa3');P(9,13,2,1,'#c2185b');\n"
    "  P(2,8,1,11,'rgba(255,255,255,0.85)');P(17,9,1,4,'rgba(255,255,255,0.6)');\n"
    "  if(glow)for(let q=0;q<4;q++){const ph=(tNow*2+q*0.25)%1;if(ph<0.5){const sx=[-3,21,-2,20][q],sy=[6,9,17,19][q];P(sx,sy,1,1,'#ffd23f');if(ph<0.25){P(sx-1,sy,3,1,'#ffd23f');P(sx,sy-1,1,3,'#ffd23f');}}}}\n"
    "function drawBankJar(by){if(!bankOn())return;const g=bankG(),x=4,y=by-27,ok=g>=SHOP.bank.open,full=g>=SHOP.bank.max;\n"
    "  btn('bankjar',2,y-2,24,27,()=>{bankOpen=true;save.bank=save.bank||{g:0};save.bank.seen=true;sfx('click');try{track('bank_open',{gems:g});}catch(e){}persist();});\n"
    "  drawJar(x,y,1,g/SHOP.bank.max,ok);\n"
    "  if(full){const tw=textW('FULL')+4;R(b,x+10-Math.floor(tw/2)-1,y-6,tw+2,9,K);R(b,x+10-Math.floor(tw/2),y-5,tw,7,'#e8283f');text(b,'FULL',x+10-Math.floor(tw/2)+2,y-4,'#ffffff',{outline:null});}\n"
    "  else if(!(save.bank&&save.bank.seen)){R(b,x+17,y+3,6,6,K);R(b,x+18,y+4,4,4,'#e8283f');}\n"
    "  if(bankFx){if(bankFx.t0==null)bankFx.t0=tNow;const k=tNow-bankFx.t0;if(k>1.6)bankFx=null;else{const yy=Math.round(y+2-k*10);text(b,'+'+bankFx.n,x+10,yy,'#ff8fc8',{align:'center'});}}}\n"
    "function bankBuy(){if(bankG()<SHOP.bank.open){sfx('deny');return;}\n"
    "  IAP.buy('bank',()=>{const n=bankG();if(n<SHOP.bank.open)return;save.gems=(save.gems||0)+n;save.bank.g=0;save.bank.broken=(save.bank.broken||0)+1;track('iap_test',{item:'snow_bank',gems:n,price:SHOP.bank.price});\n"
    "    bankOpen=false;sfx('fanfare');buzz(30);youGot('SNOW BANK',[[SPR.gem,'+'+n+' GEMS','#ff8fc8'],[null,'THE JAR STARTS AGAIN','#9fc0e8']]);persist();});}\n"
    "function drawBank(){const x=14,y=56,w=152,h=204,B=SHOP.bank,g=bankG(),ok=g>=B.open,full=g>=B.max;b.fillStyle='rgba(11,24,56,0.84)';b.fillRect(0,0,W,H);btn('bankbg',0,0,W,H,()=>{});panel(x,y,w,h,'#13306b','#ffd23f');\n"
    "  text(b,'SNOW BANK',W/2,y+9,'#ffd23f',{align:'center',scale:2});text(b,'IT FILLS UP AS YOU PLAY',W/2,y+27,'#9fc0e8',{align:'center',outline:null});\n"
    "  drawJar(W/2-20,y+37,2,g/B.max,ok);\n"
    "  text(b,g+' GEMS INSIDE',W/2,y+87,'#ff8fc8',{align:'center'});if(g>0)text(b,'WORTH '+gemCash(g)+' IN GEM PACKS',W/2,y+96,'#9fc0e8',{align:'center',outline:null});\n"
    "  {const bx=x+16,bw=w-32,yy=y+106;R(b,bx,yy,bw,8,K);R(b,bx+1,yy+1,bw-2,6,'#0b1838');R(b,bx+1,yy+1,Math.round((bw-2)*Math.min(1,g/B.max)),6,'#ff8fc8');\n"
    "    const mx=bx+1+Math.round((bw-2)*B.open/B.max);R(b,mx,yy-2,1,12,'#ffd23f');text(b,''+B.open,mx,yy+11,'#ffd23f',{align:'center',outline:null});text(b,'0',bx,yy+11,'#9fc0e8',{outline:null});text(b,''+B.max,bx+bw,yy+11,'#9fc0e8',{align:'right',outline:null});}\n"
    "  text(b,'+'+B.perJob+' GEMS A JOB, +'+B.perStar+' A STAR',W/2,y+128,'#ffffff',{align:'center',outline:null});\n"
    "  text(b,full?'FULL: BREAK IT TO KEEP FILLING':ok?'READY TO BREAK OPEN':'BREAKS OPEN AT '+B.open+' GEMS',W/2,y+137,full?'#ff9aa8':ok?'#7fe08a':'#9fc0e8',{align:'center',outline:null});\n"
    "  if(Math.floor(bankValue()+1e-9)>=2){const t='UP TO '+Math.floor(bankValue()+1e-9)+'X VALUE',tw=textW(t)+6;R(b,W/2-Math.floor(tw/2),y+147,tw,9,'#e8283f');text(b,t,W/2,y+149,'#ffffff',{align:'center',outline:null});}\n"
    "  if(ok)button('bankbuy',x+26,y+159,w-52,20,'green',B.price,bankBuy,{scale:textW(B.price,2)<=w-60?2:1});\n"
    "  else button('bankbuy',x+26,y+159,w-52,20,'grey','NEED '+(B.open-g)+' MORE GEMS',()=>{sfx('deny');showToast('KEEP PLAYING: '+(B.open-g)+' MORE TO GO','#9fc0e8');});\n"
    "  button('bankno',x+46,y+183,w-92,16,'navy','NOT NOW',()=>{bankOpen=false;sfx('click');});}\n"
    "function drawShop(){")
# fill it after every finished job
rep("function drawSettings(){",
    "{const o=endRound;endRound=function(){const was=run&&run.ended;const r=o.apply(this,arguments);try{if(run&&!was&&run.res&&!run.bankDone&&!run.drive&&bankOn()){run.bankDone=true;save.bank=save.bank||{g:0};\n"
    "  const add=Math.min(SHOP.bank.max-save.bank.g,SHOP.bank.perJob+SHOP.bank.perStar*(run.res.stars||0));if(add>0){save.bank.g+=add;bankFx={n:add,t0:null};}persist();}}catch(e){}return r;};}\n"
    "function drawSettings(){")
# the jar on the map, above the book; the card over the map
rep("  const boy=button('book',3,by,22,18,'purple',","  drawBankJar(by);\n  const boy=button('book',3,by,22,18,'purple',")
rep("  if(settingsOpen)drawSettings();","  if(bankOpen&&state==='map')drawBank();\n  if(settingsOpen)drawSettings();")
rep("||!!gotCard);}","||!!gotCard||bankOpen);}")
open(f,'w',encoding='utf-8').write(s)
print('p177 lab Snow Bank: jar on the map from job 10, +4 gems a job +1 a star up to 400, break from 220 for $2.99')
