const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const OUT=process.env.OUTDIR||'/tmp/screens';fs.mkdirSync(OUT,{recursive:true});
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx=await b.newContext({viewport:{width:360,height:640}});const p = await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'index6.html')+'?test=1'); await p.waitForTimeout(900);
  const shot=async(name)=>{await p.evaluate(async()=>{await new Promise(r=>requestAnimationFrame(()=>r()));window.__STEP(9,1/30,0);await new Promise(r=>requestAnimationFrame(()=>r()));window.__STEP(9,1/30,0);await new Promise(r=>requestAnimationFrame(()=>r()));await new Promise(r=>requestAnimationFrame(()=>r()));});
    const u=await p.evaluate(()=>document.querySelector('canvas').toDataURL());fs.writeFileSync(OUT+'/'+name+'.png',Buffer.from(u.split(',')[1],'base64'));};
  await shot('00_title');
  await p.evaluate(()=>{const R=window.__SR;window.__HOLD=true;R.save.tut=true;R.save.privSeen=true;R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};R.save.coins=1234567;R.save.gems=140;R.save.tool=5;R.save.use=5;R.save.lv.helpers=3;for(let i=0;i<30;i++){R.save.stars[i]=1+(i%3);R.save.best[i]=70;}R.save.streak={n:3,last:-9,savers:1,best:3};R.goMap();R.dailyOpen=false;});
  const P=async(id)=>p.evaluate((id)=>window.__UI.press(id),id);
  const reset=async()=>p.evaluate(()=>{const R=window.__SR;R.dailyOpen=false;R.weeklyOpen=false;R.trophiesOpen=false;R.jobInfo=-1;try{R.goMap();}catch(e){}R.dailyOpen=false;for(let k=0;k<5;k++){window.__STEP(1,1/30,0);const l=window.__UI.list();const c=['sok','sclose','dclose','tclose','bkclose','wkclose','close','wok','ofclose','trclose','skclose'].find(x=>l.includes(x));if(!c)break;window.__UI.press(c);}R.dailyOpen=false;});
  await shot('01_map');
  for(const id of ['daily','trophies','gear','book','weekly','winfo','vlist']){await reset();await shot('_tmp');const ok=await P(id);await shot('02_map_'+id+(ok?'':'_MISSING'));}
  await reset();await p.evaluate(()=>{window.__SR.jobInfo=6;});await shot('03_jobinfo');
  await reset();await p.evaluate(()=>window.__SR.goGarage());await shot('04_garage');
  for(const id of ['sk0','outfits','trails']){await reset();await p.evaluate(()=>window.__SR.goGarage());await shot('_tmp');const ok=await P(id);await shot('05_garage_'+id+(ok?'':'_MISSING'));}
  await reset();await p.evaluate(()=>window.__SR.goUpgrades());await shot('06_upgrades');
  await reset();await p.evaluate(()=>window.__SR.openShop());await shot('07_shop_offers');await P('stab1');await shot('07_shop_coins');await P('sclose');
  await reset();await p.evaluate(()=>{const R=window.__SR;R.startLevel(6);window.__STEP(90,1/30,0);});await shot('08_play');
  await P('pause');await shot('09_pause');
  await p.evaluate(()=>{const R=window.__SR;window.__UI.press('resume');R.G.cleared=R.G.clearable*0.97;window.__MONEY.endRound(true);window.__STEP(130,1/30,0);});await shot('10_results_allclear');
  await reset();await p.evaluate(()=>{const R=window.__SR;R.startLevel(7);window.__STEP(60,1/30,0);R.G.cleared=R.G.clearable*0.31;window.__MONEY.endRound(false);window.__STEP(130,1/30,0);});await shot('11_results_soclose');
  await reset();await p.evaluate(()=>{const R=window.__SR;R.startLevel(8);window.__STEP(60,1/30,0);R.G.cleared=R.G.clearable*0.1;window.__MONEY.endRound(false);window.__STEP(130,1/30,0);});await shot('12_results_fail');
  await p.evaluate(()=>{window.__UI.press('rad');});await shot('13_adscreen');
  console.log('errs',errs);await b.close();})();
