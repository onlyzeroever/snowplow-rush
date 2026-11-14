const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = [], out = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 2 })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  const start = (id, ti) => page.evaluate(([id, ti]) => { const R = window.__SR, i = R.LEVELS.findIndex(L => L.id === id); R.save.tut = true; R.save.story = { suburbs: true, farm: true, city: true }; R.save.tool = 5; R.save.use = ti; R.startLevel(i); }, [id, ti]);
  // 1. snow cannon: clear the ground in front of it, let it spray once, count re-covered cells
  await start('sledhill', 2); await page.waitForTimeout(3300);
  const c1 = await page.evaluate(() => { const R = window.__SR, G = R.G, hz = G.hazards.find(h => h.kind === 'cannon'); R.P.x = 90; R.P.y = hz.y + 60; window.__cells = [];
    for (let cy = 0; cy < G.rows; cy++) for (let cx = 0; cx < G.cols; cx++) { const dx = cx * 2 - hz.mx, dy = cy * 2 - hz.my; if (Math.hypot(dx, dy) < 80 && G.type[cy * G.cols + cx] !== 9) { G.depth[cy * G.cols + cx] = 0; window.__cells.push(cy * G.cols + cx); } }
    hz.state = 'idle'; hz.t = 0; return { cells: window.__cells.length, per: hz.per }; });
  await page.waitForTimeout(2900);
  await page.screenshot({ path: '/home/claude/levels/out/mech_cannon.png' });
  const c2 = await page.evaluate(() => { const G = window.__SR.G; let n = 0, s = 0; for (const i of window.__cells) { if (G.depth[i] > 0.3) n++; s += G.depth[i]; } return { recovered: n, depthSum: +s.toFixed(0) }; });
  out.push(['cannon spray', c1, c2, 'of clearable', await page.evaluate(() => window.__SR.G.clearable)]);
  // 2. jam it: put the blower against it
  const j = await page.evaluate(() => { const R = window.__SR, G = R.G, hz = G.hazards.find(h => h.kind === 'cannon'); R.P.x = hz.x + 9; R.P.y = hz.y + 28; R.P.f = 0; hz.immune = 0; hz.jam = 0; hz.state = 'idle'; hz.t = 5; window.__c0 = R.save.coins; return hz.jam; });
  await page.keyboard.down('ArrowUp'); await page.waitForTimeout(700); await page.keyboard.up('ArrowUp');
  out.push(['cannon jam', await page.evaluate(() => { const R = window.__SR, hz = R.G.hazards.find(h => h.kind === 'cannon'); return { jam: +hz.jam.toFixed(1), bonus: Math.round(R.save.coins - window.__c0), py: Math.round(R.P.y), hy: hz.y }; })]);
  await page.screenshot({ path: '/home/claude/levels/out/mech_jam.png' });
  // 3. ball machine: stand in the line of fire
  await start('tennis', 2); await page.waitForTimeout(3300);
  const b0 = await page.evaluate(() => { const R = window.__SR, hz = R.G.hazards.find(h => h.kind === 'balls'); R.P.x = 90; R.P.y = hz.my + 2; R.P.inv = 0; hz.state = 'idle'; hz.t = 0; return { hits: R.run.hits, my: hz.my }; });
  await page.waitForTimeout(450); await page.screenshot({ path: '/home/claude/levels/out/mech_balls_aim.png' });
  await page.waitForTimeout(1200);
  out.push(['ball machine', b0, await page.evaluate(() => ({ hits: window.__SR.run.hits }))]);
  // 4. neighbours at the corner shop: clear their path, they walk to the door and tip
  await start('cornershop', 1); await page.waitForTimeout(3300);
  await page.evaluate(() => { const G = window.__SR.G; for (const nb of G.neighbours) for (const i of nb.cells) G.depth[i] = 0; window.__c0 = window.__SR.save.coins; });
  await page.waitForTimeout(3500);
  out.push(['neighbours', await page.evaluate(() => ({ states: window.__SR.G.neighbours.map(n => n.state), tip: Math.round(window.__SR.save.coins - window.__c0) }))]);
  // 5. boss gate
  const g = await page.evaluate(() => { const R = window.__SR, i = R.LEVELS.findIndex(L => L.id === 'blockparty'), f = R.LEVELS.findIndex(L => L.id === 'fountainsq'); R.save.stars.fill(0); R.save.best.fill(0); R.save.stars[f] = 2;
    const a = { short: R.bossShort(i), stars: R.areaStars('suburbs') }; R.LEVELS.forEach((L, k) => { if (L.area === 'suburbs' && !L.boss) R.save.stars[k] = 2; }); return [a, { short: R.bossShort(i), stars: R.areaStars('suburbs') }]; });
  out.push(['boss gate', g]);
  console.log(out.map(o => JSON.stringify(o)).join('\n'), '\nerrors', JSON.stringify(errors)); await browser.close(); })();
