// unreachable-snow % for every job x every machine (in-game markReach). node ncsurvey.js [page] out.json
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const page=process.argv[2]||'index6.html',out=process.argv[3]||'/tmp/ncsurvey.json';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await (await b.newContext()).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('http://127.0.0.1:8765/'+page+'?test=1');await p.waitForTimeout(800);
 const r=await p.evaluate(()=>{const R=window.__SR,EV=window.__EV;window.__HOLD=true;R.save.tut=true;const TN=EV('TOOLS.length');const res={};const tids=EV('TOOLS.map(t=>t.id)');
  for(let ti=0;ti<TN;ti++){if(tids[ti]==='ufo')continue;R.save.tool=TN-1;R.save.use=ti;for(let i=0;i<R.LEVELS.length;i++){const L=R.LEVELS[i];if(L.tool||L.area==='secret')continue;R.startLevel(i);const G=EV('G');const n=G.ncN||0,tot=G.clearable+n;(res[L.id]=res[L.id]||{})[tids[ti]]=+(n/tot*100).toFixed(2);}}
  return {res,tids};});
 fs.writeFileSync(out,JSON.stringify(r));const rows=Object.entries(r.res).map(([id,m])=>[id,Math.max(...Object.values(m)),m]).sort((a,c)=>c[1]-a[1]);
 console.log('machines:',r.tids.join(' '));for(const [id,mx,m] of rows.slice(0,30))console.log(id.padEnd(13),mx.toFixed(2).padStart(6),Object.entries(m).filter(([k,v])=>v>=1).map(([k,v])=>k+':'+v).join(' '));
 console.log('jobs with any machine >=1%:',rows.filter(x=>x[1]>=1).length,' >=2%:',rows.filter(x=>x[1]>=2).length,errs.slice(0,2));await b.close();})();
