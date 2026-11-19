# p144: cars that drive sideways use the same top-down car art, turned (Alex: "when cars drive sideways their art isn't
# updated and it looks bugged and squished"). Parked cars now turn smoothly as they pull out and back in; crossing traffic
# uses the top-down car on its side (32x22) instead of the old flat side view (30x14). Hit boxes stay a little smaller
# than the art so near misses feel fair.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a);assert n==cnt,(n,a[:90]);s=s.replace(a,b)

# helpers: a top-down car turned on its side (exact 90-degree pixel turn, outer wheel stubs trimmed to fit 22px lanes)
rep("function carSideOf(col){",
"""function carTopH(v){if(v._h)return v._h;const w2=v.height,h2=v.width-2,c=mk(w2,h2),src=v.getContext('2d').getImageData(0,0,v.width,v.height).data,gc=c.getContext('2d'),od=gc.createImageData(w2,h2);
  for(let y2=0;y2<h2;y2++)for(let x2=0;x2<w2;x2++){const si=(x2*v.width+(v.width-2-y2))*4,oi=(y2*w2+x2)*4;for(let k=0;k<4;k++)od.data[oi+k]=src[si+k];}
  gc.putImageData(od,0,0);return v._h={R:c,L:flipH(c)};}
function pullAng(hz,dt){const side=hz.dir>0?-Math.PI/2:Math.PI/2,tg=(hz.state==='turn'||hz.state==='leave'||hz.state==='arrive'||hz.state==='away')?side:0;
  if(hz.state==='arrive'&&Math.abs(hz.x-hz.hx)>40)hz.ang=tg;const a=hz.ang||0,st=dt*4.6;hz.ang=Math.abs(tg-a)<=st?tg:a+Math.sign(tg-a)*st;}
function carSideOf(col){""")

# parked cars: turn angle follows the state; the sideways car's box matches the new art
rep("if(hz.kind==='pull'){hz.t-=dt;","if(hz.kind==='pull'){hz.t-=dt;pullAng(hz,dt);")
# a sideways car only stops for you when you're in front of its nose (it used to stop whenever you touched any part of it,
# which with the full-size art left cars and players waiting on each other in car-park aisles)
rep("const r={x:hz.x-4+hz.dir*3,y:hz.home+37,w:30,h:14};","const r=hz.dir>0?{x:hz.x+19,y:hz.home+35,w:12,h:18}:{x:hz.x-9,y:hz.home+35,w:12,h:18};")
rep("const r=d<0?{x:-40,y:y0+2,w:hx+44,h:24}:{x:hx+18,y:y0+2,w:g.pw+40-hx-18,h:24};",
    "const r=d<0?{x:-40,y:y0+4,w:hx+44,h:23}:{x:hx+18,y:y0+4,w:g.pw+40-hx-18,h:23};")
rep("""else if(hz.kind==='pull'&&(hz.state==='leave'||hz.state==='arrive')){if(!hz.sR){hz.sR=carSideOf(hz.body||'#d8364b');hz.sL=flipH(hz.sR);}const sp=hz.dir>0?hz.sR:hz.sL;ents.push({base:hz.home+51,draw:()=>b.drawImage(sp,hx-4,hz.home+37)});}""",
"""else if(hz.kind==='pull'&&Math.abs(hz.ang||0)>0.001){const a=hz.ang,cx=hx+11,cy=hy+14,full=Math.abs(Math.abs(a)-Math.PI/2)<0.001;
      ents.push({base:hz.home+55,draw:()=>{if(full){const t2=carTopH(hz.spr);b.drawImage(a<0?t2.R:t2.L,cx-16,cy-11);}else{b.save();b.translate(cx,cy);b.rotate(a);b.drawImage(hz.spr,-12,-16);b.restore();}}});}""")

# crossing traffic: top-down car on its side, centred on the lane; hit box 26x12 inside the 32x22 art (the body without its wheel stubs, a touch forgiving)
rep("sk==='car'?carSideSprite((h[1]+h[2])%5)","sk==='car'?carTopH(carSprite(CAR_PAL[(h[1]+h[2])%5][0],CAR_PAL[(h[1]+h[2])%5][1],false,false)).R")
rep("y:h[2],w:sk==='coaster'?88:spr.width-2,h:sk==='coaster'?20:12,",
    "y:h[2]-(sk==='car'?1:0),w:sk==='coaster'?88:spr.width-2,h:sk==='coaster'?20:sk==='car'?14:12,oy:sk==='car'?2:0,")
rep("R(b,ex-1,hy-2,8,14,K);R(b,ex,hy-1,6,12,'#ffd23f');text(b,'!',ex+3,hy+1,'#13306b',{align:'center',outline:null});",
    "const sy=hy+(hz.h>>1)-6;R(b,ex-1,sy-2,8,14,K);R(b,ex,sy-1,6,12,'#ffd23f');text(b,'!',ex+3,sy+1,'#13306b',{align:'center',outline:null});")
rep("R(b,x,hy+5,4,1,'rgba(255,210,63,0.6)')","R(b,x,sy+5,4,1,'rgba(255,210,63,0.6)')")
rep("b.drawImage(hz.spr,0,hy-2);b.restore();}else b.drawImage(hz.spr,Math.round(hz.x)-1,hy-2);}}});",
    "b.drawImage(hz.spr,0,hy-2-(hz.oy||0));b.restore();}else b.drawImage(hz.spr,Math.round(hz.x)-1,hy-2-(hz.oy||0));}}});")
open(p,'w',encoding='utf-8').write(s);print('p144 ok')
