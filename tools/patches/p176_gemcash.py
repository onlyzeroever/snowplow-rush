# What gems cost in money, next to every gem price where you buy (Nov 21). HELD from the live web game (it needs p170's
# gemCash); in the lab and the app build.
# EU consumer authorities' principles for in-game currencies: show the real-money price of an item priced in a virtual
# currency. The shop's coin bags already did (p170); now the garage does too: the BUY buttons for outfits and skins and
# the trail rows show "=$1.98" beside a gem price (at the smallest gem pack's rate, rounded up; store currency in apps).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function drawShop(){",
    "function gemMoney(price,x,y,align,col){if(!price||price.g==null)return;const t='='+gemCash(price.g);if(t.length>1)text(b,t,x,y,col||'#9fc0e8',{align:align||'left',outline:null});}\n"
    "function drawShop(){")
# outfits and skins: the BUY button moves left so button + money value sit centred together (coin prices unchanged)
rep("button('ofbuy',50,248,80,20,","const dxo=o.price.g!=null?-16:0;button('ofbuy',50+dxo,248,80,20,")
rep("text(b,'BUY',W/2-12,254,'#ffffff',{align:'center'});priceDraw(o.price,W/2+4,254,'#ffffff');}",
    "text(b,'BUY',W/2-12+dxo,254,'#ffffff',{align:'center'});priceDraw(o.price,W/2+4+dxo,254,'#ffffff');gemMoney(o.price,134+dxo,255);}")
rep("button('skbuy',50,198,80,20,","const dxs=pr.g!=null?-16:0;button('skbuy',50+dxs,198,80,20,")
rep("text(b,'BUY',W/2-12,204,'#ffffff',{align:'center'});priceDraw(pr,W/2+4,204,'#ffffff');}",
    "text(b,'BUY',W/2-12+dxs,204,'#ffffff',{align:'center'});priceDraw(pr,W/2+4+dxs,204,'#ffffff');gemMoney(pr,134+dxs,205);}")
# trails: the price button at x 116; the money value to its left, dark on the light row
rep("priceDraw(t.price,140,y+20,'#ffffff','center');}});",
    "priceDraw(t.price,140,y+20,'#ffffff','center');gemMoney(t.price,112,y+20,'right','#4f6fa0');}});")
open(f,'w',encoding='utf-8').write(s)
print('p176 gem prices in the garage show what they cost in money')
