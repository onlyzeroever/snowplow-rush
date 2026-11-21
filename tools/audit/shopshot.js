const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const file = process.argv[2] || 'lab6.html', tag = process.argv[3] || 'lab';
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://127.0.0.1:8766/${file}?test=1`); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c);
  const shot = async (n) => { const u = await EV('JSON.stringify(b.canvas.toDataURL())'); fs.writeFileSync(`/tmp/audit/${n}.png`, Buffer.from(JSON.parse(u).split(',')[1], 'base64')); };
  await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=20;save.gems=40;save.coins=5000;save.gemBuys=0;goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;}catch(e){}shopTab=0;openShop();draw();return '1';})()`);
  await p.waitForTimeout(300); await EV(`(()=>{draw();return '1';})()`); await shot(`shop_${tag}_offers`);
  const r = await EV(`(()=>{const u=ui.find(x=>x.id==='sg1');const g0=save.gems;u.fn();const g1=save.gems;const u2=ui.find(x=>x.id==='sg1');draw();const u3=ui.find(x=>x.id==='sg1');u3.fn();return JSON.stringify({first:g1-g0,second:save.gems-g1,buys:save.gemBuys});})()`);
  console.log('gem buys', r);
  await EV(`(()=>{draw();return '1';})()`); await shot(`shop_${tag}_offers_after`);
  await EV(`(()=>{shopTab=1;draw();return '1';})()`); await shot(`shop_${tag}_rides`);
  console.log('errors', JSON.stringify(errs.slice(0, 3)));
  await b.close();
})();
