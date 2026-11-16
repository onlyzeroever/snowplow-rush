const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const out=[];
 for(const pg of ['before_m2.html','index6.html']){const p=await (await b.newContext({viewport:{width:360,height:640}})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/'+pg+'?test=1');await p.waitForTimeout(800);
  const r=await p.evaluate(async()=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;const raf=()=>new Promise(r=>requestAnimationFrame(()=>r()));
   R.save.tut=true;R.save.privSeen=true;R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};R.save.tool=4;
   Object.assign(R.save.stats,{gifts:6,dodges:3,cells:42000,crushed:0,neighbours:1});R.save.ach.first=1;R.save.ach.combo=1;R.save.ach.drive3=1;R.save.treasures={KEY:1,DUCK:1,BEAR:1};R.goMap();
   const shots=[];const snap=async()=>{EV('dailyOpen=false');R.dailyOpen=false;await raf();window.__STEP(9,1/30,0);await raf();window.__STEP(9,1/30,0);await raf();await raf();shots.push(document.querySelector('canvas').toDataURL());};
   EV('trophiesOpen=true;trophyTab=0');await snap();EV('scrollY.trophies=120');await snap();EV('trophiesOpen=false;bookOpen=true');await snap();EV('bookOpen=false;jobInfo=3');await snap();return {shots,errs:[]};});
  out.push(r.shots);if(errs.length)console.log(pg,errs);}
 const u=await (await b.newContext()).newPage();const url=await u.evaluate(async(out)=>{const load=s=>new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=s;});const c=document.createElement('canvas');c.width=4*368*2;c.height=660;const x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
  for(let k=0;k<4;k++)for(let v=0;v<2;v++){const im=await load(out[v][k]);x.drawImage(im,(k*2+v)*368,20);x.fillStyle='#13306b';x.font='12px sans-serif';x.fillText(['trophies','trophies scrolled','treasure book','job info'][k]+(v?' after':' before'),(k*2+v)*368+4,14);}return c.toDataURL();},out);
 fs.writeFileSync('/tmp/audit/menus2_ba.png',Buffer.from(url.split(',')[1],'base64'));console.log('ok');await b.close();})();
