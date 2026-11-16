const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 390, height: 780 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage(); const errors = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  const ev = (f, a) => page.evaluate(f, a); const out = [];
  const setLv = (k, v) => ev(([k, v]) => { const R = window.__SR; for (const q of ['speed', 'size', 'value', 'bumper', 'helpers']) R.save.lv[q] = 0; const m = R.upg.mLv(R.upg.curMachine()); m.speed = 0; m.size = 0; m.bumper = 0; const mx = R.upg.upMax(k); if (['speed', 'size', 'bumper'].includes(k)) m[k] = Math.min(mx, v); else R.save.lv[k] = v; }, [k, v]);

  // A. buying each upgrade raises its level and charges the right price
  for (const k of ['speed', 'size', 'value', 'bumper', 'helpers']) {
    const r = await ev((k) => { const R = window.__SR; R.goUpgrades(); R.save.coins = 1e9; if (['speed', 'size', 'bumper'].includes(k)) R.upg.mLv(R.upg.curMachine())[k] = 0; else R.save.lv[k] = 0; const c = R.upg.upgCost(k), c0 = R.save.coins; R.upg.buyUpg(k); return { lv: R.upg.lvOf(k), paid: c0 - R.save.coins, cost: c }; }, k);
    out.push(['A buy ' + k, r, r.lv === 1 && Math.abs(r.paid - r.cost) < 1 ? 'PASS' : 'FAIL']);
  }
  // drive straight right on an empty job, return distance, cells cleared, coins earned
  const drive = async () => {
    await ev(() => { const R = window.__SR; R.save.tut = true; R.startLevel(0); }); await page.waitForTimeout(3300);
    await ev(() => { const R = window.__SR, G = R.G, P = R.P; G.obstacles.length = 0; G.hazards.length = 0; G.cows.length = 0; P.x = 30; P.y = 150; R.run.moved = true; R.run.combo = 0; window.__c0 = G.cleared; window.__e0 = R.run.earned; });
    await ev(() => { window.__HOLD = true; }); await page.keyboard.down('ArrowRight'); await ev(() => window.__STEP(21, 1 / 30, 0)); await page.keyboard.up('ArrowRight'); await ev(() => { window.__STEP(15, 1 / 30, 0); window.__HOLD = false; }); // fixed 0.7 s of game time, not wall-clock time, so results don't depend on machine load
    return ev(() => { const R = window.__SR; return { dx: +(R.P.x - 30).toFixed(1), cells: R.G.cleared - window.__c0, earned: +(R.run.earned - window.__e0).toFixed(1), speed: +R.upg.moveSpeed().toFixed(1), blade: R.upg.bladeCells(), vm: +R.upg.valueMult().toFixed(2) }; });
  };
  // B. speed
  await setLv('speed', 0); const s0 = await drive(); await setLv('speed', 10); const s1 = await drive();
  out.push(['B speed lv0 vs lv10', s0, s1, 'ratio ' + (s1.dx / s0.dx).toFixed(2) + ' (shovel max, expect ~1.15)', s1.dx / s0.dx > 1.1 ? 'PASS' : 'FAIL']);
  // C. size
  await setLv('size', 0); const z0 = await drive(); await setLv('size', 8); const z1 = await drive();
  out.push(['C plow width lv0 vs lv8', { blade: z0.blade, cells: z0.cells }, { blade: z1.blade, cells: z1.cells }, z1.blade > z0.blade && z1.cells > z0.cells * 1.2 ? 'PASS' : 'FAIL']);
  // D. value
  await setLv('value', 0); const v0 = await drive(); await setLv('value', 10); const v1 = await drive();
  const perCell0 = v0.earned / v0.cells, perCell1 = v1.earned / v1.cells;
  out.push(['D snow value lv0 vs lv10', { vm: v0.vm, perCell: +perCell0.toFixed(2) }, { vm: v1.vm, perCell: +perCell1.toFixed(2) }, 'ratio ' + (perCell1 / perCell0).toFixed(2) + ' (expect ~2.2)', perCell1 / perCell0 > 1.9 ? 'PASS' : 'FAIL']);
  // E. bumper: shorter stun after a bonk, fewer coins spilled when hit
  const bump = async (lv) => { await setLv('bumper', lv); await ev(() => { const R = window.__SR; R.startLevel(0); }); await page.waitForTimeout(3300);
    return ev(() => { const R = window.__SR, P = R.P; P.inv = 0; R.hit('ob'); const stun = P.stun; P.inv = 0; P.stun = 0; R.run.earned = 1000; R.save.coins = 5000; const c0 = R.save.coins; R.hit('hz', 0.3); return { red: +R.upg.bumperRed().toFixed(2), stun: +stun.toFixed(3), lost: c0 - R.save.coins }; }); };
  const b0 = await bump(0), b1 = await bump(10);
  out.push(['E bumper lv0 vs lv10', b0, b1, b1.stun < b0.stun * 0.6 && b1.lost < b0.lost * 0.6 ? 'PASS' : 'FAIL']);
  // F. helpers: coins tick up on the map, and pile up while you're away
  const help = async (lv) => { await setLv('helpers', lv); await ev(() => { const R = window.__SR; R.goMap(); R.save.coins = 1000; }); await page.waitForTimeout(3000); return ev(() => ({ gained: +(window.__SR.save.coins - 1000).toFixed(1), perSec: +window.__SR.upg.helperIncome().toFixed(2) })); };
  const h0 = await help(0), h1 = await help(5);
  out.push(['F helpers on map 3s, lv0 vs lv5', h0, h1, h0.gained < 0.01 && h1.gained > h1.perSec * 2 ? 'PASS' : 'FAIL']);
  await ev(() => { const R = window.__SR; R.save.lv.helpers = 5; R.save.last = Date.now() - 3600 * 1000; localStorage.setItem('snowplowRush.test', JSON.stringify(R.save)); window.onbeforeunload = null; });
  await page.addInitScript(() => { const k = 'snowplowRush.test'; const s = JSON.parse(localStorage.getItem(k) || 'null'); if (s && !sessionStorage.getItem('done')) { s.last = Date.now() - 3600 * 1000; localStorage.setItem(k, JSON.stringify(s)); sessionStorage.setItem('done', '1'); } });
  await page.reload(); await page.waitForTimeout(800);
  const off = await ev(() => { const R = window.__SR; return { offlineGain: Math.round(R.upg.offlineGain), perSec: +R.upg.helperIncome().toFixed(2), cap: R.upg.OFFLINE_CAP_S, rate: R.upg.OFFLINE_RATE }; });
  out.push(['F2 helpers while away 1 hour', off, off.offlineGain > 0 ? 'PASS' : 'FAIL']);
  await page.screenshot({ path: '/home/claude/proto/shots6/upg_welcome.png' });
  for (const o of out) console.log(JSON.stringify(o));
  console.log('FAILS', out.filter(o => o[o.length - 1] !== 'PASS').length, 'ERRORS', JSON.stringify(errors));
  await browser.close();
})();
