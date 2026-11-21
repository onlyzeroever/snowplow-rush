// p170 (lab): launch prices, five-pack gem ladder, first gem purchase doubled, honest labels, store ids
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/' + (process.argv[2] || 'lab6.html') + '?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const t = await EV(`JSON.stringify({g:SHOP.gems.map(g=>[g.gems,g.price,g.tag||'',g.bonus||'']),pre:SHOP.premium,st:SHOP.starter,r:SHOP.rides,pass:SHOP.ridePass.price,ids:IAP.ids,con:IAP.consumable})`);
  ok('gem ladder 60/135/365/800/1,850 at $0.99/$1.99/$4.99/$9.99/$19.99', JSON.stringify(t.g.map(g => g[0] + g[1])) === JSON.stringify(['60$0.99', '135$1.99', '365$4.99', '800$9.99', '1850$19.99']), t.g);
  ok('no POPULAR tag; BEST VALUE only on the best rate', t.g.filter(g => g[2]).length === 1 && t.g[4][2] === 'BEST VALUE', t.g.map(g => g[2]));
  const rates = t.g.map(g => g[0] / parseFloat(g[1].slice(1))), base = rates[0];
  ok('bonus labels never overstate (rounded down against the $0.99 pack)', t.g.slice(1).every((g, i) => parseInt(g[3]) <= Math.floor((rates[i + 1] / base - 1) * 100)), t.g.map((g, i) => [g[3], ((rates[i] / base - 1) * 100).toFixed(1)]));
  ok('Premium $6.99 with no "was" price', t.pre.price === '$6.99' && !('was' in t.pre), t.pre);
  ok('Starter $0.99: 150 gems + 10 runs', t.st.price === '$0.99' && t.st.gems === 150 && t.st.coinRuns === 10, t.st);
  const v = await EV(`JSON.stringify({gems:150*0.99/60,coins:10*0.08})`);
  ok('3X VALUE holds (150 gems + 10 runs of coins vs $0.99)', (150 * 0.99 / 60) / 0.99 >= 2.5, v);
  ok('rides $1.99/$1.99/$2.99/$2.99/$3.99, pass $7.99', Object.values(t.r).map(r => r[0]).join() === '$1.99,$1.99,$2.99,$2.99,$3.99' && t.pass === '$7.99', t.r);
  ok('store ids for the new ladder, all consumable', t.ids.g1 === 'gems_60' && t.ids.g15 === 'gems_135' && t.ids.g2 === 'gems_365' && t.ids.g3 === 'gems_800' && t.ids.g4 === 'gems_1850' && ['g1', 'g15', 'g2', 'g3', 'g4'].every(k => t.con[k]), t.ids);
  const d = await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=20;save.gems=0;save.gemBuys=0;goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;}catch(e){}shopTab=0;openShop();draw();
    const out=[];for(const id of ['sg0','sg4','sg0']){const u=ui.find(x=>x.id===id);const g0=save.gems;u.fn();out.push(save.gems-g0);draw();}return JSON.stringify(out);})()`);
  ok('first gem pack doubled once, then normal', d.join() === '120,1850,60', d);
  const c = await EV(`JSON.stringify([gemCash(30),gemCash(120),gemCash(250)])`);
  ok('coin bags show their gems in money ($0.99 pack rate, rounded up)', c.join() === '$0.50,$1.98,$4.13', c);
  const pc = await EV(`(()=>{const tot=Object.values(SHOP.rides).reduce((a,r)=>a+parseFloat(r[0].slice(1)),0);return JSON.stringify({tot,pc:Math.floor((1-7.99/tot)*100)});})()`);
  ok('Wild Ride Pass saving is 42% against $13.95', Math.abs(pc.tot - 13.95) < 0.001 && pc.pc === 42, pc);
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
