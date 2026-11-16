const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const pg=process.argv[2]||'cand.html',out=process.argv[3]||'/tmp/audit/slide.png',from=process.argv[4]||'map',press=process.argv[5]||'nav-upg';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext({viewport:{width:360,height:640}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+pg+'?test=1');await p.waitForTimeout(800);
 const shots=await p.evaluate(async([from,press])=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;const raf=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  R.save.tut=true;R.save.privSeen=true;R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};R.save.tool=4;R.save.coins=12345;
  if(from==='map')R.goMap();else if(from==='upgrades')R.goUpgrades();else R.goGarage();EV('dailyOpen=false');R.dailyOpen=false;
  for(let i=0;i<3;i++){await raf();window.__STEP(6,1/30,1);}await raf();const out=[document.querySelector('canvas').toDataURL()];
  window.__UI.press(press);let el=0;for(const t of [0.05,0.1,0.16,0.4]){const d=t-el;el=t;window.__STEP(Math.max(1,Math.round(d/(1/120))),1/120,1);await raf();await raf();out.push(document.querySelector('canvas').toDataURL());}
  return out;},[from,press]);
 const u=await (await b.newContext()).newPage();const url=await u.evaluate(async(sh)=>{const load=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});const c=document.createElement('canvas');c.width=sh.length*368;c.height=640;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
  for(let k=0;k<sh.length;k++){x.drawImage(await load(sh[k]),k*368,0);}return c.toDataURL();},shots);
 fs.writeFileSync(out,Buffer.from(url.split(',')[1],'base64'));console.log('ok',errs);await b.close();})();
