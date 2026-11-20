# p146 (Alex, Nov 20 22:34: "a bugged cow ... we need a whole game audit for bugged/glitched characters/props/animals";
# "you spawn in front of a pole so you crash as soon as you start").
#  1. Walking characters and animals keep their whole drawn body clear of props: no more cows inside fences, dogs
#     half inside kennels, people walking through lamp posts or behind shop walls. Movers that start overlapping a
#     prop are moved to the nearest clear spot when the job starts (also snowball throwers hidden behind buildings).
#  2. Starts with a prop in the way: Main Street (street clock right under the start), Stadium (big machines overlapped
#     the goal), Ice Rink, Penguin Colony, Apres-Ski, Train Station, Farm Shop.
import sys,json
f=sys.argv[1];s=open(f).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt,(a[:90],n)
    s=s.replace(a,b)
def job_span(jid):
    i=s.find('{"id":"%s",'%jid);assert i>=0,jid
    d=0;j=i
    while True:
        c=s[j]
        if c=='{':d+=1
        elif c=='}':
            d-=1
            if d==0:return i,j+1
        j+=1
def job_rep(jid,a,b):
    global s
    i,j=job_span(jid);sub=s[i:j];assert sub.count(a)==1,(jid,a,sub.count(a))
    s=s[:i]+sub.replace(a,b)+s[j:]

# ---- 2. starts ----
job_rep('mainst','["clock",84,40]','["clock",52,40]')          # the street clock stood right under the start
job_rep('icerink','"start":[146,2150]','"start":[124,2150]')    # a street tree 2px above the Icebreaker
job_rep('penguins','["flag",80,48,1]','["flag",44,48,1]')        # a flag 12px in front of the start
job_rep('apres','"start":[90,40]','"start":[145,40]')           # start sat above a building; the open lane is on the right
job_rep('station','["bins",112,2700]','["bins",122,2700]')       # bins + clock pinched the start lane to 33px
job_rep('station','["clock",70,2700]','["clock",56,2700]')
job_rep('farmcafe','["parasol",70,80,0]','["parasol",40,80,0]')  # parasol straight ahead of the start
rep("    g.spawners.push({kind:'sled',every:[6,9],t:5});\n    g.start={x:90,y:120};",
    "    g.spawners.push({kind:'sled',every:[6,9],t:5});\n    g.start={x:90,y:130};")   # big machines overlapped the goal at y 92-100

# ---- 1. movers keep their drawn bodies clear of props ----
rep("function updateHazards(dt,tid){", r"""// ---- movers keep their drawn body clear of props (p146) ----
const _amask=new WeakMap();
function aMask(c){let m=_amask.get(c);if(m)return m;const w=c.width,h=c.height;m=new Uint8Array(w*h);try{const d=c.getContext('2d').getImageData(0,0,w,h).data;for(let i=0;i<w*h;i++)m[i]=d[i*4+3]>40?1:0;}catch(e){m.fill(1);}_amask.set(c,m);return m;}
function propBands(){const g=G;if(g._pb)return g._pb;const m=new Map(),add=q=>{for(let k=Math.floor(q.y/64);k<=Math.floor((q.y+q.h)/64);k++){let a=m.get(k);if(!a)m.set(k,a=[]);a.push(q);}};
  for(const o of g.obstacles)add({x:o.sx,y:o.sy,w:o.spr.width,h:o.spr.height,top:o.sy+(o.spr.padTop||0),base:o.base,spr:o.spr});
  for(const o of g.scenery)add({x:o.sx,y:o.sy,w:o.spr.width,h:o.spr.height,top:o.sy+(o.spr.padTop||0),base:o.base,spr:o.spr});return g._pb=m;}
// the mover's sprite as drawn at position (x,y) of its own fields: [left, top, canvas, sort base]
function moverBox(kind,hz,x,y){let s=null,bx=0,by=0,base=0;
  if(kind==='cow'){s=COW;bx=Math.round(x)-8;by=Math.round(y)-10;base=y+3;}
  else if(kind==='dog'){s=hz.spr||SPR.dog;bx=Math.round(x)-1;by=Math.round(y)-4;base=y+hz.h;}
  else if(kind==='cart'){s=CART;bx=Math.round(x)-2;by=Math.round(y)-3;base=y+hz.h;}
  else if(kind==='ped'){if(hz.ghost||!hz.spr)return null;s=hz.spr;bx=Math.round(x)-2;by=Math.round(y)-9;base=y+hz.h;}
  else if(kind==='sheep'){if(hz.gull)return null;s=hz.peng?PENG_FR[0]:hz.horse?HORSE_FR[hz.col||0]:SHEEP_FR[0];const ox=(hz.horse||hz.peng)?1:3,oy=hz.horse?6:hz.peng?3:5;bx=Math.round(x)-ox;by=Math.round(y)-oy;base=y+hz.h;}
  else if(kind==='thrower'){s=SPR.thrower;bx=Math.round(x)-6;by=Math.round(y)-14;base=hz.y+hz.h+(y-hz.sy);}
  else if(kind==='bumper'){if(hz.fork){s=FORK_FR[0];bx=Math.round(x+hz.w/2)-8;by=Math.round(y+hz.h/2)-11;}else{s=hz.spr;bx=Math.round(x)-1;by=Math.round(y)-4;}base=y+hz.h;}
  if(!s)return null;return [bx,by,s,base];}
// clear = no prop is drawn over the mover while it stands beside the prop (feet inside the prop's height band)
function bodyClear(B){if(!B)return true;const [bx,by,s,base]=B,w=s.width,h=s.height,ma=aMask(s),pb=propBands();
  if(bx<-1||bx+w>G.pw+1)return false;
  for(let k=Math.floor(by/64);k<=Math.floor((by+h)/64);k++)for(const q of (pb.get(k)||[])){if(q.base<=base||base<=q.top+3)continue;
    const x0=Math.max(bx,q.x),x1=Math.min(bx+w,q.x+q.w),y0=Math.max(by,q.y),y1=Math.min(by+h,q.y+q.h);if(x1<=x0||y1<=y0)continue;
    const qa=aMask(q.spr);let n=0;for(let yy=y0;yy<y1;yy++)for(let xx=x0;xx<x1;xx++)if(qa[(yy-q.y)*q.w+(xx-q.x)]&&ma[(yy-by)*w+(xx-bx)]&&++n>=3)return false;}
  return true;}
function mClear(kind,hz,x,y){return bodyClear(moverBox(kind,hz,x,y));}
// at the start of a job: anything standing in a prop moves to the nearest clear spot (spiral, up to 30px)
function settleMovers(){const g=G,free=(kind,hz,x,y,w,h)=>{if(x<1||y<1||x+w>g.pw-1||y+h>g.ph-1)return false;const r={x,y,w,h};if(wildHit(r))return false;for(const o of g.obstacles)if(overlap(r,o))return false;
    for(let cy=Math.floor(y/2);cy<Math.ceil((y+h)/2);cy++)for(let cx=Math.floor(x/2);cx<Math.ceil((x+w)/2);cx++)if(g.type[cy*g.cols+cx]===T_BLOCK)return false;return mClear(kind,hz,kind==='cow'?x+5:x,kind==='cow'?y+3:y);};
  const spiral=(kind,hz,x0,y0,w,h,set)=>{if(free(kind,hz,x0,y0,w,h))return;for(let d=2;d<=30;d+=2)for(let a=0;a<16;a++){const x=Math.round(x0+Math.cos(a/16*Math.PI*2)*d),y=Math.round(y0+Math.sin(a/16*Math.PI*2)*d);if(free(kind,hz,x,y,w,h)){set(x,y);return;}}};
  for(const cw of g.cows)spiral('cow',cw,cw.x-5,cw.y-3,10,5,(x,y)=>{cw.x=x+5;cw.y=y+3;});
  for(const hz of g.hazards){if(['dog','cart','ped','sheep','bumper'].includes(hz.kind)&&!hz.gull&&!hz.ghost)spiral(hz.kind,hz,hz.x,hz.y,hz.w,hz.h,(x,y)=>{if(hz.hx!=null){hz.hx+=x-hz.x;hz.hy+=y-hz.y;}hz.x=x;hz.y=y;});
    else if(hz.kind==='thrower'&&hz.sx!=null&&!mClear('thrower',hz,hz.sx,hz.sy)){for(let d=2,done=0;d<=64&&!done;d+=2)for(let a=0;a<24&&!done;a++){const dx=Math.round(Math.cos(a/24*Math.PI*2)*d),dy=Math.round(Math.sin(a/24*Math.PI*2)*d);
        const r={x:hz.x+dx,y:hz.y+dy,w:hz.w,h:hz.h};let ok=r.x>1&&r.x+r.w<g.pw-1&&!wildHit(r);if(ok)for(const o of g.obstacles)if(overlap(r,o)){ok=false;break;}
        if(ok&&mClear('thrower',hz,hz.sx+dx,hz.sy+dy)){hz.x+=dx;hz.y+=dy;hz.sx+=dx;hz.sy+=dy;if(hz.tx!=null){hz.tx+=dx;hz.ty+=dy;}done=1;}}}}}
function updateHazards(dt,tid){""")
# props that move or vanish rebuild the bands
rep("function crushOb(o){const i=G.obstacles.indexOf(o);if(i<0)return;G.obstacles.splice(i,1);",
    "function crushOb(o){const i=G.obstacles.indexOf(o);if(i<0)return;G.obstacles.splice(i,1);G._pb=null;")
rep("o.x+=dx;o.y+=dy;o.sx+=dx;o.sy+=dy;o.base=o.y+o.h;","o.x+=dx;o.y+=dy;o.sx+=dx;o.sy+=dy;o.base=o.y+o.h;G._pb=null;")
# settle once the job (and any event/lab additions) is built
rep("G=evBuild(idx,opts);P={x:G.start.x,y:G.start.y,f:2,","G=evBuild(idx,opts);settleMovers();P={x:G.start.x,y:G.start.y,f:2,")
# cows
rep("let bad=nx<8||nx>G.pw-8||ny<30||ny>G.ph-10;if(!bad)if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}\n      if(!bad&&tid!=='ufo')",
    "let bad=nx<8||nx>G.pw-8||ny<30||ny>G.ph-10;if(!bad)if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}\n      if(!bad&&!mClear('cow',cw,nx,ny))bad=true;\n      if(!bad&&tid!=='ufo')")
# dogs (also keep the sprite inside the map)
rep("const r={x:hz.x+hz.vx*dt,y:hz.y+hz.vy*dt,w:hz.w,h:hz.h};let bad=r.x<0||r.y<hz.minY||r.x+r.w>G.pw||r.y+r.h>G.ph;if(!bad)if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}",
    "const r={x:hz.x+hz.vx*dt,y:hz.y+hz.vy*dt,w:hz.w,h:hz.h};let bad=r.x<1||r.y<hz.minY||r.x+r.w>G.pw-3||r.y+r.h>G.ph;if(!bad)if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}if(!bad&&!mClear('dog',hz,r.x,r.y))bad=true;")
# carts
rep("if(!bx&&!by)for(const o of G.obstacles)if(overlap(r,o)){if(overlap({x:r.x,y:hz.y,w:r.w,h:r.h},o))bx=true;else by=true;}",
    "if(!bx&&!by)for(const o of G.obstacles)if(overlap(r,o)){if(overlap({x:r.x,y:hz.y,w:r.w,h:r.h},o))bx=true;else by=true;}\n      if(!bx&&!by&&!mClear('cart',hz,r.x,r.y)){if(!mClear('cart',hz,r.x,hz.y))bx=true;else by=true;}")
# people
rep("let bad=ny<10||ny+hz.h>G.ph-10||nx<2||nx+hz.w>G.pw-2;if(!bad)if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}",
    "let bad=ny<10||ny+hz.h>G.ph-10||nx<2||nx+hz.w>G.pw-2;if(!bad)if(wildHit(r))bad=true;else for(const o of G.obstacles)if(overlap(r,o)){bad=true;break;}if(!bad&&!mClear('ped',hz,nx,ny))bad=true;")
# sheep, horses, penguins
rep("const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y))hz.x=nx;else hz.vx*=-0.5;if(chaserFree(hz,hz.x,ny))hz.y=ny;else hz.vy*=-0.5;",
    "const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y)&&mClear('sheep',hz,nx,hz.y))hz.x=nx;else hz.vx*=-0.5;if(chaserFree(hz,hz.x,ny)&&mClear('sheep',hz,hz.x,ny))hz.y=ny;else hz.vy*=-0.5;")
rep("const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y))hz.x=nx;else{hz.vx*=-1;",
    "const nx=hz.x+hz.vx*dt,ny=hz.y+hz.vy*dt;if(chaserFree(hz,nx,hz.y)&&mClear('bumper',hz,nx,hz.y))hz.x=nx;else{hz.vx*=-1;")
rep("if(chaserFree(hz,hz.x,ny))hz.y=ny;else hz.vy*=-1;\n      for(const o2 of G.hazards)if(o2!==hz&&o2.kind==='bumper'",
    "if(chaserFree(hz,hz.x,ny)&&mClear('bumper',hz,hz.x,ny))hz.y=ny;else hz.vy*=-1;\n      for(const o2 of G.hazards)if(o2!==hz&&o2.kind==='bumper'")
open(f,'w').write(s)
print('p146 glitch fix: movers keep clear of props, settled at start; 7 starts cleared')
