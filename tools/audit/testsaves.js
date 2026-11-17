const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const st of ['themepark','ski','pass','north']) {
    const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs=[];p.on('pageerror',e=>errs.push(e.message));
    await p.goto('http://127.0.0.1:8765/index6.html?review=' + st); await p.waitForTimeout(1200);
    const r = await p.evaluate(() => window.__SR ? null : 'no __SR (expected outside test mode)');
    // read state through the canvas world: use localStorage save
    const sv = await p.evaluate((st) => { const s = JSON.parse(localStorage.getItem('snowplowRush.review_' + st) || 'null'); return s ? { tool: s.tool, coins: s.coins, stars: (s.stars||[]).filter(x=>x>0).length, rv: s.rvStage } : null; }, st);
    await p.mouse.click(180, 400); await p.waitForTimeout(900);
    await p.screenshot({ path: `/tmp/rv_${st}.png` });
    console.log(st, JSON.stringify(sv), 'errors', JSON.stringify(errs));
    await p.context().close(); }
  await br.close(); })();
