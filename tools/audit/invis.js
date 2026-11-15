const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext()).newPage(); await p.goto('http://127.0.0.1:8765/' + (process.env.PAGE||'index6.html') + '?test=1'); await p.waitForTimeout(800);
  const r = await p.evaluate(() => { const R=window.__SR, L=R.LEVELS; const cache=new Map(); const out=[];
    const alpha=(c)=>{ let a=cache.get(c); if(!a){ const g=c.getContext('2d'); a=g.getImageData(0,0,c.width,c.height).data; cache.set(c,a); } return a; };
    L.forEach((lv,i)=>{ let g; try{ g=R._t.buildLevel(i); }catch(e){ out.push(lv.id+' build error'); return; }
      const seen={};
      for(const o of g.obstacles){ if(!o.spr||!o.spr.width||o.w*o.h<40) continue; const A=alpha(o.spr), W=o.spr.width, H=o.spr.height; let op=0, out_=0;
        for(let y=o.y;y<o.y+o.h;y++) for(let x=o.x;x<o.x+o.w;x++){ const sx=x-o.sx, sy=y-(o.sy); if(sx<0||sy<0||sx>=W||sy>=H){ out_++; continue; } if(A[(sy*W+sx)*4+3]>20) op++; }
        const area=o.w*o.h, cov=op/area; if(cov<0.3){ const key=W+'x'+H+'@'+o.w+'x'+o.h; if(seen[key]) continue; seen[key]=1; out.push(lv.id+': collision '+o.w+'x'+o.h+' at '+o.x+','+o.y+' only '+Math.round(cov*100)+'% covered by its picture ('+W+'x'+H+')'+(out_?' ['+out_+'px outside picture]':'')); } } });
    return out; });
  fs.writeFileSync('/tmp/audit/invis.txt', r.join('\n')); console.log(r.length); console.log(r.slice(0,60).join('\n')); await b.close(); })();
