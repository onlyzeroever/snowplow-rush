// Does the live build actually send its analytics? Loads the page as a real (non-bot) phone visitor,
// catches every request to PostHog and prints which events would have reached it.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const url = process.argv[2] || 'http://127.0.0.1:8770/index.html';
const mode = process.argv[3] || 'ok'; // ok | batchfail | allfail
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36' });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); });
  const got = []; const errs = [];
  await ctx.route(/posthog\.com/, async (route) => {
    const r = route.request(); const u = r.url(); let evs = [];
    try {
      const body = r.postData() || '';
      if (u.includes('/batch/')) { evs = JSON.parse(body).batch.map(e => e.event); }
      else if (u.includes('/e/')) { const d = decodeURIComponent(body.replace(/^data=/, '')); evs = JSON.parse(Buffer.from(d, 'base64').toString('utf8')).map(e => e.event); }
    } catch (e) { evs = ['(unreadable ' + e.message + ')']; }
    got.push({ t: Date.now(), path: u.replace(/^https:\/\/[^/]+/, '').slice(0, 40), method: r.method(), evs });
    if (mode === 'allfail' || (mode === 'batchfail' && u.includes('/batch/'))) return route.abort();
    return route.fulfill({ status: 200, contentType: 'application/json', headers: { 'access-control-allow-origin': '*' }, body: '{"status":1}' });
  });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  const t0 = Date.now(); await p.goto(url); await p.waitForTimeout(2500);
  await p.touchscreen.tap(195, 600); await p.waitForTimeout(1500); await p.touchscreen.tap(195, 600);
  await p.waitForTimeout(18000);
  // hide the page like a phone lock
  await p.evaluate(() => { Object.defineProperty(document, 'hidden', { get: () => true, configurable: true }); document.dispatchEvent(new Event('visibilitychange')); });
  await p.waitForTimeout(1000);
  for (const g of got) console.log(((g.t - t0) / 1000).toFixed(1) + 's', g.method, g.path, JSON.stringify(g.evs));
  console.log('page errors:', JSON.stringify(errs.slice(0, 5)));
  await b.close();
})();
