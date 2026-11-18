// Heat map of tight spots for one machine: red where its body fits but sits within 3px of a prop.
// node squeezemap.js job1,job2 machine out.png
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const ids = process.argv[2].split(','), tid = process.argv[3] || 'truck', out = process.argv[4] || '/tmp/squeezemap.png';
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] }); const p = await (await b.newContext()).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/index6.html?test=1'); await p.waitForTimeout(800);
  const url = await p.evaluate(([ids, tid]) => window.__EV(`(()=>{const ids=${JSON.stringify(ids)},tid=${JSON.stringify(tid)},imgs=[];
    for(const id of ids){const i=lvIdx(id),g=buildLevel(i),keep=G;G=g;const c=mk(g.pw,g.ph),x=c.getContext('2d');x.drawImage(g.canvas,0,0);
      for(const o of g.obstacles){if(o.spr)x.drawImage(o.spr,o.sx,o.sy);x.strokeStyle='rgba(0,0,255,0.7)';x.strokeRect(o.x+0.5,o.y+0.5,o.w-1,o.h-1);}
      for(let y=8;y<g.ph-8;y+=4)for(let xx=4;xx<g.pw-4;xx+=4){let t=0,fr=0;for(const f of [0,1]){const fp=footprint(tid,xx,y,f);if(blockedBy(fp))continue;fr++;const big={x:fp.x-3,y:fp.y-3,w:fp.w+6,h:fp.h+6};if(blockedBy(big)==='ob')t++;}
        if(fr){x.fillStyle=t?(t===fr?'rgba(255,0,0,0.75)':'rgba(255,140,0,0.6)'):'rgba(0,200,0,0.25)';x.fillRect(xx-1,y-1,3,3);}}
      G=keep;imgs.push([id,c]);}
    const H=Math.max(...imgs.map(a=>a[1].height)),S=mk(imgs.length*190,H+12),s=S.getContext('2d');s.fillStyle='#222';s.fillRect(0,0,S.width,S.height);
    imgs.forEach(([id,c],k)=>{s.drawImage(c,k*190,12);text(s,id.toUpperCase(),k*190+4,2,'#ffffff',{outline:null});});return S.toDataURL();})()`), [ids, tid]);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64')); console.log('wrote', out, 'errors', JSON.stringify(errs)); await b.close(); })();
