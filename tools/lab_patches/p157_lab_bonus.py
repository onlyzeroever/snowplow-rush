# LAB rev 3b (Alex + Lloyd, Nov 20 23:16-23:54):
#  - Random spawns for what you hunt (golden presents, lost chicks, stray sheep) change every run, through the same
#    fairness checks; what shapes the course stays fixed so jobs stay learnable.
#    Tests stay repeatable: in test mode the seed is window.__LABSEED (default 0).
#  - Bonus twists: a player who is cruising (two 3-star finishes without a bad run in between) gets the area's twist
#    on the next plain job as a BONUS TWIST (bigger gold gift). Never while struggling (a run under 2 stars resets it),
#    never in Suburbs, on boss or Wild Ride jobs, events, challenges or missions.
#  - Avalanche: boulders tumble down ahead of the wave; their shadows show where they roll; a hit stuns you and the
#    wave gains on you.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)

# ---- random spawns ----
rep("function labPost(g){const M=MODES[g.def.mode];g.lab={};",
    "function labPost(g){const M=MODES[g.def.mode];g.lab={rs:TEST_MODE?(window.__LABSEED|0):((Math.random()*1e9)|0)};")
# Alex, 23:57: "random spawns I'm not sure" -> random only for what you hunt (golden presents, lost chicks, stray
# sheep); what shapes the course (pens, power boxes, buried cars, gates, forts, shelters, penguin families) stays put.
rep("post(g){const S=g.lab,rn=srng(hashS(g.def.id)+61),n=5,","post(g){const S=g.lab,rn=srng(hashS(g.def.id)+(g.lab.rs||0)+61),n=5,")
rep("    for(const f of S.fam){let q=null;const far=Math.max(170,Math.min(320,g.ph*0.12));for(let tr=0;tr<80&&!q;tr++){const c=labSpot(g,10,10,0,g.ph,rn,",
    "    const rc=srng(hashS(g.def.id)+(g.lab.rs||0)+43);for(const f of S.fam){let q=null;const far=Math.max(170,Math.min(320,g.ph*0.12));for(let tr=0;tr<80&&!q;tr++){const c=labSpot(g,10,10,0,g.ph,rc,")
rep("    for(let j=0;j<ns;j++){const pn=S.pens[j%S.pens.length];let q=null;",
    "    const rq=srng(hashS(g.def.id)+(g.lab.rs||0)+19);for(let j=0;j<ns;j++){const pn=S.pens[j%S.pens.length];let q=null;")
rep(",c=labSpot(g,10,8,0,g.ph,rn,{near:{x:pn.cx,y:pn.cy,r0:110,r1},",",c=labSpot(g,10,8,0,g.ph,rq,{near:{x:pn.cx,y:pn.cy,r0:110,r1},")

# ---- bonus twists ----
rep("if(!ev){const ta=(opts&&opts.twist)||twistOf(idx),mk2=ta&&TWISTS[ta];if(!mk2)return buildLevel(idx);const L=LEVELS[idx],c=Object.assign({},L);\n    c.mode=mk2;c.twist=ta;c.teach=twistJobs(ta)[0]===idx;",
    "if(!ev){let ta=(opts&&opts.twist)||twistOf(idx),bon=false;if(!ta&&labBonusDue(idx,opts)){ta=LEVELS[idx].area;bon=true;}const mk2=ta&&TWISTS[ta];if(!mk2)return buildLevel(idx);const L=LEVELS[idx],c=Object.assign({},L);\n    c.mode=mk2;c.twist=ta;c.teach=!bon&&twistJobs(ta)[0]===idx;c.bonus=bon?1:0;if(bon){save.labCruise=0;track('lab_bonus_twist',{job:L.id,twist:mk2});}")
rep("  run.res={pct,stars,bonus,timeBonus,allClear,t:0,starsPlayed:0};sfx(allClear?'win':'end');",
    "  run.res={pct,stars,bonus,timeBonus,allClear,t:0,starsPlayed:0};if(PROTO&&!run.event&&!run.mission&&!L.mode){if(stars>=3)save.labCruise=(save.labCruise||0)+1;else if(stars<2)save.labCruise=0;}sfx(allClear?'win':'end');")
rep("const c=Math.max(1,Math.round(labUnit()*5));earn(c);","const c=Math.max(1,Math.round(labUnit()*(G.def.bonus?7:5)));earn(c);")
rep("text(b,(G.def.teach?'NEW! ':'')+M.name,W/2,y+5,M.col,{align:'center',scale:2});",
    "if(G.def.bonus){panel(44,y-14,92,13,'#5c3a00','#ffd23f');text(b,'BONUS TWIST!',W/2,y-11,'#ffd23f',{align:'center',outline:null});}text(b,(G.def.teach?'NEW! ':'')+M.name,W/2,y+5,M.col,{align:'center',scale:2});")
rep("function labRes(label,n,of){const M=labM();run.labRes={name:M?M.name:'',label,n,of,gift:!!(run.lab&&run.lab.gift)};}",
    "function labRes(label,n,of){const M=labM();run.labRes={name:M?M.name:'',label:(G.def.bonus?'BONUS ':'')+label,n,of,gift:!!(run.lab&&run.lab.gift)};}")

# ---- avalanche: tumbling rocks ----
rep("    else if(A.ph==='wave'){A.fy+=(A.spd||S.spd)*dt;",
    "    else if(A.ph==='wave'){A.fy+=(A.spd||S.spd)*dt;A.rt=(A.rt||0)-dt;if(A.rt<=0&&(A.rk||[]).length<6){A.rt=rnd(0.35,0.7);(A.rk=A.rk||[]).push({x:rnd(12,G.pw-12),y:A.fy+rnd(4,14),vx:rnd(-14,14),vy:(A.spd||S.spd)*rnd(1.4,1.75),r:Math.round(rnd(4,7)),h:4,vh:rnd(20,50),an:Math.random()*6,d:0});}")
rep("    if(A.ph==='calm'){A.t-=dt;if(A.t<=0&&run.time>8){A.ph='warn';",
    "    avRocks(dt,tid,A);\n    if(A.ph==='calm'){A.t-=dt;if(A.t<=0&&run.time>8){A.ph='warn';")
rep("R(b,0,y-90,W,2,'#9fb4d8');}\n    if(A.buried>0){b.fillStyle='#e8f0fa';pixCircle(b,Math.round(P.x),Math.round(P.y+2),17);",
    "R(b,0,y-90,W,2,'#9fb4d8');}\n    for(const rk of A.rk||[]){if(rk.y<cy-20||rk.y>cy+VIEW_H+20)continue;const x=Math.round(rk.x),y=Math.round(rk.y),hy=Math.round(rk.y-rk.h),r=rk.r;R(b,x-r,y+r-2,r*2+1,3,'rgba(27,31,59,0.3)');\n"
    "      b.fillStyle=K;pixCircle(b,x,hy,r+1);b.fillStyle='#7a869c';pixCircle(b,x,hy,r);b.fillStyle='#9aa6ba';pixCircle(b,x-1,hy-1,Math.max(1,r-2));b.fillStyle='#c6ccd6';pixCircle(b,x-Math.round(r*0.4),hy-Math.round(r*0.45),Math.max(1,Math.round(r*0.3)));"
    "const ca=rk.an;R(b,Math.round(x+Math.cos(ca)*r*0.55),Math.round(hy+Math.sin(ca)*r*0.55),2,1,'#4a5068');R(b,Math.round(x+Math.cos(ca+2.2)*r*0.5),Math.round(hy+Math.sin(ca+2.2)*r*0.5),1,2,'#4a5068');}\n"
    "    if(A.buried>0){b.fillStyle='#e8f0fa';pixCircle(b,Math.round(P.x),Math.round(P.y+2),17);")
rep("how:['NOW AND THEN THE MOUNTAIN LETS','GO. AT THE SIREN A WALL OF SNOW','RUSHES DOWN THE MAP: DRIVE AWAY','FROM IT OR DUCK INTO A ROCK','SHELTER. CAUGHT? YOU GET BURIED.'],",
    "how:['AT THE SIREN A WALL OF SNOW','RUSHES DOWN THE MAP: DRIVE AWAY','FROM IT OR DUCK INTO A ROCK','SHELTER. DODGE THE TUMBLING','BOULDERS. CAUGHT? YOU GET BURIED.'],")

rep("loadSave();save.sess=(save.sess||0)+1;",r"""// ================= LAB rev 3b (Nov 20) =================
function labBonusDue(idx,opts){if(!PROTO)return false;const L=LEVELS[idx];if(!L||L.boss||L.tool||!TWISTS[L.area])return false;if(opts&&(opts.event||opts.challenge||opts.mission))return false;
  if(new URLSearchParams(location.search).has('notwist')||twistOf(idx))return false;if(window.__BONUS)return true;if(TEST_MODE&&!window.__CRUISE)return false;return (save.labCruise||0)>=2;}
function avRocks(dt,tid,A){if(!A.rk||!A.rk.length)return;const fp=footprint(tid,P.x,P.y,P.f);
  for(const rk of A.rk){rk.x=clamp(rk.x+rk.vx*dt,6,G.pw-6);rk.y+=rk.vy*dt;rk.d+=rk.vy*dt;rk.an+=rk.vy*dt/Math.max(3,rk.r);rk.vh-=210*dt;rk.h+=rk.vh*dt;
    if(rk.h<=0){rk.h=0;rk.vh=Math.abs(rk.vh)*0.55+rnd(12,28);if(rk.y>camY-10&&rk.y<camY+VIEW_H+10){labBurst(rk.x,rk.y,3,'snow',30);if(Math.random()<0.4)sfx('bump',0,{vol:0.18,rate:0.55+Math.random()*0.2});}}
    const box={x:rk.x-rk.r,y:rk.y-rk.r,w:rk.r*2,h:rk.r*2};let o=null;for(const ob of G.obstacles)if(overlap(box,ob)){o=ob;break;}
    if(rk.h<7&&tid!=='ufo'&&overlap(fp,box)){if(!(P.inv>0)){hit('hz',SPILL_HAZARD);addFloat(P.x,P.y-26,'ROCK!','#ff9aa8',0.9);}rk.dead=1;}
    else if(o||rk.d>240||rk.y>G.ph-4)rk.dead=1;
    if(rk.dead){for(let k=0;k<8;k++)particles.push({x:rk.x,y:rk.y,vx:rnd(-40,40),vy:rnd(-30,20),z:2,vz:rnd(15,40),life:0.45,t:0,kind:'clump'});}}
  A.rk=A.rk.filter(rk=>!rk.dead);}
loadSave();save.sess=(save.sess||0)+1;""")
open(f,'w',encoding='utf-8').write(s)
print('p157 lab rev 3b: hunted things move each run, bonus twists for cruising players, avalanche boulders')
