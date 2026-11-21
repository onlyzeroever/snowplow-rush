# Event Pass (price doc rev 25, approved Nov 21; Alex 22:25 "build everything else we need"). LAB ONLY for now.
#  - one pass per event weekend, $2.99 (store id event_pass) or 250 gems
#  - double event progress: every job's flakes count x2, and the flakes already earned double the moment it is bought
#    (any steps that reaches pay out straight away)
#  - the bonus skin: that event's paint for every machine, kept for good (a 7th slot in the skin panel appears once you
#    own one; tap it again to switch between event paints you own). The paints are recolours of the existing machines,
#    one colour per event (needs Alex's OK on the colours before it leaves the lab)
#  - shown in the event screen (a GET THE EVENT PASS button that opens the pass card); the map banner says x2 once owned
#  - short of gems: the shop opens on the gem packs with the right one outlined
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("window.srNativeReady=()=>{","IAP.ids.evpass='event_pass';IAP.consumable.evpass=1;\nwindow.srNativeReady=()=>{")
rep("if(P('bank'))SHOP.bank.price=P('bank');","if(P('bank'))SHOP.bank.price=P('bank');if(P('evpass'))SHOP.evPass.price=P('evpass');")
rep("function drawShop(){",
    "SHOP.evPass={price:'$2.99',gems:250};let passOpen=false;\n"
    "const EV_PAINT={blizzard:['BLIZZARD','#7fc8f8'],presents:['PRESENT','#ff6fb0'],goldrush:['NUGGET','#e8962a'],yetihunt:['YETI','#c8d6f0'],snowroll:['SNOWBALL','#eef4ff'],\n"
    "  blackice:['BLACK ICE','#3a5a8c'],snowday:['SNOW DAY','#a8e0ff'],timeattack:['TURBO','#4fd36a'],forts:['FORT','#ff6f8f'],stars:['STARLIGHT','#ffe24a']};\n"
    "function mixHex(a,c,t){const p=v=>[1,3,5].map(i=>parseInt(v.slice(i,i+2),16)),A=p(a),C=p(c);return '#'+A.map((v,i)=>Math.round(v+(C[i]-v)*t).toString(16).padStart(2,'0')).join('');}\n"
    "function evPal(kind){const c=(EV_PAINT[kind]||EV_PAINT.blizzard)[1],l=mixHex(c,'#ffffff',0.45),d=mixHex(c,'#000000',0.35);return {b:c,l,d,a:mixHex(c,'#ffffff',0.25),x:c,xd:d,xh:l};}\n"
    "function paintIcon(kind){const k='pi'+kind;if(paintIcon[k])return paintIcon[k];const c=mk(7,7),g=c.getContext('2d'),p=evPal(kind);R(g,0,0,7,7,K);R(g,1,1,5,5,p.b);R(g,1,1,5,2,p.l);R(g,1,5,5,1,p.d);return paintIcon[k]=c;}\n"
    "function passOwned(ev){return !!ev&&save.evPass===ev.id;}\n"
    "function evPassBuy(gems){const ev=evNow();if(!ev||passOwned(ev))return;\n"
    "  const grant=()=>{const e=evSave(ev),before=e.flakes;save.evPass=ev.id;e.flakes*=2;const msgs=[];while(e.got<EV_STEPS.length&&e.flakes>=EV_STEPS[e.got]){msgs.push(evReward(e.got));e.got++;track('event_milestone',{event:ev.id,step:e.got,flakes:e.flakes});}\n"
    "    save.evPaints=save.evPaints||{};save.evPaints[ev.kind]=true;save.evPaintSel=ev.kind;vcache.clear();passOpen=false;sfx('fanfare');buzz(30);\n"
    "    youGot('EVENT PASS',[[SPR.star,'x2 FLAKES, ALL EVENT','#ffd23f'],[null,'FLAKES SO FAR: '+before+' TO '+e.flakes,'#9fc0e8'],[paintIcon(ev.kind),EV_PAINT[ev.kind][0]+' MACHINE PAINT']].concat(msgs.slice(-2).map(m=>[SPR.check,m,'#7fe08a'])));persist();};\n"
    "  if(gems){const c=SHOP.evPass.gems;if((save.gems||0)<c){passOpen=false;evOpen=false;shopTab=0;openShopFrom('event');needGems(c,'event_pass');return;}\n"
    "    save.gems-=c;try{track('spend',{item:'event_pass',gems:c,event:ev.kind});}catch(e){}grant();}\n"
    "  else IAP.buy('evpass',()=>{track('iap_test',{item:'event_pass',price:SHOP.evPass.price,event:ev.kind});grant();});}\n"
    "function drawPass(){const ev=evNow();if(!ev){passOpen=false;return;}const d=EVENT_DEFS[ev.kind],pn=EV_PAINT[ev.kind]||EV_PAINT.blizzard,x=14,y=58,w=152,h=196;\n"
    "  b.fillStyle='rgba(11,24,56,0.84)';b.fillRect(0,0,W,H);btn('passbg',0,0,W,H,()=>{});panel(x,y,w,h,'#13306b',d.col);\n"
    "  text(b,'EVENT PASS',W/2,y+9,'#ffd23f',{align:'center',scale:2});text(b,d.name,W/2,y+27,d.col,{align:'center',outline:null});\n"
    "  const row=(ic,t,yy,c)=>{if(ic)b.drawImage(ic,x+22+Math.floor((9-ic.width)/2),yy+3-Math.floor(ic.height/2));text(b,t,x+34,yy+1,c||'#ffffff',{outline:null});};\n"
    "  row(SPR.star,'x2 FLAKES FOR EVERY JOB',y+42,'#ffd23f');row(SPR.star,'EARNED FLAKES DOUBLE TOO',y+54,'#ffd23f');row(paintIcon(ev.kind),pn[0]+' PAINT',y+66);row(SPR.check,'ALL MACHINES, KEPT',y+78,'#7fe08a');\n"
    "  text(b,'FOR THIS EVENT. ENDS IN '+fmtDur((ev.end-Date.now())/1000),W/2,y+93,'#9fc0e8',{align:'center',outline:null});\n"
    "  button('passbuy',x+26,y+106,w-52,20,'green',SHOP.evPass.price,()=>evPassBuy(false),{scale:textW(SHOP.evPass.price,2)<=w-60?2:1});\n"
    "  text(b,'OR',W/2,y+131,'#9fc0e8',{align:'center',outline:null});\n"
    "  const okG=(save.gems||0)>=SHOP.evPass.gems;button('passgem',x+26,y+140,w-52,18,okG?'purple':'grey',null,()=>evPassBuy(true));priceRow(SPR.gemS,''+SHOP.evPass.gems+' GEMS',W/2,y+146,'#ffffff');\n"
    "  if(!okG)text(b,'YOU HAVE '+(save.gems||0)+' GEMS',W/2,y+162,'#9fc0e8',{align:'center',outline:null});\n"
    "  button('passno',x+46,y+172,w-92,16,'navy','NOT NOW',()=>{passOpen=false;sfx('click');});}\n"
    "function drawShop(){")
# double flakes while the pass is owned
rep("const e=evSave(ev),f=Math.round(pct)+stars*10+(allClear?20:0);","const e=evSave(ev),f=(Math.round(pct)+stars*10+(allClear?20:0))*(passOwned(ev)?2:1);")
# the event screen: the pass between the prize line and the jobs (job cards a little shorter to make room)
rep("  text(b,'EVENT JOBS',x+10,ty+54,'#9fc0e8',{outline:null});\n"
    "  evJobs(ev).forEach((i,k)=>{const L=LEVELS[i],ry=ty+64+k*30;card(x+8,ry,w-16,26,'#eef3fb','#9fc0e8');text(b,L.name,x+14,ry+5,'#13306b',{outline:null});\n"
    "    text(b,(save.stars[i]||0)+' OF 3 STARS',x+14,ry+15,'#4f6fa0',{outline:null});button('evp'+k,x+w-58,ry+5,44,16,'orange','PLAY',()=>{evOpen=false;startLevelUI(i,{event:ev.id});});});",
    "  if(passOwned(ev)){b.drawImage(SPR.check,x+42,ty+53);text(b,'EVENT PASS: x2 FLAKES ON',x+52,ty+54,'#7fe08a',{outline:null});}\n"
    "  else button('evpass',x+22,ty+49,w-44,16,'gold','GET THE EVENT PASS: x2',()=>{passOpen=true;sfx('click');});\n"
    "  text(b,'EVENT JOBS',x+10,ty+72,'#9fc0e8',{outline:null});\n"
    "  evJobs(ev).forEach((i,k)=>{const L=LEVELS[i],ry=ty+80+k*26;card(x+8,ry,w-16,24,'#eef3fb','#9fc0e8');text(b,L.name,x+14,ry+4,'#13306b',{outline:null});\n"
    "    text(b,(save.stars[i]||0)+' OF 3 STARS',x+14,ry+13,'#4f6fa0',{outline:null});button('evp'+k,x+w-60,ry+4,46,16,'orange','PLAY',()=>{evOpen=false;startLevelUI(i,{event:ev.id});});});")
rep("  if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();","  if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();\n  if(passOpen&&state==='map')drawPass();")
rep("||!!gotCard||bankOpen);}","||!!gotCard||bankOpen||passOpen);}")
# the map banner says x2 once the pass is owned
rep("b.drawImage(SPR.star,8,y+3);text(b,d.name,19,y+4,d.col,{outline:null});",
    "b.drawImage(SPR.star,8,y+3);text(b,d.name,19,y+4,d.col,{outline:null});if(passOwned(ev)){const px=19+textW(d.name)+4;R(b,px,y+3,13,8,'#ffd23f');text(b,'x2',px+2,y+4,'#13306b',{outline:null});}")
# the paint: a 7th skin for every machine once you own one
rep("if((i===0&&isGold(tid))||i===5)Object.assign(p,GOLD_PAL,{gold:true});return p;}",
    "if((i===0&&isGold(tid))||i===5)Object.assign(p,GOLD_PAL,{gold:true});if(i===6&&save.evPaintSel&&EV_PAINT[save.evPaintSel])Object.assign(p,evPal(save.evPaintSel),{paint:save.evPaintSel});return p;}")
rep("function skinOwned(tid,i){return i===0||","function skinOwned(tid,i){if(i===6)return !!(save.evPaints&&save.evPaintSel&&save.evPaints[save.evPaintSel]);return i===0||")
rep("  for(let k=0;k<6;k++){const x=11+k*26,y=134,sel=k===skinSel,st=skinState(tid,k);card(x,y,25,40,sel?'#fff6d8':(k===5?'#fffaf0':'#eef3fb'),sel||k===5?'#ffd23f':'#9fc0e8');drawToolIcon(tid,x+1,y+3,23,k);\n"
    "    if(st==='own')text(b,skinIdx(tid)===k?'ON':'',x+12,y+30,'#1f7a33',{align:'center',outline:null});else if(st==='earn'){b.drawImage(SPR.trophy,x+8,y+28);}else if(st==='prem')text(b,'PREM',x+12,y+30,'#a8740a',{align:'center',outline:null});else priceDraw(skinPrice(tid,k),x+12,y+31,'#13306b','center',1);",
    "  const nS=skinOwned(tid,6)?7:6,pS=nS===7?23:26,wS=nS===7?22:25;\n"
    "  for(let k=0;k<nS;k++){const x=(nS===7?10:11)+k*pS,y=134,sel=k===skinSel,st=skinState(tid,k);card(x,y,wS,40,sel?'#fff6d8':(k>=5?'#fffaf0':'#eef3fb'),sel||k>=5?'#ffd23f':'#9fc0e8');drawToolIcon(tid,x+1,y+3,wS-2,k);\n"
    "    if(st==='own')text(b,skinIdx(tid)===k?'ON':'',x+Math.floor(wS/2),y+30,'#1f7a33',{align:'center',outline:null});else if(st==='earn'){b.drawImage(SPR.trophy,x+Math.floor((wS-9)/2),y+28);}else if(st==='prem')text(b,'PREM',x+Math.floor(wS/2),y+30,'#a8740a',{align:'center',outline:null});else priceDraw(skinPrice(tid,k),x+Math.floor(wS/2),y+31,'#13306b','center',1);")
rep("    btn('sks'+k,x,y,25,40,()=>{skinSel=k;sfx('click');});}",
    "    btn('sks'+k,x,y,wS,40,()=>{if(k===6&&skinSel===6){const ks=Object.keys(save.evPaints||{}).filter(q=>save.evPaints[q]);if(ks.length>1){save.evPaintSel=ks[(ks.indexOf(save.evPaintSel)+1)%ks.length];vcache.clear();persist();}}skinSel=k;sfx('click');});}")
rep("  const nm=names[skinSel];","  const nm=skinSel===6&&save.evPaintSel?EV_PAINT[save.evPaintSel][0]+' PAINT':names[skinSel];")
open(f,'w',encoding='utf-8').write(s)
print('p178 lab Event Pass: $2.99 or 250 gems, x2 flakes (earned ones too), the event paint for every machine')
