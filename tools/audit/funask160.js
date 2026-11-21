// p160: the fun question is asked once per day at most (job5 today -> no day2 until a later day)
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ viewport: { width: 360, height: 640 } })).newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/index6.html?test=1'); await p.waitForTimeout(900);
  const EV = c => p.evaluate(x => window.__EV(x), c);
  const r = await EV(`(()=>{const out=[];save.funTest=true;save.privSeen=true;save.tut=true;save.fbRuns=5;save.funAsk1=false;save.funAsk2=false;delete save.funAsk1Day;
    save.day0=new Date(Date.now()-86400e3).toDateString();out.push(funAskDue());
    // answer the first question the way the card's button does
    goMap();for(let k=0;k<3;k++){update(1/30);draw();}drawFunCard(0.016,'job5');const u=ui.find(x=>x.id==='fun4');if(u)u.fn();out.push('pressed:'+!!u);
    out.push(funAskDue());
    save.funAsk1Day=new Date(Date.now()-86400e3).toDateString();out.push(funAskDue());
    return JSON.stringify(out);})()`);
  console.log(r, JSON.stringify(errs.slice(0, 3)));
  const ok = JSON.parse(r); console.log(ok[0] === 'job5' && ok[1] === 'pressed:true' && ok[2] === false && ok[3] === 'day2' ? 'ok   p160 fun question once a day' : 'FAIL p160');
  await b.close();
})();
