// UI fuzzer: from several save states, keep pressing random on-screen buttons; log console errors, stuck states, NaN/negative money.
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const VP={small:{width:320,height:568},phone:{width:390,height:844},tablet:{width:820,height:1180}};
const SAVES={
 fresh:null,
 early:{v:6,tv:2,tut:true,story:{suburbs:true},coins:3000,gems:10,tool:1,use:1,stars:[3,2,2,1,1,0,0,0],best:[80,70,70,60,50]},
 mid:{v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true,themepark:true},coins:900000,gems:120,tool:4,use:4,areaSeen:3,tolls:{retreat:true},winters:1},
 late:{v:6,tv:2,tut:true,story:{suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true},coins:9e8,gems:900,tool:7,use:7,areaSeen:7,tolls:{retreat:true,stadium:true},winters:2,pro:true,parts:{monster:2,jet:3}}};
async function walk(browser,vpName,saveName,seed,presses){
  const ctx=await browser.newContext({viewport:VP[vpName],hasTouch:true,isMobile:true}); const sv=SAVES[saveName];
  if(sv) await ctx.addInitScript(j=>{ if(!sessionStorage.getItem('s')){ localStorage.setItem('snowplowRush.test',j); sessionStorage.setItem('s','1'); } },JSON.stringify(sv));
  else await ctx.addInitScript(()=>{ if(!sessionStorage.getItem('s')){ localStorage.removeItem('snowplowRush.test'); sessionStorage.setItem('s','1'); } });
  const page=await ctx.newPage(); const errors=[]; page.on('pageerror',e=>errors.push('PAGE '+e.message)); page.on('console',m=>{ if(m.type()==='error') errors.push('CONSOLE '+m.text().slice(0,300)); });
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(700);
  const r=await page.evaluate(([seed,presses])=>{ window.__HOLD=true; const U=window.__UI, R=window.__SR; let rs=seed; const rnd=()=>{ rs=(rs*1103515245+12345)&0x7fffffff; return rs/0x7fffffff; };
    const pressed={}, problems=[], trail=[]; const step=n=>{ try{ window.__STEP(n,1/30,1); }catch(e){ problems.push('STEP '+String(e&&e.stack||e).slice(0,300)+' after '+trail.slice(-4).join('>')); } };
    step(5); let sameState=0, last='';
    for(let k=0;k<presses;k++){ const ids=U.list().filter(id=>!/reset|wipe|delete/i.test(id)); const st=U.state; 
      if(st==='play'){ // play a little, then leave via pause or end
        const K=R.keys; const d=['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'][Math.floor(rnd()*4)]; K[d]=true; step(20); K[d]=false; if(rnd()<0.15){ try{ window.__MONEY.endRound(rnd()<0.5); }catch(e){ problems.push('endRound '+e); } step(60); } }
      if(!ids.length){ const cv=document.querySelector('canvas'),bb=cv.getBoundingClientRect(),cx=bb.left+bb.width*(0.2+rnd()*0.6),cy=bb.top+bb.height*(0.3+rnd()*0.5),o={clientX:cx,clientY:cy,pointerId:1,bubbles:true,isPrimary:true,pointerType:'touch'}; try{ cv.dispatchEvent(new PointerEvent('pointerdown',o)); step(2); cv.dispatchEvent(new PointerEvent('pointerup',o)); }catch(e){ problems.push('TAP '+e); } trail.push(st+':tap'); step(10); if(++sameState>40){ problems.push('no buttons for 40 rounds in state '+st+' after '+trail.slice(-5).join('>')); break; } continue; }
      sameState=0; const id=ids[Math.floor(rnd()*ids.length)]; pressed[id]=(pressed[id]||0)+1; trail.push(st+':'+id);
      try{ U.press(id); }catch(e){ problems.push('PRESS '+id+' in '+st+': '+String(e&&e.stack||e).slice(0,300)); }
      step(4+Math.floor(rnd()*20));
      const sv=R.save; if(!(sv.coins>=0)||!(sv.gems>=0)||!isFinite(sv.coins)||!isFinite(sv.gems)) { problems.push('money broken coins='+sv.coins+' gems='+sv.gems+' after '+trail.slice(-3).join('>')); break; }
      if(!(sv.tool>=0&&sv.tool<R.TOOLS.length)) problems.push('tool index out of range '+sv.tool);
    }
    return {pressed:Object.keys(pressed).length, problems:[...new Set(problems)].slice(0,8), ids:Object.keys(pressed)}; },[seed,presses]);
  await ctx.close(); return {r,errors:[...new Set(errors)].slice(0,8)}; }
(async()=>{ const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']}); const allIds=new Set(); const out=[];
  const runs=[]; let seed=11; for(const vp of Object.keys(VP)) for(const sv of Object.keys(SAVES)) for(let w=0;w<(+process.env.WALKS||2);w++) runs.push([vp,sv,seed+=97]);
  const q=runs.slice(); const W=[]; for(let i=0;i<(+process.env.PAR||4);i++) W.push((async()=>{ while(q.length){ const [vp,sv,sd]=q.shift(); const res=await walk(browser,vp,sv,sd,+process.env.PRESSES||250); res.r.ids.forEach(x=>allIds.add(x));
    const line=vp+' '+sv+' seed'+sd+' pressed '+res.r.pressed+' problems '+JSON.stringify(res.r.problems)+' errors '+JSON.stringify(res.errors); out.push(line); console.log(line); } })());
  await Promise.all(W); fs.writeFileSync('/tmp/audit/uifuzz.txt',out.join('\n')+'\nALL IDS '+allIds.size+': '+[...allIds].sort().join(' ')); await browser.close(); })();
