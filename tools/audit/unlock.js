const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext()).newPage(); const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(800);
  const r = await p.evaluate(() => { const R=window.__SR, L=R.LEVELS, S=R.save; window.__HOLD=true;
    S.tut=true; S.stars=L.map(()=>0); S.best=L.map(()=>0); S.tolls={}; S.winters=0; S.tool=0; S.coins=0;
    const order=[]; const opened=new Set(); let changed=true, rounds=0;
    while(changed&&rounds<400){ changed=false; rounds++;
      for(let i=0;i<L.length;i++){ if(opened.has(i)) continue; let ok=false; try{ ok=R.levelOpen(i); }catch(e){ return {err:'levelOpen '+e}; } if(ok){ opened.add(i); order.push(L[i].id); S.stars[i]=1; S.best[i]=40; changed=true; } }
      if(!changed){ // try paying tolls, buying next machine, next winter, more stars
        for(let i=0;i<L.length;i++) if(L[i].toll&&!S.tolls[L[i].id]){ S.tolls[L[i].id]=true; changed=true; }
        if(!changed){ for(let i=0;i<L.length;i++) if(opened.has(i)&&S.stars[i]<3){ S.stars[i]=3; changed=true; } }
        if(!changed&&S.tool<R.TOOLS.length-1){ S.tool++; changed=true; }
        if(!changed&&S.winters<3){ S.winters++; changed=true; } } }
    const never=L.map((l,i)=>[l.id,l.area,i]).filter(x=>!opened.has(x[2])).map(x=>x[0]+'('+x[1]+')');
    return {opened:opened.size,total:L.length,never,rounds}; });
  console.log(JSON.stringify(r)); console.log('errs',errs.slice(0,3)); await b.close(); })();
