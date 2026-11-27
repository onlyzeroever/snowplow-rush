# Weekend events run every weekend on their own (Alex, Nov 27: "I'm up for them running whenever... how would the
# pros do it?"). The pro pattern for casual games: the same rhythm every week (Friday 00:00 to Monday 00:00 in the
# player's own time, like the Blizzard Weekend), a rotation rather than pure random (a shuffled order where nothing
# repeats until every event has had its turn, and never the same event two weekends running), a live-ops calendar
# that can override any weekend, and "what's next" always on show.
#  - Auto events: computed from the date, so every player gets the same event the same weekend with no file edits.
#    Each weekend has its own id ('w2026-11-27'): its own progress, prize and Event Pass.
#  - events.json still wins: a dated entry replaces the auto event for any weekend it overlaps (New Year's
#    Blizzard), and {"kind":"off", start, end} pauses events (the kill switch). Explicit entries can also run midweek.
#  - Whatever events the build has join the rotation: 2 in the app and on the website (Blizzard Weekend, Present
#    Hunt), all 10 in the lab. An event def with auto:false stays out of it.
#  - Between events the map's event slot says what's next: "NEXT: PRESENT HUNT   IN 2D 4H" (same place and size as the
#    event banner, so nothing moves when an event starts).
#  - ?event=<kind> previews and ?test=1 runs (the bot, the audits) see no auto events unless &autoev is added.
# Live web game, app and lab.
import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b_,cnt=1):
    global s;assert s.count(a)==cnt,(a[:90],s.count(a));s=s.replace(a,b_)
rep("let EVENTS=[],evOpen=false;", "let EVENTS=[],evOpen=false,EV_TEST=false;const EV_OFF=[];")
rep("if(q&&EVENT_DEFS[q]){const t=Date.now();EVENTS.push({id:'test-'+q,kind:q,start:t-1000,end:t+72*3600e3,test:true});return;}",
    "if(q&&EVENT_DEFS[q]){const t=Date.now();EV_TEST=true;EVENTS.push({id:'test-'+q,kind:q,start:t-1000,end:t+72*3600e3,test:true});return;}")
rep("for(const e of a){if(!e||!EVENT_DEFS[e.kind])continue;",
    "for(const e of a){if(e&&e.kind==='off'){const s0=new Date(e.start).getTime(),e0=new Date(e.end).getTime();if(isFinite(s0)&&isFinite(e0))EV_OFF.push({start:s0,end:e0});continue;}if(!e||!EVENT_DEFS[e.kind])continue;")
rep("function evNow(){const t=Date.now();return EVENTS.find(e=>t>=e.start&&t<e.end)||null;}",
    "function evAutoOn(){return !EV_TEST&&(!TEST_MODE||/[?&]autoev\\b/.test(location.search));}\n"
    "function evFri(t){const d=new Date(t);d.setHours(0,0,0,0);d.setDate(d.getDate()-((d.getDay()+2)%7));return d;}\n"
    "function evKindFor(wk){const K=Object.keys(EVENT_DEFS).filter(k=>EVENT_DEFS[k].auto!==false),n=K.length;if(!n)return null;if(n<3)return K[wk%n];"
    "const bag=c=>{let a=(Math.imul(c,2654435761)^0x9e3779b9)>>>0;const r=()=>{a=(a+0x6D2B79F5)>>>0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};"
    "const o=K.slice();for(let i=n-1;i>0;i--){const j=Math.floor(r()*(i+1));const x=o[i];o[i]=o[j];o[j]=x;}return o;};"
    "const c=Math.floor(wk/n),o=bag(c);if(o[0]===bag(c-1)[n-1]){const x=o[0];o[0]=o[1];o[1]=x;}return o[wk-c*n];}\n"
    "function evAutoAt(fri){const k=evKindFor(Math.floor(Date.UTC(fri.getFullYear(),fri.getMonth(),fri.getDate())/864e5/7));if(!k)return null;"
    "return {id:'w'+fri.getFullYear()+'-'+String(fri.getMonth()+1).padStart(2,'0')+'-'+String(fri.getDate()).padStart(2,'0'),kind:k,start:fri.getTime(),"
    "end:new Date(fri.getFullYear(),fri.getMonth(),fri.getDate()+3).getTime(),auto:true,plus:true};}\n"
    "function evAutoAdd(t){if(!evAutoOn())return;const f=evFri(t);for(const fr of [f,new Date(f.getFullYear(),f.getMonth(),f.getDate()+7)]){const a=evAutoAt(fr);if(a&&!EVENTS.some(e=>e.id===a.id))EVENTS.push(a);}}\n"
    "function evLive(e){return !e.auto||(!EVENTS.some(x=>!x.auto&&x.start<e.end&&x.end>e.start)&&!EV_OFF.some(o=>o.start<e.end&&o.end>e.start));}\n"
    "function evNow(){const t=Date.now();evAutoAdd(t);return EVENTS.find(e=>!e.auto&&t>=e.start&&t<e.end)||EVENTS.find(e=>e.auto&&t>=e.start&&t<e.end&&evLive(e))||null;}\n"
    "function evNext(){const t=Date.now();evAutoAdd(t);return EVENTS.filter(e=>e.start>t&&evLive(e)).sort((a,b)=>a.start-b.start)[0]||null;}")
rep("function drawEvBanner(){const ev=evNow();if(!ev||!dailyOn())return;",
    "function drawEvBanner(){const ev=evNow();if(!dailyOn())return;"
    "if(!ev){const nx=evNext();if(!nx||!EVENT_DEFS[nx.kind])return;const d=EVENT_DEFS[nx.kind],y=22,dt=(nx.start-Date.now())/1000;"
    "R(b,4,y,172,14,K);R(b,5,y+1,170,12,'#0b1838');text(b,'NEXT: '+d.name,9,y+4,'#9fc0e8',{outline:null});"
    "text(b,'IN '+fmtDur(dt),172,y+4,'#ffffff',{align:'right',outline:null});return;}")
open(f,'w',encoding='utf-8').write(s)
