// p161: on a slow big phone (430x932 @3x, CPU slowed 6x) does the render scale drop, and do frames get faster?
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const page = process.argv[2] || 'index6.html', rate = +(process.argv[3] || 6);
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 430, height: 932 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/' + page); await p.waitForTimeout(1500);
  const cdp = await ctx.newCDPSession(p); await cdp.send('Emulation.setCPUThrottlingRate', { rate });
  await p.evaluate(() => { try { localStorage.removeItem('sr.kscap'); } catch (e) {} window.__fr = []; let l = performance.now(); const f = t => { window.__fr.push(t - l); l = t; requestAnimationFrame(f); }; requestAnimationFrame(f); });
  await p.touchscreen.tap(215, 600); await p.waitForTimeout(1200);
  await p.keyboard.down('ArrowUp');
  const rows = [];
  for (let s = 0; s < 14; s++) {
    await p.waitForTimeout(1000);
    if (s === 6) { await p.keyboard.up('ArrowUp'); await p.keyboard.down('ArrowRight'); }
    const r = await p.evaluate(() => { const a = window.__fr.splice(0); const avg = a.reduce((x, y) => x + y, 0) / Math.max(1, a.length); return { w: document.querySelector('canvas').width, fps: Math.round(1000 / avg), slow: Math.round(a.filter(x => x > 34).length / Math.max(1, a.length) * 100) }; });
    rows.push(r);
  }
  await p.keyboard.up('ArrowRight');
  console.log(page, 'cpu x' + rate, rows.map(r => `${r.w}px ${r.fps}fps ${r.slow}%slow`).join(' | '));
  console.log('kscap:', await p.evaluate(() => localStorage.getItem('sr.kscap')), 'errors:', JSON.stringify(errs.slice(0, 2)));
  await b.close();
})();
