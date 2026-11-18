// Pinch points: places a machine's body fits but with under 4px to spare on BOTH sides (squeezing between two props, or a
// prop and the edge). These are where big machines bump. Lists the gaps (pairs of props) that pinch most, per job.
// node squeeze.js [machines=blower,truck,super,loader] [jobs=all base jobs] [focusMachine=truck]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const machines = (process.argv[2] || 'blower,truck,super,loader').split(','), jobsArg = process.argv[3] || '', focus = process.argv[4] || 'truck', areas = (process.env.AREAS || '').split(',').filter(Boolean);
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] }); const p = await (await b.newContext()).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(800);
  const r = await p.evaluate(([machines, jobsArg, focus, areas]) => window.__EV(`(()=>{const out={},M=${JSON.stringify(machines)},FOCUS=${JSON.stringify(focus)},want=${JSON.stringify(jobsArg)}.split(',').filter(Boolean),AR=${JSON.stringify(areas)};
    LEVELS.forEach((L,i)=>{if(L.tool||L.area==='secret'||(want.length&&!want.includes(L.id))||(AR.length&&!AR.includes(L.area)))return;const g=buildLevel(i);const keep=G;G=g;const row={area:L.area};
      for(const tid of M){let free=0,tight=0;const per=new Map();const blk=r=>{G.lastOb=null;const b=blockedBy(r);return b?(b==='ob'&&G.lastOb?'o'+G.lastOb.x+','+G.lastOb.y+','+G.lastOb.w+','+G.lastOb.h:'edge'):null;};for(let y=8;y<g.ph-8;y+=4)for(let x=4;x<g.pw-4;x+=4)for(const f of [0,1]){const fp=footprint(tid,x,y,f);if(blockedBy(fp))continue;free++;const a=f===0?blk({x:fp.x-4,y:fp.y+2,w:4,h:fp.h-4}):blk({x:fp.x+2,y:fp.y-4,w:fp.w-4,h:4}),c=a&&(f===0?blk({x:fp.x+fp.w,y:fp.y+2,w:4,h:fp.h-4}):blk({x:fp.x+2,y:fp.y+fp.h,w:fp.w-4,h:4}));if(a&&c&&!(a==='edge'&&c==='edge')){tight++;if(tid===FOCUS){const k=[a,c].sort().join(' + ');per.set(k,(per.get(k)||0)+1);}}}row[tid]=+(tight/Math.max(1,free)*100).toFixed(1);if(tid===FOCUS)row.top=[...per.entries()].sort((p,q)=>q[1]-p[1]).slice(0,6).map(([k,n])=>k+' x'+n);}G=keep;out[L.id]=row;});return JSON.stringify(out);})()`), [machines, jobsArg, focus, areas]);
  const res = JSON.parse(r); fs.writeFileSync('/tmp/pinch.json', JSON.stringify(res, null, 1));
  const rows = Object.entries(res).sort((a, c) => (c[1][focus] - c[1].blower) - (a[1][focus] - a[1].blower));
  console.log('job'.padEnd(13), 'area'.padEnd(10), machines.map(m => m.padStart(7)).join(''), '  most tight spots for', focus);
  for (const [id, row] of rows) console.log(id.padEnd(13), row.area.padEnd(10), machines.map(m => String(row[m]).padStart(7)).join(''), '  ', (row.top || []).slice(0, 3).join(' | '));
  console.log('errors', JSON.stringify(errs)); await b.close(); })();
