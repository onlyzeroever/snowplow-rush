// screenshots of the map screen as a new player and as a regular, on a 390x844 phone
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const file = process.argv[2] || 'index6_ship.html', tag = process.argv[3] || 'live';
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  for (const [name, setup] of [
    ['new', `save.privSeen=true;save.tut=true;save.fbRuns=1;save.best[0]=62;save.stars[0]=2;save.lastJob='driveway';`],
    ['regular', `save.privSeen=true;save.tut=true;save.fbRuns=14;save.best[0]=100;save.best[1]=90;save.best[2]=88;save.stars[0]=3;save.stars[1]=3;save.stars[2]=3;save.coins=4200;save.gems=35;`]]) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
    await p.goto(`http://127.0.0.1:8766/${file}?test=1`); await p.waitForTimeout(1000);
    await p.evaluate(c => window.__EV(c), `(()=>{${setup}save.story=Object.assign(save.story||{},{suburbs:true});persist();goMap();try{dailyOpen=false;storyOpen=null;offerOpen=null;}catch(e){}return '1';})()`);
    await p.evaluate(c => window.__EV(c), `(()=>{try{dailyOpen=false;storyOpen=null;offerOpen=null;}catch(e){}return '1';})()`);await p.waitForTimeout(700);
    await p.screenshot({ path: `/tmp/audit/map_${tag}_${name}.png` });
    const ui = await p.evaluate(c => window.__EV(c), `JSON.stringify((typeof ui!=='undefined'?ui:[]).map(u=>[u.id,u.x,u.y,u.w,u.h]).filter(u=>u[2]>250))`);
    console.log(name, ui, errs.slice(0, 2));
    await ctx.close();
  }
  await b.close();
})();
