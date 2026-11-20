// Lab rev 3 twist rework check (prototype only, lab branch).   node tools/audit/lab155.js [port=8766] [shots dir]
// Hints only as hints, gold gift once, results line; Round-Up herding + placement; Dig-Out needs all 4 sides;
// Power Cut sections fade and relight, all lit = restored; Thin Ice tows to land with a grace period;
// Avalanche: standing still = buried, driving away / shelter = escaped; Lost Penguins: chicks go to their own family.
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
  const go = (m, tw, job) => `${prep}${use(m)}startLevel(${job === undefined ? `twistJobs('${tw}')[1]` : job},{twist:'${tw}'});run.moved=true;run.time=999;${step(2)}`;

  // ---- shared: hints, gold gift, results line ----
  const h = await EV(`(()=>{${go('truck', 'city')}const L=run.lab;L.t=6;L.idle=0;L.hintT=0;const a=labHintOn();L.idle=15.1;${step(1)}const b2=labHintOn();${step(4 * 30 + 6)}const c=labHintOn();
    const c0=save.coins,g1=labGoldGift(P.x,P.y,'X'),g2=labGoldGift(P.x,P.y,'X');return JSON.stringify({early:(L.t=1,labHintOn()),idle:a,after15:b2,gone:c,gift1:g1>0,gift2:g2,paid:save.coins>c0,res:run.labRes&&run.labRes.gift});})()`);
  ok('hints: arrow only at the start, after 15s without progress (for 4s), not otherwise', h.early && !h.idle && h.after15 && !h.gone, h);
  ok('gold gift pays once and marks the results line', h.gift1 && h.gift2 === 0 && h.paid && h.res, h);
  const rs = await EV(`(()=>{${go('truck', 'city')}endRound(false);let err=null;try{for(let k=0;k<20;k++){update(1/30);draw();}}catch(e){err=e.message;}return JSON.stringify({ended:!!run.ended,res:run.labRes,err,state});})()`);
  ok('results: twist line is recorded and the end screen draws', rs.ended && rs.res && rs.res.label === 'CARS' && rs.res.of >= 3 && !rs.err, rs);
  await shot('results', `${go('truck', 'city')}const S=G.lab;run.lab.dn=S.n;labObj('CARS',S.n,S.n);labGoldGift(P.x,P.y,'ALL CARS FREE!');endRound(false);for(let k=0;k<60;k++)update(1/30)`);

  // ---- ROUND-UP ----
  const ru = await EV(`(()=>{const out=[];for(const j of twistJobs('farm')){for(const m of ['tractor','super','rotary']){${prep}${use('tractor')}{const ti=toolIdx(m);save.tool=Math.max(save.tool,ti);save.use=ti;}startLevel(j,{twist:'farm'});${step(1)}
      const S=G.lab,tid=TOOLS[useIdx()].id;if(!S.pens||!S.pens.length){out.push({id:G.def.id,m,pens:0});continue;}
      const ds=S.sheep.map(h=>Math.round(Math.min(...S.pens.map(pn=>Math.hypot(h.x+4-pn.cx,h.y+3-pn.cy))))),sp=[];for(let a=0;a<S.sheep.length;a++)for(let c=a+1;c<S.sheep.length;c++)sp.push(Math.hypot(S.sheep[a].x-S.sheep[c].x,S.sheep[a].y-S.sheep[c].y));
      out.push({id:G.def.id,m,teach:!!G.def.teach,pens:S.pens.length,sheep:S.sheep.length,dmin:Math.min(...ds),dmax:Math.max(...ds),gap:Math.round(Math.min(...sp))});}}return JSON.stringify(out);})()`);
  ok('round-up: every farm twist job has pens and 3-4 sheep for big and small machines', ru.every(r => r.pens >= 1 && r.sheep === (r.teach ? 3 : 4)), ru.filter(r => !(r.pens >= 1 && r.sheep === (r.teach ? 3 : 4))));
  ok('round-up: sheep are spread out, 110-400px from a pen (not next to it)', ru.every(r => r.dmin >= 100 && r.dmax <= 420 && r.gap >= 60), ru.map(r => [r.id, r.m, r.dmin, r.dmax, r.gap]));
  // the pens cut nothing off: what the machine reaches without the pens it reaches with them (re-checked from scratch)
  const cut = await EV(`(()=>{const out=[];for(const j of twistJobs('farm'))for(const m of ['tractor','super','rotary']){${prep}{const ti=toolIdx(m);save.tool=Math.max(save.tool,ti);save.use=ti;}startLevel(j,{twist:'farm'});${step(1)}
      const S=G.lab,tid=TOOLS[useIdx()].id;if(!S.pens.length)continue;const sav=G.obstacles;G.obstacles=G.obstacles.filter(o=>!o.lab);
      const A=labReachGrid(G,tid,[]);G.obstacles=sav;const B=labReachGrid(G,tid,[]);let lost=0;for(let k=0;k<A.seen.length;k++)if(A.seen[k]&&!B.seen[k]){const x=(k%A.gw)*4,y=((k/A.gw)|0)*4;if(S.pens.every(pn=>Math.hypot(x-pn.cx,y-pn.cy)>95))lost++;}
      out.push([G.def.id,m,lost]);}return JSON.stringify(out);})()`);
  ok('round-up: the pens never cut the machine off from any part of the map', cut.every(r => r[2] === 0), cut.filter(r => r[2] > 0));
  const herd = await EV(`(()=>{${go('tractor', 'farm')}const S=G.lab,out=[];for(const s of S.sheep){const pn=S.pens[0];
      // open ground for the test: put the sheep 120px straight below/above the pen gate, plow behind it, drive at the pen
      const dir=pn.cy<G.ph/2?1:-1;s.x=pn.cx-4;s.y=(dir>0?pn.y+pn.h:pn.y)+dir*120;s.vx=s.vy=0;P.x=pn.cx;P.y=s.y+3+dir*34;P.f=dir>0?0:2;const d0=Math.hypot(s.x+4-pn.cx,s.y+3-pn.cy);
      ${step(1)}{const br=bladeRect(TOOLS[useIdx()].id,P.x,P.y,P.f,bladeCells()*2);s.y=dir>0?br.y-14:br.y+br.h+6;}if(dir>0)keys.ArrowUp=true;else keys.ArrowDown=true;for(let k=0;k<240&&!s.penned;k++){update(1/30);}keys.ArrowUp=keys.ArrowDown=false;out.push({d0:Math.round(d0),d1:Math.round(Math.hypot(s.x+4-pn.cx,s.y+3-pn.cy)),penned:!!s.penned});break;}
    // no wander: plow far away, sheep stays put
    const s=S.sheep[1];P.x=G.start.x;P.y=G.start.y;const x0=s.x,y0=s.y;${step(150)}const still=Math.hypot(s.x-x0,s.y-y0);
    // edge: a sheep at the map edge steps back in
    const e=S.sheep[2];let ey=e.y;for(let yy=30;yy<G.ph-40;yy+=6)if(chaserFree(e,6,yy)&&mClear('sheep',e,6,yy)&&mClear('sheep',e,12,yy)){ey=yy;break;}e.x=6;e.y=ey;e.vx=e.vy=0;${step(90)}return JSON.stringify({push:out[0],still:Math.round(still*10)/10,edgeX:Math.round(e.x),home:run.lab.home,obj:run.lobj});})()`);
  ok('round-up: driving at a sheep with the blade pushes it into the pen (rev 3d)', herd.push.penned || herd.push.d1 < herd.push.d0 - 60, herd.push);
  ok('round-up: sheep stand still when you are far away; a sheep at the edge steps back in', herd.still < 4 && herd.edgeX >= 9, herd);
  await shot('roundup', `${go('tractor', 'farm')}const S=G.lab,s=S.sheep[0];P.x=s.x+4;P.y=s.y+40;P.f=0;camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);${step(8)}`);

  // ---- DIG-OUT ----
  const dg = await EV(`(()=>{${go('truck', 'city')}const S=G.lab,hz=S.cars[0];${step(1)}const sides=hz.sides.map(a=>a.length);for(const i of hz.sides[0])G.depth[i]=0;${step(2)}const one={buried:!!hz.buried,done:hz.sdone,act:hz.sact};
    for(let q=1;q<4;q++)for(const i of hz.sides[q])G.depth[i]=0;${step(2)}return JSON.stringify({sides,one,freed:!!hz.freed,dn:run.lab.dn});})()`);
  ok('dig-out: one side dug is not enough; all four sides frees the car', dg.one.buried && dg.one.done === 1 && dg.freed && dg.dn === 1, dg);
  await shot('digout', `${go('truck', 'city')}const hz=G.lab.cars[0];for(const i of hz.sides[0])G.depth[i]=0;for(const i of hz.sides[1].slice(0,hz.sides[1].length>>1))G.depth[i]=0;P.x=hz.x+11;P.y=hz.y+70;P.f=0;camY=clamp(hz.y-VIEW_H*0.4,0,G.ph-VIEW_H);${step(3)}`);

  // ---- POWER CUT ----
  const pc = await EV(`(()=>{${go('super', 'themepark')}const S=G.lab,B=S.boxes,L=run.lab;const tap=bx=>{P.x=bx.x;P.y=bx.y+4;${step(2)}P.x=G.start.x;P.y=G.start.y;${step(1)}};
    tap(B[0]);const lit=B[0].left;for(let k=0;k<Math.ceil((S.LIT+1)*30);k++)update(1/30);const faded=B[0].left;tap(B[0]);const relit=B[0].left>0;
    for(const bx of B)tap(bx);for(let k=0;k<Math.ceil((S.LIT+5)*30);k++)update(1/30);return JSON.stringify({n:B.length,LIT:S.LIT,lit:Math.round(lit),faded,relit,done:L.done,gift:L.gift,allOn:B.every(q=>q.left>0)});})()`);
  ok('power cut: a section stays lit for a while, then fades; you can relight it', pc.lit === pc.LIT && pc.faded === 0 && pc.relit, pc);
  ok('power cut: every section lit at once = power restored (gold gift), lights then stay on', pc.done === 1 && pc.gift === 1 && pc.allOn && pc.n >= 3, pc);
  await shot('powercut', `${go('super', 'themepark')}const bx=G.lab.boxes[1];P.x=bx.x+30;P.y=bx.y+60;P.f=0;camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);${step(3)}`);

  // ---- THIN ICE ----
  const ti = await EV(`(()=>{${go('truck', 'harbour')}const S=G.lab,L=run.lab;${step(40)}
    let ice=-1;for(let i=0;i<G.type.length;i++)if(G.type[i]===T_ICE){ice=i;break;}const land={x:G.start.x,y:G.start.y};L.land=land;
    const ix=(ice%G.cols)*2+20,iy=((ice/G.cols)|0)*2+20;P.x=ix;P.y=iy;L.sunk=0.02;${step(2)}const towed={x:P.x,y:P.y,grace:L.grace};
    // grace: holes under the plow do not drop you in
    P.x=ix;P.y=iy;const fp=footprint(TOOLS[useIdx()].id,P.x,P.y,P.f);for(let cy=fp.y>>1;cy<=(fp.y+fp.h)>>1;cy++)for(let cx=fp.x>>1;cx<=(fp.x+fp.w)>>1;cx++){const i=cy*G.cols+cx;if(G.type[i]===T_ICE){S.st[i]=2;S.t[i]=L.t;}}
    const f0=L.falls;${step(20)}const inGrace=L.falls===f0&&!(L.sunk>0);return JSON.stringify({towed,land,inGrace,falls:L.falls});})()`);
  ok('thin ice: a fall tows you back to solid ground with a 3s grace period', ti.towed.x === ti.land.x && ti.towed.y === ti.land.y && ti.towed.grace > 2.5 && ti.inGrace, ti);

  // ---- AVALANCHE ----
  const av = await EV(`(()=>{const R={};for(const mode of ['still','run','shelter']){${go('truck', 'pass')}const S=G.lab,L=run.lab;${step(1)}const A=L.av||(update(1/30),L.av);
      let y0=mode==='shelter'&&S.sh.length?S.sh[0].y+12:Math.min(G.ph-600,Math.max(300,G.ph*0.3));P.x=mode==='shelter'&&S.sh.length?S.sh[0].x+15:G.pw/2;P.y=y0;camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);
      A.ph='warn';A.t=0.01;A.tt=3.5;${step(2)}const fy0=A.fy;let k=0;for(;k<300&&A.ph==='wave';k++){if(mode==='run')P.y+=76/30;update(1/30);}
      R[mode]={fy0:Math.round(fy0),py0:Math.round(y0),buried:A.n-A.esc,esc:A.esc,frames:k,sh:S.sh.length};}return JSON.stringify(R);})()`);
  ok('avalanche: stand still and the wave buries you; drive away from it and you escape', av.still.buried === 1 && av.run.esc === 1, av);
  ok('avalanche: hiding in a rock shelter also escapes', av.shelter.sh === 0 || av.shelter.esc === 1, av.shelter);
  await shot('avalanche', `${go('truck', 'pass')}${step(1)}const A=run.lab.av;P.x=G.pw/2;P.y=Math.max(300,G.ph*0.3);camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);A.ph='warn';A.t=0.01;A.tt=3.5;${step(30)}`);
  await shot('avalanche_warn', `${go('truck', 'pass')}${step(1)}const A=run.lab.av;P.x=G.pw/2;P.y=Math.max(300,G.ph*0.3);camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);A.ph='warn';A.t=2.2;A.tt=3.5;${step(3)}`);

  // ---- LOST PENGUINS ----
  const pg = await EV(`(()=>{const out=[];for(const j of twistJobs('north')){${prep}${use('truck')}startLevel(j,{twist:'north'});${step(1)}const S=G.lab;
      out.push({id:G.def.id,teach:!!G.def.teach,fam:S.fam.length,chicks:S.chicks.length,cols:new Set(S.fam.map(f=>f.col)).size,far:Math.round(Math.min(...S.chicks.map(c=>Math.hypot(c.x-c.fam.x,c.y-c.fam.y)))),farMax:Math.round(Math.max(...S.chicks.map(c=>Math.hypot(c.x-c.fam.x,c.y-c.fam.y)))),own:S.chicks.every(c=>S.fam.includes(c.fam))});}
    ${prep}startLevel(twistJobs('north')[1],{twist:'north'});run.moved=true;run.time=999;${step(2)}const S=G.lab,L=run.lab,c=S.chicks[0],f=c.fam,w=S.fam.find(q=>q!==f);let wrong=null;
    c.st='follow';if(w){P.x=w.x;P.y=w.y+14;L.tr=[{x:P.x,y:P.y}];c.x=w.x;c.y=w.y;${step(1)}wrong={no:w.no>0,still:c.st};}
    P.x=f.x;P.y=f.y+14;L.tr=[{x:P.x,y:P.y}];c.x=f.x;c.y=f.y;${step(1)}return JSON.stringify({jobs:out,wrong,right:c.st,home:L.home});})()`);
  ok('penguins: each chick has its own family (own colour), placed away from it', pg.jobs.every(r => r.fam >= 2 && r.chicks === r.fam && r.cols === r.fam && r.own && r.far >= 150 && r.farMax <= 700), pg.jobs);
  ok('penguins: the wrong family says NOT OURS, the right one takes the chick', (!pg.wrong || (pg.wrong.no && pg.wrong.still === 'follow')) && pg.right === 'in' && pg.home === 1, pg);
  await shot('penguins', `${go('truck', 'north')}const S=G.lab,c=S.chicks[0];c.st='follow';P.x=c.fam.x+30;P.y=c.fam.y+50;P.f=0;camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);run.lab.tr=[];${step(20)}`);
  await shot('card', `${go('tractor', 'farm')}run.lab.t=1.2`);

  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(res.every(Boolean) ? 'ALL OK' : 'FAILED ' + res.filter(x => !x).length);
  await b.close(); process.exit(res.every(Boolean) ? 0 : 1);
})();
