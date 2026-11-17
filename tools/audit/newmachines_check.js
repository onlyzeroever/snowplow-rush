// Every job with the Front Loader and the Icebreaker: can they reach the snow (vs the Super Plow and Rotary, whose
// bodies are a pixel smaller), and how hard is each area with the machine you'd have there.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  const r = await page.evaluate(() => { const R = window.__SR, ix = id => R.TOOLS.findIndex(t => t.id === id), worse = [], area = {};
    R.LEVELS.forEach((L, i) => { if (L.id === 'farm_old') return;
      const s = R.checkJob(i, ix('super'), 0, 0), l = R.checkJob(i, ix('loader'), 0, 0), ro = R.checkJob(i, ix('rotary'), 6, 6), ib = R.checkJob(i, ix('icebreaker'), 0, 0);
      if (l.reach < s.reach - 0.5) worse.push([L.id, 'loader', l.reach, 'super', s.reach]);
      if (ib.reach < ro.reach - 0.5) worse.push([L.id, 'icebreaker', ib.reach, 'rotary', ro.reach]);
      const a = area[L.area] || (area[L.area] = { n: 0, loader0: [], icebreaker0: [], rotary66: [], superLv: [] }); a.n++;
      a.loader0.push(l.verdict); a.icebreaker0.push(ib.verdict); a.rotary66.push(ro.verdict); });
    const tally = v => { const o = {}; v.forEach(x => o[x] = (o[x] || 0) + 1); return JSON.stringify(o); };
    return { worse, areas: Object.fromEntries(Object.entries(area).map(([k, a]) => [k, { loader_lv0: tally(a.loader0), icebreaker_lv0: tally(a.icebreaker0), rotary_max: tally(a.rotary66) }])) }; });
  console.log('jobs where a new machine reaches less snow:', r.worse.length ? JSON.stringify(r.worse) : 'none');
  for (const [k, v] of Object.entries(r.areas)) console.log(k.padEnd(10), 'loader lv0', v.loader_lv0, '| icebreaker lv0', v.icebreaker_lv0, '| rotary max', v.rotary_max);
  console.log('errors', JSON.stringify(errors)); await browser.close(); })();
