// Lab rev 3 events check (prototype only, lab branch).   node tools/audit/lab156.js [port=8766] [shots dir]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const port = process.argv[2] || 8766, shots = process.argv[3] || '', base = 'http://127.0.0.1:' + port + '/'+(process.env.PAGE||'lab6.html')+'?test=1&lab&review=all';
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
  const ev = (k, m, j) => `${prep}${use(m || 'truck')}startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS['${k}'][${j || 0}]),{event:'lab-${k}'});run.moved=true;run.time=999;${step(2)}`;
  const late = `run.lab.t=6;`;

  // ---- PRESENT HUNT ----
  const ph = await EV(`(()=>{${ev('presents')}const S=G.lab,L=run.lab;const def=LEVELS[LEVELS.findIndex(q=>q.id===LAB_JOBS.presents[0])];const gifts=G.hazards.filter(h=>h.kind==='gift').length+(G.gifts?G.gifts.length:0);
    const out={n:S.gp.length,mode:G.def.mode,presents:G.def.presents,base:def.presents};const g0=S.gp[0];P.x=g0.x+60;P.y=g0.y;${step(2)}out.warm=L.nd<90;
    const c0=save.coins;for(const i of g0.cells)G.depth[i]=0;${step(2)}out.found=g0.found===1&&L.found===1;out.paid=save.coins>c0;
    for(const gp of S.gp)for(const i of gp.cells)G.depth[i]=0;${step(2)}out.all=L.found;out.gift=L.gift;return JSON.stringify(out);})()`);
  ok('present hunt: 5 golden presents buried, normal present count (not 4x)', ph.n === 5 && ph.mode === 'presenthunt' && ph.presents === ph.base, ph);
  ok('present hunt: plowing the spot digs one up and pays; all 5 = gold gift', ph.found && ph.paid && ph.all === 5 && ph.gift === 1, ph);
  await shot('presenthunt', `${ev('presents')}${late}const g0=G.lab.gp[1];P.x=g0.x+30;P.y=g0.y+30;P.f=0;camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);for(let k=0;k<12;k++){update(1/30);}G.lab.gp[1].ping=0.2`);

  // ---- GOLD RUSH ----
  const gr = await EV(`(()=>{${ev('goldrush')}const L=run.lab;let big=null,c0=0;for(let k=0;k<7;k++){for(let q=0;q<90&&!L.nug;q++)update(1/30);const n=L.nug;if(!n)break;if(n.big){big=n;c0=save.coins;}P.x=n.x;P.y=n.y;${step(2)}}
    return JSON.stringify({big:!!big,lodes:L.lodes||0,gift:L.gift,chain:L.chain,paid:save.coins>c0});})()`);
  ok('gold rush: a x6 chain brings the mother lode; it pays, gives the gold gift and restarts the chain', gr.big && gr.lodes === 1 && gr.gift === 1 && gr.chain === 0 && gr.paid, gr);

  // ---- YETI HUNT ----
  const yt = await EV(`(()=>{${ev('yetihunt')}const L=run.lab;for(let q=0;q<90&&!L.yeti;q++)update(1/30);const Y=L.yeti;if(!Y)return JSON.stringify({none:1});
    // top edge: put him at the top with the plow below: he never goes above y=24
    Y.x=G.pw/2;Y.y=30;P.x=G.pw/2;P.y=80;let minY=1e9;for(let k=0;k<90;k++){update(1/30);minY=Math.min(minY,Y.y);}
    // he runs away: plow 50px off, standing still, for 1.5s
    Y.x=G.pw/2-8;Y.y=Math.min(G.ph-200,600);Y.vx=Y.vy=0;Y.leap=null;P.x=G.pw/2;P.y=Y.y+50;P.vx=P.vy=0;const d0=Math.hypot(Y.x+8-P.x,Y.y+4-P.y);${step(45)}const d1=Math.hypot(Y.x+8-P.x,Y.y+4-P.y);
    // a bump: he leaps clear and you can't farm hits while he's stunned
    Y.leap=null;Y.inv=0;const yx=Y.x,yy=Y.y;P.x=Y.x+8;P.y=Y.y+4;${step(1)}const h1=Y.hits,leap=!!Y.leap;${step(3)}P.x=Y.x+8;P.y=Y.y+4;${step(1)}const h2=Y.hits;${step(30)}const away=Math.hypot(Y.x-yx,Y.y-yy);
    // five bumps: sack bursts, he gives up, leaves, comes back
    const c0=save.coins;for(let k=0;k<8&&Y.st==='run';k++){Y.leap=null;Y.inv=0;for(let f=0;f<4;f++){P.x=Y.x+8;P.y=Y.y+4;update(1/30);}}const give=Y.st,gifts=L.gifts.length,gift=L.gift;
    P.x=G.start.x;P.y=G.start.y;let left=false,back=false;for(let k=0;k<30*16;k++){update(1/30);if(L.yeti&&L.yeti.st==='gone')left=true;if(left&&L.yeti&&L.yeti.st==='run'){back=L.yeti.round;break;}}
    return JSON.stringify({minY:Math.round(minY),d0:Math.round(d0),d1:Math.round(d1),h1,leap,h2,away:Math.round(away),give,gifts,gift,left,back,paid:save.coins>c0});})()`);
  ok('yeti: never goes above the top edge', yt.minY >= 24, yt);
  ok('yeti: runs away when you come close', yt.d1 > yt.d0 + 15, yt);
  ok('yeti: a bump counts once, then he leaps clear (no pinning him)', yt.h1 === 1 && yt.leap && yt.h2 === 1 && yt.away >= 32, yt);
  ok('yeti: 5 bumps = sack bursts (presents), gold gift, he leaves and comes back for round 2', yt.give === 'give' && yt.gifts >= 8 && yt.gift === 1 && yt.left && yt.back === 2, yt);
  await shot('yeti', `${ev('yetihunt')}${late}for(let q=0;q<90&&!run.lab.yeti;q++)update(1/30);const Y=run.lab.yeti;P.x=Y.x+8;P.y=Y.y+60;P.f=0;camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);${step(6)}`);
  await shot('yeti_burst', `${ev('yetihunt')}${late}for(let q=0;q<90&&!run.lab.yeti;q++)update(1/30);const Y=run.lab.yeti;for(let k=0;k<8&&Y.st==='run';k++){Y.leap=null;Y.inv=0;for(let f=0;f<4;f++){P.x=Y.x+8;P.y=Y.y+4;update(1/30);}}P.y+=40;camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);${step(12)}`);

  // ---- SNOWBALL ROLL ----
  const sr = await EV(`(()=>{${ev('snowroll','truck',2)}const L=run.lab;${step(2)}L.acc=ROLL_NEED;${step(1)}const B=L.ball;
    // push it along (driving down), then stop: the ball rolls on by itself
    P.f=2;keys.ArrowDown=true;${step(30)}keys.ArrowDown=false;const bx=L.ball.x,by=L.ball.y;${step(20)}const rolled=Math.hypot(L.ball.x-bx,L.ball.y-by),grew=L.ball.r;
    // soft knock: a slow ball against a building loses chunks, no smash
    L.gone=0;if(!L.ball||L.ball.r==null)L.ball=rollSpawn(L,TOOLS[useIdx()].id);const B2=L.ball;const o=G.obstacles.find(q=>q.w>=16&&q.y>40&&q.x>14&&q.x+q.w<G.pw-14&&!rollHit({r:20},q.x+q.w/2,q.y+q.h+24)&&!rollHit({r:20},q.x+q.w/2,q.y+q.h+60));B2.snow=200;B2.r=Math.min(26,5+Math.sqrt(200)*0.3);B2.x=o.x+o.w/2;B2.y=o.y+o.h+B2.r*0.82+1.5;B2.vx=0;B2.vy=-26;P.x=B2.x;P.y=B2.y+60;const n0=B2.n;let smax=B2.snow;for(let k=0;k<10;k++){update(1/30);smax=Math.max(smax,B2.snow);}const soft={smash:B2.n>n0||L.gone>0,lost:B2.snow<smax*0.95};
    // hard hit: same ball, fast
    const B3=L.ball;B3.snow=400;B3.r=Math.min(26,5+Math.sqrt(400)*0.3);B3.x=o.x+o.w/2;B3.y=o.y+o.h+B3.r+3;B3.vx=0;B3.vy=-80;const c0=save.coins,n1=B3.n;${step(10)}const hard={smash:B3.n>n1,paid:save.coins>c0};
    return JSON.stringify({rolled:Math.round(rolled),grew:Math.round(grew*10)/10,soft,hard});})()`);
  ok('snowball roll: push it and it keeps rolling on its own, growing', sr.rolled >= 8 && sr.grew > 5, sr);
  ok('snowball roll: a soft knock breaks chunks off, a hard hit smashes and pays', !sr.soft.smash && sr.soft.lost && sr.hard.smash && sr.hard.paid, sr);
  await shot('snowroll', `${ev('snowroll','truck',2)}${late}run.lab.acc=ROLL_NEED;update(1/30);P.f=2;keys.ArrowDown=true;${step(40)}keys.ArrowDown=false;camY=clamp(P.y-VIEW_H*0.4,0,G.ph-VIEW_H);${step(3)}`);

  // ---- BLACK ICE ----
  const bi = await EV(`(()=>{${ev('blackice')}const L=run.lab;${step(2)}P.vx=P.vy=0;L.dr=3.2;L.tier=3;const c0=save.coins;${step(15)}const r1={paid:save.coins>c0,turbo:run.turbo>0.8,purp:L.purp,ch:L.ch};
    L.dr=1.2;L.tier=2;${step(15)}const r2={ch:L.ch};L.dr=3.1;${step(15)}L.dr=3.3;${step(15)}return JSON.stringify({r1,r2,purp:L.purp,gift:L.gift});})()`);
  ok('black ice: a purple drift pays and gives a mini-turbo; drifts back to back chain', bi.r1.paid && bi.r1.turbo && bi.r1.purp === 1 && bi.r2.ch === 2, bi);
  ok('black ice: 3 purple drifts = gold gift', bi.purp === 3 && bi.gift === 1, bi);

  // ---- SNOW DAY ----
  const sd = await EV(`(()=>{${ev('snowday')}const L=run.lab;${step(2)}const b0=bladeCells(),v0=G.def.value,sh0=(()=>{let m=0;for(let k=0;k<30;k++){update(1/30);m=Math.max(m,shake);}return m;})();
    L.meter=1.01;${step(1)}const b1=bladeCells(),v1=G.def.value,mega=L.mega>0;${step(8 * 30 + 6)}const b2=bladeCells(),v2=G.def.value;return JSON.stringify({b0,b1,b2,v0,v1,v2,mega,n:L.n,sh0});})()`);
  ok('snow day: normal blade until the meter fills; then 8s of mega blade at double coins; then back', sd.b1 > sd.b0 * 1.5 && sd.b2 === sd.b0 && sd.v1 === sd.v0 * 2 && sd.v2 === sd.v0 && sd.mega, sd);
  ok('snow day: no constant screen shake', sd.sh0 < 0.02, sd.sh0);

  // ---- TIME ATTACK ----
  const ta = await EV(`(()=>{delete save.labTA;const R=[];for(let run2=0;run2<2;run2++){${ev('timeattack')}const S=G.lab,L=run.lab;const t0=G.def.time;run.time=t0;const n=S.cps.length;const tr=[];
      for(let k=0;k<n;k++){const c=S.cps[k];const t1=run.time;P.x=c.cx;P.y=c.y-c.dir*3;${step(2)}P.x=c.cx;P.y=c.y+c.dir*3;${step(2)}tr.push({add:Math.round((run.time-t1)*10)/10,diff:c.diff==null?null:Math.round(c.diff*10)/10});for(let q=0;q<(run2?20:30);q++)update(1/30);}
      R.push({t0,n,route:S.cps.map(c=>c.cx+','+c.y+(c.dir>0?'v':'^')),tr:tr.slice(0,3),fin:L.fin,gift:L.gift,best:(save.labTA||{})[S.key]});}return JSON.stringify(R);})()`);
  ok('time attack: short start clock; each checkpoint adds time; the finish gives the gold gift and saves your splits', ta[0].t0 <= 40 && ta[0].n >= 3 && ta[0].tr.slice(0, Math.min(3, ta[0].n - 1)).every(x => x.add >= 3) && ta[0].fin === 1 && ta[0].gift === 1 && ta[0].best && ta[0].best.length === ta[0].n, ta[0]);
  ok('time attack: the next run shows splits against your best', ta[1].tr[1].diff !== null && ta[1].tr[1].diff < 0, ta[1].tr);
  await shot('timeattack', `${ev('timeattack')}${late}const c=G.lab.cps[0];run.time=7.3;P.x=c.cx;P.y=c.y-c.dir*40;camY=clamp(P.y-VIEW_H*0.5,0,G.ph-VIEW_H);${step(2)}`);

  // ---- SNOWBALL THROWERS ----
  const th = await EV(`(()=>{${ev('forts')}const kid=G.hazards.find(h=>h.kind==='thrower');if(!kid)return JSON.stringify({none:1});let good=0,n=0;
    for(let k=0;k<60;k++){kid.state='idle';kid.cd=0;kid.ball=null;kid.revenge=false;P.x=clamp(kid.sx+40,20,G.pw-20);P.y=kid.sy+50;P.vx=-30;P.vy=20;${step(1)}if(kid.state!=='wind')continue;n++;const T=0.7+0.55,px=P.x+P.vx*T,py=P.y-2+P.vy*T;if(Math.hypot(kid.tx-px,kid.ty-py)<8)good++;}
    // stand on the landing spot: splat
    run.moved=true;kid.state='idle';kid.cd=0;kid.ball=null;P.vx=P.vy=0;P.inv=0;P.x=clamp(kid.sx+30,20,G.pw-20);P.y=kid.sy+40;${step(1)}const tx=kid.tx,ty=kid.ty;P.x=tx;P.y=ty+2;for(let k=0;k<45;k++){P.vx=P.vy=0;P.x=tx;P.y=ty+2;update(1/30);}const splat=run.splat>0;
    // deflect: blade on the landing spot just before it lands
    kid.state='idle';kid.cd=0;kid.ball=null;kid.immune=0;P.inv=0;P.x=clamp(kid.sx+30,20,G.pw-20);P.y=kid.sy+60;P.vx=P.vy=0;${step(1)}let defl=false;for(let k=0;k<60&&kid.state!=='buried';k++){const bl=kid.ball;if(bl&&!bl.back&&bl.t/bl.dur>0.8){const br=bladeRect(TOOLS[useIdx()].id,P.x,P.y,P.f,bladeCells()*2);P.x+=bl.x1-(br.x+br.w/2);P.y+=bl.y1-(br.y+br.h/2);}update(1/30);if(kid.ball&&kid.ball.back)defl=true;}
    return JSON.stringify({n,good,share:Math.round(good/Math.max(1,n)*100),splat,defl,buried:kid.state==='buried'});})()`);
  ok('throwers: they aim ahead of you, with some misses (about 60-80% on target)', th.n >= 40 && th.share >= 50 && th.share <= 90, th);
  ok('throwers: a hit splats the screen; batting a ball back buries the kid', th.splat && th.defl && th.buried, th);
  await shot('splat', `${ev('forts')}${late}run.splat=1.2;splatFx();P.x=G.start.x;P.y=G.start.y;${step(2)}`);

  // ---- STAR SHOWER ----
  const ss = await EV(`(()=>{${ev('stars')}const L=run.lab;P.f=2;P.x=G.pw/2;P.y=Math.min(300,G.ph/2);P.vx=0;P.vy=0;L.t2=0.01;${step(2)}const st=L.st.map(q=>({dx:Math.round(q.x-P.x),dy:Math.round(q.y-P.y)}));
    let shooting=false;for(let k=0;k<3;k++){L.st=[];L.t2=0.01;${step(2)}if(L.ss)shooting=true;}const q=L.ss;let caught=false;if(q){q.t=1;const c0=save.coins;P.x=q.x;P.y=q.y;${step(1)}caught=!L.ss&&save.coins>c0;}
    return JSON.stringify({n:st.length,ahead:st.every(s=>s.dy>=40&&s.dy<=140&&Math.abs(s.dx)<40),st,shooting,caught});})()`);
  ok('star shower: six stars land in a pattern ahead of you', ss.n >= 5 && ss.ahead, ss);
  ok('star shower: every third shower has a shooting star you can catch', ss.shooting && ss.caught, ss);
  await shot('stars', `${ev('stars')}${late}P.f=0;P.x=G.pw/2;P.y=Math.max(200,G.ph/2);P.vx=0;P.vy=0;run.lab.t2=0.01;camY=clamp(P.y-VIEW_H*0.75,0,G.ph-VIEW_H);${step(40)}`);
  await shot('blackice', `${ev('blackice')}${late}run.lab.dr=2.2;P.x=G.pw/2;P.y=Math.max(200,G.ph/2);camY=clamp(P.y-VIEW_H*0.6,0,G.ph-VIEW_H);P.vx=50;P.vy=-20;`);
  await shot('snowday', `${ev('snowday')}${late}run.lab.meter=1.01;${step(10)}`);

  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(res.every(Boolean) ? 'ALL OK' : 'FAILED ' + res.filter(x => !x).length);
  await b.close(); process.exit(res.every(Boolean) ? 0 : 1);
})();
