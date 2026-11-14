const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const ids = (process.argv[2] || 'driveway,gardens,culdesac,park,school,maple,cornershop,playground,allotments,dogpark,tennis,highst,sledhill,fountainsq,blockparty').split(',');
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  const rows = await page.evaluate((ids) => { const R = window.__SR, out = [];
    for (const id of ids) { const i = R.LEVELS.findIndex(L => L.id === id), L = R.LEVELS[i]; const row = [id, L.time, L.h];
      for (const ti of [0, 1, 2, 3]) { const a = R.checkJob(i, ti, 0, 0), m = R.checkJob(i, ti, 6, 6); row.push(R.TOOLS[ti].id.slice(0, 4) + ' r' + Math.round(a.reach) + ' d' + (a.t3 / L.time).toFixed(2) + '/' + (m.t3 / L.time).toFixed(2)); }
      out.push(row.join('  ')); }
    return out; }, ids);
  console.log('job time h  | tool reach% d(lv0)/d(lv6)'); for (const r of rows) console.log(r);
  console.log('errors', JSON.stringify(errors)); await browser.close(); })();
