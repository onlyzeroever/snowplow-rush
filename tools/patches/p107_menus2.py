import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:80],s.count(a));s=s.replace(a,b_)
# Menus pass 2 (Nov 16).
# 1. Trophies: each one gets its own icon (greyed with a lock until earned) and countable ones show a progress bar
#    with the count, the way achievement screens in good mobile games do; rewards show with a coin.
rep("let trophyTab=0;","""let trophyTab=0;const TICO={};
function trophyIcon(id){if(TICO[id])return TICO[id];const c=mk(11,11),g=c.getContext('2d'),Y='#ffd23f',W2='#ffffff',dot=(x,y,col)=>R(g,x,y,1,1,col);
  const ring=(cx,cy,r,col,fill)=>{g.fillStyle=K;pixCircle(g,cx,cy,r);g.fillStyle=col;pixCircle(g,cx,cy,r-1);if(fill){g.fillStyle=fill;pixCircle(g,cx,cy,r-2);}};
  switch(id){
    case 'first':R(g,5,0,2,7,K);R(g,5,1,1,5,'#c98d4a');R(g,2,6,7,5,K);R(g,3,7,5,3,'#8793a8');R(g,3,7,5,1,'#c6ccd8');R(g,4,0,4,2,K);break;
    case 'drive3':g.drawImage(SPR.bigStar,1,1);break;
    case 'combo':ring(5,5,5,'#f07a1a');R(g,2,3,2,1,W2);R(g,3,4,1,1,W2);R(g,2,5,2,1,W2);R(g,5,3,3,1,W2);R(g,7,4,1,1,W2);R(g,6,5,2,1,W2);R(g,7,6,1,1,W2);R(g,5,7,3,1,W2);break;
    case 'gifts':g.drawImage(SPR.present,1,2);g.drawImage(SPR.bow,1,0);break;
    case 'untouch':R(g,1,0,9,7,K);R(g,2,7,7,2,K);R(g,4,9,3,2,K);R(g,2,1,7,6,'#3f86d6');R(g,3,7,5,1,'#3f86d6');R(g,5,8,1,2,'#3f86d6');R(g,2,1,3,6,'#7fbaf2');R(g,5,2,1,5,W2);R(g,3,4,5,1,W2);break;
    case 'dodge':ring(6,5,4,'#e8f2fc');R(g,4,3,2,1,W2);R(g,0,4,2,1,'#9fd8ff');R(g,0,6,2,1,'#9fd8ff');R(g,1,8,2,1,'#9fd8ff');break;
    case 'gnome':g.drawImage(SPR.gnome,1,-1);break;
    case 'snowday':case 'winter':g.drawImage(SPR.frost,1,1);if(id==='winter'){R(g,7,7,4,4,K);R(g,8,8,2,2,Y);}break;
    case 'spotless':R(g,5,0,1,11,Y);R(g,0,5,11,1,Y);R(g,4,3,3,5,Y);R(g,3,4,5,3,Y);R(g,5,4,1,3,W2);R(g,4,5,3,1,W2);dot(1,1,W2);dot(9,9,W2);break;
    case 'garage':for(let r=0;r<4;r++)R(g,4-r,r,3+r*2,1,K);R(g,1,4,9,7,K);R(g,2,4,7,6,'#c98d4a');R(g,3,6,5,4,K);R(g,4,6,3,1,'#8793a8');R(g,4,8,3,1,'#8793a8');R(g,3,1,5,2,'#d8364b');break;
    case 'night':ring(5,5,5,Y);g.fillStyle='#13306b';pixCircle(g,7,4,3);dot(9,8,W2);dot(1,1,W2);break;
    case 'takeoff':R(g,4,0,3,11,K);R(g,0,4,11,3,K);R(g,2,8,7,2,K);R(g,5,1,1,9,W2);R(g,1,5,9,1,W2);R(g,3,9,5,1,W2);R(g,5,0,1,1,'#7fbaf2');break;
    case 'neighbour':R(g,1,2,4,5,K);R(g,6,2,4,5,K);R(g,0,3,11,4,K);R(g,2,7,7,2,K);R(g,4,9,3,2,K);R(g,2,3,3,3,'#ff4fa3');R(g,6,3,3,3,'#ff4fa3');R(g,1,4,9,2,'#ff4fa3');R(g,3,6,5,2,'#ff4fa3');R(g,5,8,1,1,'#ff4fa3');R(g,2,3,1,1,W2);break;
    case 'crusher':R(g,1,5,9,6,K);R(g,2,6,7,4,'#8793a8');R(g,3,6,1,4,'#c6ccd8');R(g,5,6,1,2,K);R(g,6,8,1,2,K);R(g,4,0,3,5,K);R(g,5,1,1,3,'#d8364b');dot(1,3,Y);dot(9,2,Y);break;
    case 'moo':R(g,1,2,9,8,K);R(g,2,3,7,6,W2);R(g,2,3,3,2,'#2a2a36');R(g,6,6,3,2,'#2a2a36');R(g,3,7,5,2,'#ffb0c0');R(g,0,1,2,2,K);R(g,9,1,2,2,K);dot(4,8,K);dot(6,8,K);break;
    case 'hunter':R(g,0,3,11,8,K);R(g,1,4,9,6,'#a8673a');R(g,1,4,9,2,'#c98d4a');R(g,1,6,9,1,Y);R(g,5,5,1,3,Y);R(g,1,1,9,3,K);R(g,2,2,7,1,'#c98d4a');break;
    case 'dressed':g.drawImage(SPR.helmet,0,2);break;
    case 'winter6':g.drawImage(SPR.frost,0,0);R(g,6,5,5,6,K);R(g,7,6,3,1,Y);R(g,7,7,1,3,Y);R(g,7,9,3,1,Y);R(g,9,8,1,1,Y);R(g,8,8,1,1,Y);break;
    default:g.drawImage(SPR.trophy,1,1);}
  return TICO[id]=c;}
function trophyProg(id){const st=save.stats||{};switch(id){case 'gifts':return [st.gifts||0,10];case 'dodge':return [st.dodges||0,10];case 'snowday':return [st.cells||0,100000];case 'crusher':return [st.crushed||0,25];
  case 'moo':return [st.cows||0,10];case 'hunter':return [treasureCount(),6];case 'dressed':return [Object.keys(save.skins||{}).length+Object.keys(save.outfits||{}).length-1+Object.keys(save.trails||{}).length-1,5];
  case 'neighbour':return [st.neighbours||0,2];case 'garage':return [Math.min(save.tool+1,BASE_TOOLS),BASE_TOOLS];case 'winter6':return [winterNo(),6];}return null;}""")
rep("const VY=52,VH=214,sy=scrollArea('trophies',6,VY,168,VH,ACH.length*16);",
    "const VY=52,VH=214,RH=19,sy=scrollArea('trophies',6,VY,168,VH,ACH.length*RH);")
rep("""  ACH.forEach((a,i)=>{const y=VY+i*16-sy,on=!!save.ach[a.id],hid=a.hidden&&!on;if(y<VY-16||y>VY+VH)return;R(b,12,y,156,15,on?'#1d4f9a':'#1b2a50');
    if(on)b.drawImage(SPR.trophy,15,y+3);else b.drawImage(SPR.lock,16,y+3);
    text(b,hid?'???':a.name,28,y+1,on?'#ffd23f':'#c6d9f3',{outline:null});text(b,hid?'A SECRET...':a.how,28,y+8,'#9fc0e8',{outline:null});
    text(b,a.reward?fmt(a.reward):'-',164,y+5,on?'#7fe08a':'#7d8aa0',{align:'right',outline:null});});
  b.restore();scrollBar(170,VY+2,VH-4,'trophies',ACH.length*16);""",
"""  ACH.forEach((a,i)=>{const y=VY+i*RH-sy,on=!!save.ach[a.id],hid=a.hidden&&!on;if(y<VY-RH||y>VY+VH)return;R(b,12,y,156,RH-1,on?'#1d4f9a':'#1b2a50');if(on)R(b,12,y,156,1,'#3f6fc8');
    R(b,14,y+2,15,14,K);R(b,15,y+3,13,12,on?'#ffe9a8':'#2a3a66');if(hid)text(b,'?',22,y+6,'#7d8aa0',{align:'center',outline:null});else{if(!on)b.globalAlpha=0.35;b.drawImage(trophyIcon(a.id),16,y+4);b.globalAlpha=1;}
    if(!on){R(b,24,y+11,5,5,K);R(b,25,y+13,3,2,'#c6ccd8');R(b,25,y+11,1,2,'#c6ccd8');R(b,27,y+11,1,2,'#c6ccd8');}else{R(b,25,y+12,4,4,K);R(b,26,y+13,2,2,'#7fe08a');}
    text(b,hid?'???':a.name,32,y+2,on?'#ffd23f':'#c6d9f3',{outline:null});text(b,hid?'A SECRET...':a.how,32,y+9,'#9fc0e8',{outline:null});
    if(a.reward){const rs=fmt(a.reward),rw=textW(rs);b.drawImage(SPR.coinS,164-rw-7,y+2);text(b,rs,164,y+2,on?'#7fe08a':'#c6d9f3',{align:'right',outline:null});}
    const pg=!on&&!hid?trophyProg(a.id):null;if(pg){const fr=Math.min(1,pg[0]/pg[1]),cs=fmt(Math.min(pg[0],pg[1]))+'/'+fmt(pg[1]);R(b,32,y+15,96,3,K);R(b,33,y+16,94,1,'#0b1838');R(b,33,y+16,Math.round(94*fr),1,fr>0?'#3fcf4a':'#0b1838');text(b,cs,164,y+12,'#9fc0e8',{align:'right',outline:null});}});
  b.restore();scrollBar(170,VY+2,VH-4,'trophies',ACH.length*RH);""")
# 2. Treasure Book: unfound treasures show as silhouettes (a tease of what to look for) instead of "?".
rep("if(found){for(const [a1,b1,c1,d1,col] of (TICON[t2[0]]||[]))R(b,x+16+a1-1,y+5+b1-1,c1,d1,col);}else text(b,'?',x+22,y+8,'#7a6a4a',{align:'center',outline:null});",
    "for(const [a1,b1,c1,d1,col] of (TICON[t2[0]]||[]))R(b,x+16+a1-1,y+5+b1-1,c1,d1,found?col:'#9a8a6a');if(found&&Math.floor(tNow*1.5+k)%4===0){R(b,x+27,y+6,1,3,'#ffffff');R(b,x+26,y+7,3,1,'#ffffff');}")
# 3. One word for dismissing a panel: DONE everywhere (was a mix of DONE / CLOSE / OK).
rep("button('jclose',54,228,72,18,'blue','CLOSE',","button('jclose',54,228,72,18,'blue','DONE',")
rep("button('wkclose',54,250,72,18,'blue','CLOSE',","button('wkclose',54,250,72,18,'blue','DONE',")
rep("button('pkclose',54,246,72,18,'blue','CLOSE',","button('pkclose',54,246,72,18,'blue','DONE',")
rep("button('wok',54,262,72,20,'orange','OK',","button('wok',54,262,72,20,'orange','DONE',")
open(f,'w',encoding='utf-8').write(s)
print('p107 menus pass 2')
s=open(f,encoding='utf-8').read()
# silhouettes a touch darker so the shape reads; names wrap at a space ("RUBBER DUC / K" -> "RUBBER / DUCK")
rep("R(b,x+16+a1-1,y+5+b1-1,c1,d1,found?col:'#9a8a6a');","R(b,x+16+a1-1,y+5+b1-1,c1,d1,found?col:'#7a6a4c');")
rep("const nm=found?t2[1]:'???';text(b,nm.length>10?nm.slice(0,10):nm,x+22,y+24,'#5a3a1e',{align:'center',outline:null});if(found&&nm.length>10)text(b,nm.slice(10).trim(),x+22,y+31,'#5a3a1e',{align:'center',outline:null});",
    "const nm=found?t2[1]:'???',cut=nm.length>10?(nm.lastIndexOf(' ',10)>0?nm.lastIndexOf(' ',10):10):nm.length;text(b,nm.slice(0,cut),x+22,y+24,'#5a3a1e',{align:'center',outline:null});if(found&&cut<nm.length)text(b,nm.slice(cut).trim(),x+22,y+31,'#5a3a1e',{align:'center',outline:null});")
open(f,'w',encoding='utf-8').write(s)
print('p107b book tweaks')
