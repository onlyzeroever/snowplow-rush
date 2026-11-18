// p138 fixes from Alex's phone test (Nov 19): trolley, parked cars, grannies, light posts, snowballs, stacked messages. node tools/audit/fixes138.js
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(c => window.__EV(c), c);
  await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=8;save.tool=2;save.use=2;window.__HOLD=1;return 1;})()`);
  // trolley
  ok((await EV(`JSON.stringify([CART.width,CART.height,CARTL.width])`)) === '[14,12,14]', 'shopping trolley is a 14x12 side view, with a mirrored copy');
  // parked cars: full cycle, never driving back into the same spot straight away
  const car = JSON.parse(await EV(`(()=>{startLevel(LEVELS.findIndex(L=>L.id==='lot'));run.time=999;const h=G.hazards.find(h=>h.kind==='pull');P.x=h.x+11;P.y=h.home+90;h.t=0;
    const seen=[],blocks={};let last='';for(let i=0;i<30*40;i++){P.x=h.hx+60>170?h.hx-60:h.hx+60;P.y=h.home+90;update(1/30);if(h.state!==last){last=h.state;seen.push(last);
      const bx=Math.max(4,Math.min(170,(h.state==='leave'||h.state==='arrive'||h.state==='away')?h.x+11:h.hx+11)),by=(h.state==='leave'||h.state==='arrive'||h.state==='away')?h.home+44:h.y+12;blocks[last]=!!blockedBy({x:bx,y:by,w:4,h:4});}if(seen.length>9)break;}
    return JSON.stringify({seen,blocks});})()`));
  const want = ['warn', 'out', 'turn', 'leave', 'away', 'arrive', 'turn2', 'in', 'park'];
  ok(want.every(s => car.seen.includes(s)), 'parked car backs out, drives off, comes back and parks ' + car.seen.join('>'));
  ok(!car.blocks.leave && !car.blocks.away && !car.blocks.arrive, 'a car driving along the aisle or away does not block like a parked one ' + JSON.stringify(car.blocks));
  const honk = JSON.parse(await EV(`(()=>{const h=G.hazards.find(h=>h.kind==='pull');h.state='arrive';h.dir=1;h.x=h.hx-30;h.t=0;P.x=h.hx-10;P.y=h.home+44;const x0=h.x;floats.length=0;for(let i=0;i<10;i++)update(1/30);
    return JSON.stringify({moved:Math.round(h.x-x0),beep:floats.some(f=>f.s==='BEEP BEEP!')});})()`));
  ok(honk.moved === 0 && honk.beep, 'a car waits and beeps when you are in its way ' + JSON.stringify(honk));
  // grannies
  const gr = JSON.parse(await EV(`(()=>{startLevel(LEVELS.findIndex(L=>L.id==='maple'));run.time=999;const nb=G.neighbours[0];P.x=nb.x+20;P.y=nb.y+30;floats.length=0;for(let i=0;i<5;i++)update(1/30);
    const ln=nbLine(nb),r=ln?nbBubble(nb,ln):null;return JSON.stringify({asked:!!nb.asked,f:ln==='CLEAR MY PATH, DEAR!',inside:r?r.x>=0&&r.x+r.w<=W&&Math.abs(r.tx-nb.x)<=r.w/2:false,above:r?r.y+r.h<=nb.y-14:false});})()`));
  ok(gr.asked && gr.f && gr.inside && gr.above, 'a granny asks you to clear her path in a bubble above her head, kept on screen ' + JSON.stringify(gr));
  // posts under string lights that would hang in mid-air
  const posts = JSON.parse(await EV(`(()=>{camY=0;draw();const o=G.over.filter(o=>o.k==='lights'||o.k==='banner');return JSON.stringify(o.map(o=>[o.sx,o.spr.width,(o.posts||[]).length]));})()`));
  ok(posts.length > 0 && posts.some(o => o[2] > 0), 'string lights get a post where an end would float ' + JSON.stringify(posts));
  ok(posts.every(o => !(o[0] <= 3 && o[0] + o[1] >= 176) || o[2] === 0), 'no posts on lights that run edge to edge');
  // snowball in flight draws
  ok((await EV(`(()=>{const th=G.hazards.find(h=>h.kind==='thrower');th.ball={x0:th.sx,y0:th.sy,x1:P.x,y1:P.y,t:0.2,dur:0.8};try{draw();return 'ok';}catch(e){return String(e);}finally{th.ball=null;}})()`)) === 'ok', 'snowball in flight draws');
  // messages stack
  const st = JSON.parse(await EV(`(()=>{floats.length=0;addFloat(90,100,'COMBO OVER','#fff',1);addFloat(90,100,'DODGED!','#fff',1);addFloat(90,100,'+12','#fff',1);return JSON.stringify(floats.map(f=>Math.round(f.y)));})()`));
  ok(st[0] !== st[1] && st[2] === 100, 'two messages on one spot stack; coin numbers stay put ' + JSON.stringify(st));
  ok(errs.length === 0, 'no errors ' + JSON.stringify(errs.slice(0, 3)));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await b.close(); process.exit(fails ? 1 : 0);
})();
