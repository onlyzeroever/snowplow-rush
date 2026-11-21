// p165: save mirror to the phone, start from the phone's copy, reminders plan on hide, nudge card after a 3-star job
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 360, height: 640 } });
  await ctx.addInitScript(() => { window.__nat = { saves: [], plans: [], asked: 0 };
    window.SRNativeSave = { 'snowplowRush.test': JSON.stringify({ v: 6, tv: 3, tut: true, coins: 4242, tool: 0, gems: 7, lv: { speed: 0, size: 0, value: 0, bumper: 0, helpers: 2 }, stars: [], best: [] }) };
    window.SRNative = { platform: 'ios', buy: () => Promise.resolve({ ok: true }), storeSave: (k, j) => __nat.saves.push(k + ':' + j.length),
      scheduleReminders: list => __nat.plans.push(list), askReminders: () => { __nat.asked++; return Promise.resolve(true); } }; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/lab6.html?test=1'); await p.waitForTimeout(1000);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const s0 = await EV(`JSON.stringify({coins:save.coins,gems:save.gems})`);
  ok('an empty browser starts from the phone\'s copy of the save', s0.coins === 4242 && s0.gems === 7, s0);
  await EV(`(()=>{for(let i=0;i<20;i++)persist();return '1';})()`); const n1 = await p.evaluate(() => __nat.saves.length);
  await p.waitForTimeout(5300); const n2 = await p.evaluate(() => __nat.saves.length);
  ok('saves reach the phone at most every 5 s (20 saves -> 1 now, 1 after the wait)', n1 >= 1 && n1 <= 2 && n2 === n1 + 1, { n1, n2 });
  await EV(`(()=>{save.privSeen=true;window.__HOLD=1;startLevel(0,{});run.moved=true;G.cleared=G.clearable;run.res=null;endRound(true);return JSON.stringify({stars:run.res&&run.res.stars});})()`);
  const card = await EV(`(()=>{goMap();draw();const u=ui.find(x=>x.id==='rmyes');return JSON.stringify({ask:remindAsk,btn:!!u,blocked:overlayOpen()});})()`);
  ok('after a three-star job, the map shows the nudge card and blocks the map under it', card.ask && card.btn && card.blocked, card);
  await EV(`(()=>{ui.find(x=>x.id==='rmyes').fn();return '1';})()`); await p.waitForTimeout(100);
  const after = await EV(`JSON.stringify({asked:save.remindAsked,ok:save.remindOk,ask:remindAsk})`); const asked = await p.evaluate(() => __nat.asked);
  ok('YES PLEASE asks the phone once and turns reminders on', after.asked && after.ok && !after.ask && asked === 1, { after, asked });
  await p.evaluate(() => { Object.defineProperty(document, 'hidden', { get: () => true, configurable: true }); document.dispatchEvent(new Event('visibilitychange')); });
  const plan = await p.evaluate(() => __nat.plans.at(-1));
  ok('going to the background hands over a reminder plan (shed full, daily gift)', Array.isArray(plan) && plan.some(r => r.id === 'shed') && plan.some(r => r.id === 'daily') && plan.every(r => r.at > Date.now()), plan && plan.map(r => r.id + '@' + new Date(r.at).toISOString().slice(5, 16)));
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
