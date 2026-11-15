// Play-test bot: plays each job for real (keys, real hazards, real timer) with a greedy coverage planner.
// node bot.js job1,job2 toolIdx lv [parallel] -> per-job result line + mid-run screenshots in /home/claude/levels/out/bot_<id>_<n>.png
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const ids = process.argv[2].split(','), toolI = +(process.argv[3] || 1), lv = +(process.argv[4] || 3), par = +(process.argv[5] || 3);
const BOT = () => {
  const R = window.__SR, keys = R.keys; let plan = [], black = new Map(), curGoal = -1, now = 0, stuckT = 0, lastX = 0, lastY = 0, replanT = 0, stats = { replans: 0, stuck: 0 };
  const STEP = 4;
  function tick() {
    const G = R.G, P = R.P, run = R.run; if (!G || !P || !run || run.ended) return;
    if (run.offer) { R.endRound(); return; }
    const tid = R.TOOLS[R.save.use == null ? R.save.tool : R.save.use].id;
    const W2 = Math.floor(G.pw / STEP), H2 = Math.floor(G.ph / STEP);
    const okAt = (x, y) => { for (const f of [0, 1]) { const fp = window.__fp(tid, x, y, f); if (!window.__blk(fp)) return true; } return false; };
    replanT -= 1 / 30; const moved = Math.hypot(P.x - lastX, P.y - lastY); lastX = P.x; lastY = P.y;
    if (moved < 0.05 && P.stun <= 0) stuckT += 1 / 30; else stuckT = 0;
    now += 1 / 30; if (stuckT > 0.5) { stats.stuck++; plan = []; stuckT = 0; if (curGoal >= 0) black.set(curGoal, now + 6); }
    if (!plan.length || replanT <= 0) {
      replanT = 0.6; stats.replans++;
      // BFS from the player over a 4px grid, stop at the nearest node with snow under/around it
      const sx = Math.round(P.x / STEP), sy = Math.round(P.y / STEP), prev = new Int32Array(W2 * H2).fill(-2), q = [];
      const k0 = sy * W2 + sx; if (sx < 0 || sy < 0 || sx >= W2 || sy >= H2) return; prev[k0] = -1; q.push(k0); let goal = -1;
      const snowy = (x, y) => { let n = 0; for (let dy = -2; dy <= 2; dy += 2) for (let dx = -2; dx <= 2; dx += 2) { const cx = (x + dx) >> 1, cy = (y + dy) >> 1; if (cx < 0 || cy < 0 || cx >= G.cols || cy >= G.rows) continue; const i = cy * G.cols + cx; if (G.type[i] !== 9 && G.depth[i] > 0.3) n++; } return n >= 3; };
      const hx = Math.sign(P.vx), hy = Math.sign(P.vy), D8 = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
      const dirs = D8.slice().sort((a, b) => (b[0] * hx + b[1] * hy) - (a[0] * hx + a[1] * hy));
      for (let qi = 0; qi < q.length; qi++) { const k = q[qi], x = k % W2, y = (k / W2) | 0;
        if (qi > 0 && !(black.get(k) > now) && snowy(x * STEP, y * STEP)) { goal = k; break; }
        for (const [dx, dy] of dirs) { const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= W2 || ny >= H2) continue; const nk = ny * W2 + nx; if (prev[nk] !== -2) continue;
          if (dx && dy && (prev[y * W2 + nx] === -3 || prev[ny * W2 + x] === -3 || !okAt(nx * STEP, y * STEP) || !okAt(x * STEP, ny * STEP))) continue;
          prev[nk] = k; if (okAt(nx * STEP, ny * STEP)) q.push(nk); else prev[nk] = -3; } }
      curGoal = goal; plan = []; if (goal >= 0) { let k = goal; while (k >= 0 && k !== k0) { plan.push([(k % W2) * STEP, ((k / W2) | 0) * STEP]); k = prev[k]; } plan.reverse(); }
      // keep plowing straight past the goal for a bit: lawn-mower feel and it clears the strip
      if (plan.length) { const a = plan.length > 1 ? plan[plan.length - 2] : [P.x, P.y], b = plan[plan.length - 1], dx = Math.sign(b[0] - a[0]), dy = Math.sign(b[1] - a[1]);
        let dry = 0; for (let s = 1; s <= 70; s++) { const nx = b[0] + dx * STEP * s, ny = b[1] + dy * STEP * s; if (!okAt(nx, ny)) break; plan.push([nx, ny]); if (!snowy(nx, ny)) { if (++dry > 2) break; } else dry = 0; }
        replanT = 0.3 + plan.length / 60; } }
    while (plan.length && Math.hypot(plan[0][0] - P.x, plan[0][1] - P.y) < 2.5) plan.shift();
    for (const k of ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']) keys[k] = false;
    if (plan.length) { const dx = plan[0][0] - P.x, dy = plan[0][1] - P.y; if (dx > 1.2) keys.ArrowRight = true; if (dx < -1.2) keys.ArrowLeft = true; if (dy > 1.2) keys.ArrowDown = true; if (dy < -1.2) keys.ArrowUp = true; }
  }
  window.__botStats = stats; setInterval(tick, 1000 / 30);
};
async function one(browser, id) {
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 1 })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(700);
  const info = await page.evaluate(([id, toolI, lv]) => { const R = window.__SR, i = R.LEVELS.findIndex(L => L.id === id);
    R.save.tut = true; R.save.story = { suburbs: true, farm: true, city: true }; R.save.tool = Math.max(R.save.tool, toolI); R.save.use = toolI;
    const m = R.upg.mLv(R.TOOLS[toolI].id); m.speed = lv; m.size = lv; m.bumper = 2; R.save.lv.value = 4;
    R.startLevel(i); return { i, time: R.LEVELS[i].time }; }, [id, toolI, lv]);
  await page.evaluate(() => { const R = window.__SR; window.__fp = R.fp; window.__blk = R.blk; });
  await page.waitForTimeout(3300); await page.evaluate(BOT);
  const shots = [0.25, 0.55, 0.85]; const T = info.time * 1000 + 2500; const t0 = Date.now(); let n = 0;
  const samples = [];
  while (Date.now() - t0 < T) { await page.waitForTimeout(1000);
    const s = await page.evaluate(() => { const R = window.__SR, G = R.G, run = R.run; if (!G || !run) return null; return { pct: +(G.cleared / G.clearable * 100).toFixed(1), t: +run.time.toFixed(1), ended: !!run.ended, hits: run.hits, earned: Math.round(run.earned),
      jams: G.hazards.filter(h => h.kind === 'cannon' && h.jam > 0).length, shots: G.hazards.filter(h => h.kind === 'balls').reduce((a, h) => a + h.shots.length, 0), nb: G.neighbours.filter(x => x.state === 'done').length,
      peds: G.hazards.filter(h => h.kind === 'ped').map(h => [Math.round(h.x), Math.round(h.y)]).slice(0, 3) }; });
    if (s) samples.push(s); if (s && s.ended) break;
    if (n < shots.length && (Date.now() - t0) / T > shots[n]) { await page.screenshot({ path: `/home/claude/levels/out/bot_${id}_${n}.png` }); n++; } }
  const res = await page.evaluate(() => { const R = window.__SR, G = R.G, run = R.run, L = G.def; const pct = G.cleared / G.clearable * 100;
    return { pct: +pct.toFixed(1), stars: L.stars.filter(q => pct >= q).length, hits: run.hits, caught: run.caught || 0, chaser: (G.hazards.find(h => h.kind === 'chaser') || {}).state, earned: Math.round(run.earned), bot: window.__botStats,
      nbDone: G.neighbours.filter(x => x.state === 'done').length, nbAll: G.neighbours.length }; });
  const maxDrop = samples.reduce((a, s, i) => i ? Math.max(a, samples[i - 1].pct - s.pct) : 0, 0);
  console.log(id, JSON.stringify(res), 'pct-dips', maxDrop.toFixed(1), 'errors', JSON.stringify(errors.slice(0, 3)));
  await page.context().close();
}
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const queue = ids.slice(); const workers = []; for (let w = 0; w < par; w++) workers.push((async () => { while (queue.length) await one(browser, queue.shift()); })());
  await Promise.all(workers); await browser.close(); })();
