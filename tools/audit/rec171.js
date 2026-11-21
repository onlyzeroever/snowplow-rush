// p171 (held, lab): app recordings only for 1 in 4 new players, first visit, Wi-Fi, consent; web unchanged
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const res = []; const ok = (n, pass, info) => { res.push(pass); console.log((pass ? 'ok   ' : 'FAIL ') + n + (info !== undefined ? ' ' + JSON.stringify(info) : '')); };
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/lab6.html?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c).then(JSON.parse);
  const r = await EV(`(()=>{const out={};delete window.SRNative;save.recDraw=null;out.web=recAppOK();
    window.SRNative={platform:'ios',network:'wifi'};let yes=0;for(let k=0;k<400;k++){save.recDraw=null;save.phRec=0;if(recAppOK())yes++;}out.share=yes/400;
    save.recDraw=true;save.phRec=0;out.wifi=recAppOK();window.SRNative.network='cellular';out.cell=recAppOK();window.SRNative.network=()=> 'wifi';out.fnwifi=recAppOK();
    save.phRec=1;out.second=recAppOK();save.phRec=0;window.SRNative.recordOK=()=>false;out.noConsent=recAppOK();delete window.SRNative;
    out.src=String(phRecStart).includes('APP?1:2')&&String(phRecStart).includes('(APP?10:20)*60e3');return JSON.stringify(out);})()`);
  ok('web unchanged', r.web === true, r);
  ok('about 1 in 4 app installs drawn', r.share > 0.17 && r.share < 0.33, r.share);
  ok('Wi-Fi yes, mobile data no (value or function)', r.wifi && !r.cell && r.fnwifi, r);
  ok('first visit only', r.second === false, r);
  ok('never without consent', r.noConsent === false, r);
  ok('1 fps and 10 minutes in the app', r.src, r.src);
  ok('no page errors', errs.length === 0, errs.slice(0, 2));
  console.log(res.every(Boolean) ? 'ALL OK' : 'SOME FAILED'); await b.close();
})();
