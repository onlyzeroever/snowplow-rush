// Lab rev 3b check: hunted things move each run (course pieces stay), bonus twists for cruising players, avalanche boulders.
//   node tools/audit/lab157.js [port=8766] [shots dir]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const port = process.argv[2] || 8766, shots = process.argv[3] || '', base = 'http://127.0.0.1:' + port + '/lab6.html?test=1&lab&review=all';
const res = []; const ok = (name, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + name + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(base); await p.waitForTimeout(1000);
  const EV = code => p.evaluate(c => window.__EV(c), code).then(r => JSON.parse(r));
  const shot = async (name, code) => { if (!shots) return; const u = await p.evaluate(c => window.__EV(c), `(()=>{${code};draw();return JSON.stringify(b.canvas.toDataURL());})()`); fs.writeFileSync(shots + '/' + name + '.png', Buffer.from(JSON.parse(u).split(',')[1], 'base64')); };
  const prep = "save.privSeen=true;save.tut=true;save.fbRuns=8;window.__HOLD=1;for(const q in keys)keys[q]=false;";
  const use = m => `{const ti=toolIdx('${m}');save.tool=Math.max(save.tool,ti);save.use=ti;}`;
  const step = n => `for(let k=0;k<${n};k++)update(1/30);`;

  // ---- hunted things move each run, course pieces stay ----
  const rs = await EV(`(()=>{${prep}${use('truck')}const lay=(seed,fn)=>{window.__LABSEED=seed;fn();return JSON.stringify(cap());};let cap;const R={};
    const runOf=(fn,c)=>{cap=c;return [lay(1,fn),lay(2,fn)];};
    R.presents=runOf(()=>startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS.presents[1]),{event:'lab-presents'}),()=>G.lab.gp.map(q=>[q.x,q.y]));
    R.chicks=runOf(()=>startLevel(twistJobs('north')[1],{twist:'north'}),()=>G.lab.chicks.map(q=>[Math.round(q.x),Math.round(q.y)]));
    R.families=runOf(()=>startLevel(twistJobs('north')[1],{twist:'north'}),()=>G.lab.fam.map(q=>[Math.round(q.x),Math.round(q.y)]));
    R.sheep=runOf(()=>startLevel(twistJobs('farm')[1],{twist:'farm'}),()=>G.lab.sheep.map(q=>[q.x,q.y]));
    R.pens=runOf(()=>startLevel(twistJobs('farm')[1],{twist:'farm'}),()=>G.lab.pens.map(q=>[q.x,q.y]));
    R.cars=runOf(()=>startLevel(twistJobs('city')[1],{twist:'city'}),()=>G.lab.cars.map(q=>[q.x,q.y]));
    R.boxes=runOf(()=>startLevel(twistJobs('themepark')[1],{twist:'themepark'}),()=>G.lab.boxes.map(q=>[q.x,q.y]));
    R.n={gp:G.lab.boxes.length};window.__LABSEED=0;const out={};for(const k in R)if(Array.isArray(R[k]))out[k]=R[k][0]!==R[k][1];return JSON.stringify(out);})()`);
  ok('random each run: golden presents, lost chicks, stray sheep', rs.presents && rs.chicks && rs.sheep, rs);
  ok('fixed: pens, penguin families, buried cars, power boxes', !rs.pens && !rs.families && !rs.cars && !rs.boxes, rs);
  // fairness holds on other seeds too: sheep within 110-420px of a pen, chicks with their own family, 5 golden presents
  const fair = await EV(`(()=>{${prep}${use('super')}const out=[];for(const seed of [7,77,777,7777]){window.__LABSEED=seed;
      startLevel(twistJobs('farm')[2],{twist:'farm'});const S=G.lab,ds=S.sheep.map(h=>Math.min(...S.pens.map(pn=>Math.hypot(h.x+4-pn.cx,h.y+3-pn.cy))));
      startLevel(twistJobs('north')[2],{twist:'north'});const T=G.lab,fd=T.chicks.map(c=>Math.hypot(c.x-c.fam.x,c.y-c.fam.y));
      startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS.presents[2]),{event:'lab-presents'});const gp=G.lab.gp.length;
      out.push({seed,sheep:S.sheep.length,dmin:Math.round(Math.min(...ds)),dmax:Math.round(Math.max(...ds)),chicks:T.chicks.length,fam:T.fam.length,fmin:Math.round(Math.min(...fd)),fmax:Math.round(Math.max(...fd)),gp});}
    window.__LABSEED=0;return JSON.stringify(out);})()`);
  ok('random spots stay fair on other seeds (distances, counts)', fair.every(r => r.sheep === 4 && r.dmin >= 100 && r.dmax <= 460 && r.chicks === r.fam && r.fmin >= 150 && r.fmax <= 700 && r.gp === 5), fair);

  // ---- bonus twists ----
  const bt = await EV(`(()=>{${prep}${use('tractor')}const farm=areaJobs('farm').filter(i=>!twistOf(i)&&!LEVELS[i].boss&&!LEVELS[i].tool);const j=farm[0];
    startLevel(j);const plain=G.def.mode||null;
    // cruising: two 3-star finishes, then the next plain job is a bonus twist
    window.__CRUISE=1;save.labCruise=0;for(let k=0;k<2;k++){startLevel(j);G.cleared=G.clearable;run.moved=true;endRound(true);}const cruise=save.labCruise;
    startLevel(j);const m1=G.def.mode,b1=G.def.bonusTwist,after=save.labCruise;run.lab=run.lab||{t:0};run.lab.t=1;let err=null;try{draw();}catch(e){err=e.message;}
    const c0=save.coins;const u=labUnit();labGoldGift(P.x,P.y,'X');const gift=Math.round((save.coins-c0)/u);
    // a poor run resets it
    save.labCruise=1;startLevel(j);G.cleared=0;run.moved=true;endRound(false);const reset=save.labCruise;
    // never on Suburbs, boss or Wild Ride jobs, or events
    save.labCruise=5;const sub=areaJobs('suburbs')[3];startLevel(sub);const ms=G.def.mode||null;startLevel(j,{event:'lab-goldrush'});const me=G.def.mode;window.__CRUISE=0;save.labCruise=0;
    return JSON.stringify({plain,cruise,m1,b1,after,err,gift,reset,ms,me});})()`);
  ok('bonus twist: two 3-star runs, then the next plain job gets the area twist with a bigger gold gift', bt.plain === null && bt.cruise === 2 && bt.m1 === 'roundup' && bt.b1 === 1 && bt.after === 0 && !bt.err && bt.gift === 7, bt);
  ok('bonus twist: a poor run resets it; never in Suburbs or on top of an event', bt.reset === 0 && bt.ms === null && bt.me === 'goldrush', bt);
  await shot('bonus_card', `${prep}${use('tractor')}window.__BONUS=1;startLevel(areaJobs('farm').filter(i=>!twistOf(i)&&!LEVELS[i].boss&&!LEVELS[i].tool)[1]);window.__BONUS=0;run.moved=true;${step(2)}run.lab.t=1.2`);

  // ---- avalanche boulders ----
  const av = await EV(`(()=>{${prep}${use('truck')}startLevel(twistJobs('pass')[1],{twist:'pass'});run.moved=true;run.time=999;${step(2)}const A=run.lab.av;P.x=G.pw/2;P.y=Math.min(G.ph-500,Math.max(300,G.ph*0.3));camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);
    A.ph='warn';A.t=0.01;A.tt=3.5;${step(45)}const n=(A.rk||[]).length,faster=(A.rk||[]).every(r=>r.vy>A.spd*1.3);let hit=false;const h0=run.hits;
    for(let k=0;k<60&&!hit;k++){const r=(A.rk||[]).find(q=>q.y>A.fy+10);if(r){P.inv=0;P.x=clamp(r.x,20,G.pw-20);P.y=r.y+10;}update(1/30);if(run.hits>h0)hit=true;}
    for(let k=0;k<30*14;k++)update(1/30);return JSON.stringify({n,faster,hit,left:(A.rk||[]).length,ph:A.ph});})()`);
  ok('avalanche: boulders tumble ahead of the wave, faster than it; one can hit you; they clear away', av.n >= 1 && av.faster && av.hit && av.left === 0, av);
  await shot('boulders', `${prep}${use('truck')}startLevel(twistJobs('pass')[1],{twist:'pass'});run.moved=true;run.time=999;${step(2)}const A=run.lab.av;P.x=G.pw/2;P.y=Math.min(G.ph-500,Math.max(300,G.ph*0.3));camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);A.ph='warn';A.t=0.01;A.tt=3.5;${step(40)};camY=clamp(A.fy-20,0,G.ph-VIEW_H)`);

  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(res.every(Boolean) ? 'ALL OK' : 'FAILED ' + res.filter(x => !x).length);
  await b.close(); process.exit(res.every(Boolean) ? 0 : 1);
})();
