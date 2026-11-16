// node prof.js levelId toolIdx [frames] -> top self-time functions while stepping frames (update+draw)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const [id,ti,fr]=process.argv.slice(2);
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const ctx=await b.newContext({viewport:{width:390,height:844}});const p=await ctx.newPage();if(+(process.env.THROTTLE||1)>1){const c0=await ctx.newCDPSession(p);await c0.send('Emulation.setCPUThrottlingRate',{rate:+process.env.THROTTLE});}
 await p.goto('http://127.0.0.1:8765/'+(process.env.PAGE||'index6.html')+'?test=1');await p.waitForTimeout(800);
 await p.evaluate(([id,ti])=>{const R=window.__SR;window.__HOLD=true;R.save.tut=true;R.save.tool=12;R.save.use=+ti;R.startLevel(R.LEVELS.findIndex(l=>l.id===id));window.__STEP(60,1/30,1);if(R.run)R.run.moved=true;},[id,ti]);
 const cdp=await ctx.newCDPSession(p);await cdp.send('Profiler.enable');await cdp.send('Profiler.setSamplingInterval',{interval:100});await cdp.send('Profiler.start');
 const t=await p.evaluate((fr)=>{const R=window.__SR,P=R.P,G=R.G;const a=performance.now();let up=0,dr=0;for(let k=0;k<fr;k++){P.y=Math.max(30,G.ph*(1-(k%6)/6)-40);const t0=performance.now();window.__STEP(1,1/30,0);const t1=performance.now();window.__STEP(0,1/30,1);up+=t1-t0;dr+=performance.now()-t1;}return {per:(performance.now()-a)/fr,up:up/fr,dr:dr/fr};},+(fr||240));
 const {profile}=await cdp.send('Profiler.stop');const self={};const byId={};for(const n of profile.nodes)byId[n.id]=n;
 const dt={};const samples=profile.samples,deltas=profile.timeDeltas;for(let i=0;i<samples.length;i++){dt[samples[i]]=(dt[samples[i]]||0)+(deltas[i]||0);}
 for(const n of profile.nodes){const k=(n.callFrame.functionName||'(anon)')+':'+n.callFrame.lineNumber;self[k]=(self[k]||0)+(dt[n.id]||0);}
 const tot=Object.values(self).reduce((a,b)=>a+b,0);console.log(id,'ms/frame',t.per.toFixed(2),'update',t.up.toFixed(2),'draw',t.dr.toFixed(2));
 Object.entries(self).sort((a,b)=>b[1]-a[1]).slice(0,18).forEach(([k,v])=>console.log('  ',(v/tot*100).toFixed(1)+'%',k));await b.close();})();
