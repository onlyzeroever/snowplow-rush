const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(1000);
  const r = await p.evaluate(() => window.__EV(`(()=>{save.tut=true;save.tool=toolIdx('rotary');save.use=save.tool;const m=mLv('rotary');m.speed=6;m.size=6;m.bumper=2;save.coins=1e9;state='upgrades';return {ready:mk2Ready(),cost:mk2Cost('rotary')};})()`));
  await p.waitForTimeout(500); await p.screenshot({ path: '/tmp/mk2_ready.png' });
  const r2 = await p.evaluate(() => window.__EV(`(()=>{const v0=valueMult();buyMk2();return {mk2:isMk2('rotary'),coinsGain:+(valueMult()/v0).toFixed(3),ready:mk2Ready()};})()`));
  await p.waitForTimeout(400); await p.screenshot({ path: '/tmp/mk2_owned.png' });
  // speed in a run and the badge in the garage
  await p.evaluate(() => { const R = window.__SR; R.startLevel(R.LEVELS.findIndex(L => L.id === 'igloos')); }); await p.waitForTimeout(3300);
  const sp = await p.evaluate(() => window.__EV(`(()=>{const a=moveSpeed();save.mk2.rotary=false;_tc.k='';const b2=moveSpeed();save.mk2.rotary=true;_tc.k='';return +(a/b2).toFixed(3);})()`));
  await p.evaluate(() => window.__EV(`(()=>{run=null;state='map';goGarage();scrollY.garage=230;})()`)); await p.waitForTimeout(600); await p.screenshot({ path: '/tmp/mk2_garage.png' });
  console.log(JSON.stringify(r), JSON.stringify(r2), 'speed x', sp, 'errors', JSON.stringify(errs)); await br.close(); })();
