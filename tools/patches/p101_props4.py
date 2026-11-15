import sys,re
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
# Props audit batch 3 (Nov 16): small street, harbour and park objects. Same sizes and footprints as before.
swapfn('anchorSprite',"""function anchorSprite(){return spr([".....KKK......",".....K.K......",".....KKK......",".KKKKKKKKKKK..",".KLIIIIIIIIK..",".KKKKKKKKKKK..",".....KLK......",".....KIK......",".....KIK......","K....KIK....K.","KK...KIK...KK.","KLK..KIK..KIK.",".KIK.KIK.KIK..","..KIIKIKIIK...","...KKIIIKK....","....KKKKK....."],{I:'#6a7896',L:'#a3adc0'});}""")
swapfn('binsSprite',"""function binsSprite(){const c=mk(18,14),g=c.getContext('2d');for(const [x,col,dk,lt] of [[0,'#2f8a5a','#1f6a44','#4fae74'],[10,'#3f86d6','#2a5fa8','#7fbaf2']]){
    R(g,x,2,8,12,K);R(g,x+1,5,6,7,col);R(g,x+1,5,1,7,lt);R(g,x+6,5,1,7,dk);R(g,x+3,6,1,5,dk);R(g,x+1,2,6,3,dk);R(g,x+1,2,6,1,lt);R(g,x+2,3,4,1,col);R(g,x+3,1,2,1,K);
    R(g,x,12,2,2,K);R(g,x+6,12,2,2,K);R(g,x+3,8,2,2,'#ffffff');R(g,x+3,8,1,1,lt);}return c;}""")
swapfn('bufferSprite',"""function bufferSprite(){const c=mk(24,14),g=c.getContext('2d');R(g,0,4,24,10,K);R(g,1,5,22,8,'#ffc727');for(let x=-6;x<24;x+=6)for(let r=0;r<8;r++){const xx=x+r;if(xx>=1&&xx<23)R(g,xx,5+r,3,1,'#2a2a36');}R(g,1,5,22,1,'#fff08a');R(g,1,12,22,1,'#c98a12');
  for(const bx of [1,17]){R(g,bx,6,6,6,K);g.fillStyle=K;pixCircle(g,bx+3,3,3);g.fillStyle='#8793a8';pixCircle(g,bx+3,3,2);R(g,bx+2,2,2,1,'#c6ccd8');}R(g,10,0,4,4,K);R(g,11,1,2,2,'#ff4a4a');R(g,11,1,1,1,'#ffb0b0');return c;}""")
swapfn('clockSprite',"""function clockSprite(){const c=mk(12,34),g=c.getContext('2d');R(g,4,11,4,20,K);R(g,5,11,2,20,'#2f5f4a');R(g,5,11,1,20,'#4f8f6a');R(g,3,16,6,2,K);R(g,4,16,4,1,'#2f5f4a');
  R(g,2,29,8,5,K);R(g,3,30,6,3,'#2f5f4a');R(g,3,30,6,1,'#4f8f6a');R(g,5,0,2,2,K);R(g,5,0,2,1,'#ffd23f');
  g.fillStyle=K;pixCircle(g,6,6,5);g.fillStyle='#e8b84a';pixCircle(g,6,6,4);g.fillStyle='#fbf6e8';pixCircle(g,6,6,3);R(g,6,4,1,3,K);R(g,6,6,2,1,K);R(g,4,4,1,1,'#ffffff');return c;}""")
swapfn('fishboxSprite',"""function fishboxSprite(){const c=mk(14,10),g=c.getContext('2d');R(g,0,0,14,10,K);R(g,1,1,12,8,'#3f86d6');R(g,1,1,12,1,'#7fbaf2');R(g,2,2,10,6,'#dff0fb');R(g,0,3,1,2,'#2a5fa8');R(g,13,3,1,2,'#2a5fa8');
  for(const [x,y,d] of [[3,3,1],[6,5,-1]]){R(g,x,y,5,2,K);R(g,x,y,5,1,'#a3b8cc');R(g,x+1,y,3,1,'#d6e2ee');R(g,d>0?x+5:x-1,y,1,2,'#6a7896');R(g,d>0?x+1:x+3,y,1,1,K);}
  R(g,2,7,10,1,'#bfe0f5');return c;}""")
swapfn('gatePillarSprite',"""function gatePillarSprite(){const c=mk(12,40),g=c.getContext('2d');R(g,1,6,10,28,K);R(g,2,7,8,26,'#b8433f');
  for(let y=8;y<33;y+=3){R(g,2,y,8,1,'#8e2f2c');for(let x=2+((y/3|0)%2)*2;x<10;x+=4)R(g,x,y+1,1,2,'#8e2f2c');}R(g,2,7,1,26,'#d0645a');
  R(g,0,4,12,4,K);R(g,1,5,10,2,'#d6cfc0');R(g,1,5,10,1,'#f1ece0');g.fillStyle=K;pixCircle(g,6,2,2);g.fillStyle='#d6cfc0';R(g,5,1,2,2,'#d6cfc0');R(g,5,1,1,1,'#f1ece0');
  R(g,0,33,12,7,K);R(g,1,34,10,5,'#c6bda8');R(g,1,34,10,1,'#e3dccb');R(g,1,38,10,1,'#a89f88');return c;}""")
swapfn('haySprite',"""function haySprite(){const c=mk(12,8),g=c.getContext('2d');R(g,0,0,12,8,K);R(g,1,1,10,6,'#e8c87a');R(g,1,1,10,1,'#f6e0a0');R(g,1,6,10,1,'#c9a85a');
  for(const [x,y] of [[2,3],[5,2],[8,4],[3,5],[9,2],[6,4]])R(g,x,y,1,1,'#d8b060');R(g,3,1,1,6,'#8a5a34');R(g,8,1,1,6,'#8a5a34');R(g,1,1,10,1,PAL.W);return c;}""")
swapfn('iceBlockSprite',"""function iceBlockSprite(w,h){const c=mk(w,h),g=c.getContext('2d');const t=Math.max(3,Math.round(h*0.35));
  R(g,0,0,w,h,K);R(g,1,1,w-2,t-1,'#d4f0ff');R(g,1,t,w-2,h-t-1,'#8fcbf0');R(g,1,t,w-2,1,'#ffffff');R(g,1,1,w-2,1,'#ffffff');
  R(g,w-3,t+1,1,h-t-3,'#6fb0de');R(g,2,t+1,1,h-t-3,'#bfe6ff');R(g,Math.round(w*0.35),t+2,1,Math.max(1,h-t-5),'#bfe6ff');R(g,Math.round(w*0.35)+1,t+2+Math.max(1,h-t-5)-1,2,1,'#bfe6ff');
  R(g,3,2,2,1,'#ffffff');R(g,w-5,h-3,1,1,'#ffffff');return c;}""")
swapfn('lampSprite',"""function lampSprite(){const c=mk(7,28),g=c.getContext('2d');R(g,2,5,3,21,K);R(g,3,6,1,20,'#55607a');R(g,3,6,1,8,'#8793a8');R(g,1,24,5,4,K);R(g,2,25,3,2,'#55607a');
  R(g,0,1,7,6,K);R(g,1,2,5,3,'#ffef7a');R(g,1,2,5,1,'#fff8c0');R(g,2,0,3,2,K);R(g,0,5,7,1,K);R(g,1,5,5,1,'#55607a');return c;}""")
swapfn('lantPostSprite',"""function lantPostSprite(){const c=mk(10,30),g=c.getContext('2d');R(g,4,10,3,18,K);R(g,5,10,1,18,'#3a3f55');R(g,5,10,1,6,'#6a7896');R(g,2,26,7,4,K);R(g,3,27,5,2,'#3a3f55');R(g,3,27,5,1,'#6a7896');
  R(g,2,1,7,2,K);R(g,1,3,9,1,K);R(g,4,0,3,1,K);R(g,2,4,7,7,K);R(g,3,4,5,5,'#ffe27a');R(g,3,4,5,1,'#fff8c0');R(g,5,4,1,5,'#c98a12');R(g,3,9,5,1,'#3a3f55');R(g,3,1,5,1,PAL.W);return c;}""")
s,n=re.subn(r'SPR\.mailbox=spr\(\[[^\]]*\]\);',"""SPR.mailbox=(()=>{const c=mk(9,14),g=c.getContext('2d');R(g,3,8,3,6,K);R(g,4,8,1,6,'#8a5a34');R(g,2,12,5,2,K);
  R(g,0,2,9,7,K);R(g,1,3,7,5,'#d8364b');R(g,1,3,7,1,'#ff6a7a');R(g,2,2,5,1,K);R(g,1,7,7,1,'#a8283d');R(g,7,4,1,3,'#f4f8ff');R(g,1,4,1,3,'#ff9aa8');
  R(g,8,0,1,5,K);R(g,7,0,1,2,K);R(g,7,0,1,1,'#ffd23f');R(g,3,4,3,1,'#f4f8ff');return c;})();""",s);assert n==1
swapfn('postboxSprite',"""function postboxSprite(){const c=mk(8,14),g=c.getContext('2d');R(g,1,0,6,2,K);R(g,0,2,8,12,K);R(g,1,1,6,2,'#e03a4e');R(g,2,1,2,1,'#ff9aa8');R(g,1,3,6,1,K);
  R(g,1,4,6,8,'#d8364b');R(g,1,4,1,8,'#ff6a7a');R(g,6,4,1,8,'#a8283d');R(g,2,5,4,1,K);R(g,3,7,2,2,'#f4f8ff');R(g,3,8,2,1,'#c6d9f3');R(g,0,12,8,2,K);R(g,1,12,6,1,'#3a3f55');return c;}""")
swapfn('potsSprite',"""function potsSprite(){const c=mk(20,16),g=c.getContext('2d');
  const pot=(x,y)=>{R(g,x,y+2,10,8,K);R(g,x+1,y,8,3,K);R(g,x+1,y+3,8,6,'#5a4a3a');for(let i=x+1;i<x+9;i+=2)R(g,i,y+1,1,8,'#c9a26a');for(let j=y+4;j<y+9;j+=2)R(g,x+1,j,8,1,'#a8834f');R(g,x+2,y+1,6,1,'#e0c08a');R(g,x+1,y+9,8,1,'#2a2a36');};
  pot(0,6);pot(10,6);pot(5,0);R(g,17,3,3,4,K);R(g,18,4,1,2,'#f07a1a');R(g,15,5,3,1,'#d8b878');return c;}""")
swapfn('palletSprite',"""function palletSprite(){const c=mk(20,14),g=c.getContext('2d');R(g,0,4,20,10,K);R(g,1,5,18,8,'#5a3a20');
  for(let x=1;x<19;x+=4){R(g,x,5,3,8,'#c98d4a');R(g,x,5,3,1,'#e0b070');R(g,x+2,6,1,7,'#a8673a');}R(g,1,11,18,2,'#a8673a');R(g,1,11,18,1,'#c98d4a');R(g,0,8,1,3,'#3a2a1a');R(g,19,8,1,3,'#3a2a1a');
  R(g,2,1,16,4,K);R(g,3,1,14,3,PAL.W);R(g,4,0,12,1,K);R(g,4,1,12,1,'#ffffff');return c;}""")
swapfn('signpostSprite',"""function signpostSprite(a){const c=mk(16,26),g=c.getContext('2d');R(g,7,4,3,22,K);R(g,8,5,1,20,'#a8673a');R(g,8,5,1,8,'#c98d4a');R(g,6,24,5,2,K);R(g,7,3,3,2,K);R(g,8,2,1,1,K);
  const arr=(x,y,w,right,col)=>{R(g,x,y,w,5,K);R(g,x+1,y+1,w-2,3,col);if(right){R(g,x+w,y+1,1,3,K);R(g,x+w-1,y+1,1,3,col);R(g,x+w+1,y+2,1,1,K);R(g,x+w,y+2,1,1,col);}else{R(g,x-1,y+1,1,3,K);R(g,x,y+1,1,3,col);R(g,x-2,y+2,1,1,K);R(g,x-1,y+2,1,1,col);}
    for(let k=x+2;k<x+w-2;k+=2)R(g,k,y+2,1,1,'#f4f8ff');R(g,x+1,y+1,w-2,1,'rgba(255,255,255,0.3)');};
  arr(1,5,13,true,'#2f8a5a');arr(3,11,12,false,'#2f5fae');return c;}""")
swapfn('skipSprite',"""function skipSprite(){const c=mk(26,16),g=c.getContext('2d');R(g,0,4,26,12,K);R(g,1,5,24,10,'#ffc727');R(g,1,5,24,1,'#fff08a');R(g,2,6,22,3,'#c98a12');R(g,3,8,20,5,'#5a4a3a');
  for(const [x,y,w,col] of [[4,9,4,'#b8433f'],[9,8,5,'#a8673a'],[15,9,3,'#8793a8'],[19,8,3,'#b8433f'],[6,11,3,'#8793a8'],[12,11,4,'#c98d4a'],[18,11,3,'#6a7896']]){R(g,x,y,w,2,col);R(g,x,y,w,1,'rgba(255,255,255,0.3)');}
  R(g,1,13,24,2,'#e29a1c');R(g,0,6,1,3,'#55607a');R(g,25,6,1,3,'#55607a');R(g,4,4,18,2,PAL.W);R(g,6,3,6,1,PAL.W);return c;}""")
swapfn('warnSignSprite',"""function warnSignSprite(){const c=mk(14,20),g=c.getContext('2d');R(g,6,10,2,10,K);R(g,7,10,1,9,'#8793a8');R(g,5,18,4,2,K);
  for(let r=0;r<11;r++){const h=Math.floor(r*0.62);R(g,7-h-1,r,h*2+2,1,K);}for(let r=2;r<10;r++){const h=Math.floor(r*0.62)-1;if(h>=0)R(g,7-h-1+1,r,h*2,1,'#e03a4e');}
  for(let r=4;r<9;r++){const h=Math.floor(r*0.62)-2;if(h>=0)R(g,7-h,r,h*2,1,'#f4f8ff');}R(g,6,4,2,1,'#e03a4e');R(g,7,4,0,0,K);R(g,6,5,1,2,K);R(g,7,5,1,2,K);R(g,6,8,2,1,K);return c;}""")
swapfn('tubSprite',"""function tubSprite(){const c=mk(16,16),g=c.getContext('2d');R(g,1,0,14,16,K);R(g,0,1,16,14,K);R(g,1,1,14,14,'#a8673a');for(let x=2;x<15;x+=3)R(g,x,1,1,14,'#8a5434');R(g,1,1,14,1,'#c98d4a');
  R(g,3,3,10,10,K);R(g,4,4,8,8,'#3fb8d8');R(g,4,4,8,2,'#7fe0f2');for(const [x,y] of [[5,7],[9,8],[7,10],[10,5]])R(g,x,y,1,1,'#d8f8ff');
  for(const [x,y] of [[5,-1],[9,-2]]){R(g,x,y+2,1,2,'rgba(255,255,255,0.7)');R(g,x+1,y+1,1,2,'rgba(255,255,255,0.5)');}return c;}""")
swapfn('swanSprite',"""function swanSprite(){const c=mk(18,24),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,9,15,8);g.fillStyle='#f4f8ff';pixCircle(g,9,15,7);
  R(g,4,11,10,8,'#3f86d6');R(g,4,11,10,1,'#7fbaf2');R(g,5,13,8,1,'#2a5fa8');R(g,5,16,8,1,'#2a5fa8');R(g,2,13,2,5,'#dfe9f8');R(g,14,13,2,5,'#dfe9f8');for(const y of [14,16])R(g,1,y,2,1,'#c6d9f3'),R(g,15,y,2,1,'#c6d9f3');
  R(g,7,1,4,10,K);R(g,8,2,2,9,'#ffffff');R(g,9,2,1,9,'#dfe9f8');R(g,6,0,5,4,K);R(g,7,1,3,2,'#ffffff');R(g,10,1,2,2,K);R(g,11,1,2,1,'#f07a1a');R(g,10,2,3,1,'#e29a1c');R(g,8,1,1,1,K);
  R(g,6,22,6,1,'#c6d9f3');return c;}""")
open(f,'w',encoding='utf-8').write(s)
print('p101 small props redraw')
