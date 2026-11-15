const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext()).newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/' + (process.env.PAGE||'index6.html') + '?test=1'); await p.waitForTimeout(900);
  const url = await p.evaluate(() => { const C=window.__CAST(); const rows=[]; for(const k of Object.keys(C)){ if(k==='chasers'){ for(const [n,fr] of Object.entries(C.chasers)) rows.push(['chaser:'+n,fr]); } else rows.push([k,C[k]]); }
    const S=5, CW=150, CH=150, cols=8; const cells=[]; rows.forEach(([n,arr])=>arr.forEach((sp,i)=>cells.push([n+(arr.length>1?' '+i:''),sp])));
    const c=document.createElement('canvas'); c.width=cols*CW; c.height=Math.ceil(cells.length/cols)*CH; const x=c.getContext('2d'); x.imageSmoothingEnabled=false;
    cells.forEach(([n,sp],k)=>{ const cx=(k%cols)*CW, cy=Math.floor(k/cols)*CH; x.fillStyle=(k+Math.floor(k/cols))%2?'#e3edf8':'#f2f7fc'; x.fillRect(cx,cy,CW,CH);
      if(sp&&sp.width){ const sc=Math.max(1,Math.min(S,Math.floor(Math.min((CW-12)/sp.width,(CH-26)/sp.height)))); x.drawImage(sp,Math.round(cx+(CW-sp.width*sc)/2),Math.round(cy+20+(CH-22-sp.height*sc)/2),sp.width*sc,sp.height*sc); }
      x.fillStyle='#13306b'; x.font='bold 12px sans-serif'; x.fillText(n+(sp&&sp.width?'  '+sp.width+'x'+sp.height:''),cx+4,cy+14); });
    return c.toDataURL(); });
  fs.writeFileSync(process.env.OUT||'/tmp/audit/cast.png', Buffer.from(url.split(',')[1],'base64')); console.log('errors',JSON.stringify(errs)); await b.close(); })();
