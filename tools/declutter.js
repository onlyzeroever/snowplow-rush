// node declutter.js area.json [ids] -> for each job: drop the small props that choke a machine until every machine reaches >=97%.
// Prints the drops; writes <area>.json.drops.json  [[id,kind,x,y],...] which finish() applies.
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
let pack = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); if (!pack.jobs) pack = { jobs: Object.entries(pack).map(([id, d]) => Object.assign({ id }, d, { data: d })) }; const only = process.argv[3] ? process.argv[3].split(',') : null;
const TL = (process.env.TOOLS || '0,3,5,6,7,8,9,10,11,12').split(',').map(Number), MIN = +(process.env.MIN || 97), MINKID = +(process.env.MINKID || MIN);
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext()).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(700);
  const dropsF = process.argv[2] + '.drops.json'; let drops = fs.existsSync(dropsF) ? JSON.parse(fs.readFileSync(dropsF, 'utf8')) : [];
  for (const job of pack.jobs) { if (only && !only.includes(job.id)) continue;
    const res = await page.evaluate(([job, TL, MIN, MINKID]) => { const R = window.__SR; const def = Object.assign({}, job, job.data); delete def.data; const props = def.props.slice(); def.props = props;
      const SMALL = new Set(['bench', 'planter', 'trash', 'parasol', 'table', 'lamp', 'bollard', 'cone', 'hydrant', 'meter', 'bins', 'postbox', 'phonebox', 'news', 'stree', 'statue', 'flag', 'tlight', 'signpost', 'kiosk', 'barrel', 'crate', 'tires', 'speaker', 'lantpost', 'stonelamp', 'gnome', 'mailbox', 'snowman', 'hay', 'sacks', 'churn', 'trough', 'pole', 'rock', 'cairn', 'snowpole', 'warnsign', 'gatepole', 'mogul', 'iceblock', 'urn', 'lion', 'bikerack', 'pine', 'oak', 'bare', 'balloons', 'popcorn', 'cup', 'skip', 'works', 'pillar', 'signal', 'anchor', 'hut', 'gifts', 'polepost', 'icesculpt', 'reindeer', 'tent', 'dogsled', 'icecol', 'xmastree', 'solar', 'chevron', 'skirack', 'deckchair', 'firepit', 'trailmap', 'tub', 'booth', 'pots', 'nets', 'fishbox', 'pallet', 'lifering', 'mooring', 'buoy', 'arcade', 'claw', 'tub', 'swan', 'meter', 'clock', 'parasol', 'shelter', 'van', 'car']);
      const dropped = []; let last = null;
      for (let it = 0; it < 40; it++) { R.loadTestDef(def); const bad = []; const reach = {};
        for (const ti of TL) { const r = R.checkJob(0, ti, 0, 0); reach[R.TOOLS[ti].id] = r.reach; if (r.reach < (ti < 3 ? MINKID : MIN)) bad.push(ti); }
        last = reach; if (!bad.length) break;
        const r = R.checkJob(0, bad[bad.length - 1], 0, 0); const { C, g } = R.checkLast; const fr = [];
        for (let y = 0; y < g.rows; y++) for (let cx = 0; cx < g.cols; cx++) { const k = y * g.cols + cx; if (g.type[k] === 9 || C[y * (g.cols + 1) + cx] > 0) continue; let nb = false; for (let dy = -2; dy <= 2 && !nb; dy++) for (let dx = -2; dx <= 2; dx++) { const yy = y + dy, xx = cx + dx; if (yy >= 0 && xx >= 0 && yy < g.rows && xx < g.cols && g.type[yy * g.cols + xx] !== 9 && C[yy * (g.cols + 1) + xx] > 0) { nb = true; break; } } if (nb) fr.push([cx * 2 + 1, y * 2 + 1]); }
        let best = null;
        props.forEach((p, i) => { if (!SMALL.has(p[0])) return; const P2 = R.PROPS[p[0]]; if (!P2) return; const a = p[3] != null ? p[3] : P2.arg, f = P2.foot(a), x0 = p[1] + f[0], y0 = p[2] + f[1], x1 = x0 + f[2], y1 = y0 + f[3];
          let dmin = 1e9; for (const [fx, fy] of fr) { const dx = Math.max(x0 - fx, 0, fx - x1), dy = Math.max(y0 - fy, 0, fy - y1), dd = dx * dx + dy * dy; if (dd < dmin) dmin = dd; }
          if (Math.sqrt(dmin) <= 30 && (!best || dmin < best.d)) best = { i, d: dmin }; });
        if (!best) break; dropped.push(props[best.i].slice(0, 3)); props.splice(best.i, 1); }
      return { dropped, reach: last }; }, [job, TL, MIN, MINKID]);
    drops = drops.filter(d => d[0] !== job.id); for (const d of res.dropped) drops.push([job.id, d[0], d[1], d[2]]);
    const lo = Object.entries(res.reach).filter(([k, v]) => v < (['shovel', 'pusher', 'blower'].includes(k) ? MINKID : MIN)).map(([k, v]) => k + ':' + v);
    console.log(job.id.padEnd(12), 'dropped', res.dropped.length, JSON.stringify(res.dropped.map(d => d[0] + '@' + d[1] + ',' + d[2])), lo.length ? 'STILL LOW ' + lo.join(' ') : 'all >= ' + MIN); }
  fs.writeFileSync(dropsF, JSON.stringify(drops)); console.log('errors', JSON.stringify(errors)); await browser.close(); })();
