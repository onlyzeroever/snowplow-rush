import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Older phones, part 2 (Nov 16).
# 1. Starting a job builds it in one go: 130 ms on a desktop (330 ms for the biggest), so up to ~1.5 s on an older
#    phone with nothing on screen after the tap. Taps on PLAY / RETRY / RESTART now show a "getting ready" card at once
#    and the job is built on the next frame. (Code and tests that call startLevel directly are unchanged.)
rep("if(open)button('jlp'+i,x+w-34,y+9,30,16,'orange','PLAY',()=>startLevel(i));","if(open)button('jlp'+i,x+w-34,y+9,30,16,'orange','PLAY',()=>startLevelUI(i));")
rep("()=>{const k=jobInfo;jobInfo=-1;startLevel(k);}","()=>{const k=jobInfo;jobInfo=-1;startLevelUI(k);}")
rep("button('wkplay',40,200,100,22,'orange','PLAY',()=>{startLevel(d.i,{challenge:d.tid});});","button('wkplay',40,200,100,22,'orange','PLAY',()=>{startLevelUI(d.i,{challenge:d.tid});});")
rep("button('restart',45,135,90,20,'orange','RESTART',()=>startLevel(G.idx));","button('restart',45,135,90,20,'orange','RESTART',()=>startLevelUI(G.idx));")
rep("()=>startLevel(G.idx,run.challenge?{challenge:run.challenge}:null)","()=>startLevelUI(G.idx,run.challenge?{challenge:run.challenge}:null)")
rep("function startLevel(idx,opts){",
"""let pendingStart=null;
function startLevelUI(i,o){if(pendingStart)return;pendingStart={i,o,f:0,t:tNow};}
function runPendingStart(){if(!pendingStart||pendingStart.f<1)return false;const q=pendingStart;pendingStart=null;startLevel(q.i,q.o);return true;}
function drawLoading(){if(!pendingStart)return;pendingStart.f++;const L=LEVELS[pendingStart.i];b.fillStyle='rgba(11,24,56,0.72)';b.fillRect(0,0,W,H);
  panel(26,126,128,48,'#13306b','#9fd8ff');const nm=(L&&L.name)||'';text(b,nm,W/2,136,'#ffffff',{align:'center',scale:textW(nm,2)<=116?2:1});
  text(b,'GETTING THE PLOW READY',W/2,156,'#9fd8ff',{align:'center',outline:null});for(let k=0;k<3;k++)R(b,W/2-6+k*5,165,3,3,k===Math.floor(tNow*6)%3?'#ffd23f':'#4f6fa0');}
function startLevel(idx,opts){""")
rep("  if(!(TEST_MODE&&window.__HOLD))try{update(dt);",
    "  if(pendingStart&&runPendingStart())last=performance.now();\n  if(!(TEST_MODE&&window.__HOLD))try{update(dt);")
rep("ctx.imageSmoothingEnabled=false;ctx.drawImage(buf,0,0,W*KS,H*KS);","if(pendingStart)try{drawLoading();}catch(e){}ctx.imageSmoothingEnabled=false;ctx.drawImage(buf,0,0,W*KS,H*KS);")
rep("if(TEST_MODE)window.__STEP=(n,dt,dr)=>{for(let i=0;i<n;i++){","if(TEST_MODE)window.__STEP=(n,dt,dr)=>{if(pendingStart){pendingStart.f=1;runPendingStart();}for(let i=0;i<n;i++){")
# 2. Overhead sprites (aurora, lift line, tunnels, light strings...) were redrawn from scratch on every job start;
#    they only depend on their size, so they are cached.
rep("for(const p of D.over||[]){const f=OVERS[p[0]];if(f)g.over.push({spr:f(p[3],p[4]),sx:p[1],sy:p[2]});}",
    "for(const p of D.over||[]){const f=OVERS[p[0]];if(!f)continue;const ok=p[0]+'|'+p[3]+'|'+p[4];let sp=OVC.get(ok);if(!sp){sp=f(p[3],p[4]);OVC.set(ok,sp);}g.over.push({spr:sp,sx:p[1],sy:p[2]});}")
rep("function startLevel(idx,opts){","const OVC=new Map();\nfunction startLevel(idx,opts){")
# 3. The Treasure Book's cover, stitching and page texture (~1,000 one-pixel rectangles) are drawn once and reused.
old=s[s.index("  // leather cover, stitching, brass corners"):s.index("  if(n>=TREASURES.length)text(b,'COMPLETE!")]
static=old.replace("R(b,","R(g,").replace("brassCorner(","brassCornerG(g,").replace("text(b,","text(g,")
static=static.replace("dither(","ditherG(g,")
rep(old,"  b.drawImage(bookBg(),0,0);\n")
rep("function brassCorner(x,y,fx,fy){",
"""let BOOKBG=null;
function ditherG(g,x,y,w,h,col){g.fillStyle=col;for(let yy=y;yy<y+h;yy++)for(let xx=x+((yy-y)%2);xx<x+w;xx+=2)g.fillRect(xx,yy,1,1);}
function brassCornerG(g,x,y,fx,fy){for(let i=0;i<7;i++){R(g,x+fx*i,y,1,2,i<6?'#ffd23f':'#c98a12');R(g,x,y+fy*i,2,1,i<6?'#ffd23f':'#c98a12');}R(g,x,y,1,1,'#fff3a0');R(g,x+fx*2,y+fy*2,1,1,'#c98a12');}
function bookBg(){if(BOOKBG)return BOOKBG;const c=mk(W,H),g=c.getContext('2d');g.imageSmoothingEnabled=false;
"""+static+"""  return BOOKBG=c;}
function brassCorner(x,y,fx,fy){""")
open(f,'w',encoding='utf-8').write(s)
print('p115 loading card, cached overheads + book page')
