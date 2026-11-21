// p162: events wait in the queue until PostHog confirms them; failed sends retry; unsent events survive a reload.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const url = 'http://127.0.0.1:8766/lab6.html';
const decode = (u, body) => { try { if (u.includes('/batch/')) return JSON.parse(body).batch.map(e => e.event + (e.uuid ? '' : '!nouuid'));
  const d = decodeURIComponent(body.replace(/^data=/, '')); return JSON.parse(Buffer.from(d, 'base64').toString('utf8')).map(e => e.event + (e.uuid ? '' : '!nouuid')); } catch (e) { return ['?']; } };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36' });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => false }); });
  let mode = 'fail'; const got = []; const t0 = Date.now();
  await ctx.route(/posthog\.com\/(batch|e)\//, async r => { const evs = decode(r.request().url(), r.request().postData() || '');
    got.push({ t: ((Date.now() - t0) / 1000).toFixed(1), mode, path: r.request().url().includes('/batch/') ? 'batch' : 'e', evs });
    if (mode === 'fail') return r.abort(); return r.fulfill({ status: 200, headers: { 'access-control-allow-origin': '*' }, contentType: 'application/json', body: '{"status":1}' }); });
  await ctx.route(/posthog\.com\/(array|flags|decide)/, r => r.fulfill({ status: 200, contentType: 'application/javascript', body: '' }));
  await ctx.route(/\/ph\/posthog/, r => r.fulfill({ status: 200, contentType: 'application/javascript', body: '' }));
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url); await p.waitForTimeout(1500); await p.touchscreen.tap(195, 600); await p.waitForTimeout(5000);
  const q1 = await p.evaluate(() => JSON.parse(localStorage.getItem('sr.phq') || '[]').map(e => e.event));
  console.log('after 6.5 s with PostHog unreachable, kept in storage:', JSON.stringify(q1));
  // reload with PostHog still down: the leftovers stay; then PostHog comes back
  await p.reload(); await p.waitForTimeout(1500);
  mode = 'ok'; await p.waitForTimeout(4000);
  const q2 = await p.evaluate(() => JSON.parse(localStorage.getItem('sr.phq') || '[]').length);
  const delivered = got.filter(g => g.mode === 'ok').flatMap(g => g.evs);
  console.log('delivered once PostHog was back:', JSON.stringify(delivered));
  console.log('left in storage after delivery:', q2);
  console.log('requests:', got.map(g => g.t + 's ' + g.mode + ' ' + g.path + ' ' + g.evs.length).join(' | '));
  const sessions = delivered.filter(e => e.startsWith('session_start')).length, starts = delivered.filter(e => e.startsWith('job_start')).length;
  const ok = q1.includes('session_start') && q1.includes('job_start') && sessions === 2 && starts >= 1 && q2 === 0 && !delivered.some(e => e.includes('!nouuid'));
  console.log((ok ? 'ok   ' : 'FAIL ') + 'p162: nothing lost while PostHog was unreachable across a reload', JSON.stringify(errs.slice(0, 3)));
  await b.close();
})();
