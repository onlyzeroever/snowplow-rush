import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
# Weekend events, the system (plan doc "Weekend events", task 94). Off on live until a date is added to /events.json.
# - Schedule: /events.json on the website (no app update per event): [{"id":"2026-11-20","kind":"blizzard","start":"2026-11-20T00:00","end":"2026-11-23T00:00"}],
#   times in the player's own time. Preview any time with ?event=blizzard (or presents): a 72-hour test event from now.
# - A banner on the Jobs map (from job 4, like the dailies) opens the event card: timer, a 10-step track, 3 event jobs, the prize.
# - Event jobs are the player's own recent jobs with a twist: Blizzard = 60% more falling snow and double coins; Present Hunt = 4x presents.
#   Every machine works. They also count as normal runs (stars, best).
# - Each event run earns flakes: % cleared + 10 per star + 20 for a clean sweep. 10 steps (30 ... 950 flakes): coins sized to your best job,
#   gems (10/15/20/25) and the prize at 950 (about 12 runs). The first prizes are trails that already exist; new prizes need art.
# - Analytics: event_join, event_milestone, event_prize.

rep("function overlayOpen(){",
r"""const EVENT_DEFS={
  blizzard:{name:'BLIZZARD WEEKEND',sub:'HEAVY SNOW, DOUBLE COINS',mod:{snow:1.6,value:2},prize:{trail:'rainbow',gems:100},col:'#9fd8ff'},
  presents:{name:'PRESENT HUNT',sub:'PRESENTS EVERYWHERE',mod:{presents:4},prize:{trail:'sparkle',gems:60},col:'#ff8fc8'}};
const EV_STEPS=[30,80,150,230,320,420,530,650,780,950],EV_REW=[{c:2},{g:10},{c:3},{g:15},{c:4},{g:20},{c:5},{g:25},{c:8},{prize:1}];
let EVENTS=[],evOpen=false;
(function evLoad(){const q=new URLSearchParams(location.search).get('event');
  if(q&&EVENT_DEFS[q]){const t=Date.now();EVENTS.push({id:'test-'+q,kind:q,start:t-1000,end:t+72*3600e3,test:true});return;}
  try{fetch('/events.json?d='+new Date().toDateString().replace(/ /g,''),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(a=>{if(!Array.isArray(a))return;
    for(const e of a){if(!e||!EVENT_DEFS[e.kind])continue;const st=new Date(e.start).getTime(),en=new Date(e.end).getTime();if(isFinite(st)&&isFinite(en)&&en>st)EVENTS.push({id:String(e.id||e.start),kind:e.kind,start:st,end:en});}}).catch(()=>{});}catch(e){}})();
function evNow(){const t=Date.now();return EVENTS.find(e=>t>=e.start&&t<e.end)||null;}
function evSave(ev){if(!save.ev||save.ev.id!==ev.id)save.ev={id:ev.id,flakes:0,got:0,runs:0};return save.ev;}
function evJobs(ev){const open=[];LEVELS.forEach((L,i)=>{if(!L.tool&&!L.boss&&L.id!=='farm_old'&&levelOpen(i))open.push(i);});if(!open.length)return [0];
  const top=Math.max(...open.map(i=>AREA_SEQ.indexOf(LEVELS[i].area))),pool=open.filter(i=>AREA_SEQ.indexOf(LEVELS[i].area)>=top-1);
  let h=0;for(const ch of ev.id+ev.kind)h=(h*31+ch.charCodeAt(0))>>>0;const out=[];for(let k=0;k<pool.length&&out.length<3;k++){const i=pool[(h+k*7)%pool.length];if(!out.includes(i))out.push(i);}
  for(const i of pool)if(out.length<3&&!out.includes(i))out.push(i);return out;}
function evBuild(idx,opts){const ev=opts&&opts.event?EVENTS.find(e=>e.id===opts.event):null;if(!ev)return buildLevel(idx);
  const L=LEVELS[idx],m=EVENT_DEFS[ev.kind].mod,c=Object.assign({},L);if(m.snow)c.snowfall=L.snowfall*m.snow;if(m.presents)c.presents=Math.round(L.presents*m.presents);if(m.value)c.value=L.value*m.value;
  LEVELS[idx]=c;try{return buildLevel(idx);}finally{LEVELS[idx]=L;}}
function evReward(k){const r=EV_REW[k];if(r.c){const a=runPay()*r.c;save.coins+=a;return '+'+fmt(a)+' COINS';}if(r.g){save.gems=(save.gems||0)+r.g;return '+'+r.g+' GEMS';}
  const ev=EVENTS.find(e=>e.id===save.ev.id),pz=EVENT_DEFS[ev?ev.kind:'blizzard'].prize;
  if(pz.trail&&!save.trails[pz.trail]){save.trails[pz.trail]=true;track('event_prize',{event:save.ev.id,prize:pz.trail});return 'PRIZE: '+TRAILS.find(t=>t.id===pz.trail).name+' TRAIL!';}
  save.gems=(save.gems||0)+pz.gems;track('event_prize',{event:save.ev.id,prize:'gems'});return 'PRIZE: +'+pz.gems+' GEMS';}
function evRun(pct,stars,allClear){const ev=EVENTS.find(e=>e.id===run.event);if(!ev)return null;const e=evSave(ev),f=Math.round(pct)+stars*10+(allClear?20:0);
  if(!e.runs)track('event_join',{event:ev.id,kind:ev.kind});e.runs++;e.flakes+=f;const msgs=[];
  while(e.got<EV_STEPS.length&&e.flakes>=EV_STEPS[e.got]){msgs.push(evReward(e.got));e.got++;track('event_milestone',{event:ev.id,step:e.got,flakes:e.flakes});}
  if(msgs.length)showToast(msgs[msgs.length-1],'#ffd23f');return {f,total:e.flakes,msgs};}
function drawEvBanner(){const ev=evNow();if(!ev||!dailyOn())return;const d=EVENT_DEFS[ev.kind],e=save.ev&&save.ev.id===ev.id?save.ev:{flakes:0,got:0},y=22,left=(ev.end-Date.now())/1000;
  btn('evbanner',4,y,172,14,()=>{evOpen=true;sfx('click');});R(b,4,y,172,14,K);R(b,5,y+1,170,12,'#13306b');R(b,5,y+1,Math.round(170*Math.min(1,e.flakes/EV_STEPS[9])),12,'#1d4f9a');
  b.drawImage(SPR.star,8,y+3);text(b,d.name,19,y+4,d.col,{outline:null});text(b,fmtDur(left)+' LEFT',172,y+4,'#ffffff',{align:'right',outline:null});
  if(e.got<10&&!e.runs){R(b,169,y-2,6,6,K);R(b,170,y-1,4,4,'#e8283f');}}
function drawEvent(){const ev=evNow();if(!ev){evOpen=false;return;}const d=EVENT_DEFS[ev.kind],e=evSave(ev),x=8,y=24,w=164,h=262;
  b.fillStyle='rgba(11,24,56,0.82)';b.fillRect(0,0,W,H);panel(x,y,w,h,'#13306b',d.col);
  text(b,d.name,W/2,y+7,d.col,{align:'center',scale:2});text(b,d.sub,W/2,y+23,'#ffffff',{align:'center',outline:null});text(b,'ENDS IN '+fmtDur((ev.end-Date.now())/1000),W/2,y+32,'#9fc0e8',{align:'center',outline:null});
  // the track: 10 steps
  const ty=y+46;R(b,x+8,ty,w-16,8,K);R(b,x+9,ty+1,w-18,6,'#0b1838');R(b,x+9,ty+1,Math.round((w-18)*Math.min(1,e.flakes/EV_STEPS[9])),6,d.col);
  for(let k=0;k<10;k++){const px=x+9+Math.round((w-18)*EV_STEPS[k]/EV_STEPS[9])-3;R(b,px,ty+10,6,6,K);R(b,px+1,ty+11,4,4,k<e.got?'#ffd23f':k===9?'#ff8fc8':'#4f6fa0');}
  text(b,e.flakes+' / '+EV_STEPS[9]+' FLAKES',W/2,ty+20,'#ffffff',{align:'center',outline:null});
  const nx=e.got<10?EV_REW[e.got]:null,pz=d.prize,pzName=pz.trail&&!save.trails[pz.trail]?TRAILS.find(t=>t.id===pz.trail).name+' TRAIL':pz.gems+' GEMS';
  text(b,nx?('NEXT AT '+EV_STEPS[e.got]+': '+(nx.c?fmt(runPay()*nx.c)+' COINS':nx.g?nx.g+' GEMS':'THE PRIZE')):'ALL STEPS DONE!',W/2,ty+30,'#9fd8ff',{align:'center',outline:null});
  text(b,'PRIZE: '+pzName,W/2,ty+40,'#ff8fc8',{align:'center',outline:null});
  text(b,'EVENT JOBS',x+10,ty+54,'#9fc0e8',{outline:null});
  evJobs(ev).forEach((i,k)=>{const L=LEVELS[i],ry=ty+64+k*30;card(x+8,ry,w-16,26,'#eef3fb','#9fc0e8');text(b,L.name,x+14,ry+5,'#13306b',{outline:null});
    text(b,(save.stars[i]||0)+' OF 3 STARS',x+14,ry+15,'#4f6fa0',{outline:null});button('evp'+k,x+w-58,ry+5,44,16,'orange','PLAY',()=>{evOpen=false;startLevelUI(i,{event:ev.id});});});
  text(b,'FLAKES: % CLEARED + 10 A STAR',W/2,y+h-38,'#9fc0e8',{align:'center',outline:null});
  button('evdone',W/2-36,y+h-26,72,18,'blue','DONE',()=>{evOpen=false;sfx('click');});}
function overlayOpen(){""")
rep("||(offerOpen&&state==='map'));}","||(offerOpen&&state==='map')||(evOpen&&state==='map'));}")
rep("if(offerOpen&&state==='map'&&!storyOpen)drawOffer();","if(offerOpen&&state==='map'&&!storyOpen)drawOffer();\n  if(evOpen&&state==='map'&&!offerOpen&&!storyOpen)drawEvent();")
# banner on the map
rep("const by=NAV_Y-22;","drawEvBanner();\n  const by=NAV_Y-22;")
# event runs
rep("G=buildLevel(idx);P={x:G.start.x","G=evBuild(idx,opts);P={x:G.start.x")
rep("challenge:opts&&opts.challenge||null};","challenge:opts&&opts.challenge||null,event:opts&&opts.event||null};")
rep("function startLevel(idx,opts){offerOpen=null;","function startLevel(idx,opts){offerOpen=null;evOpen=false;")
rep("if(stars===3)earnSkinFor(L.id);persist();}","if(stars===3)earnSkinFor(L.id);if(run.event)run.res.ev=evRun(pct,stars,allClear);persist();}")
# results: flakes line (in place of the daily line)
rep("if(run.dailyDone&&dailyReadyCount()>0){b.drawImage(SPR.cal,26,py+166);text(b,'DAILY DONE! CLAIM ON JOBS',38,py+168,'#7fe08a',{outline:null});}",
    "if(r.ev){b.drawImage(SPR.star,26,py+166);text(b,'+'+r.ev.f+' FLAKES  ('+Math.min(r.ev.total,EV_STEPS[9])+'/'+EV_STEPS[9]+')',38,py+168,'#9fd8ff',{outline:null});}\n    else if(run.dailyDone&&dailyReadyCount()>0){b.drawImage(SPR.cal,26,py+166);text(b,'DAILY DONE! CLAIM ON JOBS',38,py+168,'#7fe08a',{outline:null});}")
rep("button('retry',18,py+176,46,22,'orange','RETRY',()=>startLevelUI(G.idx,run.challenge?{challenge:run.challenge}:null));",
    "button('retry',18,py+176,46,22,'orange','RETRY',()=>startLevelUI(G.idx,run.challenge?{challenge:run.challenge}:run.event&&evNow()&&evNow().id===run.event?{event:run.event}:null));")

open(f,'w',encoding='utf-8').write(s)
print('p136 weekend events: schedule from /events.json (or ?event=), map banner from job 4, event card with 10-step track, 3 event jobs with a twist, flakes, prize; event_join/milestone/prize')
