const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  // 1. day-one match: maxed Rotary owner gets each ride
  const m = await p.evaluate(() => window.__EV(`(()=>{save.tut=true;const out=[];save.tool=toolIdx('rotary');for(const id of ['super','snowcat','rotary']){const q=mLv(id);q.speed=6;q.size=6;q.bumper=2;}
    const best=bestOwned('x').rate;out.push(['best owned rate',Math.round(best)]);
    for(let i=BASE_TOOLS;i<TOOLS.length;i++){const id=TOOLS[i].id;const fresh=rateOf(id,{speed:0,size:0});grantRide(i);const m=mLv(id);out.push([id,'fresh',Math.round(fresh),'given lv',m.speed+'/'+m.size+'/b'+m.bumper,'rate',Math.round(rateOf(id,m)),Math.round(100*rateOf(id,m)/best)+'%','next best now',Math.round(bestOwned('x').rate)]);}
    return out;})()`));
  for (const r of m) console.log(JSON.stringify(r));
  // 2. pre-Rotary tease: Super Plow owner, drive keys spawn with the Monster, drive uses matched levels
  const t = await p.evaluate(() => window.__EV(`(()=>{save.tool=toolIdx('super');save.use=save.tool;for(let i=BASE_TOOLS;i<TOOLS.length;i++){const q=mLv(TOOLS[i].id);q.speed=0;q.size=0;}save.rideSeen={};save.parts={};
    const q=mLv('super');q.speed=4;q.size=4;let keys=0,parts=0;for(let k=0;k<40;k++){const g=buildLevel(lvIdx('carousel'));if(g.driveKey)keys++;if(g.part)parts++;}
    return {tease:teaseRideIdx(),next:nextRideIdx(),keys40:keys,parts40:parts,superRate:Math.round(rateOf('super',mLv('super'))),monsterMatch:JSON.stringify(matchLv('monster')),monsterMatchRate:Math.round(rateOf('monster',matchLv('monster')))};})()`));
  console.log('tease', JSON.stringify(t));
  // 3. pity: Rotary owner, partDry 7 -> every build has a part
  const pi = await p.evaluate(() => window.__EV(`(()=>{save.tool=toolIdx('rotary');save.parts={};save.partDry=7;let n=0;for(let k=0;k<30;k++){if(buildLevel(lvIdx('igloos')).part)n++;}save.partDry=0;let n0=0;for(let k=0;k<200;k++){if(buildLevel(lvIdx('igloos')).part)n0++;}return {forced30:n,random200:n0};})()`));
  console.log('pity', JSON.stringify(pi));
  // 4. early test drive in a real run + the offer screen
  await p.evaluate(() => window.__EV(`(()=>{save.tool=toolIdx('super');save.use=save.tool;save.ridePass=false;save.rideSeen={};})()`));
  await p.evaluate(() => { const R = window.__SR; R.startLevel(R.LEVELS.findIndex(L => L.id === 'carousel')); });
  await p.waitForTimeout(3300);
  const d = await p.evaluate(() => window.__EV(`(()=>{const ri=teaseRideIdx();G.driveKey={x:P.x,y:P.y,ri,taken:false};checkDrive({x:P.x-8,y:P.y-8,w:16,h:16},0.01);return {drive:run.drive,rideLv:JSON.stringify(run.rideLv),speed:Math.round(moveSpeed()),cells:bladeCells(),superSpeed:Math.round(TOOLS[toolIdx('super')].speed*(1+mspec('super').speedPer*4)),owned:save.tool};})()`));
  console.log('drive', JSON.stringify(d));
  await p.evaluate(() => { window.__HOLD = true; window.__EV('run.driveT=0.01'); window.__STEP(30, 1/30, 0); window.__EV('endRound(false)'); window.__STEP(60, 1/30, 1); window.__HOLD = false; });
  await p.waitForTimeout(1500); await p.screenshot({ path: '/tmp/ride_offer_early.png' });
  console.log('owned after offer', await p.evaluate(() => window.__EV('save.tool')), 'partDry', await p.evaluate(() => window.__EV('save.partDry')), 'errors', JSON.stringify(errs));
  await br.close(); })();
