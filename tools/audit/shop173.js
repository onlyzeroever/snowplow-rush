// p173 (lab): shop v2: free gift on top, one hero offer, real 48 h starter window, one colour per way of paying,
// short of gems -> the gem packs with the right one outlined, FREE badge on the map's SHOP button
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/' + (process.argv[2] || 'lab6.html') + '?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const base = (extra) => `save.privSeen=true;save.tut=true;save.fbRuns=20;save.sess=3;save.gems=40;save.coins=5000;save.gemBuys=0;save.pro=false;save.starter=false;save.ridePass=false;save.offers={seenShop:true,last:todayKey()};save.starterT=null;save.adGems=null;save.shopDay=null;
    for(let i=0;i<6;i++)save.best[i]=Math.max(save.best[i]||0,1);goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;weeklyOpen=false;adScreen=null;IAP.busy=0;gotCard=null;}catch(e){};${extra || ''}`;
  const open = async (extra, tab) => { await EV(`(()=>{${base(extra)};shopTab=${tab || 0};openShop();draw();return '1';})()`); await p.waitForTimeout(350); return EV(`(()=>{draw();return JSON.stringify(ui.filter(u=>/^s|^of/.test(u.id)).map(u=>[u.id,u.x,u.y,u.w,u.h]));})()`); };
  const has = (u, id) => u.find(x => x[0] === id);
  const px = (x, y) => EV(`JSON.stringify(Array.from(b.getImageData(${x},${y},1,1).data).slice(0,3))`);
  const hex = c => '#' + c.map(v => v.toString(16).padStart(2, '0')).join('');
  const C = await EV(`JSON.stringify({green:BTNC.green[0],purple:BTNC.purple[0],blue:BTNC.blue[0],grey:BTNC.grey[0]})`);

  let u = await open('');
  ok('free gift sits at the top of OFFERS', has(u, 'sad') && has(u, 'sad')[2] < 80, has(u, 'sad'));
  ok('before the starter has been offered: no Starter Pack, Premium is the hero', !has(u, 'sst') && has(u, 'spro') && has(u, 'spro')[2] < 100, [has(u, 'sst'), has(u, 'spro')]);
  const col = async (id) => { const q = has(u, id); return q ? hex(await px(q[1] + 1, q[2] + 4)) : null; };
  ok('free = blue, money = green', (await col('sad')) === C.blue && (await col('spro')) === C.green && (await col('sg0')) === C.green && (await col('sg4')) === C.green, { sad: await col('sad'), spro: await col('spro'), sg0: await col('sg0') });

  const pick = await EV(`(()=>{${base('')};save.offers={};save.sess=2;save.fbRuns=5;save.offerTest=true;offerOpen=null;offerPick();const r={offer:offerOpen,dt:Date.now()-(save.starterT||0)};offerOpen=null;save.offerTest=false;return JSON.stringify(r);})()`);
  ok('the starter pop-up starts its 48 hours', pick.offer === 'starter' && pick.dt >= 0 && pick.dt < 5000, pick);

  u = await open(`save.offers.starter=true;save.starterT=Date.now()-3600e3`);
  const left = await EV(`JSON.stringify(fmtLeft(starterLeft()))`);
  ok('while it is on: Starter Pack is the hero with a real countdown, Premium compact below', has(u, 'sst') && has(u, 'spro') && has(u, 'sst')[2] < has(u, 'spro')[2] && /^4[67]H [0-5]\dM$/.test(left), { left, sst: has(u, 'sst'), spro: has(u, 'spro') });
  ok('starter button is green', (await col('sst')) === C.green, await col('sst'));
  u = await open(`save.offers.starter=true;save.starterT=Date.now()-49*3600e3`);
  ok('after 48 hours it is gone for good (Premium is the hero again)', !has(u, 'sst') && has(u, 'spro')[2] < 100, [has(u, 'sst'), has(u, 'spro')]);
  u = await open(`save.offers.starter=true;save.starterT=null`);
  const t0 = await EV(`JSON.stringify(Date.now()-(save.starterT||0))`);
  ok('an older save that saw the pop-up before timers existed gets a fresh 48 hours from now', has(u, 'sst') && t0 >= 0 && t0 < 5000, t0);
  await EV(`(()=>{shopBuyStarter();draw();return '1';})()`); await p.waitForTimeout(200);
  u = await EV(`(()=>{draw();return JSON.stringify(ui.filter(u=>/^s/.test(u.id)).map(u=>[u.id,u.x,u.y,u.w,u.h]));})()`);
  ok('bought: the starter card goes', !has(u, 'sst'), has(u, 'sst'));
  u = await open(`save.starter=true;save.pro=true`);
  ok('Premium owners: no Premium button, gift says CLAIM (no ad)', !has(u, 'spro') && has(u, 'sad'), has(u, 'spro'));
  const g0 = await EV(`(()=>{const q=ui.find(x=>x.id==='sad');const g=save.gems;q.fn();return JSON.stringify({d:save.gems-g,n:save.adGems.n});})()`);
  ok('Premium: claiming the free gems is instant', g0.d === 5 && g0.n === 1, g0);

  u = await open('', 1);
  ok('the second tab no longer has the free gems button', !has(u, 'sad'), has(u, 'sad'));
  ok('coin bags are paid in gems: purple when affordable, grey when not', (await col('sb0')) === C.purple && (await col('sb2')) === C.grey, [await col('sb0'), await col('sb2')]);
  ok('the Wild Ride Pass is paid in money: green', (await col('spass')) === C.green, await col('spass'));

  // short of gems: the bag sends you to the gem packs with the smallest pack that covers it outlined
  await EV(`(()=>{const q=ui.find(x=>x.id==='sb2');q.fn();draw();return '1';})()`); await p.waitForTimeout(1500);
  let n = await EV(`(()=>{draw();const r=SHOP.gems.map((g,i)=>{const q=ui.find(x=>x.id==='sg'+i);const d=b.getImageData(10,q.y+4,1,1).data;return d[0]===255&&d[1]===79&&d[2]===163;});return JSON.stringify({tab:shopTab,need:shopNeed&&shopNeed.cost-save.gems,r});})()`);
  ok('TRUCKLOAD (250) with 40 gems: jumps to the gem packs, needs 210 more', n.tab === 0 && n.need === 210, n);
  ok('first buy doubles, so the 135 pack (270) is outlined, and only that one', n.r.join() === 'false,true,false,false,false', n.r);
  await EV(`(()=>{save.gemBuys=1;draw();return '1';})()`); await p.waitForTimeout(100);
  n = await EV(`(()=>{draw();return JSON.stringify(SHOP.gems.map((g,i)=>{const q=ui.find(x=>x.id==='sg'+i);const d=b.getImageData(10,q.y+4,1,1).data;return d[0]===255&&d[1]===79&&d[2]===163;}));})()`);
  ok('after a first buy: the 365 pack is the smallest that covers 210', n.join() === 'false,false,true,false,false', n);
  n = await EV(`(()=>{save.gems+=300;draw();return JSON.stringify({need:shopNeed});})()`);
  ok('once the gems are there the reminder clears', n.need === null, n);
  await EV(`(()=>{shopTab=1;draw();ui.find(x=>x.id==='sb2');save.gems=40;const q=ui.find(x=>x.id==='sb2');q.fn();draw();ui.find(x=>x.id==='stab1').fn();return '1';})()`);
  ok('switching back to COINS + RIDES clears it too', await EV(`JSON.stringify(shopNeed===null&&shopTab===1)`));
  const ride = await EV(`(()=>{save.gems=40;shopNeed=null;shopTab=1;const r=buyRide(toolIdx('monster'),true);return JSON.stringify({r,tab:shopTab,cost:shopNeed&&shopNeed.cost});})()`);
  ok('a Wild Ride paid in gems does the same (200 gems)', ride.r === false && ride.tab === 0 && ride.cost === 200, ride);
  await EV(`(()=>{draw();ui.find(x=>x.id==='sclose').fn();return '1';})()`);
  ok('DONE clears it', await EV(`JSON.stringify(shopNeed===null&&!shopOpen)`));

  // shop events (Alex OK, Nov 21 22:25)
  await EV(`(()=>{window.__TR=[];const o=track;track=function(n,p){__TR.push([n,p||{}]);return o.apply(this,arguments);};return '1';})()`);
  await EV(`(()=>{${base('')};shopOpen=false;draw();return '1';})()`); await p.waitForTimeout(400);
  const E = await EV(`(()=>{__TR.length=0;draw();ui.find(x=>x.id==='shopb').fn();draw();const a=__TR.find(e=>e[0]==='shop_open');shopOpen=false;goMap();draw();
    ui=[];drawHeaderGems(2,2,50);const gp=ui.find(x=>x.id==='gempanel');let g=null;if(gp){__TR.length=0;gp.fn();g=__TR.find(e=>e[0]==='shop_open');}
    shopTab=0;openShop();draw();__TR.length=0;ui.find(x=>x.id==='sad').fn();const fg=__TR.find(e=>e[0]==='shop_free_gift');
    save.gems=40;save.gemBuys=0;shopTab=1;draw();__TR.length=0;ui.find(x=>x.id==='sb2').fn();const ng=__TR.find(e=>e[0]==='shop_need_gems');
    draw();__TR.length=0;ui.find(x=>x.id==='sg1').fn();const it=__TR.find(e=>e[0]==='iap_test');
    return JSON.stringify({map:a&&a[1].from,gems:g&&g[1].from,fg:fg&&fg[1],ng:ng&&ng[1],it:it&&it[1]});})()`);
  ok('shop_open says where from (map, gem counter)', E.map === 'map' && E.gems === 'gems', E);
  ok('shop_free_gift fires on the free gift', !!E.fg && E.fg.pro === false, E.fg);
  ok('shop_need_gems: item, how many and the pack suggested', !!E.ng && E.ng.item === 'bag_b3' && E.ng.need === 210 && E.ng.pack === 'gems_135', E.ng);
  ok('a gem pack bought from that reminder is marked from_need', !!E.it && E.it.from_need === true, E.it);
  // map: FREE on the SHOP button until the shop has been opened today (only once the daily jobs are on)
  const badge = async (extra) => { await EV(`(()=>{${base(extra)};shopOpen=false;draw();return '1';})()`); await p.waitForTimeout(400);
    return EV(`(()=>{draw();const s=ui.find(x=>x.id==='shopb');const d=b.getImageData(s.x+s.w+1,s.y-2,1,1).data;return JSON.stringify(d[0]===232&&d[1]===40&&d[2]===63);})()`); };
  ok('map: FREE badge when the free gems are waiting', await badge(''));
  ok('map: no badge once the shop has been opened today', !(await badge(`save.shopDay=todayKey()`)));
  ok('map: no badge when the free gems are used up', !(await badge(`save.adGems={date:todayKey(),n:99}`)));
  ok('map: new players see nothing new', !(await badge(`save.fbRuns=1;save.dailyEver=false;for(let i=0;i<save.best.length;i++)save.best[i]=0`)));
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
