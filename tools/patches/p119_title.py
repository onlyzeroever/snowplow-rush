import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Title screen (Alex, Nov 17): the kid is the hero again (the Nov 16 menus pass had swapped him for a plow truck),
# drawn at 2x so he reads as the hero, clearing a road with his shovel. The village houses sit on the hill crest,
# bases tucked into a drift, clear of the pine row (one looked parked on top of a tree).
rep("for(const [hx,hy,c] of [[14,146,0],[60,140,2],[112,143,4],[150,149,1]]){const cp=mHouse(b,hx,hy,16,16,HOUSE_COLS[c][0],HOUSE_COLS[c][1],HOUSE_COLS[c][2],1,hx);if(cp)",
    "for(const [hx,hy,c] of [[14,113,0],[50,115,2],[112,136,4],[152,111,1]]){const cp=mHouse(b,hx,hy,16,16,HOUSE_COLS[c][0],HOUSE_COLS[c][1],HOUSE_COLS[c][2],1,hx);"
    "b.fillStyle='#e9f3fd';b.fillRect(hx-3,hy+14,22,4);b.fillRect(hx-1,hy+13,4,1);b.fillRect(hx+13,hy+13,5,1);if(cp)")
rep("const px=Math.round((tNow*24)%220-30);if(px>0){R(b,0,210,px,20,'#4a5068');R(b,0,210,px,1,'#a6c2ea');R(b,0,229,px,1,'#a6c2ea');for(let x=4;x<px-10;x+=12)R(b,x,219,6,1,'#ffd23f');}\n"
    "  drawRig(b,'truck',px,220,1,30,3,Math.floor(tNow*6)%2,Math.floor(tNow*8),false);for(let k=0;k<7;k++){const t2=(tNow*2.6+k/7)%1;const sx=px+17+Math.round(t2*16),sy=Math.round(206+k%3*3-Math.sin(t2*Math.PI)*12);R(b,sx,sy,k%2?2:1,k%2?2:1,'#ffffff');if(k%2)R(b,sx+1,sy+1,1,1,'#a6c2ea');}",
    "const px=Math.round((tNow*20)%240-30);{const cx=Math.max(0,px-6);if(cx>0){R(b,0,200,cx,28,'#4a5068');R(b,0,200,cx,1,'#a6c2ea');R(b,0,227,cx,1,'#a6c2ea');for(let x=3;x<cx-10;x+=14)R(b,x,213,7,2,'#ffd23f');}\n"
    "    for(let x=cx;x<W;x+=5)R(b,x+((x*3)%4),199+(x%3),2,1,'#e3ecf8');if(cx<W)R(b,cx,200,Math.min(4,W-cx),28,'#e9f1fd');}\n"
    "  {const kc=TITLE_KC||(TITLE_KC=Object.assign(document.createElement('canvas'),{width:40,height:40})),kg=kc.getContext('2d');kg.clearRect(0,0,40,40);drawRig(kg,'shovel',20,34,1,14,2,Math.floor(tNow*6)%2,0,false);\n"
    "   const ss=b.imageSmoothingEnabled;b.imageSmoothingEnabled=false;b.drawImage(kc,0,0,40,40,px-40,226-68,80,80);b.imageSmoothingEnabled=ss;}\n"
    "  for(let k=0;k<8;k++){const t2=(tNow*2.2+k/8)%1;const sx=px+12+Math.round(t2*20),sy=Math.round(196+k%3*3-Math.sin(t2*Math.PI)*18);R(b,sx,sy,k%2?3:2,k%2?3:2,'#ffffff');if(k%2)R(b,sx+2,sy+2,1,1,'#a6c2ea');}")
rep("let logoImg=null,logoReady=false,TITLE_PINE=null;","let logoImg=null,logoReady=false,TITLE_PINE=null,TITLE_KC=null;")
# Garage (Alex, Nov 17): on locked machine cards the third line ("x2.5 COINS  -  AFTER BLOWER") ran under the price.
# Locked cards now say just "AFTER BLOWER" there; the coin multiplier shows once the machine is next to buy.
rep("text(b,'x'+(cur?T2.value:t.value)+' COINS'+(!owned&&!next?'  -  AFTER '+TOOLS[i-1].name:''),x+37,y+22,",
    "text(b,!owned&&!next?'AFTER '+TOOLS[i-1].name:'x'+(cur?T2.value:t.value)+' COINS',x+37,y+22,")
# Shop (Alex, Nov 17): Premium perk bullets sat 1 px low against the 5 px caps; centre them on the text.
rep("forEach((q,k)=>{R(b,17,y+18+k*9,3,3,'#33b24a');","forEach((q,k)=>{R(b,17,y+17+k*9,3,3,'#33b24a');")
# Shop (Alex, Nov 17): the "TEST: x2 COINS" cheat from the early prototype was still in the live shop. Dev build only now.
rep("    button('stest',12,284,76,20,'purple','TEST: x2 COINS',","    if(DEV_MODE)button('stest',12,284,76,20,'purple','TEST: x2 COINS',")
open(f,'w',encoding='utf-8').write(s)
print('p119 title: kid hero, houses on the hill')
