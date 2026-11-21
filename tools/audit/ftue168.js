// p168 (live): clock waits for the first move; fingertip on the first job; 70% three stars on jobs 1-3; two free continues; + p169 locked WEEKLY/calendar placeholders
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/' + (process.argv[2]||'index6_ship.html') + '?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const t = await EV(`(()=>{window.__HOLD=1;save.tut=false;save.privSeen=true;save.ctrl='joy';startLevel(0,{});const t0=run.time;for(let k=0;k<90;k++)update(1/30);const t1=run.time;keys.ArrowUp=true;for(let k=0;k<30;k++)update(1/30);keys.ArrowUp=false;return JSON.stringify({t0,t1,t2:run.time,moved:run.moved});})()`);
  ok('the clock waits for the first move, then runs', t.t1 === t.t0 && t.t2 < t.t0 - 0.8 && t.moved, t);
  const st = await EV(`JSON.stringify(['driveway','culdesac','gardens','school'].map(id=>LEVELS.find(L=>L.id===id).stars[2]))`);
  ok('three stars at 70% on Driveway, Cul-de-sac, Gardens; School unchanged', st.join() === '70,70,70,85', st);
  const shot = async (n) => { const u = await p.evaluate(() => window.__EV('JSON.stringify(b.canvas.toDataURL())')); fs.writeFileSync('/tmp/audit/' + n + '.png', Buffer.from(JSON.parse(u).split(',')[1], 'base64')); };
  await EV(`(()=>{save.tut=false;startLevel(0,{});for(let k=0;k<12;k++)update(1/30);tNow=0.55;draw();return '1';})()`); await shot('ftue_a');
  await EV(`(()=>{tNow=1.05;draw();return '1';})()`); await shot('ftue_b');
  const c = await EV(`(()=>{save.pro=false;save.freeCont=0;const out=[];for(let n=0;n<3;n++){startLevel(0,{});run.moved=true;run.offer=true;run.time=0;draw();const u=ui.find(x=>x.id==='cont');out.push(u?u.label||u.text||u.t||'?':'none');u&&u.fn();out.push(String(!!adScreen)+':'+run.time);adScreen=null;}return JSON.stringify({out,free:save.freeCont});})()`);
  ok('the first two continues are free, the third is an ad', c.free === 2 && c.out[1] === 'false:15' && c.out[3] === 'false:15' && c.out[5].startsWith('true'), c);

  const nj = await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=1;save.best=save.best.map(()=>0);save.best[0]=62;save.stars=save.stars.map(()=>0);save.stars[0]=2;save.lastJob='driveway';save.dailyEver=false;goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;weeklyOpen=false;}catch(e){}draw();const w=ui.find(x=>x.id==='weeklyLock'),d=ui.find(x=>x.id==='dailyLock'),s1=ui.find(x=>x.id==='shopb');if(w)w.fn();return JSON.stringify({w:w&&[w.x,w.w],d:!!d,shop:s1&&[s1.x,s1.w],toast:toast&&toast.s,open:!!weeklyOpen,real:!!ui.find(x=>x.id==='weekly'||x.id==='daily'),nj:!!ui.find(x=>x.id==='nextjob')});})()`);
  ok('new player: WEEKLY and the calendar in place, locked; a tap says when they unlock', nj.w && nj.w[0] === 29 && nj.d && nj.shop[0] === 95 && /UNLOCK IN 3 JOBS/.test(nj.toast || '') && !nj.open && !nj.real && !nj.nj, nj);
  const rg = await EV(`(()=>{save.fbRuns=8;save.dailyEver=true;goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;}catch(e){}draw();return JSON.stringify({wk:!!ui.find(x=>x.id==='weekly'),dy:!!ui.find(x=>x.id==='daily'),locks:!!ui.find(x=>x.id==='weeklyLock'||x.id==='dailyLock')});})()`);
  ok('regular player: the real WEEKLY and calendar, no locks', rg.wk && rg.dy && !rg.locks, rg);
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
