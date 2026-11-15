import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:70],s.count(a));s=s.replace(a,b_)
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
# THE MANSION (Nov 16): the job's house was the generic sign-board building with "MANSION" written on it.
# Now a proper Georgian mansion: centre block with columned portico and pediment, two forward wings,
# tall lit sash windows on two floors, quoins, chimneys, dormers and a cupola. Same 176x80 size and footprint.
MANSION="""function mansionSprite(){const w=176,h=80,c=mk(w,h),g=c.getContext('2d');
  const ST='#f1e6cf',STl='#fbf5e8',STd='#d4c3a0',STs='#bfae8a';
  const roof=(x0,x1,top,eave,ins)=>{for(let y=top;y<=eave;y++){const k=Math.round(ins*(eave-y)/Math.max(1,eave-top)),a=x0+k,b2=x1-k;R(g,a,y,b2-a,1,K);if(y>top&&y<eave)R(g,a+1,y,b2-a-2,1,y===top+1?'#ffffff':(y-top)%3===0?'#e2ebf8':PAL.W);}
    R(g,x0+1,eave-1,x1-x0-2,1,'#c6d9f3');R(g,x0,eave,x1-x0,1,K);R(g,x0+1,eave+1,x1-x0-2,1,'#6a7896');icicles(g,x0+1,eave+2,x1-x0-2,x0+top,2);};
  const chim=(x,y,hh)=>{R(g,x,y,6,hh,K);R(g,x+1,y+1,4,hh-1,'#b8433f');for(let yy=y+3;yy<y+hh;yy+=3)R(g,x+1,yy,4,1,'#8e2f2c');R(g,x-1,y-1,8,3,K);R(g,x,y-1,6,2,PAL.W);R(g,x+2,y-2,2,1,'#55607a');};
  const win=(x,y,hh)=>{R(g,x-1,y-2,8,1,STs);R(g,x+2,y-3,2,2,STl);R(g,x,y,6,hh,K);R(g,x+1,y+1,4,hh-2,'#ffe27a');R(g,x+1,y+1,4,1,'#fff3b0');R(g,x+1,y+Math.floor(hh/2),4,1,'#f4f8ff');R(g,x+3,y+1,1,hh-2,'#f4f8ff');R(g,x+1,y+hh-2,1,1,'#e8b84a');R(g,x-1,y+hh,8,1,PAL.W);R(g,x-1,y+hh+1,8,1,STs);};
  const wall=(x0,x1,y0,y1)=>{R(g,x0,y0,x1-x0,y1-y0,K);R(g,x0+1,y0,x1-x0-2,y1-y0-1,ST);for(let y=y0+3;y<y1-1;y+=4)R(g,x0+1,y,x1-x0-2,1,'#e9dcc0');
    R(g,x0+1,y0,x1-x0-2,1,STd);for(const qx of [x0+1,x1-4])for(let y=y0+1,k=0;y<y1-1;y+=3,k++)R(g,qx,y,3,2,k%2?STd:STl);R(g,x0+1,y1-3,x1-x0-2,2,STd);R(g,x0+1,y1-2,x1-x0-2,1,STs);};
  // centre block
  chim(52,1,12);chim(118,1,12);
  roof(42,134,5,34,9);
  for(const dx of [58,110]){R(g,dx-1,20,9,10,K);R(g,dx,21,7,8,PAL.W);R(g,dx+1,24,5,6,K);R(g,dx+2,25,3,4,'#ffe27a');R(g,dx+2,25,3,1,'#fff3b0');R(g,dx-1,20,9,1,K);R(g,dx,19,7,2,PAL.W);}
  // cupola
  R(g,82,2,12,12,K);R(g,83,6,10,7,STl);R(g,85,8,2,4,'#ffe27a');R(g,89,8,2,4,'#ffe27a');R(g,83,6,10,1,STd);R(g,82,1,12,5,K);R(g,83,2,10,3,'#5fa89a');R(g,84,2,4,1,'#8fd0c2');R(g,87,0,2,2,K);R(g,87,0,2,1,'#ffd23f');
  wall(42,134,35,73);
  for(const x of [52,63,107,118]){win(x,40,10);win(x,56,11);}
  // portico: pediment, entablature, four columns, door with fanlight, steps
  for(let r=0;r<11;r++){const half=Math.round(17*(r+1)/11);R(g,88-half,27+r,half*2,1,K);if(half>1)R(g,89-half,27+r,half*2-2,1,r<2?PAL.W:r<4?'#e2ebf8':STl);}
  R(g,72,38,32,4,K);R(g,73,38,30,2,STl);R(g,73,40,30,1,STd);g.fillStyle=K;pixCircle(g,88,33,2);g.fillStyle='#ffe27a';pixCircle(g,88,33,1);
  R(g,73,42,30,31,'#e3d5b6');R(g,73,42,30,1,STs);
  R(g,83,57,10,16,K);R(g,84,60,8,13,'#5a3420');R(g,88,60,1,13,K);R(g,84,61,3,1,'#6e4428');R(g,89,61,3,1,'#6e4428');R(g,86,66,1,1,'#ffd23f');R(g,90,66,1,1,'#ffd23f');R(g,84,57,8,3,'#ffe27a');R(g,85,57,6,1,'#fff3b0');R(g,88,57,1,3,K);
  for(const cx of [74,79,95,100]){R(g,cx,42,4,31,K);R(g,cx+1,42,2,31,'#fbfbff');R(g,cx+1,42,1,31,'#ffffff');R(g,cx+2,43,1,30,'#d6dee9');R(g,cx-1,42,6,2,K);R(g,cx,42,4,1,STl);R(g,cx-1,71,6,2,K);R(g,cx,71,4,1,STl);}
  R(g,71,73,34,2,K);R(g,72,73,32,1,'#c6ccd8');R(g,69,75,38,2,K);R(g,70,75,36,1,'#d6dee9');R(g,67,77,42,3,K);R(g,68,77,40,2,'#e3e9f2');R(g,68,78,40,1,'#b8c2d4');
  // wings, a step forward of the centre
  for(const [x0,x1] of [[2,52],[124,174]]){chim(x0===2?8:160,4,12);roof(x0,x1,10,42,6);wall(x0,x1,43,79);R(g,x0+1,58,x1-x0-2,1,STs);R(g,x0+1,59,x1-x0-2,1,STl);
    for(const k of [0,1,2]){const wx=x0+8+k*14;win(wx,47,9);win(wx,63,11);}drift(g,x0,79,6,3);drift(g,x1-13,79,6,3);}
  return c;}
"""
rep("function bigBuilding(","%s\nfunction bigBuilding("%MANSION.strip())
rep("ob(bigBuilding(176,80,'#f4f8ff','#8793a8','MANSION','#ffc727'),2,0,0,0,176,80);","ob(mansionSprite(),2,0,0,0,176,80);")
# castle towers (Nov 16): the round towers read as blue baubles from above. Now stone turrets: crenellated rim,
# snowy deck with a hatch, a visible stone drum below and a pennant. Same 30x30 size and footprint.
swapfn('towerSprite',"""function towerSprite(){const c=mk(30,30),g=c.getContext('2d');
  g.fillStyle=K;pixCircle(g,15,17,13);g.fillStyle='#6a7896';pixCircle(g,15,17,12);for(let y=17;y<30;y+=3)for(let x=3+((y/3|0)%2)*3;x<28;x+=6){R(g,x,y,1,2,'#55607a');}R(g,3,20,24,1,'#55607a');R(g,4,25,22,1,'#55607a');
  g.fillStyle=K;pixCircle(g,15,13,13);g.fillStyle='#9aa6ba';pixCircle(g,15,13,12);
  for(let k=0;k<12;k++){const a=k/12*Math.PI*2,mx=Math.round(15+Math.cos(a)*10.5),my=Math.round(13+Math.sin(a)*10.5);R(g,mx-1,my-1,3,3,k%2?'#55607a':'#c6ccd8');if(!(k%2))R(g,mx-1,my-1,3,1,'#e3e9f2');}
  g.fillStyle=K;pixCircle(g,15,13,8);g.fillStyle='#d3e3f7';pixCircle(g,15,13,7);g.fillStyle='#f4f8ff';pixCircle(g,14,12,6);R(g,17,15,4,3,K);R(g,18,16,2,1,'#8a5a34');
  R(g,10,2,1,10,K);R(g,11,3,6,4,'#d8364b');R(g,11,3,6,1,'#ff6a7a');R(g,17,4,1,2,'#d8364b');return c;}""")
# test-mode only: evaluate an expression inside the game's scope (sprite audits)
rep("if(TEST_MODE)window.__LM=","if(TEST_MODE)window.__EV=(src)=>eval(src);if(TEST_MODE)window.__LM=")
open(f,'w',encoding='utf-8').write(s)
print('p97 mansion + castle towers')
