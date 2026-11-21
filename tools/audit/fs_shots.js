// full-screen layout: real screenshots of every main screen at several phone/tablet shapes (and a notch inset)
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const fs = require('fs');
const FILE = process.argv[2] || 'lab6.html', OUT = process.argv[3] || '/tmp/audit/fs', ONLY = process.argv[4] || '';
fs.mkdirSync(OUT, { recursive: true });
const SHAPES = [['p169', 360, 640, 0, 0], ['ip15', 393, 852, 59, 34], ['and20', 412, 915, 0, 0], ['duo', 1000, 704, 0, 0], ['ipadP', 820, 1180, 24, 20], ['ipadL', 1180, 820, 24, 20]].filter(s => !ONLY || ONLY.split(',').includes(s[0]));
const SCREENS = process.env.SET==='2' ? [
  ['settings', `goMap();settingsOpen=true;`],['book', `goMap();bookOpen=true;bookSel=-1;`],['event', `goMap();evOpen=true;`],['pass', `goMap();passOpen=true;`],
  ['weekly', `goMap();weeklyOpen=true;`],['jobinfo', `goMap();jobInfo=2;`],['trophies', `goMap();trophiesOpen=true;trophyTab=0;`],['skins', `goMap();state='garage';skinFor='shovel';`],['upgrades', `goMap();state='upgrades';`],['privacy', `goMap();save.privSeen=false;`],['pause', `startLevel(3,{});paused=true;`],['got', `goMap();youGot('SNOW BANK',[[SPR.gem,'+260 GEMS','#ff8fc8'],[null,'THE JAR STARTS AGAIN','#9fc0e8']]);`]] : [
  ['title', `state='title';`],
  ['map', `goMap();dailyOpen=false;storyOpen=null;offerOpen=null;remindAsk=null;`],
  ['shop', `goMap();shopOpen=true;shopTab=0;`],
  ['bank', `goMap();save.bank={g:150,seen:true,intro:true};bankOpen=true;`],
  ['upgrades', `goMap();state='upgrades';`],
  ['garage', `goMap();state='garage';`],
  ['job1', `startLevel(0,{});`],
  ['job5', `startLevel(5,{});`],
  ['results', `window.__HOLD=1;startLevel(2,{});G.cleared=Math.round(G.clearable*0.8);run.contUsed=true;run.moved=true;run.time=0.01;update(0.05);window.__HOLD=0;`],
];
(async () => {
  const br = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
  const errs = [];
  for (const [nm, w, h, st, sb] of SHAPES) {
    const ctx = await br.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 }); const p = await ctx.newPage(); p.on('pageerror', e => errs.push(nm + ': ' + e.message));
    await p.goto(`http://127.0.0.1:8766/${FILE}?test=1`); await p.waitForTimeout(800);
    if (st || sb) { await p.addStyleTag({ content: `#wrap{padding:${st}px 0 ${sb}px 0 !important}` }); await p.evaluate(() => window.dispatchEvent(new Event('resize'))); await p.waitForTimeout(300); }
    const EV = c => p.evaluate(x => window.__EV(x), c);
    for (const [sn, setup] of SCREENS) {
      await EV(`(()=>{save.privSeen=true;save.tut=true;save.fbRuns=14;save.sess=4;save.gems=120;save.coins=50000;for(let i=0;i<8;i++){save.best[i]=Math.max(save.best[i]||0,60);save.stars[i]=Math.max(save.stars[i]||0,2);}save.story={suburbs:true,farm:true};try{dailyOpen=false;storyOpen=null;offerOpen=null;evOpen=false;bankOpen=false;passOpen=false;gotCard=null;shopOpen=false;weeklyOpen=false;settingsOpen=false;}catch(e){};${setup}return '1';})()`);
      await p.waitForTimeout(sn === 'title' ? 1900 : sn.startsWith('job')||sn==='pause' ? 3300 : 700);
      await p.screenshot({ path: `${OUT}/${nm}_${sn}.png` });
    }
    const info = await EV(`JSON.stringify({H,SCW,SCH,COX,COY,KS})`); console.log(nm, w + 'x' + h, info);
    await ctx.close();
  }
  console.log('errors', errs.slice(0, 5)); await br.close();
})();
