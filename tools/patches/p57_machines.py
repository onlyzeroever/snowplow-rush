import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# TWO NEW MACHINES after the Super Plow, so the late areas get something new to buy and grow into:
#   SNOWCAT (bought around the Ski Resort): a piste groomer on tracks, wide front blade, rear tiller comb.
#   ROTARY BLOWER (around the Mountain Pass): a rotary snow blower truck, auger drum up front, a chute
#   throwing a plume of snow. Base machines are now 8; the Wild Rides move up two places.
# Old saves: anyone already owning a Wild Ride (tool index >= 6) is moved up two places and keeps both new
# machines as a thank-you (the chain is linear). save.tv=2 marks a migrated save.
# Wild Rides get stronger so each one still beats the Rotary Blower (they're the aspirational rides).
# ---------------------------------------------------------------------------------------------
rep("""  {id:'super',  name:'SUPER PLOW', cost:680000, width:40, speed:74, value:6.5},""",
"""  {id:'super',  name:'SUPER PLOW', cost:680000, width:40, speed:74, value:6.5},
  {id:'snowcat',name:'SNOWCAT',    cost:6.5e6,  width:52, speed:88, value:9},
  {id:'rotary', name:'ROTARY BLOWER',cost:1.8e7, width:56, speed:98, value:12.5},""")
rep("""  {id:'monster',name:'MONSTER TRUCK',cost:6e6,   width:42, speed:78, value:9,    winter:2, trick:'CRUSHES JUNK'},
  {id:'jet',    name:'JET TRUCK',  cost:2e7,     width:36, speed:82, value:12.5, winter:3, trick:'BLASTS A CONE'},
  {id:'mech',   name:'MEGA MECH',  cost:6e7,     width:46, speed:74, value:17,   winter:4, trick:'SHOVES CRATES'},
  {id:'dragon', name:'SNOW DRAGON',cost:2e8,     width:30, speed:92, value:23,   winter:5, trick:'MELTS A STRIP'},
  {id:'ufo',    name:'UFO',        cost:6e8,     width:44, speed:100,value:31,   winter:6, trick:'FLOATS, BEAMS COWS'},""",
"""  {id:'monster',name:'MONSTER TRUCK',cost:2.4e7, width:64, speed:104,value:16,   winter:2, trick:'CRUSHES JUNK'},
  {id:'jet',    name:'JET TRUCK',  cost:7e7,     width:58, speed:114,value:21,   winter:3, trick:'BLASTS A CONE'},
  {id:'mech',   name:'MEGA MECH',  cost:2e8,     width:72, speed:104,value:28,   winter:4, trick:'SHOVES CRATES'},
  {id:'dragon', name:'SNOW DRAGON',cost:6e8,     width:54, speed:124,value:37,   winter:5, trick:'MELTS A STRIP'},
  {id:'ufo',    name:'UFO',        cost:1.8e9,   width:70, speed:132,value:49,   winter:6, trick:'FLOATS, BEAMS COWS'},""")
rep("const BASE_TOOLS=6;","const BASE_TOOLS=8;")
rep("else if(i===BASE_TOOLS-1){scap=1.15;wcap=1.3;nxt=t.cost*4;}","else if(i===BASE_TOOLS-1){scap=1.15;wcap=1.15;nxt=t.cost*4;}")
# the Super Plow keeps the upgrade headroom it always had (no nerf for anyone who maxed it)
rep("  if(i>=0&&i<BASE_TOOLS-1){const n=TOOLS[i+1];scap=0.97*n.speed/t.speed;wcap=0.95*n.width/t.width;nxt=n.cost;}",
    "  if(tid==='super'){scap=1.15;wcap=1.3;nxt=TOOLS[i+1].cost;}\n  else if(i>=0&&i<BASE_TOOLS-1){const n=TOOLS[i+1];scap=0.97*n.speed/t.speed;wcap=0.95*n.width/t.width;nxt=n.cost;}")
rep("const VSPEC={tractor:{hw:8,hh:12,bt:5},truck:{hw:10,hh:18,bt:6},super:{hw:12,hh:22,bt:7},",
    "const VSPEC={tractor:{hw:8,hh:12,bt:5},truck:{hw:10,hh:18,bt:6},super:{hw:12,hh:22,bt:7},snowcat:{hw:13,hh:21,bt:7},rotary:{hw:13,hh:23,bt:8},")
rep("const VDRAW={tractor:(g,ox,oy,fr,c)=>drawTractor(g,ox,oy,c),truck:drawTruck,super:drawSuper,",
    "const VDRAW={tractor:(g,ox,oy,fr,c)=>drawTractor(g,ox,oy,c),truck:drawTruck,super:drawSuper,snowcat:drawSnowcat,rotary:drawRotary,")
rep("tail=tid==='super'?14:tid==='dragon'?8:4;","tail=tid==='super'?14:tid==='snowcat'?8:tid==='rotary'?10:tid==='dragon'?8:4;")
# the rotary's 'blade' is an auger drum
rep("  if(tid==='dragon'){for(let i=x+1;i<x+bw-1;i+=3)R(g,i,y+bt-2,2,2,'#e0c08a');return;}",
    "  if(tid==='dragon'){for(let i=x+1;i<x+bw-1;i+=3)R(g,i,y+bt-2,2,2,'#e0c08a');return;}\n  if(tid==='rotary'){R(g,x,y,bw,bt,K);R(g,x+1,y+1,bw-2,bt-2,fill);R(g,x+1,y+1,bw-2,1,hi);const ph=(c.fr||0)%2;for(let i=x+2+ph*2;i<x+bw-3;i+=4){R(g,i,y+2,2,bt-4,dark);R(g,i+1,y+2,1,1,hi);}R(g,x-1,y-1,3,bt+2,K);R(g,x+bw-2,y-1,3,bt+2,K);R(g,cx-4,y+bt,8,2,K);return;}")
# skins
rep("SKIN_NAMES={","SKIN_NAMES={snowcat:['CLASSIC','FOREST','NIGHT SHIFT','PISTE PATROL','GLACIER'],rotary:['CLASSIC','HIGHWAY','ARCTIC','INFERNO','CHROME'],")
rep("const SKIN_EARN_JOB={","const SKIN_EARN_JOB={snowcat:'blackrun',rotary:'summit',")
rep("const SKIN_PAL={","const SKIN_PAL={\n  snowcat:[{b:'#d8364b',l:'#ff7a8a',d:'#9c2a45',x:'#c6d0dc',xd:'#8793a8',xh:'#ffffff'},{b:'#2f8a4a',l:'#6fd07a',d:'#1f6a33',x:'#ffc727',xd:'#e29a1c',xh:'#ffe27a',deco:'stripe'},{b:'#1f2f5a',l:'#3f5fae',d:'#121c3a',x:'#c6d0dc',xd:'#8793a8',xh:'#ffffff',deco:'lights'},{b:'#ffc727',l:'#ffe27a',d:'#c98a12',x:'#2a2a36',xd:'#1b1f3b',xh:'#55607a',deco:'cross'},{b:'#e8f6ff',l:'#ffffff',d:'#9fd4f4',x:'#7ad3ff',xd:'#3f86d6',xh:'#d8f2ff',deco:'flake'}],\n  rotary:[{b:'#f07a1a',l:'#ffb060',d:'#b8501a',x:'#ffc727',xd:'#c98a12',xh:'#ffe27a'},{b:'#ffc727',l:'#ffe27a',d:'#c98a12',x:'#2a2a36',xd:'#1b1f3b',xh:'#55607a',deco:'chevron'},{b:'#f4f8ff',l:'#ffffff',d:'#9fb8d8',x:'#3f86d6',xd:'#2a5fa8',xh:'#7fbaf2',deco:'flake'},{b:'#2a2a36',l:'#55607a',d:'#1b1f3b',x:'#e03a4e',xd:'#a82639',xh:'#ff7a8a',deco:'flames'},{b:'#c6ccd6',l:'#ffffff',d:'#8793a8',x:'#e8eef7',xd:'#9aa6ba',xh:'#ffffff',deco:'chrome'}],")
KIT=r"""
// ---- SNOWCAT: tracks, cab, rear tiller comb (26x42 footprint)
function drawSnowcat(g,ox,oy,fr,c){const x=ox-13,y=oy-21,on=fr%2===0;
  for(const tx of [x,x+20]){R(g,tx,y+3,6,36,K);R(g,tx+1,y+4,4,34,'#3a3f52');for(let i=0;i<12;i++)R(g,tx+1,y+4+((i*3+(fr%3))%33),4,1,'#6a7088');R(g,tx+1,y+4,4,1,'#8793a8');}
  R(g,x+5,y+1,16,38,K);R(g,x+6,y+2,14,36,c.b);R(g,x+6,y+2,14,1,c.l);R(g,x+17,y+3,2,34,c.d);
  R(g,x+7,y+2,2,2,'#ffef7a');R(g,x+17,y+2,2,2,'#ffef7a');
  R(g,x+6,y+6,14,14,K);R(g,x+7,y+7,12,5,'#8fd3ff');R(g,x+8,y+7,3,2,'#d8f2ff');R(g,x+11,y+8,3,2,curHat().c);R(g,x+7,y+12,12,7,c.d);
  R(g,x+7,y+13,12,2,K);R(g,x+8,y+13,3,1,on?'#ffb43a':'#7a4a1a');R(g,x+12,y+13,2,1,'#ffef7a');R(g,x+15,y+13,3,1,on?'#7a4a1a':'#ffb43a');
  R(g,x+8,y+23,10,10,K);R(g,x+9,y+24,8,8,c.d);for(let i=0;i<4;i++)R(g,x+9,y+25+i*2,8,1,K);
  if(c.deco==='stripe'){R(g,x+12,y+2,2,36,'#ffc727');}else if(c.deco==='lights'){R(g,x+6,y+20,2,2,on?'#7ad3ff':'#2a5fa8');R(g,x+18,y+20,2,2,on?'#2a5fa8':'#7ad3ff');R(g,x+7,y+35,12,1,'#ff4a4a');}
  else if(c.deco==='cross'){R(g,x+11,y+24,4,8,'#e03a4e');R(g,x+9,y+26,8,4,'#e03a4e');}else if(c.deco==='flake'){R(g,x+12,y+23,2,10,'#ffffff');R(g,x+8,y+27,10,2,'#ffffff');R(g,x+10,y+25,6,6,'#7ad3ff');R(g,x+11,y+26,4,4,'#ffffff');}
  R(g,x+2,y+39,22,4,K);R(g,x+3,y+40,20,2,'#8793a8');for(let i=0;i<10;i++)R(g,x+3+i*2,y+42,1,2,K);}
// ---- ROTARY BLOWER: cab behind the auger, long body, chute throwing a plume (26x46 footprint)
function drawRotary(g,ox,oy,fr,c){const x=ox-13,y=oy-23,on=fr%2===0;
  for(const wy of [5,27,37]){R(g,x-2,y+wy,3,7,K);R(g,x-1,y+wy+1,1,5,PAL.X);R(g,x+25,y+wy,3,7,K);R(g,x+26,y+wy+1,1,5,PAL.X);}
  R(g,x,y,26,18,K);R(g,x+1,y+1,24,16,c.b);R(g,x+1,y+1,24,1,c.l);R(g,x+21,y+2,3,14,c.d);
  R(g,x+3,y+3,20,5,K);R(g,x+4,y+4,18,3,'#8fd3ff');R(g,x+5,y+4,3,2,'#d8f2ff');R(g,x+11,y+4,3,2,curHat().c);
  R(g,x+3,y+10,20,3,K);R(g,x+4,y+11,5,1,on?'#ffb43a':'#7a4a1a');R(g,x+10,y+11,6,1,'#ffef7a');R(g,x+17,y+11,5,1,on?'#7a4a1a':'#ffb43a');
  R(g,x+1,y+18,24,28,K);R(g,x+2,y+19,22,26,c.b);R(g,x+2,y+19,22,1,c.l);R(g,x+4,y+22,18,18,c.d);for(let i=0;i<5;i++)R(g,x+5,y+23+i*4,16,2,K);
  if(c.deco==='chevron'){for(let i=0;i<5;i++)R(g,x+2+i*5,y+43,3,2,'#2a2a36');}else if(c.deco==='flake'){R(g,x+12,y+24,2,12,'#ffffff');R(g,x+7,y+29,12,2,'#ffffff');}
  else if(c.deco==='flames'){for(const [a,b2,h2] of [[4,40,4],[8,38,6],[13,39,5],[17,37,7],[21,40,4]]){R(g,x+a,y+b2-h2+4,2,h2,'#f07a1a');R(g,x+a,y+b2,2,2,'#ffc727');}}else if(c.deco==='chrome'){R(g,x+2,y+19,3,26,'#ffffff');}
  // the chute, swinging between sides, and its plume
  R(g,x+21,y-3,4,8,K);R(g,x+22,y-2,2,6,c.x||'#ffc727');R(g,x+22,y-6,9,5,K);R(g,x+23,y-5,7,3,c.x||'#ffc727');R(g,x+29,y-7,3,4,K);
  const n=2+(c.pl||0);for(let i=0;i<n;i++){const px=x+33+i*3+(on?1:0),py=y-8+Math.round(i*1.6)+((i+fr)%2);R(g,px-1,py-1,4,4,PAL.w);R(g,px,py,3,2,PAL.W);}}
"""
rep("function drawSuper(g,ox,oy,fr,c){", KIT+"\nfunction drawSuper(g,ox,oy,fr,c){")
# rotary drum animates with the frame
rep("VDRAW[tid](g,ox,oy,fr,c);\n  drawVBlade(g,ox,oy-sp.hh-sp.bt,bw,sp.bt,tid,c);if(pl>0&&sp.bt)drawPile(",
    "VDRAW[tid](g,ox,oy,fr,tid==='rotary'?Object.assign({},c,{pl:Math.min(6,pl)}):c);\n  drawVBlade(g,ox,oy-sp.hh-sp.bt,bw,sp.bt,tid,tid==='rotary'?Object.assign({},c,{fr}):c);if(pl>0&&sp.bt&&tid!=='rotary')drawPile(")
# save migration: Wild Rides move up two places
rep("  if(s){\n  if(!s.v||s.v<6){","  if(s){\n  if(!s.tv){if(s.tool>=6)s.tool+=2;if(s.use!=null&&s.use>=6)s.use+=2;if(s.gold!=null&&s.gold>=6)s.gold+=2;s.tv=2;}\n  if(!s.v||s.v<6){")
rep("save.upgRefund=refund;}}}}catch(e){}}\nfunction persist(){","save.upgRefund=refund;}}}}catch(e){}save.tv=2;}\nfunction persist(){")
# engine note for the big new machines
rep("(tid==='tractor'?1.1:tid==='truck'?0.85:0.75)","(tid==='tractor'?1.1:tid==='truck'?0.85:tid==='snowcat'?0.66:tid==='rotary'?0.6:0.75)")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
rep("window.__SR={pineSprite,","window.__SR={drawToolIconTo,vehicleSprite,skinPal,pineSprite,")
open(f,'w',encoding='utf-8').write(s)

s=open(f,encoding='utf-8').read()
# signature feel. SNOWCAT: tracks grip on ice, no sliding. ROTARY: heavyweight, a bump stuns it half as long,
# and the chute throws a real plume of snow off to the side.
rep("  if(onIce){const k=Math.min(1,dt*1.4);","  if(onIce&&tid==='snowcat'&&!run.iceShown){run.iceShown=true;addFloat(P.x,P.y-22,'TRACKS: NO SLIDING','#9fd8ff',1.2);}\n  if(onIce&&tid!=='snowcat'){const k=Math.min(1,dt*1.4);")
rep("P.stun=(kind==='ob'?STUN_OB:STUN_HZ)*red;","P.stun=(kind==='ob'?STUN_OB:STUN_HZ)*red*(tool().id==='rotary'?0.5:1);")
rep("  if(tid==='blower'){particles.push(","  if(tid==='rotary'){const fx=(f===0||f===2)?br.x+br.w/2:br.x+br.w/2,fy=(f===0||f===2)?br.y+br.h/2:br.y+br.h/2,side=(f===0||f===3)?1:-1;particles.push({x:fx+rnd(-6,6),y:fy+rnd(-3,3),vx:(f===0||f===2)?side*rnd(55,95):rnd(-10,10),vy:(f===1||f===3)?side*rnd(55,95):rnd(-10,10),z:6,vz:rnd(60,100),life:0.9,t:0,kind:'snow'});return;}\n  if(tid==='blower'){particles.push(")
open(f,'w',encoding='utf-8').write(s)
