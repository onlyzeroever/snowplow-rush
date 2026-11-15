// node shot.js id x y "U1.2,R0.3,D1.2" out.png [tool] [wait]  -> start the job, put the plow at x,y, drive the key script, screenshot
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const [id, x, y, seq, out, tool, wait] = process.argv.slice(2);
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 2 })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(700);
  await page.evaluate(([id, x, y, tool]) => { const R = window.__SR; R.save.tut = true; R.save.story = { suburbs: true, farm: true, city: true, themepark: true, harbour: true, ski: true, pass: true, north: true }; R.save.tool = Math.max(R.save.tool, +tool); R.save.use = +tool; R.startLevel(R.LEVELS.findIndex(L => L.id === id)); R.P.x = +x; R.P.y = +y; }, [id, x, y, tool || 5]);
  for (const st of (seq || '').split(',').filter(Boolean)) { const k = { U: 'ArrowUp', D: 'ArrowDown', L: 'ArrowLeft', R: 'ArrowRight' }[st[0]], t = parseFloat(st.slice(1)) * 1000;
    await page.evaluate(k => { window.__SR.keys[k] = true; }, k); await page.waitForTimeout(t); await page.evaluate(k => { window.__SR.keys[k] = false; }, k); }
  await page.waitForTimeout(+(wait || 300)); await page.screenshot({ path: out }); console.log('errors', JSON.stringify(errors)); await browser.close(); })();
