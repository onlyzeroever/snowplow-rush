const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({viewport:{width:390,height:844}})).newPage(); const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,150))});
  const TH=+(process.env.THROTTLE||1),PG=process.env.PAGE||'index6.html';if(TH>1){const cdp=await p.context().newCDPSession(p);await cdp.send('Emulation.setCPUThrottlingRate',{rate:TH});}
  await p.goto('http://127.0.0.1:8765/'+PG+'?test=1'); await p.waitForTimeout(800);
  await p.evaluate((o)=>{window.__ONLY=o;},process.env.ONLY?process.env.ONLY.split(','):null);
  const r = await p.evaluate(()=>{ window.__HOLD=true; const R=window.__SR,M=window.__MONEY,L=R.LEVELS,out=[]; R.save.tut=true; R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true}; R.save.tool=7;
    const AT={suburbs:2,farm:3,city:4,themepark:5,harbour:5,ski:6,pass:7,north:7,secret:7};
    const ONLY=window.__ONLY;L.forEach((l,i)=>{if(ONLY&&!ONLY.includes(l.id))return; R.save.use=l.tool?R.TOOLS.findIndex(t=>t.id===l.tool):AT[l.area]; if(R.save.use>R.save.tool) R.save.tool=R.save.use; const t0=performance.now(); M.startLevel(i); const tb=performance.now()-t0; window.__STEP(100,1/30,1);
      const P=R.P; const ts=[]; for(let k=0;k<6;k++){ P.y=Math.max(30,R.G.ph*(1-k/6)-40); const a=performance.now(); window.__STEP(20,1/30,1); ts.push((performance.now()-a)/20); }
      out.push([l.id,+tb.toFixed(0),+(ts.reduce((x,y)=>x+y,0)/ts.length).toFixed(2),+Math.max(...ts).toFixed(2)]); try{M.endRound(true);}catch(e){} window.__STEP(5,1/30,1); });
    return out; });
  require('fs').writeFileSync(process.env.OUTJ||'/tmp/perf_out.json',JSON.stringify(r));r.sort((a,b)=>b[3]-a[3]); const med=r.map(x=>x[2]).sort((a,b)=>a-b)[r.length>>1];
  console.log('median ms/frame',med,' slowest:'); r.slice(0,12).forEach(x=>console.log(' ',x.join(' '))); const bl=r.slice().sort((a,b)=>b[1]-a[1]).slice(0,6); console.log('slowest build ms:',bl.map(x=>x[0]+':'+x[1]).join(' '));
  console.log('errs',errs.slice(0,3)); await b.close(); })();
