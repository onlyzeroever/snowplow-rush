// Checks for the tester-review fixes (Nov 27): p188 Starter Pack clock that ticks, p189 master limiter + quieter coin.
//   node tools/audit/review188.js            (local server on :8765 serving index6.html, app6.html, lab6.html)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  for (const pg of ['index6.html', 'app6.html', 'lab6.html']) {
    const ctx = await browser.newContext({ viewport: { width: 360, height: 640 } });
    const page = await ctx.newPage(); const errs = []; page.on('pageerror', e => errs.push(e.message));
    await page.goto(`http://127.0.0.1:8765/${pg}?test=1&review=all&starter`); await page.waitForTimeout(900);
    // p189: audio starts with the limiter in the chain and sounds still play
    const a = await page.evaluate(() => window.__EV(`(()=>{audioInit();const r={ac:!!AC,state:AC&&AC.state,coin:SFX_VOL.coin};
      try{sfx('coin');sfx('combo');sfx('buy');r.played=true;}catch(e){r.err=String(e);}return JSON.stringify(r);})()`));
    const r = JSON.parse(a);
    ok(r.ac && r.played && !r.err, `${pg}: audio starts and plays with the limiter (${r.state})`);
    ok(r.coin === 0.27, `${pg}: coin volume 0.27`);
    const src = await page.evaluate(() => document.documentElement.innerHTML.includes('createDynamicsCompressor'));
    ok(src, `${pg}: limiter in the build`);
    if (pg !== 'index6.html') {
      // p188: the shop card and the offer pop-up show a clock with seconds that moves
      const c1 = await page.evaluate(() => window.__EV(`(()=>{const l=starterLeft();return JSON.stringify({l,txt:fmtClock(l)});})()`));
      await page.waitForTimeout(2200);
      const c2 = await page.evaluate(() => window.__EV(`(()=>{const l=starterLeft();return JSON.stringify({l,txt:fmtClock(l)});})()`));
      const A = JSON.parse(c1), B = JSON.parse(c2);
      ok(A.l > 0 && /^\d+:\d\d:\d\d$/.test(A.txt), `${pg}: starter clock reads ${A.txt}`);
      ok(A.txt !== B.txt && A.l - B.l >= 1500, `${pg}: clock moved in 2 s (${A.txt} -> ${B.txt})`);
      const f = await page.evaluate(() => window.__EV(`[fmtClock(48*3600e3),fmtClock(3599e3),fmtClock(61e3),fmtClock(9e3),fmtClock(0)].join(' ')`));
      ok(f === '48:00:00 59:59 1:01 0:09 0:00', `${pg}: formats ${f}`);
      const html = await page.evaluate(() => document.documentElement.innerHTML);
      ok(!html.includes("'FOR THE NEXT 48 HOURS'"), `${pg}: no fixed "48 hours" text left`);
    }
    ok(errs.length === 0, `${pg}: no page errors ${errs.slice(0, 2).join(' | ')}`);
    await ctx.close();
  }
  await browser.close();
  console.log(fails ? `${fails} FAILED` : 'ALL OK'); process.exit(fails ? 1 : 0);
})();
