# Snow Bank (price doc rev 25, approved Nov 21; Alex 23:28 and 23:31: include it, better jar art, lined up). HELD from the live web game; in the lab and the app build.
#  - from the 10th job: a glass jar on the map (above the book) that fills after every finished job:
#    starts with 50 gems in it (Alex Nov 22: pace it like the pros, ready around job 30); +5 gems a job, +2 a star, up to 400 (test drives don't count); "+6" floats up from it back on the map
#  - tap it: the Snow Bank card (the jar, gems inside and what they are worth in money, a bar with the 220 mark,
#    how it fills); from 220 gems it breaks open for $2.99 (store id snow_bank, consumable); the gems go to you and
#    the jar starts again from empty
#  - honest labels: UP TO 2X VALUE only when 400 gems at the smallest pack's rate are worth 2x the bank's price in the
#    prices on show (so it follows each store's currency); a full jar says FULL (it stops filling)
#  - the jar pulses when it can be broken, and shows a red dot until the first look
#  - events: bank_open; the purchase is an iap_test like the other store items
#  - preview: ?review=all&bank shows the jar with 250 gems in it (review saves only)
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("if(label)text(b,label,x+w/2,y+Math.floor((h-5)/2)-1+oy,'#ffffff',{align:'center',scale:opt.scale||1});",
    "if(label&&opt.icon){const ic=opt.icon,sc=opt.scale||1,tw=textW(label,sc),lx=x+Math.floor((w-(ic.width+4+tw))/2);b.drawImage(ic,lx,y+Math.floor((h-ic.height)/2)-1+oy);text(b,label,lx+ic.width+4,y+Math.floor((h-5*sc)/2)-1+oy,'#ffffff',{scale:sc});}\n"
    "  else if(label)text(b,label,x+w/2,y+Math.floor((h-5)/2)-1+oy,'#ffffff',{align:'center',scale:opt.scale||1});")
rep("window.srNativeReady=()=>{","IAP.ids.bank='snow_bank';IAP.consumable.bank=1;\nwindow.srNativeReady=()=>{")
rep("if(P('ride_pass'))SHOP.ridePass.price=P('ride_pass');","if(P('ride_pass'))SHOP.ridePass.price=P('ride_pass');if(P('bank'))SHOP.bank.price=P('bank');")
rep("function drawShop(){",
    "SHOP.bank={price:'$2.99',open:220,max:400,perJob:5,perStar:2,from:10,seed:50};let bankOpen=false,bankFx=null;\n"
    "const BANK_PREVIEW=REVIEW_MODE&&/[?&]bank\\b/.test(location.search);\n"
    "function bankOn(){if(BANK_PREVIEW&&!save.bank)save.bank={g:250};return (save.fbRuns||0)>=SHOP.bank.from||BANK_PREVIEW;}\n"
    "function bankG(){return (save.bank&&save.bank.g)||0;}\n"
    "function bankValue(){const p=priceParse(SHOP.bank.price),g0=SHOP.gems[0],p0=priceParse(g0.price);return p&&p0&&p.n>0?SHOP.bank.max*p0.n/g0.gems/p.n:0;}\n"
    "// the jar: frosted glass, a blue lid with snow on it, real gem pieces piling up inside (map icon and card sizes)\n"
    "function drawJarArt(x,y,w,h,f,big){const lid=big?8:4,neck=big?3:2,by=y+lid+neck,bh=h-lid-neck,g2=b;\n"
    "  R(g2,x+2,y+1,w-4,lid-1,K);R(g2,x+3,y,w-6,1,K);R(g2,x+3,y+1,w-6,lid-2,'#2f7fd6');R(g2,x+3,y+lid-2,w-6,1,'#1d4f9a');\n"
    "  R(g2,x+3,y+1,w-6,big?3:1,'#f4f8ff');if(big){R(g2,x+5,y+4,2,1,'#f4f8ff');R(g2,x+w-9,y+4,3,1,'#f4f8ff');R(g2,x+3,y+1,w-6,1,'#ffffff');}\n"
    "  R(g2,x+4,y+lid,w-8,neck,K);R(g2,x+5,y+lid,w-10,neck,'#d4ebff');\n"
    "  if(big){R(g2,x+3,by,w-6,1,K);R(g2,x+1,by+1,w-2,2,K);R(g2,x,by+3,w,bh-6,K);R(g2,x+1,by+bh-3,w-2,2,K);R(g2,x+3,by+bh-1,w-6,1,K);\n"
    "    R(g2,x+3,by+1,w-6,1,'#e6f4ff');R(g2,x+2,by+2,w-4,1,'#e6f4ff');R(g2,x+1,by+3,w-2,bh-6,'#e6f4ff');R(g2,x+2,by+bh-3,w-4,1,'#e6f4ff');R(g2,x+3,by+bh-2,w-6,1,'#e6f4ff');R(g2,x+3,by+1,w-6,1,'#cfe6fb');\n"
    "    for(const q of [[5,4],[9,3],[w-8,5],[w-12,3],[14,6]])R(g2,x+q[0],by+q[1],1,1,'#ffffff');}\n"
    "  else{R(g2,x+1,by,w-2,bh,K);R(g2,x,by+1,w,bh-2,K);R(g2,x+1,by+1,w-2,bh-2,'#e6f4ff');R(g2,x+1,by+1,w-2,1,'#cfe6fb');}\n"
    "  if(f>0){const inX=x+1,inW=w-2,botY=by+bh-2,gw=big?7:3,gh=big?7:3,sx=big?6:4,sy=big?5:3,rows=[];\n"
    "    for(let r=0;r<20;r++){const yy=botY-gh+1-r*sy;if(yy<by+(big?2:1))break;const nA=Math.floor((inW-gw)/sx)+1,n=r%2?nA-1:nA,wd=(n-1)*sx+gw;rows.push({yy,n,x0:inX+Math.floor((inW-wd)/2)});}\n"
    "    const cap=rows.reduce((a,q)=>a+q.n,0);let left=f>=1?cap:Math.max(1,Math.round(cap*f));\n"
    "    for(const q of rows){if(left<=0)break;const m=Math.min(q.n,left),s0=Math.floor((q.n-m)/2);left-=m;\n"
    "      for(let i=s0;i<s0+m;i++){const gx=q.x0+i*sx;if(big)g2.drawImage(SPR.gem,gx,q.yy);else{R(g2,gx,q.yy,3,3,'#b3216e');R(g2,gx+1,q.yy,1,3,'#ff4fa3');R(g2,gx,q.yy+1,3,1,'#ff4fa3');R(g2,gx+1,q.yy+1,1,1,'#ffc2e0');R(g2,gx,q.yy,1,1,'#d63a8a');}}}}\n"
    "  R(g2,x+2,by+2,1,bh-5,'rgba(255,255,255,0.85)');if(big)R(g2,x+3,by+2,1,Math.floor(bh/3),'rgba(255,255,255,0.5)');R(g2,x+w-3,by+3,1,Math.max(2,Math.floor(bh/4)),'rgba(255,255,255,0.6)');}\n"
    "// the map button: the jar in a button of the book button's size, right above it\n"
    "function drawBankJar(by){if(!bankOn())return;const g=bankG(),x=3,w=22,h=23,y=by-h-3,ok=g>=SHOP.bank.open,full=g>=SHOP.bank.max;\n"
    "  const oy=button('bankjar',x,y,w,h,ok?'gold':'blue',null,()=>{bankOpen=true;save.bank=save.bank||{g:SHOP.bank.seed};save.bank.seen=true;save.bank.intro=true;sfx('click');try{track('bank_open',{gems:g});}catch(e){}persist();})||0;\n"
    "  if(!(save.bank&&save.bank.seen)&&Math.floor(tNow*3)%2){R(b,x-1,y-1,w+2,1,'#ffd23f');R(b,x-1,y+h,w+2,1,'#ffd23f');R(b,x-1,y,1,h,'#ffd23f');R(b,x+w,y,1,h,'#ffd23f');}\n"
    "  drawJarArt(x+4,y+2+oy,14,18,g/SHOP.bank.max,false);\n"
    "  if(ok&&!full){const ph=(tNow*1.6)%1;if(ph<0.35){R(b,x+w-4,y+3+oy,1,3,'#ffffff');R(b,x+w-5,y+4+oy,3,1,'#ffffff');}else if(ph>0.5&&ph<0.85){R(b,x+3,y+12+oy,1,3,'#ffffff');R(b,x+2,y+13+oy,3,1,'#ffffff');}}\n"
    "  if(full){const tw=textW('FULL')+4,tx=x+Math.floor(w/2)-Math.floor(tw/2);R(b,tx-1,y-7,tw+2,9,K);R(b,tx,y-6,tw,7,'#e8283f');text(b,'FULL',tx+2,y-5,'#ffffff',{outline:null});}\n"
    "  else if(!(save.bank&&save.bank.seen)){R(b,x+w-5,y-2,6,6,K);R(b,x+w-4,y-1,4,4,'#e8283f');}\n"
    "  if(bankFx&&bankFx.ready&&!bankFx.said){bankFx.said=true;showToast('SNOW BANK: READY TO OPEN','#ffd23f');}\n"
    "  if(bankFx){if(bankFx.t0==null)bankFx.t0=tNow;const k=tNow-bankFx.t0;if(k>1.6)bankFx=null;else{const yy=Math.round(y-2-k*10);text(b,'+'+bankFx.n,x+Math.floor(w/2),yy,'#ff8fc8',{align:'center'});}}}\n"
    "// one card the first time the jar appears, so it is explained once (not a pop-up in the middle of the screen)\n"
    "function drawBankIntro(dt){const x=6,w=W-12,h=52,y=MAP_VY+16;btn('bankintrobg',x,y,w,h,()=>{});panel(x,y,w,h,'#13306b','#ffd23f');b.drawImage(SPR.gem,x+9,y+5);\n"
    "  text(b,'NEW: THE SNOW BANK',x+21,y+6,'#ffd23f',{outline:null});text(b,'EVERY JOB ADDS GEMS TO THE JAR',x+21,y+17,'#ffffff',{outline:null});text(b,'AT THE BOTTOM LEFT. OPENS AT '+SHOP.bank.open+'.',x+21,y+25,'#9fc0e8',{outline:null});\n"
    "  button('bankintrook',x+w-116,y+h-18,52,13,'navy','GOT IT',()=>{save.bank=save.bank||{g:SHOP.bank.seed};save.bank.intro=true;persist();sfx('click');});\n"
    "  button('bankintroopen',x+w-60,y+h-18,52,13,'blue','LOOK',()=>{save.bank=save.bank||{g:SHOP.bank.seed};save.bank.intro=true;save.bank.seen=true;bankOpen=true;persist();sfx('click');});}\n"
    "function bankBuy(){if(bankG()<SHOP.bank.open){sfx('deny');return;}\n"
    "  IAP.buy('bank',()=>{const n=bankG();if(n<SHOP.bank.open)return;save.gems=(save.gems||0)+n;save.bank.g=0;save.bank.broken=(save.bank.broken||0)+1;track('iap_test',{item:'snow_bank',gems:n,price:SHOP.bank.price});\n"
    "    bankOpen=false;sfx('fanfare');buzz(30);youGot('SNOW BANK',[[SPR.gem,'+'+n+' GEMS','#ff8fc8'],[null,'THE JAR STARTS AGAIN','#9fc0e8']]);persist();});}\n"
    "function drawBank(){const x=14,w=152,h=200,y=56,B=SHOP.bank,g=bankG(),ok=g>=B.open,full=g>=B.max,v=Math.floor(bankValue()+1e-9);\n"
    "  b.fillStyle='rgba(11,24,56,0.84)';b.fillRect(0,0,W,H);btn('bankbg',0,0,W,H,()=>{});panel(x,y,w,h,'#13306b','#ffd23f');\n"
    "  text(b,'SNOW BANK',W/2,y+8,'#ffd23f',{align:'center',scale:2});text(b,'GEMS PILE UP AS YOU PLAY',W/2,y+24,'#9fc0e8',{align:'center',outline:null});\n"
    "  const jx=W/2-17,jy=y+34;drawJarArt(jx,jy,34,46,g/B.max,true);\n"
    "  if(ok){const ph=(tNow*1.6)%1,sp=(px,py)=>{R(b,px,py-2,1,5,'#ffd23f');R(b,px-2,py,5,1,'#ffd23f');};if(ph<0.4)sp(jx-6,jy+16);else if(ph>0.5&&ph<0.9)sp(jx-4,jy+38);}\n"
    "  if(v>=2){const t2=v+'X VALUE',sw=textW(t2)+6,sx2=jx+29,sy2=jy+12;R(b,sx2+1,sy2,sw-2,17,K);R(b,sx2,sy2+1,sw,15,K);R(b,sx2+1,sy2+1,sw-2,15,'#e8283f');R(b,sx2+2,sy2+1,sw-4,1,'#ff6b7d');R(b,sx2+1,sy2+15,sw-2,1,'#a81c2e');\n"
    "    text(b,'UP TO',sx2+Math.floor(sw/2),sy2+3,'#ffd23f',{align:'center',outline:null});text(b,t2,sx2+Math.floor(sw/2),sy2+9,'#ffffff',{align:'center',outline:null});}\n"
    "  {const t=''+g,tw=textW(t,2),gx=Math.round(W/2-(tw+10)/2);b.drawImage(SPR.gem,gx,y+86);text(b,t,gx+10,y+84,'#ff8fc8',{scale:2});}\n"
    "  text(b,g>0?'WORTH '+gemCash(g)+' IN GEM PACKS':'FINISH JOBS TO FILL IT',W/2,y+99,'#9fc0e8',{align:'center',outline:null});\n"
    "  {const bx=x+16,bw=w-32,yy=y+110,fw=Math.round((bw-2)*Math.min(1,g/B.max));R(b,bx,yy,bw,8,K);R(b,bx+1,yy+1,bw-2,6,'#0b1838');if(fw>0){R(b,bx+1,yy+1,fw,6,'#ff8fc8');R(b,bx+1,yy+1,fw,1,'#ffc2e0');R(b,bx+1,yy+6,fw,1,'#d0307f');}\n"
    "    const mx=bx+1+Math.round((bw-2)*B.open/B.max);R(b,mx,yy-2,1,12,'#ffd23f');text(b,''+B.open,mx,yy+12,'#ffd23f',{align:'center',outline:null});text(b,'0',bx,yy+12,'#9fc0e8',{outline:null});text(b,''+B.max,bx+bw,yy+12,'#9fc0e8',{align:'right',outline:null});}\n"
    "  text(b,'+'+B.perJob+' GEMS A JOB, +'+B.perStar+' A STAR',W/2,y+133,'#ffffff',{align:'center',outline:null});\n"
    "  text(b,full?'FULL! OPEN IT TO KEEP FILLING':ok?'READY TO OPEN!':(B.open-g)+' MORE GEMS TO OPEN IT',W/2,y+142,full?'#ff9aa8':ok?'#7fe08a':'#9fc0e8',{align:'center',outline:null});\n"
    "  if(ok)button('bankbuy',x+26,y+154,w-52,20,'green',B.price,bankBuy,{scale:textW(B.price,2)<=w-60?2:1});\n"
    "  else button('bankbuy',x+26,y+154,w-52,20,'grey','OPENS AT '+B.open,()=>{sfx('deny');showToast('KEEP PLAYING: '+(B.open-g)+' MORE TO GO','#9fc0e8');},{icon:SPR.lock});\n"
    "  button('bankno',x+46,y+179,w-92,16,'navy','NOT NOW',()=>{bankOpen=false;sfx('click');});}\n"
    "function drawShop(){")
# fill it after every finished job
rep("function drawSettings(){",
    "{const o=endRound;endRound=function(){const was=run&&run.ended;const r=o.apply(this,arguments);try{if(run&&!was&&run.res&&!run.bankDone&&!run.drive&&bankOn()){run.bankDone=true;save.bank=save.bank||{g:SHOP.bank.seed};\n"
    "  const add=Math.min(SHOP.bank.max-save.bank.g,SHOP.bank.perJob+SHOP.bank.perStar*(run.res.stars||0)),before=save.bank.g;if(add>0){save.bank.g+=add;bankFx={n:add,t0:null};}\n"
    "  if(before<SHOP.bank.open&&save.bank.g>=SHOP.bank.open&&!save.bank.readySaid){save.bank.readySaid=true;bankFx&&(bankFx.ready=true);}persist();}}catch(e){}return r;};}\n"
    "function drawSettings(){")
# the jar on the map, above the book; the card over the map
rep("  const boy=button('book',3,by,22,18,'purple',","  drawBankJar(by);\n  const boy=button('book',3,by,22,18,'purple',")
rep("  if(settingsOpen)drawSettings();","  if(bankOpen&&state==='map')drawBank();\n  if(settingsOpen)drawSettings();")
rep("  if(state==='map'&&!overlayOpen()&&!save.privSeen)drawPrivacyCard(dtD);","  if(state==='map'&&!overlayOpen()&&!save.privSeen)drawPrivacyCard(dtD);\n  else if(state==='map'&&!overlayOpen()&&bankOn()&&!(save.bank&&save.bank.intro)&&!BANK_PREVIEW)drawBankIntro(dtD);")
rep("||!!gotCard);}","||!!gotCard||bankOpen);}")
open(f,'w',encoding='utf-8').write(s)
print('p177 lab Snow Bank: jar on the map from job 10, +4 gems a job +1 a star up to 400, break from 220 for $2.99')
