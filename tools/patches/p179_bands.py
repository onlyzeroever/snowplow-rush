# Tall phones (Nov 21, before the store screenshots). HELD from the live web game for Alex's look; in the lab and the
# app build. The game is 9:16, so on 19.5:9 phones (and in the full-screen apps) there were plain dark bands above and
# below it. Now the page behind the game is a night sky in the game's own pixel size: navy getting lighter toward the
# edges, scattered snowflakes, a snowy edge along the bottom. Drawn once per resize (no cost while playing).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("#wrap{position:fixed;inset:0;box-sizing:border-box;",
    "#bg{position:fixed;inset:0;width:100%;height:100%}\n#wrap{position:fixed;inset:0;z-index:1;box-sizing:border-box;")
rep('<div id="wrap"><canvas id="c"','<canvas id="bg" aria-hidden="true"></canvas><div id="wrap"><canvas id="c"')
rep("function resize(){",
    "function drawBands(cs){const bg=document.getElementById('bg');if(!bg||!(cs>0))return;const w=Math.max(1,Math.ceil(innerWidth/cs)),h=Math.max(1,Math.ceil(innerHeight/cs));if(bg.width===w&&bg.height===h)return;\n"
    "  bg.width=w;bg.height=h;const g=bg.getContext('2d'),gr=g.createLinearGradient(0,0,0,h);gr.addColorStop(0,'#1d4f9a');gr.addColorStop(0.22,'#13306b');gr.addColorStop(0.5,'#0b1838');gr.addColorStop(0.78,'#13306b');gr.addColorStop(1,'#1d4f9a');g.fillStyle=gr;g.fillRect(0,0,w,h);\n"
    "  let r=20261121;const rnd=()=>{r=(r*1103515245+12345)&0x7fffffff;return r/0x7fffffff;};\n"
    "  for(let i=0,n=Math.round(w*h/70);i<n;i++){const x=Math.floor(rnd()*w),y=Math.floor(rnd()*h),big=rnd()<0.12;g.fillStyle=big?'rgba(255,255,255,0.7)':'rgba(207,227,248,0.4)';g.fillRect(x,y,big?2:1,big?2:1);}\n"
    "  for(let x=0;x<w;x++){const hh=4+Math.round(2*Math.sin(x*0.19)+1.5*Math.sin(x*0.071+1));g.fillStyle='#cfe3f8';g.fillRect(x,h-hh,1,hh);g.fillStyle='#ffffff';g.fillRect(x,h-hh,1,1);g.fillStyle='#a8c8ec';if(x%5===0)g.fillRect(x,h-hh+2,1,1);}}\n"
    "function resize(){")
rep("ctx.imageSmoothingEnabled=false;}\nwindow.addEventListener('resize',resize);resize();",
    "ctx.imageSmoothingEnabled=false;try{drawBands(cs);}catch(e){}}\nwindow.addEventListener('resize',resize);resize();")
open(f,'w',encoding='utf-8').write(s)
print('p179 tall phones: a snowy night sky behind the game instead of plain bands')
