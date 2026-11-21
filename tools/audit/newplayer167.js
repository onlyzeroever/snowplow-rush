// p167 + switchable p164: ?newplayer gives a fresh save every time the link is opened (kept on reload), no event;
// &oldftue gives the live game's start (clock runs at once, old stars, no hand, ad continue)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 360, height: 640 } });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  await p.goto('http://127.0.0.1:8766/lab6.html?test=1&newplayer'); await p.waitForTimeout(900);
  const a = await EV(`(()=>{save.coins=5555;save.tut=true;persist();return JSON.stringify({key:SAVE_KEY,events:EVENTS.length});})()`);
  await p.reload(); await p.waitForTimeout(900);
  const r1 = await EV(`JSON.stringify({coins:save.coins,tut:!!save.tut})`);
  ok('a reload keeps the test save', r1.coins === 5555, r1);
  await p.goto('about:blank'); await p.goto('http://127.0.0.1:8766/lab6.html?test=1&newplayer'); await p.waitForTimeout(900);
  const r2 = await EV(`JSON.stringify({coins:save.coins,tut:!!save.tut,key:SAVE_KEY,events:EVENTS.length})`);
  ok('opening the link again starts a brand-new player, own save slot, no weekend event', r2.coins === 0 && !r2.tut && r2.key === 'snowplowRush.newplayer' && r2.events === 0 && a.events === 0, r2);
  const nw = await EV(`(()=>{window.__HOLD=1;save.ctrl='joy';startLevel(0,{});const t0=run.time;for(let k=0;k<60;k++)update(1/30);return JSON.stringify({held:run.time===t0,stars:['driveway','culdesac','gardens'].map(id=>LEVELS.find(L=>L.id===id).stars[2]),ftue:FTUE_NEW});})()`);
  ok('new start: clock waits, 70% three stars', nw.held && nw.stars.join() === '70,70,70' && nw.ftue, nw);
  await p.goto('about:blank'); await p.goto('http://127.0.0.1:8766/lab6.html?test=1&newplayer&oldftue'); await p.waitForTimeout(900);
  const od = await EV(`(()=>{window.__HOLD=1;save.ctrl='joy';startLevel(0,{});const t0=run.time;for(let k=0;k<60;k++)update(1/30);run.offer=true;run.time=0;draw();const u=ui.find(x=>x.id==='cont');return JSON.stringify({runs:run.time<t0||run.offer,stars:['driveway','culdesac','gardens'].map(id=>LEVELS.find(L=>L.id===id).stars[2]),ftue:FTUE_NEW,label:u&&(u.label||u.text||u.t)});})()`);
  ok('old start (&oldftue): clock runs at once, stars 80/85/85, no free continue', od.runs && od.stars.join() === '80,85,85' && !od.ftue, od);
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
