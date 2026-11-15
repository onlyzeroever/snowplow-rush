const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const ZOO={
 A:[['ped',20,330],['pedx',150,300],['thrower',130,190],['chaser',30,170,'grimshaw',6],['skier',70,0,3,1],['cross',0,250,-1,3],['dog',84,350],['cart',40,230]],
 B:[['cow',30,330],['sheep',110,300,3],['peng',60,220,3],['gull',60,260,3],['taxi',60,-60,2],['forklift',130,170,0],['bumper',30,170,4]],
 C:[['balls',165,330,-1,3],['cannon',2,280,0.35,6.5,70],['barrier',60,200,60,3],['orbit',90,240,40,0.6],['ghost',40,350,0],['rockfall',90,0,3,0],['sled',0,0,[1,2]]]};
const RUNS=(process.env.RUNS||'A:suburbs,A:farm,A:ski,A:north,B:farm,B:harbour,B:north,C:themepark,C:city,C:ski').split(',');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 }); const p = await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/' + (process.env.PAGE||'index6.html') + '?test=1'); await p.waitForTimeout(900);
  for (const run of RUNS) { const [z,area]=run.split(':');
    const ground = area==='ski'||area==='north'||area==='pass' ? 'piste' : area==='city'||area==='harbour'?'asph':area==='themepark'?'pave':'grass';
    const def={id:'zoo',name:'ZOO',area,h:420,time:90,value:1,stars:[35,60,85],snowfall:20,presents:0,squall:0,ground:[[ground,0,0,180,420]],props:[],hazards:ZOO[z],start:[90,400]};
    await p.evaluate((def)=>{ window.__SR.testLevel(def,0); }, def); await p.waitForTimeout(300); await p.keyboard.down('ArrowLeft'); await p.waitForTimeout(60); await p.keyboard.up('ArrowLeft'); await p.waitForTimeout(+(process.env.WAIT||2600));
    await p.screenshot({ path: '/tmp/audit/zoo_'+z+'_'+area+'.png', clip:{x:0,y:122,width:390,height:560} });
  }
  console.log('errors', JSON.stringify(errs)); await b.close(); })();
