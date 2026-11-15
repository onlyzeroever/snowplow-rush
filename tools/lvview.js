// usage: node lvview.js defs.json outdir [ids,comma]  -> one PNG per job: snow view | ground + footprints view
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs');
let defs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); if (defs.jobs) { const o = {}; for (const j of defs.jobs) o[j.id] = { packId: j.id }; defs = o; } const out = process.argv[3]; const only = process.argv[4] ? process.argv[4].split(',') : null;
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errors = []; const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/' + (process.env.PAGE || 'index6.html') + '?test=1'); await page.waitForTimeout(600);
  for (const id of Object.keys(defs)) { if (only && !only.includes(id)) continue;
    const url = await page.evaluate(([def, clean, snowy]) => { const R = window.__SR; if (def.packId) { R.save.tut = true; R.save.story = { suburbs: true, farm: true, city: true, themepark: true, harbour: true, ski: true, pass: true, north: true }; R.startLevel(R.LEVELS.findIndex(L => L.id === def.packId)); } else R.testLevel(def, 2); const G = R.G, pw = G.pw, ph = G.ph;
      const c = document.createElement('canvas'); c.width = pw * 2 + 8; c.height = ph; const x = c.getContext('2d'); x.fillStyle = '#ff00ff'; x.fillRect(0, 0, c.width, ph);
      x.drawImage(G.canvas, 0, 0); const im = x.createImageData(pw, ph); for (let i = 0; i < pw * ph; i++) { im.data[i * 4] = G.ground[i * 3]; im.data[i * 4 + 1] = G.ground[i * 3 + 1]; im.data[i * 4 + 2] = G.ground[i * 3 + 2]; im.data[i * 4 + 3] = 255; } if (snowy) { const sn = x.getImageData(0, 0, pw, ph).data, cols = G.cols, rows = G.rows, T = G.type, S = new Int32Array((cols + 1) * (rows + 1));
        for (let yy = 0; yy < rows; yy++) { let rs = 0; for (let xx = 0; xx < cols; xx++) { rs += T[yy * cols + xx] === 9 ? 1 : 0; S[(yy + 1) * (cols + 1) + xx + 1] = S[yy * (cols + 1) + xx + 1] + rs; } }
        const near = (cx, cy, r) => { const x0 = Math.max(0, cx - r), y0 = Math.max(0, cy - r), x1 = Math.min(cols, cx + r + 1), y1 = Math.min(rows, cy + r + 1); return S[y1 * (cols + 1) + x1] - S[y0 * (cols + 1) + x1] - S[y1 * (cols + 1) + x0] + S[y0 * (cols + 1) + x0] > 0; };
        const hsh = (a, b) => { let h = (Math.imul(a, 374761393) + Math.imul(b, 668265263)) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
        const nz = (cx, cy) => { const fx = cx / 9, fy = cy / 9, ix = Math.floor(fx), iy = Math.floor(fy), tx = fx - ix, ty = fy - iy, a = hsh(ix, iy), b = hsh(ix + 1, iy), c2 = hsh(ix, iy + 1), d2 = hsh(ix + 1, iy + 1); return (a * (1 - tx) + b * tx) * (1 - ty) + (c2 * (1 - tx) + d2 * tx) * ty; };
        const keep = new Uint8Array(cols * rows); for (let cy = 0; cy < rows; cy++) for (let cx = 0; cx < cols; cx++) { const i = cy * cols + cx; keep[i] = T[i] === 9 || near(cx, cy, 2 + (hsh(cx, cy * 7) < 0.4 ? 1 : 0)) || cx < 2 || cx >= cols - 2 || nz(cx, cy) > 0.78 ? 1 : 0; }
        for (let cy = 0; cy < rows; cy++) for (let cx = 0; cx < cols; cx++) { const i = cy * cols + cx; for (let sy = 0; sy < 2; sy++) for (let sx = 0; sx < 2; sx++) { const px = cx * 2 + sx, py = cy * 2 + sy, o = (py * pw + px) * 4;
          if (keep[i]) { im.data[o] = sn[o]; im.data[o + 1] = sn[o + 1]; im.data[o + 2] = sn[o + 2]; if (sy === 1 && cy + 1 < rows && !keep[i + cols] && T[i] !== 9) { im.data[o] = 0xa6; im.data[o + 1] = 0xc2; im.data[o + 2] = 0xea; } }
          else if (sy === 0 && cy > 0 && keep[i - cols]) { im.data[o] *= 0.72; im.data[o + 1] *= 0.72; im.data[o + 2] *= 0.72; } } } }
      x.putImageData(im, pw + 8, 0);
      for (const d of G.decor) { x.drawImage(d.spr, d.x, d.y); x.drawImage(d.spr, pw + 8 + d.x, d.y); }
      const obs = G.obstacles.slice().sort((a, b) => a.base - b.base); const all = obs.concat(G.scenery || []).sort((a, b) => a.base - b.base); for (const o of all) { x.drawImage(o.spr, o.sx, o.sy); x.drawImage(o.spr, pw + 8 + o.sx, o.sy); } for (const o of (G.over || [])) { x.drawImage(o.spr, o.sx, o.sy); x.drawImage(o.spr, pw + 8 + o.sx, o.sy); }
      if (clean) return c.toDataURL(); x.strokeStyle = 'rgba(255,0,0,0.9)'; x.lineWidth = 1; for (const o of obs) x.strokeRect(pw + 8 + o.x + 0.5, o.y + 0.5, o.w - 1, o.h - 1);
      const hz = { dog: '#ff8800', thrower: '#ff00aa', ped: '#00ccff', cart: '#ffff00', pull: '#ff4444', taxi: '#ff0000', balls: '#d7f03a', cannon: '#00ffff' };
      for (const h of G.hazards) { x.fillStyle = hz[h.kind] || '#fff'; x.fillRect(pw + 8 + h.x, h.y, Math.max(4, h.w), Math.max(4, h.h)); x.fillRect(h.x, h.y, Math.max(4, h.w), Math.max(4, h.h)); }
      for (const cw of G.cows) { x.fillStyle = '#8b4513'; x.fillRect(pw + 8 + cw.x - 5, cw.y - 3, 10, 5); }
      for (const p of G.presents) { x.fillStyle = '#d8364b'; x.fillRect(pw + 8 + p.x - 2, p.y - 2, 4, 4); }
      for (const nb of G.neighbours) { x.fillStyle = 'rgba(255,79,163,0.5)'; for (const r of nb.rects) x.fillRect(pw + 8 + r[0], r[1], r[2], r[3]); }
      x.fillStyle = '#00ff00'; x.fillRect(pw + 8 + G.start.x - 3, G.start.y - 3, 6, 6); x.fillRect(G.start.x - 3, G.start.y - 3, 6, 6);
      return c.toDataURL(); }, [defs[id], !!process.env.CLEAN, !!process.env.SNOWY]);
    fs.writeFileSync(out + '/' + id + '.png', Buffer.from(url.split(',')[1], 'base64')); }
  console.log('errors', JSON.stringify(errors)); await browser.close(); })();
