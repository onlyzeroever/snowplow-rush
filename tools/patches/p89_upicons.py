import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
# UI pass 1 (Nov 16): the Upgrades screen gets big, detailed icons (speedometer, plow blade with a width arrow,
# hazard bumper, coin stack, a helper kid with a shovel) in place of the tiny 7-9 px HUD icons.
blade=["..K..................K..",
       ".KK..................KK.",
       "KKKKKKKKKKKKKKKKKKKKKKKK",
       ".KK..................KK.",
       "..K..................K..",
       "........................",
       ".KKKKKKKKKKKKKKKKKKKKKK.",
       ".KEEEEEEEEEEEEEEEEEEEdK.",
       ".KYKYYYYYYYYYYYYYYYKYdK.",
       ".KYYYYYYYYYYYYYYYYYYYdK.",
       ".KyyyyyyyyyyyyyyyyyyydK.",
       ".KKKKKKKKKKKKKKKKKKKKKK.",
       "..WWWw...WWWWw...WWWw...",
       ".WWWWWw.WWWWWWw.WWWWWw.."]
for r in blade: assert len(r)==24,(len(r),r)
code=r"""
const UPICO={};function upIcon(k){if(UPICO[k])return UPICO[k];let c;
  if(k==='speed'){c=mk(24,18);const g=c.getContext('2d');for(let y=0;y<16;y++)for(let x=0;x<24;x++){const dx=x+0.5-12,dy=y+0.5-15,d=Math.sqrt(dx*dx+dy*dy);if(dy>0.5||d>11.6)continue;let col;
      if(d>10.5)col=K;else if(d>8.2){const a=Math.atan2(-dy,dx);col=a>2.1?'#33b24a':a>1.05?'#ffc727':'#e03a4e';if(dx<-3&&dy<-3&&d>9.6)col=a>2.1?'#6fd67f':a>1.05?'#ffe27a':'#f28b8b';}else col=(dx+dy<-6)?'#ffffff':'#f4f8ff';R(g,x,y,1,1,col);}
    for(const a of [2.75,2.2,1.6,1.0,0.4])R(g,Math.round(12+Math.cos(a)*7.2)-1,Math.round(15-Math.sin(a)*7.2)-1,1,1,'#55607a');
    for(let d=1;d<9;d++)R(g,Math.round(11.5+Math.cos(0.55)*d),Math.round(14.5-Math.sin(0.55)*d),1,2,'#d8364b');R(g,10,13,3,3,K);R(g,11,14,1,1,'#c6d0dc');R(g,0,15,24,3,K);R(g,1,16,22,1,'#55607a');}
  else if(k==='size'){c=spr(BLADE_ROWS,{E:'#ffe27a',d:'#c98a12',y:'#d49a12',w:'#c6d9f3'});}
  else if(k==='bumper'){c=mk(24,16);const g=c.getContext('2d');R(g,1,3,18,10,K);R(g,0,4,20,8,K);for(let y=4;y<12;y++)for(let x=1;x<19;x++){if((y===4||y===11)&&(x===1||x===18))continue;R(g,x,y,1,1,((x+y)%6<3)?'#ffc727':'#2a2a36');}
    R(g,2,4,16,1,'#ffe27a');R(g,2,11,16,1,'#1b1f3b');R(g,4,13,2,3,K);R(g,13,13,2,3,K);R(g,21,3,2,1,K);R(g,21,7,3,1,K);R(g,21,11,2,1,K);R(g,20,5,1,1,K);R(g,20,9,1,1,K);}
  else if(k==='value'){c=mk(24,20);const g=c.getContext('2d');const disk=(x,y)=>{R(g,x+1,y,7,1,K);R(g,x,y+1,9,3,K);R(g,x+1,y+4,7,1,K);R(g,x+1,y+1,7,1,'#ffe27a');R(g,x+1,y+2,7,1,'#ffd23f');R(g,x+1,y+3,7,1,'#c98a12');};disk(1,15);disk(1,12);disk(2,9);
    g.fillStyle=K;pixCircle(g,15,12,7);for(let y=5;y<20;y++)for(let x=8;x<23;x++){const dx=x-15,dy=y-12,d=Math.sqrt(dx*dx+dy*dy);if(d<=6.3)R(g,x,y,1,1,dx+dy>4?'#c98a12':dx+dy<-5?'#ffe27a':'#ffd23f');}
    const sf='#c98a12';R(g,15,8,1,9,sf);R(g,11,12,9,1,sf);for(let i=1;i<4;i++){R(g,15-i,12-i,1,1,sf);R(g,15+i,12-i,1,1,sf);R(g,15-i,12+i,1,1,sf);R(g,15+i,12+i,1,1,sf);}R(g,15,12,1,1,'#ffe27a');
    R(g,4,1,1,5,'#ffffff');R(g,2,3,5,1,'#ffffff');R(g,4,0,1,1,'#8fb0dc');R(g,4,6,1,1,'#8fb0dc');R(g,1,3,1,1,'#8fb0dc');R(g,7,3,1,1,'#8fb0dc');}
  else{c=mk(22,20);const g=c.getContext('2d');g.drawImage(spr(ROWS_DOWN,{Y:'#3f86d6',y:'#2a5fa8',R:'#33b24a',r:'#1f7a33',M:'#1f7a33'}),0,2);
    for(let i=0;i<9;i++)R(g,13+Math.round(i*0.55),3+i,2,1,K);for(let i=0;i<8;i++)R(g,14+Math.round(i*0.55),3+i,1,1,'#c98d4a');R(g,15,12,7,6,K);R(g,16,13,5,4,'#c6d0dc');R(g,16,13,5,1,'#f4f8ff');R(g,20,14,1,3,'#8793a8');
    R(g,17,0,3,1,'#ffd23f');R(g,18,-1,1,3,'#ffd23f');}
  return UPICO[k]=c;}
"""
code="const BLADE_ROWS="+repr(blade).replace("'",'"')+";"+code
a="function drawUpgrades(){"
assert s.count(a)==1
s=s.replace(a,code+a,1)
old="const rows=[['speed',SPR.boot],['size',SPR.bladeIco],['bumper',SPR.helmet],['value',SPR.coinBig],['helpers',SPR.helper]];"
assert s.count(old)==1
s=s.replace(old,"const rows=[['speed',upIcon('speed')],['size',upIcon('size')],['bumper',upIcon('bumper')],['value',upIcon('value')],['helpers',upIcon('helpers')]];")
open(f,'w',encoding='utf-8').write(s)
print('p89 upgrade icons')
