// Bot playtest on every build: plays jobs for real inside the game (real hazards, real timer, real machine physics),
// stepped faster than real time with a fixed random seed, so two builds can be compared run for run.
//   node tools/audit/botplay.js [jobs=all|id,id] [workers=3] [lv=3] [out=/tmp/botplay.json] [baseline=tools/audit/bot_baseline.json] [machines=all|entry] [seeds=1]
// Busy later jobs swing a lot from one set of random numbers to the next, so compare builds on the median of 3 seeds (seeds=3).
// Every build: machines=entry (~125 runs, ~4 min). Before a release or after big changes: all (~560 runs, ~20 min on 2 CPUs).
// For each job: the area's entry machine, the next two, the Icebreaker and the UFO (Wild Ride jobs: their own ride).
// Prints a table and flags: no star with the entry machine, stuck spots (stuck 3 s+), errors, and changes against the baseline.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs');
const arg = (i, d) => (process.argv[i] === undefined || process.argv[i] === '' ? d : process.argv[i]);
const JOBS = arg(2, 'all'), WORKERS = +arg(3, 3), MACH = arg(7, 'all'), SEEDS = +arg(8, 1), LV = arg(4, 'arrive'), OUT = arg(5, '/tmp/botplay.json'), BASE = arg(6, __dirname + '/bot_baseline.json');
const URL = 'http://127.0.0.1:8765/index6.html?test=1';
// the same job and machine always get the same random numbers, whatever else is in the run
// upgrade levels a typical player has on arrival (matches the skip-ahead test saves: themepark 4, ski 6, pass 4, north 6)
const ARRIVE_LV = { suburbs: 1, farm: 2, city: 3, themepark: 4, harbour: 4, ski: 6, pass: 4, north: 6 };
const seedOf = str => { let h = 2166136261; for (const c of str) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return h >>> 0; };

// runs inside the page: one job, one machine, start to finish
const PLAY = ([jobId, toolId, lv, seed, AVOID]) => {
  const R = window.__SR, EV = window.__EV;
  // fixed random numbers for this run
  let a = seed >>> 0; const rnd = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const realRandom = Math.random; Math.random = rnd;
  // sounds are rate-limited by the wall clock and pick random pitches: give them a game clock so the random numbers line up run to run
  const realNow = performance.now; let fakeMs = 0; performance.now = () => fakeMs;
  const out = { job: jobId, tool: toolId, lv, err: null };
  try {
    window.__HOLD = true;
    const i = R.LEVELS.findIndex(L => L.id === jobId), ti = R.TOOLS.findIndex(t => t.id === toolId);
    EV(`(()=>{tNow=0;shake=0;flakes.forEach((f,i)=>{f.x=(i*53)%W;f.y=(i*37)%H;f.s=10+(i*13)%17;f.ph=i*0.7;});save.tut=true;save.privSeen=true;save.story=save.story||{};AREA_SEQ.forEach(a=>save.story[a]=true);save.fbRuns=0;save.dailyEver=true;offerOpen=null;
      save.tool=Math.max(save.tool,${Math.min(ti, 9)});save.rides=save.rides||{};${ti >= 10 ? `save.rides['${toolId}']=true;save.ibEver=true;` : ''}save.use=${ti};
      const m=mLv('${toolId}');m.speed=${lv};m.size=${lv};m.bumper=2;save.lv.value=4;_tc.k='';return 1;})()`);
    R.startLevel(i);
    const G = R.G, P = R.P, run = R.run, L = G.def, tid = toolId;
    const STEP = 4, W2 = Math.floor(G.pw / STEP), H2 = Math.floor(G.ph / STEP), okCs = {};
    // a test drive swaps the machine for 15 s of driving: plan with whatever is being driven right now
    const curId = () => run.drive || tid; let lastId = tid;
    const STATIC_HZ = G.hazards.filter(h => !['barrier', 'ped', 'pull'].includes(h.kind));
    // big machines fit some gaps only at exact spots: each 4 px grid point may shift up to 2 px to find a spot where the machine fits
    const OFF = [[0, 0], [2, 0], [-2, 0], [0, 2], [0, -2], [1, 0], [-1, 0], [0, 1], [0, -1], [2, 2], [-2, 2], [2, -2], [-2, -2]];
    const okK = (gx, gy) => { if (gx < 0 || gy < 0 || gx >= W2 || gy >= H2) return 0; const k = gy * W2 + gx, id = curId(), okC = okCs[id] || (okCs[id] = new Int8Array(W2 * H2));
      if (!okC[k]) { okC[k] = -1; const hs = G.hazards; G.hazards = STATIC_HZ; // the cache holds the fixed layout only; gates and people are checked live
        for (let o = 0; o < OFF.length; o++) { const x = gx * STEP + OFF[o][0], y = gy * STEP + OFF[o][1]; if (!R.blk(R.fp(id, x, y, 0)) || !R.blk(R.fp(id, x, y, 1))) { okC[k] = o + 1; break; } }
        G.hazards = hs; }
      return okC[k] > 0 ? okC[k] : 0; };
    const okAt = (x, y) => okK(Math.round(x / STEP), Math.round(y / STEP)) > 0;
    const posK = k => { const gx = k % W2, gy = (k / W2) | 0, o = OFF[(okK(gx, gy) || 1) - 1]; return [gx * STEP + o[0], gy * STEP + o[1]]; };
    const snowy = (x, y) => { let n = 0; for (let dy = -2; dy <= 2; dy += 2) for (let dx = -2; dx <= 2; dx += 2) { const cx = (x + dx) >> 1, cy = (y + dy) >> 1;
      if (cx < 0 || cy < 0 || cx >= G.cols || cy >= G.rows) continue; const k = cy * G.cols + cx; if (G.type[k] !== 9 && G.depth[k] > 0.25) n++; } return n >= 3; };
    let progC = 0, progT = 0, plan = [], black = new Map(), curGoal = -1, now = 0, stuckT = 0, lastX = P.x, lastY = P.y, replanT = 0;
    const st = { replans: 0, stuck: 0, stuckMax: 0, stuckAt: [], hits0: run.hits || 0 };
    const keys = R.keys;
    const tick = () => {
      if (!R.G || run.ended || run.sweep) return;
      if (curId() !== lastId) { lastId = curId(); plan = []; black.clear(); st.drives = (st.drives || 0) + 1; }
      // no progress for 3 s while chasing a goal (rocking on the spot, pushing a wall): give that spot up for a while
      const pc = G.cleared; if (pc > progC + 0.002 * G.clearable) { progC = pc; progT = 0; } else if ((progT += 1 / 30) > 3 && curGoal >= 0) { black.set(curGoal, now + 8); plan = []; progT = 0; st.stalls = (st.stalls || 0) + 1; }
      replanT -= 1 / 30; now += 1 / 30; const moved = Math.hypot(P.x - lastX, P.y - lastY); lastX = P.x; lastY = P.y;
      if (moved < 0.05 && !(P.stun > 0)) { stuckT += 1 / 30; st.stuckMax = Math.max(st.stuckMax, stuckT); } else stuckT = 0;
      if (stuckT > 0.5 && plan.length) { st.stuck++; if (stuckT < 0.54) st.stuckAt.push([Math.round(P.x), Math.round(P.y)]); plan = []; if (curGoal >= 0) black.set(curGoal, now + 6); }
      if (!plan.length || replanT <= 0) {
        replanT = 0.6; st.replans++;
        const sx = Math.round(P.x / STEP), sy = Math.round(P.y / STEP); if (sx < 0 || sy < 0 || sx >= W2 || sy >= H2) return;
        const prev = new Int32Array(W2 * H2).fill(-2), q = [sy * W2 + sx], k0 = q[0]; prev[k0] = -1; let goal = -1;
        const hx = Math.sign(P.vx || 0), hy = Math.sign(P.vy || 0), D8 = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
        const dirs = D8.slice().sort((p, r) => (r[0] * hx + r[1] * hy) - (p[0] * hx + p[1] * hy));
        const fr = R.fp(curId(), P.x, P.y, 0), minD = Math.max(3, 0.5 * Math.max(fr.w, fr.h));
        // steer around people, animals and vehicles where they are now (a player waits or goes round; bumping them stuns the machine)
        const hz = G.hazards.filter(h => typeof h.x === 'number' && typeof h.w === 'number' && h.w > 0 && h.w < 60 && Math.hypot(h.x + h.w / 2 - P.x, h.y + (h.h || 0) / 2 - P.y) < 140)
          .map(h => ({ x: h.x - 3, y: h.y - 3, w: h.w + 6, h: (h.h || h.w) + 6 })).filter(h => !(P.x > h.x - fr.w / 2 && P.x < h.x + h.w + fr.w / 2 && P.y > h.y - fr.h / 2 && P.y < h.y + h.h + fr.h / 2));
        // level-crossing gates: closed (or about to close) ones block the way for now
        const gates = G.hazards.filter(h => h.kind === 'barrier' && (h.closed || h.warn > 0)).map(h => ({ x: h.x - 2, y: h.y - 4, w: h.w + 4, h: h.h + 8 }));
        const gateAt = k => { if (!gates.length) return false; const [x, y] = posK(k); for (const f of [R.fp(curId(), x, y, 0), R.fp(curId(), x, y, 1)]) { let hit = false; for (const h of gates) if (f.x < h.x + h.w && f.x + f.w > h.x && f.y < h.y + h.h && f.y + f.h > h.y) { hit = true; break; } if (!hit) return false; } return true; };
        const hzAt = k => { if (!hz.length) return false; const [x, y] = posK(k), f = R.fp(curId(), x, y, (P.f === 0 || P.f === 2) ? 0 : 1); for (const h of hz) if (f.x < h.x + h.w && f.x + f.w > h.x && f.y < h.y + h.h && f.y + f.h > h.y) return true; return false; };
        for (let qi = 0; qi < q.length; qi++) { const k = q[qi], x = k % W2, y = (k / W2) | 0;
          if (qi > 0 && !(black.get(k) > now) && Math.hypot(x * STEP - P.x, y * STEP - P.y) >= minD && snowy(x * STEP, y * STEP)) { goal = k; break; }
          for (const [dx, dy] of dirs) { const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= W2 || ny >= H2) continue; const nk = ny * W2 + nx; if (prev[nk] !== -2) continue;
            if (dx && dy && (!okAt(nx * STEP, y * STEP) || !okAt(x * STEP, ny * STEP))) continue;
            if (okAt(nx * STEP, ny * STEP) && !gateAt(nk) && !(AVOID && hzAt(nk))) { prev[nk] = k; q.push(nk); } else prev[nk] = -3; } }
        curGoal = goal; plan = []; st.lastK0 = k0;
        if (goal < 0) { // boxed in on the planning grid (the real machine can sit between grid points): back out toward open space, then plan again
          st.escapes = (st.escapes || 0) + 1; const id = curId(); let best = null, bestN = -1;
          for (const [dx, dy] of D8) { let n = 0; for (let s = 1; s <= 6; s++) { const x = P.x + dx * s * 3, y = P.y + dy * s * 3; if (R.blk(R.fp(id, x, y, 0)) && R.blk(R.fp(id, x, y, 1))) break; n++; } if (n > bestN) { bestN = n; best = [dx, dy]; } }
          if (best && bestN > 0) plan = [[P.x + best[0] * bestN * 3, P.y + best[1] * bestN * 3]]; else { const a = Math.random() * 6.283; plan = [[P.x + Math.cos(a) * 12, P.y + Math.sin(a) * 12]]; }
          replanT = 0.5; return; }
        if (goal >= 0) { let k = goal; while (k >= 0 && k !== k0) { plan.push(posK(k)); k = prev[k]; } plan.reverse();
          const p2 = plan.length > 1 ? plan[plan.length - 2] : [P.x, P.y], b = plan[plan.length - 1], dx = Math.sign(b[0] - p2[0]), dy = Math.sign(b[1] - p2[1]);
          let dry = 0; for (let s = 1; s <= 70; s++) { const nx = b[0] + dx * STEP * s, ny = b[1] + dy * STEP * s; if (!okAt(nx, ny)) break; plan.push(posK(Math.round(ny / STEP) * W2 + Math.round(nx / STEP))); if (!snowy(nx, ny)) { if (++dry > 2) break; } else dry = 0; }
          replanT = 0.3 + plan.length / 60; } }
      while (plan.length && Math.hypot(plan[0][0] - P.x, plan[0][1] - P.y) < 2.5) plan.shift();
      // the nearest snow is right under us (the blade is out front): skip that spot for a few seconds
      if (!plan.length && curGoal >= 0) { black.set(curGoal, now + 3); replanT = 0; st.skips = (st.skips || 0) + 1; }
      for (const k of ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']) keys[k] = false;
      // steer: a loose dead zone while rolling, a tight one when pressed against something (lines a big machine up with a narrow gap)
      if (plan.length) { const dx = plan[0][0] - P.x, dy = plan[0][1] - P.y, dz = moved < 0.3 ? 0.25 : 1.2; if (dx > dz) keys.ArrowRight = true; if (dx < -dz) keys.ArrowLeft = true; if (dy > dz) keys.ArrowDown = true; if (dy < -dz) keys.ArrowUp = true; }
    };
    window.__botTick = tick; window.__botDbg = () => ({ k0: st.lastK0, W2, pw: G.pw, plan: plan.length, goal: curGoal, x: P.x, y: P.y, st, okHere: okAt(P.x, P.y), grid: [W2, H2] });
    const tStar = [null, null, null], T0 = run.time; let steps = 0, t;
    const maxSteps = Math.ceil((T0 + 20) * 30);
    while (steps < maxSteps && !run.ended) {
      fakeMs += 1000 / 30; window.__STEP(1, 1 / 30, 0); steps++;
      if (run.offer) { EV('(()=>{run.offer=false;endRound(false);return 1;})()'); break; }
      const pct = G.cleared / G.clearable * 100; t = steps / 30;
      for (let s = 0; s < 3; s++) if (tStar[s] === null && pct >= L.stars[s]) tStar[s] = +t.toFixed(1);
    }
    window.__botTick = null; for (const k of ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown']) keys[k] = false;
    const pct = G.cleared / G.clearable * 100;
    Object.assign(out, { area: L.area, time: L.time, pct: +pct.toFixed(1), stars: L.stars.filter(q => pct >= q).length, tStar, sweep: !!run.swept, hits: (run.hits || 0) - st.hits0,
      stuck: st.stuck, stuckMax: +st.stuckMax.toFixed(1), stuckAt: st.stuckAt.slice(0, 4), replans: st.replans, drives: st.drives || 0, stalls: st.stalls || 0, skips: st.skips || 0, escapes: st.escapes || 0, steps });
  } catch (e) { out.err = String(e && e.stack || e).slice(0, 300); }
  Math.random = realRandom; performance.now = realNow; window.__botTick = null;
  try { window.__EV('(()=>{if(run&&!run.ended){run.ended=true;}G=null;state="map";return 1;})()'); } catch (e) {}
  return out;
};

(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  // job list and machines per job, read from the game itself
  const p0 = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage();
  await p0.goto(URL); await p0.waitForTimeout(800);
  const plan = await p0.evaluate(([JOBS, MACH]) => { const R = window.__SR, T = R.TOOLS.map(t => t.id), out = [];
    const areas = []; R.LEVELS.forEach(L => { if (!areas.includes(L.area) && !L.tool) areas.push(L.area); });
    const entry = {}; areas.forEach(a => { const g = R.LEVELS.find(L => L.area === a && L.gate); entry[a] = g ? T.indexOf(g.gate) : 0; });
    // the machine a typical player has when they arrive (same as the skip-ahead test saves: themepark super, ski snowcat, pass/north rotary)
    const ARRIVE = { suburbs: 'shovel', farm: 'tractor', city: 'truck', themepark: 'super', harbour: 'loader', ski: 'snowcat', pass: 'rotary', north: 'rotary' };
    areas.forEach((a, k) => { if (ARRIVE[a] && T.includes(ARRIVE[a])) entry[a] = T.indexOf(ARRIVE[a]); else if (k && entry[a] <= 0) entry[a] = Math.max(0, entry[areas[k - 1]]); });
    R.LEVELS.forEach(L => { if (L.id === 'farm_old') return; if (JOBS !== 'all' && !JOBS.split(',').includes(L.id)) return;
      let ms; if (L.tool) ms = [L.tool]; else { const e = Math.max(0, entry[L.area]); ms = [...new Set([e, e + 1, e + 2, T.indexOf('icebreaker'), T.indexOf('ufo')].filter(x => x >= 0 && x < T.length))].map(x => T[x]); }
      (MACH === 'entry' ? ms.slice(0, 1) : ms).forEach(m => out.push([L.id, m, L.area])); });
    return { runs: out, entry }; }, [JOBS, MACH]);
  await p0.context().close();
  console.log('runs', plan.runs.length, 'entry machine per area', JSON.stringify(plan.entry));
  const runs = []; plan.runs.forEach(r => { for (let sd = 0; sd < SEEDS; sd++) runs.push([r[0], r[1], sd, r[2]]); });
  const queue = runs.map((r, k) => ({ r, k })), raw = new Array(queue.length); let done = 0; const t0 = Date.now();
  const worker = async () => {
    let page = null, used = 0;
    const fresh = async () => { if (page) await page.context().close(); page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage();
      page.on('pageerror', e => { if (page.__cur) page.__cur.pageErr = (page.__cur.pageErr || '') + e.message.slice(0, 160) + ' | '; });
      await page.goto(URL); await page.waitForTimeout(500); used = 0; };
    await fresh();
    while (queue.length) { const { r, k } = queue.shift(); if (used >= 1) await fresh(); used++;
      const cur = {}; page.__cur = cur; let res;
      try { const lv = LV === 'arrive' ? (ARRIVE_LV[r[3]] ?? 3) : +LV; res = await page.evaluate(PLAY, [r[0], r[1], lv, seedOf(r[0] + '/' + r[1] + '/' + lv + (r[2] ? '/' + r[2] : '')), !!process.env.BOT_AVOID]); } catch (e) { res = { job: r[0], tool: r[1], lv: LV, err: 'page: ' + String(e).slice(0, 200) }; await fresh(); }
      if (cur.pageErr) res.err = (res.err || '') + cur.pageErr; raw[k] = res; done++;
      if (done % 25 === 0) console.log(`  ${done}/${runs.length}  ${Math.round((Date.now() - t0) / 1000)}s`); }
    if (page) await page.context().close(); };
  await Promise.all(Array.from({ length: WORKERS }, worker));
  await browser.close();
  // one row per job and machine: the median run of its seeds, with the spread
  const results = []; for (let i = 0; i < raw.length; i += SEEDS) { const g = raw.slice(i, i + SEEDS).filter(Boolean); if (!g.length) continue;
    const ok = g.filter(r => !r.err).sort((a, b) => a.pct - b.pct), m = ok.length ? ok[Math.floor((ok.length - 1) / 2)] : g[0];
    results.push(Object.assign({}, m, { seeds: g.length, lo: ok.length ? ok[0].pct : null, hi: ok.length ? ok[ok.length - 1].pct : null,
      stuckMax: Math.max(...g.map(r => r.stuckMax || 0)), stuckAt: (g.find(r => (r.stuckMax || 0) >= 3) || m).stuckAt, err: g.map(r => r.err).filter(Boolean).join(' | ') || null })); }
  fs.writeFileSync(OUT, JSON.stringify({ when: new Date().toISOString(), lv: LV, seeds: SEEDS, results, raw }, null, 0));

  // report
  const key = r => r.job + '/' + r.tool, base = fs.existsSync(BASE) ? Object.fromEntries(JSON.parse(fs.readFileSync(BASE)).results.map(r => [key(r), r])) : null;
  const flags = []; const pad = (s, n) => String(s).padEnd(n);
  console.log('\n' + pad('job', 14) + pad('area', 11) + pad('machine', 11) + pad('cleared', 9) + pad('stars', 6) + pad('star times', 18) + pad('hits', 6) + pad('stuck', 7) + 'notes');
  for (const r of results) { if (!r) continue; const notes = [];
    if (r.err) { notes.push('ERROR ' + r.err.slice(0, 80)); flags.push(['error', key(r), r.err.slice(0, 160)]); }
    if (r.seeds > 1 && r.lo != null) notes.push(`range ${r.lo}-${r.hi}%`);
    if (r.stuckMax >= 3) { notes.push('stuck ' + r.stuckMax + 's at ' + JSON.stringify(r.stuckAt[0] || [])); flags.push(['stuck', key(r), r.stuckMax + 's at ' + JSON.stringify(r.stuckAt)]); }
    if (base && base[key(r)] && !r.err) { const b = base[key(r)]; if (Math.abs(r.pct - b.pct) >= (SEEDS > 1 ? 15 : 10) || (SEEDS > 1 ? Math.abs(r.stars - b.stars) >= 1 && Math.abs(r.pct - b.pct) >= 8 : r.stars !== b.stars)) { notes.push(`was ${b.pct}% ${b.stars}*`); flags.push(['changed', key(r), `${b.pct}% ${b.stars}* -> ${r.pct}% ${r.stars}*`]); } }
    console.log(pad(r.job, 14) + pad(r.area || '', 11) + pad(r.tool, 11) + pad((r.pct ?? '-') + '%', 9) + pad(r.stars ?? '-', 6) + pad(JSON.stringify(r.tStar || []), 18) + pad(r.hits ?? '-', 6) + pad(r.stuck ?? '-', 7) + notes.join('; '));
  }
  // the entry machine should earn at least 1 star everywhere
  const byJob = {}; for (const r of results) if (r) (byJob[r.job] = byJob[r.job] || []).push(r);
  // a job much harder than the rest of its area for the arrival machine (the bot is weaker than people, so compare within the area, not to the stars)
  const areaPct = {}; for (const rs of (base ? Object.values(Object.values(base).reduce((m, r) => ((m[r.job] = m[r.job] || []).push(r), m), {})) : Object.values(byJob))) { const e = rs[0]; if (e && !e.err && e.area) (areaPct[e.area] = areaPct[e.area] || []).push(e.pct); }
  const med = a => { const v = a.slice().sort((x, y) => x - y); return v.length ? v[Math.floor(v.length / 2)] : 0; };
  for (const [job, rs] of Object.entries(byJob)) { const e = rs[0]; if (e && !e.err && e.area && areaPct[e.area] && areaPct[e.area].length > 3 && e.pct < 0.6 * med(areaPct[e.area])) flags.push(['much harder than its area', job + '/' + e.tool, e.pct + '% vs area median ' + med(areaPct[e.area]) + '%']); }
  console.log('\nFLAGS ' + flags.length); for (const f of flags) console.log('  ' + f.join(' :: '));
  console.log(`done ${raw.filter(Boolean).length} runs (${results.length} job/machine pairs x ${SEEDS} seeds) in ${Math.round((Date.now() - t0) / 1000)}s -> ${OUT}`);
})();
