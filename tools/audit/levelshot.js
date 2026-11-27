// Whole-map picture of one job (the full height, stitched from the game's own camera views).
//   node tools/audit/levelshot.js job=<id> [tool=truck] [page=app6.html] [play=0] [out=/tmp/level_<job>.png]
// play=N lets the test bot play N seconds first (to see what is left after a run); the grandmas, cars and
// people are drawn where they are at that moment. Needs the local server on :8765.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { PLAY, seedOf } = require('./botplay.js');
const A = {}; for (const a of process.argv.slice(2)) { const i = a.indexOf('='); if (i > 0) A[a.slice(0, i)] = a.slice(i + 1); }
const PAGE = A.page || 'app6.html', TOOL = A.tool || 'truck', OUT = A.out || `/tmp/level_${A.job}.png`;
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ viewport: { width: 360, height: 640 } })).newPage();
  await page.goto(`http://127.0.0.1:8765/${PAGE}?test=1&review=all`); await page.waitForTimeout(900);
  const secs = +(A.play || 0);
  if (secs > 0) {
    await page.evaluate(n => { window.__onStep = s => { if (s >= n * 30) throw new Error('stop'); }; }, secs);
    await page.evaluate(PLAY, [A.job, TOOL, 4, seedOf(A.job + '/' + TOOL), true]);
    // PLAY ends the run when it stops; start it again from the saved state is not possible, so re-enter quickly:
  }
  const info = await page.evaluate(([job, tool, secs]) => {
    const R = window.__SR, EV = window.__EV;
    if (!secs) {
      const i = R.LEVELS.findIndex(L => L.id === job), ti = R.TOOLS.findIndex(t => t.id === tool);
      // same set-up as the bot (tools/audit/botplay.js PLAY): machine by index, story seen, no pop-ups
      EV(`(()=>{tNow=0;save.tut=true;save.privSeen=true;save.story=save.story||{};AREA_SEQ.forEach(a=>save.story[a]=true);save.dailyEver=true;offerOpen=null;
        save.tool=Math.max(save.tool,${Math.min(ti, 9)});save.rides=save.rides||{};if(${ti}>=10){save.rides['${tool}']=true;save.ibEver=true;}save.use=${ti};
        const m=mLv('${tool}');m.speed=4;m.size=4;save.lv.value=4;return 1;})()`);
      R.startLevel(i); window.__HOLD = true;
      window.__STEP(2, 1 / 30, 0);
    }
    return JSON.parse(EV('JSON.stringify({ph:G.ph,pw:G.pw,VIEW_Y,VIEW_H,H,nb:G.neighbours.map(n=>({x:n.x,y:n.y,path:n.path,rects:n.rects,state:n.state}))})'));
  }, [A.job, TOOL, secs]);
  const strips = [];
  for (let y = 0; y < info.ph; y += info.VIEW_H) {
    const cy = Math.min(y, info.ph - info.VIEW_H);
    const d = await page.evaluate(cy => { window.__EV(`camY=${cy};1`); window.__STEP(0, 0, 0); return window.__EV('buf').toDataURL('image/png'); }, cy);
    strips.push({ cy, d });
  }
  require('fs').writeFileSync(OUT + '.json', JSON.stringify({ ...info, strips: strips.map(s => s.cy) }));
  // stitch in node with a tiny canvas page
  const html = `<canvas id=c width=${info.pw} height=${info.ph}></canvas>`;
  const p2 = await (await browser.newContext()).newPage(); await p2.setContent(html);
  const png = await p2.evaluate(async ([strips, vy, vh]) => {
    const c = document.getElementById('c'), x = c.getContext('2d');
    for (const s of strips) { const im = new Image(); im.src = s.d; await im.decode(); x.drawImage(im, 0, vy, im.width, vh, 0, s.cy, im.width, vh); }
    return c.toDataURL('image/png');
  }, [strips, info.VIEW_Y, info.VIEW_H]);
  require('fs').writeFileSync(OUT, Buffer.from(png.split(',')[1], 'base64'));
  console.log(`${A.job}: ${info.pw}x${info.ph} -> ${OUT}; grandmas: ${JSON.stringify(info.nb.map(n => ({ at: [Math.round(n.x), Math.round(n.y)], to: n.path[n.path.length - 1], rects: n.rects })))}`);
  await browser.close();
})();
