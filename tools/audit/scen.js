const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const NOW=Date.now();
const SC=[
 ['offline collect', {v:6,tv:2,tut:true,story:{suburbs:true},coins:1000,tool:2,use:2,lv:{speed:0,size:0,value:0,bumper:0,helpers:3},mlv:{},last:NOW-3*3600e3}, ['collect']],
 ['offline ad', {v:6,tv:2,tut:true,story:{suburbs:true},coins:1000,tool:2,use:2,lv:{speed:0,size:0,value:0,bumper:0,helpers:3},mlv:{},last:NOW-3*3600e3}, ['offad','@wait90']],
 ['refund note', {v:6,tv:2,tut:true,story:{suburbs:true},coins:50,tool:1,use:1,lv:{speed:4,size:3,value:0,bumper:0,helpers:0}}, ['refundok']],
 ['continue offer', {v:6,tv:2,tut:true,story:{suburbs:true},coins:50,tool:0,use:0,mlv:{}}, ['@job:park','@timeout','cont','@wait90','@timeout','nocont']],
 ['winter', {v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true},coins:5e7,tool:7,use:7,mlv:{},areaSeen:7,allstars:3}, ['@map','winter','wno','winter','wgo']],
 ['shop ride', {v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true},coins:9e8,gems:999,tool:7,use:7,mlv:{},rideSeen:{monster:true}}, ['@map','shop','sride']],
 ['shop ride gems', {v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true},coins:0,gems:999,tool:7,use:7,mlv:{},rideSeen:{monster:true}}, ['@map','shop','srideg']],
 ['toll', {v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true},coins:9e6,tool:4,use:4,mlv:{},allstars:3,upto:'stadium'}, ['@map','@info:stadium','jtoll','jplay']],
 ['garage ride peek', {v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true},coins:9e8,gems:10,tool:7,use:7,mlv:{}}, ['@map','nav-gar','ride','@wait30']],
];
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const [name, sv, acts] of SC) { const ctx = await browser.newContext({ viewport:{width:390,height:844} });
    await ctx.addInitScript(j=>{ if(!sessionStorage.getItem('s')){ localStorage.setItem('snowplowRush.test',j); sessionStorage.setItem('s','1'); } }, JSON.stringify(sv));
    const page = await ctx.newPage(); const errors=[]; page.on('pageerror',e=>errors.push('PAGE '+e.message)); page.on('console',m=>{ if(m.type()==='error') errors.push('CONSOLE '+m.text().slice(0,200)); });
    await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(700);
    const log = await page.evaluate(([sv,acts])=>{ window.__HOLD=true; const R=window.__SR, U=window.__UI, M=window.__MONEY, out=[]; const step=n=>{ try{ window.__STEP(n,1/30,1); }catch(e){ out.push('STEP ERR '+e); } };
      if(sv.allstars){ const L=R.LEVELS; L.forEach((l,i)=>{ if(l.area!=='secret'&&(!sv.upto||i<L.findIndex(x=>x.id===sv.upto))) { R.save.stars[i]=sv.allstars; R.save.best[i]=90; } }); }
      step(10); const snap=()=>({st:U.state,c:Math.round(R.save.coins),g:R.save.gems,tool:R.save.tool,w:R.save.winters||0});
      out.push('start '+JSON.stringify(snap())+' buttons: '+U.list().slice(0,14).join(','));
      for(const a of acts){
        if(a==='@map'){ try{ R.goHome&&R.goHome(); }catch(e){} step(20); if(U.state==='title'){ const cv=document.querySelector('canvas'),bb=cv.getBoundingClientRect(),o={clientX:bb.left+bb.width/2,clientY:bb.top+bb.height*0.7,pointerId:1,bubbles:true,isPrimary:true}; cv.dispatchEvent(new PointerEvent('pointerdown',o)); step(2); cv.dispatchEvent(new PointerEvent('pointerup',o)); step(30);} out.push('@map -> '+JSON.stringify(snap())); continue; }
        if(a.startsWith('@wait')){ step(+a.slice(5)); continue; }
        if(a.startsWith('@job:')){ const i=R.LEVELS.findIndex(l=>l.id===a.slice(5)); M.startLevel(i); step(120); out.push('job started '+JSON.stringify(snap())); continue; }
        if(a.startsWith('@info:')){ R.jobInfo=R.LEVELS.findIndex(l=>l.id===a.slice(6)); step(5); out.push('info open, buttons '+U.list().join(',')); continue; }
        if(a==='@timeout'){ const run=M.run; if(run){ run.time=0.05; } step(60); out.push('after timeout '+JSON.stringify(snap())+' offer='+!!(M.run&&M.run.offer)+' buttons '+U.list().join(',')); continue; }
        const ids=U.list(); const id=ids.find(x=>x===a)||ids.find(x=>x.startsWith(a)); if(!id){ out.push('MISSING button '+a+' (have: '+ids.join(',')+')'); continue; }
        U.press(id); step(15); out.push('pressed '+id+' -> '+JSON.stringify(snap())); }
      return out; },[sv,acts]);
    console.log('### '+name); console.log(log.join('\n')); if(errors.length) console.log('ERRORS',JSON.stringify(errors.slice(0,5))); await ctx.close(); }
  await browser.close(); })();
