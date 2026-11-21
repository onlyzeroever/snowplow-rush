// Shop layout audit: every text, card and button the shop and its pop-ups draw, in every state and store currency.
// Checks: no text over text, no stray text over a button, text and buttons inside their card, everything inside the
// panel, every price button in the one right-hand column (x 118, 46 wide).   node shoplayout.js [file] [shots dir]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const file = process.argv[2] || 'lab6.html', shots = process.argv[3] || '';
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined && !pass ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://127.0.0.1:8766/${file}?test=1`); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c);
  await EV(`(()=>{window.__LAY=null;window.__REC=false;const rec=()=>window.__LAY&&window.__REC;
    const wrapRec=(f)=>function(){window.__REC=true;try{return f.apply(this,arguments);}finally{window.__REC=false;}};drawShop=wrapRec(drawShop);drawOffer=wrapRec(drawOffer);
    const _t=text;text=function(g,s,x,y,col,o){o=o||{};if(rec()&&g===b&&!o.shadow&&!window.__INPR){const sc=o.scale||1,w=textW(String(s),sc);let X=x;if(o.align==='center')X=x-Math.floor(w/2);else if(o.align==='right')X=x-w;
      __LAY.push({k:'t',s:String(s),x:Math.round(X),y:Math.round(y),w:w-sc,h:5*sc,lab:window.__INBTN||null});}return _t.apply(this,arguments);};
    const _bn=button;button=function(id,x,y,w,h){if(rec())__LAY.push({k:'b',id,x,y,w,h});window.__INBTN=id;try{return _bn.apply(this,arguments);}finally{window.__INBTN=null;}};
    const _c=card;card=function(x,y,w,h){if(rec())__LAY.push({k:'c',x,y,w,h});return _c.apply(this,arguments);};
    const _pr=priceRow;priceRow=function(ic,s,x,y,col){const w=ic.width+2+textW(String(s));if(rec())__LAY.push({k:'t',s:'[gem]'+s,x:Math.round(x-w/2),y,w:w-1,h:5,lab:null});window.__INPR=true;try{return _pr.apply(this,arguments);}finally{window.__INPR=false;}};
    return '1';})()`);
  const NATIVE = (pr) => `window.SRNative={platform:'ios',prices:()=>Promise.resolve(${pr}),owned:()=>Promise.resolve([]),buy:()=>Promise.resolve({ok:false,reason:'cancelled'}),restore:()=>Promise.resolve([])};IAP.prices();`;
  const WEB = `window.SRNative=undefined;SHOP.gems.forEach((g,i)=>g.price=['$0.99','$1.99','$4.99','$9.99','$19.99'][i]);SHOP.premium.price='$6.99';SHOP.starter.price='$0.99';Object.keys(SHOP.rides).forEach((k,i)=>SHOP.rides[k][0]=['$1.99','$1.99','$2.99','$2.99','$3.99'][i]);SHOP.ridePass.price='$7.99';`;
  const STORES = {
    us: WEB,
    uk: NATIVE(`{gems_60:'£0.99',gems_135:'£1.99',gems_365:'£4.99',gems_800:'£9.99',gems_1850:'£19.99',premium:'£6.99',starter_pack:'£0.99',ride_monster:'£1.99',ride_jet:'£1.99',ride_mech:'£2.99',ride_dragon:'£2.99',ride_ufo:'£3.99',wild_ride_pass:'£7.99'}`),
    eu: NATIVE(`{gems_60:'0,99\\u00a0€',gems_135:'1,99\\u00a0€',gems_365:'5,49\\u00a0€',gems_800:'10,99\\u00a0€',gems_1850:'21,99\\u00a0€',premium:'7,99\\u00a0€',starter_pack:'0,99\\u00a0€',ride_monster:'2,29\\u00a0€',ride_jet:'2,29\\u00a0€',ride_mech:'3,29\\u00a0€',ride_dragon:'3,29\\u00a0€',ride_ufo:'4,49\\u00a0€',wild_ride_pass:'8,99\\u00a0€'}`),
    ch: NATIVE(`{gems_60:'CHF\\u00a01.00',gems_135:'CHF\\u00a02.00',gems_365:'CHF\\u00a05.00',gems_800:'CHF\\u00a010.00',gems_1850:'CHF\\u00a020.00',premium:'CHF\\u00a07.00',starter_pack:'CHF\\u00a01.00',ride_monster:'CHF\\u00a02.00',ride_jet:'CHF\\u00a02.00',ride_mech:'CHF\\u00a03.00',ride_dragon:'CHF\\u00a03.00',ride_ufo:'CHF\\u00a04.00',wild_ride_pass:'CHF\\u00a08.00'}`),
    id: NATIVE(`{gems_60:'Rp\\u00a016.000',gems_135:'Rp\\u00a032.000',gems_365:'Rp\\u00a079.000',gems_800:'Rp\\u00a0159.000',gems_1850:'Rp\\u00a0329.000',premium:'Rp\\u00a0109.000',starter_pack:'Rp\\u00a016.000',ride_monster:'Rp\\u00a032.000',ride_jet:'Rp\\u00a032.000',ride_mech:'Rp\\u00a049.000',ride_dragon:'Rp\\u00a049.000',ride_ufo:'Rp\\u00a065.000',wild_ride_pass:'Rp\\u00a0129.000'}`),
  };
  const base = `save.privSeen=true;save.tut=true;save.fbRuns=20;save.sess=3;save.gems=40;save.coins=5000;save.gemBuys=0;save.pro=false;save.starter=false;save.ridePass=false;save.offers={seenShop:true,last:todayKey()};save.starterT=null;save.adGems=null;save.shopDay=null;save.rides={};save.rideSeen={};
    for(let i=0;i<6;i++)save.best[i]=Math.max(save.best[i]||0,1);goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;weeklyOpen=false;}catch(e){};shopNeed=null;`;
  const STATES = {
    starter: `save.offers.starter=true;save.starterT=Date.now()-3600e3;shopTab=0;openShop();`,
    premium: `shopTab=0;openShop();`,
    pro: `save.pro=true;shopTab=0;openShop();`,
    pro_starter: `save.pro=true;save.offers.starter=true;save.starterT=Date.now()-3600e3;shopTab=0;openShop();`,
    gifts_used: `save.adGems={date:todayKey(),n:99};save.gemBuys=2;shopTab=0;openShop();`,
    need: `save.offers.starter=true;save.starterT=Date.now()-3600e3;shopTab=0;openShop();shopNeed={cost:250,t:tNow-5};`,
    rides: `shopTab=1;openShop();`,
    rides_sale: `save.tool=toolIdx('super');save.rideSeen={monster:true};shopTab=1;openShop();`,
    rides_rich: `save.gems=2000;save.tool=toolIdx('super');save.rideSeen={monster:true};shopTab=1;openShop();`,
    rides_owned: `save.ridePass=true;save.tool=toolIdx('super');save.rideSeen={monster:true};shopTab=1;openShop();`,
    pop_starter: `shopOpen=false;offerOpen='starter';`,
    pop_premium: `shopOpen=false;offerOpen='premium';`,
  };
  const COL = new Set(['sad', 'sst', 'spro', 'spass', 'sg0', 'sg1', 'sg2', 'sg3', 'sg4', 'sb0', 'sb1', 'sb2']);
  let n = 0;
  for (const [store, setStore] of Object.entries(STORES)) {
    for (const [name, st] of Object.entries(STATES)) {
      await EV(`(()=>{${base}${setStore}return '1';})()`); await p.waitForTimeout(store === 'us' ? 30 : 120);
      await EV(`(()=>{${st}draw();return '1';})()`); await p.waitForTimeout(260);
      const L = JSON.parse(await EV(`(()=>{window.__LAY=[];draw();const r=__LAY;window.__LAY=null;return JSON.stringify(r);})()`));
      if (shots && (store === 'us' || store === 'eu' || store === 'id')) { const u = await EV(`JSON.stringify(b.canvas.toDataURL())`); fs.writeFileSync(`${shots}/lay_${store}_${name}.png`, Buffer.from(JSON.parse(u).split(',')[1], 'base64')); }
      // only what the shop or the pop-up drew (after the panel): skip the map underneath
      const T = L.filter(e => e.k === 't'), B = L.filter(e => e.k === 'b'), C = L.filter(e => e.k === 'c');
      const ov = (a, c) => a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h && c.y < a.y + a.h;
      const pop = name.startsWith('pop');
      const inPanel = e => pop ? (e.x >= 15 && e.x + e.w <= 165 && e.y >= 71 && e.y + e.h <= 237) : (e.x >= 8 && e.x + e.w <= 172 && e.y >= 8 && e.y + e.h <= 310);
      const shopT = T, shopB = B;
      const prob = [];
      for (let i = 0; i < shopT.length; i++) for (let j = i + 1; j < shopT.length; j++) { const a = shopT[i], c = shopT[j]; if (ov(a, c) && !(a.x === c.x && a.y === c.y && a.s === c.s)) prob.push('text/text "' + a.s + '" + "' + c.s + '"'); }
      for (const t of shopT) for (const bt of shopB) if (!t.lab && ov(t, bt) && !t.s.startsWith('[gem]') && !(t.s.startsWith('=') && bt.id.startsWith('sb'))) prob.push('text over button "' + t.s + '" / ' + bt.id);
      for (const t of shopT) if (t.lab) { const bt = shopB.find(x => x.id === t.lab); if (bt && (t.x < bt.x + 1 || t.x + t.w > bt.x + bt.w - 1)) prob.push('label wider than its button "' + t.s + '" ' + bt.id); }
      for (const e of [...shopT, ...shopB]) { const c = C.find(c => e.x >= c.x && e.x < c.x + c.w && e.y >= c.y && e.y < c.y + c.h); if (c && (e.x < c.x + 2 || e.x + e.w > c.x + c.w - 2 || e.y < c.y + 2 || e.y + e.h > c.y + c.h - 2)) prob.push('outside its card ' + (e.s ? '"' + e.s + '"' : e.id)); }
      for (const e of [...shopT, ...shopB]) if (!inPanel(e)) prob.push('outside the panel ' + (e.s ? '"' + e.s + '"' : e.id));
      for (const bt of shopB) if (COL.has(bt.id) && (bt.x !== 118 || bt.w !== 46)) prob.push('price button off the column ' + bt.id + ' x' + bt.x + ' w' + bt.w);
      for (let i = 0; i < shopB.length; i++) for (let j = i + 1; j < shopB.length; j++) if (ov(shopB[i], shopB[j])) prob.push('button/button ' + shopB[i].id + ' + ' + shopB[j].id);
      if (!pop) { const cs = C.filter(c => c.x !== 12 || c.w !== 156); if (cs.length) prob.push('card off the grid ' + JSON.stringify(cs)); }
      ok(`${store} ${name} (${shopT.length} texts, ${shopB.length} buttons)`, prob.length === 0, [...new Set(prob)].slice(0, 6)); n++;
    }
  }
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(n + ' screens; ' + (res.every(Boolean) ? 'ALL OK' : 'SOME FAILED')); await br.close();
})();
