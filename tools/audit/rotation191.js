// Weekend event rotation (p191): checks with a fake clock in two time zones.
//   node tools/audit/rotation191.js        (local server on :8765 serving index6.html, app6.html, lab6.html)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const open = async (pg, q, tz) => {
    const ctx = await browser.newContext({ viewport: { width: 360, height: 640 }, timezoneId: tz });
    await ctx.addInitScript(() => { const RN = Date.now.bind(Date); let off = 0; window.__setNow = T => { off = T - RN(); }; Date.now = () => RN() + off; });
    const page = await ctx.newPage(); const errs = []; page.on('pageerror', e => errs.push(e.message));
    await page.goto(`http://127.0.0.1:8765/${pg}?${q}`); await page.waitForTimeout(900);
    return { page, ctx, errs };
  };
  // local time -> evNow / evNext
  const at = (page, y, mo, d, h, mi) => page.evaluate(([y, mo, d, h, mi]) => { window.__setNow(new Date(y, mo - 1, d, h, mi).getTime());
    return JSON.parse(window.__EV(`(()=>{const n=evNow(),x=evNext();return JSON.stringify({now:n&&{id:n.id,kind:n.kind,auto:!!n.auto,s:new Date(n.start).toString().slice(0,21),e:new Date(n.end).toString().slice(0,21)},next:x&&{id:x.id,kind:x.kind,inH:Math.round((x.start-Date.now())/36e5)}});})()`)); }, [y, mo, d, h, mi]);

  for (const pg of ['app6.html', 'index6.html']) for (const tz of ['Europe/London', 'Asia/Bangkok']) {
    const { page, ctx, errs } = await open(pg, 'test=1&review=all&autoev', tz);
    const fri = await at(page, 2026, 11, 27, 10, 0);
    ok(fri.now && fri.now.auto && fri.now.id === 'w2026-11-27' && /Fri Nov 27 2026 00:00/.test(fri.now.s) && /Mon Nov 30 2026 00:00/.test(fri.now.e),
      `${pg} ${tz}: Friday 10:00 -> ${fri.now && fri.now.kind} weekend (Fri 00:00 to Mon 00:00 local)`);
    const sun = await at(page, 2026, 11, 29, 23, 59);
    ok(sun.now && sun.now.id === 'w2026-11-27', `${pg} ${tz}: Sunday 23:59 still on`);
    const mon = await at(page, 2026, 11, 30, 0, 1);
    ok(!mon.now && mon.next && mon.next.id === 'w2026-12-04' && mon.next.inH === 96, `${pg} ${tz}: Monday 00:01 off, next in ${mon.next && mon.next.inH}h (${mon.next && mon.next.kind})`);
    const thu = await at(page, 2026, 12, 3, 23, 0);
    ok(!thu.now && thu.next && thu.next.inH === 1, `${pg} ${tz}: Thursday 23:00 -> next in 1h`);
    // 20 weekends: never the same twice running, both kinds used
    const seq = [];
    for (let k = 0; k < 20; k++) { const r = await at(page, 2026, 11, 27 + k * 7, 12, 0); seq.push(r.now && r.now.kind); }
    ok(seq.every(Boolean) && seq.every((x, i) => !i || x !== seq[i - 1]) && new Set(seq).size === 2, `${pg} ${tz}: 20 weekends, no repeats: ${seq.slice(0, 8).join(' ')}...`);
    // events.json override wins for its weekend; "off" pauses the auto event; next skips a paused weekend
    const ov = await page.evaluate(() => { window.__setNow(new Date(2027, 0, 1, 12, 0).getTime());
      return window.__EV(`(()=>{EVENTS.push({id:'newyear-2027',kind:'blizzard',start:new Date(2027,0,1).getTime(),end:new Date(2027,0,4).getTime()});const n=evNow();
        EV_OFF.push({start:new Date(2027,0,8).getTime(),end:new Date(2027,0,11).getTime()});Date.now();
        return JSON.stringify({now:n.id,kind:n.kind});})()`); });
    const o = JSON.parse(ov);
    ok(o.now === 'newyear-2027' && o.kind === 'blizzard', `${pg} ${tz}: events.json New Year entry replaces that weekend's auto event`);
    const paused = await at(page, 2027, 1, 8, 12, 0);
    ok(!paused.now && paused.next && paused.next.id === 'w2027-01-15', `${pg} ${tz}: an "off" entry pauses its weekend; next = ${paused.next && paused.next.id}`);
    ok(errs.length === 0, `${pg} ${tz}: no page errors ${errs.slice(0, 2).join(' | ')}`);
    await ctx.close();
  }
  // tests and previews stay predictable
  { const { page, ctx } = await open('app6.html', 'test=1&review=all', 'Europe/London');
    const r = await at(page, 2026, 11, 27, 10, 0); ok(!r.now && !r.next, 'app6 ?test=1 without &autoev: no auto events (bot and audits unchanged)'); await ctx.close(); }
  { const { page, ctx } = await open('app6.html', 'test=1&review=all&autoev&event=presents', 'Europe/London');
    const r = await at(page, 2026, 11, 27, 10, 0); ok(r.now && r.now.id === 'test-presents' && !r.next, '?event=presents preview: only the preview event'); await ctx.close(); }
  { const { page, ctx, errs } = await open('lab6.html', 'test=1&review=all&autoev&lab', 'Europe/London');
    const r = await at(page, 2026, 11, 27, 10, 0); ok(!r.now && !r.next && !errs.length, 'lab: no auto events (lab events are picked on the LAB screen)'); await ctx.close(); }
  // pictures of the map slot: Thursday (next event) and Friday (event on)
  for (const [name, d, h] of [['thu', 3, 20], ['fri', 4, 9]]) {
    const { page, ctx } = await open('app6.html', 'test=1&review=all&autoev', 'Europe/London');
    await page.evaluate(([d, h]) => { window.__setNow(new Date(2026, 11, d, h, 0).getTime()); window.__EV("(()=>{save.dailyEver=true;state='map';return 1;})()"); }, [d, h]);
    await page.waitForTimeout(500); await page.screenshot({ path: `/tmp/rot_${name}.png` }); await ctx.close();
  }
  await browser.close();
  console.log(fails ? `${fails} FAILED` : 'ALL OK'); process.exit(fails ? 1 : 0);
})();
