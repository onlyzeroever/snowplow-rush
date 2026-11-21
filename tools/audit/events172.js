// p172: in the apps the event schedule comes from https://snowplowrush.app; on the web from /events.json
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] }); const out = {};
  for (const [name, init] of [['web', null], ['app', () => { window.SRNative = { platform: 'ios', buy: () => Promise.resolve({ ok: false }), owned: () => Promise.resolve([]), prices: () => Promise.resolve({}) }; }]]) {
    const ctx = await b.newContext(); if (init) await ctx.addInitScript(init); const p = await ctx.newPage(); const urls = [];
    p.on('request', r => { if (r.url().includes('events.json')) urls.push(r.url().replace(/\?.*/, '')); });
    await p.route('https://snowplowrush.app/**', r => r.fulfill({ status: 200, contentType: 'application/json', body: '[]' }));
    await p.goto('http://127.0.0.1:8766/app6.html?test=1'); await p.waitForTimeout(1500); out[name] = urls; await ctx.close();
  }
  const ok = out.web.some(u => u === 'http://127.0.0.1:8766/events.json') && out.app.some(u => u === 'https://snowplowrush.app/events.json');
  console.log(JSON.stringify(out)); console.log(ok ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
