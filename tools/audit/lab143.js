// Prototype lab check: every event and area twist starts, runs, draws without errors; screenshots for review.
// node tools/audit/lab143.js [page=lab6.html] [outDir=/tmp/lab]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const page = process.argv[2] || 'lab6.html', out = process.argv[3] || '/tmp/lab'; fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/' + page + '?test=1&lab=1&review=all'); await p.waitForTimeout(1200);
  const EV = c => p.evaluate(c => window.__EV(c), c);
  await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=8;save.bzTips=9;window.__HOLD=1;state='map';labOpen=true;return 1;})()`);
  await EV('(draw(),1)'); await p.screenshot({ path: out + '/lab_menu.png' });
  await EV('(labTab=1,draw(),1)'); await p.screenshot({ path: out + '/lab_twists.png' });
  await EV("(labTab=0,labPick='nightshift',draw(),1)"); await p.screenshot({ path: out + '/lab_pick.png' });
  const kinds = JSON.parse(await EV('JSON.stringify(Object.keys(EVENT_DEFS))')), twists = JSON.parse(await EV('JSON.stringify(Object.keys(TWISTS))'));
  const res = [];
  for (const k of [...kinds.map(k => 'ev:' + k), ...twists.map(a => 'tw:' + a)]) {
    const r = await EV(`(()=>{const k=${JSON.stringify(k)},tw=k.startsWith('tw:'),key=k.slice(3);const ids=tw?twistJobs(key):LAB_JOBS[key].map(id=>LEVELS.findIndex(L=>L.id===id));const i=ids[tw?0:1]>=0?ids[tw?0:1]:ids[0];
      labOpen=false;startLevel(i,tw?{twist:key}:{event:'lab-'+key});run.moved=true;const t0=run.time;const id0=inputDir,vy=G.start.y<G.ph/2?0.75:-0.75;let f=0;
      for(;f<30*7;f++){inputDir=()=>({x:Math.sin(f/25)*0.7,y:vy,m:1});P.inv=Math.min(P.inv,0.1);update(1/30);}inputDir=id0;draw();
      const flags=Object.keys(G.def).filter(x=>x.startsWith('ev_')||x==='twist'||x==='gust'||x==='gustMild'||x==='fogMild');
      return JSON.stringify({k,job:LEVELS[i].id,time:[t0,Math.round(run.time)],flags,earned:Math.round(run.earned),pct:Math.round(G.cleared/G.clearable*100),
        extra:{throwers:G.hazards.filter(h=>h.kind==='thrower').length,chasers:G.hazards.filter(h=>h.kind==='chaser').length,cannons:G.hazards.filter(h=>h.kind==='cannon').length,clocks:(G.clocks||[]).length,gold:G.gold?G.gold.reduce((a,v)=>a+v,0):0,mud:G.mud?G.mud.reduce((a,v)=>a+v,0):0,stars:(run.stars||[]).length,hail:(run.hail||[]).length,night:!!G.night,blade:bladeCells()}});})()`);
    res.push(JSON.parse(r)); await p.screenshot({ path: `${out}/${k.replace(':', '_')}.png`, clip: { x: 0, y: 0, width: 390, height: 700 } });
  }
  for (const r of res) console.log(r.k.padEnd(16), r.job.padEnd(12), JSON.stringify(r.time), r.pct + '%', JSON.stringify(r.extra), r.flags.join(','));
  // live game unaffected: no lab without ?lab
  const p2 = await (await b.newContext()).newPage(); await p2.goto('http://127.0.0.1:8765/' + page + '?test=1'); await p2.waitForTimeout(900);
  const off = await p2.evaluate(() => window.__EV('JSON.stringify({proto:PROTO,tw:twistOf(LEVELS.findIndex(L=>L.id==="lane")),labEvents:EVENTS.filter(e=>e.lab).length})'));
  console.log('without ?lab:', off); console.log('errors', JSON.stringify(errs.slice(0, 5)));
  await b.close();
})();
