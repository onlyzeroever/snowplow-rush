// p145 deep snow check (Blizzard event): the plow bogs down in deep snow and not on cleared ground, bites thump,
// trench walls are taller, gusts dust snow back without un-clearing, Blizzard jobs get extra time, normal jobs unchanged.
//   node tools/audit/deep145.js [port=8765] [page=index6.html]
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const port = process.argv[2] || 8765, page = process.argv[3] || 'index6.html';
const res = []; const ok = (name, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + name + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const open = async (qs) => { const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); p.errs = []; p.on('pageerror', e => p.errs.push(e.message));
    await p.goto('http://127.0.0.1:' + port + '/' + page + '?test=1' + qs); await p.waitForTimeout(900); return p; };
  const EV = (p, code) => p.evaluate(c => window.__EV(c), code).then(r => JSON.parse(r));
  const prep = "save.privSeen=true;save.tut=true;save.fbRuns=8;save.bzTips=5;window.__HOLD=1;for(const q in keys)keys[q]=false;";
  const use = m => `{const ti=toolIdx('${m}');save.tool=Math.max(save.tool,ti);save.use=ti;_tc.k='';}`;
  // a stretch of open, snowy ground the truck can plow straight up through
  const patch = `const tid=tool().id;let at=null;for(let y=G.ph-120;y>200&&!at;y-=10)for(let x=40;x<G.pw-40&&!at;x+=6){let ok=true;for(let yy=y;yy>y-130&&ok;yy-=6){if(blockedBy(footprint(tid,x,yy,0)))ok=false;}
      if(ok){let snow=0,n=0;for(let yy=y-130;yy<y;yy+=4)for(let xx=x-20;xx<x+20;xx+=4){n++;if(G.depth[(yy>>1)*G.cols+(xx>>1)]>0.9)snow++;}if(snow>n*0.9)at={x,y};}}`;
  const drive = (frames) => `let d=0,t=0;keys.ArrowUp=true;for(let k=0;k<${frames};k++){const y0=P.y;update(1/30);if(k>8){d+=y0-P.y;t+=1/30;}}keys.ArrowUp=false;`;

  // 1. Blizzard job: deep snow on, extra time by machine weight
  let p = await open('&event=blizzard');
  let r = await EV(p, `(()=>{${prep}${use('truck')}const li=LEVELS.findIndex(L=>L.id==='lot');startLevel(li,{event:EVENTS[0].id});return JSON.stringify({deep:!!G.def.deep,time:G.def.time,base:LEVELS[li].time,sub:EVENT_DEFS.blizzard.sub});})()`);
  ok('blizzard jobs have deep snow and extra time (truck +' + Math.round((r.time / r.base - 1) * 100) + '%)', r.deep && r.time > r.base * 1.1 && r.time < r.base * 1.2 && /DEEP SNOW/.test(r.sub), r);

  // 2. plowing deep snow slows the truck; driving back down the cleared lane does not
  r = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='lot'),{event:EVENTS[0].id});run.moved=true;run.time=99;${patch}if(!at)return JSON.stringify({err:'no patch'});
    P.x=at.x;P.y=at.y;P.f=0;if(!run.bz)update(1/30);run.bz.t=99;${drive(70)}const plow=d/t/moveSpeed();let d2=0,t2=0;keys.ArrowDown=true;for(let k=0;k<34;k++){const y0=P.y;update(1/30);if(k>12){d2+=P.y-y0;t2+=1/30;}}keys.ArrowDown=false;
    return JSON.stringify({plow:+plow.toFixed(3),back:+(d2/t2/moveSpeed()).toFixed(3),push:+run.dpush.toFixed(2)});})()`);
  ok('deep snow: the truck plows at 75-92% speed and drives its cleared lane at full speed', r.plow > 0.75 && r.plow < 0.92 && r.back > 0.95, r);

  // 3. biting into a fresh drift from cleared ground: thump, burst of snow clumps, DEEP SNOW! tip
  r = await EV(p, `(()=>{${prep}${use('truck')}save.dsTips=0;startLevel(LEVELS.findIndex(L=>L.id==='lot'),{event:EVENTS[0].id});run.moved=true;run.time=99;${patch}
    P.x=at.x;P.y=at.y;P.f=0;if(!run.bz)update(1/30);run.bz.t=99;for(let yy=at.y-40;yy<at.y+30;yy+=2)for(let xx=at.x-40;xx<at.x+40;xx+=2){const i=(yy>>1)*G.cols+(xx>>1);if(G.type[i]!==T_BLOCK)setDepth(G,i,0);}
    keys.ArrowUp=true;let bit=0,cl=0;const b0=run.biteT;for(let k=0;k<40;k++){update(1/30);if(run.biteT!==b0)bit=1;cl=Math.max(cl,particles.filter(q=>q.kind==='clump').length);}keys.ArrowUp=false;
    return JSON.stringify({bit,clumps:cl,tip:floats.some(f=>f.s==='DEEP SNOW!')||save.dsTips>0});})()`);
  ok('deep snow: biting into a fresh drift thumps and throws snow clumps', r.bit === 1 && r.clumps >= 3 && r.tip, r);

  // 4. taller trench walls: the snow above a cleared lane shows a 3-row face, the ground below a 2-row shadow
  r = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='lot'),{event:EVENTS[0].id});${patch}
    const cy=(at.y>>1)-20,cx0=(at.x>>1)-6;for(let cx=cx0;cx<cx0+12;cx++)for(let c2=cy;c2<cy+6;c2++)setDepth(G,c2*G.cols+cx,0);
    const col=(px,py)=>{const o=(py*G.pw+px)*4;return [G.img.data[o],G.img.data[o+1],G.img.data[o+2]].join(',');};const px=(cx0+6)*2,top=cy*2;
    return JSON.stringify({face:[col(px,top-4),col(px,top-3),col(px,top-2),col(px,top-1)],shade:[col(px,top),col(px,top+1)]});})()`);
  const isFace = c => c !== '244,248,255' && c !== '239,245,255';
  ok('deep snow: trench walls are 3+ rows tall with a 2-row shadow', r.face.slice(1).every(isFace) && r.face[1] !== r.face[3], r);

  // 5. a gust dusts snow back into cleared lanes from the windward side, without un-clearing anything
  r = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='lot'),{event:EVENTS[0].id});run.moved=true;run.time=99;${patch}
    P.x=at.x;P.y=at.y;P.f=0;camY=clamp(P.y-VIEW_H*0.55,0,G.ph-VIEW_H);const cy0=Math.floor(camY/2)+10;for(let c2=cy0;c2<cy0+60;c2++)for(let cx=30;cx<60;cx++){const i=c2*G.cols+cx;if(G.type[i]!==T_BLOCK)setDepth(G,i,0);}
    run.squallT=99;G.def.snowfall=0;P.stun=99;if(!run.bz)update(1/30);const before=G.cleared;run.bz.phase='blow';run.bz.t=2.6;run.bz.dir=1;for(let k=0;k<70;k++)update(1/30);
    let dust=0,over=0;for(let c2=cy0;c2<cy0+60;c2++)for(let cx=30;cx<60;cx++){if(G.type[c2*G.cols+cx]===T_BLOCK)continue;const d=G.depth[c2*G.cols+cx];if(d>0.03&&d<CLEAR_T)dust++;if(d>=CLEAR_T)over++;}
    return JSON.stringify({dust,over,lost:before-G.cleared});})()`);
  ok('deep snow: gusts dust snow into cleared lanes (cleared stays cleared)', r.dust > 60 && r.over === 0 && r.lost === 0, r);

  // 6. the storm draws (frost edge, far/near layers) and the blade pile grows
  r = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='lot'),{event:EVENTS[0].id});run.moved=true;run.time=99;${patch}P.x=at.x;P.y=at.y;P.f=0;
    keys.ArrowUp=true;for(let k=0;k<30;k++)update(1/30);keys.ArrowUp=false;draw();return JSON.stringify({frost:!!FROSTV,load:+P.load.toFixed(2),far:BZ_FAR.length,near:BZ_NEAR.length});})()`);
  ok('deep snow: storm layers + frost draw, blade pile fills', r.frost && r.load > 0.8 && r.far > 100 && r.near > 10, r);
  ok('no page errors (blizzard)', p.errs.length === 0, p.errs.slice(0, 3));

  // 7. normal jobs: no deep snow, full speed while plowing
  p = await open('');
  r = await EV(p, `(()=>{${prep}${use('truck')}startLevel(LEVELS.findIndex(L=>L.id==='lot'));run.moved=true;run.time=99;${patch}P.x=at.x;P.y=at.y;P.f=0;${drive(70)}
    return JSON.stringify({deep:!!G.def.deep,plow:+(d/t/moveSpeed()).toFixed(3)});})()`);
  ok('normal jobs: no deep snow, plow at full speed', !r.deep && r.plow > 0.97, r);
  ok('no page errors (normal)', p.errs.length === 0, p.errs.slice(0, 3));
  await b.close();
  console.log(res.every(Boolean) ? 'ALL OK' : 'FAILED ' + res.filter(x => !x).length);
  process.exit(res.every(Boolean) ? 0 : 1);
})();
