import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# UI: prices on buttons (coin/gem icon + number) are centred as one group under the button label, like the
# HUD buttons already were, instead of starting at the button's left edge.
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]; s=s.replace(a,b)
rep("function drawUpgrades(){","function priceRow(ico,str,cx,y,col,opt){const tw=ico.width+2+textW(str),sx=Math.round(cx-tw/2);b.drawImage(ico,sx,y);text(b,str,sx+ico.width+2,y,col,opt);}\nfunction drawUpgrades(){")
rep("b.drawImage(SPR.coinS,x+w-42,y+24);text(b,fmt(cost),x+w-35,y+24,afford?'#ffffff':'#ffd0d6');","priceRow(SPR.coinS,fmt(cost),x+w-25,y+24,afford?'#ffffff':'#ffd0d6');")
rep("b.drawImage(SPR.coinS,x+w-42,y+17);text(b,fmt(t.cost),x+w-35,y+17,afford?'#ffffff':'#ffd0d6');","priceRow(SPR.coinS,fmt(t.cost),x+w-25,y+17,afford?'#ffffff':'#ffd0d6');")
rep("b.drawImage(SPR.coinS,114,y+23);text(b,fmt(rw),121,y+23,'#ffffff',{outline:null});","priceRow(SPR.coinS,fmt(rw),135,y+23,'#ffffff',{outline:null});")
rep("b.drawImage(SPR.gemS,130,y+7);text(b,''+bg.cost,137,y+7,'#ffffff');","priceRow(SPR.gemS,''+bg.cost,143,y+7,'#ffffff');")
open(f,'w',encoding='utf-8').write(s)
print('p91 centred prices')
