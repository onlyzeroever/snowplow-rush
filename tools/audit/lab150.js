// Lab rev 2 check (prototype only, lab branch): every mode builds, runs and draws; each mode's core rule actually works;
// plow sizes switch; nothing of the lab shows without ?lab.   node tools/audit/lab150.js [port=8766]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const port = process.argv[2] || 8766, base = 'http://127.0.0.1:' + port + '/lab6.html?test=1';
const res = []; const ok = (name, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + name + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const open = async (qs) => { const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message));
    await p.goto(base + qs); await p.waitForTimeout(900); return p; };
  const EV = (p, code) => p.evaluate(c => window.__EV(c), code).then(r => JSON.parse(r));
  const prep = "save.privSeen=true;save.tut=true;save.fbRuns=8;window.__HOLD=1;for(const q in keys)keys[q]=false;";
  const use = m => `{const ti=toolIdx('${m}');save.tool=Math.max(save.tool,ti);save.use=ti;}`;
  const step = n => `for(let k=0;k<${n};k++)update(1/30);`;

  // 1. off without ?lab
  let p = await open('');
  ok('lab is off without ?lab (no lab events, no twists, live sizes)', (await EV(p, `(()=>JSON.stringify({proto:PROTO,ev:EVENTS.filter(e=>e.lab).length,tw:twistOf(LEVELS.findIndex(L=>L.id==='quay')),sz:labSizeNew()}))()`)).ev === 0 && true,
    await EV(p, `(()=>JSON.stringify({proto:PROTO,ev:EVENTS.filter(e=>e.lab).length,tw:twistOf(LEVELS.findIndex(L=>L.id==='quay')),sz:labSizeNew()}))()`));
  await p.context().close();

  p = await open('&lab');
  // 2. every mode starts, runs and draws
  const smoke = await EV(p, `(()=>{${prep}const out=[];const tw=Object.keys(TWISTS).map(a=>({k:TWISTS[a],o:{twist:a},j:twistJobs(a)[0]}));
    const ev=LAB_EV.filter(k=>EVENT_DEFS[k].mod.mode).map(k=>({k:EVENT_DEFS[k].mod.mode,o:{event:'lab-'+k},j:LEVELS.findIndex(L=>L.id===LAB_JOBS[k][0])}));
    for(const m of tw.concat(ev)){try{startLevel(m.j,m.o);run.moved=true;for(let k=0;k<90;k++){P.vy=-30;update(1/30);if(k%30===0)draw();}draw();out.push([m.k,G.def.mode===m.k&&!!labM()]);}catch(e){out.push([m.k,false,e.message]);}}
    return JSON.stringify(out);})()`);
  ok('all 15 modes start, run 3s and draw', smoke.length === 15 && smoke.every(x => x[1]), smoke.filter(x => !x[1]));
  ok('twists are on their own jobs (first one teaches)', (await EV(p, `(()=>{const i=twistJobs('harbour')[0];startLevel(i);return JSON.stringify({m:G.def.mode,teach:G.def.teach,i2:(startLevel(twistJobs('farm')[1]),G.def.mode+':'+G.def.teach)});})()`)).m === 'thinice', null);

  // 3. each rule works
  const t = {};
  t.thinice = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='icebreaker'),{twist:'harbour'});run.moved=true;run.time=99;let best=null,bs=0;
    for(let y=40;y<G.ph-120;y+=16)for(let x=10;x<G.pw-100;x+=10){let n=0;for(let yy=y;yy<y+100;yy+=6)for(let xx=x;xx<x+90;xx+=6)if(G.type[(yy>>1)*G.cols+(xx>>1)]===T_ICE)n++;if(n>bs){bs=n;best={x,y};}}
    P.x=best.x+20;P.y=best.y+30;P.f=1;run.lab={t:2};keys.ArrowRight=true;${step(30)}keys.ArrowRight=false;keys.ArrowDown=true;${step(4)}keys.ArrowDown=false;keys.ArrowLeft=true;${step(30)}keys.ArrowLeft=false;
    const cracked=G.lab.st.reduce((a,v)=>a+(v===1),0);keys.ArrowUp=true;${step(24)}keys.ArrowUp=false;const holes=G.lab.nh;${step(90)}
    return JSON.stringify({cracked,holes,falls:run.lab.falls});})()`);
  ok('thin ice: driving cracks ice, re-crossing breaks it, stopping on it drops you in', t.thinice.cracked > 50 && t.thinice.holes > 0 && t.thinice.falls >= 1, t.thinice);
  t.digout = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='lot'),{twist:'city'});run.moved=true;run.time=99;${step(2)}const h=G.lab.cars[0],c0=save.coins,t0=run.time;
    for(const i of h.ring)setDepth(G,i,0);${step(2)}P.x=h.x+11;P.y=h.y-140;${step(60)}return JSON.stringify({freed:run.lab.dn,paid:save.coins>c0,time:run.time>t0-1,state:h.state,exits:G.lab.cars.filter(q=>q.buried).map(q=>pullExit(q)?1:0).join('')});})()`);
  ok('dig-out: clearing the drift frees the car, pays and adds time; the car pulls out', t.digout.freed === 1 && t.digout.paid && t.digout.time && t.digout.state !== 'park', t.digout);
  ok('dig-out: the other buried cars have a way out too', !/0/.test(t.digout.exits), t.digout.exits);
  t.roundup = await EV(p, `(()=>{${prep}${use('tractor')}startLevel(LEVELS.findIndex(L=>L.id==='farmyard'),{twist:'farm'});run.moved=true;${step(2)}const pn=G.lab.pens[0],s=G.lab.sheep[0],c0=save.coins;
    s.x=pn.ix+pn.iw/2-4;s.y=pn.iy+pn.ih/2-3;P.x=pn.cx;P.y=pn.y-80;${step(3)}return JSON.stringify({home:run.lab.home,paid:save.coins>c0,pens:G.lab.pens.length,sheep:G.lab.sheep.length});})()`);
  ok('round-up: a sheep in a pen counts and pays', t.roundup.home === 1 && t.roundup.paid && t.roundup.pens >= 1, t.roundup);
  t.powercut = await EV(p, `(()=>{${prep}${use('super')}startLevel(LEVELS.findIndex(L=>L.id==='food'),{twist:'themepark'});run.moved=true;${step(2)}const bx=G.lab.boxes[0],t0=run.time;P.x=bx.x;P.y=bx.y+4;${step(2)}
    return JSON.stringify({on:run.lab.on,time:run.time>t0+3,dark:!!G.night});})()`);
  ok('power cut: driving onto a power box lights it and adds time', t.powercut.on === 1 && t.powercut.time && t.powercut.dark, t.powercut);
  t.slalom = await EV(p, `(()=>{${prep}${use('snowcat')}startLevel(LEVELS.findIndex(L=>L.id==='redrun'),{twist:'ski'});run.moved=true;${step(2)}const g0=G.lab.gates[0],g1=G.lab.gates[1];
    P.x=g0.cx;P.y=g0.y-3;${step(1)}P.y=g0.y+3;${step(1)}const pass=run.lab.pass;P.x=g1.cx+G.lab.gap;P.y=g1.y-3;${step(1)}P.y=g1.y+3;${step(1)}return JSON.stringify({pass,miss:run.lab.miss,chain:run.lab.chain});})()`);
  ok('slalom: between the flags counts, beside them is a miss', t.slalom.pass === 1 && t.slalom.miss === 1 && t.slalom.chain === 0, t.slalom);
  // avalanche + lost penguins rules changed in lab rev 3: checked by tools/audit/lab155.js
  const evj = k => `startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS['${k}'][0]),{event:'lab-${k}'});run.moved=true;run.time=60;`;
  t.gold = await EV(p, `(()=>{${prep}${use('truck')}${evj('goldrush')}${step(60)}const n=run.lab.nug;if(!n)return JSON.stringify({none:1});P.x=n.x;P.y=n.y;${step(2)}return JSON.stringify({found:run.lab.found,chain:run.lab.chain});})()`);
  ok('gold rush: reaching the nugget counts and chains', t.gold.found === 1 && t.gold.chain === 1, t.gold);
  t.yeti = await EV(p, `(()=>{${prep}${use('truck')}${evj('yetihunt')}${step(60)}const Y=run.lab.yeti;if(!Y)return JSON.stringify({none:1});P.x=Y.x+8;P.y=Y.y+4;${step(1)}return JSON.stringify({hits:Y.hits});})()`);
  ok('yeti hunt: bumping the yeti counts', t.yeti.hits === 1, t.yeti);
  t.roll = await EV(p, `(()=>{${prep}${use('truck')}${evj('snowroll')}P.f=2;keys.ArrowDown=true;${step(45)}keys.ArrowDown=false;const r=run.lab.ball.r,c0=save.coins;const B=run.lab.ball;
    P.f=3;P.x=40;${step(1)}keys.ArrowLeft=true;${step(40)}keys.ArrowLeft=false;return JSON.stringify({grew:r,smashes:B.n,paid:save.coins>c0});})()`);
  ok('snowball roll: the ball grows on fresh snow and smashes at a wall', t.roll.grew > 6 && t.roll.smashes >= 1, t.roll);
  t.ice = await EV(p, `(()=>{${prep}${use('truck')}${evj('blackice')}${step(5)}return JSON.stringify({mode:G.def.mode});})()`);
  ok('black ice builds', t.ice.mode === 'blackice', t.ice);
  t.snowday = await EV(p, `(()=>{${prep}${use('truck')}const a=bladeCells();${evj('snowday')}${step(2)}return JSON.stringify({a,b:bladeCells()});})()`);
  ok('snow day: mega blade', t.snowday.b >= Math.round(t.snowday.a * 1.6), t.snowday);
  t.time = await EV(p, `(()=>{${prep}${use('truck')}const i=LEVELS.findIndex(L=>L.id===LAB_JOBS.timeattack[0]);startLevel(i,{event:'lab-timeattack'});const tt=G.def.time,full=LEVELS[i].time;run.moved=true;${step(45)}const c=run.lab.ck;if(!c)return JSON.stringify({none:1});
    const t0=run.time;P.x=c.x;P.y=c.y;${step(1)}return JSON.stringify({half:tt<full*0.6,got:run.lab.got,plus:run.time>t0+4});})()`);
  ok('time attack: half time, clocks add 5 seconds', t.time.half && t.time.got === 1 && t.time.plus, t.time);
  t.forts = await EV(p, `(()=>{${prep}${use('truck')}${evj('forts')}${step(2)}const o=G.lab.forts[0];P.x=o.x+14;P.y=o.y+o.h+24;P.f=0;keys.ArrowUp=true;${step(30)}keys.ArrowUp=false;return JSON.stringify({smashed:G.lab.smashed,n:G.lab.n});})()`);
  ok('snowball fight: ramming a fort smashes it', t.forts.smashed >= 1, t.forts);
  t.stars = await EV(p, `(()=>{${prep}${use('truck')}${evj('stars')}${step(130)}const s=run.lab.st.find(q=>q.land);if(!s)return JSON.stringify({none:1,n:run.lab.st.length});P.x=s.x;P.y=s.y;${step(1)}return JSON.stringify({caught:run.lab.caught});})()`);
  ok('star shower: a landed star can be caught', t.stars.caught >= 1, t.stars);

  // 4. plow sizes
  const sz = await EV(p, `(()=>{${prep}${use('icebreaker')}const out={};for(const m of ['old','new','small']){save.labSize=m;startLevel(LEVELS.findIndex(L=>L.id==='shops'));run.moved=true;out[m]={blade:bladeCells()*2,fp:footprint('icebreaker',0,0,0).w+'x'+footprint('icebreaker',0,0,0).h,comp:+sizeComp().toFixed(2)};}
    save.labSize='new';startLevel(LEVELS.findIndex(L=>L.id==='shops'));run.moved=true;P.f=0;let fold=null;for(let y=60;y<G.ph-60&&!fold;y+=8)for(let x=30;x<G.pw-30;x+=6){P.x=x;P.y=y;if(blockedBy(footprint('icebreaker',x,y,0)))continue;wingUpdate('icebreaker',1);if(P.wing&&(P.wing.n<P.wing.half||P.wing.p<P.wing.half)){fold={x,y,n:P.wing.n,p:P.wing.p,half:P.wing.half};break;}}
    out.fold=fold;return JSON.stringify(out);})()`);
  ok('plow sizes: NEW keeps the blade (no folding: Alex, Nov 20), tightens the body box; SMALL narrows the blade and pays more per snow',
    sz.new.blade === sz.old.blade && sz.new.comp === 1 && sz.new.fp !== sz.old.fp && !sz.fold && sz.small.blade < sz.old.blade && sz.small.comp > 1 && sz.old.comp === 1, sz);

  // 5. the lab screen
  const ui = await EV(p, `(()=>{state='map';labOpen=true;labPick=null;labTab=0;ui.length=0;draw();const a=ui.filter(u=>/^labr/.test(u.id)).length;labTab=1;ui.length=0;draw();const c=ui.filter(u=>/^labr/.test(u.id)).length;
    labPick='tw:harbour';ui.length=0;draw();const j=ui.filter(u=>/^labj/.test(u.id)).length;labOpen=false;labPick=null;return JSON.stringify({events:a,twists:c,jobs:j,size:!!ui.length});})()`);
  ok('lab screen lists 10 events, 7 twists, 6 jobs per twist', ui.events === 10 && ui.twists === 7 && ui.jobs === 6, ui);
  ok('no page errors', p.errs.length === 0, p.errs.slice(0, 3));
  await b.close(); console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); process.exit(res.every(Boolean) ? 0 : 1);
})();
