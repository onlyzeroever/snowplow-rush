# Launch prices (Alex approved the pro review, Nov 21 20:23). HELD from the live web game; in the lab and the app build.
#  - Starter Pack $0.99: 150 gems + 10 runs of coins + Explorer outfit (3X VALUE holds: about $3.28 at the $0.99 pack rate)
#  - gems: 60 $0.99, 135 $1.99 (+10%), 365 $4.99 (+20%), 800 $9.99 (+30%), 1,850 $19.99 (+50%, BEST VALUE); no POPULAR tag
#    (no sales data behind it); labels round down against the $0.99 pack's 60.6 gems a dollar
#  - the first gem pack anyone buys gives double gems, shown on every pack until then
#  - Premium $6.99 (no "was" price anywhere); Wild Rides $1.99/$1.99/$2.99/$2.99/$3.99; Wild Ride Pass $7.99 with
#    SAVE 42% (against $13.95 one by one, rounded down)
#  - coin bags show what their gems cost in money (at the $0.99 pack rate, the most a player would pay)
#  - store product ids for the new ladder: gems_60, gems_135, gems_365, gems_800, gems_1850
#  - Nov 21 22:10: every label that compares prices is worked out from the prices on show, so it stays true in any
#    store currency (the apps show '£4.99', '4,99 €', '¥800' ...): pack bonuses, BEST VALUE, the coin bags' money
#    value and the pass saving. A price that can't be read shows no claim at all.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("gems:[{id:'g1',gems:60,price:'$0.99'},{id:'g2',gems:330,price:'$4.99',tag:'POPULAR'},{id:'g3',gems:700,price:'$9.99',tag:'BEST'}],",
    "gems:[{id:'g1',gems:60,price:'$0.99'},{id:'g15',gems:135,price:'$1.99'},{id:'g2',gems:365,price:'$4.99'},{id:'g3',gems:800,price:'$9.99'},{id:'g4',gems:1850,price:'$19.99'}],")
rep("premium:{price:'$4.99',was:'$7.99',coinRuns:25,shedS:43200},","premium:{price:'$6.99',coinRuns:25,shedS:43200},")
rep("starter:{price:'$1.99',gems:250,coinRuns:10},","starter:{price:'$0.99',gems:150,coinRuns:10},")
rep("rides:{monster:['$1.99',200],jet:['$2.49',250],mech:['$2.99',300],dragon:['$3.49',350],ufo:['$3.99',400]},",
    "rides:{monster:['$1.99',200],jet:['$1.99',250],mech:['$2.99',300],dragon:['$2.99',350],ufo:['$3.99',400]},")
rep("ridePass:{price:'$9.99'},","ridePass:{price:'$7.99'},")
rep("g1:'gems_60',g2:'gems_330',g3:'gems_700',","g1:'gems_60',g15:'gems_135',g2:'gems_365',g3:'gems_800',g4:'gems_1850',")
rep("consumable:{g1:1,g2:1,g3:1},","consumable:{g1:1,g15:1,g2:1,g3:1,g4:1},")
rep("text(b,'2X VALUE',","text(b,'3X VALUE',",2)
# gem packs: a list of five rows instead of three cards
a=s.find("    text(b,'GEMS',14,176,'#9fc0e8',{outline:null});")
z_mark="text(b,'NO RANDOM BOXES, EVER',W/2,248,'#9fc0e8',{align:'center',outline:null});"
z=s.find(z_mark,a);assert a>0 and z>a,(a,z)
s=s[:a]+("    {const fx2=!save.gemBuys,n2=v=>v.toLocaleString('en-US');text(b,'GEMS',14,176,'#9fc0e8',{outline:null});if(fx2)text(b,'FIRST BUY: DOUBLE GEMS',166,176,'#ff8fc8',{align:'right',outline:null});\n"
         "    SHOP.gems.forEach((g,i)=>{const y=184+i*18,best=i===gemBest();card(12,y,156,17,best?'#fff6d8':'#eef3fb',best?'#ffd23f':'#9fc0e8');\n"
         "      for(let k=0;k<=Math.min(4,i);k++)b.drawImage(SPR.gem,16+k*4,y+5-(k%2));\n"
         "      let tx=44;text(b,n2(g.gems),tx,y+6,'#13306b',{outline:null});tx+=textW(n2(g.gems))+3;\n"
         "      if(fx2){text(b,'x2',tx,y+6,'#e0397a',{outline:null});tx+=textW('x2')+3;}\n"
         "      {const gb=gemBonus(i);if(gb){text(b,gb,tx,y+6,'#1f7a33',{outline:null});tx+=textW(gb)+3;}}\n"
         "      if(best){const t=textW('BEST VALUE')+4<=116-tx?'BEST VALUE':'BEST',tw=textW(t)+4;R(b,tx,y+4,tw,9,'#e8283f');text(b,t,tx+2,y+5,'#ffffff',{outline:null});}\n"
         "      button('sg'+i,118,y+2,46,13,'green',g.price,()=>IAP.buy(g.id,()=>{const first=!save.gemBuys,add=g.gems*(first?2:1);save.gemBuys=(save.gemBuys||0)+1;track('iap_test',{item:'gems_'+g.gems,price:g.price});save.gems=(save.gems||0)+add;sfx('buy');buzz(20);showToast('+'+n2(add)+' GEMS'+(first?' (FIRST BUY x2)':'')+(IAP.native()?'':' (TEST)'),'#ff8fc8');persist();}));});\n"
         "    text(b,'NO RANDOM BOXES, EVER',W/2,276,'#9fc0e8',{align:'center',outline:null});}")+s[z+len(z_mark):]
# coin bags: the money value of their gems under the gem price
rep("      priceRow(SPR.gemS,''+bg.cost,143,y+7,'#ffffff');});",
    "      priceRow(SPR.gemS,''+bg.cost,143,y+4,'#ffffff');text(b,'='+gemCash(bg.cost),143,y+12,'#e8fbe8',{align:'center',outline:null});});")
rep("function drawShop(){",
    "// a price as the store writes it ('$0.99', '£0.99', '0,99 €', '¥160', 'CHF 1.00', 'KR 1 234,00'): its number, decimals,\n"
    "// separators and the text around it\n"
    "function priceParse(s){s=String(s||'');const m=s.match(/\\d(?:[\\d.,' \\u00a0\\u202f]*\\d)?/);if(!m)return null;const t=m[0].replace(/[ '\\u00a0\\u202f]/g,''),L=Math.max(t.lastIndexOf('.'),t.lastIndexOf(','));let n,dec=0,sep='.',ths=',';\n"
    "  if(L>=0){const after=t.length-L-1,head=t.slice(0,L).replace(/[.,]/g,'');if(after!==3||head==='0'){dec=after;sep=t[L];ths=sep===','?'.':',';n=parseFloat(head+'.'+t.slice(L+1));}else{ths=t[L];sep=ths==='.'?',':'.';n=parseFloat(t.replace(/[.,]/g,''));}}else n=parseFloat(t);\n"
    "  if(/[ \\u00a0\\u202f]/.test(m[0]))ths=' ';else if(m[0].includes(\"'\"))ths=\"'\";\n"
    "  return isFinite(n)?{n,dec,sep,ths,pre:s.slice(0,m.index),post:s.slice(m.index+m[0].length)}:null;}\n"
    "// an amount of money written the same way as a store price, rounded up (it never shows less than it costs)\n"
    "function priceFmt(p,v){const f=Math.pow(10,p.dec),r=Math.ceil(v*f-1e-6)/f,q=r.toFixed(p.dec).split('.');return p.pre+q[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,p.ths)+(p.dec?p.sep+q[1]:'')+p.post;}\n"
    "// what gems cost in money, at the smallest pack's rate (the most a player pays for a gem): EU guidance on in-game currencies\n"
    "function gemCash(n){const g=SHOP.gems[0],p=priceParse(g.price);return p?priceFmt(p,n*p.n/g.gems):'';}\n"
    "// each pack's bonus against the smallest pack, from the prices on show, rounded down to 10%; BEST VALUE = the best rate\n"
    "function gemRate(g){const p=priceParse(g&&g.price);return p&&p.n>0?g.gems/p.n:0;}\n"
    "function gemBonus(i){const r0=gemRate(SHOP.gems[0]),r=gemRate(SHOP.gems[i]);if(!i||!r0||!r)return '';const pc=Math.floor((r/r0-1)*10+1e-9)*10;return pc>0?'+'+pc+'%':'';}\n"
    "function gemBest(){let bi=-1,br=0;SHOP.gems.forEach((g,i)=>{const r=gemRate(g);if(r>br*1.001){br=r;bi=i;}});return bi>0?bi:-1;}\n"
    "function drawShop(){")
# Wild Ride Pass: the saving against buying the five one by one, rounded down
rep("if(save.ridePass)button('spass',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));else button('spass',124,y+7,40,16,'gold',SHOP.ridePass.price,buyRidePass);}",
    "if(save.ridePass)button('spass',124,y+7,40,16,'grey','OWNED',()=>sfx('click'));else{const pp=priceParse(SHOP.ridePass.price),rs=Object.values(SHOP.rides).map(r=>priceParse(r[0])),tot=rs.every(Boolean)?rs.reduce((a,r)=>a+r.n,0):0,pc=pp&&tot>0?Math.floor((1-pp.n/tot)*100):0;\n"
    "        if(pc>0){R(b,124,y+2,40,8,'#e8283f');text(b,'SAVE '+pc+'%',144,y+3,'#ffffff',{align:'center',outline:null});}button('spass',124,pc>0?y+11:y+7,40,16,'gold',SHOP.ridePass.price,buyRidePass);}}")
# the shop's "TEST MODE: NOTHING IS CHARGED" line only on the web (in the apps the store charges for real)
rep("text(b,'TEST MODE: NOTHING IS CHARGED',W/2,28,'#7fe08a',{align:'center',outline:null});",
    "if(!IAP.native())text(b,'TEST MODE: NOTHING IS CHARGED',W/2,28,'#7fe08a',{align:'center',outline:null});")
open(f,'w',encoding='utf-8').write(s)
print('p170 lab prices: $0.99 starter, 5-pack gem ladder with first-buy x2, Premium $6.99, rides + pass, gem cash values')
