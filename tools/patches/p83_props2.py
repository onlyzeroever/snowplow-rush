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
# Props art pass, batch 2 (Nov 16): reeds, golf flags, hurdles, water trough, stone lions, grain silo, kettle BBQ,
# drinks urn, car-park pillar, lift pylon, fishing nets and marker poles. Sizes and footprints unchanged.
swapfn('reedSprite',"""function reedSprite(){return spr([".K.K.","KTKTK","KTKTK",".gKg.",".KgK."],{T:'#7a4a2a',g:'#7aa35c'});}""")
swapfn('holeSprite',"""function holeSprite(a){const i=a%3,col=['#e03a4e','#ffc727','#3f86d6'][i],sh=['#a82639','#d49a12','#2a5fa8'][i],hi=['#f28b8b','#ffe27a','#7ab4f0'][i];const c=mk(10,16),g=c.getContext('2d');
  R(g,1,0,3,13,K);R(g,2,1,1,12,'#f4f8ff');R(g,3,1,7,5,K);R(g,3,2,6,3,col);R(g,3,2,6,1,hi);R(g,3,4,6,1,sh);R(g,8,2,1,1,K);R(g,8,4,1,1,K);
  g.fillStyle=K;pixCircle(g,3,13,2);R(g,2,13,3,1,'#2a2a36');R(g,1,14,1,1,'#c6d9f3');return c;}""")
swapfn('hurdleSprite',"""function hurdleSprite(){return spr(["KKK..........KKK","KWK..........KWK","KWKKKKKKKKKKKKWK","KWKRRWWRRWWRRKWK","KWKrrwwrrwwrrKWK","KWKKKKKKKKKKKKWK","KwK..........KwK","KKKK........KKKK"],{r:'#a82639',w:'#c6d9f3'});}""")
swapfn('troughSprite',"""function troughSprite(){const c=mk(24,8),g=c.getContext('2d');R(g,0,0,24,7,K);R(g,1,1,22,5,'#8a5a34');R(g,1,1,22,1,'#c98d4a');R(g,2,2,20,2,'#9fd4f4');R(g,3,2,5,1,'#ffffff');R(g,13,3,4,1,'#d6f0ff');R(g,2,3,1,1,'#7ab4e0');
  R(g,1,4,22,1,'#a8743f');R(g,1,5,22,1,'#6b4426');R(g,5,4,1,2,'#55607a');R(g,18,4,1,2,'#55607a');R(g,2,7,2,1,K);R(g,20,7,2,1,K);return c;}""")
swapfn('lionSprite',"""function lionSprite(f){const c=mk(14,18),g=c.getContext('2d'),cx=f?6:7;
  R(g,0,12,14,6,K);R(g,1,13,12,4,'#c6c0b0');R(g,1,13,12,1,'#e2ddd0');R(g,1,16,12,1,'#9a9484');R(g,10,14,2,2,'#a8a292');
  R(g,2,10,4,3,K);R(g,3,10,2,2,'#c6cdd9');R(g,8,10,4,3,K);R(g,9,10,2,2,'#a3adc0');
  g.fillStyle=K;pixCircle(g,cx,5,5);for(let y=0;y<11;y++)for(let x=0;x<14;x++){const dx=x-cx,dy=y-5,d=Math.sqrt(dx*dx+dy*dy);if(d<=4.3){let col=(dx+dy)<-1?'#a3adc0':(dx+dy)>2?'#7d8599':'#8f98ad';if(d>3&&((x*3+y*5)%7===0))col='#6f788c';R(g,x,y,1,1,col);}}
  g.fillStyle='#c6cdd9';pixCircle(g,cx,5,2);R(g,cx-2,4,1,2,'#c6cdd9');R(g,cx+2,4,1,2,'#b8c0cf');R(g,cx-1,4,1,1,K);R(g,cx+1,4,1,1,K);R(g,cx,6,1,1,'#55607a');R(g,cx-1,7,3,1,'#d6dee9');R(g,cx-1,3,1,1,'#e3ebf6');return c;}""")
swapfn('siloSprite',"""function siloSprite(){const c=mk(23,23),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,11,11,11);const T=['#e3ebf6','#c6d0e0','#a3adc0','#8793a8'];
  for(let y=0;y<23;y++)for(let x=0;x<23;x++){const dx=x-11,dy=y-11,d=Math.sqrt(dx*dx+dy*dy);if(d<=10.4){const l=-(dx+dy)/Math.max(1,d);let col=T[l>0.5?0:l>-0.1?1:l>-0.6?2:3];const a=Math.atan2(dy,dx)/(Math.PI/8);if(d>3.5&&Math.abs(a-Math.round(a))<0.08)col='#6a7896';if(d>9.5)col='#6a7896';R(g,x,y,1,1,col);}}
  g.fillStyle=K;pixCircle(g,11,11,3);g.fillStyle='#8793a8';pixCircle(g,11,11,2);R(g,10,10,1,1,'#d6dee9');R(g,12,12,1,1,'#55607a');return c;}""")
swapfn('bbqSprite',"""function bbqSprite(){return spr(["....KKKK....","..KKcUUXKK..",".KcUUUUUUXK.","KcUUUUUUUUXK","KKKKKKKKKKKK","KOOOYYOOOOoK","KcUUUUUUUUXK",".KcUUUUUUXK.","..KKKKKKKK..","..K..KK..K..",".K...KK...K.","KK..KKKK..KK"],{c:'#6a7286',U:'#3a3f55',X:'#1f2233',O:'#f07a1a',Y:'#ffd23f',o:'#b8501a'});}""")
swapfn('urnSprite',"""function urnSprite(){const c=mk(16,18),g=c.getContext('2d');for(const [x,y,k] of [[7,6,1],[6,5,0],[6,4,1],[7,3,0],[8,2,1],[8,1,0],[10,5,0],[11,4,1],[11,3,0],[10,2,1],[10,1,0]])R(g,x,y,1,1,k?'#e3ebf6':'#c6d0dc');
  R(g,1,7,14,3,K);R(g,2,8,12,1,'#7a2a35');R(g,3,8,3,1,'#a8434f');R(g,2,9,12,1,'#e0a060');R(g,2,9,12,7,K);R(g,3,10,10,5,'#b8743a');R(g,3,10,10,1,'#e0a060');R(g,4,11,2,3,'#e0a060');R(g,11,11,2,4,'#7a4a2a');R(g,3,13,10,1,'#8a5a2c');
  R(g,0,10,2,3,K);R(g,0,11,1,1,'#b8743a');R(g,14,10,2,3,K);R(g,15,11,1,1,'#7a4a2a');R(g,3,15,3,3,K);R(g,10,15,3,3,K);R(g,4,16,1,1,'#55607a');R(g,11,16,1,1,'#55607a');return c;}""")
swapfn('pillarSprite',"""function pillarSprite(){const c=mk(10,16),g=c.getContext('2d');R(g,0,0,10,16,K);R(g,1,1,8,14,'#a8aeba');R(g,1,1,2,14,'#c6ccd6');R(g,7,1,2,14,'#8a90a0');R(g,1,1,8,1,'#d6dee9');
  for(let y=10;y<14;y++)for(let x=1;x<9;x++)R(g,x,y,1,1,((x+y)%4<2)?'#ffc727':'#2a2a36');R(g,1,14,8,1,'#6a7080');return c;}""")
swapfn('pylonSprite',"""function pylonSprite(){const c=mk(14,46),g=c.getContext('2d');const leg=y=>{const hw=Math.round(1.5+3.5*(y-5)/38);return [6-hw,7+hw];};
  for(let y=5;y<43;y++){const [a,b]=leg(y);R(g,a,y,1,1,K);R(g,b,y,1,1,K);R(g,a+1,y,1,1,'#8793a8');R(g,b-1,y,1,1,'#55607a');}
  for(let y0=8;y0<40;y0+=7){const [a0,b0]=leg(y0);R(g,a0,y0,b0-a0+1,1,K);for(let k=1;k<7;k++){const y=y0+k,[a,b]=leg(y),x=Math.round(a+(b-a)*k/7);R(g,x,y,1,1,'#3a3f55');}}
  R(g,0,1,14,4,K);R(g,1,2,12,2,'#8793a8');R(g,1,2,12,1,'#c6d0e0');for(const x of [1,10]){R(g,x,5,3,3,K);R(g,x+1,6,1,1,'#ffc727');}
  R(g,1,42,12,4,K);R(g,2,43,10,2,'#9aa1b5');R(g,2,43,10,1,'#c6d0e0');return c;}""")
swapfn('netsSprite',"""function netsSprite(){const c=mk(22,12),g=c.getContext('2d');const sp=[[5,16],[3,18],[2,19],[1,20],[1,20],[1,20],[1,20],[1,20],[1,20],[1,20]];
  for(let i=0;i<10;i++){const y=2+i,[x0,x1]=sp[i];R(g,x0,y,x1-x0+1,1,K);if(i>0&&i<9)for(let x=x0+1;x<x1;x++){let col=((x+y)%3===0||(x-y+30)%3===0)?'#1d6650':'#2f8a6a';if(i<3&&x<x0+5)col=col==='#2f8a6a'?'#4fae8a':col;R(g,x,y,1,1,col);}}
  const fl=(x,y,col)=>{R(g,x,y+1,4,2,K);R(g,x+1,y,2,4,K);R(g,x+1,y+1,2,2,col);R(g,x+1,y+1,1,1,'#ffffff');};fl(4,0,'#e03a4e');fl(11,1,'#ffc727');fl(16,5,'#e03a4e');
  R(g,3,9,5,1,'#c98d4a');R(g,4,10,4,1,'#8a5a2c');return c;}""")
swapfn('snowPoleSprite',"""function snowPoleSprite(){const c=mk(4,18),g=c.getContext('2d');R(g,0,0,4,18,K);for(let y=1;y<17;y+=4){R(g,1,y,1,2,'#ffa04a');R(g,2,y,1,2,'#d0600f');if(y+2<17){R(g,1,y+2,1,2,'#6a7286');R(g,2,y+2,1,2,'#2a2a36');}}return c;}""")
open(f,'w',encoding='utf-8').write(s)
print('p83 props batch 2: 12 props redrawn')
