import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old));s=s.replace(old,new)
# Earning a Wild Ride (agreed Nov 15, built Nov 16): once you own the Rotary Blower, three PARTS of the next Wild Ride
# are hidden in jobs (a purple glint under the snow, like treasures). Find all three and its secret job opens as a
# MISSION played with the ride on loan; finish it with 2 stars or more and you keep the ride. Test drives, buying it,
# the Wild Ride Pass and New Winter remain the other ways in.

# a mission job is open when its ride's three parts are found and you don't own the ride yet
rep("const levelAvail=i=>(LEVELS[i].winter||1)<=winterNo();","const levelAvail=i=>(LEVELS[i].winter||1)<=winterNo()||missionOn(i);\nfunction missionOn(i){const L=LEVELS[i];return !!(L&&L.area==='secret'&&L.tool&&save&&save.parts&&(save.parts[L.tool]||0)>=3&&save.tool<toolIdx(L.tool));}")
rep("function starsNeeded(){let n=0;for(let i=0;i<NL;i++)if(levelAvail(i))n+=3;return n;}","function starsNeeded(){let n=0;for(let i=0;i<NL;i++)if((LEVELS[i].winter||1)<=winterNo())n+=3;return n;}")
rep("if(L.tool)return save.tool>=toolIdx(L.tool);","if(L.tool)return save.tool>=toolIdx(L.tool)||missionOn(i);")
# during a mission run the ride is on loan (no upgrades, like a test drive)
rep("function drv(){return !!(run&&run.drive&&state==='play'&&!run.ended);}","function drv(){return !!(run&&run.drive&&state==='play'&&!run.ended);}\nfunction msn(){return !!(run&&run.mission&&state==='play'&&!run.ended);}")
rep("function curLv(){if(chal()||drv())return ZERO_LV;","function curLv(){if(chal()||drv()||msn())return ZERO_LV;")
rep("if(drv())return TOOLS[toolIdx(run.drive)];","if(drv())return TOOLS[toolIdx(run.drive)];if(msn())return TOOLS[toolIdx(run.mission)];")
rep("((chal()||drv())?0:mLv(t.id).size)","((chal()||drv()||msn())?0:mLv(t.id).size)")
rep("save.boostNext=false;P.vx=0;P.vy=0;if(run.challenge&&G.driveKey)G.driveKey=null;","save.boostNext=false;P.vx=0;P.vy=0;if(run.challenge&&G.driveKey)G.driveKey=null;if(run.challenge)G.part=null;if(!run.challenge&&missionOn(idx)){run.mission=LEVELS[idx].tool;G.driveKey=null;G.part=null;_tc.k='';addFloat(P.x,P.y-30,'MISSION: 2 STARS KEEPS IT','#ffd23f',2.2);}")

# hide a part in a job now and then
rep("  g.driveKey=null;{const ri=nextRideIdx();","""  g.part=null;{const ri=nextRideIdx();if(ri>=0&&!LEVELS[idx].tool){const id2=TOOLS[ri].id,n=(save.parts||{})[id2]||0;if(n<3&&Math.random()<(n===0?0.45:0.3)){
    for(let k=0;k<300;k++){const x=16+Math.floor(Math.random()*(pw-32)),y=Math.floor(ph*0.15+Math.random()*ph*0.75);if(g.type[(y>>1)*cols+(x>>1)]!==T_BLOCK&&Math.hypot(x-g.start.x,y-g.start.y)>140){g.part={x,y,ri,found:false};break;}}}}}
  g.driveKey=null;{const ri=nextRideIdx();""")
rep("function checkDrive(br,dt){","""function checkPart(br){const pt=G.part;if(!pt||pt.found||!overlap(br,{x:pt.x-5,y:pt.y-5,w:10,h:10}))return;pt.found=true;const t=TOOLS[pt.ri];save.parts=save.parts||{};const n=(save.parts[t.id]||0)+1;save.parts[t.id]=n;
  sfx('trophy');buzz(30);for(let k=0;k<16;k++)particles.push({x:pt.x,y:pt.y,vx:rnd(-40,40),vy:rnd(-30,30),z:2,vz:rnd(40,80),life:0.8,t:0,kind:'spark'});
  if(n>=3){save.rideSeen=save.rideSeen||{};save.rideSeen[t.id]=true;const job=LEVELS.find(L=>L.tool===t.id);addFloat(pt.x,pt.y-16,'ALL 3 PARTS!','#c4a0f5',2);showToast('MISSION UNLOCKED: '+(job?job.name:'')+'!','#c4a0f5');}
  else{addFloat(pt.x,pt.y-16,'PART '+n+'/3','#c4a0f5',1.8);showToast(t.name+' PART '+n+' OF 3','#c4a0f5');}persist();}
let PART_ICON=null;function partIcon(){if(PART_ICON)return PART_ICON;const c=mk(12,12),g=c.getContext('2d');g.fillStyle=K;pixCircle(g,6,6,5);g.fillStyle='#9b5fd6';pixCircle(g,6,6,4);for(let k=0;k<8;k++){const a=k*Math.PI/4;R(g,Math.round(6+Math.cos(a)*5)-1,Math.round(6+Math.sin(a)*5)-1,2,2,'#c4a0f5');}g.fillStyle='#2a1d4a';pixCircle(g,6,6,1);return PART_ICON=c;}
function checkDrive(br,dt){checkPart(br);""")
# the part shows as a purple glint while buried, and as a cog once its snow is cleared
rep("  if(G.driveKey&&!G.driveKey.taken&&G.driveKey.y>top&&G.driveKey.y<bot){","  if(G.part&&!G.part.found&&G.part.y>top&&G.part.y<bot){const pt=G.part,ci=(pt.y>>1)*G.cols+(pt.x>>1),open=G.depth[ci]<CLEAR_T;if(open)b.drawImage(partIcon(),pt.x-6,pt.y-6);else if(Math.floor(tNow*1.6+pt.x)%3===0){R(b,pt.x,pt.y-2,1,5,'#e0c8ff');R(b,pt.x-2,pt.y,5,1,'#e0c8ff');R(b,pt.x,pt.y,1,1,'#9b5fd6');}}\n  if(G.driveKey&&!G.driveKey.taken&&G.driveKey.y>top&&G.driveKey.y<bot){")

# results: win the mission (2 stars) and the ride is yours
rep("function drawResults(){\n  ui=[];const r=run.res,t=r.t;","""function drawResults(){
  ui=[];const r=run.res,t=r.t;if(run.mission&&r.missionWon==null){r.missionWon=r.stars>=2;if(r.missionWon){grantRide(toolIdx(run.mission));}}""")
rep("  if(offerRide&&t>0.6){const ti=run.drove,","""  if(run.mission&&t>0.4){const T4=TOOLS[toolIdx(run.mission)];panel(14,18,152,24,r.missionWon?'#1f5a2a':'#3a1d6e',r.missionWon?'#7fe08a':'#c4a0f5');
    text(b,r.missionWon?'MISSION WON!':'MISSION: 2 STARS TO KEEP IT',W/2,22,'#ffd23f',{align:'center',outline:null});text(b,r.missionWon?'THE '+T4.name+' IS YOURS':'TRY AGAIN, THE '+T4.name+' WAITS',W/2,31,'#ffffff',{align:'center',outline:null});}
  if(offerRide&&t>0.6){const ti=run.drove,""")
# job card: mission banner instead of the machine picker
rep("  if(open&&save.tool>0){const u=useIdx(),tu=TOOLS[u],n=save.tool+1;R(b,22,177,136,18,K);","  if(missionOn(i)){R(b,22,177,136,18,K);R(b,23,178,134,16,'#3a1d6e');text(b,'MISSION: 2 STARS KEEPS THE '+TOOLS[toolIdx(L.tool)].name,W/2,183,'#ffd23f',{align:'center',outline:null});}\n  if(open&&save.tool>0&&!missionOn(i)){const u=useIdx(),tu=TOOLS[u],n=save.tool+1;R(b,22,177,136,18,K);")
# shop: show part progress for the next ride when it is not on sale yet
rep("['FIND A TEST DRIVE IN A JOB','TO UNLOCK THIS OFFER']","['PARTS FOUND: '+((save.parts||{})[TOOLS[nx].id]||0)+' OF 3 ('+TOOLS[nx].name+')','OR FIND A TEST DRIVE IN A JOB']")
# test hooks
rep("startLevel:(i,o)=>startLevel(i,o),endRound:a=>endRound(a),TOOLS};","startLevel:(i,o)=>startLevel(i,o),endRound:a=>endRound(a),missionOn:i=>missionOn(i),TOOLS};")
open(f,'w',encoding='utf-8').write(s)
