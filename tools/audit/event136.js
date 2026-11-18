// p136 weekend events: schedule, banner, event card, event jobs with a twist, flakes, steps and prize. node tools/audit/event136.js
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errs = [];
  const page = async q => { const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.on('pageerror', e => errs.push(String(e)));
    await p.goto('http://127.0.0.1:8765/index6.html?test=1' + q); await p.waitForTimeout(900); return p; };
  const setup = `(()=>{save.privSeen=true;save.tut=true;save.story={suburbs:true,farm:true,city:true};save.fbRuns=8;save.dailyEver=true;save.dailySeen=todayKey();save.tool=4;save.use=4;for(let i=0;i<20;i++){save.stars[i]=2;save.best[i]=70;}storyOpen=null;goMap();return 1;})()`;
  const ids = p => p.evaluate(() => window.__UI.list().map(u => u.id || u));
  // no event: no banner
  let p = await page(''); await p.evaluate(c => window.__EV(c), setup); await p.waitForTimeout(400);
  const live = JSON.parse(await p.evaluate(() => window.__EV('JSON.stringify({n:EVENTS.length,on:!!evNow()})')));
  const fileN = JSON.parse(require('fs').readFileSync(__dirname + '/../../events.json', 'utf8')).length;
  ok(live.n === fileN, 'schedule file read: ' + live.n + ' event(s)');
  ok((await ids(p)).includes('evbanner') === live.on, 'banner only while an event is on (' + (live.on ? 'on now' : 'none on now') + ')');
  await p.context().close();
  // test event
  p = await page('&event=blizzard'); const EV = c => p.evaluate(c => window.__EV(c), c);
  await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=1;save.dailyEver=false;save.best=save.best.map(()=>0);save.dailySeen=todayKey();goMap();return 1;})()`); await p.waitForTimeout(400);
  ok(!(await ids(p)).includes('evbanner'), 'no banner in the first jobs (same rule as the dailies)');
  await EV(setup); await p.waitForTimeout(400);
  ok((await ids(p)).includes('evbanner'), 'banner on the map from job 4');
  await p.evaluate(() => window.__UI.press('evbanner')); await p.waitForTimeout(300);
  const u2 = await ids(p); ok(['evp0', 'evp1', 'evp2', 'evdone'].every(x => u2.includes(x)), 'event card shows 3 jobs and DONE');
  const jobs = JSON.parse(await EV(`JSON.stringify(evJobs(evNow()).map(i=>({id:LEVELS[i].id,open:levelOpen(i),boss:!!LEVELS[i].boss,ride:!!LEVELS[i].tool})))`));
  ok(jobs.length === 3 && jobs.every(j => j.open && !j.boss && !j.ride), 'event jobs are open, not bosses or ride jobs ' + JSON.stringify(jobs.map(j => j.id)));
  const st = JSON.parse(await EV(`(()=>{window.__HOLD=1;const i=evJobs(evNow())[0];startLevel(i,{event:evNow().id});return JSON.stringify({ev:run.event,snow:G.def.snowfall/LEVELS[i].snowfall,val:G.def.value/LEVELS[i].value,restored:LEVELS[i]!==G.def&&LEVELS[i].id===G.def.id,idx:G.idx===i});})()`));
  ok(st.ev && Math.abs(st.snow - 1.4) < 0.01 && st.val === 2 && st.restored && st.idx, 'blizzard job: 40% more snow, double coins, the job itself untouched ' + JSON.stringify(st));
  // Alex, Nov 19: the blizzard has to feel like one - gusts push the machine, squalls drop snow
  const gz = JSON.parse(await EV(`(()=>{const out={gust:G.def.gust,squall:G.def.squall,phases:{}};run.contUsed=true;run.time=99;const x0=P.x;let maxDx=0;
    for(let i=0;i<30*14;i++){update(1/30);if(run.bz)out.phases[run.bz.phase]=1;maxDx=Math.max(maxDx,Math.abs(P.x-x0));}out.maxDx=Math.round(maxDx);out.squalls=!!run.squallT;return JSON.stringify(out);})()`));
  ok(gz.gust === 1 && gz.squall > 0 && gz.phases.calm && gz.phases.warn && gz.phases.blow, 'blizzard has calm, warning and gust phases, plus squalls ' + JSON.stringify(gz));
  ok(gz.maxDx >= 10, 'a gust pushes the machine sideways (' + gz.maxDx + ' px)');
  const r1 = JSON.parse(await EV(`(()=>{const g0=save.gems||0;G.cleared=Math.round(G.clearable*0.7);run.contUsed=true;run.time=0.01;update(0.05);return JSON.stringify({ended:run.ended,ev:run.res&&run.res.ev,got:save.ev.got,dg:(save.gems||0)-g0});})()`));
  ok(r1.ended && r1.ev && r1.ev.f === 70 + 10 * 2, 'flakes = % cleared + 10 a star ' + JSON.stringify(r1.ev));
  ok(r1.got === 2 && r1.dg >= 10, 'first two steps paid (coins, 10 gems)');
  const r2 = JSON.parse(await EV(`(()=>{save.trails.rainbow=false;delete save.trails.rainbow;save.ev.flakes=940;save.ev.got=9;const i=evJobs(evNow())[1];startLevel(i,{event:evNow().id});G.cleared=Math.round(G.clearable*0.5);run.contUsed=true;run.time=0.01;update(0.05);
    return JSON.stringify({got:save.ev.got,trail:!!save.trails.rainbow,msgs:run.res.ev.msgs});})()`));
  ok(r2.got === 10 && r2.trail, 'prize at 950 flakes: the Rainbow trail ' + JSON.stringify(r2.msgs));
  const r3 = JSON.parse(await EV(`(()=>{const g0=save.gems||0;save.ev.got=9;save.ev.flakes=900;evRun.call(null,60,0,false);return JSON.stringify({dg:(save.gems||0)-g0});})()`));
  ok(r3.dg === 100, 'prize already owned: 100 gems instead');
  const r4 = JSON.parse(await EV(`(()=>{const i=evJobs(evNow())[0];startLevel(i);return JSON.stringify({ev:run.event,same:G.def===LEVELS[i]});})()`));
  ok(r4.ev === null && r4.same, 'normal runs are normal');
  ok(errs.length === 0, 'no errors ' + JSON.stringify(errs.slice(0, 3)));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await b.close(); process.exit(fails ? 1 : 0);
})();
