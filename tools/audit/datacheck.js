const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs=require('fs');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext()).newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/' + (process.env.PAGE||'index6.html') + '?test=1'); await p.waitForTimeout(900);
  const r = await p.evaluate(() => { const R=window.__SR, A=window.__AUD(), L=R.LEVELS, T=R.TOOLS; const issues=[]; const add=(id,msg)=>issues.push(id+': '+msg);
    const AREA_TOOL={suburbs:0,farm:2,city:3,themepark:4,harbour:5,ski:5,pass:6,north:7};
    const ids=new Set(); const mapPos={};
    const crossSk=new Set(['dragon','sled','car','float','coaster','farm']);
    const rnd=A.srng(1);
    L.forEach((lv,i)=>{ const id=lv.id;
      if(ids.has(id)) add(id,'duplicate id'); ids.add(id);
      for(const f of (lv.from||[])) if(!L.some(x=>x.id===f)) add(id,'from unknown job '+f);
      if(!(lv.stars&&lv.stars[0]<lv.stars[1]&&lv.stars[1]<lv.stars[2])) add(id,'star thresholds not increasing '+JSON.stringify(lv.stars));
      if(!(lv.time>0)) add(id,'bad time '+lv.time);
      const mk=lv.area+'|'+lv.mx+'|'+lv.my; if(lv.area!=='secret'){ if(mapPos[mk]) add(id,'same map position as '+mapPos[mk]); mapPos[mk]=id; }
      const D=lv.data;
      if(D){
        if(D.h!=null&&D.h!==lv.h) add(id,'data.h '+D.h+' != h '+lv.h);
        for(const g of D.ground||[]) if(A.GROUND_T[g[0]]==null) add(id,'unknown ground '+g[0]);
        for(const c of D.circles||[]) if(A.GROUND_T[c[0]]==null) add(id,'unknown circle ground '+c[0]);
        for(const pth of D.paths||[]){const nm=pth[0][0]==='~'?pth[0].slice(1):pth[0]; if(A.GROUND_T[nm]==null) add(id,'unknown path ground '+nm);}
        for(const pr of D.props||[]){ if(!A.PROPS[pr[0]]) add(id,'unknown prop '+pr[0]); else if(pr[1]<-40||pr[1]>200||pr[2]<-120||pr[2]>lv.h+20) add(id,'prop off-map '+JSON.stringify(pr)); }
        for(const pr of D.scen||[]) if(!A.PROPS[pr[0]]) add(id,'unknown scen prop '+pr[0]);
        for(const pr of D.over||[]) if(!A.OVERS[pr[0]]) add(id,'unknown overlay '+pr[0]);
        for(const w of D.wilds||[]){ let ok=false; try{ ok=!!A.wildSpr(w[0],A.srng(3)); }catch(e){} if(!ok) add(id,'wild kind draws nothing: '+w[0]); }
        for(const h of D.hazards||[]){ const H=A.HAZ[h[0]]; if(!H){ add(id,'unknown hazard '+h[0]); continue; }
          if(H.chaser&&h[3]&&!A.CHASERS[h[3]]) add(id,'unknown chaser skin '+h[3]);
          if(H.cross&&h[5]&&!crossSk.has(h[5])) add(id,'unknown cross skin '+h[5]);
          if(!H.spawner&&!H.skier&&!H.cross&&h[0]!=='taxi'&&(h[1]<-20||h[1]>200||h[2]<-60||h[2]>lv.h+20)) add(id,'hazard off-map '+JSON.stringify(h)); }
        if(D.start&&(D.start[0]<4||D.start[0]>176||D.start[1]<4||D.start[1]>lv.h-4)) add(id,'start off-map '+D.start);
      }
      let g; try{ g=R._t.buildLevel(i); }catch(e){ add(id,'BUILD CRASH '+e.message); return; }
      const s=g.start, sr={x:s.x-6,y:s.y-6,w:12,h:12};
      for(const o of g.obstacles) if(sr.x<o.x+o.w&&sr.x+sr.w>o.x&&sr.y<o.y+o.h&&sr.y+sr.h>o.y){ add(id,'start overlaps an obstacle at '+o.x+','+o.y); break; }
      if(g.wild){ const ci=(Math.floor(s.y/2))*g.cols+Math.floor(s.x/2); if(g.wild[ci]) add(id,'start inside wild/blocked area'); }
      for(const nb of g.neighbours) for(const rc of nb.rects) if(rc[0]<0||rc[0]+rc[2]>180||rc[1]<0||rc[1]+rc[3]>lv.h) add(id,'neighbour rect off-map');
      if(lv.area!=='secret'){ const ti=lv.tool?T.findIndex(t=>t.id===lv.tool):AREA_TOOL[lv.area]; if(ti==null||ti<0){ add(id,'no tool for area '+lv.area); return; }
        try{ const c0=R.checkJob(i,ti,0,0), c5=R.checkJob(i,ti,5,5);
          if(c0.reach<90) add(id,'only '+c0.reach+'% of snow reachable with '+T[ti].id+' (lv0)');
          if(c5.reach<90) add(id,'only '+c5.reach+'% reachable with '+T[ti].id+' (lv5)');if(c5.d>1.25) add(id,'3 stars very hard even fully upgraded: d='+c5.d+' ('+c5.verdict+')');
          if(c5.verdict&&/IMPOSSIBLE|TOO HARD/i.test(c5.verdict)) add(id,'checker verdict at lv5: '+c5.verdict);
        }catch(e){ add(id,'checkJob crash '+e.message); } }
    });
    return issues; });
  fs.writeFileSync('/tmp/audit/datacheck.txt', r.join('\n')); console.log(r.length+' issues'); console.log(r.join('\n')); console.log('page errors', JSON.stringify(errs)); await b.close(); })();
