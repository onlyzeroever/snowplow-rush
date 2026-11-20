// Lab rev 3c check: snowball rolled up from plowed snow, crumbling, edge slope; gate Time Attack; yeti keeps off the
// edges and leaps less; Snow Day ground fills back in; drift tiers; map-only menu; start facing into the map.
//   node tools/audit/lab158.js [port=8766] [shots dir]
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
  const ev = (k, m, j) => `${prep}${use(m || 'truck')}startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS['${k}'][${j || 0}]),{event:'lab-${k}'});run.moved=true;run.time=999;${step(2)}`;

  // ---- snowball ----
  const sb = await EV(`(()=>{${ev('snowroll', 'truck', 1)}const L=run.lab;P.f=2;keys.ArrowDown=true;let k=0;for(;k<120&&!L.ball;k++)update(1/30);keys.ArrowDown=false;const formed=!!L.ball,sec=Math.round(k/3)/10;${step(20)}
    // a small ball wedged in a prop crumbles (no smash pay-out) and a new one needs plowing
    const o=G.obstacles.find(q=>q.w>=10&&q.h>=8)||G.obstacles[0];const B=L.ball;const n0=B.n;B.snow=10;B.r=6;B.x=o.x+o.w/2;B.y=o.y+o.h/2;B.vx=B.vy=0;${step(2)}const crumbled=L.gone>0,smashed=B.n>n0;${step(20)}const needs=L.need===1;
    // edge slope: a ball resting at the side rolls back toward the middle
    let spot=null;for(let y=60;y<G.ph-60&&!spot;y+=8)for(let x=30;x<=G.pw-30;x+=10)if(!blockedBy(footprint('truck',x,y,2))&&!rollHit({r:8},x,y+26)&&!rollHit({r:8},x,y+34)){spot={x,y};break;}if(!spot)spot={x:G.start.x,y:G.start.y};
    P.x=spot.x;P.y=spot.y;P.f=2;L.acc=ROLL_NEED;${step(1)}const C=L.ball;const fresh=C!==B&&L.need===0;let ey=-1,ex=0;for(let y=60;y<G.ph-60&&ey<0;y+=6)for(let x=Math.ceil(C.r)+3;x<=C.r+14;x+=2){let free=Math.abs(y-P.y)>60;for(let dx=0;dx<=20&&free;dx+=2)if(rollHit({r:C.r},x+dx,y))free=false;if(free){ey=y;ex=x;break;}}
    C.x=ex;C.y=ey;C.vx=C.vy=0;const trk=[];for(let k=0;k<30;k++){const g0=L.gone||0,n0=C.n;update(1/30);if((L.gone||0)>g0+0.01||C.n!==n0){const r3=C.r*0.82,bx3={x:C.x-r3,y:C.y-r3,w:r3*2,h:r3*2};trk.push(G.obstacles.filter(ob=>overlap(bx3,ob)).map(ob=>[Math.round(ob.x),Math.round(ob.y),ob.w,ob.h,!!ob.lab,ob.kind||'']));}if((L.gone||0)>g0+0.01||C.n!==n0)trk.push([k,Math.round(C.x),Math.round(C.y),Math.round(C.vx),Math.round(C.vy),L.gone,C.n-n0,Math.round(P.x),Math.round(P.y),Math.round(P.vx||0),Math.round(P.vy||0)]);}const moved=ey<0?-1:Math.round(C.x-ex);const dbg={trk,ex,ey,cx:Math.round(C.x),vx:Math.round(C.vx),gone:L.gone,need:L.need,same:L.ball===C,r:Math.round(C.r),px:Math.round(P.x),py:Math.round(P.y)};
    return JSON.stringify({formed,sec,crumbled,smashed,needs,fresh,moved,dbg});})()`);
  ok('snowball: plowing rolls one up', sb.formed && sb.sec <= 3, sb);
  ok('snowball: wedged in a prop it crumbles (no smash pay-out); then you plow a new one', sb.crumbled && !sb.smashed && sb.needs && sb.fresh, sb);
  ok('snowball: the map edge slopes it back toward the middle', sb.moved >= 4, sb);

  // ---- time attack gates ----
  const ta = await EV(`(()=>{const out=[];for(const job of LAB_JOBS.timeattack){${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id===job),{event:'lab-timeattack'});run.moved=true;run.time=999;${step(1)}const S=G.lab;
      out.push({job,n:S.cps.length,gw:S.cps.every(c=>c.gw<=48),fair:S.cps.every((c,k)=>c.seg>=2),t0:G.def.time});}
    ${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id===LAB_JOBS.timeattack[1]),{event:'lab-timeattack'});run.moved=true;run.time=999;${step(1)}const S=G.lab,L=run.lab,c=S.cps[0];
    P.x=c.cx+c.gw;P.y=c.y-c.dir*3;${step(2)}P.y=c.y+c.dir*3;${step(2)}const outside=L.k;P.x=c.cx;P.y=c.y-c.dir*3;${step(2)}P.y=c.y+c.dir*3;${step(2)}return JSON.stringify({jobs:out,outside,inside:L.k});})()`);
  ok('time attack: 3+ gates per job, each 44px wide, times from the drivable path', ta.jobs.every(j => j.n >= 3 && j.gw && j.fair && j.t0 <= 45), ta.jobs);
  ok('time attack: driving past the side of a gate does not count, through it does', ta.outside === 0 && ta.inside === 1, ta);

  // ---- yeti keeps off the edges ----
  const ye = await EV(`(()=>{${ev('yetihunt', 'truck', 2)}const L=run.lab;for(let q=0;q<90&&!L.yeti;q++)update(1/30);const Y=L.yeti;let edge=0,n=0;
    for(let r=0;r<4;r++){Y.x=G.pw/2-8;Y.y=Math.min(G.ph-260,300+r*120);Y.leap=null;Y.vx=Y.vy=0;P.x=G.pw/2+(r%2?-30:30);P.y=Y.y+(r<2?60:-60);
      for(let k=0;k<120;k++){const ang=k/20;P.x=clamp(Y.x+8+Math.cos(ang+r)*55,20,G.pw-20);P.y=clamp(Y.y+4+Math.sin(ang+r)*55,30,G.ph-30);P.inv=9;Y.inv=9;update(1/30);n++;if(Y.x<14||Y.x+Y.w>G.pw-14)edge++;}}
    return JSON.stringify({edgeShare:Math.round(edge/n*100)});})()`);
  ok('yeti: spends little time hugging the map sides', ye.edgeShare <= 25, ye);

  // ---- snow day: cleared ground fills back in where you are ----
  const sd = await EV(`(()=>{${ev('snowday')}const y0=Math.floor(camY/2)+10,y1=y0+40;let n=0;for(let cy=y0;cy<y1;cy++)for(let cx=0;cx<G.cols;cx++){const i=cy*G.cols+cx;if(G.type[i]!==T_BLOCK&&!(G.nc&&G.nc[i])){setDepth(G,i,0);n++;}}
    P.x=G.pw/2;P.y=camY+VIEW_H*0.6;${step(30 * 12)}let back=0;for(let cy=y0;cy<y1;cy++)for(let cx=0;cx<G.cols;cx++){const i=cy*G.cols+cx;if(G.type[i]!==T_BLOCK&&!(G.nc&&G.nc[i])&&G.depth[i]>=CLEAR_T)back++;}return JSON.stringify({n,back:Math.round(back/n*100)});})()`);
  ok('snow day: cleared ground in view fills back in (about half within 12s)', sd.back >= 25 && sd.back <= 80, sd);

  // ---- drift tiers ----
  const dr = await EV(`(()=>JSON.stringify([0.4,0.6,1.2,1.9].map(d=>driftTier(d))))()`);
  ok('drift: blue at 0.5, orange at 1.1, purple at 1.8 (was 0.6 / 1.6 / 3)', JSON.stringify(dr) === '[0,1,2,3]', dr);

  // ---- map only, start facing ----
  const mf = await EV(`(()=>{save.mapView='list';state='map';ui=[];draw();const ids=ui.map(u=>u.id);const out={view:save.mapView,toggle:ids.includes('vlist')||ids.includes('vmap'),shop:ids.includes('shopb')};
    const fs=[];for(let i=0;i<LEVELS.length;i++){const L=LEVELS[i];if(L.tool)continue;startLevel(i);fs.push([G.start.y>G.ph*0.5,P.f]);}out.bottomUp=fs.filter(q=>q[0]).every(q=>q[1]===0);out.topDown=fs.filter(q=>!q[0]).every(q=>q[1]===2);out.nBottom=fs.filter(q=>q[0]).length;state='map';return JSON.stringify(out);})()`);
  ok('menu: map only (no map/list switcher; a saved list view opens the map)', mf.view === 'map' && !mf.toggle && mf.shop, mf);
  ok('start: machines start facing into the map (up when the start is low)', mf.bottomUp && mf.topDown, mf);

  await shot('pill_presents', `${ev('presents')}run.lab.t=6;const g=G.lab.gp[0];P.x=g.x+30;P.y=g.y+20;${step(3)}`);
  await shot('ta_gate', `${ev('timeattack')}run.lab.t=6;const c=G.lab.cps[0];P.x=c.cx;P.y=c.y-c.dir*45;camY=clamp(P.y-VIEW_H*(c.dir>0?0.3:0.7),0,G.ph-VIEW_H);run.time=12.4;`);
  await shot('map_menu', `${prep}state='map';`);
  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(res.every(Boolean) ? 'ALL OK' : 'FAILED ' + res.filter(x => !x).length);
  await b.close(); process.exit(res.every(Boolean) ? 0 : 1);
})();
