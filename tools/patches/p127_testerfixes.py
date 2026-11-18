import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Tester feedback, Nov 18:
# 1. Trophies with a progress bar (Dressed to Plow showed 5/5 but never paid out) are now checked whenever you're back on
#    the map or open the trophies, not only at the moment of a purchase.
# 2. The job card's machine picker includes your Wild Rides (it only cycled the regular machines).
# 3. UFO: drawn above everything (it went under cars and roofs); hovers with a gentle drift everywhere (balance for floating
#    over every obstacle); thrown snowballs and snowball shots can hit it.
# 4. Upgrades screen says when a Wild Ride is in use that the upgrades go to your best machine (looked like a reset).
rep("function award(id){",
    "function checkTrophyProg(){if(!save||!save.ach)return;for(const a of ACH){if(save.ach[a.id])continue;const p=trophyProg(a.id);if(p&&p[1]>0&&p[0]>=p[1])award(a.id);}}\nfunction award(id){")
rep("function goMap(){","function goMap(){checkTrophyProg();")
rep("button('trophies',137,2,20,17,'gold',null,()=>{trophiesOpen=true;","button('trophies',137,2,20,17,'gold',null,()=>{checkTrophyProg();trophiesOpen=true;")
# 2. picker over every machine and ride you own
rep("if(open&&save.tool>0&&!missionOn(i)){const u=useIdx(),tu=TOOLS[u],n=save.tool+1;",
    "if(open&&save.tool>0&&!missionOn(i)){const u=useIdx(),tu=TOOLS[u],own=[];for(let j=0;j<TOOLS.length;j++)if(owns(j))own.push(j);const pi=Math.max(0,own.indexOf(u)),on=own.length;")
rep("button('jtl',23,178,17,16,'blue',null,()=>equip((u+n-1)%n));","button('jtl',23,178,17,16,'blue',null,()=>equip(own[(pi+on-1)%on]));")
rep("button('jtr',140,178,17,16,'blue',null,()=>equip((u+1)%n));","button('jtr',140,178,17,16,'blue',null,()=>equip(own[(pi+1)%on]));")
# 3a. UFO above everything
rep("ents.push({base:fp.y+fp.h,draw:()=>{drawRig(b,tid,P.x","let ufoTop=null;const pdraw=()=>{drawRig(b,tid,P.x")
rep("R(b,sx,sy,1,1,front?'#ffffff':'#ffe27a');}}}});","R(b,sx,sy,1,1,front?'#ffffff':'#ffe27a');}}};if(tid==='ufo')ufoTop=pdraw;else ents.push({base:fp.y+fp.h,draw:pdraw});")
rep("  // snowballs in flight\n","  if(ufoTop)ufoTop();\n  // snowballs in flight\n")
# 3b. UFO hovers: a gentle drift everywhere (ice no longer matters to it)
rep("  if(onIce&&tid!=='snowcat'&&tid!=='icebreaker'){",
    "  if(tid==='ufo'){const k=Math.min(1,dt*UFO_GRIP);P.vx+=(tvx-P.vx)*k;P.vy+=(tvy-P.vy)*k;if(!run.hoverShown){run.hoverShown=true;addFloat(P.x,P.y-22,'HOVERING: IT DRIFTS!','#7fe08a',1.4);}}\n"
    "  else if(onIce&&tid!=='snowcat'&&tid!=='icebreaker'){")
rep("if(P.stun>0&&!onIce){P.vx=0;P.vy=0;}","if(P.stun>0&&(!onIce||tid==='ufo')){P.vx=0;P.vy=0;}")
rep("const BASE_TOOLS=10;","const BASE_TOOLS=10;\nconst UFO_GRIP=3.2;   // how fast the UFO's speed follows your finger (ice is 1.4; ground machines are instant)")
# 3c. snowballs are in the air too
rep("if(b.t>=b.dur){if(tid!=='ufo'&&overlap(pr,{x:b.x1-6,y:b.y1-5,w:12,h:10}))","if(b.t>=b.dur){if(overlap(pr,{x:b.x1-6,y:b.y1-5,w:12,h:10}))")
rep("        if(tid!=='ufo'&&overlap(pr,br)){s2.dead=true;hit('hz',SPILL_HAZARD*0.5);","        if(overlap(pr,br)){s2.dead=true;hit('hz',SPILL_HAZARD*0.5);")
# 4. upgrades screen: say where a ride's upgrades go
rep("  woodBg();drawHeaderGems(2,2,50);drawHeaderCoins(W-74,2,72);sign('UPGRADES',22);",
    "  woodBg();drawHeaderGems(2,2,50);drawHeaderCoins(W-74,2,72);sign('UPGRADES',22);\n"
    "  {const u=useIdx();if(u>=BASE_TOOLS){const ride=TOOLS[u],m=TOOLS[save.tool],mn=SHORT_NAME[m.id]||m.name,rn=SHORT_NAME[ride.id]||ride.name;let t=rn+' USES YOUR '+mn+' UPGRADES';if(textW(t)>164)t=rn+' USES THE '+mn+\"'S\";if(textW(t)>164)t='YOUR RIDE USES THESE';R(b,8,36,164,9,'rgba(19,48,107,0.85)');text(b,t,W/2,37,'#ffd23f',{align:'center',outline:null});}}")
# 5. the road fee says it's once per winter (tolls reset with each New Winter, which testers didn't expect)
rep("const why=jobLockReason(i);b.drawImage(SPR.lock,W/2-4,180);text(b,why,W/2,192,'#ff9aa8',{align:'center',outline:null});",
    "const why=jobLockReason(i);b.drawImage(SPR.lock,W/2-4,180);text(b,why==='ROAD FEE'?'ROAD FEE, ONCE EACH WINTER':why,W/2,192,'#ff9aa8',{align:'center',outline:null});")
open(f,'w',encoding='utf-8').write(s)
print('p127 tester fixes: trophy progress, ride picker, UFO on top + hover + snowballs, ride upgrade note')
