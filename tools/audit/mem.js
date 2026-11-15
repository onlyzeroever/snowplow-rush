const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox','--js-flags=--expose-gc'] });
  const p = await (await b.newContext({viewport:{width:390,height:844}})).newPage(); await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(800);
  const r = await p.evaluate(()=>{ window.__HOLD=true; const R=window.__SR,M=window.__MONEY,L=R.LEVELS; R.save.tut=true; R.save.tool=7; R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};
    const heap=()=>{ gc(); return Math.round(performance.memory.usedJSHeapSize/1e6); }; const pts=[heap()];
    for(let round=0;round<3;round++){ for(let i=0;i<L.length;i+=3){ R.save.use=Math.min(7,i%8); M.startLevel(i); window.__STEP(40,1/30,1); try{M.endRound(true);}catch(e){} window.__STEP(30,1/30,1); try{R.goHome();}catch(e){} window.__STEP(10,1/30,1); } pts.push(heap()); }
    return pts; });
  console.log('heap MB after each pass of ~42 jobs:', r.join(' -> ')); await b.close(); })();
