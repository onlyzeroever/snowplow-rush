const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext()).newPage(); await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(800);
  const r = await p.evaluate(()=>{ window.__HOLD=true; const R=window.__SR,M=window.__MONEY,L=R.LEVELS,out=[]; R.save.tut=true; R.save.tool=7; R.save.story={suburbs:true,farm:true,city:true,themepark:true,harbour:true,ski:true,pass:true,north:true};
    let tot=0,bad=0,want=0,have=0;
    L.forEach((l,i)=>{ M.startLevel(i); const G=R.G; want+=l.presents||0; have+=G.presents.length;
      if((l.presents||0)>0&&G.presents.length<l.presents) out.push(l.id+': wanted '+l.presents+' presents, placed '+G.presents.length);
      for(const pr of G.presents){ tot++; const r={x:pr.x-3,y:pr.y-3,w:6,h:6}; let hit=false; for(const o of G.obstacles) if(r.x<o.x+o.w&&r.x+r.w>o.x&&r.y<o.y+o.h&&r.y+r.h>o.y){hit=true;break;}
        if(!hit&&G.wild){ const ci=(pr.y>>1)*G.cols+(pr.x>>1); if(G.wild[ci]) hit=true; } if(hit){ bad++; out.push(l.id+': present inside something at '+Math.round(pr.x)+','+Math.round(pr.y)); } }
      try{M.endRound(true);}catch(e){} });
    out.unshift('presents total '+tot+' (wanted '+want+'), blocked '+bad); return out; });
  console.log(r.slice(0,40).join('\n')); await b.close(); })();
