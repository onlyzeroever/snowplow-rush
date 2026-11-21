// p164 (lab): clock waits for the first move; fingertip on the first job; 70% three stars on jobs 1-3; two free continues
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/lab6.html?test=1'); await p.waitForTimeout(900);
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
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
