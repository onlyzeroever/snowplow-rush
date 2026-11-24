// Records the real game for promo videos. The test bot plays one job (real hazards, timer and physics, stepped at an exact
// 30 frames a second, so the recording is smooth whatever the machine's speed). Every frame is saved as a PNG at the
// game's own pixel size (180 x H; scale it up later with nearest-neighbour so the pixels stay sharp), and every sound the
// game asks for is logged with its frame number, so tools/promo/mixaudio.py can rebuild the audio in sync.
//
//   node tools/promo/capture.js list                      job ids, areas, machines
//   node tools/promo/capture.js job=<id> tool=<id> [lv=6] [seed=1] [from=0] [secs=75] [every=1] [h=320]
//        [page=app6.html] [avoid=1] [coins=12480] [out=/home/claude/promo/work/<job>_<tool>_<seed>]
//
// Needs the local game server (python3 -m http.server 8765 in the folder with app6.html, its audio/ and ph/).
// from/secs are in seconds of job time; every=N keeps one frame in N (stills). h=320 is a 9:16 phone; up to 420 = taller.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const { PLAY, seedOf } = require('../audit/botplay.js');

const A = {}; for (const a of process.argv.slice(2)) { const i = a.indexOf('='); if (i < 0) A[a] = true; else A[a.slice(0, i)] = a.slice(i + 1); }
const PAGE = A.page || 'app6.html', URL = `http://127.0.0.1:8765/${PAGE}?test=1&review=all`;
const FPS = 30, LV = +(A.lv || 6), SEED = +(A.seed || 1), FROM = Math.round(+(A.from || 0) * FPS), TO = FROM + Math.round(+(A.secs || 75) * FPS);
const EVERY = +(A.every || 1), HH = +(A.h || 320), COINS = Math.round(+(A.coins || 12480));

(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--autoplay-policy=no-user-gesture-required'] });
  // the window's shape sets the game's height: 360 x 2H keeps the game column exactly 180 x H (no side margins)
  const ctx = await browser.newContext({ viewport: { width: 360, height: HH * 2 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errs = []; page.on('pageerror', e => errs.push(e.message.slice(0, 200)));
  await page.goto(URL); await page.waitForTimeout(900);
  if (A.list) {
    const l = await page.evaluate(() => ({ jobs: window.__SR.LEVELS.map(L => [L.id, L.area, L.name || '', L.time, L.tool || '']), tools: window.__SR.TOOLS.map(t => t.id) }));
    for (const j of l.jobs) console.log(j.join('  ')); console.log('machines:', l.tools.join(' ')); await browser.close(); return;
  }
  if (!A.job || !A.tool) { console.error('job=<id> tool=<id> needed (see: list)'); process.exit(1); }
  const OUT = A.out || `/home/claude/promo/work/${A.job}_${A.tool}_${SEED}`; fs.mkdirSync(OUT, { recursive: true });
  for (const f of fs.readdirSync(OUT)) if (/^f\d+\.png$/.test(f)) fs.unlinkSync(path.join(OUT, f));

  // log every sound call with the frame it happens on, and grab the game's own pixels after each step
  const meta = await page.evaluate(([from, to, every]) => {
    const EV = window.__EV; window.__snd = []; window.__frames = []; window.__pos = []; window.__fi = 0; window.__cv = EV('buf');
    // where the machine is on screen in each saved frame (split-screen layouts crop around it)
    const posNow = EV('(()=>()=>P&&G?[Math.round(P.x),Math.round(P.y-camY+VIEW_Y)]:[90,160])()');
    EV(`(()=>{const pb=playBuf;playBuf=function(n,v,r,p){window.__snd.push([window.__fi+1,'b',n,v==null?1:v,r||1,p||0]);return pb.apply(this,arguments);};
      const ls=loopSet;loopSet=function(n,g,r){window.__snd.push([window.__fi+1,'l',n,g,r||0]);return ls.apply(this,arguments);};
      const sl=stopLoops;stopLoops=function(){window.__snd.push([window.__fi+1,'s']);return sl.apply(this,arguments);};
      const tn=tone;tone=function(f,d,ty,v,s2,de){window.__snd.push([window.__fi+1,'t',f,d,ty||'square',v||0.1,s2||0,de||0]);return tn.apply(this,arguments);};
      const pm=playMusic;playMusic=function(w,f){window.__snd.push([window.__fi+1,'m',w]);return pm.apply(this,arguments);};return 1;})()`);
    window.__onStep = steps => {
      window.__fi = steps;
      if (steps > from && steps <= to && (steps - from - 1) % every === 0) { window.__frames.push(window.__cv.toDataURL('image/png')); window.__pos.push(posNow()); }
      if (steps >= to) throw new Error('capture done');
    };
    return JSON.parse(EV('JSON.stringify({W,H,SFX_VOL,SFX_LOOPS,MUSIC})'));
  }, [FROM, TO, EVERY]);

  // a believable wallet for the area (the review save has millions)
  await page.evaluate(c => window.__EV(`save.coins=${c};1`), COINS);
  const t0 = Date.now();
  const res = await page.evaluate(PLAY, [A.job, A.tool, LV, seedOf(A.job + '/' + A.tool + '/' + LV + '/' + SEED), A.avoid !== '0']);
  let n = 0;
  for (;;) {
    const chunk = await page.evaluate(() => window.__frames.splice(0, 60));
    if (!chunk.length) break;
    for (const d of chunk) fs.writeFileSync(path.join(OUT, 'f' + String(++n).padStart(5, '0') + '.png'), Buffer.from(d.slice(d.indexOf(',') + 1), 'base64'));
  }
  const snd = await page.evaluate(() => window.__snd);
  fs.writeFileSync(path.join(OUT, 'pos.json'), JSON.stringify(await page.evaluate(() => window.__pos)));
  const done = String(res.err || '').includes('capture done');
  const info = { page: PAGE, job: A.job, tool: A.tool, lv: LV, seed: SEED, fps: FPS / EVERY, every: EVERY, fromFrame: FROM, frames: n,
    W: meta.W, H: meta.H, result: done ? 'stopped at secs' : (res.err ? 'error: ' + res.err : 'job ended'), pct: res.pct, stars: res.stars, steps: res.steps,
    SFX_VOL: meta.SFX_VOL, SFX_LOOPS: meta.SFX_LOOPS, MUSIC: meta.MUSIC, pageErrors: errs };
  fs.writeFileSync(path.join(OUT, 'meta.json'), JSON.stringify(info, null, 1));
  fs.writeFileSync(path.join(OUT, 'sounds.json'), JSON.stringify(snd.filter(e => e[0] > FROM && e[0] <= TO).map(e => [e[0] - FROM - 1, ...e.slice(1)])));
  console.log(`${n} frames (${meta.W}x${meta.H}) + ${snd.length} sound calls -> ${OUT}  [${info.result}${res.pct != null ? ', cleared ' + res.pct + '%' : ''}] in ${Math.round((Date.now() - t0) / 1000)}s`);
  if (errs.length) console.log('page errors:', errs.slice(0, 3).join(' | '));
  await browser.close();
})();
