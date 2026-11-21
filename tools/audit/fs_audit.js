// p183 full-screen checks at several screen shapes: layout numbers, taps land where things are drawn (nav, cards,
// shop), map drags from beside the map, steering from the side on wide screens, unfold/fold mid-job, no page errors
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const FILE = process.argv[2] || 'lab6.html';
let fails = 0; const ok = (n, c, d) => { console.log((c ? 'ok   ' : 'FAIL ') + n + (d !== undefined && !c ? ' ' + JSON.stringify(d) : '')); if (!c) fails++; };
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const shapes = [['16:9 phone', 360, 640, 0, 0, { H: 320, SCW: 180, COX: 0 }], ['iPhone with notch', 393, 852, 59, 34, { H: 348, COX: 0 }], ['20:9 Android', 412, 915, 0, 0, { H: 400 }],
    ['iPhone Duo open', 1000, 704, 0, 0, { H: 320, COX: 137 }], ['iPad portrait', 820, 1180, 24, 20, { H: 320 }], ['very tall', 360, 900, 0, 0, { H: 420 }]];
  const errs = [];
  for (const [nm, w, h, st, sb, exp] of shapes) {
    const ctx = await br.newContext({ viewport: { width: w, height: h }, hasTouch: false }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(nm + ': ' + e.message));
    await p.goto(`http://127.0.0.1:8766/${FILE}?test=1`); await p.waitForTimeout(800);
    if (st || sb) { await p.addStyleTag({ content: `#wrap{padding:${st}px 0 ${sb}px 0 !important}` }); await p.evaluate(() => window.dispatchEvent(new Event('resize'))); await p.waitForTimeout(250); }
    const EV = c => p.evaluate(x => window.__EV(x), c).then(r => { try { return JSON.parse(r); } catch (e) { return r; } });
    const L = await EV(`JSON.stringify({H,SCW,SCH,COX,COY,NAV_Y,VIEW_H,MAP_VH})`);
    ok(`${nm}: layout ${JSON.stringify(L)}`, Object.keys(exp).every(k => L[k] === exp[k]) && L.NAV_Y === L.H - 30 && L.VIEW_H === L.H - 62 && L.COY + L.H <= L.SCH && L.COX + 180 <= L.SCW, exp);
    // the canvas covers the whole window
    const r = await p.evaluate(() => { const c = document.getElementById('c').getBoundingClientRect(); return { l: c.left, t: c.top, w: c.width, h: c.height }; });
    ok(`${nm}: the game fills the window`, r.l <= 0.5 && r.t <= 0.5 && r.w >= w - 1 && r.h >= h - 1, r);
    const base = `save.privSeen=true;save.tut=true;save.fbRuns=14;save.sess=4;save.gems=120;save.coins=50000;for(let i=0;i<8;i++){save.best[i]=Math.max(save.best[i]||0,60);save.stars[i]=Math.max(save.stars[i]||0,2);}save.story={suburbs:true,farm:true};save.bank={g:150,seen:true,intro:true};goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;remindAsk=null;evOpen=false;bankOpen=false;passOpen=false;gotCard=null;shopOpen=false;weeklyOpen=false;settingsOpen=false;}catch(e){};`;
    const tapId = async (id) => { const u = await EV(`(()=>{draw();const u=ui.find(q=>q.id==='${id}');return JSON.stringify(u?{x:u.x,y:u.y,w:u.w,h:u.h,SCW,SCH,COX,COY}:null);})()`); if (!u) return false;
      const c = await p.evaluate(() => { const c = document.getElementById('c').getBoundingClientRect(); return { l: c.left, t: c.top, w: c.width, h: c.height }; });
      const px = c.l + (u.x + u.w / 2 + u.COX) / u.SCW * c.w, py = c.t + (u.y + u.h / 2 + u.COY) / u.SCH * c.h; await p.mouse.click(px, py); await p.waitForTimeout(250); return true; };
    // nav tap on the map
    await EV(`(()=>{${base}return 1;})()`); await p.waitForTimeout(400);
    ok(`${nm}: tapping UPGRADES in the bottom bar opens upgrades`, await tapId('nav-upg') && (await EV('state')) === 'upgrades');
    await EV(`(()=>{${base}return 1;})()`); await p.waitForTimeout(400);
    // a card in the middle of a tall screen: NOT NOW on the Snow Bank card
    await EV(`(()=>{bankOpen=true;return 1;})()`); await p.waitForTimeout(300);
    ok(`${nm}: NOT NOW on the Snow Bank card closes it`, await tapId('bankno') && (await EV('bankOpen')) === false);
    // the shop: DONE
    await EV(`(()=>{shopOpen=true;shopTab=0;return 1;})()`); await p.waitForTimeout(300);
    ok(`${nm}: DONE closes the shop`, await tapId('sclose') && (await EV('shopOpen')) === false);
    // a drag that starts beside the map (or on it) scrolls the map
    await EV(`(()=>{scrollY.map=Math.max(fogMinScroll(),MAP_H-MAP_VH-400);mapPan=null;mapFling=null;return 1;})()`); await p.waitForTimeout(250);
    const y0 = await EV('scrollY.map'); const sideX = L.COX > 20 ? 10 : w / 2; await p.mouse.move(sideX, h * 0.45); await p.mouse.down(); await p.mouse.move(sideX, h * 0.6, { steps: 6 }); await p.mouse.up(); await p.waitForTimeout(300);
    const y1 = await EV('scrollY.map'); ok(`${nm}: dragging ${L.COX > 20 ? 'beside' : 'on'} the map scrolls it`, Math.abs(y1 - y0) > 10, { y0, y1 });
    // a job: steer from the side margin on wide screens (or the middle), the plow moves
    await EV(`(()=>{save.ctrl='joy';startLevel(3,{});return 1;})()`); await p.waitForTimeout(3300);
    const pa = await EV(`JSON.stringify({x:P.x,y:P.y,cam:camY,st:state})`);
    const gx = L.COX > 20 ? 20 : w / 2, gy = h * 0.55; await p.mouse.move(gx, gy); await p.mouse.down(); await p.mouse.move(gx + 30, gy, { steps: 5 }); await p.waitForTimeout(700); await p.mouse.up();
    const pb = await EV(`JSON.stringify({x:P.x,y:P.y})`); ok(`${nm}: steering ${L.COX > 20 ? 'from beside the job' : 'in the job'} moves the plow`, pa.st === 'play' && Math.abs(pb.x - pa.x) > 3, { pa, pb });
    // a short job (driveway) sits in the middle of a tall view
    await EV(`(()=>{startLevel(0,{});return 1;})()`); await p.waitForTimeout(600);
    const sj = await EV(`JSON.stringify({cam:Math.round(camY),ph:G.ph,vh:VIEW_H})`); ok(`${nm}: a short job sits in the middle (camera ${sj.cam})`, sj.ph >= sj.vh ? sj.cam >= 0 : sj.cam === Math.round((sj.ph - sj.vh) / 2), sj);
    await ctx.close();
  }
  // unfold and fold in the middle of a job
  { const ctx = await br.newContext({ viewport: { width: 393, height: 852 } }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push('fold: ' + e.message));
    await p.goto(`http://127.0.0.1:8766/${FILE}?test=1`); await p.waitForTimeout(800); const EV = c => p.evaluate(x => window.__EV(x), c).then(r => { try { return JSON.parse(r); } catch (e) { return r; } });
    await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=12;startLevel(4,{});return 1;})()`); await p.waitForTimeout(3300);
    const a = await EV(`JSON.stringify({st:state,job:G.def.id,H,COX})`); await p.setViewportSize({ width: 1000, height: 704 }); await p.waitForTimeout(600);
    const c = await EV(`JSON.stringify({st:state,job:G.def.id,H,COX})`); await p.setViewportSize({ width: 393, height: 852 }); await p.waitForTimeout(600);
    const d = await EV(`JSON.stringify({st:state,job:G.def.id,H,COX})`);
    ok('unfold and fold mid-job: the job carries on and the layout follows ' + JSON.stringify([a.H, c.H, d.H, c.COX]), a.st === 'play' && c.st === 'play' && d.st === 'play' && a.job === d.job && a.H === 390 && c.H === 320 && c.COX > 100 && d.H === 390);
    await ctx.close(); }
  ok('no page errors', errs.length === 0, errs.slice(0, 4));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await br.close();
})();
