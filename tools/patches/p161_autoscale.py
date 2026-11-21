# Audit Nov 21: one tester's Android (3.75 pixel ratio) ran under 30 fps for 36% of its frames and needed a continue
# in all 4 of its jobs. Big phones draw the 180x320 game into a canvas of up to 1440x2560 (KS up to 8) every frame.
# Automatic render scale: when more than 20% of frames are slow (>34 ms) over 4 s of play, the canvas drops to a
# lower scale (8 -> 4 -> 3 -> 2). The page still upscales with image-rendering: pixelated, so the pixel art looks the
# same. Remembered per phone (localStorage sr.kscap, not the save, which can move between devices). Off in test mode
# unless window.__AQTEST is set.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("function resize(){const vw=wrap.clientWidth||innerWidth,vh=wrap.clientHeight||innerHeight;const cs=Math.min(vw/W,vh/H);const dpr=window.devicePixelRatio||1;\n  KS=Math.max(1,Math.min(window.SR_KS||8,Math.ceil(cs*dpr)));",
    "let KS_CAP=8;try{KS_CAP=Math.max(2,Math.min(8,+localStorage.getItem('sr.kscap')||8));}catch(e){}\n"
    "const AQ={n:0,s:0,t:0,last:0};\n"
    "// automatic render scale: a phone that can't keep up draws at a lower scale (the pixelated upscale keeps the look)\n"
    "function aqTick(now){const gap=now-AQ.last;AQ.last=now;if((TEST_MODE&&!window.__AQTEST)||state!=='play'||paused||KS<=2||!run||run.ended||Date.now()-(PH.jobT||0)<2500){AQ.n=AQ.s=0;AQ.t=now;return;}\n"
    "  AQ.n++;if(gap>34)AQ.s++;if(now-AQ.t<4000)return;\n"
    "  if(AQ.n>=60&&AQ.s/AQ.n>0.2){const was=KS;KS_CAP=KS>4?4:KS>3?3:2;try{localStorage.setItem('sr.kscap',String(KS_CAP));}catch(e){}resize();AQ.drop={from:was,to:KS,slow:Math.round(AQ.s/AQ.n*100)};}\n"
    "  AQ.n=AQ.s=0;AQ.t=now;}\n"
    "function resize(){const vw=wrap.clientWidth||innerWidth,vh=wrap.clientHeight||innerHeight;const cs=Math.min(vw/W,vh/H);const dpr=window.devicePixelRatio||1;\n  KS=Math.max(1,Math.min(window.SR_KS||8,KS_CAP,Math.ceil(cs*dpr)));")
rep("function frame(now){const dt=Math.min(0.05,(now-last)/1000);last=now;",
    "function frame(now){const dt=Math.min(0.05,(now-last)/1000);last=now;try{aqTick(now);}catch(e){}")
open(f,'w',encoding='utf-8').write(s)
print('p161 automatic render scale for slow phones')
