// p134 first session: one tap into job 1, notice on the title, 90 s driveway, no early +15 s pop-up, dailies after job 4. node tools/audit/ftue134.js
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  const EV = c => p.evaluate(c => window.__EV(c), c);
  const ids = async () => p.evaluate(() => window.__UI.list().map(u => u.id || u));
  // fresh player: title shows a cog, one tap starts job 1
  ok((await EV(`state`)) === 'title' && (await ids()).includes('tgear'), 'title has a settings cog');
  const box = await p.locator('canvas').boundingBox(); await p.mouse.click(box.x + box.width / 2, box.y + box.height * 0.8); await p.waitForTimeout(700);
  const s1 = JSON.parse(await EV(`JSON.stringify({st:state,job:G&&G.def.id,t:Math.round(run.time),priv:save.privSeen,story:!!(save.story&&save.story.suburbs)})`));
  ok(s1.st === 'play' && s1.job === 'driveway', 'first tap goes straight into the driveway ' + JSON.stringify(s1));
  ok(s1.t >= 88 && s1.t <= 90, 'driveway has 90 seconds');
  ok(s1.priv === true, 'tapping play marks the title notice as seen');
  ok((await EV(`JSON.stringify(LEVELS[0].stars)`)) === '[30,55,80]', 'driveway stars at 30/55/80%');
  // no +15 s pop-up in the first 3 jobs
  const o1 = JSON.parse(await EV(`(()=>{window.__HOLD=1;save.fbRuns=0;G.cleared=Math.round(G.clearable*0.4);run.time=0.01;update(0.05);return JSON.stringify({offer:!!run.offer,ended:!!run.ended});})()`));
  ok(!o1.offer && o1.ended, 'job 1 ends without the ad pop-up ' + JSON.stringify(o1));
  const o2 = JSON.parse(await EV(`(()=>{save.fbRuns=3;startLevel(0);G.cleared=Math.round(G.clearable*0.4);run.time=0.01;update(0.05);return JSON.stringify({offer:!!run.offer,ended:!!run.ended});})()`));
  ok(o2.offer && !o2.ended, 'from job 4 the +15 s offer is back ' + JSON.stringify(o2));
  // dailies wait
  const d1 = JSON.parse(await EV(`(()=>{save.fbRuns=1;save.dailyEver=false;save.best=save.best.map(()=>0);save.best[0]=60;save.stars[0]=2;save.dailySeen='';save.story={suburbs:true};goMap();
    const before=save.daily?save.daily.goals.map(g=>g.prog).join():'';dailyAdd('stars2',9);const after=save.daily?save.daily.goals.map(g=>g.prog).join():'';return JSON.stringify({open:dailyOpen,on:dailyOn(),same:before===after});})()`));
  ok(!d1.open && !d1.on && d1.same, 'after job 1: no daily pop-up, no daily progress ' + JSON.stringify(d1));
  await EV(`(window.__HOLD=0,1)`); await p.waitForTimeout(400);
  let ui = await ids(); ok(!ui.includes('daily') && !ui.includes('weekly'), 'map hides daily and weekly early');
  ok(ui.includes('node0') && !ui.includes('privok'), 'map shows jobs and no privacy card over job 1');
  const d2 = JSON.parse(await EV(`(()=>{save.fbRuns=4;dailyOpen=false;save.dailySeen='';goMap();return JSON.stringify({open:dailyOpen,on:dailyOn(),ever:save.dailyEver});})()`));
  ok(d2.open === 'new' && d2.on && d2.ever, 'after job 4 the dailies arrive ' + JSON.stringify(d2));
  await EV(`(dailyOpen=false,1)`); await p.waitForTimeout(400); ui = await ids();
  ok(ui.includes('daily') && ui.includes('weekly'), 'and the daily and weekly buttons show');
  // returning player: title tap goes to the map
  await EV(`(()=>{state='title';save.privSeen=true;return 1;})()`); await p.waitForTimeout(200);
  await p.mouse.click(box.x + box.width / 2, box.y + box.height * 0.8); await p.waitForTimeout(500);
  ok((await EV(`state`)) === 'map', 'a returning player taps through to the map');
  // job card copes before the map art exists (safety)
  ok((await EV(`(()=>{jobInfo=0;try{draw();return 'ok';}catch(e){return String(e);}finally{jobInfo=-1;}})()`)) === 'ok', 'job card draws');
  ok(errs.length === 0, 'no errors ' + JSON.stringify(errs.slice(0, 3)));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await b.close(); process.exit(fails ? 1 : 0);
})();
