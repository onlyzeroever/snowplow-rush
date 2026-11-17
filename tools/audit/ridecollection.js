// Wild Ride collection (p125): migration, scaling, getting rides before the Rotary, missions, garage and upgrades screens.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8765/index6.html';
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const fails = []; const ok = (c, m) => { if (!c) fails.push(m); console.log((c ? 'ok   ' : 'FAIL ') + m); };
  // 1. an old save that owns the Jet (index 9) migrates: Rotary is the best machine, Monster + Jet are rides, ride upgrades reset
  { const ctx = await br.newContext({ viewport: { width: 360, height: 640 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await ctx.addInitScript(() => { localStorage.setItem('snowplowRush.test', JSON.stringify({ v: 6, tv: 2, tut: true, coins: 1e6, tool: 9, use: 9, gems: 0, lv: { speed: 0, size: 0, value: 5, bumper: 0, helpers: 0 },
      mlv: { rotary: { speed: 6, size: 6, bumper: 4 }, monster: { speed: 6, size: 6, bumper: 5 }, jet: { speed: 3, size: 3, bumper: 2 } }, stars: [], best: [] })); });
    await p.goto(BASE + '?test=1'); await p.waitForTimeout(900);
    const m = await p.evaluate(() => { const s = window.__SR.save; const r = { tool: s.tool, use: s.use, rides: s.rides, monster: s.mlv.monster, jet: s.mlv.jet, inUse: window.__EV('tool().id') }; localStorage.removeItem('snowplowRush.test'); return r; });
    console.log('migrated', JSON.stringify(m));
    ok(m.tool === 7 && m.use === 9 && m.rides.monster && m.rides.jet && !m.rides.mech, 'old save: Rotary best machine, Monster + Jet owned as rides, Jet still in use');
    ok(m.monster.speed === 0 && m.monster.size === 0 && m.jet.size === 0, 'old save: ride upgrade levels reset (rides follow the best machine now)');
    ok(errs.length === 0, 'old save: no errors ' + JSON.stringify(errs));
    await ctx.close(); }
  const ctx = await br.newContext({ viewport: { width: 360, height: 640 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(BASE + '?test=1'); await p.waitForTimeout(1000);
  const EV = c => p.evaluate(x => window.__EV(x), c);
  // 2. scaling: every ride is +15% clearing and coins on the best machine, at any point in the ladder
  const sc = await EV(`(()=>{save.tut=true;const out=[];const rate=t=>moveSpeed()*bladeCells();for(const [best,lv] of [['super',[0,0]],['super',[6,6]],['snowcat',[3,3]],['rotary',[6,6]]]){
      save.tool=toolIdx(best);save.rides={};for(let i=BASE_TOOLS;i<TOOLS.length;i++)save.rides[TOOLS[i].id]=true;const q=mLv(best);q.speed=lv[0];q.size=lv[1];
      save.use=save.tool;_tc.k='';const r0=rate(),v0=valueMult();const row={best,lv:lv.join('/'),rate:Math.round(r0)};
      for(let i=BASE_TOOLS;i<TOOLS.length;i++){save.use=i;_tc.k='';row[TOOLS[i].id]=Math.round(100*rate()/r0)+'%/'+Math.round(100*valueMult()/v0)+'% w'+bladeCells()+' s'+Math.round(moveSpeed());}
      out.push(row);}return out;})()`);
  for (const r of sc) console.log(JSON.stringify(r));
  ok(sc.every(r => ['monster', 'jet', 'mech', 'dragon', 'ufo'].every(id => { const [a, b] = r[id].split(' ')[0].split('/').map(x => parseInt(x)); return a >= 111 && a <= 119 && b === 115; })), 'every ride clears ~15% faster (rounding of width) and earns exactly 15% more than the best machine');
  // 3. Super Plow owner: test drive tease, drive is scaled, offer after the run, buy with gems, owns it without skipping machines
  await EV(`(()=>{save.rides={};save.tool=toolIdx('super');save.use=save.tool;const q=mLv('super');q.speed=3;q.size=3;save.ridePass=false;save.rideSeen={};save.parts={};save.gems=500;_tc.k='';})()`);
  const t = await EV(`(()=>{let keys=0,parts=0;for(let k=0;k<40;k++){const g=buildLevel(lvIdx('carousel'));if(g.driveKey)keys++;if(g.part)parts++;}return {tease:teaseRideIdx(),parts:nextRideIdx(),keys,partsN:parts,sale:rideForSale()};})()`);
  console.log('super owner', JSON.stringify(t));
  ok(t.tease === 8 && t.parts === -1 && t.keys > 0 && t.partsN === 0, 'Super Plow owner: Monster test drives turn up, no parts yet');
  await p.evaluate(() => { const R = window.__SR; R.startLevel(R.LEVELS.findIndex(L => L.id === 'carousel')); }); await p.waitForTimeout(3300);
  const d = await EV(`(()=>{const sr=moveSpeed()*bladeCells();const ri=teaseRideIdx();G.driveKey={x:P.x,y:P.y,ri,taken:false};checkDrive({x:P.x-8,y:P.y-8,w:16,h:16},0.01);return {drive:run.drive,ratio:Math.round(100*moveSpeed()*bladeCells()/sr),cells:bladeCells(),seen:!!save.rideSeen.monster,sale:rideForSale()};})()`);
  console.log('drive', JSON.stringify(d));
  ok(d.drive === 'monster' && d.ratio >= 110 && d.ratio <= 120 && d.sale === 8, 'test drive: Monster at ~+15% on your Super Plow, then for sale');
  await p.evaluate(() => { window.__HOLD = true; window.__EV('run.driveT=0.01'); window.__STEP(30, 1 / 30, 0); window.__EV('endRound(false)'); window.__STEP(60, 1 / 30, 1); window.__HOLD = false; });
  await p.waitForTimeout(1500); await p.screenshot({ path: '/tmp/rc_offer.png' });
  const b = await EV(`(()=>{const ok=buyRide(8,true);return {ok,gems:save.gems,tool:save.tool,use:save.use,owns:owns(8),next:rideNextIdx(),machine:curMachine()};})()`);
  console.log('bought', JSON.stringify(b));
  ok(b.ok && b.gems <= 310 && b.gems >= 300 && b.tool === 5 && b.use === 8 && b.owns && b.next === 9 && b.machine === 'super', 'gems buy before the Rotary: ride owned, still on the Super Plow ladder, upgrades go to the Super Plow');
  // 4. upgrading the Super Plow while the Monster is in use makes the Monster better too; buying the Loader... (Snowcat) still works
  const u = await EV(`(()=>{save.coins=1e9;const r0=moveSpeed()*bladeCells();buyUpg('speed');buyUpg('size');const r1=moveSpeed()*bladeCells();const lv=mLv('super');buyTool();return {r0:Math.round(r0),r1:Math.round(r1),superLv:lv.speed+'/'+lv.size,tool:TOOLS[save.tool].id,use:TOOLS[useIdx()].id,monsterLv:JSON.stringify(mLv('monster'))};})()`);
  console.log('upgrade while riding', JSON.stringify(u));
  ok(u.r1 > u.r0 && u.superLv === '4/4' && u.tool === 'snowcat' && u.monsterLv.includes('"speed":0'), 'upgrades with a ride in use go to the best machine and lift the ride; buyTool buys the next regular machine');
  // 5. coins can't buy a ride before its winter; can in winter 2 (in order)
  const w = await EV(`(()=>{save.coins=1e10;const a=owns(9);buyRideCoins(9);const b=owns(9);save.winters=2;buyRideCoins(10);const c=owns(10);buyRideCoins(9);const d=owns(9);return {a,b,c,d,winter:winterNo()};})()`);
  console.log('coins', JSON.stringify(w));
  ok(!w.b && !w.c && w.d, 'coins: Jet (winter 3) not buyable in winter 1, Mech refused out of order, Jet buyable in winter ' + w.winter);
  // 6. missions after the Rotary: parts -> mission -> win gives the ride
  const ms = await EV(`(()=>{save.winters=0;save.tool=toolIdx('rotary');save.rides={monster:true};save.parts={jet:3};const li=LEVELS.findIndex(L=>L.tool==='jet');return {next:nextRideIdx(),on:missionOn(li),reach:levelReach(li)};})()`);
  console.log('mission', JSON.stringify(ms));
  ok(ms.next === 9 && ms.on && ms.reach, 'Rotary owner with 3 Jet parts: mission open');
  await p.evaluate(() => { const R = window.__SR; R.startLevel(R.LEVELS.findIndex(L => L.tool === 'jet')); }); await p.waitForTimeout(3300);
  const mr = await EV(`(()=>{const t=tool();return {id:t.id,ride:!!t.ride,cells:bladeCells(),mission:run.mission};})()`);
  console.log('mission run', JSON.stringify(mr));
  ok(mr.id === 'jet' && mr.ride && mr.mission === 'jet', 'mission runs the Jet built on your Rotary');
  await EV(`(()=>{grantRide(toolIdx('jet'));})()`);
  // 7. garage and upgrades screens
  await EV(`(()=>{save.rides={monster:true,jet:true};save.tool=toolIdx('rotary');save.use=toolIdx('jet');save.rideSeen={mech:true};save.coins=5e7;_tc.k='';})()`);
  await p.evaluate(() => window.__SR.goGarage()); await p.waitForTimeout(400);
  await EV('scrollY.garage=999'); await p.waitForTimeout(400); await p.screenshot({ path: '/tmp/rc_garage.png' });
  await p.evaluate(() => window.__SR.goUpgrades()); await p.waitForTimeout(500); await p.screenshot({ path: '/tmp/rc_upgrades.png' });
  // winter 2, Super Plow owner who has driven the Monster: Monster buyable with coins; peek at the Jet
  await EV(`(()=>{save.rides={};save.tool=toolIdx('super');save.use=save.tool;save.winters=1;save.rideSeen={monster:true};save.coins=3e7;_tc.k='';})()`);
  await p.evaluate(() => window.__SR.goGarage()); await EV('scrollY.garage=999'); await p.waitForTimeout(400); await p.screenshot({ path: '/tmp/rc_garage2.png' });
  await EV(`(()=>{save.winters=0;save.rides={monster:true};save.rideSeen={monster:true,jet:true};save.gems=400;ridePeek='jet';})()`); await p.waitForTimeout(400); await p.screenshot({ path: '/tmp/rc_peek.png' });
  await EV('ridePeek=null');
  ok(errs.length === 0, 'no errors ' + JSON.stringify(errs));
  console.log(fails.length ? 'FAILS ' + fails.length : 'ALL OK');
  await br.close(); })();
