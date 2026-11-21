// lab p185: the big Snow Bank after the first one (lab only); p186: EVENT PASS+ (lab and app build), switchable per event
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
let fails = 0; const ok = (n, c, d) => { console.log((c ? 'ok   ' : 'FAIL ') + n + (d !== undefined && !c ? ' ' + JSON.stringify(d) : '')); if (!c) fails++; };
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await br.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  const FILE = process.argv[2] || 'lab6.html'; await p.goto(`http://127.0.0.1:8766/${FILE}?test=1`); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(r => { try { return JSON.parse(r); } catch (e) { return r; } });
  const shot = async n => { const u = await EV(`JSON.stringify(b.canvas.toDataURL())`); fs.writeFileSync(`/tmp/audit/m/m185_${n}.png`, Buffer.from(u.split(',')[1], 'base64')); };
  const base = `save.privSeen=true;save.tut=true;save.sess=4;save.gems=40;save.coins=5000;save.fbRuns=14;save.evPass=null;save.evPassPlus=null;goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;remindAsk=null;evOpen=false;bankOpen=false;passOpen=false;gotCard=null;shopOpen=false;weeklyOpen=false;}catch(e){};`;
  const hasBig = await EV(`typeof BANK2!=='undefined'`); console.log(FILE, hasBig ? '(big jar here)' : '(no big jar in this build: PASS+ checks only)');
  if (hasBig) {
  // first jar -> buy -> the big jar
  await EV(`(()=>{${base}save.bank={g:260,seen:true,intro:true};bankOpen=true;return 1;})()`); await p.waitForTimeout(300);
  let a = await EV(`JSON.stringify({open:SHOP.bank.open,max:SHOP.bank.max,price:SHOP.bank.price,big:!!SHOP.bank.big})`);
  ok('the first jar: opens at 220, holds 400, $2.99', a.open === 220 && a.max === 400 && a.price === '$2.99' && !a.big, a);
  let c = await EV(`(()=>{draw();const g0=save.gems;ui.find(x=>x.id==='bankbuy').fn();return JSON.stringify({gems:save.gems-g0,bank:bankG(),broken:save.bank.broken,got:gotCard&&gotCard.title,rows:gotCard&&gotCard.rows.map(r=>r[1]),big:!!SHOP.bank.big,open:SHOP.bank.open,max:SHOP.bank.max,price:SHOP.bank.price});})()`);
  ok('opening it gives the 260 gems, and a BIG jar takes its place (440 / 800 / $4.99)', c.gems === 260 && c.bank === 0 && c.broken === 1 && c.big && c.open === 440 && c.max === 800 && c.price === '$4.99' && /BIG JAR, 800/.test(c.rows.join('|')), c);
  await shot('got1');
  await EV(`(()=>{gotCard=null;save.bank.g=500;bankOpen=true;return 1;})()`); await p.waitForTimeout(300); await shot('bigcard');
  const t = await EV(`(()=>{const T=[];const o=text;text=function(g,s){T.push(String(s));return o.apply(this,arguments);};draw();text=o;return JSON.stringify(T);})()`);
  ok('the big jar card says BIG SNOW BANK, fills twice as fast, and still claims only what the prices back (UP TO 2X)', t.includes('BIG SNOW BANK') && t.includes('IT FILLS TWICE AS FAST') && t.some(s => /\+10 GEMS A JOB, \+4 A STAR/.test(s)) && t.includes('2X VALUE'), t.filter(s => /BANK|FAST|GEMS A JOB|VALUE/.test(s)));
  c = await EV(`(()=>{const g0=save.gems;ui.find(x=>x.id==='bankbuy').fn();return JSON.stringify({gems:save.gems-g0,bank:bankG(),broken:save.bank.broken,big:!!SHOP.bank.big,rows:gotCard&&gotCard.rows.map(r=>r[1]),title:gotCard&&gotCard.title});})()`);
  ok('the big jar opens for its 500 gems and starts again (still big)', c.gems === 500 && c.bank === 0 && c.broken === 2 && c.big && c.title === 'BIG SNOW BANK' && /BIG JAR STARTS AGAIN/.test(c.rows.join('|')), c);
  // a job fills the big jar twice as fast
  await EV(`(()=>{gotCard=null;window.__HOLD=1;startLevel(0,{});G.cleared=Math.round(G.clearable*0.95);run.contUsed=true;run.moved=true;run.time=0.01;update(0.05);window.__HOLD=0;return 1;})()`); await p.waitForTimeout(200);
  const j = await EV(`JSON.stringify({g:bankG(),stars:run.res?run.res.stars:null})`); ok('a job puts +10 and +4 a star in the big jar', j.g === 10 + 4 * (j.stars || 0), j);
  }
  // EVENT PASS+
  await EV(`(()=>{${base}EVENTS.unshift({id:'t185',kind:'blizzard',start:Date.now()-1000,end:Date.now()+86400e3});save.ev={id:'t185',flakes:40,got:1,runs:2};passOpen=true;return 1;})()`); await p.waitForTimeout(300); await shot('pass');
  const u = await EV(`(()=>{draw();return JSON.stringify(ui.map(x=>x.id));})()`); ok('the pass card offers PASS+ next to the pass', u.includes('passplus') && u.includes('passbuy') && u.includes('passgem'), u);
  c = await EV(`(()=>{ui.find(x=>x.id==='passplus').fn();const e=save.ev;return JSON.stringify({owned:save.evPass,plus:save.evPassPlus,flakes:e.flakes,got:e.got,title:gotCard&&gotCard.title,rows:gotCard&&gotCard.rows.map(r=>r[1])});})()`);
  ok('PASS+ doubles the flakes, adds 300, pays out the steps reached, and says so', c.owned === 't185' && c.plus === 't185' && c.flakes === 40 * 2 + 300 && c.got === 5 && c.title === 'EVENT PASS+' && /300 FLAKES HEAD START/.test(c.rows.join('|')), c);
  await shot('passgot');
  // switched off for one event from the schedule: the card shows the plain pass only
  const off = await EV(`(()=>{${base}EVENTS.unshift({id:'t185b',kind:'blizzard',start:Date.now()-1000,end:Date.now()+86400e3,plus:false});save.ev={id:'t185b',flakes:0,got:0,runs:0};passOpen=true;draw();return JSON.stringify(ui.map(x=>x.id));})()`);
  ok('an event marked plus:false in the schedule hides PASS+', !off.includes('passplus') && off.includes('passbuy'), off);
  await EV(`(()=>{EVENTS.shift();return 1;})()`);
  // layout of the pass card with PASS+: nothing overlaps, everything inside the panel
  await EV(`(()=>{${base}save.ev={id:'t185',flakes:0,got:0,runs:0};passOpen=true;return 1;})()`); await p.waitForTimeout(300);
  const lay = await EV(`(()=>{const L=[];const o=text,ob=button,od=drawPass,op2=priceRow;drawPass=function(){window.__INP=1;try{return od.apply(this,arguments);}finally{window.__INP=0;}};priceRow=function(){window.__INB=1;try{return op2.apply(this,arguments);}finally{window.__INB=0;}};text=function(g,s,x,y,col,op){op=op||{};if(g===b&&window.__INP){const w=textW(String(s),op.scale||1);let X=x;if(op.align==='center')X=x-Math.floor(w/2);else if(op.align==='right')X=x-w;L.push({k:'t',s:String(s),x:X,y,w,h:5*(op.scale||1),inb:!!window.__INB});}return o.apply(this,arguments);};
    button=function(id,x,y,w,h){if(window.__INP)L.push({k:'b',id,x,y,w,h});window.__INB=1;try{return ob.apply(this,arguments);}finally{window.__INB=0;}};draw();text=o;button=ob;drawPass=od;priceRow=op2;return JSON.stringify(L);})()`);
  const T = lay.filter(e => e.k === 't' && !e.inb && e.y > 30), B = lay.filter(e => e.k === 'b' && /^pass/.test(e.id)), ov = (a, d) => a.x < d.x + d.w && d.x < a.x + a.w && a.y < d.y + d.h && d.y < a.y + a.h, prob = [];
  for (const tt of T) for (const bb of B) if (ov(tt, bb)) prob.push(tt.s + ' / ' + bb.id);
  for (let i = 0; i < B.length; i++) for (let k = i + 1; k < B.length; k++) if (ov(B[i], B[k])) prob.push(B[i].id + ' / ' + B[k].id);
  ok('pass card with PASS+: no text over buttons, no buttons over buttons', prob.length === 0, prob);
  ok('no page errors', errs.length === 0, errs.slice(0, 3));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await br.close();
})();
