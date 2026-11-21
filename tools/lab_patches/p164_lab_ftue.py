# Audit Nov 21, first-job pack (lab, for Alex to play): a third of new players left job 1 after 20-35 s, and half of
# the Driveway finishes needed the +15 s continue.
#  - the job clock starts on the first move (every job), not while the player is still reading the hint;
#  - on the very first job, a fingertip shows the drag (press, slide up, let go) next to the plow, and the hint box sits
#    low instead of over the middle of the screen;
#  - jobs 1-3 (Driveway, Cul-de-sac, Gardens) give three stars at 70% (was 80/85%);
#  - the first two "time's up" continues are free (no ad), so the first ad isn't on the first job.
# ?oldftue switches all four off (side-by-side test links, Nov 21).
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("if(!(DEV_MODE&&DEV.freeze))run.time-=dt;const pct=G.cleared/G.clearable*100;",
    "if(!(DEV_MODE&&DEV.freeze)&&(run.moved||!FTUE_NEW))run.time-=dt;const pct=G.cleared/G.clearable*100;")
rep("if(!run.moved&&!run.ended){const kb=!('ontouchstart' in window)&&!navigator.maxTouchPoints;panel(20,VIEW_Y+VIEW_H-110,140,kb?46:36,'#13306b','#ffd23f');\n"
    "    text(b,save.ctrl==='joy'?'DRAG ANYWHERE':'USE THE D-PAD',W/2,VIEW_Y+VIEW_H-103,'#ffffff',{align:'center',scale:2});text(b,'TO PUSH THE SNOW',W/2,VIEW_Y+VIEW_H-88,'#ffd23f',{align:'center'});if(!('ontouchstart' in window)&&!navigator.maxTouchPoints)text(b,'OR USE ARROW KEYS / WASD',W/2,VIEW_Y+VIEW_H-76,'#9fd8ff',{align:'center'});}",
    "if(!run.moved&&!run.ended){const kb=!('ontouchstart' in window)&&!navigator.maxTouchPoints,first=!save.tut&&FTUE_NEW,hy=first?VIEW_Y+VIEW_H-(kb?52:42):VIEW_Y+VIEW_H-110;\n"
    "    if(first&&save.ctrl==='joy')ftueFinger();\n"
    "    panel(20,hy,140,kb?46:36,'#13306b','#ffd23f');\n"
    "    text(b,save.ctrl==='joy'?'DRAG ANYWHERE':'USE THE D-PAD',W/2,hy+7,'#ffffff',{align:'center',scale:2});text(b,'TO PUSH THE SNOW',W/2,hy+22,'#ffd23f',{align:'center'});if(kb)text(b,'OR USE ARROW KEYS / WASD',W/2,hy+34,'#9fd8ff',{align:'center'});}")
rep("function drawStoreBusy(){",
    "// first job: a fingertip next to the plow presses, slides up 36 px and lets go, every 1.6 s, until the first move\n"
    "// ?oldftue (lab test link) switches the whole first-job pack off, to compare with the game as it is live\n"
    "const FTUE_NEW=!/[?&]oldftue/.test(location.search);\n"
    "if(!FTUE_NEW){for(const [id,st] of [['driveway',[30,55,80]],['culdesac',[35,60,85]],['gardens',[35,60,85]]]){const L=LEVELS.find(l=>l.id===id);if(L)L.stars=st;}}\n"
    "const HAND=['....OO......','...OWWO.....','...OWWO.....','...OWWO.....','...OWWOOO...','...OWWOWWOO.','.OOOWWOWWOWO','OWWOWWWWWOWO','OWWWWWWWWWWO','OWWWWWWWWWWO','.OWWWWWWWWWO','..OWWWWWWWO.','...OWWWWWO..','...OOOOOOO..'];\n"
    "function ftueFinger(){const T=(tNow%1.6)/1.6,sx=Math.round(P.x)+20,sy0=Math.round(P.y-camY+VIEW_Y)+24,u=Math.min(1,Math.max(0,(T-0.22)/0.5)),dy=Math.round((1-Math.pow(1-u,2))*38),sy=sy0-dy;\n"
    "  if(T<0.3){const r=3+Math.round(T/0.3*8);b.globalAlpha=1-T/0.3;for(let a=0;a<28;a++){const an=a/28*Math.PI*2;R(b,Math.round(sx+Math.cos(an)*r),Math.round(sy0+Math.sin(an)*r),1,1,'#ffffff');}b.globalAlpha=1;}\n"
    "  for(let k=5;k<dy-2;k+=5)R(b,sx-1,sy0-k,2,2,'rgba(255,255,255,0.7)');\n"
    "  if(T<0.88){b.globalAlpha=T>0.76?(0.88-T)/0.12:1;const x0=sx-5,y0=sy-1;HAND.forEach((row,j)=>{for(let i=0;i<row.length;i++){const ch=row[i];if(ch!=='.')R(b,x0+i,y0+j,1,1,ch==='O'?'#13306b':'#ffffff');}});b.globalAlpha=1;}}\n"
    "function drawStoreBusy(){")
rep("{id:'driveway',name:'DRIVEWAY',     area:'suburbs',h:260, time:90,value:1,   stars:[30,55,80]",
    "{id:'driveway',name:'DRIVEWAY',     area:'suburbs',h:260, time:90,value:1,   stars:[25,50,70]")
rep("{id:'culdesac',name:'CUL-DE-SAC',   area:'suburbs',h:460, time:70,value:1.3, stars:[35,60,85]",
    "{id:'culdesac',name:'CUL-DE-SAC',   area:'suburbs',h:460, time:70,value:1.3, stars:[30,50,70]")
rep("{id:'gardens', name:'GARDENS',      area:'suburbs',h:360, time:65,value:1.15,stars:[35,60,85]",
    "{id:'gardens', name:'GARDENS',      area:'suburbs',h:360, time:65,value:1.15,stars:[30,50,70]")
rep("button('cont',30,146,120,20,save.pro?'gold':'purple',save.pro?'PREMIUM: +15 SECONDS':'WATCH AD: +15 SECONDS',()=>{if(save.pro)go();else IAP.ad('continue',{t:2.5,reward:0,onDone:go});sfx('click');});",
    "{const fr=FTUE_NEW&&!save.pro&&(save.freeCont||0)<2;button('cont',30,146,120,20,save.pro?'gold':fr?'green':'purple',save.pro?'PREMIUM: +15 SECONDS':fr?'FREE: +15 SECONDS':'WATCH AD: +15 SECONDS',()=>{if(save.pro)go();else if(fr){save.freeCont=(save.freeCont||0)+1;persist();go();}else IAP.ad('continue',{t:2.5,reward:0,onDone:go});sfx('click');});}")
open(f,'w',encoding='utf-8').write(s)
print('p164 lab first-job pack: clock on first move, fingertip hint, 70% three stars on jobs 1-3, two free continues')
