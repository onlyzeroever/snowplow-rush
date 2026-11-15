const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const W=[['bad json','{"coins":12'],['coins string',{v:6,tv:2,coins:'abc',tut:true}],['tool 99',{v:6,tv:2,tool:99,use:99,tut:true}],['use -5',{v:6,tv:2,tool:3,use:-5,tut:true}],['stars string',{v:6,tv:2,stars:'x',best:7,tut:true}],
 ['huge upgrades',{v:6,tv:2,tut:true,mlv:{shovel:{speed:999,size:999,bumper:999}},lv:{value:999,helpers:999}}],['parts 99',{v:6,tv:2,tut:true,tool:7,parts:{monster:99,zzz:3}}],['bad skins',{v:6,tv:2,tut:true,skin:{shovel:99,nope:2},skins:{x:1},outfit:'nope',hat:'nope',trail:'nope'}],
 ['bad daily/weekly',{v:6,tv:2,tut:true,daily:{goal:'?'},weekly:5,dailySeen:7}],['nulls',{v:6,tv:2,tut:true,coins:null,gems:null,lv:null,mlv:null,stars:null,tolls:null,story:null}],['negative',{v:6,tv:2,tut:true,coins:-500,gems:-3}],['future last',{v:6,tv:2,tut:true,last:Date.now()+9e9,lv:{helpers:5}}],['ancient v0',{coins:500,tool:1,stars:[3,2,1,1,0],best:[90,80,70,60,0]}]];
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const [name, sv] of W) { const ctx = await browser.newContext({ viewport:{width:390,height:844} }); const raw=typeof sv==='string'?sv:JSON.stringify(sv);
    await ctx.addInitScript(j=>{ if(!sessionStorage.getItem('s')){ localStorage.setItem('snowplowRush.test',j); sessionStorage.setItem('s','1'); } }, raw);
    const page = await ctx.newPage(); const errors=[]; page.on('pageerror',e=>errors.push('PAGE '+e.message)); page.on('console',m=>{ if(m.type()==='error') errors.push('CONSOLE '+m.text().slice(0,200)); });
    await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(700);
    const r = await page.evaluate(()=>{ window.__HOLD=true; const R=window.__SR,U=window.__UI,M=window.__MONEY, out={}; const step=n=>{ try{ window.__STEP(n,1/30,1); }catch(e){ out.err=(out.err||'')+' STEP '+String(e).slice(0,160); } };
      step(10); const cv=document.querySelector('canvas'),bb=cv.getBoundingClientRect(),o={clientX:bb.left+bb.width/2,clientY:bb.top+bb.height*0.7,pointerId:1,bubbles:true,isPrimary:true}; cv.dispatchEvent(new PointerEvent('pointerdown',o)); step(2); cv.dispatchEvent(new PointerEvent('pointerup',o)); step(30);
      for(const k of ['collect','refundok','dclose','wno']) if(U.list().includes(k)){ U.press(k); step(10); }
      out.map=U.state; try{ M.startLevel(0); }catch(e){ out.err=(out.err||'')+' start '+e; } step(200); out.play=U.state; try{ M.endRound(true); }catch(e){} step(100); try{ R.goHome(); }catch(e){} step(20);
      for(const id of ['nav-gar','nav-upg','shop']){ if(U.list().includes(id)){ U.press(id); step(20); } }
      const s=R.save; out.save={coins:s.coins,gems:s.gems,tool:s.tool,use:s.use}; out.ok=isFinite(s.coins)&&s.coins>=0&&isFinite(s.gems)&&s.gems>=0&&s.tool>=0&&s.tool<R.TOOLS.length; return out; });
    console.log(name.padEnd(18), JSON.stringify(r), errors.length?'ERRORS '+JSON.stringify([...new Set(errors)].slice(0,3)):''); await ctx.close(); }
  await browser.close(); })();
