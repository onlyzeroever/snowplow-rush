// p177 Snow Bank + p178 Event Pass (lab): rules, honest labels, purchases, layout, screenshots.  node money178.js [file] [shots dir]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const file = process.argv[2] || 'lab6.html', shots = process.argv[3] || '';
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://127.0.0.1:8766/${file}?test=1`); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(r => { try { return JSON.parse(r); } catch (e) { return r; } });
  const shot = async n => { if (!shots) return; const u = await EV(`JSON.stringify(b.canvas.toDataURL())`); fs.writeFileSync(`${shots}/m_${n}.png`, Buffer.from(u.split(',')[1], 'base64')); };
  // layout check for one overlay: no text over text, no stray text over a button, labels inside buttons, inside the panel
  await EV(`(()=>{window.__LAY=null;window.__REC=false;const rec=()=>window.__LAY&&window.__REC;const wr=(f)=>function(){window.__REC=true;try{return f.apply(this,arguments);}finally{window.__REC=false;}};
    drawBank=wr(drawBank);drawPass=wr(drawPass);drawEvent=wr(drawEvent);drawGot=wr(drawGot);
    const _t=text;text=function(g,s,x,y,col,o){o=o||{};if(rec()&&g===b&&!o.shadow&&!window.__INPR){const sc=o.scale||1,w=textW(String(s),sc);let X=x;if(o.align==='center')X=x-Math.floor(w/2);else if(o.align==='right')X=x-w;__LAY.push({k:'t',s:String(s),x:Math.round(X),y:Math.round(y),w:w-sc,h:5*sc,lab:window.__INBTN||null});}return _t.apply(this,arguments);};
    const _bn=button;button=function(id,x,y,w,h){if(rec())__LAY.push({k:'b',id,x,y,w,h});window.__INBTN=id;try{return _bn.apply(this,arguments);}finally{window.__INBTN=null;}};
    const _pr=priceRow;priceRow=function(ic,s,x,y){const w=ic.width+2+textW(String(s));if(rec())__LAY.push({k:'t',s:'[gem]'+s,x:Math.round(x-w/2),y,w:w-1,h:5,lab:'row'});window.__INPR=true;try{return _pr.apply(this,arguments);}finally{window.__INPR=false;}};return '1';})()`);
  const layout = async (name) => { const L = await EV(`(()=>{window.__LAY=[];draw();const r=__LAY;window.__LAY=null;return JSON.stringify(r);})()`);
    const T = L.filter(e => e.k === 't'), B = L.filter(e => e.k === 'b'), ov = (a, c) => a.x < c.x + c.w && c.x < a.x + a.w && a.y < c.y + c.h && c.y < a.y + a.h, prob = [];
    for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++) if (ov(T[i], T[j]) && !(T[i].x === T[j].x && T[i].y === T[j].y)) prob.push('text/text "' + T[i].s + '" + "' + T[j].s + '"');
    for (const t of T) for (const bt of B) if (!t.lab && ov(t, bt)) prob.push('text over button "' + t.s + '" / ' + bt.id);
    for (const t of T) if (t.lab && t.lab !== 'row') { const bt = B.find(x => x.id === t.lab); if (bt && (t.x < bt.x + 1 || t.x + t.w > bt.x + bt.w - 1)) prob.push('label wider than button "' + t.s + '"'); }
    for (const e of [...T, ...B]) if (e.x < 8 || e.x + e.w > 172) prob.push('off the panel ' + (e.s || e.id));
    ok('layout: ' + name + ' (' + T.length + ' texts, ' + B.length + ' buttons)', prob.length === 0, prob.length ? [...new Set(prob)].slice(0, 5) : undefined); };
  const base = (x) => `(()=>{save.privSeen=true;save.tut=true;save.sess=3;save.gems=40;save.coins=5000;save.gemBuys=1;save.pro=false;save.starter=true;save.offers={seenShop:true,last:todayKey()};save.bank=null;save.evPass=null;save.evPaints=null;save.evPaintSel=null;
    for(let i=0;i<6;i++)save.best[i]=Math.max(save.best[i]||0,1);goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;weeklyOpen=false;adScreen=null;evOpen=false;bankOpen=false;passOpen=false;gotCard=null;shopOpen=false;}catch(e){};${x};draw();return '1';})()`;
  const ui = async () => EV(`(()=>{draw();return JSON.stringify(ui.map(u=>u.id));})()`);

  // ---- Snow Bank
  await EV(base(`save.fbRuns=9`)); await p.waitForTimeout(400);
  ok('no jar before the 10th job', !(await ui()).includes('bankjar'));
  await EV(base(`save.fbRuns=10`)); await p.waitForTimeout(400);
  let u = await ui(); ok('a jar on the map from the 10th job', u.includes('bankjar'));
  await shot('map_jar_new');
  // a real job fills it: +4, +1 a star
  await EV(`(()=>{window.__HOLD=1;startLevel(0,{});G.cleared=Math.round(G.clearable*0.95);run.contUsed=true;run.moved=true;run.time=0.01;update(0.05);window.__HOLD=0;return '1';})()`); await p.waitForTimeout(200);
  const j1 = await EV(`JSON.stringify({g:bankG(),ended:!!(run&&run.ended),stars:run&&run.res?run.res.stars:null})`);
  ok('a finished job puts 4 gems + 1 a star in the jar', j1.ended && j1.g === 4 + (j1.stars || 0), j1);
  await EV(base(`save.fbRuns=12;save.bank={g:397}`)); await EV(`(()=>{window.__HOLD=1;startLevel(0,{});G.cleared=Math.round(G.clearable*0.95);run.contUsed=true;run.moved=true;run.time=0.01;update(0.05);window.__HOLD=0;return '1';})()`); await p.waitForTimeout(200);
  ok('it stops at 400', (await EV(`JSON.stringify(bankG())`)) === 400);
  // the card
  await EV(base(`save.fbRuns=12;save.bank={g:150}`)); await p.waitForTimeout(300);
  await EV(`(()=>{draw();ui.find(x=>x.id==='bankjar').fn();draw();return '1';})()`); await p.waitForTimeout(250);
  let c = await EV(`(()=>{draw();const q=ui.find(x=>x.id==='bankbuy');const g0=save.gems;q.fn();return JSON.stringify({open:bankOpen,seen:save.bank.seen,gems:save.gems-g0,bank:bankG()});})()`);
  ok('below 220 it cannot be broken (and says how many more)', c.open && c.seen && c.gems === 0 && c.bank === 150, c);
  await shot('bank_150'); await layout('Snow Bank card at 150');
  await EV(`(()=>{save.bank.g=250;draw();return '1';})()`); await p.waitForTimeout(200); await shot('bank_250'); await layout('Snow Bank card at 250');
  c = await EV(`(()=>{draw();const g0=save.gems;ui.find(x=>x.id==='bankbuy').fn();draw();return JSON.stringify({gems:save.gems-g0,bank:bankG(),got:!!gotCard,open:bankOpen,broken:save.bank.broken});})()`);
  ok('from 220: buying it gives you every gem inside and empties the jar', c.gems === 250 && c.bank === 0 && c.got && !c.open && c.broken === 1, c);
  await p.waitForTimeout(200); await shot('bank_got'); await layout('YOU GOT after the Snow Bank');
  const v = await EV(`(()=>{const a=bankValue();const keep=SHOP.bank.price;SHOP.bank.price='$3.99';const b2=bankValue();SHOP.bank.price='3,29 €';const g0=SHOP.gems[0].price;SHOP.gems[0].price='0,99 €';const c2=bankValue();SHOP.bank.price=keep;SHOP.gems[0].price=g0;return JSON.stringify({usd:+a.toFixed(3),at399:+b2.toFixed(3),eur:+c2.toFixed(3)});})()`);
  ok('UP TO 2X VALUE holds at $2.99 (400 gems = $6.60) and in euros; it would not at $3.99', v.usd >= 2 && v.eur >= 2 && v.at399 < 2, v);
  await EV(base(`save.fbRuns=12;save.bank={g:400,seen:true}`)); await p.waitForTimeout(400); await shot('map_jar_full');

  // ---- Event Pass (a test event running now)
  await EV(`(()=>{EVENTS.unshift({id:'test-blizzard',kind:'blizzard',start:Date.now()-3600e3,end:Date.now()+30*3600e3});return '1';})()`);
  await EV(base(`save.fbRuns=12;save.gems=300;save.ev={id:'test-blizzard',flakes:100,got:2,runs:3};evOpen=true`)); await p.waitForTimeout(300);
  u = await ui(); ok('the event screen offers the pass', u.includes('evpass'), u.filter(x => /^ev/.test(x)));
  await shot('event_screen'); await layout('event screen with the pass button');
  await EV(`(()=>{ui.find(x=>x.id==='evpass').fn();draw();return '1';})()`); await p.waitForTimeout(200);
  await shot('pass_card'); await EV(`(()=>{evOpen=false;return '1';})()`); await layout('Event Pass card'); await EV(`(()=>{evOpen=true;return '1';})()`);
  let e = await EV(`(()=>{draw();const g0=save.gems,c0=save.coins;ui.find(x=>x.id==='passgem').fn();const e=save.ev;return JSON.stringify({gems:save.gems-g0,pass:save.evPass,flakes:e.flakes,got:e.got,coins:save.coins-c0,paint:save.evPaints,card:!!gotCard});})()`);
  ok('250 gems: pass owned, flakes so far doubled (100 to 200), steps reached pay out', e.gems === -250 && e.pass === 'test-blizzard' && e.flakes === 200 && e.got === 3 && e.coins > 0 && e.card, e);
  await p.waitForTimeout(200); await shot('pass_got'); await EV(`(()=>{evOpen=false;return '1';})()`); await layout('YOU GOT after the Event Pass');
  const f2 = await EV(`(()=>{run=run||{};run.event='test-blizzard';const r=evRun(50,1,false);return JSON.stringify(r&&r.f);})()`);
  ok('every job after that counts x2 ((50% + 1 star x10) x 2 = 120)', f2 === 120, f2);
  const sk = await EV(`(()=>{const tid=TOOLS[save.tool].id;return JSON.stringify({own:skinOwned(tid,6),col:skinPal(tid,6).b,name:EV_PAINT[save.evPaintSel][0]});})()`);
  ok('the blizzard paint is yours, on every machine', sk.own && sk.col === '#7fc8f8' && sk.name === 'BLIZZARD', sk);
  await EV(base(`save.fbRuns=12;save.evPaints={blizzard:true};save.evPaintSel='blizzard';state='garage';skinFor=TOOLS[save.tool].id;skinSel=6`)); await p.waitForTimeout(500);
  u = await ui(); ok('skin panel: a 7th slot for the paint', u.includes('sks6'), u.filter(x => /^sks|^ske/.test(x)));
  await shot('skin_paint');
  await EV(base(`save.fbRuns=12;save.gems=100;save.ev={id:'test-blizzard',flakes:40,got:1,runs:1};passOpen=true`)); await p.waitForTimeout(300);
  await layout('Event Pass card, not enough gems'); await shot('pass_card_poor');
  e = await EV(`(()=>{draw();const g0=save.gems;ui.find(x=>x.id==='passgem').fn();return JSON.stringify({gems:save.gems-g0,pass:save.evPass,shop:shopOpen,tab:shopTab,need:shopNeed&&shopNeed.cost-save.gems});})()`);
  ok('short of gems: nothing taken, the shop opens on the gem packs (needs 150 more)', e.gems === 0 && !e.pass && e.shop && e.tab === 0 && e.need === 150, e);
  await EV(base(`save.fbRuns=12;save.gems=0;save.ev={id:'test-blizzard',flakes:40,got:1,runs:1};passOpen=true`)); await p.waitForTimeout(300);
  e = await EV(`(()=>{draw();ui.find(x=>x.id==='passbuy').fn();return JSON.stringify({pass:save.evPass,flakes:save.ev.flakes});})()`);
  ok('or buy it with money', e.pass === 'test-blizzard' && e.flakes === 80, e);
  await EV(base(`save.fbRuns=12;save.evPass='test-blizzard';save.ev={id:'test-blizzard',flakes:80,got:2,runs:1}`)); await p.waitForTimeout(400); await shot('map_banner_x2');
  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await br.close();
})();
