const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c); const fails = []; const ok = (c, m) => { if (!c) fails.push(m); console.log((c ? 'ok   ' : 'FAIL ') + m); };
  const t1 = await EV(`(()=>{save.tut=true;save.ach={};save.skins={'super:4':true,'truck:4':true,'snowcat:4':true};save.outfits={classic:true,dino:true,elf:true};goMap();return !!save.ach.dressed;})()`);
  ok(t1, 'Dressed to Plow pays out when you are back on the map at 5/5');
  const t2 = await EV(`(()=>{save.tool=toolIdx('rotary');save.rides={monster:true,ufo:true};save.use=save.tool;_tc.k='';const own=[];for(let j=0;j<TOOLS.length;j++)if(owns(j))own.push(j);const seen=[];let u=useIdx();for(let k=0;k<own.length;k++){const pi=own.indexOf(u);u=own[(pi+1)%own.length];seen.push(TOOLS[u].id);}return seen.join(',');})()`);
  console.log('   picker cycle:', t2); ok(t2.includes('monster') && t2.includes('ufo'), 'job card picker reaches the Wild Rides');
  // UFO drift + on top: Main Street (cars)
  await EV(`(()=>{save.use=toolIdx('ufo');_tc.k='';})()`);
  await p.evaluate(() => { const R = window.__SR; R.startLevel(R.LEVELS.findIndex(L => L.id === 'street')); }); await p.waitForTimeout(3300);
  const d = await p.evaluate(() => { window.__HOLD = true; const K = window.__SR.keys; K.ArrowDown = true; window.__STEP(3, 1 / 30, 0); const v1 = window.__EV('Math.round(P.vy)'); window.__STEP(30, 1 / 30, 0); const v2 = window.__EV('Math.round(P.vy)'); K.ArrowDown = false; window.__STEP(3, 1 / 30, 0); const v3 = window.__EV('Math.round(P.vy)'); window.__HOLD = false; return [v1, v2, v3, window.__EV('Math.round(moveSpeed())')]; });
  console.log('   ufo vx after 0.1s / 1s / 0.1s after letting go, top speed:', JSON.stringify(d)); ok(d[0] < d[3] * 0.5 && d[1] > d[3] * 0.85 && d[2] > 10, 'UFO eases up to speed and drifts after letting go');
  // put the UFO over a parked car and screenshot
  const car = await EV(`(()=>{const o=G.obstacles.filter(o=>o.w>=12&&o.h>=18&&o.y>200).sort((a,b)=>b.w*b.h-a.w*a.h)[0];if(!o)return null;P.x=o.x+o.w/2;P.y=o.y+o.h/2+4;P.vx=0;P.vy=0;return [o.x,o.y,o.w,o.h];})()`);
  console.log('   car', JSON.stringify(car)); await p.evaluate(() => { window.__HOLD = true; window.__STEP(2, 1 / 30, 1); window.__HOLD = false; }); await p.waitForTimeout(200); await p.screenshot({ path: '/tmp/ufo_car.png' });
  // snowball hits the UFO
  const sb = await EV(`(()=>{const h={kind:'thrower',x:P.x+30,y:P.y,w:10,h:14,state:'cool',cd:9,ball:{t:0.99,dur:1,x0:P.x+30,y0:P.y,x1:P.x,y1:P.y}};G.hazards.push(h);const before=run.hits||0;P.inv=0;return before;})()`);
  await p.evaluate(() => { window.__HOLD = true; window.__STEP(2, 1 / 30, 0); window.__HOLD = false; });
  const sb2 = await EV('JSON.stringify({hits:run.hits||0,stun:P.stun>0})'); console.log('   snowball', sb, sb2); ok(JSON.parse(sb2).hits > sb, 'a thrown snowball hits the UFO');
  await EV('endRound(false)'); await p.waitForTimeout(300);
  await p.evaluate(() => window.__SR.goUpgrades()); await p.waitForTimeout(500); await p.screenshot({ path: '/tmp/upg_ride.png' });
  console.log(fails.length ? 'FAILS ' + fails.length : 'ALL OK', 'errors', JSON.stringify(errs)); await br.close(); })();
