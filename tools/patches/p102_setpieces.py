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
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:70],s.count(a));s=s.replace(a,b_)
# Props audit batch 4 (Nov 16): set pieces. Same sizes and footprints as before.
rep("function climbSprite(","""function pxPoly(g,pts,col){let y0=1e9,y1=-1e9;for(const p of pts){y0=Math.min(y0,p[1]);y1=Math.max(y1,p[1]);}for(let y=Math.floor(y0);y<=Math.ceil(y1);y++){const yc=y+0.5,xs=[];for(let i=0;i<pts.length;i++){const a=pts[i],c2=pts[(i+1)%pts.length];if((a[1]<=yc&&c2[1]>yc)||(c2[1]<=yc&&a[1]>yc))xs.push(a[0]+(yc-a[1])*(c2[0]-a[0])/(c2[1]-a[1]));}xs.sort((p,q)=>p-q);for(let k=0;k+1<xs.length;k+=2){const xa=Math.round(xs[k]),xb=Math.round(xs[k+1]);if(xb>xa)R(g,xa,y,xb-xa,1,col);}}}
function pxPolyO(g,pts,col){for(const [dx,dy] of [[-1,0],[1,0],[0,-1],[0,1]])pxPoly(g,pts.map(p=>[p[0]+dx,p[1]+dy]),K);pxPoly(g,pts,col);}
function climbSprite(""")
swapfn('climbSprite',"""function climbSprite(){const c=mk(24,22),g=c.getContext('2d');
  for(const x of [0,11,21]){R(g,x,2,3,20,K);R(g,x+1,2,1,19,'#c98d4a');}R(g,0,0,24,4,K);R(g,1,1,22,2,'#a8673a');R(g,1,1,22,1,'#c98d4a');R(g,1,0,22,1,PAL.W);
  for(let y=6;y<20;y+=4){R(g,2,y,10,2,K);R(g,3,y,8,1,'#3f86d6');R(g,3,y,8,1,'#7fbaf2');}
  for(let y=4;y<21;y++)for(let x=14;x<21;x++)if(((x+y)%4===0)||((x-y+40)%4===0))R(g,x,y,1,1,'#d8b878');
  R(g,0,20,24,2,K);R(g,1,20,22,1,'#8a5a34');return c;}""")
swapfn('fountainSprite',"""function fountainSprite(){const c=mk(26,26),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,13,13,12);g.fillStyle='#8793a8';pixCircle(g,13,13,11);g.fillStyle='#c6ccd8';pixCircle(g,12,12,10);g.fillStyle='#e3e9f2';pixCircle(g,11,11,9);
  g.fillStyle=K;pixCircle(g,13,13,9);g.fillStyle='#8fcff0';pixCircle(g,13,13,8);g.fillStyle='#bfe6ff';pixCircle(g,12,12,6);R(g,6,15,4,1,'#d8f2ff');R(g,16,8,3,1,'#d8f2ff');R(g,8,9,1,3,'#d8f2ff');R(g,17,16,2,1,'#6fb0de');
  g.fillStyle=K;pixCircle(g,13,13,4);g.fillStyle='#c6ccd8';pixCircle(g,13,13,3);g.fillStyle='#bfe6ff';pixCircle(g,13,13,2);R(g,12,11,2,4,K);R(g,12,10,2,1,'#e3e9f2');R(g,13,12,1,2,'#8793a8');
  for(const [x,y] of [[13,7],[19,13],[13,19],[7,13]])R(g,x,y,1,1,'#ffffff');R(g,4,6,4,2,PAL.W);R(g,18,19,4,2,PAL.W);R(g,19,4,3,1,PAL.W);return c;}""")
swapfn('icebergSprite',"""function icebergSprite(a){const c=mk(44,34),g=c.getContext('2d');R(g,1,29,42,5,K);R(g,2,30,40,3,'#3f6fa0');for(let x=4;x<40;x+=6)R(g,x,31,3,1,'#6f9fd0');
  const body=[[3,30],[7,19],[13,13],[19,3],[25,9],[31,5],[37,15],[41,30]];pxPolyO(g,body,'#9fd0f0');
  pxPoly(g,[[13,13],[19,3],[21,17],[11,25],[7,19]],'#e3f4ff');pxPoly(g,[[19,3],[25,9],[23,20],[21,17]],'#cfeafd');pxPoly(g,[[25,9],[31,5],[30,21],[23,20]],'#e3f4ff');
  pxPoly(g,[[31,5],[37,15],[41,30],[30,30],[30,21]],'#7ab8e6');pxPoly(g,[[3,30],[7,19],[11,25],[13,30]],'#b8e0f8');
  R(g,18,4,3,2,'#ffffff');R(g,30,6,3,2,'#ffffff');R(g,16,9,1,5,'#ffffff');R(g,27,11,1,4,'#ffffff');R(g,34,18,1,6,'#6aa6d8');R(g,4,28,36,1,'#d8f2ff');return c;}""")
swapfn('spireSprite',"""function spireSprite(){const c=mk(16,34),g=c.getContext('2d');for(let y=0;y<30;y++){const hw=Math.round(y*0.24)+1;R(g,8-hw-1,y,hw*2+2,1,K);R(g,8-hw,y,hw,1,'#d4f0ff');R(g,8,y,hw,1,'#8fc8f0');R(g,8,y,1,1,'#bfe6ff');}
  for(const y of [9,16,23])R(g,8-Math.round(y*0.24),y,Math.round(y*0.24)*2+1,1,'rgba(255,255,255,0.35)');R(g,7,2,1,12,'#ffffff');R(g,8,0,1,1,'#ffffff');
  R(g,0,29,16,5,K);R(g,1,29,14,4,PAL.W);R(g,1,32,14,1,'#c6d9f3');R(g,3,28,10,2,PAL.W);return c;}""")
swapfn('startHutSprite',"""function startHutSprite(){const c=mk(60,40),g=c.getContext('2d');
  R(g,0,3,60,9,K);R(g,1,4,58,7,'#6b3f22');for(let x=3;x<58;x+=5)R(g,x,6,1,5,'#55321d');R(g,1,3,58,3,PAL.W);for(let x=2;x<58;x+=7)R(g,x,6,3,1,PAL.W);R(g,1,10,58,1,'#55321d');
  for(const [px,fc] of [[3,'#3f86d6'],[55,'#d8364b']]){R(g,px,0,2,6,K);R(g,px===3?5:50,0,5,3,K);R(g,px===3?5:51,0,4,2,fc);}
  R(g,1,11,58,29,K);R(g,2,12,56,27,'#e03a4e');for(let x=4;x<58;x+=4)R(g,x,12,1,27,'#c8302e');R(g,2,12,56,1,'#ff6a7a');icicles(g,2,12,56,7,3);
  R(g,6,14,48,10,K);R(g,7,15,46,8,'#13306b');sprText(g,'START',30-sprTextW('START')/2|0,17,'#ffd23f');
  R(g,5,26,13,9,K);R(g,6,27,11,7,'#8fd3ff');R(g,7,27,4,1,'#d8f2ff');R(g,11,27,1,7,'#f4f8ff');R(g,5,34,13,1,PAL.W);
  R(g,42,26,13,9,K);R(g,43,27,11,7,'#11131f');for(const [x,y] of [[44,29],[48,29],[51,29]])R(g,x,y,2,3,'#ff4a4a');R(g,47,30,1,1,'#ff4a4a');R(g,42,34,13,1,PAL.W);
  R(g,22,26,16,14,K);R(g,23,27,14,13,'#2a2a36');R(g,23,33,14,2,'#f4f8ff');for(let x=23;x<37;x+=4)R(g,x,33,2,2,'#d8364b');R(g,22,26,16,1,'#ffd23f');
  drift(g,0,39,6,3);drift(g,47,39,6,3);return c;}""")
swapfn('slideSprite',"""function slideSprite(){const c=mk(12,26),g=c.getContext('2d');R(g,0,0,12,9,K);R(g,1,1,10,3,'#d8364b');R(g,1,1,10,1,'#ff6a7a');R(g,1,4,10,4,'#c98d4a');for(let x=2;x<10;x+=2)R(g,x,4,1,4,'#a8673a');
  R(g,1,0,10,2,PAL.W);R(g,2,9,8,17,K);R(g,3,9,6,16,'#ffc727');R(g,3,9,1,16,'#e29a1c');R(g,8,9,1,16,'#e29a1c');R(g,5,9,2,16,'#fff08a');R(g,3,9,6,3,PAL.W);R(g,4,12,4,1,'#dfe9f8');R(g,2,24,8,2,K);R(g,3,24,6,1,'#e29a1c');return c;}""")
swapfn('mastSprite',"""function mastSprite(){const c=mk(18,70),g=c.getContext('2d');
  for(let y=2;y<64;y++){const hw=1+Math.round((y-2)*0.105),red=((y/10)|0)%2===0,col=red?'#d8364b':'#f4f8ff',ln=red?'#a8283d':'#a3adc0';R(g,9-hw-1,y,hw*2+3,1,K);R(g,9-hw,y,hw*2+1,1,col);
    if(y%6===2)R(g,9-hw,y,hw*2+1,1,ln);else{const t=(y%6)/6,xa=Math.round(9-hw+t*(hw*2)),xb=Math.round(9+hw-t*(hw*2));R(g,xa,y,1,1,ln);R(g,xb,y,1,1,ln);}R(g,9-hw,y,1,1,red?'#ff6a7a':'#ffffff');}
  R(g,8,0,2,3,K);R(g,8,0,2,1,'#ff4a4a');for(const [x,y] of [[1,18],[12,30]]){g.fillStyle=K;pixCircle(g,x+2,y+2,3);g.fillStyle='#c6ccd8';pixCircle(g,x+2,y+2,2);R(g,x+1,y+1,1,1,'#ffffff');}
  R(g,0,63,18,7,K);R(g,1,64,16,5,'#8793a8');R(g,1,64,16,1,'#c6ccd8');R(g,3,66,12,1,'#6a7896');return c;}""")
swapfn('rampSprite',"""function rampSprite(){const c=mk(40,24),g=c.getContext('2d');R(g,0,0,40,24,K);R(g,1,1,38,3,'#ffffff');R(g,1,3,38,1,'#d8364b');
  for(let y=4;y<21;y++)R(g,4,y,32,1,y%2?'#eef4fc':'#dfe9f8');R(g,4,4,32,1,'#ffffff');for(const x of [1,36]){R(g,x,4,3,17,'#a8673a');for(let y=6;y<20;y+=4)R(g,x,y,3,1,'#8a5434');R(g,x,4,3,1,'#c98d4a');}
  R(g,1,21,38,2,'#9fc0e8');R(g,12,8,1,10,'#c6d9f3');R(g,27,8,1,10,'#c6d9f3');return c;}""")
swapfn('solarSprite',"""function solarSprite(){const c=mk(30,16),g=c.getContext('2d');R(g,6,11,2,5,K);R(g,22,11,2,5,K);R(g,6,11,1,4,'#8793a8');R(g,22,11,1,4,'#8793a8');
  R(g,0,0,30,12,K);R(g,1,1,28,10,'#c6ccd8');R(g,2,2,26,8,'#1f3f8a');for(let x=2;x<28;x+=5)R(g,x,2,1,8,'#3f6fc8');R(g,2,5,26,1,'#3f6fc8');for(let k=0;k<6;k++)R(g,12+k,2+k,2,1,'rgba(200,230,255,0.55)');R(g,1,0,28,2,PAL.W);return c;}""")
swapfn('dropSprite',"""function dropSprite(){const c=mk(22,92),g=c.getContext('2d');R(g,7,0,8,92,K);R(g,8,0,6,91,'#c6d0e0');R(g,8,0,1,91,'#e3e9f2');R(g,13,0,1,91,'#8793a8');for(let y=3;y<86;y+=6){R(g,9,y,4,1,'#8793a8');R(g,9,y+3,1,1,'#8793a8');R(g,12,y+3,1,1,'#8793a8');}
  R(g,1,29,20,12,K);R(g,2,30,18,10,'#d8364b');R(g,2,30,18,1,'#ff6a7a');for(let x=3;x<19;x+=4){R(g,x,32,3,5,'#ffc727');R(g,x,32,3,1,'#fff08a');R(g,x+1,37,1,3,'#3f86d6');}
  R(g,5,0,12,5,K);R(g,6,1,10,3,'#ffc727');for(let x=6;x<16;x+=3)R(g,x,2,1,1,'#ffffff');R(g,0,84,22,8,K);R(g,1,85,20,6,'#8793a8');R(g,1,85,20,1,'#c6ccd8');return c;}""")
# warehouse: the sign was narrower than "WAREHOUSE", so the word wrapped onto two lines
rep("R(g,dx-2,h-42,dw+4,9,K);R(g,dx-1,h-41,dw+2,7,'#13306b');fitText(g,nm,w>>1,h-40,dw,'#ffd23f',null);",
    "const sw=Math.min(w-4,Math.max(dw+4,textW(nm)+6)),sx=(w-sw)>>1;R(g,sx,h-42,sw,9,K);R(g,sx+1,h-41,sw-2,7,'#13306b');fitText(g,nm,w>>1,h-40,sw-4,'#ffd23f',null);")
open(f,'w',encoding='utf-8').write(s)
print('p102 set pieces redraw')
