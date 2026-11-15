import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def swapfn(name,new):
    global s
    assert s.count('function '+name+'(')==1,name
    a=s.index('function '+name+'(');depth=0;i=s.index('{',a)
    while True:
        ch=s[i]
        if ch=='{':depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:break
        elif ch in "'\"":
            q=ch;i+=1
            while s[i]!=q:
                if s[i]=='\\':i+=1
                i+=1
        i+=1
    s=s[:a]+new+s[i+1:]
# Props audit batch 2 (Nov 16): vehicles seen from above. Same canvas sizes and footprints as before.
swapfn('busSprite',"""function busSprite(){const c=mk(24,52),g=c.getContext('2d');
  for(const ty of [6,37]){R(g,0,ty,2,8,K);R(g,22,ty,2,8,K);R(g,0,ty+2,1,4,'#3a3f55');R(g,23,ty+2,1,4,'#3a3f55');}
  R(g,2,0,20,52,K);R(g,3,1,18,50,'#2f7fd6');R(g,3,1,18,1,'#5aa0e8');
  for(let y=4;y<37;y+=5){R(g,3,y,2,4,'#8fd3ff');R(g,19,y,2,4,'#8fd3ff');R(g,3,y,1,1,'#d8f2ff');R(g,19,y,1,1,'#d8f2ff');}
  R(g,5,2,14,36,PAL.W);R(g,5,2,1,36,'#e3ecf8');R(g,18,2,1,36,'#c6d9f3');for(let y=6;y<36;y+=6)R(g,7,y,10,1,'#e8eff9');
  for(const hy of [9,24]){R(g,8,hy,8,5,K);R(g,9,hy+1,6,3,'#8793a8');R(g,9,hy+1,6,1,'#c6ccd8');R(g,9,hy+3,6,1,'#6a7896');}
  R(g,5,37,14,1,'#c6d9f3');R(g,4,38,16,3,K);R(g,5,39,14,1,'#ffc727');for(let x=6;x<18;x+=3)R(g,x,39,1,1,'#fff08a');
  R(g,3,41,18,5,K);R(g,4,42,16,3,'#8fd3ff');R(g,5,42,4,1,'#d8f2ff');R(g,13,43,1,1,'#d8f2ff');R(g,11,42,1,3,'#5a8fb8');
  R(g,0,40,2,3,K);R(g,22,40,2,3,K);
  R(g,3,46,18,4,'#1d4f9a');R(g,3,47,4,2,'#fff3b0');R(g,17,47,4,2,'#fff3b0');R(g,8,47,8,2,'#2a2a36');R(g,9,47,6,1,'#55607a');
  R(g,2,50,20,2,K);R(g,3,50,18,1,'#8793a8');return c;}""")
swapfn('vanSprite',"""function vanSprite(a){const c=mk(24,42),g=c.getContext('2d'),st=['#e03a4e','#3f86d6','#33b24a','#f07a1a','#9b5fd6','#33b24a'][a%6];
  for(const ty of [5,29]){R(g,0,ty,2,8,K);R(g,22,ty,2,8,K);R(g,0,ty+2,1,4,'#3a3f55');R(g,23,ty+2,1,4,'#3a3f55');}
  R(g,1,0,22,42,K);R(g,2,1,20,40,'#e8ecf2');R(g,2,1,1,40,'#b8c0cc');R(g,21,1,1,40,'#b8c0cc');R(g,3,1,18,1,'#ffffff');
  R(g,3,1,4,2,'#fff3b0');R(g,17,1,4,2,'#fff3b0');R(g,8,1,8,2,'#55607a');R(g,9,1,6,1,'#8793a8');
  R(g,3,4,18,6,K);R(g,4,5,16,4,'#8fd3ff');R(g,5,5,4,1,'#d8f2ff');R(g,15,6,1,1,'#d8f2ff');R(g,7,8,4,1,'#5a8fb8');R(g,13,8,4,1,'#5a8fb8');
  R(g,0,6,2,3,K);R(g,22,6,2,3,K);
  R(g,3,11,18,27,PAL.W);R(g,3,11,18,1,'#c6d9f3');R(g,3,11,1,27,'#e3ecf8');R(g,20,11,1,27,'#dfe9f8');
  R(g,6,13,1,23,'#8793a8');R(g,17,13,1,23,'#8793a8');for(let y=15;y<36;y+=5)R(g,6,y,12,1,'#b8c2d4');
  R(g,2,12,1,26,st);R(g,21,12,1,26,st);R(g,3,24,18,3,st);R(g,3,24,18,1,'rgba(255,255,255,0.35)');
  if(a===5){R(g,3,11,18,27,'#d8364b');R(g,3,11,18,1,'#ff6a7a');R(g,10,11,4,27,'#ffd23f');R(g,3,22,18,4,'#ffd23f');R(g,10,11,1,27,'#fff08a');R(g,3,22,18,1,'#fff08a');
    R(g,7,19,4,3,'#ffd23f');R(g,13,19,4,3,'#ffd23f');R(g,7,19,4,1,K);R(g,13,19,4,1,K);R(g,9,21,6,3,K);R(g,10,22,4,1,'#ffd23f');R(g,2,12,1,26,'#d8364b');R(g,21,12,1,26,'#d8364b');}
  R(g,3,38,18,1,K);R(g,11,38,1,3,K);R(g,3,39,3,2,'#e03a4e');R(g,18,39,3,2,'#e03a4e');R(g,7,40,3,1,'#8793a8');R(g,14,40,3,1,'#8793a8');return c;}""")
swapfn('wagonSprite',"""function wagonSprite(a){const c=mk(24,60),g=c.getContext('2d'),col=['#8a5a34','#2f5fae','#55607a','#2f8a4a','#c8302e'][a%5];
  for(const by of [6,44]){R(g,0,by,24,9,K);R(g,0,by+2,1,5,'#55607a');R(g,23,by+2,1,5,'#55607a');}
  R(g,10,0,4,3,K);R(g,11,0,2,2,'#8793a8');R(g,10,57,4,3,K);R(g,11,58,2,2,'#8793a8');
  R(g,1,2,22,56,K);R(g,2,3,20,54,col);R(g,2,3,20,1,'rgba(255,255,255,0.35)');R(g,2,3,1,54,'rgba(255,255,255,0.18)');R(g,21,3,1,54,'rgba(27,31,59,0.3)');
  for(let y=6;y<56;y+=8){R(g,2,y,2,3,'rgba(27,31,59,0.35)');R(g,20,y,2,3,'rgba(27,31,59,0.35)');R(g,2,y,1,1,'#c6ccd8');R(g,20,y,1,1,'#c6ccd8');}
  R(g,4,5,16,50,K);R(g,5,6,14,48,'#c6d9f3');
  for(let y=6;y<54;y++){const w2=Math.round(5+1.6*Math.sin(y*0.45)+(y%9===0?1:0));R(g,12-w2,y,w2*2,1,PAL.W);R(g,12-w2,y,1,1,'#ffffff');R(g,11+w2,y,1,1,'#dfe9f8');}
  for(let y=9;y<52;y+=7)R(g,9,y,5,1,'#ffffff');R(g,5,6,14,1,'#a6c2ea');return c;}""")
swapfn('trainSprite',"""function trainSprite(len,col){const c=mk(24,len),g=c.getContext('2d');
  for(let y=0;y<len;y+=34){const hh=Math.min(32,len-y),first=y===0,last=y+34>=len;
    R(g,0,y,24,hh,K);R(g,1,y+1,22,hh-2,col);R(g,1,y+1,1,hh-2,'rgba(255,255,255,0.3)');R(g,22,y+1,1,hh-2,'rgba(27,31,59,0.3)');
    for(let yy=y+(first?8:4);yy<y+hh-4;yy+=5){R(g,2,yy,2,3,'#8fd3ff');R(g,20,yy,2,3,'#8fd3ff');R(g,2,yy,1,1,'#d8f2ff');R(g,20,yy,1,1,'#d8f2ff');}
    const ry=y+(first?7:2),rh=hh-(first?9:4);R(g,5,ry,14,rh,'#c6ccd8');R(g,5,ry,1,rh,'#e3e9f2');R(g,18,ry,1,rh,'#8793a8');R(g,6,ry,12,rh,PAL.W);
    for(let yy=ry+4;yy<ry+rh-4;yy+=10){R(g,9,yy,6,4,K);R(g,10,yy+1,4,2,'#8793a8');R(g,10,yy+1,4,1,'#c6ccd8');}
    if(first){R(g,3,1,18,6,K);R(g,4,1,16,2,'#ffd23f');R(g,5,3,14,3,'#8fd3ff');R(g,6,3,4,1,'#d8f2ff');R(g,2,1,3,2,'#fff3b0');R(g,19,1,3,2,'#fff3b0');}
    if(!last&&hh===32){R(g,6,y+32,12,2,K);for(let x=7;x<17;x+=2)R(g,x,y+32,1,2,'#55607a');}
    if(last){R(g,3,y+hh-2,3,1,'#e03a4e');R(g,18,y+hh-2,3,1,'#e03a4e');}}
  return c;}""")
swapfn('tugboatSprite',"""function tugboatSprite(){const c=mk(30,56),g=c.getContext('2d');const hw=y=>Math.round(14*Math.min(1,(y+6)/22));
  for(let y=0;y<56;y++){const h=hw(y);R(g,15-h,y,h*2,1,K);}
  for(let y=1;y<55;y++){const h=hw(y)-1;if(h>0)R(g,15-h,y,h*2,1,'#2a2a36');}
  for(let y=2;y<54;y++){const h=hw(y)-2;if(h>0){R(g,15-h,y,h*2,1,'#e03a4e');R(g,15-h,y,1,1,'#ff6a7a');}}
  for(let y=4;y<52;y++){const h=hw(y)-4;if(h>0)R(g,15-h,y,h*2,1,y%3===0?'#8a5a34':'#b0804a');}
  for(let y=8;y<52;y+=9){R(g,0,y,2,5,K);R(g,28,y,2,5,K);R(g,0,y+1,1,3,'#55607a');R(g,29,y+1,1,3,'#55607a');}
  R(g,13,6,4,3,K);R(g,14,7,2,1,'#8793a8');
  R(g,7,15,16,20,K);R(g,8,16,14,18,'#f4f8ff');R(g,8,16,14,3,'#8fd3ff');R(g,9,16,3,1,'#d8f2ff');R(g,8,19,1,13,'#8fd3ff');R(g,21,19,1,13,'#8fd3ff');
  R(g,9,19,12,14,PAL.W);R(g,9,19,12,1,'#c6d9f3');R(g,14,22,2,2,K);R(g,14,21,2,1,'#ff4a4a');R(g,10,27,10,1,'#dfe9f8');
  R(g,22,27,4,4,K);R(g,23,28,2,2,'#f4f8ff');R(g,22,27,2,2,'#f07a1a');R(g,24,29,2,2,'#f07a1a');
  R(g,11,36,8,7,K);R(g,12,37,6,5,'#ffc727');R(g,12,37,6,1,'#2a2a36');R(g,13,38,4,1,'#fff08a');
  R(g,13,46,4,3,K);R(g,14,47,2,1,'#8793a8');g.fillStyle=K;pixCircle(g,9,48,3);g.fillStyle='#d8b878';pixCircle(g,9,48,2);R(g,9,48,1,1,'#8a5a34');R(g,7,47,1,1,'#f0d8a0');
  return c;}""")
swapfn('parkedTractorSprite',"""function parkedTractorSprite(a){const body=['#d8364b','#33b24a','#3f86d6'][a%3];const c=mk(18,28),g=c.getContext('2d');
  const tyre=(x,y,w,h)=>{R(g,x,y,w,h,K);R(g,x+1,y+1,w-2,h-2,'#2a2a36');for(let yy=y+1;yy<y+h-1;yy+=2)R(g,x+1+((yy>>1)%2),yy,w-3,1,'#55607a');};
  tyre(0,14,6,13);tyre(12,14,6,13);tyre(2,2,4,8);tyre(12,2,4,8);
  R(g,5,0,8,15,K);R(g,6,1,6,13,body);R(g,6,1,6,2,'#55607a');for(let x=6;x<12;x+=2)R(g,x,1,1,2,'#8793a8');R(g,6,3,1,11,'rgba(255,255,255,0.3)');R(g,11,3,1,11,'rgba(27,31,59,0.3)');
  R(g,10,5,2,4,K);R(g,10,4,2,1,PAL.W);
  R(g,0,12,6,3,K);R(g,12,12,6,3,K);R(g,1,13,4,1,body);R(g,13,13,4,1,body);
  R(g,3,13,12,13,K);R(g,4,14,10,11,body);R(g,4,14,10,1,'#8fd3ff');R(g,5,15,8,9,PAL.W);R(g,5,15,8,1,'#ffffff');R(g,5,23,8,1,'#c6d9f3');
  R(g,7,25,4,3,K);R(g,8,26,2,1,'#8793a8');return c;}""")
swapfn('trailerSprite',"""function trailerSprite(){const c=mk(22,40),g=c.getContext('2d');
  R(g,9,3,4,4,K);R(g,10,4,2,2,'#8793a8');R(g,10,0,2,4,K);R(g,9,0,4,2,K);R(g,10,0,2,1,'#c6ccd8');
  for(const ty of [27]){R(g,0,ty,3,10,K);R(g,19,ty,3,10,K);for(let y=ty+1;y<ty+9;y+=2){R(g,1,y,1,1,'#55607a');R(g,20,y,1,1,'#55607a');}}
  R(g,1,6,20,31,K);R(g,2,7,18,29,'#a8673a');for(let x=4;x<19;x+=3)R(g,x,7,1,29,'#8a5434');R(g,2,7,18,1,'#c98d4a');
  for(let y=8;y<34;y+=9)for(let x=3;x<19;x+=8){R(g,x,y,8,8,K);R(g,x+1,y+1,6,6,'#e8c87a');R(g,x+1,y+1,6,1,'#f6e0a0');R(g,x+1,y+6,6,1,'#c9a85a');
    for(let k=0;k<5;k++)R(g,x+1+((k*3+y)%6),y+2+((k*5+x)%4),1,1,'#d8b060');R(g,x+2,y+1,1,6,'#8a5a34');R(g,x+5,y+1,1,6,'#8a5a34');R(g,x+1,y,6,2,PAL.W);R(g,x+2,y-1,4,1,PAL.W);}
  R(g,1,36,20,1,K);R(g,2,36,3,1,'#e03a4e');R(g,17,36,3,1,'#e03a4e');return c;}""")
swapfn('locoSprite',"""function locoSprite(){const c=mk(24,78),g=c.getContext('2d');
  R(g,2,2,5,4,K);R(g,17,2,5,4,K);R(g,3,3,3,2,'#c6ccd8');R(g,18,3,3,2,'#c6ccd8');R(g,1,5,22,4,K);R(g,2,6,20,2,'#c8302e');R(g,2,6,20,1,'#ff6a7a');R(g,11,4,2,3,K);
  for(const wy of [14,30,46]){R(g,0,wy,1,10,K);R(g,23,wy,1,10,K);}
  R(g,1,9,22,62,K);R(g,2,10,20,60,'#55607a');R(g,2,10,1,60,'#8793a8');R(g,21,10,1,60,'#3a3f55');
  R(g,4,9,16,9,K);R(g,5,10,14,7,'#2a2a36');R(g,5,10,14,1,'#55607a');g.fillStyle=K;pixCircle(g,12,13,3);g.fillStyle='#3a3f55';pixCircle(g,12,13,2);R(g,11,12,2,2,'#11131f');R(g,10,10,4,1,'#fff3b0');
  R(g,4,18,16,31,K);R(g,5,18,14,31,'#1f6a44');R(g,9,18,6,31,'#2f8a5a');R(g,11,18,2,31,'#4fae74');R(g,5,18,2,31,'#145146');R(g,17,18,2,31,'#145146');
  for(const by of [22,30,38,46])R(g,5,by,14,1,'#ffc727');
  g.fillStyle=K;pixCircle(g,12,27,3);g.fillStyle='#e8b84a';pixCircle(g,12,27,2);R(g,11,26,1,1,'#fff08a');R(g,11,40,3,3,K);R(g,12,41,1,1,'#e8b84a');
  R(g,3,49,18,21,K);R(g,4,50,16,19,'#1f6a44');R(g,5,50,3,2,'#8fd3ff');R(g,16,50,3,2,'#8fd3ff');R(g,5,53,14,15,PAL.W);R(g,5,53,14,1,'#c6d9f3');R(g,9,58,6,3,'#dfe9f8');
  R(g,2,70,20,8,K);R(g,3,71,18,6,'#8a5a34');R(g,4,71,16,5,'#2a2a36');for(let k=0;k<9;k++)R(g,4+(k*5)%15,71+(k*3)%5,2,1,'#55607a');R(g,6,71,6,2,PAL.W);R(g,13,73,5,2,PAL.W);
  return c;}""")
open(f,'w',encoding='utf-8').write(s)
print('p100 vehicles redraw')
