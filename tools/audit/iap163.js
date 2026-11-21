// p163: every price and ad button goes through IAP. Web: unchanged. Apps (a fake window.SRNative here): store prices,
// buy ok / cancelled, ad ok / no fill (reward given back), silent owned sync, Restore Purchases.
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  // 1) web, no native layer
  { const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://127.0.0.1:8766/lab6.html?test=1'); await p.waitForTimeout(900);
    const r = JSON.parse(await p.evaluate(() => window.__EV(`(()=>{save.pro=false;save.starter=false;save.gems=0;const c0=save.coins;shopBuyPremium();const pro=save.pro;shopBuyStarter();
      const g=save.gems;IAP.ad('double_coins',{t:2.5,reward:100});const card=!!adScreen;adScreen=null;IAP.restore();return JSON.stringify({pro,starter:save.starter,g,card,coins:save.coins>c0,busy:IAP.busy});})()`)));
    ok('web: Premium and Starter grant at once, ads use the test card, nothing busy', r.pro && r.starter && r.g === 250 && r.card && r.coins && !r.busy, r);
    ok('web: no page errors', errs.length === 0, errs.slice(0, 2)); await p.close(); }
  // 2) the apps: a fake native layer
  const ctx = await b.newContext({ viewport: { width: 360, height: 640 } });
  await ctx.addInitScript(() => { window.__log = []; window.__next = { buy: 'ok', ad: 'ok' };
    window.SRNative = { buy: id => { __log.push('buy:' + id); return new Promise(r => setTimeout(() => r(__next.buy === 'ok' ? { ok: true } : { ok: false, reason: __next.buy }), 50)); },
      owned: () => Promise.resolve(['ride_jet']), restore: () => Promise.resolve(['premium', 'starter_pack']),
      prices: () => Promise.resolve({ premium: '£4.99', starter_pack: '£1.99', gems_60: '£0.99', wild_ride_pass: '£9.99', ride_ufo: '£3.99' }),
      showAd: pl => { __log.push('ad:' + pl); return new Promise(r => setTimeout(() => r(__next.ad === 'ok' ? { ok: true } : { ok: false, reason: 'no_fill' }), 50)); } }; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/lab6.html?test=1'); await p.waitForTimeout(1200);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const pr = await EV(`JSON.stringify({p:SHOP.premium.price,s:SHOP.starter.price,g:SHOP.gems[0].price,pass:SHOP.ridePass.price,ufo:SHOP.rides.ufo[0],jet:owns(toolIdx('jet'))})`);
  ok('apps: store prices replace the test prices; owned rides come back silently', pr.p === '£4.99' && pr.s === '£1.99' && pr.g === '£0.99' && pr.pass === '£9.99' && pr.ufo === '£3.99' && pr.jet, pr);
  await EV(`(()=>{save.pro=false;save.owned={};window.__next.buy='cancelled';shopBuyPremium();return JSON.stringify(1);})()`); await p.waitForTimeout(200);
  const c1 = await EV(`JSON.stringify({pro:save.pro,busy:IAP.busy,toast:toast&&toast.s})`);
  ok('apps: a cancelled purchase grants nothing and says so', !c1.pro && !c1.busy && /CANCELLED/.test(c1.toast || ''), c1);
  await EV(`(()=>{window.__next.buy='ok';const c0=save.coins;window.__c0=c0;shopBuyPremium();return JSON.stringify(IAP.busy>0);})()`);
  const mid = await EV(`(()=>{draw();return JSON.stringify({busy:IAP.busy>0,pro:save.pro});})()`); await p.waitForTimeout(200);
  const c2 = await EV(`JSON.stringify({pro:save.pro,owned:save.owned,coins:save.coins>window.__c0,busy:IAP.busy})`);
  ok('apps: a purchase waits for the store, then grants Premium (with its coins) and records it', mid.busy && !mid.pro && c2.pro && c2.owned.premium && c2.coins && !c2.busy, { mid, c2 });
  await EV(`(()=>{window.__next.ad='fail';startLevel(0,{});run.earned=500;run.adUsed=true;IAP.ad('double_coins',{t:2.5,reward:500,onFail:()=>{if(run)run.adUsed=false;}});return JSON.stringify(1);})()`); await p.waitForTimeout(200);
  const a1 = await EV(`JSON.stringify({adUsed:run.adUsed,card:!!adScreen,toast:toast&&toast.s})`);
  ok('apps: an ad that fails to load gives the x2 button back, no test card', a1.adUsed === false && !a1.card && /NO AD/.test(a1.toast || ''), a1);
  await EV(`(()=>{window.__next.ad='ok';window.__g0=save.gems||0;IAP.ad('free_gems',{t:2.5,reward:5,gems:true});return JSON.stringify(1);})()`); await p.waitForTimeout(200);
  const a2 = await EV(`JSON.stringify({gems:(save.gems||0)-window.__g0})`);
  ok('apps: a watched ad pays its reward', a2.gems === 5, a2);
  await EV(`(()=>{save.pro=false;save.starter=false;save.outfits={classic:true};window.__c1=save.coins;window.__g1=save.gems;IAP.restore();return JSON.stringify(1);})()`); await p.waitForTimeout(200);
  const r1 = await EV(`JSON.stringify({pro:save.pro,starter:save.starter,explorer:!!save.outfits.explorer,sameCoins:save.coins===window.__c1,sameGems:save.gems===window.__g1,toast:toast&&toast.s})`);
  ok('apps: Restore Purchases brings back Premium and the Starter outfit without paying coins or gems again', r1.pro && r1.starter && r1.explorer && r1.sameCoins && r1.sameGems && /RESTORED 2/.test(r1.toast || ''), r1);
  const set = await EV(`(()=>{goMap();settingsOpen=true;draw();const u=ui.find(x=>x.id==='restore');settingsOpen=false;return JSON.stringify(!!u&&u.y+u.h<=290);})()`);
  ok('Settings has a Restore Purchases button above the nav bar', set === true);
  console.log('native calls:', JSON.stringify(await p.evaluate(() => __log)));
  ok('apps: no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
