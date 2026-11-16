// node bookshot.js page out.png [found keys csv] [extra EV after open]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const [pg,out,keys,extra]=process.argv.slice(2);
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext({viewport:{width:360,height:640}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+pg+'?test=1');await p.waitForTimeout(800);
 const u=await p.evaluate(async([keys,extra])=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;const raf=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  R.save.tut=true;R.save.privSeen=true;R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};R.save.tool=4;
  R.save.treasures={};for(const k of (keys||'').split(',').filter(Boolean))R.save.treasures[k]=true;R.goMap();EV('dailyOpen=false');R.dailyOpen=false;
  await raf();window.__STEP(9,1/30,0);await raf();EV('bookOpen=true');if(extra)EV(extra);for(let i=0;i<4;i++){await raf();window.__STEP(9,1/30,0);}await raf();await raf();return document.querySelector('canvas').toDataURL();},[keys,extra]);
 fs.writeFileSync(out,Buffer.from(u.split(',')[1],'base64'));console.log('ok',errs);await b.close();})();
