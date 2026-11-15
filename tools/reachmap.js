// node reachmap.js id,id toolIdx -> /home/claude/levels/out/reach_<id>.png : ground view, unreachable snow in red
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const ids = process.argv[2].split(','), ti = +(process.argv[3] || 0);
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  for (const id of ids) { const r = await page.evaluate(([id, ti]) => { const R = window.__SR, i = R.LEVELS.findIndex(L => L.id === id); const res = R.checkJob(i, ti, 0, 0); const { C, g } = R.checkLast;
      const c = document.createElement('canvas'); c.width = g.pw; c.height = g.ph; const x = c.getContext('2d'); const im = x.createImageData(g.pw, g.ph);
      for (let p = 0; p < g.pw * g.ph; p++) { im.data[p * 4] = g.ground[p * 3]; im.data[p * 4 + 1] = g.ground[p * 3 + 1]; im.data[p * 4 + 2] = g.ground[p * 3 + 2]; im.data[p * 4 + 3] = 255; } x.putImageData(im, 0, 0);
      for (const o of g.obstacles.concat(g.scenery || []).sort((a, b) => a.base - b.base)) x.drawImage(o.spr, o.sx, o.sy); x.fillStyle = 'rgba(20,20,40,0.45)'; for (let y = 0; y < g.rows; y++) for (let cx = 0; cx < g.cols; cx++) if (g.type[y * g.cols + cx] === 9) x.fillRect(cx * 2, y * 2, 2, 2);
      let miss = []; x.fillStyle = 'rgba(255,0,0,0.85)'; for (let y = 0; y < g.rows; y++) for (let cx = 0; cx < g.cols; cx++) { const k = y * g.cols + cx; if (g.type[k] !== 9 && C[y * (g.cols + 1) + cx] <= 0) { x.fillRect(cx * 2, y * 2, 2, 2); if (miss.length < 12 && (miss.length === 0 || Math.abs(miss[miss.length - 1][1] - y * 2) > 6 || Math.abs(miss[miss.length - 1][0] - cx * 2) > 10)) miss.push([cx * 2, y * 2]); } }
      const fr = []; x.fillStyle = '#ffff00'; for (let y = 0; y < g.rows; y++) for (let cx = 0; cx < g.cols; cx++) { const k = y * g.cols + cx; if (g.type[k] === 9 || C[y * (g.cols + 1) + cx] > 0) continue; let nb = false; for (let dy = -3; dy <= 3 && !nb; dy++) for (let dx = -3; dx <= 3; dx++) { const yy = y + dy, xx = cx + dx; if (yy >= 0 && xx >= 0 && yy < g.rows && xx < g.cols && g.type[yy * g.cols + xx] !== 9 && C[yy * (g.cols + 1) + xx] > 0) { nb = true; break; } } if (nb) { x.fillRect(cx * 2, y * 2, 2, 2); fr.push(y * 2); } }
      const ys = [...new Set(fr.map(v => Math.round(v / 40) * 40))]; miss = ys.slice(0, 20);
      x.fillStyle = '#00ff00'; x.fillRect(g.start.x - 3, g.start.y - 3, 6, 6); return { url: c.toDataURL(), reach: res.reach, miss }; }, [id, ti]);
    fs.writeFileSync('/home/claude/levels/out/reach_' + id + '.png', Buffer.from(r.url.split(',')[1], 'base64')); console.log(id, 'reach', r.reach.toFixed ? r.reach.toFixed(1) : r.reach, 'frontier y', JSON.stringify(r.miss)); }
  console.log('errors', JSON.stringify(errors)); await browser.close(); })();
