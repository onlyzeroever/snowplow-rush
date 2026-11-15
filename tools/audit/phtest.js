const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const page_ of ['index6.html','dev.html']) {
  const ctx = await b.newContext({ viewport:{width:390,height:844} }); const got=[]; const errs=[];
  await ctx.route('https://us.i.posthog.com/**', async (route) => { const req=route.request(); try{ const j=JSON.parse(req.postData()); got.push({url:req.url(),key:j.api_key,events:j.batch.map(e=>e.event+'('+(e.properties.job||e.properties.name||e.properties.kind||e.properties.item||'')+')'),sample:j.batch[0].properties}); }catch(e){ got.push({bad:req.postData()}); }
    await route.fulfill({status:200,headers:{'access-control-allow-origin':'*','content-type':'application/json'},body:'{"status":"Ok"}'}); });
  const p = await ctx.newPage(); p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto('http://127.0.0.1:8765/'+page_); await p.waitForTimeout(1200);
  const cv=await p.locator('canvas').boundingBox(); await p.mouse.click(cv.x+cv.width/2,cv.y+cv.height*0.75); await p.waitForTimeout(800);
  await p.evaluate(()=>{ const M=window.__MONEY; M.startLevel(0); }); await p.waitForTimeout(4000);
  await p.evaluate(()=>{ window.__SR.keys.ArrowUp=true; }); await p.waitForTimeout(1500); await p.evaluate(()=>{ window.__SR.keys.ArrowUp=false; window.__MONEY.endRound(true); });
  await p.waitForTimeout(1500);
  await p.evaluate(()=>{ Object.defineProperty(document,'visibilityState',{value:'hidden',configurable:true}); Object.defineProperty(document,'hidden',{value:true,configurable:true}); document.dispatchEvent(new Event('visibilitychange')); });
  await p.waitForTimeout(1500);
  console.log('### '+page_+' requests:',got.length); for(const g of got) console.log(JSON.stringify({key:g.key&&g.key.slice(0,8),events:g.events})); if(got[0]) console.log('sample props:',JSON.stringify(got[0].sample).slice(0,600)); console.log('errs',errs.slice(0,3));
  await ctx.close(); }
  await b.close(); })();
