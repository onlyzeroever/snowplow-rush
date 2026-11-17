import sys, os
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Two new regular machines (plan doc decision 2, prices from sim v10 / ladder3):
#   FRONT LOADER after the Super Plow: 48 wide, speed 84, x7.5 coins, 2.5M. Arrives around the Theme Park.
#   ICEBREAKER after the Rotary, the North finale: 62 wide, speed 132, x18 coins, 180M. 14% faster than a maxed Rotary;
#   tracks, so no sliding on ice, and like the Rotary it shrugs off half the bump stun.
# The Super Plow's upgrades now point at the Loader (like the early machines). The Snowcat and Rotary keep today's caps
# and upgrade prices. Saves move their machine indexes across (tv 3).
DRAW=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'p126_newmachines_draw.js'),encoding='utf-8').read()
rep("  {id:'super',  name:'SUPER PLOW', cost:680000, width:40, speed:74, value:6.5},\n",
    "  {id:'super',  name:'SUPER PLOW', cost:680000, width:40, speed:74, value:6.5},\n"
    "  {id:'loader', name:'FRONT LOADER',cost:2.5e6, width:48, speed:84, value:7.5},\n")
rep("  {id:'rotary', name:'ROTARY BLOWER',cost:1.8e7, width:48, speed:104,value:13.5},\n",
    "  {id:'rotary', name:'ROTARY BLOWER',cost:1.8e7, width:48, speed:104,value:13.5},\n"
    "  {id:'icebreaker',name:'ICEBREAKER',cost:1.8e8, width:62, speed:132,value:18},\n")
rep("const BASE_TOOLS=8;","const BASE_TOOLS=10;")
# upgrade caps: an explicit table where the formula doesn't fit
rep("if(tid==='super'){scap=1.15;wcap=1.3;nxt=TOOLS[i+1].cost;}",
    "if(MCAPS[tid]){const q=MCAPS[tid];scap=q[0];wcap=q[1];nxt=q[2]||TOOLS[i+1].cost;}")
rep("function mspec(tid){","const MCAPS={super:[0.97*84/74,0.95*48/40],loader:[1.062,1.10],rotary:[1.15,1.25,7.2e7]};  // [speed cap, width cap, upgrade price base]\nfunction mspec(tid){")
# saves: machine indexes by id (tv 3)
rep("  if(!s.tv){if(s.tool>=6)s.tool+=2;if(s.use!=null&&s.use>=6)s.use+=2;if(s.gold!=null&&s.gold>=6)s.gold+=2;s.tv=2;}",
    "  if(!s.tv){if(s.tool>=6)s.tool+=2;if(s.use!=null&&s.use>=6)s.use+=2;if(s.gold!=null&&s.gold>=6)s.gold+=2;s.tv=2;}\n"
    "  if(s.tv===2){const OLD=['shovel','pusher','blower','tractor','truck','super','snowcat','rotary','monster','jet','mech','dragon','ufo'],mv=i=>(Number.isInteger(i)&&i>=0&&i<OLD.length)?Math.max(0,TOOLS.findIndex(t=>t.id===OLD[i])):i;\n"
    "    if(Number.isInteger(s.tool)&&s.tool>=8&&s.tool<OLD.length){s.rides=(s.rides&&typeof s.rides==='object')?s.rides:{};for(let j=8;j<=s.tool;j++)s.rides[OLD[j]]=true;s.tool=7;if(s.mlv&&typeof s.mlv===\'object\')for(let j=8;j<OLD.length;j++){const q=s.mlv[OLD[j]];if(q&&typeof q===\'object\'){q.speed=0;q.size=0;}}}  // rides used to imply the whole ladder up to the Rotary\n"
    "    s.tool=mv(s.tool);if(s.use!=null)s.use=mv(s.use);if(s.gold!=null)s.gold=mv(s.gold);s.tv=3;}")
rep("save.mlv={};if(refund>0){save.coins+=refund;save.upgRefund=refund;}}}}catch(e){}save.tv=2;sanitizeSave();}",
    "save.mlv={};if(refund>0){save.coins+=refund;save.upgRefund=refund;}}}}catch(e){}save.tv=3;sanitizeSave();}")
rep("s={v:6,tv:2,tut:true,coins:P.coins,tool:ix(P.m),use:ix(P.m),","s={v:6,tv:3,tut:true,coins:P.coins,tool:ix(P.m),use:ix(P.m),")
# art: the two sprites, their blades, no snow pile on the Icebreaker's bow wave
rep("const VDRAW={","// ---------------- FRONT LOADER + ICEBREAKER ----------------\n"+DRAW+"\nconst VDRAW={")
rep("const VDRAW={tractor:","const VDRAW={loader:drawLoader,icebreaker:drawIcebreaker,tractor:")
rep("const VSPEC={tractor:","const VSPEC={loader:{hw:13,hh:22,bt:8},icebreaker:{hw:14,hh:24,bt:7},tractor:")
rep("function drawVBlade(g,cx,y,bw,bt,tid,c){if(bt<=0)return;const x=cx-Math.floor(bw/2);c=c||skinPal(tid);",
    "function drawVBlade(g,cx,y,bw,bt,tid,c){if(bt<=0)return;const x=cx-Math.floor(bw/2);c=c||skinPal(tid);\n"
    "  if(tid==='loader'){bladeLoader(g,cx,y,bw,bt,c);return;}if(tid==='icebreaker'){bladeIcebreaker(g,cx,y,bw,bt,c,c.fr);return;}")
rep("drawVBlade(g,ox,oy-sp.hh-sp.bt,bw,sp.bt,tid,tid==='rotary'?Object.assign({},c,{fr}):c);if(pl>0&&sp.bt&&tid!=='rotary')",
    "drawVBlade(g,ox,oy-sp.hh-sp.bt,bw,sp.bt,tid,tid==='rotary'||tid==='icebreaker'?Object.assign({},c,{fr}):c);if(pl>0&&sp.bt&&tid!=='rotary'&&tid!=='icebreaker')")
# skins: 5 each (+ gold paint, added for every machine)
rep("const SKIN_NAMES={snowcat:","const SKIN_NAMES={loader:['CLASSIC','HARBOUR BLUE','LIME','NIGHT SHIFT','BUBBLEGUM'],icebreaker:['CLASSIC','POLAR BLUE','COASTGUARD','STEALTH','AURORA'],snowcat:")
rep("const SKIN_PAL={\n  snowcat:",
    "const SKIN_PAL={\n"
    "  loader:[{b:'#f5b82e',l:'#ffe07a',d:'#c4861a'},{b:'#3f86d6',l:'#7fbaf2',d:'#2a5fa8'},{b:'#7ccf3a',l:'#b6f07a',d:'#4f9a22'},{b:'#3a3f52',l:'#5f6880',d:'#23273a'},{b:'#ff6fb0',l:'#ffb0d6',d:'#c23a7c'}],\n"
    "  icebreaker:[{b:'#d8343c',l:'#ff6a6a',d:'#9a1f2a'},{b:'#2f6fc8',l:'#6fa8f0',d:'#1f4a8a'},{b:'#f07a1a',l:'#ffb060',d:'#b8501a'},{b:'#2a2a36',l:'#55607a',d:'#1b1f3b'},{b:'#2fb59a',l:'#7fe8d0',d:'#1d7a68'}],\n"
    "  snowcat:")
rep("const SKIN_EARN_JOB={snowcat:'blackrun',","const SKIN_EARN_JOB={loader:'containers',icebreaker:'icefield',snowcat:'blackrun',")
# feel: engine note, tracks on ice, heavy like the Rotary
rep("tid==='rotary'?0.6:0.75)+0.45*sr);","tid==='rotary'?0.6:tid==='icebreaker'?0.5:tid==='loader'?0.8:0.75)+0.45*sr);")
rep("onIce&&tid==='snowcat'&&!run.iceShown){","onIce&&(tid==='snowcat'||tid==='icebreaker')&&!run.iceShown){")
rep("if(onIce&&tid!=='snowcat'){","if(onIce&&tid!=='snowcat'&&tid!=='icebreaker'){")
rep("(tool().id==='rotary'?0.5:1);shake=0.25*red;","(tool().id==='rotary'||tool().id==='icebreaker'?0.5:1);shake=0.25*red;")
open(f,'w',encoding='utf-8').write(s)
print('p126 Front Loader + Icebreaker')
