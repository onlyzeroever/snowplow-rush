// How cramped each job is for each machine: of the places a machine's body fits, the share where it sits within 3px of
// a prop (a likely bump). Also lists the props that make the most tight spots, per job, for the given machine.
// node squeeze.js [machines=blower,truck,super,loader] [jobs=all base jobs] [focusMachine=truck]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const machines = (process.argv[2] || 'blower,truck,super,loader').split(','), jobsArg = process.argv[3] || '', focus = process.argv[4] || 'truck';
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] }); const p = await (await b.newContext()).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(800);
  const r = await p.evaluate(([machines, jobsArg, focus]) => window.__EV(`(()=>{const out={},M=${JSON.stringify(machines)},FOCUS=${JSON.stringify(focus)},want=${JSON.stringify(jobsArg)}.split(',').filter(Boolean);
    LEVELS.forEach((L,i)=>{if(L.tool||L.area==='secret'||(want.length&&!want.includes(L.id)))return;const g=buildLevel(i);const keep=G;G=g;const row={area:L.area};
      for(const tid of M){let free=0,tight=0;const per=new Map();for(let y=8;y<g.ph-8;y+=4)for(let x=4;x<g.pw-4;x+=4)for(const f of [0,1]){const fp=footprint(tid,x,y,f);if(blockedBy(fp))continue;free++;
        G.lastOb=null;const big={x:fp.x-3,y:fp.y-3,w:fp.w+6,h:fp.h+6};if(big.x<0||big.y<0||big.x+big.w>g.pw||big.y+big.h>g.ph){}else if(blockedBy(big)==='ob'){tight++;if(tid===FOCUS&&G.lastOb){const o=G.lastOb,k=o.x+','+o.y+','+o.w+','+o.h;per.set(k,(per.get(k)||0)+1);}}}
        row[tid]=+(tight/Math.max(1,free)*100).toFixed(1);if(tid===FOCUS)row.top=[...per.entries()].sort((a,c)=>c[1]-a[1]).slice(0,6).map(([k,n])=>k+' x'+n);}
      G=keep;out[L.id]=row;});return JSON.stringify(out);})()`), [machines, jobsArg, focus]);
  const res = JSON.parse(r); fs.writeFileSync('/tmp/squeeze.json', JSON.stringify(res, null, 1));
  const rows = Object.entries(res).sort((a, c) => (c[1][focus] - c[1].blower) - (a[1][focus] - a[1].blower));
  console.log('job'.padEnd(13), 'area'.padEnd(10), machines.map(m => m.padStart(7)).join(''), '  most tight spots for', focus);
  for (const [id, row] of rows) console.log(id.padEnd(13), row.area.padEnd(10), machines.map(m => String(row[m]).padStart(7)).join(''), '  ', (row.top || []).slice(0, 3).join(' | '));
  console.log('errors', JSON.stringify(errs)); await b.close(); })();
