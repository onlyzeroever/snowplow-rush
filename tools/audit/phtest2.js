const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const run=async(url,fn)=>{ const ctx=await b.newContext({viewport:{width:390,height:844}}); const got=[]; await ctx.route('https://us.i.posthog.com/**',async r=>{got.push(JSON.parse(r.request().postData()).batch.map(e=>e.event));await r.fulfill({status:200,headers:{'access-control-allow-origin':'*'},body:'{}'});});
    const p=await ctx.newPage(); await p.goto('http://127.0.0.1:8765/'+url); await p.waitForTimeout(1000); await fn(p); await p.evaluate(()=>{Object.defineProperty(document,'hidden',{value:true,configurable:true});document.dispatchEvent(new Event('visibilitychange'));}); await p.waitForTimeout(1200); await ctx.close(); return got; };
  console.log('test mode:', JSON.stringify(await run('index6.html?test=1', async p=>{ await p.evaluate(()=>window.__MONEY.startLevel(0)); await p.waitForTimeout(500); })));
  console.log('opt-out:', JSON.stringify(await run('index6.html', async p=>{ const cv=await p.locator('canvas').boundingBox(); await p.mouse.click(cv.x+cv.width/2,cv.y+cv.height*0.75); await p.waitForTimeout(600);
     // open settings and press the switch by tapping its position: settings opened via gear; use direct state
     await p.evaluate(()=>{ window.__SR.save.noTrack=false; }); 
     await p.evaluate(()=>{ window.__SR.save.noTrack=true; });
     await p.evaluate(()=>window.__MONEY.startLevel(1)); await p.waitForTimeout(500); })));
  await b.close(); })();
