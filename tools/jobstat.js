// usage: TOOLS=2,5 node jobstat.js [area|ids,comma|all] > out.json   -> {id:{time,h,tools:{ti:{r,t3,r6,t36}}}}
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const sel = process.argv[2] || 'all';
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  const out = await page.evaluate(([sel, TL]) => { const R = window.__SR, o = {};
    const ids = sel === 'all' ? R.LEVELS.map(L => L.id) : sel.includes(',') || R.LEVELS.some(L => L.id === sel) ? sel.split(',') : R.LEVELS.filter(L => L.area === sel).map(L => L.id);
    for (const id of ids) { const i = R.LEVELS.findIndex(L => L.id === id), L = R.LEVELS[i]; const e = { time: L.time, h: L.h, area: L.area, tools: {} };
      for (const ti of TL) { if (!R.TOOLS[ti]) continue; const a = R.checkJob(i, ti, 0, 0), m = R.checkJob(i, ti, 6, 6); e.tools[ti] = { id: R.TOOLS[ti].id, r: +a.reach.toFixed(1), t3: +a.t3.toFixed(1), r6: +m.reach.toFixed(1), t36: +m.t3.toFixed(1) }; }
      o[id] = e; }
    return o; }, [sel, (process.env.TOOLS || '2,3,5').split(',').map(Number)]);
  if (errors.length) console.error('errors', JSON.stringify(errors));
  console.log(JSON.stringify(out)); await browser.close(); })();
