import sys
BOOK=r'''const TR_PAL={y:'#ffd23f',Y:'#c98a12',o:'#e0a81a',w:'#ffffff',l:'#f4f8ff',g:'#c6d0dc',G:'#8793a8',s:'#dfe7f2',r:'#e03a4e',R:'#a8243a',p:'#ff9fb0',b:'#3f86d6',B:'#2a5fa8',c:'#9fd8ff',n:'#a8673a',N:'#7a4a2a',t:'#c98d4a',T:'#8a5a2a',O:'#f07a1a',e:'#33b24a',E:'#1f7a33',h:'#fff3a0',m:'#5a3a1e'};
const TR_ART={KEY:['................','................','................','................','..yyyy..........','.yhhyyY.........','.yh..yYyyyyyyy..','.yy..YYYYYYYYY..','.YyyyYY...Yy.Y..','..YYYY....YY.Y..','..........YY....','................','................','................','................','................'],
  MIT:['................','................','.....rrrr.......','....rpprrr......','....rprrrr......','....rrrrrr.rr...','....rrrrrrrrrR..','....rrrrrrrrRR..','....rrrrrrrRR...','....rrrrrrrR....','....rrrrrrRR....','...wwwwwwwwww...','...wgwgwgwgwg...','...gggggggggg...','................','................'],
  CAR:['................','................','................','................','.....BBBBBB.....','....BccBcccB....','...BBccBcccBB...','.bbbbbbbbbbbbbb.','.bhbbbbbbbbbbyb.','.bbbbbbbbbbbbbb.','.BBBkkBBBBBkkBB.','...kGgk...kGgk..','....kk.....kk...','................','................','................'],
  DUCK:['................','................','.........yyyy...','........yhyyyy..','........yykyyOO.','........yyyyyOO.','..y......yyyy...','..yy....yyyy....','..yyyyyyyyyyy...','..yyhhyyyyyyyY..','..yyyyyyyyyyyY..','...yyyyyyyyyYY..','....YYYYYYYYY...','................','................','................'],
  WATCH:['................','.......gg.......','......g..g......','.......gg.......','.....gggggg.....','....gwwwwwwG....','...gwwwkwwwwG...','...gwwwkwwwwG...','...gwwwkkkwwG...','...gwwwwwwwwG...','...gwkwwwwkwG...','....GwwwwwwG....','.....GGGGGG.....','................','................','................'],
  BALL:['................','................','................','.....bbbbbb.....','....bccbbbbb....','...bcwcbbbbbb...','...bccbbbcbbb...','...bbbbbcbbbb...','...bbbbcbbbBb...','...bbbcbbbBBb...','....bbbbbBBB....','.....BBBBBB.....','................','................','................','................'],
  COMP:['................','.......tt.......','.....tttttt.....','....tllllllT....','...tlllrrlllT...','...tlllrrlllT...','...tllrrrrllT...','...tlllkklllT...','...tllGGGGllT...','...tlllGGlllT...','...tlllGGlllT...','....TllllllT....','.....TTTTTT.....','................','................','................'],
  BEAR:['................','..nnn....nnn....','..nTn....nTn....','..nnnnnnnnnn....','...nnnnnnnn.....','...nnknnknn.....','...nnnttnnn.....','...nnntkttn.....','....nnttnn......','..nnnnnnnnnn....','.nnnnttttnnnn...','.nn.nttttn.nn...','....nnnnnn......','...nnn..nnn.....','...NNN..NNN.....','................'],
  HARM:['................','................','................','................','................','.gggggggggggggg.','.gsssssssssssgG.','.GGGGGGGGGGGGGG.','.nknknknknknknN.','.GGGGGGGGGGGGGG.','.gsssssssssssgG.','.GGGGGGGGGGGGGG.','................','................','................','................'],
  GLOBE:['................','.....cccccc.....','....cwcccccc....','...cwccceccc....','...cccceeecc....','...ccceeeeecc...','...ccccceccccc..','...cwcccncccc...','....cccccccc....','.....cccccc.....','...nnnnnnnnnn...','...nttttttttN...','...NNNNNNNNNN...','................','................','................'],
  COIN:['................','................','.....oooooo.....','....oyyyyyyo....','...oyyyhyyyYo...','...oyyyhhyyYo...','...oyhhhhhhYo...','...oyyhhhhyYo...','...oyyhyyhyYo...','...oyyyyyyyYo...','....oYYYYYYo....','.....oooooo.....','................','................','................','................'],
  GOLD:['.....yyyyyy.....','.....y....y.....','.....yyyyyy.....','.......YY.......','.......YY.......','.......YY.......','.......YY.......','......oooo......','....yyyyyyyy....','....yhyyyyyY....','....yhyyyyyY....','....yhyyyyyY....','....yhyyyyyY....','....yyyyyyyY....','.....yyyyyY.....','......YYYY......']};
const TR_TXT={KEY:['SOMEONE HAS BEEN LOCKED','OUT ALL WINTER.'],MIT:['THE OTHER ONE IS STILL','OUT THERE SOMEWHERE.'],CAR:['A LITTLE PLOW DRIVER','IN TRAINING. VROOM!'],
  DUCK:['IT SQUEAKS. OF COURSE','YOU SQUEEZED IT.'],WATCH:['STILL TICKING. GRANDAD','WILL BE SO PLEASED.'],BALL:['A PERFECT BLUE SWIRL.','THE BEST ONE IN THE BAG.'],
  COMP:['ALWAYS POINTS TO THE','NEXT BIG SNOWDRIFT.'],BEAR:['A BIT COLD, BUT','STILL SMILING.'],HARM:['PLAYS A LITTLE TUNE','WHEN THE WIND BLOWS.'],
  GLOBE:['A WHOLE WINTER IN','THE PALM OF YOUR HAND.'],COIN:['MINTED LONG BEFORE','THE VERY FIRST PLOW.'],GOLD:['SAID TO HAVE CLEARED','THE VERY FIRST ROAD.']};
const TRI={};
function trIco(id,sil){const key=id+(sil?'s':'');if(TRI[key])return TRI[key];const rows=TR_ART[id],c=mk(18,18),g=c.getContext('2d'),on=(x,y)=>x>=0&&y>=0&&x<16&&y<16&&rows[y][x]!=='.';
  for(let y=0;y<16;y++)for(let x=0;x<16;x++){if(!on(x,y))continue;g.fillStyle=sil?'#6e5a40':TR_PAL[rows[y][x]]||K;g.fillRect(x+1,y+1,1,1);}
  g.fillStyle=sil?'rgba(110,90,64,0.4)':K;for(let y=0;y<18;y++)for(let x=0;x<18;x++){if(on(x-1,y-1))continue;if(on(x-2,y-1)||on(x,y-1)||on(x-1,y-2)||on(x-1,y))g.fillRect(x,y,1,1);}
  return TRI[key]=c;}
let bookSel=-1,bookSelT=0;
function bookClose(){bookOpen=false;bookSel=-1;if(save.trSeen)for(const k in (save.treasures||{}))save.trSeen[k]=true;sfx('click');persist();}
function brassCorner(x,y,fx,fy){for(let i=0;i<7;i++){R(b,x+fx*i,y,1,2,i<6?'#ffd23f':'#c98a12');R(b,x,y+fy*i,2,1,i<6?'#ffd23f':'#c98a12');}R(b,x,y,1,1,'#fff3a0');R(b,x+fx*2,y+fy*2,1,1,'#c98a12');}
function trLabel(nm,cx,y,col){if(textW(nm)<=44){text(b,nm,cx,y+3,col,{align:'center',outline:null});return;}const sp=nm.indexOf(' ');text(b,nm.slice(0,sp),cx,y,col,{align:'center',outline:null});text(b,nm.slice(sp+1),cx,y+7,col,{align:'center',outline:null});}
function drawBook(){b.fillStyle='rgba(11,24,56,0.82)';b.fillRect(0,0,W,H);b.imageSmoothingEnabled=false;
  const tr=save.treasures||{},n=treasureCount(),seen=save.trSeen;
  // leather cover, stitching, brass corners
  R(b,7,24,166,284,K);R(b,6,25,168,282,K);R(b,7,25,166,282,'#6b3f22');R(b,7,25,166,1,'#8a5a32');R(b,7,306,166,1,'#4a2a14');
  for(let x=11;x<169;x+=4){R(b,x,28,2,1,'#b07a40');R(b,x,303,2,1,'#b07a40');}for(let y=29;y<303;y+=4){R(b,10,y,1,2,'#b07a40');R(b,169,y,1,2,'#b07a40');}
  brassCorner(7,25,1,1);brassCorner(172,25,-1,1);brassCorner(7,305,1,-1);brassCorner(172,305,-1,-1);
  // the page (with the edges of the pages under it)
  R(b,15,278,154,1,'#c9b48a');R(b,14,277,155,1,'#e3d1a5');R(b,169,34,1,244,'#c9b48a');R(b,168,33,1,244,'#e3d1a5');
  R(b,13,31,155,246,'#f4e8c8');dither(13,31,155,1,'#e6d4aa');dither(13,276,155,1,'#e6d4aa');dither(13,31,1,246,'#e6d4aa');dither(167,31,1,246,'#e6d4aa');
  R(b,13,31,155,1,'#e9dab5');
  // ribbon bookmark
  R(b,157,22,9,25,K);R(b,158,22,7,24,'#e03a4e');R(b,163,22,2,24,'#a8243a');R(b,158,22,1,24,'#ff6a7e');R(b,160,43,3,4,K);R(b,159,45,5,2,K);R(b,161,42,1,1,K);
  // title, subtitle
  text(b,'TREASURE BOOK',W/2-1,36,'#fbf3dc',{align:'center',scale:2,outline:null});text(b,'TREASURE BOOK',W/2-1,35,'#7a4a2a',{align:'center',scale:2,outline:null});
  if(n>=TREASURES.length)text(b,'COMPLETE! EVERY TREASURE FOUND',W/2,49,'#c98a12',{align:'center',outline:null});else text(b,'FIND THEM GLINTING IN THE SNOW',W/2,49,'#a0784a',{align:'center',outline:null});
  // progress bar: 12 segments, trophy at 6 (TREASURE HUNTER), star at 12
  {const bx=20,bw=140,by=58,f=Math.round((bw-2)*n/TREASURES.length);R(b,bx,by,bw,7,K);R(b,bx+1,by+1,bw-2,5,'#d9c69a');R(b,bx+1,by+1,bw-2,1,'#c9b48a');
    if(f){R(b,bx+1,by+1,f,5,'#ffd23f');R(b,bx+1,by+1,f,1,'#fff3a0');R(b,bx+1,by+5,f,1,'#c98a12');}
    for(let i=1;i<TREASURES.length;i++){const x=bx+1+Math.round((bw-2)*i/TREASURES.length);R(b,x,by+1,1,5,i<=n?'#c98a12':'#c9b48a');}
    const mx=bx+1+Math.round((bw-2)/2),got=!!(save.ach&&save.ach.hunter)||n>=6;R(b,mx-6,by-3,13,13,K);R(b,mx-5,by-2,11,11,got?'#ffd23f':'#d9c69a');R(b,mx-5,by-2,11,1,got?'#fff3a0':'#e6d4aa');
    if(!got)b.globalAlpha=0.45;b.drawImage(SPR.trophy,mx-Math.floor(SPR.trophy.width/2),by-Math.floor(SPR.trophy.height/2)+3);b.globalAlpha=1;
    R(b,bx+bw-6,by-3,13,13,K);R(b,bx+bw-5,by-2,11,11,n>=TREASURES.length?'#5a3a1e':'#d9c69a');if(n<TREASURES.length)b.globalAlpha=0.45;b.drawImage(SPR.star,bx+bw+1-Math.ceil(SPR.star.width/2),by+3-Math.floor(SPR.star.height/2));b.globalAlpha=1;}
  text(b,n+' OF '+TREASURES.length+' FOUND',20,70,'#7a4a2a',{outline:null});{const t='+'+Math.round(n*TREASURE_BONUS*100)+'% COINS',w2=textW(t);text(b,t,160-w2,70,'#a8740a',{outline:null});b.drawImage(SPR.coin,160-w2-10,69);}
  // the collection
  TREASURES.forEach((t2,k)=>{const id=t2[0],x=16+(k%3)*51,y=78+Math.floor(k/3)*44,found=!!tr[id],rare=id==='GOLD';
    R(b,x,y,46,41,'#ead9b0');R(b,x,y,46,1,'#d4c094');R(b,x,y,1,41,'#d4c094');R(b,x,y+40,46,1,'#fbf3dc');R(b,x+45,y,1,41,'#fbf3dc');
    if(rare){R(b,x+1,y+1,44,1,'#e0b040');R(b,x+1,y+1,1,39,'#e0b040');R(b,x+1,y+39,44,1,'#e0b040');R(b,x+44,y+1,1,39,'#e0b040');}
    if(found){R(b,x+9,y+18,28,5,'#4a1420');R(b,x+10,y+17,26,7,'#4a1420');R(b,x+10,y+18,26,4,'#a8324a');R(b,x+11,y+17,24,1,'#c84a62');R(b,x+11,y+18,24,1,'#e0687e');R(b,x+11,y+22,24,1,'#7a2236');
      const hop=Math.sin(tNow*2.2+k*1.7)>0.85?1:0;b.drawImage(trIco(id),x+14,y+1-hop);
      if((tNow*1.1+k*0.61)%3<0.3){R(b,x+31,y+2,1,5,'#ffffff');R(b,x+29,y+4,5,1,'#ffffff');}}
    else b.drawImage(trIco(id,true),x+14,y+4);
    trLabel(found?t2[1]:'???',x+23,y+26,found?'#5a3a1e':'#a8946c');
    if(found&&seen&&!seen[id]&&Math.floor(tNow*3)%3){R(b,x+1,y+1,17,7,K);R(b,x+2,y+2,15,5,'#e0397a');text(b,'NEW',x+3,y+2,'#ffffff',{outline:null});}
    btn('bk'+k,x,y,46,41,()=>{bookSel=k;bookSelT=tNow;if(seen&&tr[id])seen[id]=true;sfx('click');});});
  text(b,'TAP A TREASURE TO LOOK CLOSER',W/2,256,'#a0784a',{align:'center',outline:null});text(b,'EACH ONE: +2% COINS FOREVER',W/2,265,'#7a4a2a',{align:'center',outline:null});
  button('bkclose',54,284,72,18,'blue','DONE',bookClose);
  if(bookSel>=0)drawBookCard();}
function drawBookCard(){const k=bookSel,t2=TREASURES[k],id=t2[0],found=!!(save.treasures||{})[id],a=Math.min(1,(tNow-bookSelT)/0.12);
  btn('bkx',0,0,W,H,()=>{bookSel=-1;sfx('click');});
  b.fillStyle='rgba(40,24,10,0.55)';b.fillRect(0,0,W,H);b.save();b.globalAlpha=a;b.translate(0,Math.round((1-a)*6));
  const x0=16,y0=62,w=148,h=188,cx=W/2,iy=y0+40;
  R(b,x0+1,y0,w-2,h,K);R(b,x0,y0+1,w,h-2,K);R(b,x0+1,y0+1,w-2,h-2,'#c9a24a');R(b,x0+2,y0+2,w-4,h-4,'#fbf3dc');R(b,x0+4,y0+4,w-8,1,'#ead9b0');R(b,x0+4,y0+h-5,w-8,1,'#ead9b0');
  if(found){const rot=tNow*0.5;for(let i=0;i<8;i++){const a1=rot+i*Math.PI/4,a2=a1+0.2;pxPoly(b,[[cx,iy],[cx+Math.cos(a1)*36,iy+Math.sin(a1)*36],[cx+Math.cos(a2)*36,iy+Math.sin(a2)*36]],'#fff0bf');}
    R(b,cx-24,iy+18,48,8,'#4a1420');R(b,cx-25,iy+19,50,6,'#4a1420');R(b,cx-24,iy+19,48,5,'#a8324a');R(b,cx-23,iy+18,46,1,'#c84a62');R(b,cx-23,iy+19,46,1,'#e0687e');R(b,cx-23,iy+23,46,1,'#7a2236');
    b.drawImage(trIco(id),0,0,18,18,cx-27,iy-30,54,54);}
  else{b.drawImage(trIco(id,true),0,0,18,18,cx-27,iy-26,54,54);text(b,'?',cx+1,iy-8,'#f4e8c8',{align:'center',scale:2,outline:null});}
  text(b,found?t2[1]:'???',cx,y0+72,'#5a3a1e',{align:'center',scale:2,outline:null});R(b,cx-40,y0+86,80,1,'#e3d1a5');
  const L2=found?TR_TXT[id]||['','']:['NOT FOUND YET. LOOK FOR','A GLINT IN THE SNOW.'];text(b,L2[0],cx,y0+92,'#7a4a2a',{align:'center',outline:null});text(b,L2[1],cx,y0+100,'#7a4a2a',{align:'center',outline:null});
  if(found){const wh=(save.trWhere||{})[id];text(b,wh?'FOUND AT: '+wh:'FOUND!',cx,y0+114,'#a0784a',{align:'center',outline:null});}
  else text(b,'IT COULD BE ON ANY JOB',cx,y0+114,'#a0784a',{align:'center',outline:null});
  {const t=found?'+2% COINS FOREVER':'WORTH +2% COINS',tw=textW(t)+12;R(b,cx-tw/2-4,y0+126,tw+8,13,K);R(b,cx-tw/2-3,y0+127,tw+6,11,found?'#5a3a1e':'#8a7a5c');b.drawImage(SPR.coin,cx-tw/2,y0+129);text(b,t,cx-tw/2+11,y0+130,found?'#ffd23f':'#e6d4aa',{outline:null});}
  text(b,(k+1)+' / '+TREASURES.length,cx,y0+152,'#a0784a',{align:'center',outline:null});text(b,'TAP ANYWHERE TO CLOSE',cx,y0+170,'#c9b48a',{align:'center',outline:null});
  for(const [dx,dir] of [[x0+6,-1],[x0+w-20,1]]){const yb=y0+144;R(b,dx,yb,14,16,K);R(b,dx+1,yb+1,12,14,'#c9a24a');R(b,dx+1,yb+1,12,1,'#ffe9a8');
    for(let i=0;i<4;i++)R(b,dir<0?dx+8-i:dx+5+i,yb+4+i,1,8-i*2,'#5a3a1e');
    btn(dir<0?'bkp':'bkn',dx-4,yb-4,22,24,()=>{bookSel=(bookSel+dir+TREASURES.length)%TREASURES.length;bookSelT=tNow;const id2=TREASURES[bookSel][0];if(save.trSeen&&(save.treasures||{})[id2])save.trSeen[id2]=true;sfx('click');});}
  b.restore();}
'''
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# ---- 1. Tab screens slide like pages (Jobs < Upgrades < Garage): the old screen is pushed out as the new one comes in,
# 0.26s ease-out; the nav underline glides with it. Taps on the incoming page wait until it has landed.
rep("  ui=[];scrollAreas=[];\n  if(state==='title')drawTitle();",
    "  ui=[];scrollAreas=[];\n  {const TB=['map','upgrades','garage'];if(state!==draw.st&&draw.st&&TB.includes(state)&&TB.includes(draw.st)&&!overlayOpen()){const SH=NAV_Y-2;if(!draw.snap){draw.snap=mk(W,SH);draw.cur=mk(W,SH);}\n    const sg=draw.snap.getContext('2d');sg.clearRect(0,0,W,SH);sg.drawImage(b.canvas,0,0,W,SH,0,0,W,SH);draw.slT=tNow;draw.slFrom=TB.indexOf(draw.st);draw.slDir=TB.indexOf(state)>draw.slFrom?1:-1;}}\n  if(state==='title')drawTitle();")
rep("  if(state==='map'||state==='upgrades'||state==='garage')drawNav();",
    "  if(state==='map'||state==='upgrades'||state==='garage'){drawNav();const sl=slideE();if(sl<1){const SH=NAV_Y-2,cg=draw.cur.getContext('2d');cg.clearRect(0,0,W,SH);cg.drawImage(b.canvas,0,0,W,SH,0,0,W,SH);\n    const ox=Math.round(W*sl)*draw.slDir,seam=draw.slDir>0?W-ox:-ox;R(b,0,0,W,SH,'#0b1838');b.drawImage(draw.snap,-ox,0);b.drawImage(draw.cur,draw.slDir*W-ox,0);\n    b.fillStyle='rgba(11,24,56,0.35)';b.fillRect(draw.slDir>0?seam-3:seam,0,3,SH);R(b,draw.slDir>0?seam-1:seam,0,1,SH,'#0b1838');ui=ui.filter(u=>String(u.id).startsWith('nav-'));scrollAreas=[];}}")
rep("  if(state!==draw.st){if(draw.st&&['map','upgrades','garage'].includes(state)&&['map','upgrades','garage'].includes(draw.st))draw.stT=tNow;draw.st=state;}\n  if(draw.stT!=null&&tNow-draw.stT<0.16&&!ovk){b.fillStyle='rgba(11,24,56,'+(0.45*(1-(tNow-draw.stT)/0.16)).toFixed(2)+')';b.fillRect(0,0,W,NAV_Y);}\n",
    "  if(state!==draw.st)draw.st=state;\n")
rep("function drawNav(){","function slideE(){if(draw.slT==null)return 1;const t=Math.min(1,Math.max(0,(tNow-draw.slT)/0.26));return 1-Math.pow(1-t,3);}\nfunction drawNav(){")
rep("R(b,3+sel*59+20,NAV_Y+26,16,2,'#ffd23f');","{const e=slideE(),fx=e<1&&draw.slFrom!=null?draw.slFrom+(sel-draw.slFrom)*e:sel;R(b,Math.round(3+fx*59+20),NAV_Y+26,16,2,'#ffd23f');}")
# ---- 2. Treasure Book: a proper collector's book. Leather cover with stitching and brass corners, ribbon bookmark,
# a progress bar with the TREASURE HUNTER milestone, each treasure on a velvet cushion (silhouettes until found, NEW tags),
# and a close-up card per treasure (big sprite, a line about it, where it was found). New 16px treasure sprites, also used
# in the in-game "TREASURE!" toast.
rep("  const T2=TREASURES[tr.idx];save.treasures[T2[0]]=true;","  const T2=TREASURES[tr.idx];save.treasures[T2[0]]=true;(save.trWhere||(save.trWhere={}))[T2[0]]=(G.def&&G.def.name)||'';")
rep("achQueue.push({kind:'treasure',name:T2[1],t:2.6});","achQueue.push({kind:'treasure',name:T2[1],id:T2[0],t:2.6});")
rep("else if(q.kind==='treasure'){panel(x,y,160,24,'#5a3a1e','#ffd23f');b.drawImage(SPR.coin,x+6,y+8);text(b,'TREASURE: '+q.name,x+20,y+5,'#ffd23f');text(b,'+2% COINS FOREVER',x+20,y+14,'#ffffff',{outline:null});}",
    "else if(q.kind==='treasure'){panel(x,y,160,24,'#5a3a1e','#ffd23f');if(q.id&&TR_ART[q.id])b.drawImage(trIco(q.id),x+3,y+3);else b.drawImage(SPR.coin,x+6,y+8);text(b,'TREASURE: '+q.name,x+24,y+5,'#ffd23f');text(b,'+2% COINS FOREVER',x+24,y+14,'#ffffff',{outline:null});}")
rep("const boy=button('book',3,by,22,18,'purple',null,()=>{bookOpen=true;save.bookSeen=treasureCount();sfx('click');persist();})||0;",
    "const boy=button('book',3,by,22,18,'purple',null,()=>{bookOpen=true;bookSel=-1;if(!save.trSeen)save.trSeen=Object.assign({},save.treasures||{});save.bookSeen=treasureCount();sfx('click');persist();})||0;")
i=s.index("function drawBook(){");j=s.index("let trophyTab=0;",i)
s=s[:i]+BOOK+s[j:]
open(f,'w',encoding='utf-8').write(s)
print('p110 menus 3: sliding tabs, treasure book')
