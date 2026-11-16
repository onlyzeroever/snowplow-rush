const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await br.newContext({ viewport: { width: 360, height: 640 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  // premium player coming back after 5 h
  await p.addInitScript(() => { try { const k = 'snowplowRush.test'; } catch (e) {} });
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  await p.evaluate(() => window.__EV(`(()=>{save.tut=true;save.pro=true;save.lv.helpers=5;save.last=Date.now()-5*3600*1000;persist();})()`));
  await p.evaluate(() => window.__EV(`(()=>{const away=5*3600;offlineAway=away;offlineGain=helperIncome()*Math.min(offCap(),away)*OFFLINE_RATE*(save.pro?2:1);})()`));
  const g = await p.evaluate(() => window.__EV(`[Math.round(offlineGain),Math.round(save.coins)]`));
  await p.evaluate(() => window.__EV(`state='title'`)); await p.waitForTimeout(500); await p.screenshot({ path: '/tmp/prem_welcome.png' }); await p.evaluate(() => window.__EV(`(()=>{save.pro=false;offlineGain=36000;})()`)); await p.waitForTimeout(300); await p.screenshot({ path: '/tmp/free_welcome.png' }); await p.evaluate(() => window.__EV(`save.pro=true`));
  // results screen for premium
  await p.evaluate(() => window.__EV(`offlineGain=0`));
  await p.evaluate(() => { const R = window.__SR; R.save.tool = 3; R.save.use = 3; R.startLevel(R.LEVELS.findIndex(L => L.id === 'farmyard')); });
  await p.waitForTimeout(3300);
  const before = await p.evaluate(() => window.__SR.save.coins);
  await p.evaluate(() => { const R = window.__SR; window.__HOLD = true; R.keys.ArrowRight = true; window.__STEP(120, 1/30, 0); R.keys.ArrowRight = false; window.__EV('endRound(false)'); window.__STEP(150, 1/30, 1); window.__HOLD = false; });
  await p.waitForTimeout(2500); await p.screenshot({ path: '/tmp/prem_results.png' });
  const after = await p.evaluate(() => [window.__SR.save.coins, window.__SR.run.earned, window.__SR.run.proDbl, window.__EV('state')]);
  console.log('welcome gain,coins', JSON.stringify(g), 'coins before end', Math.round(before), 'after', JSON.stringify(after), 'errors', JSON.stringify(errs));
  await br.close(); })();
