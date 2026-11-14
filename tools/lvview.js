// usage: node lvview.js defs.json outdir [ids,comma]  -> one PNG per job: snow view | ground + footprints view
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs');
const defs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); const out = process.argv[3]; const only = process.argv[4] ? process.argv[4].split(',') : null;
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(600);
  for (const id of Object.keys(defs)) { if (only && !only.includes(id)) continue;
    const url = await page.evaluate((def) => { const R = window.__SR; R.testLevel(def, 2); const G = R.G, pw = G.pw, ph = G.ph;
      const c = document.createElement('canvas'); c.width = pw * 2 + 8; c.height = ph; const x = c.getContext('2d'); x.fillStyle = '#ff00ff'; x.fillRect(0, 0, c.width, ph);
      x.drawImage(G.canvas, 0, 0); const im = x.createImageData(pw, ph); for (let i = 0; i < pw * ph; i++) { im.data[i * 4] = G.ground[i * 3]; im.data[i * 4 + 1] = G.ground[i * 3 + 1]; im.data[i * 4 + 2] = G.ground[i * 3 + 2]; im.data[i * 4 + 3] = 255; } x.putImageData(im, pw + 8, 0);
      for (const d of G.decor) { x.drawImage(d.spr, d.x, d.y); x.drawImage(d.spr, pw + 8 + d.x, d.y); }
      const obs = G.obstacles.slice().sort((a, b) => a.base - b.base); for (const o of obs) { x.drawImage(o.spr, o.sx, o.sy); x.drawImage(o.spr, pw + 8 + o.sx, o.sy); }
      x.strokeStyle = 'rgba(255,0,0,0.9)'; x.lineWidth = 1; for (const o of obs) x.strokeRect(pw + 8 + o.x + 0.5, o.y + 0.5, o.w - 1, o.h - 1);
      const hz = { dog: '#ff8800', thrower: '#ff00aa', ped: '#00ccff', cart: '#ffff00', pull: '#ff4444', taxi: '#ff0000', balls: '#d7f03a', cannon: '#00ffff' };
      for (const h of G.hazards) { x.fillStyle = hz[h.kind] || '#fff'; x.fillRect(pw + 8 + h.x, h.y, Math.max(4, h.w), Math.max(4, h.h)); x.fillRect(h.x, h.y, Math.max(4, h.w), Math.max(4, h.h)); }
      for (const cw of G.cows) { x.fillStyle = '#8b4513'; x.fillRect(pw + 8 + cw.x - 5, cw.y - 3, 10, 5); }
      for (const p of G.presents) { x.fillStyle = '#d8364b'; x.fillRect(pw + 8 + p.x - 2, p.y - 2, 4, 4); }
      for (const nb of G.neighbours) { x.fillStyle = 'rgba(255,79,163,0.5)'; for (const r of nb.rects) x.fillRect(pw + 8 + r[0], r[1], r[2], r[3]); }
      x.fillStyle = '#00ff00'; x.fillRect(pw + 8 + G.start.x - 3, G.start.y - 3, 6, 6); x.fillRect(G.start.x - 3, G.start.y - 3, 6, 6);
      return c.toDataURL(); }, defs[id]);
    fs.writeFileSync(out + '/' + id + '.png', Buffer.from(url.split(',')[1], 'base64')); }
  console.log('errors', JSON.stringify(errors)); await browser.close(); })();
