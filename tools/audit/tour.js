const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
const AREA_TOOL={suburbs:[0,2],farm:[2,3],city:[3,4],themepark:[4,5],harbour:[5,6],ski:[5,6],pass:[6,7],north:[7,7]};
const TN=['shovel','pusher','blower','tractor','truck','super','snowcat','rotary','monster','jet','mech','dragon','ufo'];
async function one(browser, id, ti) {
  const errors=[]; const ctx=await browser.newContext({ viewport:{width:360,height:640} }); const page=await ctx.newPage();
  page.on('pageerror',e=>errors.push('PAGE '+e.message)); page.on('console',m=>{ if(m.type()==='error') errors.push('CONSOLE '+m.text().slice(0,240)); });
  await page.goto('http://127.0.0.1:8765/index6.html?test=1'); await page.waitForTimeout(500);
  const r = await page.evaluate(([id,ti])=>{ window.__HOLD=true; const R=window.__SR, i=R.LEVELS.findIndex(L=>L.id===id);
    R.save.tut=true; R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true}; R.save.tool=Math.max(R.save.tool,ti); R.save.use=ti; R.startLevel(i);
    const out={visited:0,errs:[]}; const step=(n)=>{ try{ window.__STEP(n,1/30,1); }catch(e){ out.errs.push(String(e&&e.stack||e).slice(0,300)); } };
    step(100); const G=R.G, P=R.P, tid=R.TOOLS[ti].id, K=R.keys, dirs=['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'];
    let rs=7; const rnd=()=>{ rs=(rs*1103515245+12345)&0x7fffffff; return rs/0x7fffffff; };
    const ys=[];for(let y=20;y<G.ph-10;y+=36)ys.push(y);ys.sort((a,b)=>Math.abs(a-G.start.y)-Math.abs(b-G.start.y));for(const y of ys){ let placed=false; for(let tries=0;tries<30&&!placed;tries++){ const x=10+rnd()*160; const fp=R.fp(tid,x,y,0); if(!R.blk(fp)){ P.x=x; P.y=y; placed=true; } }
      if(!placed) continue; out.visited++;
      for(let s=0;s<3;s++){ for(const d of dirs) K[d]=false; K[dirs[Math.floor(rnd()*4)]]=true; step(8); }
      if(R.run&&R.run.ended) break; }
    for(const d of dirs) K[d]=false; out.pct=+(G.cleared/G.clearable*100).toFixed(1); out.hz=G.hazards.length;
    try{ window.__MONEY.endRound(true); }catch(e){ out.errs.push('endRound '+String(e).slice(0,200)); } step(200);
    try{ R.goHome(); }catch(e){ out.errs.push('goHome '+String(e).slice(0,200)); } step(30); return out; },[id,ti]);
  const line=id+' '+TN[ti]+' '+JSON.stringify(r)+' errors '+JSON.stringify(errors.slice(0,4)); fs.appendFileSync(process.env.OUT||'/tmp/audit/tour.txt', line+'\n'); console.log(line); await ctx.close(); }
(async () => { const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p0=await (await browser.newContext()).newPage(); await p0.goto('http://127.0.0.1:8765/index6.html?test=1'); await p0.waitForTimeout(500);
  const all=await p0.evaluate(()=>window.__SR.LEVELS.map(l=>[l.id,l.area,l.tool||null])); await p0.context().close();
  const sel=process.argv[2]==='all'?all:all.filter(a=>process.argv[2].split(',').includes(a[0]));
  const jobs=[]; for(const [id,area,tool] of sel){ if(tool) jobs.push([id,TN.indexOf(tool)]); else for(const t of new Set(AREA_TOOL[area]||[3])) jobs.push([id,t]); }
  if(process.env.ALLRIDES) for(const [id,area] of sel.filter(a=>a[1]!=='secret').slice(0,+process.env.ALLRIDES)) for(const t of [8,9,10,11,12]) jobs.push([id,t]);
  const q=jobs.slice(); const W=[]; for(let w=0;w<(+process.argv[3]||4);w++) W.push((async()=>{ while(q.length){ const [id,t]=q.shift(); await one(browser,id,t); } })());
  await Promise.all(W); await browser.close(); })();
