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
# Props audit batch 1 (Nov 16): walls, fences and rails, the pieces drawn all over every job. Same sizes and
# footprints; now with shaded rails and posts, block bevels, mesh, ballast and leaf texture.
swapfn('railSprite',"""function railSprite(w,h){const c=mk(w,h),g=c.getContext('2d');
  if(w>=h){R(g,0,1,w,4,K);R(g,0,2,w,1,'#9fd0e8');R(g,0,3,w,1,'#2f6f8a');R(g,0,5,w,2,K);R(g,0,5,w,1,'#3f7f9a');for(let x=0;x<w-1;x+=6){R(g,x,0,2,h,K);R(g,x,1,1,h-2,'#8793a8');}R(g,w-2,0,2,h,K);R(g,w-2,1,1,h-2,'#8793a8');}
  else{R(g,0,0,w,h,K);R(g,1,0,1,h,'#9fd0e8');R(g,2,0,1,h,'#2f6f8a');R(g,3,0,1,h,'#1d4a5e');for(let y=0;y<h-1;y+=6){R(g,0,y,w,2,K);R(g,1,y,w-2,1,'#8793a8');}R(g,0,h-2,w,2,K);R(g,1,h-2,w-2,1,'#8793a8');}return c;}""")
swapfn('fenceSprite',"""function fenceSprite(h){const c=mk(12,h),g=c.getContext('2d');R(g,0,0,12,h,K);R(g,1,0,10,h,'#a8673a');R(g,2,0,1,h,'#e0b070');R(g,3,0,1,h,'#c98d4a');R(g,9,0,2,h,'#7a4a2a');
  for(let y=0;y<h;y+=6){R(g,1,y,10,1,'#6b4426');if((y/6)%3===1)R(g,5,y+3,2,1,'#7a4a2a');}for(let y=0;y<h;y+=24){R(g,0,y,12,4,K);R(g,1,y+1,10,2,'#55321d');R(g,1,y+1,10,1,'#8a5a34');}R(g,1,0,1,h,PAL.W);return c;}""")
swapfn('snowFenceSprite',"""function snowFenceSprite(w,v){const c=v?mk(6,w):mk(w,8),g=c.getContext('2d');const mesh=(i,j)=>((i+j*2)%4===0)||((i-j*2+400)%4===0);
  if(v){R(g,1,0,4,w,K);for(let y=0;y<w;y++)for(let x=2;x<4;x++)R(g,x,y,1,1,mesh(y,x-2)?'#ffd0a0':(x===2?'#ffa04a':'#f07a1a'));for(let y=0;y<w;y+=24){R(g,0,y,6,3,K);R(g,1,y+1,4,1,'#8793a8');}}
  else{R(g,0,1,w,6,K);for(let y=2;y<6;y++)for(let x=0;x<w;x++)R(g,x,y,1,1,mesh(x,y-2)?'#ffd0a0':(y===2?'#ffa04a':y===5?'#c85a10':'#f07a1a'));for(let x=0;x<w;x+=24){R(g,x,0,3,8,K);R(g,x+1,1,1,6,'#8793a8');}}return c;}""")
swapfn('stoneWallSprite',"""function stoneWallSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,'#4a5068');const cols=[['#9aa6ba','#7a869c','#b8c2d4'],['#a8b2c4','#8793a8','#c6ccd6'],['#8793a8','#6a7896','#a3adc0'],['#b0b8c8','#8f98ad','#d0d6e0']];
  if(w>=h){for(let y=1;y<h-1;y+=3)for(let x=1+((y/3|0)%2)*3-3;x<w-1;x+=6){const x0=Math.max(1,x),x1=Math.min(w-1,x+5);if(x1<=x0)continue;const cc=cols[((x*7+y*3)>>>0)%4];R(g,x0,y,x1-x0,2,cc[0]);R(g,x0,y+1,x1-x0,1,cc[1]);R(g,x0,y,1,1,cc[2]);}}
  else{for(let x=1;x<w-1;x+=3)for(let y=1+((x/3|0)%2)*3-3;y<h-1;y+=6){const y0=Math.max(1,y),y1=Math.min(h-1,y+5);if(y1<=y0)continue;const cc=cols[((x*3+y*7)>>>0)%4];R(g,x,y0,2,y1-y0,cc[0]);R(g,x+1,y0,1,y1-y0,cc[1]);R(g,x,y0,1,1,cc[2]);}R(g,1,1,1,h-2,PAL.W);}return c;}""")
swapfn('wallSprite',"""function wallSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,'#4a5068');
  if(w>=h){for(let y=1;y<h-1;y+=6)for(let x=1-((y/6|0)%2)*4;x<w-1;x+=8){const x0=Math.max(1,x),x1=Math.min(w-1,x+7),y1=Math.min(h-1,y+5);if(x1<=x0)continue;R(g,x0,y,x1-x0,y1-y,'#8793a8');R(g,x0,y,x1-x0,1,'#a9b4c6');R(g,x0,y1-1,x1-x0,1,'#6a7896');R(g,x1-1,y+1,1,y1-y-1,'#6a7896');}for(let x=1;x<w-1;x+=6)R(g,x,1,3,3,'#f4f8ff');}
  else{for(let x=1;x<w-1;x+=6)for(let y=1-((x/6|0)%2)*4;y<h-1;y+=8){const y0=Math.max(1,y),y1=Math.min(h-1,y+7),x1=Math.min(w-1,x+5);if(y1<=y0)continue;R(g,x,y0,x1-x,y1-y0,'#8793a8');R(g,x,y0,1,y1-y0,'#a9b4c6');R(g,x1-1,y0,1,y1-y0,'#6a7896');R(g,x,y1-1,x1-x,1,'#6a7896');}for(let y=1;y<h-1;y+=6)R(g,1,y,3,3,'#f4f8ff');}return c;}""")
swapfn('iceWallSprite',"""function iceWallSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,'#7dbfe8');
  if(w>=h){for(let y=1;y<h-1;y+=5)for(let x=1+((y/5|0)%2)*4-4;x<w-1;x+=8){const x0=Math.max(1,x),x1=Math.min(w-1,x+7),y1=Math.min(h-1,y+4);if(x1<=x0)continue;R(g,x0,y,x1-x0,y1-y,'#a8dcfa');R(g,x0,y,x1-x0,1,'#d4f0ff');R(g,x0,y,1,y1-y,'#d4f0ff');if(((x*5+y)>>>0)%3===0)R(g,x0+1,y+1,1,1,'#ffffff');}R(g,1,1,w-2,1,PAL.W);for(let x=0;x<w;x+=8){R(g,x,0,4,3,K);R(g,x+1,0,2,2,'#d4f0ff');}}
  else{for(let x=1;x<w-1;x+=5)for(let y=1+((x/5|0)%2)*4-4;y<h-1;y+=8){const y0=Math.max(1,y),y1=Math.min(h-1,y+7),x1=Math.min(w-1,x+4);if(y1<=y0)continue;R(g,x,y0,x1-x,y1-y0,'#a8dcfa');R(g,x,y0,x1-x,1,'#d4f0ff');R(g,x,y0,1,y1-y0,'#d4f0ff');if(((y*5+x)>>>0)%3===0)R(g,x+1,y0+1,1,1,'#ffffff');}R(g,1,1,1,h-2,PAL.W);}return c;}""")
swapfn('hedgeSprite',"""function hedgeSprite(w,h){const c=mk(w,h),g=c.getContext('2d');R(g,0,0,w,h,K);R(g,1,1,w-2,h-2,'#1d5e34');
  const cl=(xx,yy,ww,hh,col)=>{const x0=Math.max(1,xx),y0=Math.max(1,yy),x1=Math.min(w-1,xx+ww),y1=Math.min(h-1,yy+hh);if(x1>x0&&y1>y0)R(g,x0,y0,x1-x0,y1-y0,col);};
  for(let j=0;j*3<h;j++)for(let i=-1;i*4<w;i++){const x=1+i*4+(j%2)*2,y=1+j*3,n=((i*7+j*13)>>>0)%5;
    cl(x+1,y,2,1,'#3f9e58');cl(x,y+1,4,2,'#2f8a4a');cl(x,y+1,1,1,'#4fb46a');if(n)cl(x+1,y+1,1,1,'#6fd07f');cl(x+3,y+2,1,1,'#246f3d');if(n===0)cl(x+2,y+1,1,1,'#d8364b');}
  if(w>=h)R(g,1,1,w-2,1,'#f4f8ff');else R(g,1,1,1,h-2,'#f4f8ff');return c;}""")
swapfn('rockNetSprite',"""function rockNetSprite(h){const c=mk(8,h),g=c.getContext('2d');for(let y=0;y<h;y++)for(let x=1;x<7;x++){if(((x+y)%4===0)||((x-y+4000)%4===0))R(g,x,y,1,1,'#3a3f55');}R(g,0,0,1,h,'#2a2a36');R(g,7,0,1,h,'#2a2a36');
  for(let y=0;y<h;y+=28){R(g,1,y,6,6,K);R(g,2,y+1,4,4,'#8793a8');R(g,2,y+1,4,1,'#c6d0e0');R(g,5,y+2,1,3,'#55607a');}return c;}""")
swapfn('coasterSprite',"""function coasterSprite(w,h){const c=mk(w,h),g=c.getContext('2d');const hz=w>=h;
  if(hz){for(let x=2;x<w;x+=10){R(g,x,4,2,h-4,K);R(g,x,5,1,h-6,'#c6d0dc');if(x+7<w)for(let k=0;k<Math.min(5,h-6);k++)R(g,x+2+k,5+k,1,1,'#8793a8');}R(g,0,0,w,5,K);R(g,0,1,w,1,'#f28b8b');R(g,0,3,w,1,'#d8364b');for(let x=1;x<w;x+=3)R(g,x,2,1,1,'#8793a8');}
  else{for(let y=4;y<h;y+=10){R(g,0,y,w,2,K);R(g,0,y,w,1,'#c6d0dc');}R(g,1,0,5,h,K);R(g,2,0,1,h,'#f28b8b');R(g,4,0,1,h,'#d8364b');for(let y=1;y<h;y+=3)R(g,3,y,1,1,'#8793a8');}return c;}""")
swapfn('trackSprite',"""function trackSprite(h){const c=mk(22,h),g=c.getContext('2d');R(g,1,0,20,h,'#9aa1b5');for(let y=0;y<h;y++)for(let x=1;x<21;x++){const n=((x*31+y*17+x*y*7)>>>0)%9;if(n<2)R(g,x,y,1,1,'#7a8196');else if(n===2)R(g,x,y,1,1,'#c6ccd8');}
  for(let y=0;y<h;y+=5){R(g,0,y,22,2,K);R(g,1,y,20,1,'#a8743f');R(g,1,y+1,20,1,'#6b4426');}R(g,3,0,2,h,K);R(g,17,0,2,h,K);R(g,3,0,1,h,'#e3ebf6');R(g,17,0,1,h,'#e3ebf6');R(g,4,0,1,h,'#8793a8');R(g,18,0,1,h,'#8793a8');return c;}""")
swapfn('netSprite',"""function netSprite(w){const c=mk(w,8),g=c.getContext('2d');R(g,0,0,3,8,K);R(g,w-3,0,3,8,K);R(g,1,1,1,7,'#c6d9f3');R(g,w-2,1,1,7,'#c6d9f3');
  R(g,3,1,w-6,6,K);R(g,3,2,w-6,1,'#f4f8ff');for(let x=3;x<w-3;x++)for(let y=3;y<6;y++)R(g,x,y,1,1,((x+y)%3===0||(x-y+999)%3===0)?'#55607a':'#c6d0dc');return c;}""")
swapfn('avFenceSprite',"""function avFenceSprite(w){const c=mk(w,10),g=c.getContext('2d');R(g,0,3,w,6,K);for(let y=4;y<8;y++)for(let x=0;x<w;x++)R(g,x,y,1,1,((x+y)%3===0||(x-y+999)%3===0)?'#a3adc0':'#3a3f55');R(g,0,4,w,1,'#c6d0dc');
  for(let x=0;x<w;x+=20){R(g,x,0,3,10,K);R(g,x+1,1,1,8,'#8793a8');}return c;}""")
open(f,'w',encoding='utf-8').write(s)
print('p95 props batch 3: walls/fences/rails')
