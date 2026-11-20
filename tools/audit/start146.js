// Start check (Alex, Nov 20: "you spawn in front of a pole so you crash as soon as you start"): for every job and
// the machines that play it, the machine's body at the start must be clear of props, and it must be able to drive
// 24px straight up and 24px straight down (or reach the map edge) without hitting anything.
//   node tools/audit/start146.js [out.json] [page=index6.html] [port=8765]
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const out = process.argv[2] || '/tmp/start146.json', page = process.argv[3] || 'index6.html', port = process.argv[4] || 8765;
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:' + port + '/' + page + '?test=1'); await p.waitForTimeout(900);
  const r = await p.evaluate(() => window.__EV(`(()=>{save.privSeen=true;save.tut=true;window.__HOLD=1;const ENTRY={suburbs:'shovel',farm:'tractor',city:'truck',themepark:'super',harbour:'loader',ski:'snowcat',pass:'rotary',north:'rotary'};
    const out=[];for(let i=0;i<LEVELS.length;i++){const L=LEVELS[i];const ms=L.tool?[L.tool]:[...new Set([ENTRY[L.area]||'truck','rotary','icebreaker','monster'])];
      const g=buildLevel(i);const G0=G;G=g;const sx=g.start.x,sy=g.start.y;
      for(const m of ms){const hits=[];const hitAt=(f,x,y)=>{const fp=footprint(m,x,y,f);for(const o of g.obstacles)if(overlap(fp,o))return o;return null;};
        const fw=sy<g.ph/2?2:0;for(const f of [0,2]){const o=hitAt(f,sx,sy);if(o){hits.push({at:'start',f,ob:[Math.round(o.x),Math.round(o.y),o.w,o.h]});continue;}if(f!==fw)continue;
          for(let d=2;d<=16;d+=2){const y=sy+(f===0?-d:d);const fp=footprint(m,sx,y,f);if(fp.y<0||fp.y+fp.h>g.ph)break;const o2=hitAt(f,sx,y);if(o2){hits.push({at:(f===0?'up ':'down ')+d+'px',f,ob:[Math.round(o2.x),Math.round(o2.y),o2.w,o2.h]});break;}}}
        if(hits.length)out.push({id:L.id,m,start:[sx,sy],hits});}
      G=G0;}
    return JSON.stringify(out);})()`));
  const res = JSON.parse(r); fs.writeFileSync(out, JSON.stringify(res, null, 1));
  for (const o of res) console.log(o.id, o.m, JSON.stringify(o.start), JSON.stringify(o.hits));
  console.log(res.length + ' job/machine starts with a prop in the way', 'errors', errs.slice(0, 3)); await b.close();
})();
