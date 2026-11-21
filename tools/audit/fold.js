// fold/unfold mid-job: the run carries on, the canvas re-fits, no errors
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await br.newContext({ viewport: { width: 393, height: 852 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/app6.html?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c);
  await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=12;startLevel(1);return 1;})()`); await p.waitForTimeout(3500);
  const look = async () => JSON.parse(await EV(`JSON.stringify({st:state,t:+run.time.toFixed(1),job:G&&G.def.id,css:(()=>{const c=[...document.querySelectorAll('canvas')].find(c=>c.id!=='bg');const r=c.getBoundingClientRect();return Math.round(r.width)+'x'+Math.round(r.height)+'@'+Math.round(r.left)})()})`));
  const a = await look();
  await p.setViewportSize({ width: 1000, height: 704 }); await p.waitForTimeout(800); const c = await look();
  await p.setViewportSize({ width: 393, height: 852 }); await p.waitForTimeout(800); const d = await look();
  const ok = a.st === 'play' && c.st === 'play' && d.st === 'play' && a.job === d.job && c.css !== a.css && d.css === a.css && errs.length === 0;
  console.log(JSON.stringify({ a, c, d }), 'errors', errs.slice(0, 2)); console.log(ok ? 'ALL OK' : 'FAILS'); await br.close();
})();
