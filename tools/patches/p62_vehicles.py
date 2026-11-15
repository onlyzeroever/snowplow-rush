import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)

# ---------------------------------------------------------------------------------------------
# VEHICLE PASS (Alex, Nov 15):
#  - from the Snowcat on, no starting blade wider than ~3.5x the body; their power is speed + value + perks.
#    Width upgrades on the big machines are a flat +25% (Super Plow keeps its +30%): wing blades.
#  - the width upgrade is drawn as hinged WING BLADES either side of the base blade, so an upgraded machine
#    visibly grows wings instead of one very long plank.
#  - PUSHER: a proper wide snow pusher with a curled lip, end fins and a push bar (no longer a recoloured shovel).
#  - BLOWER: a walk-behind snow blower: auger housing, engine block, a chute with a deflector, and a plume of
#    snow thrown off to the chute side while you clear.
# ---------------------------------------------------------------------------------------------
rep("  {id:'snowcat',name:'SNOWCAT',    cost:6.5e6,  width:52, speed:88, value:9},","  {id:'snowcat',name:'SNOWCAT',    cost:6.5e6,  width:44, speed:92, value:9.5},")
rep("  {id:'rotary', name:'ROTARY BLOWER',cost:1.8e7, width:56, speed:98, value:12.5},","  {id:'rotary', name:'ROTARY BLOWER',cost:1.8e7, width:48, speed:104,value:13.5},")
rep("  {id:'monster',name:'MONSTER TRUCK',cost:2.4e7, width:64, speed:104,value:16,","  {id:'monster',name:'MONSTER TRUCK',cost:2.4e7, width:46, speed:108,value:17,")
rep("  {id:'jet',    name:'JET TRUCK',  cost:7e7,     width:58, speed:114,value:21,","  {id:'jet',    name:'JET TRUCK',  cost:7e7,     width:42, speed:120,value:22,")
rep("  {id:'mech',   name:'MEGA MECH',  cost:2e8,     width:72, speed:104,value:28,","  {id:'mech',   name:'MEGA MECH',  cost:2e8,     width:50, speed:106,value:29,")
rep("  {id:'dragon', name:'SNOW DRAGON',cost:6e8,     width:54, speed:124,value:37,","  {id:'dragon', name:'SNOW DRAGON',cost:6e8,     width:38, speed:130,value:38,")
rep("  {id:'ufo',    name:'UFO',        cost:1.8e9,   width:70, speed:132,value:49,","  {id:'ufo',    name:'UFO',        cost:1.8e9,   width:48, speed:136,value:50,")
rep("  if(tid==='super'){scap=1.15;wcap=1.3;nxt=TOOLS[i+1].cost;}",
    "  if(tid==='super'){scap=1.15;wcap=1.3;nxt=TOOLS[i+1].cost;}\n  else if(i>5){const n=TOOLS[i+1];scap=(i<BASE_TOOLS-1&&n)?Math.max(1.06,0.97*n.speed/t.speed):1.15;wcap=1.25;nxt=(i<BASE_TOOLS-1&&n)?n.cost:t.cost*(i<BASE_TOOLS?4:1.5);}")
# wing blades: the part of the blade beyond the machine's own base width is drawn as hinged wings
rep("  R(g,x,y,bw,bt,K);R(g,x+1,y+1,bw-2,bt-2,fill);R(g,x+1,y+1,bw-2,1,hi);R(g,x+1,y+bt-2,bw-2,1,dark);\n  if(tid==='super'&&!c.deco)",
    "  {const T0=TOOLS[toolIdx(tid)],base=T0?Math.min(bw,T0.width*2):bw,wing=Math.floor((bw-base)/2);\n    if(wing>=3){const bx=cx-Math.floor(base/2);for(const [wx,ww] of [[x,wing],[bx+base,wing]]){R(g,wx,y+1,ww,bt-1,K);R(g,wx+1,y+2,ww-2,bt-3,fill);R(g,wx+1,y+2,ww-2,1,hi);}\n      R(g,bx-2,y,3,bt,K);R(g,bx-1,y+1,1,bt-2,'#8793a8');R(g,bx+base-1,y,3,bt,K);R(g,bx+base,y+1,1,bt-2,'#8793a8');R(g,bx,y,base,bt,K);R(g,bx+1,y+1,base-2,bt-2,fill);R(g,bx+1,y+1,base-2,1,hi);R(g,bx+1,y+bt-2,base-2,1,dark);}\n    else{R(g,x,y,bw,bt,K);R(g,x+1,y+1,bw-2,bt-2,fill);R(g,x+1,y+1,bw-2,1,hi);R(g,x+1,y+bt-2,bw-2,1,dark);}}\n  if(tid==='super'&&!c.deco)")
# kid tools: the pusher is a deeper scoop (4px), the blower a machine
rep("const th=tid==='blower'?6:3;const ks=kidOverride||kidSet();","const th=tid==='blower'?6:tid==='pusher'?4:3;const ks=kidOverride||kidSet();")
rep("const th=tid==='blower'?6:3;const r=kidBladeRect(Math.round(x),Math.round(y),f,bw,th);","const th=tid==='blower'?6:tid==='pusher'?4:3;const r=kidBladeRect(Math.round(x),Math.round(y),f,bw,th);")
rep("function drawToolHead(g,x,y,w,h,tid,si){const c=skinPal(tid,si),fill=c.x,dark=c.xd,hz=w>h;",
    """function drawToolHead(g,x,y,w,h,tid,si){const c=skinPal(tid,si),fill=c.x,dark=c.xd,hz=w>h;
  if(tid==='pusher'&&!c.deco){const cx=x+(w>>1),cy=y+(h>>1);R(g,x,y,w,h,K);R(g,x+1,y+1,w-2,h-2,fill);if(hz){R(g,x+1,y+1,w-2,1,'#ffffff');R(g,x+1,y+h-2,w-2,1,dark);R(g,x-1,y-1,3,h+2,K);R(g,x+w-2,y-1,3,h+2,K);R(g,x,y,1,h,fill);R(g,x+w-1,y,1,h,fill);R(g,cx-4,y+h,8,2,K);R(g,cx-3,y+h,6,1,'#8793a8');}
    else{R(g,x+1,y+1,1,h-2,'#ffffff');R(g,x+w-2,y+1,1,h-2,dark);R(g,x-1,y-1,w+2,3,K);R(g,x-1,y+h-2,w+2,3,K);R(g,x,y,w,1,fill);R(g,x,y+h-1,w,1,fill);}return;}
  if(tid==='blower'&&!c.deco){const cx=x+(w>>1),cy=y+(h>>1),on=Math.floor(tNow*12)%2;R(g,x,y,w,h,K);R(g,x+1,y+1,w-2,h-2,fill);
    if(hz){for(let i=x+2+on;i<x+w-2;i+=3)R(g,i,y+2,1,h-4,K);R(g,x+1,y+1,w-2,1,'#ff9aa8');R(g,cx-4,y-4,8,5,K);R(g,cx-3,y-3,6,3,'#55607a');R(g,cx+2,y-7,3,5,K);R(g,cx+3,y-6,1,4,fill);R(g,cx+3,y-8,5,2,K);R(g,cx+4,y-8,3,1,fill);}
    else{for(let i=y+2+on;i<y+h-2;i+=3)R(g,x+2,i,w-4,1,K);R(g,x+1,y+1,1,h-2,'#ff9aa8');R(g,x-4,cy-4,5,8,K);R(g,x-3,cy-3,3,6,'#55607a');R(g,x-7,cy+2,5,3,K);R(g,x-6,cy+3,4,1,fill);}return;}""")
# the blower throws its snow off to the chute side in an arc, not both ways at random
rep("  if(tid==='blower'){particles.push({x:br.x+br.w/2,y:br.y+br.h/2,vx:(f===1||f===3)?rnd(-70,70):rnd(30,70)*(Math.random()<0.5?-1:1),vy:(f===1||f===3)?rnd(-15,15):0,z:2,vz:rnd(50,90),life:0.8,t:0,kind:'snow'});return;}",
    "  if(tid==='blower'){const side=(f===0||f===3)?1:-1;particles.push({x:br.x+br.w/2,y:br.y+br.h/2,vx:(f===0||f===2)?side*rnd(40,80):rnd(-12,12),vy:(f===1||f===3)?side*rnd(40,80):rnd(-12,12),z:4,vz:rnd(55,95),life:0.85,t:0,kind:'snow'});if(Math.random()<0.6)particles.push({x:br.x+br.w/2,y:br.y+br.h/2,vx:(f===0||f===2)?side*rnd(20,50):rnd(-8,8),vy:(f===1||f===3)?side*rnd(20,50):rnd(-8,8),z:3,vz:rnd(40,70),life:0.7,t:0,kind:'snow'});return;}")
open(f,'w',encoding='utf-8').write(s)
s=open(f,encoding='utf-8').read()
rep("window.__SR={frostOf,","window.__SR={drawRig,frostOf,")
open(f,'w',encoding='utf-8').write(s)
