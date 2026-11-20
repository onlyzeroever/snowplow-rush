// Lab rev 3d check: blade-push sheep, Dig-Out without lines, old headlights, more slalom gates, no avalanche shelters,
// secret presents.   node tools/audit/lab159.js [port=8766] [shots dir]
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
  const tw = (a, m, j) => `${prep}${use(m || 'tractor')}startLevel(twistJobs('${a}')[${j || 1}],{twist:'${a}'});run.moved=true;run.time=999;${step(2)}`;

  // blade push: for each machine, a sheep set in front of the blade 110px from the pen gate goes in when you drive at the gate
  const rp = await EV(`(()=>{const out=[];for(const m of ['tractor','truck','super','rotary']){${tw('farm', 'tractor')}{const ti=toolIdx(m);save.tool=Math.max(save.tool,ti);save.use=ti;}startLevel(twistJobs('farm')[1],{twist:'farm'});run.moved=true;run.time=999;${step(2)}
      const S=G.lab,pn=S.pens[0],s=S.sheep[0],dir=pn.cy<G.ph/2?1:-1,gy=dir>0?pn.y+pn.h:pn.y;P.f=dir>0?0:2;P.x=pn.cx;const fp=footprint(TOOLS[useIdx()].id,0,0,P.f);
      // place the plow so its blade front is 110px from the gate, the sheep just ahead of the blade
      P.y=gy+dir*130;${step(1)}const br=bladeRect(TOOLS[useIdx()].id,P.x,P.y,P.f,bladeCells()*2);s.x=pn.cx-4;s.y=(dir>0?br.y-14:br.y+br.h+6);s.vx=s.vy=0;
      if(dir>0)keys.ArrowUp=true;else keys.ArrowDown=true;let k=0;for(;k<150&&!s.penned;k++)update(1/30);keys.ArrowUp=keys.ArrowDown=false;
      out.push({m,penned:!!s.penned,sec:Math.round(k/3)/10,left:Math.round(Math.hypot(s.x+4-pn.cx,s.y+3-pn.cy))});}return JSON.stringify(out);})()`);
  ok('round-up: a sheep ahead of the blade is pushed into the pen (every machine size)', rp.every(r => r.penned), rp);
  const side = await EV(`(()=>{${tw('farm')}const S=G.lab,s=S.sheep[1];P.f=0;P.x=G.pw/2;P.y=300;${step(1)}const br=bladeRect(TOOLS[useIdx()].id,P.x,P.y,P.f,bladeCells()*2);s.x=Math.round(br.x+br.w+4);s.y=P.y-6;s.vx=s.vy=0;const x0=s.x;keys.ArrowUp=true;${step(20)}keys.ArrowUp=false;
    return JSON.stringify({sidestep:Math.round(Math.abs(s.x-x0)),y:Math.round(s.y)});})()`);
  ok('round-up: a sheep beside the plow steps aside instead of riding the blade', side.sidestep >= 3, side);
  const fence = await EV(`(()=>{${tw('farm')}const S=G.lab,pn=S.pens[0],s=S.sheep[2];const dir=pn.cy<G.ph/2?1:-1;const fy=dir>0?pn.y+pn.h-1:pn.y+6;
    s.x=pn.x+2;s.y=fy+dir*6-3;s.vx=0;s.vy=-dir*30;P.x=G.pw/2;P.y=fy+dir*200;const x0=s.x;let k=0;for(;k<90&&!s.penned;k++){s.vy=s.vy||-dir*20;update(1/30);}return JSON.stringify({slid:Math.round(s.x-x0),penned:!!s.penned});})()`);
  ok('round-up: a sheep pushed against the pen fence slides toward the gate', fence.slid >= 6 || fence.penned, fence);

  const dg = await EV(`(()=>{${tw('city', 'truck')}const hz=G.lab.cars[0];for(const i of hz.sides[0])G.depth[i]=0;${step(2)}return JSON.stringify({top:dgK(hz,-3,-13),left:dgK(hz,-13,2),sd:hz.sdone});})()`);
  ok('dig-out: the dug side drift is gone, the others still there', dg.top < 0.05 && dg.left > 0.9 && dg.sd === 1, dg);
  const misc = await EV(`(()=>{const out={};${tw('ski', 'snowcat')}out.gates=G.lab.gates.length;${tw('pass', 'truck')}out.shelters=G.lab.sh.length;
    ${prep}startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS.presents[0]),{event:'lab-presents'});out.secret=typeof SECRETP!=='undefined'&&SECRETP.width===11;return JSON.stringify(out);})()`);
  ok('slalom has more gates; avalanche has no shelters; secret presents have their own sprite', misc.gates >= 6 && misc.shelters === 0 && misc.secret, misc);
  await shot('digout', `${tw('city', 'truck')}const hz=G.lab.cars[0];for(const i of hz.sides[0])G.depth[i]=0;for(const i of hz.sides[3])G.depth[i]=0;P.x=hz.x+11;P.y=hz.y+70;P.f=0;camY=clamp(hz.y-VIEW_H*0.4,0,G.ph-VIEW_H);run.lab.t=6;${step(2)}`);
  await shot('powercut', `${tw('themepark', 'super')}run.lab.t=6;const bx=G.lab.boxes[1];P.x=bx.x+30;P.y=bx.y+60;P.f=0;camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);${step(2)}`);
  await shot('roundup', `${tw('farm')}run.lab.t=6;const S=G.lab,pn=S.pens[0],s=S.sheep[0];const dir=pn.cy<G.ph/2?1:-1;P.f=dir>0?0:2;P.x=pn.cx;P.y=(dir>0?pn.y+pn.h:pn.y)+dir*90;${step(1)}const br=bladeRect(TOOLS[useIdx()].id,P.x,P.y,P.f,bladeCells()*2);s.x=pn.cx-4;s.y=(dir>0?br.y-14:br.y+br.h+6);camY=clamp(pn.cy-VIEW_H*0.5,0,G.ph-VIEW_H);if(dir>0)keys.ArrowUp=true;else keys.ArrowDown=true;${step(15)}keys.ArrowUp=keys.ArrowDown=false;`);
  await shot('secret', `${prep}startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS.presents[0]),{event:'lab-presents'});run.moved=true;run.time=999;${step(2)}run.lab.t=6;const g=G.lab.gp[0];for(const i of g.cells)G.depth[i]=0;P.x=g.x+30;P.y=g.y+40;camY=clamp(g.y-VIEW_H*0.5,0,G.ph-VIEW_H);${step(8)}`);
  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(res.every(Boolean) ? 'ALL OK' : 'FAILED ' + res.filter(x => !x).length);
  await b.close(); process.exit(res.every(Boolean) ? 0 : 1);
})();
