// p174 (lab + app build): store prices in the pixel font (£ € ¥ ₩ ₹ ₺ ₪ ₱ drawn; anything else rebuilt or cleaned)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/' + (process.argv[2] || 'lab6.html') + '?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const cases = [['£4.99', '£4.99'], ['4,99 €', '4,99 €'], ['¥800', '¥800'], ['₩6,600', '₩6,600'], ['₹399', '₹399'], ['R$ 24,90', 'R$ 24,90'], ['CA$6.99', 'CA$6.99'],
    ['69,00 kr', '69,00 KR'], ['24,99 zł', '24,99 ZL'], ['149 Kč', '149 KC'], ['CHF 6.00', 'CHF 6.00'], ['₺249,99', '₺249,99'], ['₪24.90', '₪24.90'], ['₱349.00', '₱349.00'],
    ['Rp 99.000', 'RP 99.000'], ['RM27.90', 'RM27.90'], ['NT$210', 'NT$210'], ['US$6.99', 'US$6.99'], ['$6.99', '$6.99'], ['E£ 99.99', 'E£ 99.99'], ['1 234,00 kr', '1 234,00 KR'],
    [{ price: '149.000 ₫', amount: 149000, currency: 'VND' }, 'VND 149,000'], [{ price: '‏١٨٫٩٩ ر.س.‏', amount: 18.99, currency: 'SAR' }, 'SAR 18.99'],
    [{ price: '£1.99', amount: 1.99, currency: 'GBP' }, '£1.99'], [{ price: '‏١٨٫٩٩ ر.س.‏' }, '18.99'], [null, null], [{ amount: 1 }, null]];
  const r = await EV(`JSON.stringify(${JSON.stringify(cases.map(c => c[0]))}.map(v=>{const o=fontPrice(v);return [o,o==null||[...o].every(c=>FONT[c]),o==null?0:textW(o)];}))`);
  const bad = cases.map((c, i) => [c[1], r[i][0], r[i][1]]).filter(x => x[0] !== x[1] || !x[2]);
  ok('store prices come out in the pixel font (' + cases.length + ' cases)', bad.length === 0, bad.length ? bad : undefined);
  ok('every cleaned price fits a 46 px price button', r.every(x => x[2] <= 44), r.filter(x => x[2] > 44));
  const g = await EV(`JSON.stringify(['£','€','¥','₩','₹','₺','₪','₱'].map(c=>[c,!!FONT[c]&&FONT[c].length===5&&FONT[c].every(row=>row.length===FONT[c][0].length)]))`);
  ok('new glyphs: £ € ¥ ₩ ₹ ₺ ₪ ₱, 5 rows each', g.every(x => x[1]), g);
  ok('the euro is not drawn like E or C', await EV(`JSON.stringify(FONT['€'].join()!==FONT.E.join()&&FONT['€'].join()!==FONT.C.join()&&FONT['€'].join()!==FONT['£'].join())`));
  const LIT = async () => { await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=20;goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;}catch(e){}shopTab=0;openShop();draw();return '1';})()`); await p.waitForTimeout(400);
    return EV(`(()=>{draw();const d=b.getImageData(0,24,180,10).data;let lit=0;for(let i=0;i<d.length;i+=4)if(d[i+1]>200&&d[i]<160&&d[i+2]<170)lit++;shopOpen=false;return JSON.stringify(lit);})()`); };
  const litWeb = await LIT();
  await EV(`(()=>{window.SRNative={platform:'ios',prices:()=>Promise.resolve({gems_60:'£0.99',gems_135:{price:'£1.99',amount:1.99,currency:'GBP'},gems_365:'£4.99',gems_800:'£9.99',gems_1850:'£19.99',premium:'£6.99',starter_pack:'£0.99',ride_monster:'£1.99',wild_ride_pass:{price:'\\u200f٢٩٫٩٩ ر.س.\\u200f',amount:29.99,currency:'SAR'}}),owned:()=>Promise.resolve([]),buy:()=>Promise.resolve({ok:false,reason:'cancelled'})};IAP.prices();return JSON.stringify(!!IAP.native());})()`);
  await p.waitForTimeout(200);
  const s = await EV(`JSON.stringify({g:SHOP.gems.map(g=>g.price),pre:SHOP.premium.price,st:SHOP.starter.price,m:SHOP.rides.monster[0],jet:SHOP.rides.jet[0],pass:SHOP.ridePass.price,native:IAP.native()})`);
  ok('IAP.prices() puts the cleaned store prices in the shop (strings and {price, amount, currency})', s.g.join() === '£0.99,£1.99,£4.99,£9.99,£19.99' && s.pre === '£6.99' && s.st === '£0.99' && s.m === '£1.99' && s.pass === 'SAR 29.99', s);
  ok('a product the store gave no price for keeps its test price', s.jet === '$1.99', s.jet);
  const litApp = await LIT();
  ok('the shop says TEST MODE on the web and not in the apps', litWeb > 20 && litApp === 0, { litWeb, litApp });
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
