// p130-p132: UFO blocked only by buildings, capstone lock, upgrades banner, Ride Mastery. node tools/audit/ufo_mastery130.js
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
let fails = 0; const ok = (c, m) => { console.log((c ? 'ok   ' : 'FAIL ') + m); if (!c) fails++; };
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] }); const p = await (await b.newContext()).newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(c => window.__EV(c), c);
  // collision: a building blocks, a car does not
  const col = JSON.parse(await EV(`(()=>{window.__HOLD=1;save.tut=true;save.tool=toolIdx('icebreaker');save.ibEver=true;save.rides={monster:true,jet:true,mech:true,dragon:true,ufo:true};save.use=toolIdx('ufo');_tc.k='';
    startLevel(LEVELS.findIndex(L=>L.id==='street'));const bld=G.obstacles.find(o=>o.bld),car=G.obstacles.find(o=>!o.bld&&o.w===22&&o.h===28);
    const inB=blockedBy({x:bld.x+2,y:bld.y+2,w:6,h:6}),inC=car?blockedBy({x:car.x+2,y:car.y+2,w:6,h:6}):'nocar';return JSON.stringify({inB,inC,nb:G.obstacles.filter(o=>o.bld).length});})()`));
  ok(col.inB === 'ob', 'a building blocks the UFO'); ok(col.inC === null, 'a car does not block the UFO ' + JSON.stringify(col));
  // capstone lock
  const lk = JSON.parse(await EV(`(()=>{const U=toolIdx('ufo');save.tool=toolIdx('rotary');save.ibEver=false;save.rides={monster:true,jet:true,mech:true,dragon:true};
    const a=rideNextIdx(),bb=rideForSale(),c=nextRideIdx();save.tool=toolIdx('icebreaker');const d=rideNextIdx()===U;save.tool=0;const e=rideNextIdx()===U;save.ibEver=false;save.rides.ufo=true;const f=owns(U);return JSON.stringify({a,bb,c,d,e,f});})()`));
  ok(lk.a === -1 && lk.bb === -1 && lk.c === -1, 'no route to the UFO before the Icebreaker'); ok(lk.d && lk.e, 'owning the Icebreaker unlocks it for good'); ok(lk.f, 'players who have the UFO keep it');
  // mastery
  const ms = JSON.parse(await EV(`(()=>{save.tool=toolIdx('icebreaker');save.rides={monster:true,jet:true,mech:true,dragon:true,ufo:true};save.mastery={};save.gems=0;const v0=(save.use=toolIdx('monster'),_tc.k='',valueMult());
    mastAdd('monster',12);const lv=mastLv('monster'),g=save.gems,v1=valueMult();mastAdd('monster',100);return JSON.stringify({lv,g,ratio:+(v1/v0).toFixed(3),max:mastLv('monster'),gold:skinOwned('monster',5),goldJet:skinOwned('jet',5),goldTruck:skinOwned('truck',5)});})()`));
  ok(ms.lv === 2 && ms.g === 20 && ms.ratio === 1.04, 'mastery 2: +4% coins with that ride, 20 gems ' + JSON.stringify(ms));
  ok(ms.max === 5 && ms.gold && !ms.goldJet && !ms.goldTruck, 'mastery 5 gives that ride its Gold Paint only');
  ok(errs.length === 0, 'no errors ' + JSON.stringify(errs.slice(0, 3)));
  console.log(fails ? 'FAILS ' + fails : 'ALL OK'); await b.close(); })();
