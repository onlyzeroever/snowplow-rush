const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const mode of ['json_ok','json_cors_fail']) { const ctx=await b.newContext({viewport:{width:390,height:844}}); const got=[];
    await ctx.route('https://us.i.posthog.com/**', async r=>{ const req=r.request(), u=req.url();
      if(u.includes('/batch/')){ if(mode==='json_cors_fail'){ await r.abort('failed'); return; } const j=JSON.parse(req.postData()); got.push('batch:'+j.batch.map(e=>e.event).join(',')); }
      else { const d=decodeURIComponent(req.postData().replace(/^data=/,'')); const arr=JSON.parse(Buffer.from(d,'base64').toString('utf8')); got.push('form:'+arr.map(e=>e.event+(e.properties.token?'':'(NO TOKEN)')).join(',')+' id='+arr[0].properties.distinct_id.slice(0,6)); }
      await r.fulfill({status:200,headers:{'access-control-allow-origin':'*'},body:'{"status":1}'}); });
    const p=await ctx.newPage(); await p.goto('http://127.0.0.1:8765/index6.html'); await p.waitForTimeout(900);
    const cv=await p.locator('canvas').boundingBox(); await p.mouse.click(cv.x+cv.width/2,cv.y+cv.height*0.75); await p.waitForTimeout(500);
    await p.evaluate(()=>window.__MONEY.startLevel(0)); await p.waitForTimeout(2500); await p.evaluate(()=>window.__MONEY.endRound(true)); await p.waitForTimeout(500);
    await p.waitForTimeout(16000); // interval flush
    await p.evaluate(()=>window.__MONEY.startLevel(1)); await p.waitForTimeout(500);
    await p.evaluate(()=>{Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'));}); await p.waitForTimeout(1500);
    console.log(mode, JSON.stringify(got)); await ctx.close(); }
  await b.close(); })();
